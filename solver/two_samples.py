"""M3 — Comparación de parámetros para 2 poblaciones independientes y apareadas.

Implementa §3 del esquema_teorico_examen_estadistica.md:
- Test F para comparación de varianzas (igualdad de varianzas como paso obligatorio)
- IC y ensayo de diferencia de medias con varianzas supuestas iguales (pooled)
- IC y ensayo de diferencia de medias con varianzas probadas distintas (Welch)
- IC y ensayo de diferencia de medias para muestras apareadas
"""

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from . import distributions as dist
from .intervals import IntervalResult, SampleSizeResult
from .hypothesis_one import HypothesisTestResult


# ---------------------------------------------------------------------------
# 3.1 Test F — Comparación de varianzas
# ---------------------------------------------------------------------------

def f_test_equal_variances(
    s1: float, n1: int, s2: float, n2: int, alpha: float
) -> HypothesisTestResult:
    """Test F para decidir entre pooled (σ1²=σ2²) y Welch (σ1²≠σ2²).

    Convención de la cátedra (verificada contra los ejercicios reales NDMA y
    de la hiladora, TEMA V): se coloca la varianza muestral MAYOR en el
    numerador para que j² >= 1, y se usa el valor crítico F_(1-α; df_num, df_den)
    con α COMPLETO (no α/2). Aunque H0 se enuncia como σ1²=σ2² (aparentemente
    bilateral), la cátedra siempre lo resuelve como un test de una cola sobre
    la relación ya orientada hacia la varianza mayor.
    Los grados de libertad corresponden a la muestra que quedó en el numerador.
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    s2_1 = s1 ** 2
    s2_2 = s2 ** 2

    # Determinar cuál varianza es mayor
    if s2_1 >= s2_2:
        s2_mayor = s2_1
        s2_menor = s2_2
        n_mayor = n1
        n_menor = n2
    else:
        s2_mayor = s2_2
        s2_menor = s2_1
        n_mayor = n2
        n_menor = n1

    j_squared = s2_mayor / s2_menor
    df_num = n_mayor - 1
    df_den = n_menor - 1

    # F_c = F_{(1-alpha; df_num, df_den)}, alpha completo (convención verificada
    # contra ejercicios reales NDMA y hiladora, no alpha/2).
    f_c = dist.f_one_tailed(alpha, df_num, df_den)

    rejects = j_squared > f_c

    result = HypothesisTestResult(
        h0_text=f"σ₁² = σ₂²",
        h1_text=f"σ₁² ≠ σ₂²",
        tail="bilateral",
        critical_value=f_c,
        observed_value=j_squared,
        rejects_h0=rejects,
        distribution="F",
        df=df_num,  # numerator df, the relevant one for rejection
    )

    return result


def ic_ratio_varianzas(
    s1: float, n1: int, s2: float, n2: int, alpha: float
) -> Tuple[IntervalResult, IntervalResult]:
    """IC para la razón de varianzas φ² = σ₁²/σ₂² (sin reordenar por magnitud).

    Devuelve:
    - IntervalResult para φ² = σ₁²/σ₂²
    - IntervalResult para 1/φ² = σ₂²/σ₁² (la razón inversa)
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    s2_1 = s1 ** 2
    s2_2 = s2 ** 2
    ratio = s2_1 / s2_2

    # IC directo: σ₁²/σ₂²
    f_upper = dist.f_two_tailed(alpha, n1 - 1, n2 - 1)  # F_{(1-α/2; n₁-1, n₂-1)}
    f_lower = dist.f_value(alpha / 2, n1 - 1, n2 - 1)   # F_{(α/2; n₁-1, n₂-1)}

    a_direct = ratio / f_upper
    b_direct = ratio / f_lower

    result_direct = IntervalResult(
        a=a_direct,
        b=b_direct,
        error=(b_direct - a_direct) / 2,
        point_estimate=ratio,
        distribution="F",
        df=n1 - 1,
    )

    # IC inverso: σ₂²/σ₁²
    ratio_inv = 1 / ratio
    a_inv = 1 / b_direct
    b_inv = 1 / a_direct

    result_inverse = IntervalResult(
        a=a_inv,
        b=b_inv,
        error=(b_inv - a_inv) / 2,
        point_estimate=ratio_inv,
        distribution="F",
        df=n1 - 1,
    )

    return result_direct, result_inverse


# ---------------------------------------------------------------------------
# 3.2A Comparación de medias — varianzas IGUALES (pooled)
# ---------------------------------------------------------------------------

def ic_media_diferencia_varianzas_iguales(
    xbar1: float,
    s1: float,
    n1: int,
    xbar2: float,
    s2: float,
    n2: int,
    alpha: float,
) -> IntervalResult:
    """IC para δ = μ₁ - μ₂ usando método pooled (varianzas supuestas iguales)."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    # Cuasivarianza pooled
    s2_p = ((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)
    s_p = math.sqrt(s2_p)

    # Desvío estándar de la diferencia
    sigma_d = s_p * math.sqrt(1 / n1 + 1 / n2)

    # Grados de libertad
    df = n1 + n2 - 2

    # Valor crítico t
    t = dist.t_two_tailed(alpha, df)

    # Diferencia observada y error
    d = xbar1 - xbar2
    e = t * sigma_d

    return IntervalResult(
        a=d - e,
        b=d + e,
        error=e,
        point_estimate=d,
        distribution="t",
        df=df,
        critical_value=t,
    )


def ensayo_media_diferencia_varianzas_iguales(
    xbar1: float,
    s1: float,
    n1: int,
    xbar2: float,
    s2: float,
    n2: int,
    delta0: float,
    alpha: float,
    tail: str = "derecha",
) -> HypothesisTestResult:
    """Ensayo de hipótesis para δ = μ₁ - μ₂ usando método pooled (varianzas supuestas iguales)."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    # Cuasivarianza pooled
    s2_p = ((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)
    s_p = math.sqrt(s2_p)

    # Desvío estándar de la diferencia
    sigma_d = s_p * math.sqrt(1 / n1 + 1 / n2)

    # Grados de libertad
    df = n1 + n2 - 2

    # Diferencia observada
    d = xbar1 - xbar2

    if tail == "derecha":
        t_alpha = dist.t_one_tailed(alpha, df)
        d_c = delta0 + t_alpha * sigma_d
        h0_text = f"δ ≤ {delta0}"
        h1_text = f"δ > {delta0}"
        rejects = d > d_c
        critical_value = d_c
    elif tail == "izquierda":
        t_alpha = dist.t_one_tailed(alpha, df)
        d_c = delta0 - t_alpha * sigma_d
        h0_text = f"δ ≥ {delta0}"
        h1_text = f"δ < {delta0}"
        rejects = d < d_c
        critical_value = d_c
    elif tail == "bilateral":
        t_alpha = dist.t_two_tailed(alpha, df)
        d_c1 = delta0 - t_alpha * sigma_d
        d_c2 = delta0 + t_alpha * sigma_d
        h0_text = f"δ = {delta0}"
        h1_text = f"δ ≠ {delta0}"
        rejects = d < d_c1 or d > d_c2
        critical_value = (d_c1, d_c2)
    else:
        raise ValueError(f"tail debe ser 'derecha', 'izquierda' o 'bilateral', no {tail}")

    result = HypothesisTestResult(
        h0_text=h0_text,
        h1_text=h1_text,
        tail=tail,
        critical_value=critical_value,
        observed_value=d,
        rejects_h0=rejects,
        distribution="t",
        df=df,
    )

    return result


def n_media_diferencia_varianzas_iguales_para_error(
    s1: float,
    s2: float,
    e: float,
    alpha: float,
    n_inicial: int = 30,
    max_iter: int = 50,
) -> SampleSizeResult:
    """Calcula n (mismo en ambos grupos) para reducir el error a la mitad usando pooled.

    Asume tamaños de muestra iguales: n1 = n2 = n.
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    n_actual = n_inicial
    historial = []

    # S_p cuando n1 = n2 = n: S_p = sqrt((S1^2 + S2^2) / 2)
    s_p = math.sqrt((s1 ** 2 + s2 ** 2) / 2)

    for _ in range(max_iter):
        df = 2 * n_actual - 2
        t = dist.t_two_tailed(alpha, df)

        # Formula: n = 2 * (t * S_p / e)^2
        n_siguiente = math.ceil(2 * ((t * s_p) / e) ** 2)
        historial.append(n_siguiente)

        if n_siguiente == n_actual:
            break
        n_actual = n_siguiente
    else:
        raise RuntimeError(
            f"El bucle iterativo no convergió en {max_iter} iteraciones "
            f"(historial: {historial})."
        )

    return SampleSizeResult(n=n_actual, iterations=len(historial), converged_values=historial)


# ---------------------------------------------------------------------------
# 3.2B Comparación de medias — varianzas DISTINTAS (Welch)
# ---------------------------------------------------------------------------

def ic_media_diferencia_varianzas_distintas(
    xbar1: float,
    s1: float,
    n1: int,
    xbar2: float,
    s2: float,
    n2: int,
    alpha: float,
) -> IntervalResult:
    """IC para δ = μ₁ - μ₂ usando test de Welch (varianzas distintas)."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    # Desvío estándar de la diferencia
    sigma_d = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)

    # Grados de libertad de Welch (Aspin-Welch-Satterthwaite)
    numerator = (s1 ** 2 / n1 + s2 ** 2 / n2) ** 2
    denominator = (s1 ** 2 / n1) ** 2 / (n1 - 1) + (s2 ** 2 / n2) ** 2 / (n2 - 1)
    df_welch = math.floor(numerator / denominator)

    # Valor crítico t
    t = dist.t_two_tailed(alpha, df_welch)

    # Diferencia observada y error
    d = xbar1 - xbar2
    e = t * sigma_d

    return IntervalResult(
        a=d - e,
        b=d + e,
        error=e,
        point_estimate=d,
        distribution="t",
        df=df_welch,
        critical_value=t,
    )


def ensayo_media_diferencia_varianzas_distintas(
    xbar1: float,
    s1: float,
    n1: int,
    xbar2: float,
    s2: float,
    n2: int,
    delta0: float,
    alpha: float,
    tail: str = "derecha",
) -> HypothesisTestResult:
    """Ensayo de hipótesis para δ = μ₁ - μ₂ usando test de Welch (varianzas distintas)."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    # Desvío estándar de la diferencia
    sigma_d = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)

    # Grados de libertad de Welch
    numerator = (s1 ** 2 / n1 + s2 ** 2 / n2) ** 2
    denominator = (s1 ** 2 / n1) ** 2 / (n1 - 1) + (s2 ** 2 / n2) ** 2 / (n2 - 1)
    df_welch = math.floor(numerator / denominator)

    # Diferencia observada
    d = xbar1 - xbar2

    if tail == "derecha":
        t_alpha = dist.t_one_tailed(alpha, df_welch)
        d_c = delta0 + t_alpha * sigma_d
        h0_text = f"δ ≤ {delta0}"
        h1_text = f"δ > {delta0}"
        rejects = d > d_c
        critical_value = d_c
    elif tail == "izquierda":
        t_alpha = dist.t_one_tailed(alpha, df_welch)
        d_c = delta0 - t_alpha * sigma_d
        h0_text = f"δ ≥ {delta0}"
        h1_text = f"δ < {delta0}"
        rejects = d < d_c
        critical_value = d_c
    elif tail == "bilateral":
        t_alpha = dist.t_two_tailed(alpha, df_welch)
        d_c1 = delta0 - t_alpha * sigma_d
        d_c2 = delta0 + t_alpha * sigma_d
        h0_text = f"δ = {delta0}"
        h1_text = f"δ ≠ {delta0}"
        rejects = d < d_c1 or d > d_c2
        critical_value = (d_c1, d_c2)
    else:
        raise ValueError(f"tail debe ser 'derecha', 'izquierda' o 'bilateral', no {tail}")

    result = HypothesisTestResult(
        h0_text=h0_text,
        h1_text=h1_text,
        tail=tail,
        critical_value=critical_value,
        observed_value=d,
        rejects_h0=rejects,
        distribution="t",
        df=df_welch,
    )

    return result


# ---------------------------------------------------------------------------
# 3.3 Muestras apareadas (paired samples)
# ---------------------------------------------------------------------------

def ic_media_apareada(
    differences: List[float],
    alpha: float,
) -> IntervalResult:
    """IC para δ = μ₁ - μ₂ usando muestras apareadas (t sobre las diferencias)."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    n = len(differences)

    # Media de las diferencias
    d_bar = sum(differences) / n

    # Desvío muestral de las diferencias
    variance = sum((d - d_bar) ** 2 for d in differences) / (n - 1)
    s_d = math.sqrt(variance)

    # Grados de libertad (n-1, donde n = cantidad de pares)
    df = n - 1

    # Valor crítico t
    t = dist.t_two_tailed(alpha, df)

    # Error
    e = t * s_d / math.sqrt(n)

    return IntervalResult(
        a=d_bar - e,
        b=d_bar + e,
        error=e,
        point_estimate=d_bar,
        distribution="t",
        df=df,
        critical_value=t,
    )


def ensayo_media_apareada(
    differences: List[float],
    delta0: float,
    alpha: float,
    tail: str = "derecha",
) -> HypothesisTestResult:
    """Ensayo de hipótesis para δ = μ₁ - μ₂ usando muestras apareadas."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    n = len(differences)

    # Media de las diferencias
    d_bar = sum(differences) / n

    # Desvío muestral de las diferencias
    variance = sum((d - d_bar) ** 2 for d in differences) / (n - 1)
    s_d = math.sqrt(variance)

    # Grados de libertad
    df = n - 1

    # Error estándar
    se = s_d / math.sqrt(n)

    if tail == "derecha":
        t_alpha = dist.t_one_tailed(alpha, df)
        d_c = delta0 + t_alpha * se
        h0_text = f"δ ≤ {delta0}"
        h1_text = f"δ > {delta0}"
        rejects = d_bar > d_c
        critical_value = d_c
    elif tail == "izquierda":
        t_alpha = dist.t_one_tailed(alpha, df)
        d_c = delta0 - t_alpha * se
        h0_text = f"δ ≥ {delta0}"
        h1_text = f"δ < {delta0}"
        rejects = d_bar < d_c
        critical_value = d_c
    elif tail == "bilateral":
        t_alpha = dist.t_two_tailed(alpha, df)
        d_c1 = delta0 - t_alpha * se
        d_c2 = delta0 + t_alpha * se
        h0_text = f"δ = {delta0}"
        h1_text = f"δ ≠ {delta0}"
        rejects = d_bar < d_c1 or d_bar > d_c2
        critical_value = (d_c1, d_c2)
    else:
        raise ValueError(f"tail debe ser 'derecha', 'izquierda' o 'bilateral', no {tail}")

    result = HypothesisTestResult(
        h0_text=h0_text,
        h1_text=h1_text,
        tail=tail,
        critical_value=critical_value,
        observed_value=d_bar,
        rejects_h0=rejects,
        distribution="t",
        df=df,
    )

    return result


def n_media_apareada_para_error(
    s_d: float,
    e: float,
    alpha: float,
    n_inicial: int = 100,
    max_iter: int = 20,
) -> SampleSizeResult:
    """Calcula n (cantidad de pares) para reducir el error usando muestras apareadas.

    Método iterativo (mismo que media sigma desconocido en intervals.py).
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    n_actual = n_inicial
    historial = []

    for _ in range(max_iter):
        df = n_actual - 1
        t = dist.t_two_tailed(alpha, df)
        n_siguiente = math.ceil((t * s_d / e) ** 2)
        historial.append(n_siguiente)

        if n_siguiente == n_actual:
            break
        n_actual = n_siguiente
    else:
        raise RuntimeError(
            f"El bucle iterativo no convergió en {max_iter} iteraciones "
            f"(historial: {historial})."
        )

    return SampleSizeResult(n=n_actual, iterations=len(historial), converged_values=historial)
