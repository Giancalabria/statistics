"""M2 — Ensayos de Hipótesis para 1 población.

Implementa §2 del esquema_teorico_examen_estadistica.md:
- Media con σ conocido (Z)
- Media con σ desconocido (t)
- Varianza (χ²)
- Proporción (Binomial exacto, no aproximación normal)
"""

from dataclasses import dataclass, field
from math import ceil, sqrt
from typing import List, Optional, Tuple

from . import distributions as dist


@dataclass
class HypothesisTestResult:
    """Resultado de un ensayo de hipótesis."""
    h0_text: str
    h1_text: str
    tail: str  # "derecha" | "izquierda" | "bilateral"
    critical_value: object  # float o tupla (c1, c2) si es bilateral
    observed_value: float  # x̄, S² o r según el caso
    rejects_h0: bool
    distribution: str
    df: Optional[float] = None
    beta: Optional[float] = None
    power: Optional[float] = None
    p_value: Optional[float] = None
    warnings: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 2.2 Media poblacional (mu), sigma CONOCIDO
# ---------------------------------------------------------------------------

def ensayo_media_sigma_conocido(
    xbar: float,
    sigma: float,
    n: int,
    mu0: float,
    alpha: float,
    tail: str = "derecha",
    mu1: Optional[float] = None,
) -> HypothesisTestResult:
    """Ensayo de hipótesis para media con σ conocido."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    if tail == "derecha":
        z_alpha = dist.z_one_tailed(alpha)
        se = sigma / sqrt(n)
        xbar_c = mu0 + z_alpha * se
        h0_text = f"μ ≤ {mu0}"
        h1_text = f"μ > {mu0}"
        rejects = xbar > xbar_c
        critical_value = xbar_c
    elif tail == "izquierda":
        z_alpha = dist.z_one_tailed(alpha)
        se = sigma / sqrt(n)
        xbar_c = mu0 - z_alpha * se
        h0_text = f"μ ≥ {mu0}"
        h1_text = f"μ < {mu0}"
        rejects = xbar < xbar_c
        critical_value = xbar_c
    elif tail == "bilateral":
        z_alpha = dist.z_two_tailed(alpha)
        se = sigma / sqrt(n)
        xbar_c1 = mu0 - z_alpha * se
        xbar_c2 = mu0 + z_alpha * se
        h0_text = f"μ = {mu0}"
        h1_text = f"μ ≠ {mu0}"
        rejects = xbar < xbar_c1 or xbar > xbar_c2
        critical_value = (xbar_c1, xbar_c2)
    else:
        raise ValueError(f"tail debe ser 'derecha', 'izquierda' o 'bilateral', no {tail}")

    result = HypothesisTestResult(
        h0_text=h0_text,
        h1_text=h1_text,
        tail=tail,
        critical_value=critical_value,
        observed_value=xbar,
        rejects_h0=rejects,
        distribution="Z",
    )

    if mu1 is not None:
        se = sigma / sqrt(n)
        if tail == "derecha":
            z_beta = (xbar_c - mu1) / se
            result.beta = dist.norm_cdf(z_beta)
        elif tail == "izquierda":
            z_beta = (xbar_c - mu1) / se
            result.beta = 1 - dist.norm_cdf(z_beta)
        else:  # bilateral
            z_beta_sup = (xbar_c2 - mu1) / se
            z_beta_inf = (xbar_c1 - mu1) / se
            result.beta = dist.norm_cdf(z_beta_sup) - dist.norm_cdf(z_beta_inf)
        result.power = 1 - result.beta

    return result


def n_media_sigma_conocido_para_potencia(
    sigma: float,
    mu0: float,
    mu1: float,
    alpha: float,
    beta: float,
    tail: str = "derecha",
) -> int:
    """Calcula n para una potencia (1-β) fijada, σ conocido."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    if tail == "bilateral":
        z_alpha = dist.z_two_tailed(alpha)
    else:
        z_alpha = dist.z_one_tailed(alpha)

    z_beta = dist.z_value(1 - beta)
    delta = abs(mu0 - mu1)
    n = ceil(((z_alpha + z_beta) * sigma / delta) ** 2)
    return n


def n_media_sigma_desconocido_para_potencia(
    s: float,
    mu0: float,
    mu1: float,
    alpha: float,
    beta: float,
    tail: str = "derecha",
    n_inicial: int = 100,
    max_iter: int = 20,
) -> int:
    """Análogo a n_media_sigma_conocido_para_potencia pero con S/t (σ desconocido).

    Mismo bucle iterativo que intervals.n_media_sigma_desconocido: t depende de
    nu=n-1, así que se itera hasta que el n que sale coincide con el que entra.
    No se encontró un ejercicio real de la cátedra para validar este caso puntual
    (σ desconocido + potencia fijada); la fórmula es la extensión analógica
    directa del caso con σ conocido, verificar si aparece un ejercicio real.
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    delta = abs(mu0 - mu1)
    n_actual = n_inicial
    historial = []
    for _ in range(max_iter):
        df = n_actual - 1
        t_alpha = dist.t_two_tailed(alpha, df) if tail == "bilateral" else dist.t_one_tailed(alpha, df)
        t_beta = dist.t_value(1 - beta, df)
        n_siguiente = ceil(((t_alpha + t_beta) * s / delta) ** 2)
        historial.append(n_siguiente)
        if n_siguiente == n_actual:
            break
        n_actual = n_siguiente
    else:
        raise RuntimeError(
            f"El bucle iterativo no convergió en {max_iter} iteraciones (historial: {historial})."
        )
    return n_actual


def ensayo_media_sigma_desconocido(
    xbar: float,
    s: float,
    n: int,
    mu0: float,
    alpha: float,
    tail: str = "derecha",
    mu1: Optional[float] = None,
) -> HypothesisTestResult:
    """Ensayo de hipótesis para media con σ desconocido (usar t)."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    df = n - 1
    if tail == "derecha":
        t_alpha = dist.t_one_tailed(alpha, df)
        se = s / sqrt(n)
        xbar_c = mu0 + t_alpha * se
        h0_text = f"μ ≤ {mu0}"
        h1_text = f"μ > {mu0}"
        rejects = xbar > xbar_c
        critical_value = xbar_c
    elif tail == "izquierda":
        t_alpha = dist.t_one_tailed(alpha, df)
        se = s / sqrt(n)
        xbar_c = mu0 - t_alpha * se
        h0_text = f"μ ≥ {mu0}"
        h1_text = f"μ < {mu0}"
        rejects = xbar < xbar_c
        critical_value = xbar_c
    elif tail == "bilateral":
        t_alpha = dist.t_two_tailed(alpha, df)
        se = s / sqrt(n)
        xbar_c1 = mu0 - t_alpha * se
        xbar_c2 = mu0 + t_alpha * se
        h0_text = f"μ = {mu0}"
        h1_text = f"μ ≠ {mu0}"
        rejects = xbar < xbar_c1 or xbar > xbar_c2
        critical_value = (xbar_c1, xbar_c2)
    else:
        raise ValueError(f"tail debe ser 'derecha', 'izquierda' o 'bilateral', no {tail}")

    result = HypothesisTestResult(
        h0_text=h0_text,
        h1_text=h1_text,
        tail=tail,
        critical_value=critical_value,
        observed_value=xbar,
        rejects_h0=rejects,
        distribution="t",
        df=df,
    )

    if mu1 is not None:
        se = s / sqrt(n)
        if tail == "derecha":
            z_beta = (xbar_c - mu1) / se
            result.beta = dist.norm_cdf(z_beta)
        elif tail == "izquierda":
            z_beta = (xbar_c - mu1) / se
            result.beta = 1 - dist.norm_cdf(z_beta)
        else:  # bilateral
            z_beta_sup = (xbar_c2 - mu1) / se
            z_beta_inf = (xbar_c1 - mu1) / se
            result.beta = dist.norm_cdf(z_beta_sup) - dist.norm_cdf(z_beta_inf)
        result.power = 1 - result.beta

    return result


def curva_potencia_media(
    mu0: float,
    sigma_or_s: float,
    n: int,
    alpha: float,
    mu1_list: List[float],
    tail: str = "derecha",
    sigma_conocido: bool = True,
) -> List[Tuple[float, float, float]]:
    """Curva OC / de potencia: para cada mu1 en mu1_list, devuelve (mu1, beta, potencia).

    Reutiliza ensayo_media_sigma_conocido/desconocido (el valor de x̄ no afecta
    a beta/potencia, solo mu0, sigma o S, n, alpha, tail y mu1).
    """
    resultados = []
    for mu1 in mu1_list:
        if sigma_conocido:
            r = ensayo_media_sigma_conocido(
                xbar=mu0, sigma=sigma_or_s, n=n, mu0=mu0, alpha=alpha, tail=tail, mu1=mu1
            )
        else:
            r = ensayo_media_sigma_desconocido(
                xbar=mu0, s=sigma_or_s, n=n, mu0=mu0, alpha=alpha, tail=tail, mu1=mu1
            )
        resultados.append((mu1, r.beta, r.power))
    return resultados


def ensayo_varianza(
    s2: float,
    n: int,
    sigma0_2: float,
    alpha: float,
    tail: str = "derecha",
    sigma1_2: Optional[float] = None,
) -> HypothesisTestResult:
    """Ensayo de hipótesis para varianza (χ²)."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    df = n - 1

    if tail == "derecha":
        chi2_alpha = dist.chi2_one_tailed(alpha, df)
        s2_c = sigma0_2 * chi2_alpha / df
        h0_text = f"σ² ≤ {sigma0_2}"
        h1_text = f"σ² > {sigma0_2}"
        rejects = s2 > s2_c
        critical_value = s2_c
    elif tail == "izquierda":
        chi2_alpha = dist.chi2_value(alpha, df)
        s2_c = sigma0_2 * chi2_alpha / df
        h0_text = f"σ² ≥ {sigma0_2}"
        h1_text = f"σ² < {sigma0_2}"
        rejects = s2 < s2_c
        critical_value = s2_c
    elif tail == "bilateral":
        chi2_lower = dist.chi2_lower(alpha, df)
        chi2_upper = dist.chi2_upper(alpha, df)
        s2_c1 = sigma0_2 * chi2_lower / df
        s2_c2 = sigma0_2 * chi2_upper / df
        h0_text = f"σ² = {sigma0_2}"
        h1_text = f"σ² ≠ {sigma0_2}"
        rejects = s2 < s2_c1 or s2 > s2_c2
        critical_value = (s2_c1, s2_c2)
    else:
        raise ValueError(f"tail debe ser 'derecha', 'izquierda' o 'bilateral', no {tail}")

    result = HypothesisTestResult(
        h0_text=h0_text,
        h1_text=h1_text,
        tail=tail,
        critical_value=critical_value,
        observed_value=s2,
        rejects_h0=rejects,
        distribution="chi2",
        df=df,
    )

    if sigma1_2 is not None:
        if tail == "derecha":
            chi2_transformado = df * s2_c / sigma1_2
            result.beta = dist.chi2_cdf(chi2_transformado, df)
        elif tail == "izquierda":
            chi2_transformado = df * s2_c / sigma1_2
            result.beta = 1 - dist.chi2_cdf(chi2_transformado, df)
        else:  # bilateral
            chi2_transformado_1 = df * s2_c1 / sigma1_2
            chi2_transformado_2 = df * s2_c2 / sigma1_2
            result.beta = dist.chi2_cdf(chi2_transformado_2, df) - dist.chi2_cdf(chi2_transformado_1, df)
        result.power = 1 - result.beta

    return result


def _buscar_rc_derecha(n: int, p0: float, alpha: float) -> int:
    """Busca r_c para cola derecha."""
    for r in range(n + 1):
        prob_upper = dist.binom_upper_tail(r, n, p0)
        if prob_upper <= alpha:
            return r
    return n + 1


def _buscar_rc_izquierda(n: int, p0: float, alpha: float) -> int:
    """Busca r_c para cola izquierda."""
    for r in range(n, -1, -1):
        prob_lower = dist.binom_cdf(r, n, p0)
        if prob_lower <= alpha:
            return r
    return -1


def ensayo_proporcion(
    r: int,
    n: int,
    p0: float,
    alpha: float,
    tail: str = "derecha",
    p1: Optional[float] = None,
) -> HypothesisTestResult:
    """Ensayo de hipótesis para proporción (Binomial exacto)."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    if r < 0 or r > n:
        raise ValueError(f"r debe estar entre 0 y n, no r={r} con n={n}")
    p_hat = r / n

    if tail == "derecha":
        rc = _buscar_rc_derecha(n, p0, alpha)
        h0_text = f"p ≤ {p0}"
        h1_text = f"p > {p0}"
        rejects = r >= rc
        critical_value = rc
        p_value = dist.binom_upper_tail(r, n, p0)
    elif tail == "izquierda":
        rc = _buscar_rc_izquierda(n, p0, alpha)
        h0_text = f"p ≥ {p0}"
        h1_text = f"p < {p0}"
        rejects = r <= rc
        critical_value = rc
        p_value = dist.binom_cdf(r, n, p0)
    elif tail == "bilateral":
        alpha_media = alpha / 2
        rc_derecha = _buscar_rc_derecha(n, p0, alpha_media)
        rc_izquierda = _buscar_rc_izquierda(n, p0, alpha_media)
        h0_text = f"p = {p0}"
        h1_text = f"p ≠ {p0}"
        rejects = r <= rc_izquierda or r >= rc_derecha
        critical_value = (rc_izquierda, rc_derecha)
        p_value_der = dist.binom_upper_tail(r, n, p0)
        p_value_izq = dist.binom_cdf(r, n, p0)
        p_value = min(p_value_der, p_value_izq) * 2
    else:
        raise ValueError(f"tail debe ser 'derecha', 'izquierda' o 'bilateral', no {tail}")

    result = HypothesisTestResult(
        h0_text=h0_text,
        h1_text=h1_text,
        tail=tail,
        critical_value=critical_value,
        observed_value=float(r),
        rejects_h0=rejects,
        distribution="Binomial (exacto)",
        p_value=p_value,
    )

    if p1 is not None:
        if tail == "derecha":
            result.beta = dist.binom_cdf(rc - 1, n, p1)
            result.power = 1 - result.beta
        elif tail == "izquierda":
            result.beta = 1 - dist.binom_cdf(rc, n, p1)
            result.power = 1 - result.beta
        else:  # bilateral
            # potencia = P(rechazar | p1) = P(X <= rc_izq | p1) + P(X >= rc_der | p1);
            # beta es el complemento (no rechazar cuando p1 es verdadera).
            result.power = (
                dist.binom_cdf(rc_izquierda, n, p1) +
                (1 - dist.binom_cdf(rc_derecha - 1, n, p1))
            )
            result.beta = 1 - result.power

    return result
