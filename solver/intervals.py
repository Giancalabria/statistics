"""M1 — Estimación de parámetros por intervalos de confianza.

Implementa §1.1 (media), §1.2 (varianza/desvío) y §1.3 (proporción) de
esquema_teorico_examen_estadistica.md.
"""

from dataclasses import dataclass, field
from math import ceil, sqrt
from typing import List, Optional, Tuple

from . import distributions as dist


@dataclass
class IntervalResult:
    a: float
    b: float
    error: Optional[float]
    point_estimate: float
    distribution: str
    df: Optional[float] = None
    critical_value: Optional[object] = None
    finite_population: bool = False
    warnings: List[str] = field(default_factory=list)


@dataclass
class SampleSizeResult:
    n: int
    iterations: int = 1
    converged_values: Optional[List[int]] = None
    warnings: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 1.1 Media poblacional (mu)
# ---------------------------------------------------------------------------

def ic_media_sigma_conocido(
    xbar: float, sigma: float, n: int, alpha: float, N: Optional[float] = None
) -> IntervalResult:
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    z = dist.z_two_tailed(alpha)
    se = sigma / sqrt(n)
    if N is not None:
        se *= dist.fpc(N, n)
    e = z * se
    return IntervalResult(
        a=xbar - e, b=xbar + e, error=e, point_estimate=xbar,
        distribution="Z", critical_value=z, finite_population=N is not None,
    )


def ic_media_sigma_desconocido(
    xbar: float, s: float, n: int, alpha: float, N: Optional[float] = None
) -> IntervalResult:
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    df = n - 1
    t = dist.t_two_tailed(alpha, df)
    se = s / sqrt(n)
    if N is not None:
        se *= dist.fpc(N, n)
    e = t * se
    return IntervalResult(
        a=xbar - e, b=xbar + e, error=e, point_estimate=xbar,
        distribution="t", df=df, critical_value=t, finite_population=N is not None,
    )


def n_media_sigma_conocido(
    sigma: float, e: float, alpha: float, N: Optional[float] = None
) -> SampleSizeResult:
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    z = dist.z_two_tailed(alpha)
    n_inf = ceil((z * sigma / e) ** 2)
    if N is None:
        return SampleSizeResult(n=n_inf)
    n = ceil((N * n_inf) / (N + n_inf))
    return SampleSizeResult(n=n)


def n_media_sigma_desconocido(
    s: float,
    e: float,
    alpha: float,
    N: Optional[float] = None,
    n_inicial: int = 100,
    max_iter: int = 20,
) -> SampleSizeResult:
    """Algoritmo iterativo de §1.1 CASO B: t depende de nu=n-1, que depende de n.

    Se arranca con un n grande (n_inicial), se recalcula n con el t de ese nu,
    y se repite hasta que el n que sale sea igual al que entró.
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    n_actual = n_inicial
    historial = []
    for _ in range(max_iter):
        df = n_actual - 1
        t = dist.t_two_tailed(alpha, df)
        n_siguiente = ceil((t * s / e) ** 2)
        historial.append(n_siguiente)
        if n_siguiente == n_actual:
            break
        n_actual = n_siguiente
    else:
        raise RuntimeError(
            f"El bucle iterativo no convergió en {max_iter} iteraciones "
            f"(historial: {historial})."
        )

    n_infinito = n_actual
    if N is None:
        return SampleSizeResult(n=n_infinito, iterations=len(historial), converged_values=historial)

    n_finito = ceil((N * n_infinito) / (N + n_infinito))
    return SampleSizeResult(n=n_finito, iterations=len(historial), converged_values=historial)


def ic_total_poblacional(result: IntervalResult, N: float) -> IntervalResult:
    """Convierte un IC de la media en un IC del total poblacional T = N * mu.

    Varios ejercicios de la guía (p. ej. peso total de una tirada de fardos,
    producción diaria total) piden T en vez de mu; se resuelve multiplicando
    los límites del IC de la media por N.
    """
    return IntervalResult(
        a=result.a * N,
        b=result.b * N,
        error=None if result.error is None else result.error * N,
        point_estimate=result.point_estimate * N,
        distribution=result.distribution,
        df=result.df,
        critical_value=result.critical_value,
        finite_population=result.finite_population,
        warnings=list(result.warnings),
    )


# ---------------------------------------------------------------------------
# 1.2 Varianza / desvío poblacional (sigma^2, sigma)
# ---------------------------------------------------------------------------

def ic_varianza(s2: float, n: int, alpha: float) -> IntervalResult:
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    df = n - 1
    chi2_up = dist.chi2_upper(alpha, df)
    chi2_low = dist.chi2_lower(alpha, df)
    a = (n - 1) * s2 / chi2_up
    b = (n - 1) * s2 / chi2_low
    return IntervalResult(
        a=a, b=b, error=None, point_estimate=s2,
        distribution="chi2", df=df, critical_value=(chi2_low, chi2_up),
    )


def ic_desvio(s2: float, n: int, alpha: float) -> IntervalResult:
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    var_result = ic_varianza(s2, n, alpha)
    return IntervalResult(
        a=sqrt(var_result.a), b=sqrt(var_result.b), error=None,
        point_estimate=sqrt(s2), distribution="chi2", df=var_result.df,
        critical_value=var_result.critical_value,
    )


# ---------------------------------------------------------------------------
# 1.3 Proporción poblacional (p)
# ---------------------------------------------------------------------------

def ic_proporcion_exacto(r: int, n: int, alpha: float) -> IntervalResult:
    """IC exacto de Clopper-Pearson (equivalente a la transformación F que usa la
    cátedra, ver TEMA III de la guía de problemas). Es el método que la guía usa
    como resultado principal para el IC de una proporción, sea cual sea n.
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    if r < 0 or r > n:
        raise ValueError(f"r debe estar entre 0 y n, no r={r} con n={n}")
    if n < 1:
        raise ValueError(f"n debe ser al menos 1, no {n}")
    p_hat = r / n
    warnings = []

    if r == 0:
        # Con r = 0 el limite inferior es exactamente 0 y no consume riesgo: el
        # intervalo tiene una sola cota, asi que el alpha entero va al extremo
        # superior (no alpha/2). Ej.: n=10, alpha=0.10 -> [0 ; 0.2057].
        a = 0.0
        b = dist.beta_value(1 - alpha, r + 1, n - r)
        warnings.append(
            "Con r = 0 el intervalo es unilateral (solo cota superior): se usa \u03b1 "
            "completo en el extremo superior, no \u03b1/2."
        )
    elif r == n:
        # Simetrico al caso anterior: el limite superior es exactamente 1.
        a = dist.beta_value(alpha, r, n - r + 1)
        b = 1.0
        warnings.append(
            "Con r = n el intervalo es unilateral (solo cota inferior): se usa \u03b1 "
            "completo en el extremo inferior, no \u03b1/2."
        )
    else:
        a = dist.beta_value(alpha / 2, r, n - r + 1)
        b = dist.beta_value(1 - alpha / 2, r + 1, n - r)

    return IntervalResult(
        a=a, b=b, error=(b - a) / 2, point_estimate=p_hat,
        distribution="F (Clopper-Pearson)", warnings=warnings,
    )


def ic_proporcion_normal(p_hat: float, n: int, alpha: float) -> IntervalResult:
    """Aproximación normal (§1.3 del esquema). Se mantiene como referencia/comparación:
    la guía usa el modelo exacto como resultado principal, y solo recurre a esta
    aproximación cuando no hay forma cerrada exacta (p. ej. cálculo de n).
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    if not (0 <= p_hat <= 1):
        raise ValueError(f"p_hat debe estar entre 0 y 1, no {p_hat}")
    warnings = []
    if p_hat in (0.0, 1.0):
        warnings.append(
            "Con p\u0302 = 0 (o p\u0302 = 1) el error estandar de la aproximacion normal es 0 "
            "y el intervalo degenera en un punto: usar el metodo exacto."
        )
    if n * p_hat < 5 or n * (1 - p_hat) < 5:
        warnings.append(
            "No se cumple n·p̂ ≥ 5 y n·(1-p̂) ≥ 5: la aproximación normal puede no ser confiable."
        )
    z = dist.z_two_tailed(alpha)
    se = sqrt(p_hat * (1 - p_hat) / (n - 1))
    e = z * se
    return IntervalResult(
        a=p_hat - e, b=p_hat + e, error=e, point_estimate=p_hat,
        distribution="Z", critical_value=z, warnings=warnings,
    )


def n_proporcion(p_hat: float, e: float, alpha: float) -> SampleSizeResult:
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    if not (0 <= p_hat <= 1):
        raise ValueError(f"p_hat debe estar entre 0 y 1, no {p_hat}")
    z = dist.z_two_tailed(alpha)
    n0 = ceil((z ** 2 * p_hat * (1 - p_hat)) / e ** 2 + 1)
    warnings = []
    if p_hat in (0.0, 1.0):
        warnings.append(
            "Con p\u0302 = 0 (o p\u0302 = 1) la varianza estimada p\u0302(1-p\u0302) es 0 y el n "
            "que sale no tiene sentido practico: si no hay estimacion previa "
            "confiable, usar el caso mas desfavorable p\u0302 = 0.5."
        )
    return SampleSizeResult(n=n0, warnings=warnings)
