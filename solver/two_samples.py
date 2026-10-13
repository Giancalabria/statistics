"""M3 — Comparación de parámetros para 2 poblaciones independientes y apareadas.

Implementa §3 del esquema_teorico_examen_estadistica.md:
- Test F para comparación de varianzas (igualdad de varianzas como paso obligatorio)
- IC y ensayo de diferencia de medias con varianzas supuestas iguales (pooled)
- IC y ensayo de diferencia de medias con varianzas probadas distintas (Welch)
- IC y ensayo de diferencia de medias para muestras apareadas
"""

import math
from math import sqrt
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from . import distributions as dist
from .intervals import IntervalResult, SampleSizeResult, iterar_n
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
# 3.1 bis — TEMA IV completo: φ = σ₁/σ₂ contra un valor φ₀ (no solo 1)
# ---------------------------------------------------------------------------
#
# Convención: la muestra 1 va en el NUMERADOR (j² = S₁²/S₂², ν₁ = n₁-1) y φ₀ es
# la relación de DESVÍOS ("reducir el desvío un 12%" → φ₀ = 0,88). Bajo φ = φ₀:
#     j²/φ₀² ~ F(ν₁; ν₂)
# Verificado contra la guía (TEMA IV, problemas 2 a 5).

_SIGNO_H0 = {"derecha": "≤", "izquierda": "≥", "bilateral": "="}
_SIGNO_H1 = {"derecha": ">", "izquierda": "<", "bilateral": "≠"}


def _criticos_relacion(phi0: float, alpha: float, df1: int, df2: int, tail: str):
    """Valores críticos de j² = S₁²/S₂² para H0 sobre φ = σ₁/σ₂."""
    phi0_2 = phi0 ** 2
    if tail == "derecha":
        return phi0_2 * dist.f_one_tailed(alpha, df1, df2)
    if tail == "izquierda":
        return phi0_2 * dist.f_value(alpha, df1, df2)
    if tail == "bilateral":
        return (phi0_2 * dist.f_value(alpha / 2, df1, df2), phi0_2 * dist.f_two_tailed(alpha, df1, df2))
    raise ValueError(f"tail debe ser 'derecha', 'izquierda' o 'bilateral', no {tail}")


def _potencia_relacion(j2_c, phi1: float, df1: int, df2: int, tail: str) -> float:
    """P(rechazar H0 | φ = φ₁): si φ = φ₁, j²/φ₁² ~ F(ν₁; ν₂)."""
    phi1_2 = phi1 ** 2
    if tail == "derecha":
        return 1 - dist.f_cdf(j2_c / phi1_2, df1, df2)
    if tail == "izquierda":
        return dist.f_cdf(j2_c / phi1_2, df1, df2)
    c1, c2 = j2_c
    return dist.f_cdf(c1 / phi1_2, df1, df2) + 1 - dist.f_cdf(c2 / phi1_2, df1, df2)


def ensayo_relacion_desvios(
    s1: float, n1: int, s2: float, n2: int, alpha: float,
    phi0: float = 1.0, tail: str = "bilateral", phi1: Optional[float] = None,
) -> HypothesisTestResult:
    """Ensayo F sobre φ = σ₁/σ₂ con H0 en φ₀ (TEMA IV).

    - izquierda (H1: φ < φ₀, p. ej. 'reducir el desvío un 12%'): j²c = φ₀²·F(α; ν₁; ν₂)
    - derecha   (H1: φ > φ₀): j²c = φ₀²·F(1-α; ν₁; ν₂)
    - bilateral: j²c₁ = φ₀²·F(α/2), j²c₂ = φ₀²·F(1-α/2)

    Si se da φ₁ calcula β = P(no rechazar H0 | φ = φ₁) y la potencia.
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    if phi0 <= 0 or s1 <= 0 or s2 <= 0:
        raise ValueError("φ₀ y los desvíos deben ser positivos")
    df1, df2 = n1 - 1, n2 - 1
    j2 = s1 ** 2 / s2 ** 2
    crit = _criticos_relacion(phi0, alpha, df1, df2, tail)
    if tail == "derecha":
        rejects = j2 > crit
    elif tail == "izquierda":
        rejects = j2 < crit
    else:
        rejects = j2 < crit[0] or j2 > crit[1]
    result = HypothesisTestResult(
        h0_text=f"φ = σ₁/σ₂ {_SIGNO_H0[tail]} {phi0:g}",
        h1_text=f"φ = σ₁/σ₂ {_SIGNO_H1[tail]} {phi0:g}",
        tail=tail,
        critical_value=crit,
        observed_value=j2,
        rejects_h0=rejects,
        distribution="F",
        df=df1,
    )
    if phi1 is not None:
        result.power = _potencia_relacion(crit, phi1, df1, df2, tail)
        result.beta = 1 - result.power
    return result


@dataclass
class DisenoRelacionResult:
    """n (igual en ambas muestras) para que el ensayo F tenga β ≤ β objetivo en φ₁."""
    n: int
    tail: str
    j2_c: float
    beta_real: float
    potencia_real: float
    h0_text: str
    h1_text: str


def _menor_n(cumple, n_min: int = 2, n_max: int = 1_000_000) -> int:
    """Menor n entero en [n_min, n_max] con cumple(n) True (cumple es monótona en n)."""
    hi = n_min
    while not cumple(hi):
        if hi >= n_max:
            raise RuntimeError(f"No se encontró n ≤ {n_max} que cumpla las condiciones")
        hi = min(hi * 2, n_max)
    lo = max(n_min, hi // 2)
    if cumple(lo):
        return lo
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cumple(mid):
            hi = mid
        else:
            lo = mid
    return hi


def n_relacion_desvios_para_potencia(
    phi0: float, phi1: float, alpha: float, beta: float, tail: Optional[str] = None,
) -> DisenoRelacionResult:
    """Menor n (n₁ = n₂ = n) tal que el ensayo F con riesgo α tenga β ≤ `beta` en φ = φ₁.

    Búsqueda exacta sobre F con ν₁ = ν₂ = n-1 (equivale a pedir R = φ₀²/φ₁² ≥ F(1-α)·F(1-β)).
    Verificado contra la guía: IV-2 n = 483, IV-3 n = 260, IV-4 n = 128, IV-5 n = 127 y 174.
    """
    if not (0 < alpha < 1) or not (0 < beta < 1):
        raise ValueError("α y β deben estar entre 0 y 1")
    if phi0 <= 0 or phi1 <= 0 or phi0 == phi1:
        raise ValueError("φ₀ y φ₁ deben ser positivos y distintos")
    if tail is None:
        tail = "derecha" if phi1 > phi0 else "izquierda"
    if tail not in ("derecha", "izquierda"):
        raise ValueError("Para dimensionar por potencia se usa un ensayo unilateral")

    def beta_de(n):
        df = n - 1
        return 1 - _potencia_relacion(_criticos_relacion(phi0, alpha, df, df, tail), phi1, df, df, tail)

    n = _menor_n(lambda k: beta_de(k) <= beta)
    b = beta_de(n)
    return DisenoRelacionResult(
        n=n, tail=tail, j2_c=_criticos_relacion(phi0, alpha, n - 1, n - 1, tail),
        beta_real=b, potencia_real=1 - b,
        h0_text=f"φ = σ₁/σ₂ {_SIGNO_H0[tail]} {phi0:g}", h1_text=f"φ = σ₁/σ₂ {_SIGNO_H1[tail]} {phi0:g}",
    )


@dataclass
class RelacionLimitesResult:
    """n (igual en ambas muestras) para que el IC de la relación tenga B/A ≤ R objetivo."""
    n: int
    sobre: str                    # "varianzas" (σ₁²/σ₂²) o "desvios" (σ₁/σ₂)
    r_objetivo: float             # B/A buscado, en la escala de `sobre`
    r_logrado: float              # B/A real con ese n
    r_actual: Optional[float] = None
    reduccion: Optional[float] = None


def relacion_limites_f(alpha: float, df1: int, df2: int, sobre: str = "varianzas") -> float:
    """B/A del IC de σ₁²/σ₂² (= F(1-α/2; ν₁; ν₂)/F(α/2; ν₁; ν₂)); su raíz si es para los desvíos."""
    r = dist.f_two_tailed(alpha, df1, df2) / dist.f_value(alpha / 2, df1, df2)
    return sqrt(r) if sobre == "desvios" else r


def n_relacion_por_limites(
    r_objetivo: float, alpha: float, sobre: str = "varianzas",
    r_actual: Optional[float] = None, reduccion: Optional[float] = None,
) -> RelacionLimitesResult:
    """Menor n (n₁ = n₂ = n) tal que el IC de la relación tenga B/A ≤ r_objetivo.

    No depende de los desvíos muestrales: B/A = F(1-α/2; ν; ν)/F(α/2; ν; ν).
    Verificado contra la guía: IV-1 b) n = 45 (varianzas), d) n = 444 (desvíos); IV-3 e) n = 68.
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    if sobre not in ("varianzas", "desvios"):
        raise ValueError("sobre debe ser 'varianzas' o 'desvios'")
    if r_objetivo <= 1:
        raise ValueError(f"La relación objetivo entre límites debe ser mayor que 1, no {r_objetivo}")
    n = _menor_n(lambda k: relacion_limites_f(alpha, k - 1, k - 1, sobre) <= r_objetivo)
    return RelacionLimitesResult(n=n, sobre=sobre, r_objetivo=r_objetivo,
                                 r_logrado=relacion_limites_f(alpha, n - 1, n - 1, sobre),
                                 r_actual=r_actual, reduccion=reduccion)


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
    # S_p cuando n1 = n2 = n: S_p = sqrt((S1^2 + S2^2) / 2)
    s_p = math.sqrt((s1 ** 2 + s2 ** 2) / 2)

    # Formula: n = 2 * (t * S_p / e)^2, con ν = 2n - 2
    n_actual, historial = iterar_n(
        lambda n: math.ceil(2 * ((dist.t_two_tailed(alpha, 2 * n - 2) * s_p) / e) ** 2), n_inicial, max_iter
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
    n_actual, historial = iterar_n(
        lambda n: math.ceil((dist.t_two_tailed(alpha, n - 1) * s_d / e) ** 2), n_inicial, max_iter
    )
    return SampleSizeResult(n=n_actual, iterations=len(historial), converged_values=historial)


# ---------------------------------------------------------------------------
# 3.4 Comparación de medias general (TEMA V): pooled / Welch / σ conocidos,
#     hipótesis con diferencia δ₀ o proporcional (μ₁ = h·μ₂) y n con tamaños iguales
# ---------------------------------------------------------------------------
#
# Con h ≠ 1 el parámetro es δ* = μ₁ - h·μ₂ (p. ej. 'B supera a A en un 24%' → H0: μB ≤ 1,24·μA):
#     d* = x̄₁ - h·x̄₂,  σ(d*) = √(S₁²/n₁ + h²·S₂²/n₂)  (Welch)   o   Sa·√(1/n₁ + h²/n₂)  (pooled).
# Verificado contra la guía: V-6 b) d*c = 0,0438, d) h = 1,2329; V-3 d) h = 1,0506; V-8 d) 4,90 %.

METODOS_DOS_MEDIAS = ("pooled", "welch", "z")


@dataclass
class ErrorDosMedias:
    """Error estándar de d* = x̄₁ - h·x̄₂ y sus grados de libertad."""
    se: float
    df: Optional[int]               # None si es Z (σ conocidos)
    df_raw: Optional[float] = None  # ν de Aspin-Welch sin redondear
    s_a: Optional[float] = None     # desvío amalgamado (pooled)


def error_dos_medias(s1: float, n1: int, s2: float, n2: int, metodo: str, h: float = 1.0) -> ErrorDosMedias:
    """σ(d*) para pooled (Sa), Welch (ν de Aspin-Welch, redondeado hacia abajo) o Z (σ₁, σ₂ conocidos)."""
    if metodo not in METODOS_DOS_MEDIAS:
        raise ValueError(f"metodo debe ser uno de {METODOS_DOS_MEDIAS}, no {metodo}")
    if metodo == "pooled":
        s_a = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
        return ErrorDosMedias(se=s_a * math.sqrt(1 / n1 + h ** 2 / n2), df=n1 + n2 - 2, s_a=s_a)
    v1, v2 = s1 ** 2 / n1, h ** 2 * s2 ** 2 / n2
    if metodo == "z":
        return ErrorDosMedias(se=math.sqrt(v1 + v2), df=None)
    nu = (v1 + v2) ** 2 / (v1 ** 2 / (n1 - 1) + v2 ** 2 / (n2 - 1))
    return ErrorDosMedias(se=math.sqrt(v1 + v2), df=math.floor(nu), df_raw=nu)


def _fractil(alpha: float, df: Optional[int], dos_colas: bool) -> float:
    if df is None:
        return dist.z_two_tailed(alpha) if dos_colas else dist.z_one_tailed(alpha)
    return dist.t_two_tailed(alpha, df) if dos_colas else dist.t_one_tailed(alpha, df)


@dataclass
class EnsayoDosMediasResult(HypothesisTestResult):
    """Ensayo sobre δ* = μ₁ - h·μ₂ (h = 1: la diferencia de medias de siempre)."""
    se: float = 0.0
    fractil: float = 0.0
    h: float = 1.0
    delta0: float = 0.0
    metodo: str = "pooled"
    df_raw: Optional[float] = None
    s_a: Optional[float] = None


def ensayo_dos_medias(
    xbar1: float, s1: float, n1: int, xbar2: float, s2: float, n2: int,
    alpha: float, tail: str = "derecha", delta0: float = 0.0, h: float = 1.0, metodo: str = "pooled",
) -> EnsayoDosMediasResult:
    """Ensayo de H0 sobre δ* = μ₁ - h·μ₂ contra δ₀ (s1, s2 son σ₁, σ₂ si metodo = 'z').

    Valor crítico: d*c = δ₀ ± fractil·σ(d*) (t con ν de pooled / Welch, o Z)."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    if tail not in _SIGNO_H0:
        raise ValueError(f"tail debe ser 'derecha', 'izquierda' o 'bilateral', no {tail}")
    err = error_dos_medias(s1, n1, s2, n2, metodo, h)
    q = _fractil(alpha, err.df, tail == "bilateral")
    d = xbar1 - h * xbar2
    if tail == "derecha":
        crit = delta0 + q * err.se
        rejects = d > crit
    elif tail == "izquierda":
        crit = delta0 - q * err.se
        rejects = d < crit
    else:
        crit = (delta0 - q * err.se, delta0 + q * err.se)
        rejects = d < crit[0] or d > crit[1]
    param = "δ" if h == 1 else f"δ* = μ₁ - {h:g}·μ₂"
    z = (d - delta0) / err.se
    from scipy import stats
    cdf = stats.norm.cdf(z) if err.df is None else stats.t.cdf(z, err.df)
    p_value = 1 - cdf if tail == "derecha" else cdf if tail == "izquierda" else 2 * min(cdf, 1 - cdf)
    return EnsayoDosMediasResult(
        h0_text=f"{param} {_SIGNO_H0[tail]} {delta0:g}", h1_text=f"{param} {_SIGNO_H1[tail]} {delta0:g}",
        tail=tail, critical_value=crit, observed_value=d, rejects_h0=rejects,
        distribution="Z" if err.df is None else "t", df=err.df, p_value=float(p_value),
        se=err.se, fractil=q, h=h, delta0=delta0, metodo=metodo, df_raw=err.df_raw, s_a=err.s_a,
    )


def ic_dos_medias(
    xbar1: float, s1: float, n1: int, xbar2: float, s2: float, n2: int,
    alpha: float, metodo: str = "pooled", cota: Optional[str] = None,
) -> IntervalResult:
    """IC para δ = μ₁ - μ₂. `cota` = 'inf' / 'sup': límite unilateral (α entero en una cola)."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    err = error_dos_medias(s1, n1, s2, n2, metodo)
    q = _fractil(alpha, err.df, cota is None)
    d = xbar1 - xbar2
    e = q * err.se
    a = d - e if cota in (None, "inf") else -math.inf
    b = d + e if cota in (None, "sup") else math.inf
    return IntervalResult(a=a, b=b, error=e, point_estimate=d, distribution="Z" if err.df is None else "t",
                          df=err.df, critical_value=q)


def h_limite_dos_medias(
    xbar1: float, s1: float, n1: int, xbar2: float, s2: float, n2: int,
    alpha: float, metodo: str = "pooled", cota: str = "inf",
) -> float:
    """Relación h = μ₁/μ₂ mínima ('inf') o máxima ('sup') que se garantiza con 1-α de confianza.

    Es el h que deja justo en el límite el ensayo H0: μ₁ ≤ h·μ₂ (o ≥):
        x̄₁ - h·x̄₂ ∓ fractil(1-α; ν(h))·σ(d*(h)) = 0.
    El incremento porcentual garantizado es (h - 1)·100."""
    from scipy.optimize import brentq
    signo = -1 if cota == "inf" else 1

    def f(h):
        err = error_dos_medias(s1, n1, s2, n2, metodo, h)
        return xbar1 - h * xbar2 + signo * _fractil(alpha, err.df, False) * err.se

    centro = xbar1 / xbar2
    lo, hi = centro * 0.5, centro * 1.5
    for _ in range(60):
        if f(lo) * f(hi) < 0:
            break
        lo, hi = lo * 0.5, hi * 2
    return brentq(f, lo, hi, xtol=1e-12)


def nu_welch_iguales(s1: float, s2: float, n: int) -> float:
    """ν de Aspin-Welch con n₁ = n₂ = n: (n-1)·(S₁² + S₂²)²/(S₁⁴ + S₂⁴)."""
    return (n - 1) * (s1 ** 2 + s2 ** 2) ** 2 / (s1 ** 4 + s2 ** 4)


def n_dos_medias_para_error(
    s1: float, s2: float, e: float, alpha: float, metodo: str = "pooled", n_inicial: int = 30, max_iter: int = 50,
) -> SampleSizeResult:
    """n (igual en ambas muestras) para que el error del IC de δ sea e.

    e = fractil·√((S₁² + S₂²)/n): pooled con ν = 2n - 2, Welch con ν = ⌊(n-1)(S₁²+S₂²)²/(S₁⁴+S₂⁴)⌋, Z sin iterar.
    Verificado contra la guía: V-1 c) n = 45 (pooled), V-3 c) n = 43 (Welch)."""
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    if metodo == "pooled":
        return n_media_diferencia_varianzas_iguales_para_error(s1, s2, e, alpha, n_inicial, max_iter)
    suma = s1 ** 2 + s2 ** 2
    if metodo == "z":
        n = math.ceil(dist.z_two_tailed(alpha) ** 2 * suma / e ** 2)
        return SampleSizeResult(n=n, iterations=1, converged_values=[n])
    n_actual, historial = iterar_n(
        lambda n: math.ceil(dist.t_two_tailed(alpha, max(1, math.floor(nu_welch_iguales(s1, s2, n)))) ** 2 * suma / e ** 2),
        n_inicial, max_iter,
    )
    return SampleSizeResult(n=n_actual, iterations=len(historial), converged_values=historial)


def verificar_desvio_afirmado(s: float, n: int, sigma0: float, alpha: float) -> Tuple[float, bool]:
    """¿El desvío que se afirma conocido (σ₀) es compatible con la muestra? H0: σ ≤ σ₀ (cola derecha, χ²).

    Devuelve (Sc, rechaza): Sc = σ₀·√(χ²(1-α; n-1)/(n-1)); si S > Sc el σ afirmado no vale y se trabaja con S."""
    sc = sigma0 * math.sqrt(dist.chi2_value(1 - alpha, n - 1) / (n - 1))
    return sc, s > sc
