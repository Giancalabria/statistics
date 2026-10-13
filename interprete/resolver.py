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

from .modelo import DESPACHO_EXTRA, TIPOS, Analisis, Inciso
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
    if d.get("r_buenas") and d.get("r") is not None and d.get("n"):
        d["_r_contado"] = d["r"]
        d["r"] = int(d["n"]) - int(d["r"])
        d.pop("p_hat", None)
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
    k = d.get("escala")
    if k and k != 1:
        res.pasos.append(f"**En unidades** (los datos venían en miles, × {fmt(k)}): entre {fmt(r.a * k, 2)} y "
                         f"{fmt(r.b * k, 2)} (e = {fmt(r.error * k, 2)}).")
        res.conclusion += f" En unidades: entre {fmt(r.a * k, 2)} y {fmt(r.b * k, 2)}."
        res.numeros += [r.a * k, r.b * k]


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
        res.pasos.append(f"**Población finita**: n∞ = {r.n_infinito}; n = N·n∞/(N + n∞) = {fmt(N)}·{r.n_infinito}/"
                         f"({fmt(N)} + {r.n_infinito}) → n = {r.n}.")
    res.numeros = [r.n]
    n_act = an_n = d.get("n")
    texto = f"El tamaño de muestra necesario es n = {r.n}."
    if an_n:
        delta = max(0, r.n - int(n_act))
        texto += f" Como ya se tomaron {int(n_act)}, hay que agregar Δn = {r.n} - {int(n_act)} = {delta} unidades más."
        res.numeros.append(delta)
        if r.n <= int(n_act):
            texto += " (El tamaño de muestra actual alcanza.)"
    if r.n_exacto and (not an_n or r.n <= int(n_act)):
        # para decidir si la muestra tomada alcanza se compara contra el valor sin redondear
        texto += f" (Sin redondear, la fórmula da {fmt(r.n_exacto, 2)}.)"
        res.numeros.append(r.n_exacto)
    if N and r.n_infinito:
        res.numeros.append(r.n_infinito)
    res.conclusion = texto
    res.resumen = f"n = {r.n}" + (f" (Δn = {max(0, r.n - int(n_act))})" if an_n else "")
    estado["n"] = r.n
    _costo(d, r.n, max(0, r.n - int(n_act)) if an_n else None, res)


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


def _neto(d, bruto):
    """(neto, explicación) si hay un costo fijo o una comisión que descontar de la media; si no, None."""
    if d.get("comision"):
        k = d["comision"]
        return bruto * (1 - k), f"x̄ neto = x̄·(1 - {fmt(k, 4)}) = {fmt(bruto, 2)}·{fmt(1 - k, 4)} = {fmt(bruto * (1 - k), 2)}"
    if d.get("costo_fijo"):
        c = d["costo_fijo"]
        return bruto - c, f"x̄ neto = x̄ - {fmt(c, 2)} = {fmt(bruto, 2)} - {fmt(c, 2)} = {fmt(bruto - c, 2)}"
    return None


def _bruto(d, neto):
    if d.get("comision"):
        return neto / (1 - d["comision"])
    return neto + (d.get("costo_fijo") or 0)


def media_ensayo(d, alpha, res: Resultado, estado):
    mu0, s, n = _req(d, "mu0", "desvio", "n")
    d = dict(d, desvio=_desvio_efectivo(d, res))
    s = d["desvio"]
    tail = d.get("tail") or "bilateral"
    xbar = d.get("xbar")
    if xbar is None:
        raise FaltaDato("Falta la media muestral x̄ para decidir")
    bruto, neto_txt = xbar, _neto(d, xbar)
    if neto_txt:
        xbar = neto_txt[0]
        d = dict(d, xbar=xbar)
        res.pasos.append(f"**Valor neto**: lo que se compara con μ₀ es la media NETA: {neto_txt[1]}.")
    f = hyp.ensayo_media_sigma_conocido if d.get("sigma_conocido") else hyp.ensayo_media_sigma_desconocido
    kw = {"sigma": s} if d.get("sigma_conocido") else {"s": s}
    r = f(xbar=xbar, n=int(n), mu0=mu0, alpha=alpha, tail=tail, mu1=d.get("mu1"), **kw)
    _pasos_ensayo_media(d, r, alpha, res)
    estado.update(tail=tail, xc=r.critical_value)
    res.numeros = list(r.critical_value) if isinstance(r.critical_value, tuple) else [r.critical_value]
    if neto_txt and not isinstance(r.critical_value, tuple):
        xc_bruto = _bruto(d, r.critical_value)
        res.pasos.append(f"**Equivalente en valores brutos**: la media bruta debería superar x̄c bruto = {fmt(xc_bruto, 2)} "
                         f"(se obtuvo {fmt(bruto, 2)}).")
        res.numeros.append(xc_bruto)
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
    if d.get("prob_xbar"):
        # '¿probabilidad de tener una media de 6,6?' con el proceso en su valor nominal: P(x̄ ≥ 6,6 | μ₀)
        se = s / sqrt(int(n))
        z = (mu1 - mu0) / se
        p = 1 - dist.norm_cdf(z) if mu1 >= mu0 else dist.norm_cdf(z)
        op = "≥" if mu1 >= mu0 else "≤"
        res.pasos.append(f"**Distribución de la media** con el proceso en su valor nominal: x̄ ~ N(μ₀ = {fmt(mu0, 4)}; "
                         f"σ/√n = {fmt(s, 4)}/√{int(n)} = {fmt(se, 4)}).")
        res.pasos.append(f"**Probabilidad**: P(x̄ {op} {fmt(mu1, 4)}) = P(Z {op} {fmt(z, 4)}) = {fmt(p, 6)}.")
        res.numeros += [p, z]
        res.resumen = f"P(x̄ {op} {fmt(mu1, 4)}) = {fmt(p, 6)}"
        res.conclusion = (f"P(x̄ {op} {fmt(mu1, 4)}) = {fmt(p, 6)}" +
                          (": es prácticamente imposible obtener esa media si el proceso está en su valor nominal; "
                           "si apareciera, el proceso está fuera de control." if p < 0.001 else "."))
        return
    if d.get("mu1_bruto") and _neto(d, mu1):
        neto, txt = _neto(d, mu1)
        res.pasos.append(f"**Valor alternativo neto** (el enunciado lo da sin descontar): μ₁ {txt.split('=', 1)[1].strip()}"
                         .replace("μ₁ x̄", "μ₁"))
        mu1 = neto
        d = dict(d, mu1=mu1)
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
    for v0, v1 in (("mu0", "mu1"), ("sigma0", "sigma1"), ("p0", "p1"), ("phi0", "phi1")):
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
    k = d.get("repeticiones")
    if k and int(k) >= 2:
        k = int(k)
        combina = d.get("combina", "ninguna")
        if combina == "ninguna":
            v, txt = beta ** k, f"P(ninguna de las {k} muestras lo detecte) = β^{k} = {fmt(beta, 4)}^{k}"
        elif combina == "alguna":
            v, txt = 1 - beta ** k, f"P(al menos una de las {k} muestras lo detecte) = 1 - β^{k} = 1 - {fmt(beta, 4)}^{k}"
        else:
            v, txt = potencia ** k, f"P(las {k} muestras lo detecten) = (1-β)^{k} = {fmt(potencia, 4)}^{k}"
        res.pasos.append(f"**Ensayos repetidos** (muestras independientes): {txt} = {fmt(v, 4)}.")
        res.conclusion = f"La probabilidad pedida es {txt} = {fmt(v, 4)}."
        res.numeros = [v] + res.numeros
        res.resumen = f"{combina} de {k}: {fmt(v, 4)} (β = {fmt(beta, 4)})"


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
        res.numeros = [r.n] + (list(r.critical_value) if isinstance(r.critical_value, tuple) else [r.critical_value]) + [mu0]
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
    periodos = d.get("datos") if d.get("medias_periodo") and d.get("datos") else None
    r = f(xbar=mu0 if periodos else d.get("xbar", mu0), n=int(n), mu0=mu0, alpha=alpha, tail=tail, mu1=mu1, **kw)
    _pasos_ensayo_media(d, r, alpha, res, decidir=d.get("xbar") is not None and not periodos)
    if tail == "bilateral":
        c1, c2 = r.critical_value
        regla = f"Si en una muestra de {int(n)} la media cae fuera de [{fmt(c1, 4)} ; {fmt(c2, 4)}] se rechaza H0."
    else:
        regla = (f"Si en una muestra de {int(n)} la media es {'mayor' if tail == 'derecha' else 'menor'} que "
                 f"{fmt(r.critical_value, 4)} se rechaza H0.")
    res.pasos.append(f"**Regla de decisión**: {regla}")
    res.conclusion = res.conclusion or regla
    if periodos:
        # los datos son medias de cada período (semana, día, lote): cada una se compara con los límites de control
        def fuera(x):
            if tail == "bilateral":
                return x < c1 or x > c2
            return x > r.critical_value if tail == "derecha" else x < r.critical_value
        afuera = [(k + 1, x) for k, x in enumerate(periodos) if fuera(x)]
        res.pasos.append("**Control de cada período** (cada valor es la media de una muestra de "
                         f"{int(n)}): " + ", ".join(f"{k}: {fmt(x, 4)}{' ✗' if fuera(x) else ''}"
                                                    for k, x in enumerate(periodos, 1)) + ".")
        if afuera:
            res.conclusion = (regla + f" Hay {len(afuera)} período(s) fuera de los límites (" +
                              ", ".join(f"n.º {k}: {fmt(x, 4)}" for k, x in afuera) +
                              "): hay razones para alarmarse, el proceso estuvo fuera de control.")
        else:
            res.conclusion = regla + " Todos los períodos quedan dentro de los límites: no hay razones para alarmarse."
    res.numeros = list(r.critical_value) if isinstance(r.critical_value, tuple) else [r.critical_value]
    res.resumen = f"H0: {r.h0_text}; x̄c = {_cv(r.critical_value)}"
    if periodos:
        res.resumen += f"; {len(afuera)} período(s) fuera de control" if afuera else "; todos dentro de los límites"
    estado.update(tail=tail, xc=r.critical_value)
    beta = d.get("beta")
    if mu1 is None and beta is not None and tail in ("derecha", "izquierda") and 0 < beta < 1:
        # n y x̄c fijos + β fijado: la media alternativa es la que deja β del lado de 'no rechazar'
        xc, se = r.critical_value, s / sqrt(int(n))
        z_b = dist.z_one_tailed(beta)
        mu1 = xc + z_b * se if tail == "derecha" else xc - z_b * se
        op = "+" if tail == "derecha" else "-"
        res.pasos.append(f"**Media alternativa** (la que se detecta con 1-β = {fmt(1 - beta, 4)}): μ₁ = x̄c {op} Z(1-β)·σ/√n = "
                         f"{fmt(xc, 4)} {op} {fmt(z_b, 4)}·{fmt(s, 4)}/√{int(n)} = {fmt(mu1, 4)}.")
        res.conclusion += f" La media alternativa definida por β = {fmt(beta, 4)} es μ₁ = {fmt(mu1, 4)}."
        res.numeros.append(mu1)
        res.resumen += f"; μ₁ = {fmt(mu1, 4)}"
        estado["mu1"] = mu1


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
    res.numeros = [rv.a, rv.b, rs.a, rs.b, rs.b / rs.a]
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
    r = hyp.ensayo_varianza(s ** 2, n, round(s0 ** 2, 10), alpha, tail=tail, sigma1_2=s1 ** 2 if s1 else None)
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
    # forma equivalente con la variable estandarizada: χ²calc = ν·S²/σ₀² contra el χ² de tabla
    chi_calc = (n - 1) * s ** 2 / s0 ** 2
    chi_tab = tuple((n - 1) * c / s0 ** 2 for c in crit) if isinstance(crit, tuple) else (n - 1) * crit / s0 ** 2
    res.pasos.append(f"**Equivalente con χ²**: χ²calc = ν·S²/σ₀² = {n - 1}·{fmt(s ** 2, 5)}/{fmt(s0 ** 2, 5)} = "
                     f"{fmt(chi_calc, 4)} contra χ² de tabla = {_cv(chi_tab)}.")
    res.numeros += [chi_calc] + (list(chi_tab) if isinstance(chi_tab, tuple) else [chi_tab])
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
    if d.get("_r_contado") is not None:
        res.pasos.append(f"**Casos**: se contaron {int(d['_r_contado'])} buenas y se pregunta por las malas → "
                         f"r = n - {int(d['_r_contado'])} = {int(n)} - {int(d['_r_contado'])} = {int(r_)}.")
    res.pasos.append(f"**Datos**: n = {int(n)}, r = {int(r_)}, p̂ = r/n = {fmt(int(r_) / int(n), 4)}.")
    res.pasos.append(f"**Modelo exacto** (Beta / F, el que usa la cátedra): A = {fmt(r.a, 4)} ; B = {fmt(r.b, 4)}.")
    res.pasos.append(f"Referencia, aproximación normal: p̂ ∓ Z·√(p̂(1-p̂)/(n-1)) = [{fmt(rn.a, 4)} ; {fmt(rn.b, 4)}] "
                     f"(e = {fmt(rn.error, 4)}).")
    for w in r.warnings:
        res.avisos.append(w)
    # la estimación de la cátedra es el IC exacto: su error es la semiamplitud (B - A)/2 y su relación B/A
    estado["e_actual"] = (r.b - r.a) / 2
    if r.a > 0:
        estado["r_prop"] = r.b / r.a
    if d.get("cota"):
        _cierre_cota(d, r.a, r.b, alpha_orig, "p", res)
        res.numeros += [x * 100 for x in res.numeros]
        return
    res.conclusion = (f"El porcentaje poblacional estará entre {fmt(r.a * 100, 2)}% y {fmt(r.b * 100, 2)}%, con un "
                      f"{_pct(alpha)} de confianza: " + _p("p", r.a, r.b, alpha) + ".")
    res.numeros = [r.a, r.b, r.a * 100, r.b * 100]
    if d.get("r") is not None and d.get("n"):
        res.numeros += [d["r"] / d["n"], 100 * d["r"] / d["n"]]  # p̂
    res.resumen = f"IC p: [{fmt(r.a, 4)} ; {fmt(r.b, 4)}]"


def _n_plan_dado(d, res: Resultado, estado):
    """Plan con r_c fijo: el mayor n con P(aceptar | p₀) = P(r < r_c) ≥ la probabilidad pedida."""
    rc, prob = int(d["rc"]), float(d["prob_aceptar"])
    p0 = _req(d, "p0")[0]
    n = rc
    while n < 1_000_000 and 1 - hyp._prob_rechazo_binomial(n + 1, rc, p0, "derecha") >= prob:
        n += 1
    acepta = 1 - hyp._prob_rechazo_binomial(n, rc, p0, "derecha")
    res.pasos.append(f"**Plan**: se rechaza si r ≥ {rc}. P(aceptar | p₀ = {fmt(p0, 4)}) = P(r ≤ {rc - 1}) decrece con n: "
                     f"el mayor n con P ≥ {fmt(prob, 4)} es n = {n} (P = {fmt(acepta, 4)}).")
    res.conclusion = f"n = {n}: con n mayor la probabilidad de aceptar un lote con p = {fmt(p0, 4)} baja de {fmt(prob, 4)}."
    res.numeros = [n]
    res.resumen = f"n = {n}"
    estado.update(n=n, tail="derecha", rc=rc)
    poi = hyp.n_plan_dado_poisson(p0, rc, prob)
    if poi:
        n_p, m = poi
        res.pasos.append(f"**Por aproximación de Poisson** (como la guía, con la tabla de Poisson: m al 0,1): el mayor m con "
                         f"P(r ≤ {rc - 1} | m) ≥ {fmt(prob, 4)} en la tabla es m = {fmt(m, 1)} → n = m/p₀ = {n_p}.")
        res.conclusion += f" (Por aproximación de Poisson con la tabla: n = {n_p}.)"
        res.numeros.append(n_p)
        res.resumen += f" | Poisson: n = {n_p}"
        estado["n_poisson"] = n_p


def prop_n(d, alpha, res: Resultado, estado):
    if d.get("rc") is not None and d.get("prob_aceptar") is not None:
        _n_plan_dado(d, res, estado)
        return
    p_hat = d.get("p_hat")
    if p_hat is None:
        p_hat = 0.5
        res.avisos.append("Sin estimación previa de p: se usa el caso más desfavorable p̂ = 0,5.")
    e = d.get("e")
    extra = []
    if e is None and d.get("reduccion") is not None and d.get("reduce_relacion"):
        # relación entre límites R = B/A del IC exacto: (p̂ + e)/(p̂ - e) = R' → e = p̂·(R' - 1)/(R' + 1)
        r_act = estado.get("r_prop")
        if r_act is None:
            raise FaltaDato("Falta la relación entre límites actual (calculá antes el IC)")
        r_new = r_act * (1 - d["reduccion"])
        if r_new <= 1:
            raise FaltaDato("La relación pedida queda ≤ 1: revisá la reducción")
        e = p_hat * (r_new - 1) / (r_new + 1)
        res.pasos.append(f"**Relación entre límites**: R = B/A = {fmt(r_act, 5)} → R' = R·(1 - {fmt(d['reduccion'], 4)}) = "
                         f"{fmt(r_new, 5)}. Con la aproximación normal (p̂ + e)/(p̂ - e) = R' → e = p̂·(R' - 1)/(R' + 1) = "
                         f"{fmt(e, 6)}.")
        extra = [r_act, r_new]
    if e is None and d.get("reduccion") is not None:
        e_act = estado.get("e_actual")
        if e_act is None and d.get("n"):
            e_act = ic.ic_proporcion_normal(p_hat, int(d["n"]), alpha).error
        if e_act is None:
            raise FaltaDato("Falta el error actual para aplicar la reducción")
        e = e_act * (1 - d["reduccion"])
        res.pasos.append(f"**Error buscado**: e = {fmt(e_act, 6)}·(1 - {fmt(d['reduccion'], 4)}) = {fmt(e, 6)}.")
        extra = [e_act, e]
    if e is None:
        raise FaltaDato("Falta el error admitido e")
    r = ic.n_proporcion(p_hat, e, alpha)
    z = dist.z_two_tailed(alpha)
    res.pasos.append(f"**Fórmula** (aprox. normal): n = Z²·p̂(1-p̂)/e² + 1 = {fmt(z, 4)}²·{fmt(p_hat, 4)}·{fmt(1 - p_hat, 4)}/"
                     f"{fmt(e, 4)}² + 1 → n = {r.n}.")
    res.conclusion = f"El tamaño de muestra necesario es n = {r.n}."
    res.numeros = [r.n]
    delta = None
    if d.get("n"):
        delta = max(0, r.n - int(d["n"]))
        res.conclusion += f" Respecto de la muestra de {int(d['n'])}: Δn = {delta}."
        res.numeros.append(delta)
    res.numeros += extra
    res.resumen = f"n = {r.n}"
    _costo(d, r.n, delta, res)


def _costo(d, n, delta, res: Resultado):
    """'cada unidad cuesta c': inversión adicional = Δn·c (o total = n·c si no había muestra)."""
    c = d.get("costo_unitario")
    if not c:
        return
    unidades = delta if delta is not None else n
    total = unidades * c
    que = "adicional (Δn·c)" if delta is not None else "total (n·c)"
    res.pasos.append(f"**Costo** {que}: {unidades}·{fmt(c)} = {fmt(total, 2)}.")
    res.conclusion += f" Inversión {que}: {fmt(total, 2)}."
    res.numeros.append(total)


def _beta_plan_dado(d, res: Resultado, estado):
    """P(rechazar) / P(aceptar) con un plan ya fijado (n, r_c) para la proporción pedida."""
    n, rc = int(_req(d, "n")[0]), int(d["rc"])
    tail = d.get("rc_cola") or "derecha"
    p = d.get("p1") if d.get("p1") is not None else d.get("p0")
    if p is None:
        raise FaltaDato("Falta la proporción para la que se pide la probabilidad")
    op = "≥" if tail == "derecha" else "≤"
    pot = hyp._prob_rechazo_binomial(n, rc, p, tail)
    res.pasos.append(f"**Plan dado**: n = {n}; se rechaza si r {op} {rc}.")
    res.pasos.append(f"**Binomial** con p = {fmt(p, 4)}: P(rechazar) = P(r {op} {rc}) = {fmt(pot, 4)}; "
                     f"P(no rechazar / aceptar) = {fmt(1 - pot, 4)}.")
    _cierre_beta(dict(d, p1=p, tail=tail), 1 - pot, pot, res)
    n_p = estado.get("n_poisson")
    if n_p and tail == "derecha":
        from scipy.stats import poisson
        acepta_p = float(poisson.cdf(rc - 1, n_p * p))
        res.pasos.append(f"**Por aproximación de Poisson** (con el n = {n_p} de Poisson): m = n·p = {fmt(n_p * p, 4)}; "
                         f"P(aceptar) = P(r ≤ {rc - 1} | m) = {fmt(acepta_p, 4)}.")
        res.numeros += [acepta_p, 1 - acepta_p]
        res.conclusion += f" (Por aproximación de Poisson: P(aceptar) = {fmt(acepta_p, 4)}.)"
    estado.update(n=n, tail=tail)


def prop_ensayo(d, alpha, res: Resultado, estado, beta_modo=False):
    if beta_modo and d.get("rc") is not None:
        _beta_plan_dado(d, res, estado)
        return
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
        plan_n = estado.get("plan_normal")
        if plan_n and int(n) == estado.get("n") and tail in ("derecha", "izquierda"):
            pot_n = hyp._prob_rechazo_binomial(plan_n[0], plan_n[1], d["p1"], tail)
            res.pasos.append(f"**Con el plan por aproximación normal** (n = {plan_n[0]}, r_c = {plan_n[1]}): "
                             f"1-β = {fmt(pot_n, 4)}, β = {fmt(1 - pot_n, 4)}.")
            res.numeros += [pot_n, 1 - pot_n]
            res.resumen += f" | normal: 1-β = {fmt(pot_n, 4)}"
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


def _plan_dado(d, alpha, res: Resultado, estado):
    """Plan de muestreo ya fijado (n, r_c): riesgos reales, AQL / LTPD o el p del lote 'malo'.

    Se rechaza si r ≥ r_c (si el enunciado da el número de aceptación c, r_c = c + 1)."""
    n, rc = int(d["n"]), int(d["rc"])
    tail = d.get("rc_cola") or "derecha"
    op = "≥" if tail == "derecha" else "≤"
    p0, p1, beta = d.get("p0"), d.get("p1"), d.get("beta")
    h0 = f"p ≤ {fmt(p0, 4)}" if p0 is not None and tail == "derecha" else (f"p ≥ {fmt(p0, 4)}" if p0 is not None else "")
    res.pasos.append(f"**Plan dado**: n = {n}; se rechaza H0 si r {op} {rc}" + (f" (H0: {h0}, criterio optimista)." if h0 else "."))
    numeros, partes = [], []
    if p0 is not None:
        a_real = hyp._prob_rechazo_binomial(n, rc, p0, tail)
        res.pasos.append(f"**Riesgo del proveedor** α = P(r {op} {rc} | n = {n}; p₀ = {fmt(p0, 4)}) = {fmt(a_real, 4)} "
                         f"(binomial exacto).")
        numeros.append(a_real)
        partes.append(f"α = {fmt(a_real, 4)}")
    elif alpha is not None and p1 is None and beta is not None:   # pide AQL y LTPD para (α, β)
        aql = hyp.p_para_aceptacion(n, rc, alpha, tail)
        res.pasos.append(f"**AQL**: p₀ tal que P(rechazar | p₀) = α = {fmt(alpha, 4)} → AQL = p₀ = {fmt(aql, 6)}.")
        numeros.append(aql)
        partes.append(f"AQL = {fmt(aql, 6)}")
    if p1 is not None:
        pot = hyp._prob_rechazo_binomial(n, rc, p1, tail)
        res.pasos.append(f"**Con p₁ = {fmt(p1, 4)}**: β = P(no rechazar) = {fmt(1 - pot, 4)}; potencia = {fmt(pot, 4)}.")
        numeros += [1 - pot, pot]
        partes.append(f"β = {fmt(1 - pot, 4)}")
        n_p = estado.get("n_poisson")
        if n_p and tail == "derecha":
            from scipy.stats import poisson
            b_p = float(poisson.cdf(rc - 1, n_p * p1))
            res.pasos.append(f"**Por aproximación de Poisson** (n = {n_p}): m = n·p₁ = {fmt(n_p * p1, 4)}; "
                             f"β = P(r ≤ {rc - 1} | m) = {fmt(b_p, 4)}.")
            numeros += [b_p, 1 - b_p]
            partes.append(f"Poisson: β = {fmt(b_p, 4)}")
    elif beta is not None:
        ltpd = hyp.p_para_aceptacion(n, rc, 1 - beta, tail)
        res.pasos.append(f"**LTPD / lote malo**: p₁ tal que P(aceptar | p₁) = β = {fmt(beta, 4)} → p₁ = {fmt(ltpd, 6)}.")
        numeros.append(ltpd)
        partes.append(f"p₁ = {fmt(ltpd, 6)}")
    res.conclusion = "; ".join(partes) + "." if partes else "Plan dado: completá p₀ / p₁ o los riesgos."
    res.numeros = numeros
    res.resumen = "; ".join(partes) or "plan dado"
    estado.update(n=n, tail=tail, rc=rc)


def prop_diseno(d, alpha, res: Resultado, estado):
    if d.get("rc") is not None and d.get("n") and not (d.get("p1") is not None and d.get("beta") is not None):
        _plan_dado(d, alpha, res, estado)
        return
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
        try:
            rn = hyp.plan_proporcion_normal(p0, p1, alpha, beta, tail=r.tail)
        except (ValueError, RuntimeError):
            rn = None
        if rn is not None:
            res.pasos.append(f"**Por aproximación normal** (la guía la informa como alternativa): n = [(Z(1-α)·√(p₀q₀) + "
                             f"Z(1-β)·√(p₁q₁))/(p₁ - p₀)]² → n = {rn.n}; con ese n el binomial da r_c = {rn.rc} "
                             f"(α real = {fmt(rn.alpha_real, 4)}, β real = {fmt(rn.beta_real, 4)}).")
            res.conclusion += f" (Por aproximación normal: n = {rn.n} y r_c = {rn.rc}.)"
            res.numeros += [rn.n, rn.rc]
            res.resumen += f" | normal: n = {rn.n}; rc = {rn.rc}"
            estado["plan_normal"] = (rn.n, rn.rc)
        try:
            planes = hyp.planes_factibles(p0, p1, alpha, beta, r.tail)
        except (ValueError, RuntimeError):
            planes = []
        if planes and (len(planes) > 1 or planes[0][1] != planes[0][2]):
            filas = ["| r_c | n mínimo | n máximo |", "|---|---|---|"] + \
                [f"| {rc} | {a} | {b} |" for rc, a, b in planes]
            res.pasos.append("**Otros planes válidos**: para cada r_c, todos los n del rango cumplen α y β (uno de los "
                             "riesgos baja y el otro sube con n). La app informa el menor n; la guía a veces da el mayor del "
                             "rango o usa el r_c siguiente.\n\n" + "\n".join(filas))
            for rc_, a, b in planes:
                res.numeros += [rc_, a, b]
        poi = hyp.plan_poisson_tabla(p0, r.rc, alpha, r.tail)
        if poi:
            n_p, m = poi
            op = "≥" if r.tail == "derecha" else "≤"
            res.pasos.append(f"**Por aproximación de Poisson** (como la guía, con la tabla de Poisson: m al 0,1): con r_c = "
                             f"{r.rc}, m₀ = n·p₀ tal que P(r {op} {r.rc} | m₀) ≤ α en la tabla → m₀ = {fmt(m, 1)} → "
                             f"n = m₀/p₀ = {n_p}.")
            res.numeros.append(n_p)
            res.resumen += f" | Poisson: n = {n_p}"
            res.conclusion += f" (Por aproximación de Poisson con la tabla: n = {n_p}.)"
        estado.update(n=r.n, tail=r.tail, rc=r.rc, n_es_diseno=True)
        return
    if d.get("rc") is not None and d.get("n"):
        _plan_dado(d, alpha, res, estado)
        return
    n = _req(d, "n")[0]
    tail = d.get("tail") or "derecha"
    r = hyp.ensayo_proporcion(int(round(p0 * n)), int(n), p0, alpha, tail=tail, p1=p1)
    op = "≥" if tail == "derecha" else "≤"
    res.pasos.append(f"**Hipótesis**: H0: {r.h0_text}  vs  H1: {r.h1_text}.")
    res.pasos.append(f"**Condición de rechazo**: r_c = {r.critical_value} (binomial n = {int(n)}, p₀ = {fmt(p0, 4)}). "
                     f"Si r {op} {r.critical_value} ⇒ se rechaza H0.")
    res.conclusion = f"Si en la muestra de {int(n)} se encuentran r {op} {r.critical_value}, se rechaza H0."
    res.numeros = list(r.critical_value) if isinstance(r.critical_value, tuple) else [r.critical_value]
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


def _phi_txt(d) -> str:
    a, b = _nombres(d)
    return f"φ = σ({a})/σ({b})"


def _cola_relacion(d, estado) -> str:
    tail = d.get("tail") or estado.get("tail") or "bilateral"
    phi1 = d.get("phi1")
    phi0 = d.get("phi0") or 1.0
    if d.get("orden") == "mayor" and tail != "bilateral":
        tail = "derecha"   # arriba va el de mayor desvío: lo que se quiere probar es que es MAYOR
    if phi1 is not None and tail != "bilateral" and phi1 != phi0:
        tail = "izquierda" if phi1 < phi0 else "derecha"
    return tail


def _criticos_txt(phi0, alpha, df1, df2, tail, crit) -> str:
    if tail == "bilateral":
        c1, c2 = crit
        return (f"j²c₁ = φ₀²·F({fmt(alpha / 2, 4)}; {df1}; {df2}) = {fmt(c1, 4)} y j²c₂ = φ₀²·F({fmt(1 - alpha / 2, 4)}; "
                f"{df1}; {df2}) = {fmt(c2, 4)} (jc = {fmt(sqrt(c1), 4)} ; {fmt(sqrt(c2), 4)})")
    p = alpha if tail == "izquierda" else 1 - alpha
    f = dist.f_value(p, df1, df2)
    return (f"j²c = φ₀²·F({fmt(p, 4)}; {df1}; {df2}) = {fmt(phi0 ** 2, 4)}·{fmt(f, 4)} = {fmt(crit, 4)} "
            f"(jc = {fmt(sqrt(crit), 4)})")


def _cond_relacion(tail, crit) -> str:
    if tail == "bilateral":
        return f"j² < {fmt(crit[0], 4)} o j² > {fmt(crit[1], 4)}"
    return f"j² {_signo(tail)} {fmt(crit, 4)}"


def dos_var_ensayo(d, alpha, res: Resultado, estado, beta_modo=False):
    """TEMA IV: ensayo F sobre φ = σ₁/σ₂ (muestra 1 arriba) contra φ₀ (1 o, p. ej., 0,88 si se pide reducir un 12%)."""
    a, b = _nombres(d)
    phi0 = d.get("phi0") or 1.0
    tail = _cola_relacion(d, estado)
    phi1 = d.get("phi1")
    con_muestras = all(d.get(k) for k in ("s1", "n1", "s2", "n2"))
    if con_muestras:
        s1, n1, s2, n2 = float(d["s1"]), int(d["n1"]), float(d["s2"]), int(d["n2"])
    elif beta_modo and estado.get("n_relacion"):
        s1 = s2 = 1.0   # diseño sin datos: solo hacen falta los valores críticos con el n del diseño
        n1 = n2 = int(estado["n_relacion"])
    else:
        s1, n1, s2, n2 = _req(d, "s1", "n1", "s2", "n2")
    r = two.ensayo_relacion_desvios(s1, int(n1), s2, int(n2), alpha, phi0=phi0, tail=tail, phi1=phi1)
    df1, df2 = int(n1) - 1, int(n2) - 1
    h0, h1 = r.h0_text.replace("φ = σ₁/σ₂", _phi_txt(d)), r.h1_text.replace("φ = σ₁/σ₂", _phi_txt(d))
    res.pasos.append(f"**Hipótesis**: H0: {h0}  vs  H1: {h1}  (α = {fmt(alpha, 4)}).  En varianzas: φ₀² = "
                     f"{fmt(phi0 ** 2, 4)}.")
    res.pasos.append(f"**Estadístico**: j² = S²({a})/S²({b}); bajo H0, j²/φ₀² ~ F(ν₁ = n({a}) - 1 = {df1}; "
                     f"ν₂ = n({b}) - 1 = {df2}).")
    crit = r.critical_value
    res.pasos.append(f"**Condición de rechazo**: {_criticos_txt(phi0, alpha, df1, df2, tail, crit)}. "
                     f"Si {_cond_relacion(tail, crit)} ⇒ se rechaza H0.")
    estado.update(tail=tail, n_relacion=n1 if n1 == n2 else estado.get("n_relacion"))
    res.numeros = (list(crit) + [sqrt(c) for c in crit]) if isinstance(crit, tuple) else [crit, sqrt(crit)]
    if beta_modo:
        if phi1 is None:
            raise FaltaDato("Falta la relación alternativa φ₁ (p. ej. 'reducción del 30%' → φ₁ = 0,70)")
        if tail == "bilateral":
            res.pasos.append(f"**β** = P(no rechazar H0 | φ = {fmt(phi1, 4)}) = {fmt(r.beta, 4)}.")
        else:
            corte = crit / phi1 ** 2
            p_txt = f"P(F({df1}; {df2}) {'<' if tail == 'izquierda' else '>'} j²c/φ₁²)"
            res.pasos.append(f"**Si φ = φ₁ = {fmt(phi1, 4)}** (φ₁² = {fmt(phi1 ** 2, 4)}), j²/φ₁² ~ F({df1}; {df2}). "
                             f"P(rechazar H0) = {p_txt} = P(F {'<' if tail == 'izquierda' else '>'} "
                             f"{fmt(crit, 4)}/{fmt(phi1 ** 2, 4)} = {fmt(corte, 4)}) = {fmt(r.power, 4)}.")
        _cierre_beta(dict(d, phi0=phi0, tail=tail), r.beta, r.power, res)
        return
    j = sqrt(r.observed_value)
    res.pasos.append(f"**Decisión**: j² = {fmt(s1 ** 2, 6)}/{fmt(s2 ** 2, 6)} = {fmt(r.observed_value, 4)} (j = {fmt(j, 4)}) → " +
                     ("cae en la zona de rechazo." if r.rejects_h0 else "no cae en la zona de rechazo."))
    res.conclusion = _ensayo_txt(r, alpha, f"j² = {fmt(r.observed_value, 4)}", d).replace("φ = σ₁/σ₂", _phi_txt(d))
    res.regla = _regla(d, f"calcula la relación j² = S²({a})/S²({b}) con las muestras de {int(n1)} y {int(n2)}",
                       _cond_relacion(tail, crit), h1)
    res.numeros += [r.observed_value, j]
    res.resumen = f"H0: {h0}; j² = {fmt(r.observed_value, 4)} vs j²c = {_cv(crit)}: " + \
                  ("RECHAZA H0" if r.rejects_h0 else "NO rechaza H0")


def dos_var_beta(d, alpha, res: Resultado, estado):
    dos_var_ensayo(d, alpha, res, estado, beta_modo=True)


def dos_var_diseno(d, alpha, res: Resultado, estado):
    """n igual en ambas muestras para una potencia fijada (o, con n dado, solo H0 + CR + RD)."""
    a, b = _nombres(d)
    phi0 = d.get("phi0") or 1.0
    phi1, beta = d.get("phi1"), d.get("beta")
    if phi1 is None or beta is None:
        raise FaltaDato("Para el diseño faltan la relación alternativa φ₁ y/o β")
    tail = _cola_relacion(d, estado)
    r = two.n_relacion_desvios_para_potencia(phi0, phi1, alpha, beta, tail=tail if tail != "bilateral" else None)
    h0, h1 = r.h0_text.replace("φ = σ₁/σ₂", _phi_txt(d)), r.h1_text.replace("φ = σ₁/σ₂", _phi_txt(d))
    nu = r.n - 1
    res.pasos.append(f"**Hipótesis**: H0: {h0}  vs  H1: {h1}.")
    res.pasos.append(f"**Condiciones**: P(rechazar H0 | φ = {fmt(phi0, 4)}) = α = {fmt(alpha, 4)} y "
                     f"P(no rechazar H0 | φ = {fmt(phi1, 4)}) = β = {fmt(beta, 4)}.")
    res.pasos.append(f"**Tamaño de muestra** (n₁ = n₂ = n, ν₁ = ν₂ = n - 1): hay que cumplir R = φ₀²/φ₁² = "
                     f"{fmt(phi0 ** 2, 4)}/{fmt(phi1 ** 2, 4)} = {fmt(max(phi0, phi1) ** 2 / min(phi0, phi1) ** 2, 4)} ≥ "
                     f"F(1-α; ν; ν)·F(1-β; ν; ν). Iterando sobre F: n = {r.n} (ν = {nu}).")
    p = alpha if r.tail == "izquierda" else 1 - alpha
    res.pasos.append(f"**Condición de rechazo**: j²c = φ₀²·F({fmt(p, 4)}; {nu}; {nu}) = {fmt(r.j2_c, 4)} "
                     f"(jc = {fmt(sqrt(r.j2_c), 4)}). Si j² {_signo(r.tail)} {fmt(r.j2_c, 4)} ⇒ se rechaza H0.")
    si, no = _acciones(d, _coma(h1))
    regla = (f"Si en {r.n} muestras de cada grupo la relación j = S({a})/S({b}) es "
             f"{'menor' if r.tail == 'izquierda' else 'mayor'} que {fmt(sqrt(r.j2_c), 4)}, se rechaza H0 → {si}. "
             f"En caso contrario no se rechaza H0 → {no}.")
    res.pasos.append(f"**Regla de decisión**: {_coma(regla)}")
    res.pasos.append(f"Con n = {r.n}: β real = {fmt(r.beta_real, 4)}, potencia real = {fmt(r.potencia_real, 4)}.")
    res.conclusion = f"n = {r.n} en cada muestra ({a} y {b}). " + _coma(regla)
    res.numeros = [r.n, sqrt(r.j2_c), r.j2_c]
    previo = estado.get("n_relacion")
    if previo and r.n > int(previo):
        res.conclusion += f" Respecto de las {int(previo)} anteriores: Δn = {r.n - int(previo)} más en cada una."
        res.numeros.append(r.n - int(previo))
    elif d.get("n1") and d.get("n2"):
        res.conclusion += (f" (Hoy hay {int(d['n1'])} de {a} y {int(d['n2'])} de {b}: Δn = {max(0, r.n - int(d['n1']))} y "
                           f"{max(0, r.n - int(d['n2']))}.)")
    res.resumen = f"n = {r.n}; jc = {fmt(sqrt(r.j2_c), 4)}"
    estado.update(n_relacion=r.n, tail=r.tail)


def dos_var_ic(d, alpha, res: Resultado, estado):
    s1, n1, s2, n2 = _req(d, "s1", "n1", "s2", "n2")
    a, b = _nombres(d)
    df1, df2 = int(n1) - 1, int(n2) - 1
    rd, ri = two.ic_ratio_varianzas(s1, int(n1), s2, int(n2), alpha)
    f_hi, f_lo = dist.f_two_tailed(alpha, df1, df2), dist.f_value(alpha / 2, df1, df2)
    sobre = d.get("sobre") or "varianzas"
    res.pasos.append(f"**Modelo**: (S²₁/σ²₁)/(S²₂/σ²₂) ~ F(ν₁ = {df1}; ν₂ = {df2}); F({fmt(alpha / 2, 4)}) = {fmt(f_lo, 4)}, "
                     f"F({fmt(1 - alpha / 2, 4)}) = {fmt(f_hi, 4)}.")
    res.pasos.append(f"**IC para φ² = σ²({a})/σ²({b})**: j²/F(1-α/2) ; j²/F(α/2) = {fmt(rd.point_estimate, 4)}/{fmt(f_hi, 4)} ; "
                     f"{fmt(rd.point_estimate, 4)}/{fmt(f_lo, 4)} = [{fmt(rd.a, 4)} ; {fmt(rd.b, 4)}]. "
                     f"Inversa σ²({b})/σ²({a}): [{fmt(ri.a, 4)} ; {fmt(ri.b, 4)}].")
    res.pasos.append(f"**IC para φ = σ({a})/σ({b})** (raíz de los límites): [{fmt(sqrt(rd.a), 4)} ; {fmt(sqrt(rd.b), 4)}]. "
                     f"Inversa σ({b})/σ({a}): [{fmt(sqrt(ri.a), 4)} ; {fmt(sqrt(ri.b), 4)}].")
    r_var, r_sig = rd.b / rd.a, sqrt(rd.b / rd.a)
    res.pasos.append(f"**Relación entre límites** B/A: {fmt(r_var, 4)} para las varianzas y {fmt(r_sig, 4)} para los desvíos.")
    estado.update(rel_varianzas=r_var, rel_desvios=r_sig, sobre=sobre)
    lo, hi = (sqrt(rd.a), sqrt(rd.b)) if sobre == "desvios" else (rd.a, rd.b)
    par = f"σ({a})/σ({b})" if sobre == "desvios" else f"σ²({a})/σ²({b})"
    res.conclusion = f"Con un {_pct(alpha)} de confianza: " + _p(par, lo, hi, alpha) + "."
    if sobre == "desvios" and lo > 1:
        res.conclusion += (f" El desvío de {a} es mayor que el de {b} entre un {fmt((lo - 1) * 100, 2)}% y un "
                           f"{fmt((hi - 1) * 100, 2)}%.")
    elif sobre == "desvios" and hi < 1:
        res.conclusion += (f" El desvío de {a} es menor que el de {b} entre un {fmt((1 - hi) * 100, 2)}% y un "
                           f"{fmt((1 - lo) * 100, 2)}%.")
    res.numeros = [rd.a, rd.b, ri.a, ri.b, sqrt(rd.a), sqrt(rd.b), sqrt(ri.a), sqrt(ri.b), lo - 1, hi - 1, 1 - lo, 1 - hi]
    res.resumen = f"IC {par}: [{fmt(lo, 4)} ; {fmt(hi, 4)}]"


def dos_var_n(d, alpha, res: Resultado, estado):
    """n igual en ambas muestras para que el IC de la relación tenga una relación entre límites dada."""
    sobre = d.get("sobre") or estado.get("sobre") or "varianzas"
    clave = "rel_desvios" if sobre == "desvios" else "rel_varianzas"
    rel = d.get("relacion")
    r_act = None
    if rel is None and d.get("reduccion") is not None:
        r_act = estado.get(clave)
        if r_act is None:
            s1, n1, s2, n2 = _req(d, "s1", "n1", "s2", "n2")
            r_act = two.relacion_limites_f(alpha, int(n1) - 1, int(n2) - 1, sobre)
        rel = r_act * (1 - d["reduccion"])
        res.pasos.append(f"**Relación buscada** B/A = {fmt(r_act, 4)}·(1 - {fmt(d['reduccion'], 4)}) = {fmt(rel, 4)} "
                         f"({'desvíos' if sobre == 'desvios' else 'varianzas'}).")
    elif rel is not None:
        res.pasos.append(f"**Relación buscada** B/A = {fmt(rel, 4)} ({'desvíos' if sobre == 'desvios' else 'varianzas'}).")
    else:
        raise FaltaDato("Falta la relación entre límites buscada o la reducción pedida")
    r = two.n_relacion_por_limites(rel, alpha, sobre=sobre, r_actual=r_act, reduccion=d.get("reduccion"))
    nu = r.n - 1
    formula = "F(1-α/2; ν; ν)/F(α/2; ν; ν)" if sobre == "varianzas" else "√[F(1-α/2; ν; ν)/F(α/2; ν; ν)]"
    res.pasos.append(f"Con n₁ = n₂ = n la relación entre límites ya no depende de los desvíos: B/A = {formula}. "
                     f"Iterando sobre F: n = {r.n} (ν = {nu}) da B/A = {fmt(r.r_logrado, 4)} ≤ {fmt(rel, 4)}.")
    res.conclusion = f"Se necesitan n = {r.n} unidades en cada muestra (ν = {nu})."
    res.numeros = [r.n, nu]
    if d.get("n1") and d.get("n2"):
        res.conclusion += f" (Hoy hay {int(d['n1'])} y {int(d['n2'])}: Δn = {max(0, r.n - int(d['n1']))} y {max(0, r.n - int(d['n2']))}.)"
    res.resumen = f"n = {r.n}"


# TEMA V (comparación de dos medias): interprete/dos_muestras.py (se registra en DESPACHO_EXTRA).


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
    res.numeros = [r.chi2_calc, r.chi2_critico, float(r.df)]
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
    res.numeros = [r.chi2_calc, r.chi2_critico, float(r.df)]
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
    ("dos_varianzas", "beta"): dos_var_beta, ("dos_varianzas", "diseno"): dos_var_diseno, ("dos_varianzas", "n"): dos_var_n,
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
        propia = d.get("tail_mu" if tema == "media" else "tail_sigma")
        if propia:
            dd["tail"] = propia   # cada condición tiene su dirección (μ > 4,6 pero σ < 0,55)
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


def _alternativas(d, f, res: Resultado, estado):
    """Varias alternativas de planteo (cada una con su H0, α, β y valor alternativo): se resuelve cada una."""
    resumenes, conclusiones = [], []
    distintos = len({a.get("_criterio") for a in d["alternativas"]}) > 1   # si todos dicen lo mismo no informa
    for alt in d["alternativas"]:
        if not distintos:
            alt = dict(alt, _criterio=None)
        dd = {k: v for k, v in d.items() if k != "alternativas"}
        dd.update({k: v for k, v in alt.items() if not k.startswith("_")})
        sub = Resultado()
        f(dd, float(dd.get("alpha", 0.05)), sub, estado)
        crit = f" (criterio {alt['_criterio']})" if alt.get("_criterio") else ""
        res.pasos.append(f"**— {alt['_nombre']}{crit} —**")
        res.pasos += sub.pasos
        res.numeros += sub.numeros
        resumenes.append(f"{alt['_nombre']}: {sub.resumen}")
        conclusiones.append(f"{alt['_nombre']}: {sub.conclusion}")
    res.resumen = " | ".join(resumenes)
    res.conclusion = " ".join(conclusiones)


def resolver_inciso(an: Analisis, inc: Inciso, estado: Dict) -> Resultado:
    res = Resultado(titulo=f"{inc.letra}) {TITULOS.get(inc.tipo) or TIPOS.get(inc.tipo, 'Sin cálculo')}")
    tema = inc.params.get("tema") or an.tema   # un inciso puede ser de otro parámetro que el planteo
    f = DESPACHO_EXTRA.get((tema, inc.tipo)) or DESPACHO.get((tema, inc.tipo))
    if f is None:
        res.errores.append("La app no calcula este tipo de pregunta para este tema. "
                           "Mirá la teoría y los ejercicios parecidos de la guía.")
        res.resumen = "sin cálculo"
        return res
    try:
        d = _datos(an, inc, estado)
        alpha = d.get("alpha")
        if alpha is None and tema.startswith("regresion"):
            alpha = 0.05
            if inc.tipo not in ("recta", "origen") and not d.get("puntual"):
                res.avisos.append("El inciso no fija el riesgo α: se usó α = 0,05.")
        if alpha is None and inc.tipo == "ensayo":
            alpha = 0.05
            res.avisos.append("El enunciado no fija el riesgo α: se usó α = 0,05. Mirá el valor a posteriori α*: "
                              "se rechaza H0 para cualquier α ≥ α* (así lo responde la guía en estos casos).")
        if alpha is None:
            raise FaltaDato("Falta el riesgo α")
        _paso_resumen(d, res) if tema in ("media", "varianza") else None
        cola_previa = estado.get("tail")
        if d.get("ambos") and tema in ("media", "varianza") and inc.tipo in ("ensayo", "ic"):
            _ambos(d, float(alpha), inc.tipo, res, estado)
        elif d.get("alternativas"):
            _alternativas(d, f, res, estado)
        else:
            f(d, float(alpha), res, estado)
        # la cola efectiva: la que fijó este inciso (un diseño la corrige según μ₁) o la del inciso
        cola = estado.get("tail") if estado.get("tail") != cola_previa else (d.get("tail") or estado.get("tail"))
        res.pasos = agregar_presentacion(res.pasos, tema, inc.tipo, dict(d, alpha=alpha), an.criterio, cola)
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
