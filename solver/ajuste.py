"""Bondad de ajuste χ² a un modelo (TEMA VI), calculando las frecuencias esperadas.

Sigue el apunte de la cátedra ("Contrastes Chi Cuadrado", Dopazo):
- Los parámetros desconocidos se estiman por momentos con las marcas de clase: μ ≈ x̄ y
  σ ≈ S (desvío corregido, n-1). Cada parámetro estimado resta un grado de libertad.
- La primera y la última clase se extienden hasta el borde del dominio del modelo
  (la primera es F(ls₁), la última es G(li_k) = 1 - F(li_k)).
- Las clases con frecuencia esperada < 5 se amalgaman con la vecina (de los extremos hacia adentro).
- ν = k - 1 - p, con k = clases efectivas (después de amalgamar) y p = parámetros estimados.

Modelos discretos: uniforme, binomial, poisson. Continuos: uniforme_continua, normal,
lognormal, exponencial, gamma, weibull, gumbel_max, gumbel_min, pareto.
"""

from dataclasses import dataclass, field
from math import exp, gamma as G, log, pi, sqrt
from typing import Dict, List, Optional, Sequence, Tuple

from scipy import stats
from scipy.optimize import brentq

from . import distributions as dist

EULER = 0.5772156649

NOMBRES = {
    "uniforme": "Uniforme discreto", "binomial": "Binomial", "poisson": "Poisson",
    "uniforme_continua": "Uniforme (continuo)", "normal": "Normal", "lognormal": "Log-Normal",
    "exponencial": "Exponencial", "gamma": "Gamma", "weibull": "Weibull",
    "gumbel_max": "Gumbel del máximo", "gumbel_min": "Gumbel del mínimo", "pareto": "Pareto",
}
DISCRETOS = {"uniforme", "binomial", "poisson"}


@dataclass
class Clase:
    etiqueta: str
    fo: float
    prob: float
    fe: float


@dataclass
class AjusteResult:
    modelo: str
    parametros: Dict[str, float]
    estimados: List[str]  # nombres de los parámetros estimados con la muestra
    media: Optional[float]
    desvio: Optional[float]
    tabla: List[Clase]  # antes de amalgamar
    tabla_final: List[Clase]  # la que se ensaya
    chi2_calc: float
    df: int
    chi2_critico: float
    rechaza: bool
    alpha: float
    avisos: List[str] = field(default_factory=list)


# ---------------------------------------------------------------- estimación por momentos

def _momentos(marcas: Sequence[float], fo: Sequence[float]) -> Tuple[float, float]:
    N = sum(fo)
    m = sum(x * f for x, f in zip(marcas, fo)) / N
    s2 = sum(f * (x - m) ** 2 for x, f in zip(marcas, fo)) / (N - 1)
    return m, sqrt(s2)


def _weibull_forma(cv: float) -> float:
    """Forma w tal que el coeficiente de variación de la Weibull sea cv (tabla de la cátedra)."""
    def f(w):
        g1 = G(1 + 1 / w)
        return sqrt(G(1 + 2 / w) - g1 * g1) / g1 - cv
    return brentq(f, 0.05, 100)


def _cdf(modelo: str, prm: Dict[str, float]):
    if modelo == "normal":
        return lambda x: stats.norm.cdf(x, prm["mu"], prm["sigma"])
    if modelo == "lognormal":
        return lambda x: 0.0 if x <= 0 else stats.norm.cdf((log(x) - prm["m"]) / prm["D"])
    if modelo == "exponencial":
        return lambda x: 0.0 if x <= 0 else 1 - exp(-prm["lambda"] * x)
    if modelo == "gamma":
        return lambda x: 0.0 if x <= 0 else stats.gamma.cdf(x, prm["r"], scale=1 / prm["lambda"])
    if modelo == "weibull":
        return lambda x: 0.0 if x <= 0 else 1 - exp(-((x / prm["beta"]) ** prm["w"]))
    if modelo == "gumbel_max":
        return lambda x: exp(-exp(-(x - prm["u"]) / prm["beta"]))
    if modelo == "gumbel_min":
        return lambda x: 1 - exp(-exp((x - prm["u"]) / prm["beta"]))
    if modelo == "pareto":
        return lambda x: 0.0 if x <= prm["alpha"] else 1 - (prm["alpha"] / x) ** prm["b"]
    if modelo == "uniforme_continua":
        return lambda x: min(1.0, max(0.0, (x - prm["a"]) / (prm["b"] - prm["a"])))
    raise ValueError(f"Modelo desconocido: {modelo}")


def estimar_continuo(modelo: str, m: float, s: float, conocidos: Dict[str, float],
                     limites: Sequence[Tuple[float, float]]) -> Tuple[Dict[str, float], List[str]]:
    """Parámetros del modelo por momentos (los que vienen en `conocidos` no se estiman)."""
    p = dict(conocidos)
    est = []

    def falta(*nombres):
        faltan = [n for n in nombres if n not in p]
        est.extend(faltan)
        return faltan

    if modelo == "normal":
        if falta("mu"):
            p["mu"] = m
        if falta("sigma"):
            p["sigma"] = s
    elif modelo == "lognormal":
        if "m" not in p or "D" not in p:
            D2 = log(1 + (s / m) ** 2)
            if falta("m"):
                p["m"] = log(m) - D2 / 2
            if falta("D"):
                p["D"] = sqrt(D2)
    elif modelo == "exponencial":
        if falta("lambda"):
            p["lambda"] = 1 / m
    elif modelo == "gamma":
        if falta("r"):
            p["r"] = (m / s) ** 2
        if falta("lambda"):
            p["lambda"] = m / s ** 2
    elif modelo == "weibull":
        if falta("w"):
            p["w"] = _weibull_forma(s / m)
        if falta("beta"):
            p["beta"] = m / G(1 + 1 / p["w"])
    elif modelo in ("gumbel_max", "gumbel_min"):
        if falta("beta"):
            p["beta"] = s * sqrt(6) / pi
        if falta("u"):
            p["u"] = m - EULER * p["beta"] if modelo == "gumbel_max" else m + EULER * p["beta"]
    elif modelo == "pareto":
        if falta("alpha"):
            p["alpha"] = limites[0][0]
        if falta("b"):
            p["b"] = m / (m - p["alpha"])
    elif modelo == "uniforme_continua":
        if falta("a"):
            p["a"] = limites[0][0]
        if falta("b"):
            p["b"] = limites[-1][1]
        est = []  # los extremos del recorrido no se estiman con momentos
    return p, est


# ---------------------------------------------------------------- amalgamado

def amalgamar(tabla: List[Clase], minimo: float = 5) -> List[Clase]:
    t = [Clase(c.etiqueta, c.fo, c.prob, c.fe) for c in tabla]

    def unir(i, j):  # une la clase j dentro de la i (adyacentes)
        a, b = (t[i], t[j]) if i < j else (t[j], t[i])
        ini = a.etiqueta.split(" a ")[0] if " a " in a.etiqueta else a.etiqueta
        fin = b.etiqueta.split(" a ")[-1] if " a " in b.etiqueta else b.etiqueta
        nueva = Clase(f"{ini} a {fin}", a.fo + b.fo, a.prob + b.prob, a.fe + b.fe)
        k = min(i, j)
        t[k:k + 2] = [nueva]

    while len(t) > 1 and t[0].fe < minimo:
        unir(0, 1)
    while len(t) > 1 and t[-1].fe < minimo:
        unir(len(t) - 1, len(t) - 2)
    i = 1
    while i < len(t) - 1:
        if t[i].fe < minimo:
            vecino = i - 1 if t[i - 1].fe <= t[i + 1].fe else i + 1
            unir(i, vecino)
            i = max(1, i - 1)
        else:
            i += 1
    return t


def _contraste(modelo, prm, est, m, s, tabla, alpha, avisos, extra_df=0):
    final = amalgamar(tabla)
    if len(final) < len(tabla):
        avisos.append(f"Se amalgamaron clases con Fe < 5: de {len(tabla)} a {len(final)} clases efectivas.")
    N = sum(c.fo for c in tabla)
    if N < 60:
        avisos.append(f"N = {N:g} < 60: la aproximación χ² exige N ≥ 60 (profesor en clase).")
    chi2 = sum((c.fo - c.fe) ** 2 / c.fe for c in final)
    df = len(final) - 1 - len(est) - extra_df
    if df <= 0:
        raise ValueError(f"Grados de libertad no válidos (ν = {df}): hay pocas clases para el modelo.")
    crit = dist.chi2_one_tailed(alpha, df)
    from .chi_square import aviso_demasiado_perfecto
    perfecto = aviso_demasiado_perfecto(chi2, df, alpha)
    if perfecto:
        avisos.append(perfecto)
    return AjusteResult(modelo=modelo, parametros=prm, estimados=est, media=m, desvio=s, tabla=tabla,
                        tabla_final=final, chi2_calc=chi2, df=df, chi2_critico=crit, rechaza=chi2 > crit,
                        alpha=alpha, avisos=avisos)


# ---------------------------------------------------------------- API

def ajuste_continuo(modelo: str, limites: Sequence[Tuple[float, float]], fo: Sequence[float], alpha: float,
                    conocidos: Optional[Dict[str, float]] = None, extremos_abiertos: bool = True) -> AjusteResult:
    """`limites` = [(li, ls), ...] de cada clase en orden; `fo` = frecuencias observadas."""
    if len(limites) != len(fo):
        raise ValueError("Cantidad de clases y de frecuencias distinta")
    marcas = [(a + b) / 2 for a, b in limites]
    m, s = _momentos(marcas, fo)
    prm, est = estimar_continuo(modelo, m, s, conocidos or {}, limites)
    F = _cdf(modelo, prm)
    N = sum(fo)
    tabla = []
    k = len(limites)
    for i, ((a, b), f) in enumerate(zip(limites, fo)):
        Fa = 0.0 if (extremos_abiertos and i == 0) else F(a)
        Fb = 1.0 if (extremos_abiertos and i == k - 1) else F(b)
        prob = Fb - Fa
        tabla.append(Clase(f"{a:g} a {b:g}", f, prob, N * prob))
    return _contraste(modelo, prm, est, m, s, tabla, alpha, [])


def ajuste_discreto(modelo: str, valores: Sequence[float], fo: Sequence[float], alpha: float,
                    conocidos: Optional[Dict[str, float]] = None, ultima_abierta: bool = True) -> AjusteResult:
    """`valores` = valores de la variable (r = 0, 1, 2...) o categorías (uniforme)."""
    conocidos = dict(conocidos or {})
    N = sum(fo)
    k = len(fo)
    avisos = []
    est: List[str] = []
    m = s = None
    if modelo == "uniforme":
        probs = conocidos.get("probs") or [1 / k] * k
        prm = {"k": k}
        tabla = [Clase(str(v), f, p, N * p) for v, f, p in zip(valores, fo, probs)]
        return _contraste(modelo, prm, est, m, s, tabla, alpha, avisos)
    vals = [float(v) for v in valores]
    m = sum(v * f for v, f in zip(vals, fo)) / N
    if modelo == "poisson":
        if "m" not in conocidos:
            conocidos["m"] = m
            est.append("m")
        lam = conocidos["m"]
        pmf = lambda r: stats.poisson.pmf(r, lam)
        cdf = lambda r: stats.poisson.cdf(r, lam)
    elif modelo == "binomial":
        n = int(conocidos["n"])
        if "p" not in conocidos:
            conocidos["p"] = m / n
            est.append("p")
        p = conocidos["p"]
        pmf = lambda r: stats.binom.pmf(r, n, p)
        cdf = lambda r: stats.binom.cdf(r, n, p)
    else:
        raise ValueError(f"Modelo discreto desconocido: {modelo}")
    # Completar el dominio como el profesor (22/10): las clases observadas llevan la probabilidad PUNTUAL y se agrega
    # una clase al principio y/o al final con O = 0 y la probabilidad ACUMULADA (F o G), no la puntual.
    tabla = []
    if vals[0] > 0 and cdf(vals[0] - 1) > 0:
        tabla.append(Clase(f"≤ {vals[0] - 1:g}", 0.0, cdf(vals[0] - 1), N * cdf(vals[0] - 1)))
        avisos.append(f"Se completó el dominio al principio con la clase «≤ {vals[0] - 1:g}» (O = 0, probabilidad "
                      f"acumulada F({vals[0] - 1:g})).")
    for v, f in zip(vals, fo):
        tabla.append(Clase(f"{v:g}", f, pmf(v), N * pmf(v)))
    cola = 1 - cdf(vals[-1])
    if ultima_abierta and cola > 1e-12:
        tabla.append(Clase(f"≥ {vals[-1] + 1:g}", 0.0, cola, N * cola))
        avisos.append(f"Se completó el dominio al final con la clase «≥ {vals[-1] + 1:g}» (O = 0, probabilidad "
                      f"acumulada G({vals[-1] + 1:g}) = {cola:.4f}), no la puntual.")
    return _contraste(modelo, conocidos, est, m, None, tabla, alpha, avisos)
