"""Regresión y correlación (TEMA VII simple, TEMA VIII modelo lineal general).

Sigue la teoría de la cátedra (Dopazo, "Teoría de la Regresión y Análisis de Correlación"):

- Recta de mínimos cuadrados ŷ = b0 + b1·x, S² = SCR/(n-2), r, r².
- Ensayo de β1 (H0: β1 = β10) con t de Student, ν = n-2, S_b1 = S/√(Σx² - n·x̄²).
- IC para ρ por la transformación de Fisher (Z = ½·ln((1+r)/(1-r)) ± z/√(n-3)).
- IC para β1, para la ley promedio (μ_y|x0) y de predicción (y individual en x0).
- Modelos linealizables: log-log, log-lin (ln y = a + b·x), lin-log (y = a + b·ln x),
  exponencial e inverso. Se ajusta la recta sobre las variables transformadas.
- Regresión múltiple: b = (X'X)⁻¹X'y, S² = SCR/(n-p), R², R² ajustado, F global, t parciales
  con C_ii de la diagonal de (X'X)⁻¹, PRESS, DET (determinante de la matriz de correlaciones de
  las explicativas), Cp de Mallows y VIF; tabla de selección de todos los modelos candidatos.
"""

from dataclasses import dataclass, field
from itertools import combinations
from math import atanh, exp, log, sqrt, tanh
from typing import Dict, List, Optional, Sequence

import numpy as np

from .distributions import f_value, t_value, z_value

TRANSFORMACIONES = {
    "lineal": ("y", "x", "ŷ = b0 + b1·x"),
    "loglog": ("ln y", "ln x", "ln ŷ = b0 + b1·ln x  (y = e^b0 · x^b1, elasticidad constante)"),
    "loglin": ("ln y", "x", "ln ŷ = b0 + b1·x  (y = e^b0 · e^(b1·x))"),
    "linlog": ("y", "ln x", "ŷ = b0 + b1·ln x"),
    "inversa": ("y", "1/x", "ŷ = b0 + b1·(1/x)"),
}


def _tx(v: float, que: str) -> float:
    if que.startswith("ln"):
        return log(v)
    if que == "1/x":
        return 1 / v
    return v


@dataclass
class RegresionSimple:
    n: int
    b0: float
    b1: float
    xbar: float
    ybar: float
    sum_x2: float
    sum_y2: float
    sum_xy: float
    Sxx: float  # Σx² - n·x̄²
    Syy: float
    Sxy: float
    SCR: float
    SCE: float
    SCT: float
    S2: float
    S: float
    r: float
    r2: float
    Sb1: float
    Sb0: float
    nu: int
    modelo: str = "lineal"
    origen: bool = False
    x: List[float] = field(default_factory=list)  # ya transformadas
    y: List[float] = field(default_factory=list)

    def predecir(self, x0: float) -> float:
        """ŷ en la escala transformada (x0 en la escala original)."""
        return self.b0 + self.b1 * _tx(x0, TRANSFORMACIONES[self.modelo][1])

    def a_original(self, v: float) -> float:
        """Vuelve un valor de ŷ (escala transformada) a la escala original de y."""
        return exp(v) if TRANSFORMACIONES[self.modelo][0].startswith("ln") else v

    def ecuacion(self, dec: int = 4) -> str:
        yv, xv, _ = TRANSFORMACIONES[self.modelo]
        signo = "+" if self.b1 >= 0 else "-"
        yv = "ŷ" if yv == "y" else yv.replace("y", "ŷ")
        if self.origen:
            return f"{yv} = {self.b1:.{dec}f}·{xv}"
        return f"{yv} = {self.b0:.{dec}f} {signo} {abs(self.b1):.{dec}f}·{xv}"


def ajustar_simple(x: Sequence[float], y: Sequence[float], modelo: str = "lineal",
                   origen: bool = False) -> RegresionSimple:
    if len(x) != len(y):
        raise ValueError("x e y deben tener la misma cantidad de datos")
    if len(x) < 3:
        raise ValueError("Se necesitan al menos 3 puntos")
    ty, tx, _ = TRANSFORMACIONES[modelo]
    X = [_tx(v, tx) for v in x]
    Y = [_tx(v, "ln y" if ty.startswith("ln") else "y") for v in y]
    reg = desde_sumatorias(len(X), sum(X), sum(v * v for v in X), sum(Y), sum(v * v for v in Y),
                           sum(a * b for a, b in zip(X, Y)), modelo=modelo, origen=origen)
    reg.x, reg.y = X, Y
    return reg


def desde_sumatorias(n: int, sx: float, sxx: float, sy: float, syy: float, sxy: float,
                     modelo: str = "lineal", origen: bool = False) -> RegresionSimple:
    """La recta a partir de las sumatorias (Σx, Σx², Σy, Σy², Σxy), como las da la guía a veces."""
    n = int(n)
    xbar, ybar = sx / n, sy / n
    Sxx = sxx - n * xbar ** 2
    Syy = syy - n * ybar ** 2
    Sxy = sxy - n * xbar * ybar
    if origen:
        b1 = sxy / sxx
        b0 = 0.0
        SCR = syy - b1 * sxy
        nu = n - 1
        SCT = syy
    else:
        b1 = Sxy / Sxx
        b0 = ybar - b1 * xbar
        SCR = syy - b0 * sy - b1 * sxy
        nu = n - 2
        SCT = Syy
    SCE = SCT - SCR
    S2 = SCR / nu
    r = Sxy / sqrt(Sxx * Syy) if Sxx > 0 and Syy > 0 else 0.0
    Sb1 = sqrt(S2 / (sxx if origen else Sxx))
    Sb0 = 0.0 if origen else sqrt(S2 * sxx / (n * Sxx))
    return RegresionSimple(n=n, b0=b0, b1=b1, xbar=xbar, ybar=ybar, sum_x2=sxx, sum_y2=syy, sum_xy=sxy,
                           Sxx=Sxx, Syy=Syy, Sxy=Sxy, SCR=SCR, SCE=SCE, SCT=SCT, S2=S2, S=sqrt(S2),
                           r=r, r2=r * r, Sb1=Sb1, Sb0=Sb0, nu=nu, modelo=modelo, origen=origen)


# ---------------------------------------------------------------- ensayos e intervalos (simple)

@dataclass
class EnsayoCoef:
    h0: str
    h1: str
    tail: str
    alpha: float
    estimado: float
    error_std: float
    t_c: float
    t_critico: float  # positivo; en bilateral es t(1-α/2)
    b_critico: tuple  # valores críticos sobre b (uno o dos)
    nu: int
    rechaza: bool
    p_valor: float


def _t_crit(alpha: float, nu: int, tail: str) -> float:
    return t_value(1 - alpha / 2, nu) if tail == "bilateral" else t_value(1 - alpha, nu)


def _p_valor_t(t_c: float, nu: int, tail: str) -> float:
    from scipy.stats import t as tdist
    if tail == "bilateral":
        return 2 * tdist.sf(abs(t_c), nu)
    if tail == "derecha":
        return tdist.sf(t_c, nu)
    return tdist.cdf(t_c, nu)


def ensayo_beta1(reg: RegresionSimple, alpha: float, beta10: float = 0.0,
                 tail: str = "bilateral") -> EnsayoCoef:
    """H0: β1 = β10 (o ≤ / ≥ según la cola). tail="existencia" es la validación de la cátedra (|t| > t(1-α))."""
    t_c = (reg.b1 - beta10) / reg.Sb1
    tc = _t_crit(alpha, reg.nu, tail)
    if tail == "existencia":
        # criterio de la cátedra para validar la relación: |tc| > t(1-α; ν)
        tc = t_value(1 - alpha, reg.nu)
        return EnsayoCoef(h0="β1 = 0 (ρ = 0)", h1="β1 ≠ 0 (existe relación lineal)", tail=tail, alpha=alpha,
                          estimado=reg.b1, error_std=reg.Sb1, t_c=t_c, t_critico=tc, b_critico=(), nu=reg.nu,
                          rechaza=abs(t_c) > tc, p_valor=_p_valor_t(t_c, reg.nu, "bilateral"))
    if tail == "bilateral":
        rechaza = abs(t_c) > tc
        crit = (beta10 - tc * reg.Sb1, beta10 + tc * reg.Sb1)
        h0, h1 = f"β1 = {beta10:g}", f"β1 ≠ {beta10:g}"
    elif tail == "derecha":
        rechaza = t_c > tc
        crit = (beta10 + tc * reg.Sb1,)
        h0, h1 = f"β1 ≤ {beta10:g}", f"β1 > {beta10:g}"
    else:
        rechaza = t_c < -tc
        crit = (beta10 - tc * reg.Sb1,)
        h0, h1 = f"β1 ≥ {beta10:g}", f"β1 < {beta10:g}"
    return EnsayoCoef(h0=h0, h1=h1, tail=tail, alpha=alpha, estimado=reg.b1, error_std=reg.Sb1, t_c=t_c,
                      t_critico=tc, b_critico=crit, nu=reg.nu, rechaza=rechaza,
                      p_valor=_p_valor_t(t_c, reg.nu, tail))


def ensayo_rho(reg: RegresionSimple, alpha: float) -> EnsayoCoef:
    """H0: ρ = 0 con t = r·√(n-2)/√(1-r²) (equivale al ensayo de β1 = 0)."""
    nu = reg.n - 2
    t_c = reg.r * sqrt(nu) / sqrt(1 - reg.r2)
    tc = _t_crit(alpha, nu, "bilateral")
    return EnsayoCoef(h0="ρ = 0", h1="ρ ≠ 0", tail="bilateral", alpha=alpha, estimado=reg.r,
                      error_std=sqrt((1 - reg.r2) / nu), t_c=t_c, t_critico=tc, b_critico=(), nu=nu,
                      rechaza=abs(t_c) > tc, p_valor=_p_valor_t(t_c, nu, "bilateral"))


@dataclass
class IntervaloReg:
    que: str
    A: Optional[float]
    B: Optional[float]
    centro: float
    error: float
    critico: float
    nu: Optional[int]
    A_orig: Optional[float] = None  # en escala original si el modelo transforma y
    B_orig: Optional[float] = None
    centro_orig: Optional[float] = None


def _limites(centro, error, cola):
    if cola == "inferior":  # mínimo con probabilidad 1-α
        return centro - error, None
    if cola == "superior":
        return None, centro + error
    return centro - error, centro + error


def ic_beta1(reg: RegresionSimple, alpha: float, cola: str = "bilateral") -> IntervaloReg:
    tc = t_value(1 - alpha / 2, reg.nu) if cola == "bilateral" else t_value(1 - alpha, reg.nu)
    e = tc * reg.Sb1
    A, B = _limites(reg.b1, e, cola)
    return IntervaloReg("β1", A, B, reg.b1, e, tc, reg.nu)


def ic_beta0(reg: RegresionSimple, alpha: float) -> IntervaloReg:
    tc = t_value(1 - alpha / 2, reg.nu)
    e = tc * reg.Sb0
    return IntervaloReg("β0", reg.b0 - e, reg.b0 + e, reg.b0, e, tc, reg.nu)


def ic_rho(reg: RegresionSimple, alpha: float) -> IntervaloReg:
    z = atanh(reg.r)
    zc = z_value(1 - alpha / 2)
    e = zc / sqrt(reg.n - 3)
    return IntervaloReg("ρ", tanh(z - e), tanh(z + e), reg.r, e, zc, None)


def _ic_y(reg: RegresionSimple, x0: float, alpha: float, cola: str, individual: bool) -> IntervaloReg:
    x0t = _tx(x0, TRANSFORMACIONES[reg.modelo][1])
    centro = reg.b0 + reg.b1 * x0t
    tc = t_value(1 - alpha / 2, reg.nu) if cola == "bilateral" else t_value(1 - alpha, reg.nu)
    if reg.origen:
        var = x0t ** 2 / reg.sum_x2
    else:
        var = 1 / reg.n + (x0t - reg.xbar) ** 2 / reg.Sxx
    if individual:
        var += 1
    e = tc * reg.S * sqrt(var)
    A, B = _limites(centro, e, cola)
    que = "y individual (pronóstico)" if individual else "ley promedio μ(y|x0)"
    res = IntervaloReg(que, A, B, centro, e, tc, reg.nu)
    if TRANSFORMACIONES[reg.modelo][0].startswith("ln"):
        res.centro_orig = exp(centro)
        res.A_orig = exp(A) if A is not None else None
        res.B_orig = exp(B) if B is not None else None
    return res


def ic_media_y(reg: RegresionSimple, x0: float, alpha: float, cola: str = "bilateral") -> IntervaloReg:
    return _ic_y(reg, x0, alpha, cola, individual=False)


def ic_prediccion(reg: RegresionSimple, x0: float, alpha: float, cola: str = "bilateral") -> IntervaloReg:
    return _ic_y(reg, x0, alpha, cola, individual=True)


def validez_por_r2(r2: float) -> str:
    """Segundo criterio de validación de la cátedra (fuerza de la relación)."""
    if r2 >= 0.9:
        return "r² ≥ 0,9: el modelo es válido para cualquier campo de aplicación"
    if r2 >= 0.8:
        return "r² ≥ 0,8: válido para procesos físicos e industriales"
    if r2 >= 0.6:
        return "r² ≥ 0,6: válido para econometría (variables macro y microeconómicas)"
    if r2 >= 0.4:
        return "r² ≥ 0,4: válido solo para sociología o psicología"
    return "r² < 0,4: la relación es débil, el modelo no es útil"


# ---------------------------------------------------------------- regresión múltiple

@dataclass
class RegresionMultiple:
    nombres: List[str]
    n: int
    k: int
    p: int
    b: List[float]
    SCR: float
    SCE: float
    SCT: float
    S2: float
    S: float
    R2: float
    R2aj: float
    F_c: float
    C: List[float]  # diagonal de (X'X)^-1, empezando por b0
    Sb: List[float]
    t_c: List[float]
    PRESS: float
    DET: float
    VIF: List[float]
    XtX_inv: List[List[float]] = field(default_factory=list)

    def ecuacion(self, dec: int = 4) -> str:
        s = f"ŷ = {self.b[0]:.{dec}f}"
        for bi, nom in zip(self.b[1:], self.nombres):
            s += f" {'+' if bi >= 0 else '-'} {abs(bi):.{dec}f}·{nom}"
        return s


def _corr_det(cols: List[np.ndarray]) -> float:
    if len(cols) < 2:
        return 1.0
    return float(np.linalg.det(np.corrcoef(np.vstack(cols))))


def ajustar_multiple(xs: List[Sequence[float]], y: Sequence[float], nombres: Optional[List[str]] = None
                     ) -> RegresionMultiple:
    Y = np.asarray(y, dtype=float)
    cols = [np.asarray(c, dtype=float) for c in xs]
    n, k = len(Y), len(cols)
    nombres = nombres or [f"x{i + 1}" for i in range(k)]
    p = k + 1
    if n <= p:
        raise ValueError("Hay menos observaciones que parámetros")
    X = np.column_stack([np.ones(n)] + cols)
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ Y
    yhat = X @ b
    res = Y - yhat
    SCR = float(res @ res)
    SCT = float(((Y - Y.mean()) ** 2).sum())
    SCE = SCT - SCR
    S2 = SCR / (n - p)
    R2 = SCE / SCT
    R2aj = 1 - (1 - R2) * (n - 1) / (n - p)
    F_c = (SCE / k) / S2 if k else float("nan")
    C = np.diag(XtX_inv)
    Sb = np.sqrt(S2 * C)
    t_c = b / Sb
    H = X @ XtX_inv @ X.T
    press = float(((res / (1 - np.diag(H))) ** 2).sum())
    vif = []
    for i in range(k):
        otros = [cols[j] for j in range(k) if j != i]
        if not otros:
            vif.append(1.0)
            continue
        Xo = np.column_stack([np.ones(n)] + otros)
        bo = np.linalg.lstsq(Xo, cols[i], rcond=None)[0]
        ri = cols[i] - Xo @ bo
        r2i = 1 - float(ri @ ri) / float(((cols[i] - cols[i].mean()) ** 2).sum())
        vif.append(1 / (1 - r2i) if r2i < 1 else float("inf"))
    return RegresionMultiple(nombres=nombres, n=n, k=k, p=p, b=[float(v) for v in b], SCR=SCR, SCE=SCE,
                             SCT=SCT, S2=S2, S=sqrt(S2), R2=R2, R2aj=R2aj, F_c=F_c,
                             C=[float(v) for v in C], Sb=[float(v) for v in Sb], t_c=[float(v) for v in t_c],
                             PRESS=press, DET=_corr_det(cols), VIF=vif, XtX_inv=XtX_inv.tolist())


@dataclass
class EnsayoGlobal:
    F_c: float
    F_critico: float
    nu1: int
    nu2: int
    rechaza: bool


def ensayo_global(reg: RegresionMultiple, alpha: float) -> EnsayoGlobal:
    nu1, nu2 = reg.k, reg.n - reg.p
    fc = f_value(1 - alpha, nu1, nu2)
    return EnsayoGlobal(reg.F_c, fc, nu1, nu2, reg.F_c > fc)


@dataclass
class EnsayoParcial:
    nombre: str
    b: float
    Sb: float
    t_c: float
    t_critico: float
    rechaza: bool


def ensayos_parciales(reg: RegresionMultiple, alpha: float) -> List[EnsayoParcial]:
    """H0: βi = 0 para cada variable; criterio de la cátedra: |tc| > t(1-α; n-p)."""
    tc = t_value(1 - alpha, reg.n - reg.p)
    return [EnsayoParcial(nom, reg.b[i + 1], reg.Sb[i + 1], reg.t_c[i + 1], tc, abs(reg.t_c[i + 1]) > tc)
            for i, nom in enumerate(reg.nombres)]


def determinacion_parcial(xs: List[Sequence[float]], y: Sequence[float], nombres: List[str]) -> Dict[str, float]:
    """Aporte parcial de cada x_i en presencia de las demás: (R² - R²_sin_i) / (1 - R²_sin_i)."""
    total = ajustar_multiple(xs, y, nombres).R2
    out = {}
    for i, nom in enumerate(nombres):
        otros = [xs[j] for j in range(len(xs)) if j != i]
        r2o = ajustar_multiple(otros, y).R2 if otros else 0.0
        out[nom] = (total - r2o) / (1 - r2o)
    return out


@dataclass
class Candidato:
    variables: List[str]
    p: int
    R2: float
    R2aj: float
    S2: float
    PRESS: float
    DET: float
    Cp: float
    Cp_p: float
    VIF_max: float
    cumple: bool  # DET > 0,1 y Cp/p < 5 (criterios excluyentes de la cátedra)
    reg: RegresionMultiple = None


def seleccion_modelos(xs: List[Sequence[float]], y: Sequence[float], nombres: List[str]) -> List[Candidato]:
    """Tabla de selección (análisis exploratorio) con todos los subconjuntos de variables."""
    completo = ajustar_multiple(xs, y, nombres)
    s2_full = completo.S2
    n = completo.n
    out = []
    for m in range(1, len(xs) + 1):
        for idx in combinations(range(len(xs)), m):
            reg = ajustar_multiple([xs[i] for i in idx], y, [nombres[i] for i in idx])
            cp = reg.SCR / s2_full - (n - 2 * reg.p)
            out.append(Candidato(variables=reg.nombres, p=reg.p, R2=reg.R2, R2aj=reg.R2aj, S2=reg.S2,
                                 PRESS=reg.PRESS, DET=reg.DET, Cp=cp, Cp_p=cp / reg.p,
                                 VIF_max=max(reg.VIF), cumple=reg.DET > 0.1 and cp / reg.p < 5, reg=reg))
    return out


def mejor_candidato(cands: List[Candidato]) -> Candidato:
    """Entre los que cumplen DET y Cp, el de mayor R² ajustado; a igualdad, el más simple (parsimonia)."""
    validos = [c for c in cands if c.cumple] or cands
    return max(validos, key=lambda c: (round(c.R2aj, 3), -c.p, -c.PRESS))
