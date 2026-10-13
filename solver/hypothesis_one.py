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

def critico_catedra(xc, tail: str, decimales: int = 4):
    """Valor crítico redondeado hacia afuera (achicando la región de rechazo), como lo usa la cátedra para
    calcular β: cola derecha hacia arriba, izquierda hacia abajo; bilateral (abajo, arriba).
    Con el crítico exacto no se reproducen I-9b, I-11b, I-27b (convención C-3 / modo cátedra)."""
    from math import floor
    k = 10 ** decimales
    arriba = lambda v: ceil(v * k - 1e-9) / k
    abajo = lambda v: floor(v * k + 1e-9) / k
    if tail == "bilateral":
        return abajo(xc[0]), arriba(xc[1])
    return arriba(xc) if tail == "derecha" else abajo(xc)


def _beta_media(xc, mu1: float, se: float, tail: str) -> float:
    """β en μ₁ (con la normal) usando el crítico de la cátedra (redondeado hacia afuera a 4 decimales)."""
    xc = critico_catedra(xc, tail)
    if tail == "derecha":
        return dist.norm_cdf((xc - mu1) / se)
    if tail == "izquierda":
        return 1 - dist.norm_cdf((xc - mu1) / se)
    return dist.norm_cdf((xc[1] - mu1) / se) - dist.norm_cdf((xc[0] - mu1) / se)


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
        result.beta = _beta_media(critical_value, mu1, se, tail)
        result.power = 1 - result.beta

    return result


@dataclass
class DisenoEnsayoResult:
    """Diseño completo de un ensayo: no sólo n, también el punto crítico y la regla de decisión.

    Responde el tipo de consigna "se desea un sistema de muestreo tal que si μ=μ₀ se
    detenga con probabilidad α y si μ=μ₁ se detenga con probabilidad 1-β": hay que
    indicar H0, la condición de rechazo (x̄_c), n y la regla de decisión.
    """
    h0_text: str
    h1_text: str
    tail: str
    mu0: float
    mu1: float
    alpha: float
    beta_objetivo: float
    n_exacto: float          # n sin redondear (el que sale de la fórmula)
    n: int                   # n redondeado hacia arriba
    z_alpha: float
    z_beta: float
    critical_value: object   # x̄_c recalculado con el n redondeado (float, o tupla si bilateral)
    xc_sistema: Optional[float]  # x̄_c de la intersección de ambas condiciones, sin redondear n
    beta_real: float         # β efectivo en μ₁ con el n redondeado
    potencia_real: float     # 1-β efectivo en μ₁ con el n redondeado
    se: float                # σ/√n con el n redondeado
    distribution: str = "Z"
    df: Optional[float] = None
    regla_decision: str = ""
    warnings: List[str] = field(default_factory=list)


def _z_alpha_para(tail: str, alpha: float) -> float:
    return dist.z_two_tailed(alpha) if tail == "bilateral" else dist.z_one_tailed(alpha)


def _potencia_media(xc, mu: float, se: float, tail: str) -> float:
    """Potencia = P(rechazar H0 | μ) para el ensayo de media con región crítica xc."""
    if tail == "derecha":
        return 1 - dist.norm_cdf((xc - mu) / se)
    if tail == "izquierda":
        return dist.norm_cdf((xc - mu) / se)
    c1, c2 = xc
    return dist.norm_cdf((c1 - mu) / se) + (1 - dist.norm_cdf((c2 - mu) / se))


def disenar_ensayo_media_sigma_conocido(
    sigma: float,
    mu0: float,
    mu1: float,
    alpha: float,
    beta: float,
    tail: Optional[str] = None,
) -> DisenoEnsayoResult:
    """Diseña el ensayo de media (σ conocido) a partir de las dos condiciones α y β.

    Devuelve n, el punto crítico x̄_c, β/potencia reales y la regla de decisión.
    Si `tail` es None se deduce de la posición de μ₁ respecto de μ₀ (criterio
    optimista: H0 incluye a μ₀ y se rechaza hacia el lado donde está μ₁).
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    if not (0 < beta < 1):
        raise ValueError(f"beta debe estar entre 0 y 1, no {beta}")
    if mu0 == mu1:
        raise ValueError("μ₀ y μ₁ deben ser distintos para poder dimensionar la muestra.")

    if tail is None:
        tail = "izquierda" if mu1 < mu0 else "derecha"
    if tail not in ("derecha", "izquierda", "bilateral"):
        raise ValueError(f"tail debe ser 'derecha', 'izquierda' o 'bilateral', no {tail}")

    warnings: List[str] = []
    if tail == "derecha" and mu1 < mu0:
        warnings.append("Elegiste cola derecha pero μ₁ < μ₀: revisá el sentido del ensayo.")
    if tail == "izquierda" and mu1 > mu0:
        warnings.append("Elegiste cola izquierda pero μ₁ > μ₀: revisá el sentido del ensayo.")

    z_alpha = _z_alpha_para(tail, alpha)
    z_beta = dist.z_value(1 - beta)
    delta = abs(mu0 - mu1)

    n_exacto = ((z_alpha + z_beta) * sigma / delta) ** 2
    n = ceil(n_exacto)
    se = sigma / sqrt(n)

    if tail == "derecha":
        h0_text, h1_text = f"μ ≤ {mu0}", f"μ > {mu0}"
        critical_value = mu0 + z_alpha * se
        # x̄_c donde ambas condiciones se cumplen exactamente (con n sin redondear)
        xc_sistema = (mu0 * z_beta + mu1 * z_alpha) / (z_alpha + z_beta)
    elif tail == "izquierda":
        h0_text, h1_text = f"μ ≥ {mu0}", f"μ < {mu0}"
        critical_value = mu0 - z_alpha * se
        xc_sistema = (mu0 * z_beta + mu1 * z_alpha) / (z_alpha + z_beta)
    else:
        h0_text, h1_text = f"μ = {mu0}", f"μ ≠ {mu0}"
        critical_value = (mu0 - z_alpha * se, mu0 + z_alpha * se)
        xc_sistema = None

    potencia_real = _potencia_media(critical_value, mu1, se, tail)
    beta_real = 1 - potencia_real

    if tail == "bilateral":
        c1, c2 = critical_value
        regla = (
            f"Tomar una muestra de n = {n}. Si la media muestral cae fuera del intervalo "
            f"[{c1:.4f}, {c2:.4f}] se rechaza H0."
        )
    else:
        signo = ">" if tail == "derecha" else "<"
        regla = (
            f"Tomar una muestra de n = {n}. Si la media de esa muestra es "
            f"{'superior' if tail == 'derecha' else 'inferior'} a "
            f"{critical_value:.4f} (x̄ {signo} x̄_c) se rechaza H0."
        )

    return DisenoEnsayoResult(
        h0_text=h0_text,
        h1_text=h1_text,
        tail=tail,
        mu0=mu0,
        mu1=mu1,
        alpha=alpha,
        beta_objetivo=beta,
        n_exacto=n_exacto,
        n=n,
        z_alpha=z_alpha,
        z_beta=z_beta,
        critical_value=critical_value,
        xc_sistema=xc_sistema,
        beta_real=beta_real,
        potencia_real=potencia_real,
        se=se,
        distribution="Z",
        regla_decision=regla,
        warnings=warnings,
    )


def n_media_sigma_conocido_para_potencia(
    sigma: float,
    mu0: float,
    mu1: float,
    alpha: float,
    beta: float,
    tail: str = "derecha",
) -> int:
    """Calcula n para una potencia (1-β) fijada, σ conocido.

    Atajo sobre `disenar_ensayo_media_sigma_conocido` cuando sólo interesa n.
    """
    return disenar_ensayo_media_sigma_conocido(
        sigma=sigma, mu0=mu0, mu1=mu1, alpha=alpha, beta=beta, tail=tail
    ).n


def disenar_ensayo_media_sigma_desconocido(
    s: float,
    mu0: float,
    mu1: float,
    alpha: float,
    beta: float,
    tail: Optional[str] = None,
    n_inicial: int = 100,
    max_iter: int = 20,
) -> DisenoEnsayoResult:
    """Análogo a disenar_ensayo_media_sigma_conocido pero con S/t (σ desconocido).

    Bucle iterativo igual al de intervals.n_media_sigma_desconocido: t depende de
    nu=n-1, así que se itera hasta que el n que sale coincide con el que entra.
    No se encontró un ejercicio real de la cátedra para validar este caso puntual
    (σ desconocido + potencia fijada); la fórmula es la extensión analógica
    directa del caso con σ conocido, verificar si aparece un ejercicio real.
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    if not (0 < beta < 1):
        raise ValueError(f"beta debe estar entre 0 y 1, no {beta}")
    if mu0 == mu1:
        raise ValueError("μ₀ y μ₁ deben ser distintos para poder dimensionar la muestra.")

    if tail is None:
        tail = "izquierda" if mu1 < mu0 else "derecha"
    if tail not in ("derecha", "izquierda", "bilateral"):
        raise ValueError(f"tail debe ser 'derecha', 'izquierda' o 'bilateral', no {tail}")

    delta = abs(mu0 - mu1)
    n_actual = n_inicial
    historial = []
    for _ in range(max_iter):
        df = n_actual - 1
        t_alpha = dist.t_two_tailed(alpha, df) if tail == "bilateral" else dist.t_one_tailed(alpha, df)
        t_beta = dist.t_value(1 - beta, df)
        n_exacto = ((t_alpha + t_beta) * s / delta) ** 2
        n_siguiente = ceil(n_exacto)
        historial.append(n_siguiente)
        if n_siguiente == n_actual:
            break
        n_actual = n_siguiente
    else:
        raise RuntimeError(
            f"El bucle iterativo no convergió en {max_iter} iteraciones (historial: {historial})."
        )

    n = n_actual
    df = n - 1
    se = s / sqrt(n)

    if tail == "derecha":
        h0_text, h1_text = f"μ ≤ {mu0}", f"μ > {mu0}"
        critical_value = mu0 + t_alpha * se
        xc_sistema = (mu0 * t_beta + mu1 * t_alpha) / (t_alpha + t_beta)
    elif tail == "izquierda":
        h0_text, h1_text = f"μ ≥ {mu0}", f"μ < {mu0}"
        critical_value = mu0 - t_alpha * se
        xc_sistema = (mu0 * t_beta + mu1 * t_alpha) / (t_alpha + t_beta)
    else:
        h0_text, h1_text = f"μ = {mu0}", f"μ ≠ {mu0}"
        critical_value = (mu0 - t_alpha * se, mu0 + t_alpha * se)
        xc_sistema = None

    # β/potencia se evalúan con la normal, igual que en ensayo_media_sigma_desconocido
    potencia_real = _potencia_media(critical_value, mu1, se, tail)
    beta_real = 1 - potencia_real

    if tail == "bilateral":
        c1, c2 = critical_value
        regla = (
            f"Tomar una muestra de n = {n}. Si la media muestral cae fuera del intervalo "
            f"[{c1:.4f}, {c2:.4f}] se rechaza H0."
        )
    else:
        signo = ">" if tail == "derecha" else "<"
        regla = (
            f"Tomar una muestra de n = {n}. Si la media de esa muestra es "
            f"{'superior' if tail == 'derecha' else 'inferior'} a "
            f"{critical_value:.4f} (x̄ {signo} x̄_c) se rechaza H0."
        )

    return DisenoEnsayoResult(
        h0_text=h0_text,
        h1_text=h1_text,
        tail=tail,
        mu0=mu0,
        mu1=mu1,
        alpha=alpha,
        beta_objetivo=beta,
        n_exacto=n_exacto,
        n=n,
        z_alpha=t_alpha,
        z_beta=t_beta,
        critical_value=critical_value,
        xc_sistema=xc_sistema,
        beta_real=beta_real,
        potencia_real=potencia_real,
        se=se,
        distribution="t",
        df=df,
        regla_decision=regla,
        warnings=[
            "Caso no validado contra un ejercicio real de la cátedra "
            "(σ desconocido + potencia fijada): es una extensión analógica."
        ],
    )


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
    """Atajo sobre `disenar_ensayo_media_sigma_desconocido` cuando sólo interesa n."""
    return disenar_ensayo_media_sigma_desconocido(
        s=s, mu0=mu0, mu1=mu1, alpha=alpha, beta=beta, tail=tail,
        n_inicial=n_inicial, max_iter=max_iter,
    ).n


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
        result.beta = _beta_media(critical_value, mu1, se, tail)
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


# ---------------------------------------------------------------------------
# Diseño por potencia fijada: varianza (χ²) y proporción (plan de muestreo binomial)
# ---------------------------------------------------------------------------

@dataclass
class DisenoVarianzaResult:
    n: int
    tail: str
    s2_c: float          # S²_c: valor crítico de la varianza muestral
    beta_real: float
    potencia_real: float
    h0_text: str
    h1_text: str


def n_varianza_para_potencia(
    sigma0: float,
    sigma1: float,
    alpha: float,
    beta: float,
    tail: Optional[str] = None,
    n_max: int = 200_000,
) -> DisenoVarianzaResult:
    """Menor n tal que el ensayo de σ² con riesgo α tenga β ≤ `beta` cuando σ = σ₁.

    Verificado contra la guía (TEMA II): σ₀=5, σ₁=8, α=0,05, β=0,05 -> n=27;
    σ₀²=0,09, σ₁²=0,11, α=0,05, 1-β=0,95 -> n=540.
    """
    if not (0 < alpha < 1) or not (0 < beta < 1):
        raise ValueError("α y β deben estar entre 0 y 1")
    if sigma0 <= 0 or sigma1 <= 0 or sigma0 == sigma1:
        raise ValueError("σ₀ y σ₁ deben ser positivos y distintos")
    if tail is None:
        tail = "derecha" if sigma1 > sigma0 else "izquierda"
    if tail not in ("derecha", "izquierda"):
        raise ValueError("Para dimensionar por potencia se usa un ensayo unilateral")
    s0_2, s1_2 = sigma0 ** 2, sigma1 ** 2
    for n in range(2, n_max):
        df = n - 1
        if tail == "derecha":
            s2_c = s0_2 * dist.chi2_one_tailed(alpha, df) / df
            b = dist.chi2_cdf(df * s2_c / s1_2, df)
        else:
            s2_c = s0_2 * dist.chi2_value(alpha, df) / df
            b = 1 - dist.chi2_cdf(df * s2_c / s1_2, df)
        if b <= beta:
            h0, h1 = (f"σ² ≤ {s0_2:g}", f"σ² > {s0_2:g}") if tail == "derecha" else (f"σ² ≥ {s0_2:g}", f"σ² < {s0_2:g}")
            return DisenoVarianzaResult(n=n, tail=tail, s2_c=s2_c, beta_real=b, potencia_real=1 - b,
                                        h0_text=h0, h1_text=h1)
    raise RuntimeError(f"No se encontró n ≤ {n_max} que cumpla las condiciones")


@dataclass
class PlanMuestreoResult:
    """Plan de muestreo binomial: tomar n unidades y rechazar H0 según r_c."""
    n: int
    rc: int
    tail: str
    alpha_real: float
    beta_real: float
    potencia_real: float
    h0_text: str
    h1_text: str
    regla_decision: str


def disenar_plan_proporcion(
    p0: float,
    p1: float,
    alpha: float,
    beta: float,
    tail: Optional[str] = None,
    n_max: int = 50_000,
) -> PlanMuestreoResult:
    """Plan de muestreo (n, r_c) de menor n que cumple α y β con el modelo binomial exacto.

    Cola derecha: se rechaza H0 si r ≥ r_c. Cola izquierda: si r ≤ r_c.
    Verificado contra la guía (TEMA III): p₀=0,11, p₁=0,16, α=0,05, 1-β=0,99 ->
    n=739, r_c=96; p₀=0,01, p₁=0,02, α=0,01, 1-β=0,95 -> n=2.258, r_c=35;
    p₀=0,14, p₁=0,10, α=0,01, 1-β=0,95 -> n=1.043, r_c=120.
    """
    from scipy import stats

    if not (0 < alpha < 1) or not (0 < beta < 1):
        raise ValueError("α y β deben estar entre 0 y 1")
    if not (0 < p0 < 1) or not (0 < p1 < 1) or p0 == p1:
        raise ValueError("p₀ y p₁ deben estar entre 0 y 1 y ser distintos")
    if tail is None:
        tail = "derecha" if p1 > p0 else "izquierda"
    if tail not in ("derecha", "izquierda"):
        raise ValueError("El plan de muestreo se diseña con un ensayo unilateral")

    for n in range(2, n_max):
        if tail == "derecha":
            rc = int(stats.binom.isf(alpha, n, p0)) + 1
            while rc > 0 and stats.binom.sf(rc - 2, n, p0) <= alpha:
                rc -= 1
            while stats.binom.sf(rc - 1, n, p0) > alpha:
                rc += 1
            if rc > n:
                continue
            a_real = stats.binom.sf(rc - 1, n, p0)
            b = stats.binom.cdf(rc - 1, n, p1)
        else:
            rc = int(stats.binom.ppf(alpha, n, p0))
            while rc >= 0 and stats.binom.cdf(rc, n, p0) > alpha:
                rc -= 1
            while stats.binom.cdf(rc + 1, n, p0) <= alpha:
                rc += 1
            if rc < 0:
                continue
            a_real = stats.binom.cdf(rc, n, p0)
            b = stats.binom.sf(rc, n, p1)
        if b <= beta:
            if tail == "derecha":
                h0, h1 = f"p ≤ {p0:g}", f"p > {p0:g}"
                regla = (f"Tomar una muestra de n = {n}. Si se encuentran r ≥ {rc} casos, "
                         f"se rechaza H0.")
            else:
                h0, h1 = f"p ≥ {p0:g}", f"p < {p0:g}"
                regla = (f"Tomar una muestra de n = {n}. Si se encuentran r ≤ {rc} casos, "
                         f"se rechaza H0.")
            return PlanMuestreoResult(n=n, rc=rc, tail=tail, alpha_real=float(a_real), beta_real=float(b),
                                      potencia_real=float(1 - b), h0_text=h0, h1_text=h1, regla_decision=regla)
    raise RuntimeError(f"No se encontró un plan con n ≤ {n_max}")


def planes_factibles(p0: float, p1: float, alpha: float, beta: float, tail: Optional[str] = None,
                     cuantos: int = 3, n_max: int = 50_000) -> List[Tuple[int, int, int]]:
    """[(r_c, n_mín, n_máx)] para los primeros `cuantos` r_c que admiten algún n (binomial exacto).

    Para un r_c fijo, uno de los riesgos baja y el otro sube con n, así que los n que cumplen α y β
    forman un rango: cualquiera sirve. La guía a veces informa el menor y a veces el mayor.
    """
    from scipy import stats
    tail = tail or ("derecha" if p1 > p0 else "izquierda")
    base = disenar_plan_proporcion(p0, p1, alpha, beta, tail, n_max)

    def cumple(n, rc):
        if tail == "derecha":
            return stats.binom.sf(rc - 1, n, p0) <= alpha and stats.binom.cdf(rc - 1, n, p1) <= beta
        return stats.binom.cdf(rc, n, p0) <= alpha and stats.binom.sf(rc, n, p1) <= beta

    salida = []
    rc = base.rc
    n = base.n
    intentos = 0
    while len(salida) < cuantos and intentos < 40:
        intentos += 1
        # el menor n que cumple con este r_c (a partir del anterior) y después todos los consecutivos
        m = n
        while m < n_max and not cumple(m, rc):
            m += 1
            if m - n > 20 * max(1, rc) + 200:
                break
        if m < n_max and cumple(m, rc):
            hasta = m
            while cumple(hasta + 1, rc):
                hasta += 1
            salida.append((rc, m, hasta))
            n = hasta
        rc += 1 if tail == "derecha" else 1
    return salida


def plan_mas_proximo(p0: float, p1: float, alpha: float, beta: float, tail: Optional[str] = None
                     ) -> Tuple[int, int, float, float]:
    """Plan «más próximo a las premisas» (regla inferida de la guía, reproduce 10 de 11 planes: III-16c, III-17,
    III-22b además de los que ya da el n mínimo): entre los planes factibles con r_c igual al del plan de n mínimo
    o el siguiente, el que minimiza |α_real - α| + |β_real - β|. Devuelve (n, r_c, α_real, β_real)."""
    import numpy as np
    from scipy import stats
    tail = tail or ("derecha" if p1 > p0 else "izquierda")
    base = disenar_plan_proporcion(p0, p1, alpha, beta, tail)
    mejor = (base.n, base.rc, base.alpha_real, base.beta_real)
    puntaje = abs(base.alpha_real - alpha) + abs(base.beta_real - beta)
    for rc in (base.rc, base.rc + 1):
        ns = np.arange(max(rc, 1), int(base.n * 1.6) + 2)
        if tail == "derecha":
            a_, b_ = stats.binom.sf(rc - 1, ns, p0), stats.binom.cdf(rc - 1, ns, p1)
        else:
            a_, b_ = stats.binom.cdf(rc, ns, p0), stats.binom.sf(rc, ns, p1)
        for i in np.nonzero((a_ <= alpha) & (b_ <= beta))[0]:
            sc = abs(a_[i] - alpha) + abs(b_[i] - beta)
            if sc < puntaje - 1e-15:
                puntaje, mejor = sc, (int(ns[i]), rc, float(a_[i]), float(b_[i]))
    return mejor


def _m_tabla(m: float, hacia: str) -> float:
    """m redondeado a la resolución de una tabla de Poisson (0,1), del lado conservador."""
    from math import ceil, floor
    return (ceil(m * 10 - 1e-9) if hacia == "arriba" else floor(m * 10 + 1e-9)) / 10


def plan_poisson_tabla(p0: float, rc: int, alpha: float, tail: str) -> Optional[Tuple[int, float]]:
    """n por la aproximación de Poisson como la guía: m₀ = n·p₀ que cumple α buscado en la tabla (m al 0,1).

    Cola derecha (rechazo si r ≥ r_c): mayor m₀ con P(r ≥ r_c | m₀) ≤ α → n = m₀/p₀ (hacia abajo).
    Cola izquierda (rechazo si r ≤ r_c): menor m₀ con P(r ≤ r_c | m₀) ≤ α → n = m₀/p₀ (hacia arriba).
    Solo para m₀ ≤ 20 (lo que cubren las tablas). Devuelve (n, m₀ de tabla)."""
    from math import ceil, floor
    from scipy import stats
    from scipy.optimize import brentq
    if tail == "derecha":
        m = brentq(lambda x: stats.poisson.sf(rc - 1, x) - alpha, 1e-9, 1e4)
        mt = _m_tabla(m, "abajo")
        n = floor(mt / p0 + 1e-9)
    else:
        m = brentq(lambda x: stats.poisson.cdf(rc, x) - alpha, 1e-9, 1e4)
        mt = _m_tabla(m, "arriba")
        n = ceil(mt / p0 - 1e-9)
    if mt > 20 or n < 1:
        return None
    return n, mt


@dataclass
class PlanPoissonGarcia:
    n: int
    rc: int
    a: float
    nu: float          # ν de la ecuación de García (sin redondear)
    gl: int            # grados de libertad de la χ² que se usan para n
    n_alpha: float     # n que cumple α en p₀ (sin redondear)
    n_beta: float      # n que cumple β en p₁ (sin redondear)


def plan_poisson_garcia(p0: float, p1: float, alpha: float, beta: float, tail: str) -> PlanPoissonGarcia:
    """Diseño del plan por aproximación de Poisson con la Ecuación de García (teoría cap. 2 p. 26-27).

    CASO I (cola derecha, rechazo si r ≥ r_c): R = p₁/p₀, a = [Z(1-β) + Z(1-α)·∛R] / [2(∛R - 1)],
    ν = 2/9·(a + √(a² + 1))²; c = ⌊ν/2⌋, g.l. = 2c, n = máx[χ²(α; 2c)/(2p₀) ; χ²(1-β; 2c)/(2p₁)] y r_c = c + 1.
    CASO II (cola izquierda, rechazo si r ≤ r_c): R = p₀/p₁, a = [Z(1-α) + Z(1-β)·∛R] / [2(∛R - 1)],
    r_c = ⌈(ν - 2)/2⌉, g.l. = 2r_c + 2, n = máx[χ²(1-α; g.l.)/(2p₀) ; χ²(β; g.l.)/(2p₁)].
    El redondeo de ν/2 no lo da la teoría: esta regla reproduce III-11c (855), III-17 (227), III-22a (325) y
    III-22b (186). Ojo: esos planes no siempre cumplen α y β exactos (la aproximación es gruesa)."""
    from math import floor
    za, zb = dist.z_value(1 - alpha), dist.z_value(1 - beta)
    if tail == "derecha":
        R = p1 / p0
        c3 = R ** (1 / 3)
        a = (zb + za * c3) / (2 * (c3 - 1))
    else:
        R = p0 / p1
        c3 = R ** (1 / 3)
        a = (za + zb * c3) / (2 * (c3 - 1))
    if R <= 1:
        raise ValueError("Para el plan hace falta p₁ del lado de H1 respecto de p₀")
    nu = 2 / 9 * (a + sqrt(a * a + 1)) ** 2
    if tail == "derecha":
        c = max(1, floor(nu / 2 + 1e-9))
        gl, rc = 2 * c, c + 1
        n_a, n_b = dist.chi2_value(alpha, gl) / (2 * p0), dist.chi2_value(1 - beta, gl) / (2 * p1)
    else:
        rc = max(0, ceil((nu - 2) / 2 - 1e-9))
        gl = 2 * rc + 2
        n_a, n_b = dist.chi2_value(1 - alpha, gl) / (2 * p0), dist.chi2_value(beta, gl) / (2 * p1)
    return PlanPoissonGarcia(n=ceil(max(n_a, n_b) - 1e-9), rc=rc, a=a, nu=nu, gl=gl, n_alpha=n_a, n_beta=n_b)


def n_plan_dado_poisson(p0: float, rc: int, prob_aceptar: float) -> Optional[Tuple[int, float]]:
    """Plan con r_c fijo (se rechaza si r ≥ r_c): mayor n con P(aceptar | p₀) ≥ prob_aceptar usando la
    tabla de Poisson (m al 0,1, hacia abajo). III-21: P(r ≤ 1) ≥ 0,95 con p₀ = 1% → m = 0,3 → n = 30."""
    from math import floor
    from scipy import stats
    from scipy.optimize import brentq
    m = brentq(lambda x: stats.poisson.cdf(rc - 1, x) - prob_aceptar, 1e-9, 1e4)
    mt = _m_tabla(m, "abajo")
    if mt > 20 or mt <= 0:
        return None
    return floor(mt / p0 + 1e-9), mt


def _rc_binomial(n: int, p0: float, alpha: float, tail: str) -> int:
    """Valor crítico exacto (binomial) para n dado: cola derecha r ≥ r_c, izquierda r ≤ r_c."""
    return _buscar_rc_derecha(n, p0, alpha) if tail == "derecha" else _buscar_rc_izquierda(n, p0, alpha)


def _prob_rechazo_binomial(n: int, rc: int, p: float, tail: str) -> float:
    return dist.binom_upper_tail(rc, n, p) if tail == "derecha" else dist.binom_cdf(rc, n, p)


def plan_proporcion_normal(
    p0: float,
    p1: float,
    alpha: float,
    beta: float,
    tail: Optional[str] = None,
) -> PlanMuestreoResult:
    """Plan de muestreo con n por APROXIMACIÓN NORMAL, como lo informa la guía (TEMA III):

        n = [(Z(1-α)·√(p₀q₀) + Z(1-β)·√(p₁q₁)) / (p₁ - p₀)]²   (redondeado hacia arriba)

    y con ese n el valor crítico r_c y las probabilidades reales salen del binomial exacto.
    Verificado: p₀=0,11, p₁=0,16, α=0,05, β=0,01 -> n=749, r_c=98; p₀=0,14, p₁=0,10, α=0,01, β=0,05 -> n=1.058,
    r_c=121; p₀=0,01, p₁=0,02, α=0,01, β=0,05 -> n=2.133, r_c=34.
    """
    from math import ceil

    if not (0 < alpha < 1) or not (0 < beta < 1):
        raise ValueError("α y β deben estar entre 0 y 1")
    if not (0 < p0 < 1) or not (0 < p1 < 1) or p0 == p1:
        raise ValueError("p₀ y p₁ deben estar entre 0 y 1 y ser distintos")
    if tail is None:
        tail = "derecha" if p1 > p0 else "izquierda"
    z_a, z_b = dist.z_one_tailed(alpha), dist.z_one_tailed(beta)
    n = ceil(((z_a * sqrt(p0 * (1 - p0)) + z_b * sqrt(p1 * (1 - p1))) / abs(p1 - p0)) ** 2)
    n = max(n, 2)
    rc = _rc_binomial(n, p0, alpha, tail)
    a_real = _prob_rechazo_binomial(n, rc, p0, tail)
    pot = _prob_rechazo_binomial(n, rc, p1, tail)
    op = "≥" if tail == "derecha" else "≤"
    h0, h1 = (f"p ≤ {p0:g}", f"p > {p0:g}") if tail == "derecha" else (f"p ≥ {p0:g}", f"p < {p0:g}")
    return PlanMuestreoResult(n=n, rc=rc, tail=tail, alpha_real=float(a_real), beta_real=float(1 - pot),
                              potencia_real=float(pot), h0_text=h0, h1_text=h1,
                              regla_decision=f"Tomar una muestra de n = {n}. Si se encuentran r {op} {rc} casos, se rechaza H0.")


def p_para_aceptacion(n: int, rc: int, prob_rechazo: float, tail: str = "derecha") -> float:
    """Proporción p con la que un plan (n, r_c) rechaza con la probabilidad dada (binomial exacto).

    Sirve para el AQL (rechazo = α) y el LTPD / lote malo (rechazo = 1-β). Verificado (guía TEMA III):
    n=10, r_c=1: AQL con α=0,05 -> 0,005116; LTPD con β=0,10 -> 0,2057. n=100, r_c=9, β=0,15 -> p₁=0,1183."""
    from scipy.optimize import brentq

    def f(p):
        return _prob_rechazo_binomial(n, rc, p, tail) - prob_rechazo

    return float(brentq(f, 1e-12, 1 - 1e-12))
