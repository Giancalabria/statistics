"""Resolver: Analisis (ya revisado por el usuario) -> cálculos con el solver.

Cada inciso devuelve un `Resultado` con los pasos en el formato de la cátedra
(planteo, hipótesis, distribución, valor crítico, regla de decisión, conclusión)
para que se pueda copiar la presentación. Toda la matemática la hace `solver/`.
"""

from dataclasses import dataclass, field
from math import sqrt
from typing import Any, Dict, List, Optional

from solver import chi_square as chi
from solver import distributions as dist
from solver import hypothesis_one as hyp
from solver import intervals as ic
from solver import two_samples as two
from solver import wording
from solver.muestra import resumen_muestra

from .modelo import Analisis, Inciso
from .presentacion import agregar_presentacion, siete_pasos
from .texto import fmt


@dataclass
class Resultado:
    titulo: str = ""
    pasos: List[str] = field(default_factory=list)      # markdown, en orden de presentación
    conclusion: str = ""
    regla: str = ""                                       # regla de decisión en lenguaje llano (paso 5)
    resumen: str = ""                                     # una línea (para listados / evaluación)
    numeros: List[float] = field(default_factory=list)   # valores clave (para comparar con la guía)
    tabla: Optional[List[Dict[str, Any]]] = None          # curvas OC / potencia
    avisos: List[str] = field(default_factory=list)
    errores: List[str] = field(default_factory=list)


class FaltaDato(Exception):
    pass


def _req(d: Dict, *claves):
    faltan = [k for k in claves if d.get(k) in (None, "", [])]
    if faltan:
        raise FaltaDato("Falta cargar: " + ", ".join(faltan))
    return [d[k] for k in claves]


def _pct(alpha: float) -> str:
    return fmt((1 - alpha) * 100, 2) + "%"


def _p(param: str, a: float, b: float, alpha: float) -> str:
    """Notación de la cátedra: P(A ≤ θ ≤ B) = 1-α."""
    return f"P({fmt(a, 4)} ≤ {param} ≤ {fmt(b, 4)}) = {fmt(1 - alpha, 4)}"


def _acciones(d: Dict, h1: str):
    """Qué se hace si se rechaza / si no se rechaza H0 (las del sistema de control, si las hay)."""
    return (d.get("accion_rechazo") or f"se da por probado que {h1}",
            d.get("accion_no_rechazo") or f"no se puede afirmar que {h1}")


def _ensayo_txt(r, alpha: float, obs: str, d: Optional[Dict] = None) -> str:
    """Conclusión formal (paso 7): nivel de significación + evidencia + acción que se sigue."""
    d = d or {}
    return _coma(wording.conclusion_formal(alpha, r.rejects_h0, f"H0: {r.h0_text}", r.h1_text, obs,
                                           d.get("accion_rechazo"), d.get("accion_no_rechazo")))


def _regla(d: Dict, que: str, cond: str, h1: str) -> str:
    """Regla de decisión (paso 5) en lenguaje llano, antes de mirar el dato muestral."""
    si, no = _acciones(d, _coma(h1))
    return _coma(f"Se {que}. Si {cond}, se rechaza H0 → {si}. En caso contrario no se rechaza H0 → {no}.")


def _coma(texto: str) -> str:
    """Los textos del solver usan punto decimal ('37.5698'): se pasan a coma."""
    import re
    texto = re.sub(r"(\d)\.(\d)", r"\1,\2", texto)
    return re.sub(r"(\d),0(?![\d,])", r"\1", texto)  # 500,0 -> 500


def _cv(v) -> str:
    if isinstance(v, tuple):
        return " ; ".join(fmt(x, 4) for x in v)
    return fmt(v, 4)


# ---------------------------------------------------------------------------
# Datos efectivos (planteo + inciso + resultados de incisos anteriores)
# ---------------------------------------------------------------------------

def _datos(an: Analisis, inc: Inciso, estado: Dict) -> Dict:
    d = dict(an.datos)
    for k, v in inc.params.items():
        if v is not None:
            d[k] = v
    if d.get("datos") and len(d["datos"]) >= 2:
        r = resumen_muestra(list(d["datos"]))
        d.setdefault("n", r.n)
        d.setdefault("xbar", r.xbar)
        if d.get("desvio") in (None, "") or d.get("usar_S"):
            d["desvio"] = r.s
            d["sigma_conocido"] = False
        d["_resumen"] = r
    elif d.get("usar_S"):
        d["sigma_conocido"] = False
    for lado in ("1", "2"):
        lista = d.get("datos" + lado)
        if lista and len(lista) >= 2:
            r = resumen_muestra(list(lista))
            d.setdefault("n" + lado, r.n)
            d.setdefault("xbar" + lado, r.xbar)
            d.setdefault("s" + lado, r.s)
    if "n" not in d and estado.get("n"):
        d["n"] = estado["n"]
    if d.get("p_hat") is None and d.get("r") is not None and d.get("n"):
        d["p_hat"] = d["r"] / d["n"]
    if d.get("r") is None and d.get("p_hat") is not None and d.get("n"):
        d["r"] = int(round(d["p_hat"] * d["n"]))
    return d


def _paso_resumen(d: Dict, res: Resultado):
    r = d.get("_resumen")
    if r:
        res.pasos.append(f"**Procesar la muestra**: n = {r.n}, x̄ = Σxᵢ/n = {fmt(r.xbar, 4)}, "
                         f"S = √[Σ(xᵢ - x̄)²/(n-1)] = {fmt(r.s, 4)}.")


# ---------------------------------------------------------------------------
# MEDIA
# ---------------------------------------------------------------------------

def _ic_media(d: Dict, alpha: float):
    xbar, s, n = _req(d, "xbar", "desvio", "n")
    N = d.get("N")
    if d.get("sigma_conocido"):
        return ic.ic_media_sigma_conocido(xbar, s, int(n), alpha, N=N)
    return ic.ic_media_sigma_desconocido(xbar, s, int(n), alpha, N=N)


def _cota(d, alpha, res: Resultado):
    """Límite unilateral: se usa el IC bilateral de riesgo 2α y se toma un solo extremo."""
    if d.get("cota") in ("sup", "inf"):
        res.pasos.append(f"**Límite unilateral** ({'máximo' if d['cota'] == 'sup' else 'mínimo'}): todo α = {fmt(alpha, 4)} "
                         f"va a una sola cola → se calcula como el extremo del IC con riesgo 2α = {fmt(2 * alpha, 4)}.")
        return 2 * alpha
    return alpha


def _cierre_cota(d, a, b, alpha_orig, param, res: Resultado):
    if d.get("cota") == "sup":
        res.conclusion = f"Con un {_pct(alpha_orig)} de confianza, {param} ≤ {fmt(b, 4)}: P({param} ≤ {fmt(b, 4)}) = {fmt(1 - alpha_orig, 4)}."
        res.numeros = [b]
        res.resumen = f"cota superior: {fmt(b, 4)}"
    else:
        res.conclusion = f"Con un {_pct(alpha_orig)} de confianza, {param} ≥ {fmt(a, 4)}: P({param} ≥ {fmt(a, 4)}) = {fmt(1 - alpha_orig, 4)}."
        res.numeros = [a]
        res.resumen = f"cota inferior: {fmt(a, 4)}"


def media_ic(d, alpha, res: Resultado, estado):
    alpha_orig, alpha = alpha, _cota(d, alpha, res)
    r = _ic_media(d, alpha)
    conocido = d.get("sigma_conocido")
    n = int(d["n"])
    fpc = " · √((N-n)/(N-1))" if d.get("N") else ""
    if conocido:
        res.pasos.append(f"**Distribución**: σ conocido → Z. Z(1-α/2) = Z({fmt(1 - alpha / 2, 4)}) = {fmt(r.critical_value, 4)}.")
        res.pasos.append(f"**Límites**: A;B = x̄ ∓ Z·σ/√n{fpc} = {fmt(d['xbar'], 4)} ∓ {fmt(r.critical_value, 4)}·"
                         f"{fmt(d['desvio'], 4)}/√{n}{fpc} = {fmt(d['xbar'], 4)} ∓ {fmt(r.error, 4)}.")
    else:
        res.pasos.append(f"**Distribución**: σ desconocido → t de Student con ν = n-1 = {n - 1}. "
                         f"t({fmt(1 - alpha / 2, 4)}; {n - 1}) = {fmt(r.critical_value, 4)}.")
        res.pasos.append(f"**Límites**: A;B = x̄ ∓ t·S/√n{fpc} = {fmt(d['xbar'], 4)} ∓ {fmt(r.critical_value, 4)}·"
                         f"{fmt(d['desvio'], 4)}/√{n}{fpc} = {fmt(d['xbar'], 4)} ∓ {fmt(r.error, 4)}.")
    estado["e_actual"] = r.error
    if d.get("total") and d.get("N"):
        rt = ic.ic_total_poblacional(r, d["N"])
        res.pasos.append(f"**Total poblacional** T = N·μ: se multiplican los límites por N = {fmt(d['N'])}.")
        res.conclusion = f"El total poblacional estará entre {fmt(rt.a, 2)} y {fmt(rt.b, 2)}: " + _p("T", rt.a, rt.b, alpha)
        res.numeros = [rt.a, rt.b]
        res.resumen = f"IC total: [{fmt(rt.a, 2)} ; {fmt(rt.b, 2)}]"
        return
    if d.get("cota"):
        _cierre_cota(d, r.a, r.b, alpha_orig, "μ", res)
        return
    res.conclusion = (f"Se concluye que la media poblacional estará comprendida entre {fmt(r.a, 4)} y {fmt(r.b, 4)}, "
                      f"afirmándolo con un {_pct(alpha)} de confianza, o sea: " + _p("μ", r.a, r.b, alpha) + ".")
    res.numeros = [r.a, r.b, r.error]
    res.resumen = f"IC μ: [{fmt(r.a, 4)} ; {fmt(r.b, 4)}]  (e = {fmt(r.error, 4)})"


def media_n(d, alpha, res: Resultado, estado):
    s = _req(d, "desvio")[0]
    N = d.get("N")
    conocido = d.get("sigma_conocido")
    e = d.get("e")
    if e is None and d.get("reduccion") is not None:
        e_actual = estado.get("e_actual")
        if e_actual is None and d.get("xbar") is not None and d.get("n"):
            e_actual = _ic_media(d, alpha).error
        if e_actual is None:
            raise FaltaDato("Para reducir el error hace falta el error actual (calculá antes el IC)")
        e = e_actual * (1 - d["reduccion"])
        res.pasos.append(f"**Error buscado**: e = e_actual·(1 - {fmt(d['reduccion'], 4)}) = {fmt(e_actual, 4)}·"
                         f"{fmt(1 - d['reduccion'], 4)} = {fmt(e, 4)}.")
    if e is None:
        raise FaltaDato("Falta el error admitido e (o la reducción pedida)")
    if conocido:
        r = ic.n_media_sigma_conocido(s, e, alpha, N=N)
        z = dist.z_two_tailed(alpha)
        res.pasos.append(f"**Fórmula** (σ conocido): n = (Z·σ/e)² = ({fmt(z, 4)}·{fmt(s, 4)}/{fmt(e, 4)})² = "
                         f"{fmt((z * s / e) ** 2, 2)} → se redondea hacia arriba.")
    else:
        r = ic.n_media_sigma_desconocido(s, e, alpha, N=N)
        res.pasos.append(f"**Fórmula** (σ desconocido): n = (t(1-α/2; n-1)·S/e)². Como t depende de n se itera: "
                         f"{r.converged_values}.")
    if N:
        res.pasos.append(f"**Población finita**: n = N·n∞/(N + n∞) con N = {fmt(N)}.")
    res.numeros = [r.n]
    n_act = an_n = d.get("n")
    texto = f"El tamaño de muestra necesario es n = {r.n}."
    if an_n:
        delta = max(0, r.n - int(n_act))
        texto += f" Como ya se tomaron {int(n_act)}, hay que agregar Δn = {r.n} - {int(n_act)} = {delta} unidades más."
        res.numeros.append(delta)
        if r.n <= int(n_act):
            texto += " (El tamaño de muestra actual alcanza.)"
    res.conclusion = texto
    res.resumen = f"n = {r.n}" + (f" (Δn = {max(0, r.n - int(n_act))})" if an_n else "")
    estado["n"] = r.n


def _signo(tail):
    return {"derecha": ">", "izquierda": "<", "bilateral": "≠"}[tail]


def _desvio_efectivo(d, res: Resultado):
    """Con población finita el error estándar lleva √((N-n)/(N-1)): se aplica al desvío."""
    s, n, N = d["desvio"], int(d["n"]), d.get("N")
    if N and N > n:
        f = dist.fpc(N, n)
        res.pasos.append(f"**Población finita** (N = {fmt(N)}): factor √((N-n)/(N-1)) = {fmt(f, 4)} → "
                         f"σ·factor = {fmt(s * f, 4)}.")
        return s * f
    return s


def media_ensayo(d, alpha, res: Resultado, estado):
    mu0, s, n = _req(d, "mu0", "desvio", "n")
    d = dict(d, desvio=_desvio_efectivo(d, res))
    s = d["desvio"]
    tail = d.get("tail") or "bilateral"
    xbar = d.get("xbar")
    if xbar is None:
        raise FaltaDato("Falta la media muestral x̄ para decidir")
    f = hyp.ensayo_media_sigma_conocido if d.get("sigma_conocido") else hyp.ensayo_media_sigma_desconocido
    kw = {"sigma": s} if d.get("sigma_conocido") else {"s": s}
    r = f(xbar=xbar, n=int(n), mu0=mu0, alpha=alpha, tail=tail, mu1=d.get("mu1"), **kw)
    _pasos_ensayo_media(d, r, alpha, res)
    estado.update(tail=tail, xc=r.critical_value)
    res.numeros = list(r.critical_value) if isinstance(r.critical_value, tuple) else [r.critical_value]
    pv = _p_valor_media(d, tail)
    if pv is not None:
        res.pasos.append(f"**Valor a posteriori** α* = P(obtener un x̄ tan extremo | H0) = {fmt(pv, 4)} "
                         f"(se rechaza H0 para cualquier α ≥ α*).")
        res.numeros += [pv, pv * 100]
    res.resumen = f"H0: {r.h0_text}; x̄c = {_cv(r.critical_value)}; " + ("RECHAZA H0" if r.rejects_h0 else "NO rechaza H0")


def _p_valor_media(d, tail):
    from scipy import stats
    n = int(d["n"])
    est = (d["xbar"] - d["mu0"]) / (d["desvio"] / sqrt(n))
    cdf = stats.norm.cdf if d.get("sigma_conocido") else (lambda x: stats.t.cdf(x, n - 1))
    if tail == "derecha":
        return 1 - cdf(est)
    if tail == "izquierda":
        return cdf(est)
    return 2 * min(cdf(est), 1 - cdf(est))


def _pasos_ensayo_media(d, r, alpha, res: Resultado, decidir=True):
    tail, n = r.tail, int(d["n"])
    conocido = d.get("sigma_conocido")
    res.pasos.append(f"**Hipótesis**: H0: {r.h0_text}  vs  H1: {r.h1_text}  (α = {fmt(alpha, 4)}).")
    cuantil = f"(1-α/2)" if tail == "bilateral" else "(1-α)"
    if conocido:
        crit = dist.z_two_tailed(alpha) if tail == "bilateral" else dist.z_one_tailed(alpha)
        res.pasos.append(f"**Distribución**: σ conocido → Z. Z{cuantil} = {fmt(crit, 4)}.")
        base = "σ/√n"
    else:
        crit = dist.t_two_tailed(alpha, n - 1) if tail == "bilateral" else dist.t_one_tailed(alpha, n - 1)
        res.pasos.append(f"**Distribución**: σ desconocido → t de Student, ν = {n - 1}. t{cuantil} = {fmt(crit, 4)}.")
        base = "S/√n"
    if tail == "bilateral":
        c1, c2 = r.critical_value
        res.pasos.append(f"**Condición de rechazo**: x̄c₁;x̄c₂ = μ₀ ∓ {fmt(crit, 4)}·{base} = {fmt(d['mu0'], 4)} ∓ {fmt(crit, 4)}·{fmt(d['desvio'], 4)}/√{n} = {fmt(c1, 4)} ; {fmt(c2, 4)}. "
                         f"Si x̄ < {fmt(c1, 4)} o x̄ > {fmt(c2, 4)} ⇒ se rechaza H0.")
    else:
        op = "+" if tail == "derecha" else "-"
        res.pasos.append(f"**Condición de rechazo**: x̄c = μ₀ {op} {fmt(crit, 4)}·{base} = {fmt(d['mu0'], 4)} {op} {fmt(crit, 4)}·{fmt(d['desvio'], 4)}/√{n} = {fmt(r.critical_value, 4)}. "
                         f"Si x̄ {_signo(tail)} {fmt(r.critical_value, 4)} ⇒ se rechaza H0.")
    if decidir and d.get("xbar") is not None:
        res.pasos.append(f"**Decisión**: x̄ = {fmt(d['xbar'], 4)} → " + ("cae en la zona de rechazo." if r.rejects_h0
                                                                         else "no cae en la zona de rechazo."))
        res.conclusion = _ensayo_txt(r, alpha, f"x̄ = {fmt(d['xbar'], 4)}", d)
    if tail == "bilateral":
        cond = f"x̄ < {fmt(r.critical_value[0], 4)} o x̄ > {fmt(r.critical_value[1], 4)}"
    else:
        cond = f"x̄ {_signo(tail)} {fmt(r.critical_value, 4)}"
    res.regla = _regla(d, f"toma una muestra de n = {n} unidades y se calcula su media x̄", cond, r.h1_text)
    if r.beta is not None:
        res.pasos.append(f"**Con μ₁ = {fmt(d['mu1'], 4)}**: β = {fmt(r.beta, 4)}, potencia 1-β = {fmt(r.power, 4)}.")


def media_beta(d, alpha, res: Resultado, estado):
    mu0, s, n, mu1 = _req(d, "mu0", "desvio", "n", "mu1")
    tail = d.get("tail") or estado.get("tail") or ("izquierda" if mu1 < mu0 else "derecha")
    f = hyp.ensayo_media_sigma_conocido if d.get("sigma_conocido") else hyp.ensayo_media_sigma_desconocido
    kw = {"sigma": s} if d.get("sigma_conocido") else {"s": s}
    r = f(xbar=mu0, n=int(n), mu0=mu0, alpha=alpha, tail=tail, mu1=mu1, **kw)
    se = s / sqrt(int(n))
    xc = r.critical_value
    res.pasos.append(f"**Región crítica** (del ensayo): H0: {r.h0_text}, x̄c = {_cv(xc)}.")
    if tail == "bilateral":
        res.pasos.append(f"**β** = P(x̄c₁ ≤ x̄ ≤ x̄c₂ | μ = {fmt(mu1, 4)}) = Φ(({fmt(xc[1], 4)} - {fmt(mu1, 4)})/{fmt(se, 4)}) - "
                         f"Φ(({fmt(xc[0], 4)} - {fmt(mu1, 4)})/{fmt(se, 4)}) = {fmt(r.beta, 4)}.")
    else:
        z = (xc - mu1) / se
        lado = "x̄ ≤ x̄c" if tail == "derecha" else "x̄ ≥ x̄c"
        res.pasos.append(f"**β** = P({lado} | μ = {fmt(mu1, 4)}) con Z = (x̄c - μ₁)/(σ/√n) = ({fmt(xc, 4)} - {fmt(mu1, 4)})/"
                         f"{fmt(se, 4)} = {fmt(z, 4)} → β = {fmt(r.beta, 4)}.")
    _cierre_beta(d, r.beta, r.power, res)
    if d.get("con_curva"):
        curva = Resultado()
        media_curva(d, alpha, curva, estado)
        res.tabla = curva.tabla
        res.pasos += curva.pasos


def _lado_h0(d) -> bool:
    """¿El valor alternativo cae del lado de H0? Entonces 'rechazar' es un error de tipo I, no una potencia."""
    tail = d.get("tail")
    for v0, v1 in (("mu0", "mu1"), ("sigma0", "sigma1"), ("p0", "p1")):
        if d.get(v0) is not None and d.get(v1) is not None:
            return (tail == "derecha" and d[v1] < d[v0]) or (tail == "izquierda" and d[v1] > d[v0])
    return False


def _cierre_beta(d, beta, potencia, res: Resultado):
    if _lado_h0(d):
        res.pasos.append(f"**Ojo**: el valor pedido cae del lado de H0 (H0 es verdadera), así que no es un β: "
                         f"P(no rechazar H0) = {fmt(beta, 4)} y P(rechazar H0) = {fmt(potencia, 4)} (un error de tipo I, "
                         f"menor que α).")
        pide_no = d.get("prob") == "beta"
        res.conclusion = (f"La probabilidad pedida es P({'no ' if pide_no else ''}rechazar H0) = "
                          f"{fmt(beta if pide_no else potencia, 4)}.")
        res.numeros = [beta, potencia] if pide_no else [potencia, beta]
        res.resumen = f"P(no rechazar) = {fmt(beta, 4)} ; P(rechazar) = {fmt(potencia, 4)}"
        return
    res.pasos.append(f"**Potencia** 1-β = {fmt(potencia, 4)}.")
    if d.get("prob") == "beta":
        res.conclusion = f"La probabilidad pedida es β = {fmt(beta, 4)} (potencia 1-β = {fmt(potencia, 4)})."
        res.numeros = [beta, potencia]
    else:
        res.conclusion = f"La probabilidad pedida es la potencia 1-β = {fmt(potencia, 4)} (β = {fmt(beta, 4)})."
        res.numeros = [potencia, beta]
    res.resumen = f"β = {fmt(beta, 4)} ; 1-β = {fmt(potencia, 4)}"


def media_diseno(d, alpha, res: Resultado, estado):
    mu0, s = _req(d, "mu0", "desvio")
    mu1, beta = d.get("mu1"), d.get("beta")
    if mu1 is not None and beta is not None:
        tail = d.get("tail")
        if tail not in ("derecha", "izquierda", "bilateral") or (tail == "derecha" and mu1 < mu0) or \
                (tail == "izquierda" and mu1 > mu0):
            tail = "izquierda" if mu1 < mu0 else "derecha"
        f = hyp.disenar_ensayo_media_sigma_conocido if d.get("sigma_conocido", True) else hyp.disenar_ensayo_media_sigma_desconocido
        kw = {"sigma": s} if d.get("sigma_conocido", True) else {"s": s}
        r = f(mu0=mu0, mu1=mu1, alpha=alpha, beta=beta, tail=tail, **kw)
        res.pasos.append(f"**Hipótesis**: H0: {r.h0_text}  vs  H1: {r.h1_text}.")
        res.pasos.append(f"**Condiciones**: P(rechazar H0 | μ = {fmt(mu0, 4)}) = α = {fmt(alpha, 4)} y "
                         f"P(no rechazar H0 | μ = {fmt(mu1, 4)}) = β = {fmt(beta, 4)}.")
        res.pasos.append(f"**Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [({fmt(r.z_alpha, 4)} + {fmt(r.z_beta, 4)})·"
                         f"{fmt(s, 4)}/{fmt(abs(mu0 - mu1), 4)}]² = {fmt(r.n_exacto, 2)} → n = {r.n}.")
        res.pasos.append(f"**Condición de rechazo**: x̄c = {_cv(r.critical_value)}  (con n = {r.n}).")
        res.pasos.append(f"**Regla de decisión**: {_coma(r.regla_decision)}")
        if d.get("control"):
            si, no = d.get("accion_rechazo", "se detiene el proceso"), d.get("accion_no_rechazo", "el proceso sigue")
            res.pasos.append(f"**En palabras del problema**: rechazar H0 ⇒ {si}. Si en una muestra de {r.n} la "
                             f"media da {'menor' if tail == 'izquierda' else 'mayor'} que {_cv(r.critical_value)}, {si}; "
                             f"si no, {no}.")
        res.pasos.append(f"Con n = {r.n}: β real = {fmt(r.beta_real, 4)}, potencia real = {fmt(r.potencia_real, 4)}.")
        res.conclusion = _coma(r.regla_decision)
        if d.get("control"):
            res.conclusion += f" Rechazar H0 ⇒ {d.get('accion_rechazo', 'se detiene el proceso')}."
        n_act = d.get("n") if "n" in d and d.get("n") and not estado.get("n_es_diseno") else None
        res.numeros = [r.n] + (list(r.critical_value) if isinstance(r.critical_value, tuple) else [r.critical_value])
        if n_act and r.n > int(n_act):
            res.conclusion += f" (Respecto de la muestra actual de {int(n_act)}: Δn = {r.n - int(n_act)}.)"
            res.numeros.append(r.n - int(n_act))
        res.resumen = f"n = {r.n}; x̄c = {_cv(r.critical_value)}"
        estado.update(n=r.n, tail=tail, xc=r.critical_value, n_es_diseno=True)
        return
    # Sin β: con n dado, H0 + condición de rechazo + regla de decisión
    n = _req(d, "n")[0]
    tail = d.get("tail") or "bilateral"
    f = hyp.ensayo_media_sigma_conocido if d.get("sigma_conocido", True) else hyp.ensayo_media_sigma_desconocido
    kw = {"sigma": s} if d.get("sigma_conocido", True) else {"s": s}
    r = f(xbar=d.get("xbar", mu0), n=int(n), mu0=mu0, alpha=alpha, tail=tail, mu1=mu1, **kw)
    _pasos_ensayo_media(d, r, alpha, res, decidir=d.get("xbar") is not None)
    if tail == "bilateral":
        c1, c2 = r.critical_value
        regla = f"Si en una muestra de {int(n)} la media cae fuera de [{fmt(c1, 4)} ; {fmt(c2, 4)}] se rechaza H0."
    else:
        regla = (f"Si en una muestra de {int(n)} la media es {'mayor' if tail == 'derecha' else 'menor'} que "
                 f"{fmt(r.critical_value, 4)} se rechaza H0.")
    res.pasos.append(f"**Regla de decisión**: {regla}")
    res.conclusion = res.conclusion or regla
    res.numeros = list(r.critical_value) if isinstance(r.critical_value, tuple) else [r.critical_value]
    res.resumen = f"H0: {r.h0_text}; x̄c = {_cv(r.critical_value)}"
    estado.update(tail=tail, xc=r.critical_value)


def media_curva(d, alpha, res: Resultado, estado):
    mu0, s, n = _req(d, "mu0", "desvio", "n")
    tail = d.get("tail") or estado.get("tail") or "bilateral"
    se = s / sqrt(int(n))
    if tail == "derecha":
        mus = [mu0 + k * se * 0.5 for k in range(0, 9)]
    elif tail == "izquierda":
        mus = [mu0 - k * se * 0.5 for k in range(0, 9)]
    else:
        mus = [mu0 + k * se * 0.5 for k in range(-8, 9, 2)]
    tabla = hyp.curva_potencia_media(mu0, s, int(n), alpha, mus, tail=tail, sigma_conocido=bool(d.get("sigma_conocido", True)))
    res.tabla = [{"μ": round(m, 4), "β (curva OC)": round(b, 4), "1-β (potencia)": round(p, 4)} for m, b, p in tabla]
    res.pasos.append(f"Se toman valores de μ del lado de H1 (cola {tail}), con n = {int(n)} y α = {fmt(alpha, 4)}; "
                     "para cada uno se calcula β = P(no rechazar H0 | μ) y la potencia 1-β.")
    res.pasos.append("En el eje X va el parámetro μ; en el eje Y la probabilidad (β para la curva OC, 1-β para la de potencia). "
                     "Marcá al menos 3 puntos con sus valores.")
    res.conclusion = "Tabla de puntos para graficar las curvas (ver abajo)."
    res.resumen = f"curva con {len(tabla)} puntos"


# ---------------------------------------------------------------------------
# VARIANZA
# ---------------------------------------------------------------------------

def varianza_ic(d, alpha, res: Resultado, estado):
    alpha_orig, alpha = alpha, _cota(d, alpha, res)
    s, n = _req(d, "desvio", "n")
    n = int(n)
    rv = ic.ic_varianza(s ** 2, n, alpha)
    rs = ic.ic_desvio(s ** 2, n, alpha)
    c_lo, c_up = rv.critical_value
    res.pasos.append(f"**Distribución**: χ² con ν = n-1 = {n - 1}. χ²({fmt(alpha / 2, 4)}; {n - 1}) = {fmt(c_lo, 4)} y "
                     f"χ²({fmt(1 - alpha / 2, 4)}; {n - 1}) = {fmt(c_up, 4)}.")
    res.pasos.append(f"**Varianza**: A = (n-1)·S²/χ²(1-α/2) = {n - 1}·{fmt(s ** 2, 4)}/{fmt(c_up, 4)} = {fmt(rv.a, 5)} ; "
                     f"B = (n-1)·S²/χ²(α/2) = {n - 1}·{fmt(s ** 2, 4)}/{fmt(c_lo, 4)} = {fmt(rv.b, 5)}.")
    res.pasos.append(f"**Desvío**: A' = √A = {fmt(rs.a, 4)} ; B' = √B = {fmt(rs.b, 4)}. Relación entre límites R' = B'/A' = "
                     f"{fmt(rs.b / rs.a, 4)}.")
    estado["r_sigma"] = rs.b / rs.a
    if d.get("cota"):
        _cierre_cota(d, rs.a, rs.b, alpha_orig, "σ", res)
        res.numeros += [rv.b if d["cota"] == "sup" else rv.a]
        return
    res.conclusion = (f"Con un {_pct(alpha)} de confianza: " + _p("σ²", rv.a, rv.b, alpha) + " y " +
                      _p("σ", rs.a, rs.b, alpha) + ".")
    res.numeros = [rv.a, rv.b, rs.a, rs.b]
    res.resumen = f"IC σ²: [{fmt(rv.a, 5)} ; {fmt(rv.b, 5)}]  IC σ: [{fmt(rs.a, 4)} ; {fmt(rs.b, 4)}]"


def varianza_n(d, alpha, res: Resultado, estado):
    rel = d.get("relacion")
    if rel is None and d.get("reduccion") is not None:
        r_act = estado.get("r_sigma")
        if r_act is None:
            s, n = _req(d, "desvio", "n")
            rs = ic.ic_desvio(s ** 2, int(n), alpha)
            r_act = rs.b / rs.a
        r = ic.n_varianza_por_reduccion(r_act, d["reduccion"], alpha)
    elif rel is not None:
        r = ic.n_varianza_por_relacion(rel, alpha)
    else:
        raise FaltaDato("Falta la relación entre límites buscada o la reducción pedida")
    res.pasos.append(f"**Relación buscada** R' = B'/A' = {fmt(r.r_sigma_objetivo, 4)} → R = (R')² = {fmt(r.r_var_objetivo, 4)}.")
    res.pasos.append(f"**Ecuación de García**: a = Z(1-α/2)·(R^(1/3)+1)/(2·(R^(1/3)-1)) = {fmt(r.a, 4)}; "
                     f"ν = (2/9)·(a + √(a²+1))² = {fmt(r.nu, 2)}; n = ν + 1 → {r.n}.")
    if r.n_exacto:
        res.pasos.append(f"Control por búsqueda exacta en χ²: n = {r.n_exacto} (R' logrado = {fmt(r.r_sigma_logrado, 4)}).")
    res.conclusion = _coma(wording.texto_tamano_muestra_varianza(r, d.get("n")))
    res.numeros = [r.n] + ([r.n - int(d["n"])] if d.get("n") else [])
    res.resumen = f"n = {r.n}"


def varianza_ensayo(d, alpha, res: Resultado, estado, beta_modo=False):
    if beta_modo and d.get("desvio") is None:
        d = dict(d, desvio=d.get("sigma0"))
    s, n, s0 = _req(d, "desvio", "n", "sigma0")
    n = int(n)
    tail = d.get("tail") or estado.get("tail") or ("derecha" if s > s0 else "izquierda")
    s1 = d.get("sigma1")
    r = hyp.ensayo_varianza(s ** 2, n, s0 ** 2, alpha, tail=tail, sigma1_2=s1 ** 2 if s1 else None)
    res.pasos.append(f"**Hipótesis**: H0: {r.h0_text}  vs  H1: {r.h1_text}  (α = {fmt(alpha, 4)}).")
    res.pasos.append(f"**Distribución**: χ² con ν = {n - 1}.")
    if isinstance(r.critical_value, tuple):
        c1, c2 = r.critical_value
        res.pasos.append(f"**Condición de rechazo**: S²c₁ = {fmt(c1, 5)}, S²c₂ = {fmt(c2, 5)} (Sc = {fmt(sqrt(c1), 4)} ; "
                         f"{fmt(sqrt(c2), 4)}). Si S² cae fuera ⇒ se rechaza H0.")
    else:
        res.pasos.append(f"**Condición de rechazo**: S²c = σ₀²·χ²/ν = {fmt(s0 ** 2, 5)}·χ²/{n - 1} = {fmt(r.critical_value, 5)} "
                         f"(Sc = {fmt(sqrt(r.critical_value), 4)}). Si S² {_signo(tail)} S²c ⇒ se rechaza H0.")
    estado["tail"] = tail
    crit = r.critical_value
    res.numeros = [sqrt(c) for c in crit] + list(crit) if isinstance(crit, tuple) else [sqrt(crit), crit]
    if beta_modo:
        if r.beta is None:
            raise FaltaDato("Falta el desvío alternativo σ₁")
        res.pasos.append(f"**β** = P(no rechazar H0 | σ = {fmt(s1, 4)}) = {fmt(r.beta, 4)}.")
        _cierre_beta(d, r.beta, r.power, res)
        return
    res.pasos.append(f"**Decisión**: S² = {fmt(s ** 2, 5)} (S = {fmt(s, 4)}) → " +
                     ("cae en la zona de rechazo." if r.rejects_h0 else "no cae en la zona de rechazo."))
    res.conclusion = _ensayo_txt(r, alpha, f"S = {fmt(s, 4)}", d)
    if isinstance(crit, tuple):
        cond = f"S < {fmt(sqrt(crit[0]), 4)} o S > {fmt(sqrt(crit[1]), 4)}"
    else:
        cond = f"S {_signo(tail)} {fmt(sqrt(crit), 4)}"
    res.regla = _regla(d, f"toma una muestra de n = {n} unidades y se calcula su desvío S", cond, r.h1_text)
    res.resumen = f"H0: {r.h0_text}; Sc = {_cv(tuple(sqrt(c) for c in crit) if isinstance(crit, tuple) else sqrt(crit))}; " + \
                  ("RECHAZA H0" if r.rejects_h0 else "NO rechaza H0")


def varianza_diseno(d, alpha, res: Resultado, estado):
    s0 = _req(d, "sigma0")[0]
    s1, beta = d.get("sigma1"), d.get("beta")
    if s1 is not None and beta is not None:
        r = hyp.n_varianza_para_potencia(s0, s1, alpha, beta)
        res.pasos.append(f"**Hipótesis**: H0: {r.h0_text}  vs  H1: {r.h1_text}.")
        res.pasos.append(f"Se busca el menor n tal que con α = {fmt(alpha, 4)} se tenga β ≤ {fmt(beta, 4)} cuando σ = {fmt(s1, 4)}: "
                         f"n = {r.n} (S²c = {fmt(r.s2_c, 5)}, Sc = {fmt(sqrt(r.s2_c), 4)}, β real = {fmt(r.beta_real, 4)}).")
        res.conclusion = f"El tamaño de muestra necesario es n = {r.n}."
        res.numeros = [r.n, sqrt(r.s2_c)]
        res.resumen = f"n = {r.n}"
        if d.get("n"):
            delta = max(0, r.n - int(d["n"]))
            res.conclusion += f" Como la muestra actual es de {int(d['n'])}, hay que tomar Δn = {r.n} - {int(d['n'])} = {delta} más."
            res.numeros.append(r.n - int(d["n"]))
            res.resumen += f" (Δn = {delta})"
        return
    d = dict(d)
    d.setdefault("desvio", s0)
    varianza_ensayo(d, alpha, res, estado)
    res.pasos = [p for p in res.pasos if not p.startswith("**Decisión**")]
    res.conclusion = "Valor crítico y condición de rechazo arriba."


# ---------------------------------------------------------------------------
# PROPORCIÓN
# ---------------------------------------------------------------------------

def prop_ic(d, alpha, res: Resultado, estado):
    alpha_orig, alpha = alpha, _cota(d, alpha, res)
    r_, n = _req(d, "r", "n")
    r = ic.ic_proporcion_exacto(int(r_), int(n), alpha)
    rn = ic.ic_proporcion_normal(int(r_) / int(n), int(n), alpha)
    res.pasos.append(f"**Datos**: n = {int(n)}, r = {int(r_)}, p̂ = r/n = {fmt(int(r_) / int(n), 4)}.")
    res.pasos.append(f"**Modelo exacto** (Beta / F, el que usa la cátedra): A = {fmt(r.a, 4)} ; B = {fmt(r.b, 4)}.")
    res.pasos.append(f"Referencia, aproximación normal: p̂ ∓ Z·√(p̂(1-p̂)/(n-1)) = [{fmt(rn.a, 4)} ; {fmt(rn.b, 4)}] "
                     f"(e = {fmt(rn.error, 4)}).")
    for w in r.warnings:
        res.avisos.append(w)
    estado["e_actual"] = rn.error
    if d.get("cota"):
        _cierre_cota(d, r.a, r.b, alpha_orig, "p", res)
        res.numeros += [x * 100 for x in res.numeros]
        return
    res.conclusion = (f"El porcentaje poblacional estará entre {fmt(r.a * 100, 2)}% y {fmt(r.b * 100, 2)}%, con un "
                      f"{_pct(alpha)} de confianza: " + _p("p", r.a, r.b, alpha) + ".")
    res.numeros = [r.a, r.b, r.a * 100, r.b * 100]
    res.resumen = f"IC p: [{fmt(r.a, 4)} ; {fmt(r.b, 4)}]"


def prop_n(d, alpha, res: Resultado, estado):
    p_hat = d.get("p_hat")
    if p_hat is None:
        p_hat = 0.5
        res.avisos.append("Sin estimación previa de p: se usa el caso más desfavorable p̂ = 0,5.")
    e = d.get("e")
    if e is None and d.get("reduccion") is not None:
        e_act = estado.get("e_actual")
        if e_act is None and d.get("n"):
            e_act = ic.ic_proporcion_normal(p_hat, int(d["n"]), alpha).error
        if e_act is None:
            raise FaltaDato("Falta el error actual para aplicar la reducción")
        e = e_act * (1 - d["reduccion"])
        res.pasos.append(f"**Error buscado**: e = {fmt(e_act, 4)}·(1 - {fmt(d['reduccion'], 4)}) = {fmt(e, 4)}.")
    if e is None:
        raise FaltaDato("Falta el error admitido e")
    r = ic.n_proporcion(p_hat, e, alpha)
    z = dist.z_two_tailed(alpha)
    res.pasos.append(f"**Fórmula** (aprox. normal): n = Z²·p̂(1-p̂)/e² + 1 = {fmt(z, 4)}²·{fmt(p_hat, 4)}·{fmt(1 - p_hat, 4)}/"
                     f"{fmt(e, 4)}² + 1 → n = {r.n}.")
    res.conclusion = f"El tamaño de muestra necesario es n = {r.n}."
    res.numeros = [r.n]
    if d.get("n"):
        res.conclusion += f" Respecto de la muestra de {int(d['n'])}: Δn = {max(0, r.n - int(d['n']))}."
        res.numeros.append(max(0, r.n - int(d["n"])))
    res.resumen = f"n = {r.n}"


def prop_ensayo(d, alpha, res: Resultado, estado, beta_modo=False):
    n, p0 = _req(d, "n", "p0")
    r_ = d.get("r")
    if r_ is None and not beta_modo:
        raise FaltaDato("Falta r (casos observados) o p̂")
    p_obs = (r_ / n) if r_ is not None else p0
    tail = d.get("tail") or estado.get("tail") or ("derecha" if p_obs > p0 else "izquierda")
    r = hyp.ensayo_proporcion(int(r_ if r_ is not None else round(p0 * n)), int(n), p0, alpha, tail=tail, p1=d.get("p1"))
    res.pasos.append(f"**Hipótesis**: H0: {r.h0_text}  vs  H1: {r.h1_text}  (α = {fmt(alpha, 4)}).")
    res.pasos.append(f"**Modelo**: binomial exacto con n = {int(n)} y p₀ = {fmt(p0, 4)}.")
    if isinstance(r.critical_value, tuple):
        c1, c2 = r.critical_value
        res.pasos.append(f"**Condición de rechazo**: r ≤ {c1} o r ≥ {c2} ⇒ se rechaza H0.")
    else:
        op = "≥" if tail == "derecha" else "≤"
        res.pasos.append(f"**Condición de rechazo**: el menor r_c con P(r {op} r_c | p₀) ≤ α es r_c = {r.critical_value}. "
                         f"Si r {op} {r.critical_value} ⇒ se rechaza H0.")
    estado["tail"] = tail
    res.numeros = list(r.critical_value) if isinstance(r.critical_value, tuple) else [r.critical_value]
    if beta_modo:
        if r.beta is None:
            raise FaltaDato("Falta la proporción alternativa p₁")
        res.pasos.append(f"**β** = P(no rechazar H0 | p = {fmt(d['p1'], 4)}) = {fmt(r.beta, 4)}.")
        _cierre_beta(d, r.beta, r.power, res)
        return
    res.pasos.append(f"**Decisión**: r = {int(r_)} (p̂ = {fmt(p_obs, 4)}); valor a posteriori α* = {fmt(r.p_value, 4)} → " +
                     ("se rechaza H0." if r.rejects_h0 else "no se rechaza H0."))
    res.conclusion = _ensayo_txt(r, alpha, f"r = {int(r_)}", d)
    if isinstance(r.critical_value, tuple):
        cond = f"r ≤ {r.critical_value[0]} o r ≥ {r.critical_value[1]}"
    else:
        cond = f"r {'≥' if tail == 'derecha' else '≤'} {r.critical_value}"
    res.regla = _regla(d, f"toma una muestra de n = {int(n)} unidades y se cuenta la cantidad r de casos", cond,
                       r.h1_text)
    res.numeros.append(r.p_value)
    res.resumen = f"H0: {r.h0_text}; rc = {r.critical_value}; " + ("RECHAZA H0" if r.rejects_h0 else "NO rechaza H0")


def prop_diseno(d, alpha, res: Resultado, estado):
    p0 = _req(d, "p0")[0]
    p1, beta = d.get("p1"), d.get("beta")
    if p1 is not None and beta is not None:
        r = hyp.disenar_plan_proporcion(p0, p1, alpha, beta, tail=None)
        res.pasos.append(f"**Hipótesis**: H0: {r.h0_text}  vs  H1: {r.h1_text}.")
        res.pasos.append(f"**Condiciones**: P(rechazar | p₀ = {fmt(p0, 4)}) ≤ α = {fmt(alpha, 4)} y "
                         f"P(no rechazar | p₁ = {fmt(p1, 4)}) ≤ β = {fmt(beta, 4)}.")
        res.pasos.append(f"**Plan (binomial exacto, se itera n)**: n = {r.n}, r_c = {r.rc}. α real = {fmt(r.alpha_real, 4)}, "
                         f"β real = {fmt(r.beta_real, 4)}.")
        res.pasos.append(f"**Regla de decisión**: {r.regla_decision}")
        res.conclusion = r.regla_decision
        res.numeros = [r.n, r.rc]
        res.resumen = f"n = {r.n}; rc = {r.rc}"
        estado.update(n=r.n, tail=r.tail)
        return
    n = _req(d, "n")[0]
    tail = d.get("tail") or "derecha"
    r = hyp.ensayo_proporcion(int(round(p0 * n)), int(n), p0, alpha, tail=tail, p1=p1)
    op = "≥" if tail == "derecha" else "≤"
    res.pasos.append(f"**Hipótesis**: H0: {r.h0_text}  vs  H1: {r.h1_text}.")
    res.pasos.append(f"**Condición de rechazo**: r_c = {r.critical_value} (binomial n = {int(n)}, p₀ = {fmt(p0, 4)}). "
                     f"Si r {op} {r.critical_value} ⇒ se rechaza H0.")
    res.conclusion = f"Si en la muestra de {int(n)} se encuentran r {op} {r.critical_value}, se rechaza H0."
    res.numeros = [r.critical_value]
    res.resumen = f"rc = {r.critical_value}"
    estado["tail"] = tail


def prop_curva(d, alpha, res: Resultado, estado):
    n, p0 = _req(d, "n", "p0")
    tail = d.get("tail") or estado.get("tail") or "derecha"
    paso = max(0.005, round(p0 * 0.1, 3))
    ps = [p0 + (k * paso if tail != "izquierda" else -k * paso) for k in range(0, 9)]
    ps = [p for p in ps if 0 < p < 1]
    filas = []
    for p in ps:
        r = hyp.ensayo_proporcion(int(round(p0 * n)), int(n), p0, alpha, tail=tail, p1=p)
        filas.append({"p": round(p, 4), "β (curva OC)": round(r.beta, 4), "1-β (potencia)": round(r.power, 4)})
    res.tabla = filas
    res.pasos.append(f"Para cada p se calcula β = P(no rechazar H0 | p) con el binomial (n = {int(n)}).")
    res.conclusion = "Tabla de puntos para graficar las curvas (ver abajo)."
    res.resumen = f"curva con {len(filas)} puntos"


# ---------------------------------------------------------------------------
# DOS POBLACIONES
# ---------------------------------------------------------------------------

def _nombres(d):
    return d.get("nombre1") or "1", d.get("nombre2") or "2"


def dos_var_ensayo(d, alpha, res: Resultado, estado):
    s1, n1, s2, n2 = _req(d, "s1", "n1", "s2", "n2")
    a, b = _nombres(d)
    r = two.f_test_equal_variances(s1, int(n1), s2, int(n2), alpha)
    mayor = a if s1 >= s2 else b
    res.pasos.append(f"**Hipótesis**: H0: σ₁² = σ₂² (φ² = 1)  vs  H1: σ₁² ≠ σ₂².")
    res.pasos.append(f"**Estadístico**: j² = S²mayor/S²menor = {fmt(max(s1, s2) ** 2, 4)}/{fmt(min(s1, s2) ** 2, 4)} = "
                     f"{fmt(r.observed_value, 4)} (mayor: {mayor}).")
    res.pasos.append(f"**Valor crítico**: F(1-α; ν_num; ν_den) = {fmt(r.critical_value, 4)}. Si j² > Fc ⇒ se rechaza H0.")
    res.conclusion = _ensayo_txt(r, alpha, f"j² = {fmt(r.observed_value, 4)}", d)
    res.regla = _regla(d, "calcula j² = S²mayor/S²menor con las dos muestras",
                       f"j² > {fmt(r.critical_value, 4)}", "σ₁² ≠ σ₂²")
    res.numeros = [r.observed_value, r.critical_value]
    res.resumen = f"j² = {fmt(r.observed_value, 4)} vs Fc = {fmt(r.critical_value, 4)}: " + ("RECHAZA" if r.rejects_h0 else "NO rechaza")
    if d.get("tail") in ("derecha", "izquierda") or d.get("delta0"):
        res.avisos.append("Si el enunciado pide probar una reducción de un X% del desvío (φ₀ ≠ 1), ajustá el valor "
                          "crítico: j² se compara contra φ₀²·F.")


def dos_var_ic(d, alpha, res: Resultado, estado):
    s1, n1, s2, n2 = _req(d, "s1", "n1", "s2", "n2")
    rd, ri = two.ic_ratio_varianzas(s1, int(n1), s2, int(n2), alpha)
    res.pasos.append(f"**IC para φ² = σ₁²/σ₂²**: [S₁²/S₂²]/F(1-α/2) ; [S₁²/S₂²]/F(α/2) = [{fmt(rd.a, 4)} ; {fmt(rd.b, 4)}].")
    res.pasos.append(f"**IC para σ₂²/σ₁²**: [{fmt(ri.a, 4)} ; {fmt(ri.b, 4)}].")
    res.pasos.append(f"**IC para los desvíos (raíz)**: σ₁/σ₂ ∈ [{fmt(sqrt(rd.a), 4)} ; {fmt(sqrt(rd.b), 4)}], "
                     f"σ₂/σ₁ ∈ [{fmt(sqrt(ri.a), 4)} ; {fmt(sqrt(ri.b), 4)}].")
    res.conclusion = _p("σ₁²/σ₂²", rd.a, rd.b, alpha) + "."
    res.numeros = [rd.a, rd.b, ri.a, ri.b, sqrt(rd.a), sqrt(rd.b), sqrt(ri.a), sqrt(ri.b)]
    res.resumen = f"IC σ₁²/σ₂²: [{fmt(rd.a, 4)} ; {fmt(rd.b, 4)}]"


def _dos_medias_base(d, alpha, res: Resultado):
    """Devuelve (apareadas, diferencias | None, iguales: bool)."""
    a, b = _nombres(d)
    if d.get("apareadas"):
        l1, l2 = _req(d, "datos1", "datos2")
        if len(l1) != len(l2):
            raise FaltaDato("Para muestras apareadas las dos listas deben tener el mismo largo")
        dif = [x - y for x, y in zip(l1, l2)]
        rs = resumen_muestra(dif)
        res.pasos.append(f"**Muestras apareadas**: se trabaja con las diferencias dᵢ = ({a}) - ({b}): "
                         f"d̄ = {fmt(rs.xbar, 4)}, S_d = {fmt(rs.s, 4)}, n = {rs.n} pares (ν = {rs.n - 1}).")
        return True, dif, None
    s1, n1, s2, n2 = _req(d, "s1", "n1", "s2", "n2")
    f = two.f_test_equal_variances(s1, int(n1), s2, int(n2), alpha)
    iguales = not f.rejects_h0
    res.pasos.append(f"**Paso 1 — test F** (¿varianzas iguales?): j² = {fmt(f.observed_value, 4)} vs Fc = "
                     f"{fmt(f.critical_value, 4)} → " + ("no se rechaza σ₁² = σ₂² ⇒ t con varianza amalgamada (pooled)."
                                                        if iguales else "se rechaza σ₁² = σ₂² ⇒ test de Welch (ν de Aspin-Welch)."))
    return False, None, iguales


def dos_medias_ensayo(d, alpha, res: Resultado, estado):
    a, b = _nombres(d)
    apareadas, dif, iguales = _dos_medias_base(d, alpha, res)
    delta0 = d.get("delta0") or 0.0
    if apareadas:
        dbar = sum(dif) / len(dif)
    else:
        dbar = d["xbar1"] - d["xbar2"]
    if d.get("delta0_pct") and not d.get("delta0"):
        ref = d.get("xbar2") if not apareadas else sum(d["datos2"]) / len(d["datos2"])
        delta0 = d["delta0_pct"] * ref
        res.pasos.append(f"δ₀ = {fmt(d['delta0_pct'] * 100, 2)}% de x̄({b}) = {fmt(delta0, 4)}.")
    tail = d.get("tail") or "bilateral"
    if tail != "bilateral":
        # se orienta H1 hacia el lado que muestran los datos (δ = μ₁ - μ₂)
        tail = "derecha" if dbar >= 0 else "izquierda"
        delta0 = abs(delta0) if dbar >= 0 else -abs(delta0)
    res.pasos.append(f"**Parámetro**: δ = μ({a}) - μ({b}); diferencia observada d = {fmt(dbar, 4)}.")
    if apareadas:
        r = two.ensayo_media_apareada(dif, delta0, alpha, tail=tail)
    elif iguales:
        r = two.ensayo_media_diferencia_varianzas_iguales(d["xbar1"], d["s1"], int(d["n1"]), d["xbar2"], d["s2"],
                                                           int(d["n2"]), delta0, alpha, tail=tail)
    else:
        r = two.ensayo_media_diferencia_varianzas_distintas(d["xbar1"], d["s1"], int(d["n1"]), d["xbar2"], d["s2"],
                                                             int(d["n2"]), delta0, alpha, tail=tail)
    res.pasos.append(f"**Hipótesis**: H0: {r.h0_text}  vs  H1: {r.h1_text}  (α = {fmt(alpha, 4)}; t con ν = {r.df}).")
    res.pasos.append(f"**Condición de rechazo**: d_c = {_cv(r.critical_value)}. Si d {_signo(tail)} d_c ⇒ se rechaza H0.")
    res.pasos.append(f"**Decisión**: d = {fmt(dbar, 4)} → " + ("se rechaza H0." if r.rejects_h0 else "no se rechaza H0."))
    res.conclusion = _ensayo_txt(r, alpha, f"d = {fmt(dbar, 4)}", d)
    if isinstance(r.critical_value, tuple):
        cond = f"d < {fmt(r.critical_value[0], 4)} o d > {fmt(r.critical_value[1], 4)}"
    else:
        cond = f"d {_signo(tail)} {fmt(r.critical_value, 4)}"
    res.regla = _regla(d, "calcula la diferencia d entre las medias muestrales", cond, r.h1_text)
    res.numeros = (list(r.critical_value) if isinstance(r.critical_value, tuple) else [r.critical_value]) + [dbar]
    res.resumen = f"H0: {r.h0_text}; dc = {_cv(r.critical_value)}; " + ("RECHAZA H0" if r.rejects_h0 else "NO rechaza H0")


def dos_medias_ic(d, alpha, res: Resultado, estado):
    a, b = _nombres(d)
    apareadas, dif, iguales = _dos_medias_base(d, alpha, res)
    if apareadas:
        r = two.ic_media_apareada(dif, alpha)
        estado["s_d"] = resumen_muestra(dif).s
    elif iguales:
        r = two.ic_media_diferencia_varianzas_iguales(d["xbar1"], d["s1"], int(d["n1"]), d["xbar2"], d["s2"], int(d["n2"]), alpha)
    else:
        r = two.ic_media_diferencia_varianzas_distintas(d["xbar1"], d["s1"], int(d["n1"]), d["xbar2"], d["s2"], int(d["n2"]), alpha)
    estado["e_actual"] = r.error
    res.pasos.append(f"**IC para δ = μ({a}) - μ({b})**: d ∓ t({fmt(1 - alpha / 2, 4)}; {r.df})·σ_d = {fmt(r.point_estimate, 4)} ∓ "
                     f"{fmt(r.error, 4)}.")
    res.conclusion = _p("δ", r.a, r.b, alpha) + "."
    res.numeros = [r.a, r.b, r.error]
    res.resumen = f"IC δ: [{fmt(r.a, 4)} ; {fmt(r.b, 4)}]"


def dos_medias_n(d, alpha, res: Resultado, estado):
    e = d.get("e")
    if e is None and d.get("reduccion") is not None:
        if estado.get("e_actual") is None:
            tmp = Resultado()
            dos_medias_ic(d, alpha, tmp, estado)
        e = estado["e_actual"] * (1 - d["reduccion"])
        res.pasos.append(f"**Error buscado**: e = {fmt(estado['e_actual'], 4)}·(1 - {fmt(d['reduccion'], 4)}) = {fmt(e, 4)}.")
    if e is None:
        raise FaltaDato("Falta el error e o la reducción pedida")
    if d.get("apareadas"):
        s_d = estado.get("s_d") or resumen_muestra([x - y for x, y in zip(d["datos1"], d["datos2"])]).s
        r = two.n_media_apareada_para_error(s_d, e, alpha)
        base = len(d["datos1"])
    else:
        r = two.n_media_diferencia_varianzas_iguales_para_error(d["s1"], d["s2"], e, alpha)
        base = int(min(d.get("n1") or 0, d.get("n2") or 0)) or None
    res.pasos.append(f"Iterando con t (tamaños iguales en ambas muestras): n = {r.n} {r.converged_values}.")
    res.conclusion = f"Se necesitan n = {r.n} en cada muestra." + (f" Δn = {max(0, r.n - base)} más en cada una." if base else "")
    res.numeros = [r.n] + ([max(0, r.n - base)] if base else [])
    res.resumen = f"n = {r.n}"


# ---------------------------------------------------------------------------
# CHI-CUADRADO
# ---------------------------------------------------------------------------

def chi_cont(d, alpha, res: Resultado, estado):
    tabla = _req(d, "tabla")[0]
    r = chi.tabla_contingencia([list(map(float, f)) for f in tabla], alpha)
    res.pasos.append("**Hipótesis**: H0: las variables son independientes (o los grupos son homogéneos)  vs  H1: no lo son.")
    res.pasos.append("**Frecuencias esperadas**: Eᵢⱼ = (total fila i · total columna j) / total general.")
    res.pasos.append(f"**Estadístico**: χ² = Σ (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ = {fmt(r.chi2_calc, 4)}; ν = (f-1)(c-1) = {r.df}; "
                     f"χ²crítico(1-α; {r.df}) = {fmt(r.chi2_critico, 4)}.")
    res.pasos.append(f"**Decisión**: " + ("χ² > χ²c ⇒ se rechaza H0." if r.rejects_h0 else "χ² ≤ χ²c ⇒ no se rechaza H0."))
    res.avisos += r.warnings
    res.tabla = [{f"col {j + 1}": round(v, 3) for j, v in enumerate(fila)} for fila in r.expected_table]
    res.conclusion = _coma(wording.texto_chi_cuadrado(r, "las variables son independientes (no hay asociación / los grupos son homogéneos)", alpha))
    res.regla = _regla(d, "calcula χ² = Σ(Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ con la tabla observada", f"χ² > {fmt(r.chi2_critico, 4)}",
                       "las variables están asociadas")
    res.numeros = [r.chi2_calc, r.chi2_critico]
    res.resumen = f"χ² = {fmt(r.chi2_calc, 4)} vs {fmt(r.chi2_critico, 4)}: " + ("RECHAZA" if r.rejects_h0 else "NO rechaza")


def chi_ajuste(d, alpha, res: Resultado, estado):
    obs = _req(d, "observados")[0]
    esp = d.get("esperados")
    if not esp and d.get("proporciones"):
        props = d["proporciones"]
        if len(props) != len(obs):
            raise FaltaDato("La cantidad de proporciones no coincide con la de categorías observadas")
        total = sum(obs)
        esp = [total * p for p in props]
        res.pasos.append(f"**Frecuencias esperadas**: Feᵢ = N·pᵢ con N = {fmt(total)} → " +
                         ", ".join(fmt(e, 3) for e in esp) + ".")
    if not esp:
        raise FaltaDato("Faltan las frecuencias esperadas Fe (o las proporciones del modelo)")
    p = int(d.get("p_estimados") or 0)
    r = chi.bondad_de_ajuste(list(map(float, obs)), list(map(float, esp)), p, alpha)
    res.pasos.append("**Hipótesis**: H0: los datos siguen el modelo propuesto  vs  H1: no lo siguen.")
    res.pasos.append(f"**Estadístico**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = {fmt(r.chi2_calc, 4)}; ν = k - 1 - p = {len(obs)} - 1 - {p} = {r.df}; "
                     f"χ²crítico = {fmt(r.chi2_critico, 4)}.")
    res.pasos.append("**Decisión**: " + ("χ² > χ²c ⇒ se rechaza H0." if r.rejects_h0 else "χ² ≤ χ²c ⇒ no se rechaza H0."))
    res.avisos += r.warnings
    res.conclusion = _coma(wording.texto_chi_cuadrado(r, "los datos siguen el modelo propuesto", alpha))
    res.regla = _regla(d, "calcula χ² = Σ(Foᵢ - Feᵢ)²/Feᵢ con las frecuencias observadas",
                       f"χ² > {fmt(r.chi2_critico, 4)}", "los datos no siguen el modelo propuesto")
    res.numeros = [r.chi2_calc, r.chi2_critico]
    res.resumen = f"χ² = {fmt(r.chi2_calc, 4)} vs {fmt(r.chi2_critico, 4)}: " + ("RECHAZA" if r.rejects_h0 else "NO rechaza")


# ---------------------------------------------------------------------------
# Despacho
# ---------------------------------------------------------------------------

DESPACHO = {
    ("media", "ic"): media_ic, ("media", "n"): media_n, ("media", "ensayo"): media_ensayo,
    ("media", "beta"): media_beta, ("media", "diseno"): media_diseno, ("media", "curva"): media_curva,
    ("varianza", "ic"): varianza_ic, ("varianza", "n"): varianza_n, ("varianza", "ensayo"): varianza_ensayo,
    ("varianza", "beta"): lambda d, a, r, e: varianza_ensayo(d, a, r, e, beta_modo=True),
    ("varianza", "diseno"): varianza_diseno,
    ("proporcion", "ic"): prop_ic, ("proporcion", "n"): prop_n, ("proporcion", "ensayo"): prop_ensayo,
    ("proporcion", "beta"): lambda d, a, r, e: prop_ensayo(d, a, r, e, beta_modo=True),
    ("proporcion", "diseno"): prop_diseno, ("proporcion", "curva"): prop_curva,
    ("dos_varianzas", "ensayo"): dos_var_ensayo, ("dos_varianzas", "ic"): dos_var_ic,
    ("dos_medias", "ensayo"): dos_medias_ensayo, ("dos_medias", "ic"): dos_medias_ic, ("dos_medias", "n"): dos_medias_n,
    ("chi_contingencia", "ensayo"): chi_cont, ("chi_ajuste", "ensayo"): chi_ajuste,
}

TITULOS = {"ic": "Intervalo de confianza", "n": "Tamaño de muestra", "ensayo": "Ensayo de hipótesis",
           "beta": "Probabilidad de error / potencia", "diseno": "Diseño del ensayo", "curva": "Curvas OC y de potencia"}


def _ambos(d, alpha, tipo, res: Resultado, estado):
    """Doble condición: primero la media y después el desvío (el estado queda con el del desvío)."""
    partes = []
    for tema, nombre in (("media", "la media μ"), ("varianza", "el desvío σ")):
        sub = Resultado()
        dd = dict(d)
        if tema == "media":
            dd["sigma_conocido"] = False
            dd.pop("mu1", None)
        DESPACHO[(tema, tipo)](dd, alpha, sub, estado)
        if tipo == "ensayo":
            sub.pasos = siete_pasos(sub.pasos, alpha, sub.regla)
        res.pasos.append(f"**— Sobre {nombre} —**")
        res.pasos += sub.pasos
        res.numeros += sub.numeros
        partes.append(sub)
    m, v = partes
    res.resumen = f"μ: {m.resumen} | σ: {v.resumen}"
    if tipo == "ensayo":
        rechaza = ["NO rechaza" not in x.resumen for x in partes]
        final = ("Se rechazan las DOS hipótesis nulas: se cumplen ambas condiciones → se recomienda." if all(rechaza) else
                 "No se rechazan las dos hipótesis nulas: no se puede asegurar que se cumplan ambas condiciones → "
                 "no se recomienda.")
        res.conclusion = f"Media: {m.conclusion} Desvío: {v.conclusion} {final}"
    else:
        res.conclusion = f"{m.conclusion} {v.conclusion}"


def resolver_inciso(an: Analisis, inc: Inciso, estado: Dict) -> Resultado:
    res = Resultado(titulo=f"{inc.letra}) {TITULOS.get(inc.tipo, 'Sin cálculo')}")
    f = DESPACHO.get((an.tema, inc.tipo))
    if f is None:
        res.errores.append("La app no calcula este tipo de pregunta para este tema. "
                           "Mirá la teoría y los ejercicios parecidos de la guía.")
        res.resumen = "sin cálculo"
        return res
    try:
        d = _datos(an, inc, estado)
        alpha = d.get("alpha")
        if alpha is None and inc.tipo == "ensayo":
            alpha = 0.05
            res.avisos.append("El enunciado no fija el riesgo α: se usó α = 0,05. Mirá el valor a posteriori α*: "
                              "se rechaza H0 para cualquier α ≥ α* (así lo responde la guía en estos casos).")
        if alpha is None:
            raise FaltaDato("Falta el riesgo α")
        _paso_resumen(d, res) if an.tema in ("media", "varianza") else None
        cola_previa = estado.get("tail")
        if d.get("ambos") and an.tema in ("media", "varianza") and inc.tipo in ("ensayo", "ic"):
            _ambos(d, float(alpha), inc.tipo, res, estado)
        else:
            f(d, float(alpha), res, estado)
        # la cola efectiva: la que fijó este inciso (un diseño la corrige según μ₁) o la del inciso
        cola = estado.get("tail") if estado.get("tail") != cola_previa else (d.get("tail") or estado.get("tail"))
        res.pasos = agregar_presentacion(res.pasos, an.tema, inc.tipo, dict(d, alpha=alpha), an.criterio, cola)
        res.pasos = [_coma(x) if x.startswith(("**Hipótesis**", "**Región crítica**", "**1 · Planteo")) else x
                     for x in res.pasos]
        if inc.tipo == "ensayo" and not d.get("ambos"):
            res.pasos = siete_pasos(res.pasos, float(alpha), res.regla)
    except FaltaDato as e:
        res.errores.append(str(e))
        res.resumen = "faltan datos"
    except (ValueError, RuntimeError, ZeroDivisionError, TypeError, KeyError) as e:
        res.errores.append(f"No se pudo calcular: {e}")
        res.resumen = "error"
    return res


def resolver(an: Analisis) -> List[Resultado]:
    estado: Dict = {}
    return [resolver_inciso(an, inc, estado) for inc in an.incisos]
