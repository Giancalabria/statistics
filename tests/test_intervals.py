"""Tests de solver/distributions.py y solver/intervals.py (M1).

Dos niveles de verificación:
1. distributions.py se valida contra valores de tabla conocidos (Z, t, chi2, F)
   — ancla los wrappers de scipy a la estadística "de manual".
2. intervals.py se valida recalculando cada fórmula del esquema teórico de forma
   independiente en el propio test (usando distributions.py, no intervals.py),
   para detectar errores de cableado: denominador n vs n-1, qué percentil de
   chi2 va con qué límite, ubicación del factor de finitud, redondeos, etc.
"""

import math

import pytest

from solver import distributions as dist
from solver import intervals


# ---------------------------------------------------------------------------
# 1. distributions.py contra valores de tabla conocidos
# ---------------------------------------------------------------------------

def test_z_two_tailed_95():
    assert dist.z_two_tailed(0.05) == pytest.approx(1.95996, rel=1e-4)


def test_t_two_tailed_df99_matches_gemini_example():
    # Caso citado en respuesta_gemini.md: n=100 -> nu=99 -> t ~= 1.9842
    assert dist.t_two_tailed(0.05, 99) == pytest.approx(1.9842, rel=1e-3)


def test_t_two_tailed_df24_table_value():
    assert dist.t_two_tailed(0.05, 24) == pytest.approx(2.064, rel=1e-3)


def test_chi2_table_values_df10():
    assert dist.chi2_lower(0.05, 10) == pytest.approx(3.247, rel=2e-3)
    assert dist.chi2_upper(0.05, 10) == pytest.approx(20.483, rel=2e-3)


def test_f_table_value_5_10():
    assert dist.f_one_tailed(0.05, 5, 10) == pytest.approx(3.33, rel=2e-3)


# ---------------------------------------------------------------------------
# 2. intervals.py — media (sigma conocido / desconocido)
# ---------------------------------------------------------------------------

def test_ic_media_sigma_conocido_poblacion_infinita():
    xbar, sigma, n, alpha = 50.0, 10.0, 25, 0.05
    result = intervals.ic_media_sigma_conocido(xbar, sigma, n, alpha)

    z = dist.z_two_tailed(alpha)
    e_esperado = z * sigma / math.sqrt(n)

    assert result.error == pytest.approx(e_esperado)
    assert result.a == pytest.approx(xbar - e_esperado)
    assert result.b == pytest.approx(xbar + e_esperado)
    assert not result.finite_population


def test_ic_media_sigma_conocido_poblacion_finita():
    xbar, sigma, n, alpha, N = 50.0, 10.0, 25, 0.05, 1000
    result = intervals.ic_media_sigma_conocido(xbar, sigma, n, alpha, N=N)

    z = dist.z_two_tailed(alpha)
    e_esperado = z * sigma / math.sqrt(n) * dist.fpc(N, n)

    assert result.error == pytest.approx(e_esperado)
    assert result.finite_population
    # El factor de finitud (<1) debe angostar el intervalo respecto de la población infinita
    infinita = intervals.ic_media_sigma_conocido(xbar, sigma, n, alpha)
    assert result.error < infinita.error


def test_ic_media_sigma_desconocido():
    xbar, s, n, alpha = 50.0, 10.0, 25, 0.05
    result = intervals.ic_media_sigma_desconocido(xbar, s, n, alpha)

    t = dist.t_two_tailed(alpha, n - 1)
    e_esperado = t * s / math.sqrt(n)

    assert result.df == n - 1
    assert result.error == pytest.approx(e_esperado)
    assert result.a == pytest.approx(xbar - e_esperado)
    assert result.b == pytest.approx(xbar + e_esperado)


def test_n_media_sigma_conocido():
    sigma, e, alpha = 10.0, 2.0, 0.05
    result = intervals.n_media_sigma_conocido(sigma, e, alpha)

    z = dist.z_two_tailed(alpha)
    n_esperado = math.ceil((z * sigma / e) ** 2)

    assert result.n == n_esperado


def test_n_media_sigma_conocido_redondea_siempre_hacia_arriba():
    # Regla obligatoria del esquema (§5): n nunca se redondea hacia abajo.
    sigma, e, alpha = 10.0, 2.0, 0.05
    result = intervals.n_media_sigma_conocido(sigma, e, alpha)
    z = dist.z_two_tailed(alpha)
    n_exacto = (z * sigma / e) ** 2
    assert result.n >= n_exacto


def test_n_media_sigma_desconocido_converge_y_es_punto_fijo():
    s, e, alpha = 10.0, 4.0, 0.05
    result = intervals.n_media_sigma_desconocido(s, e, alpha)

    # El esquema garantiza convergencia en <= 3 iteraciones habituales; damos margen.
    assert result.iterations <= 6

    # Punto fijo: recalcular n con el t del propio resultado debe devolver el mismo n.
    df = result.n - 1
    t = dist.t_two_tailed(alpha, df)
    n_recalculado = math.ceil((t * s / e) ** 2)
    assert n_recalculado == result.n


def test_n_media_sigma_desconocido_poblacion_finita_es_menor_o_igual():
    s, e, alpha, N = 10.0, 4.0, 0.05, 500
    infinita = intervals.n_media_sigma_desconocido(s, e, alpha)
    finita = intervals.n_media_sigma_desconocido(s, e, alpha, N=N)
    assert finita.n <= infinita.n


# ---------------------------------------------------------------------------
# 3. intervals.py — varianza / desvío
# ---------------------------------------------------------------------------

def test_ic_varianza():
    s2, n, alpha = 25.0, 20, 0.05
    result = intervals.ic_varianza(s2, n, alpha)

    df = n - 1
    chi2_up = dist.chi2_upper(alpha, df)
    chi2_low = dist.chi2_lower(alpha, df)
    a_esperado = (n - 1) * s2 / chi2_up
    b_esperado = (n - 1) * s2 / chi2_low

    assert result.a == pytest.approx(a_esperado)
    assert result.b == pytest.approx(b_esperado)
    assert result.a < s2 < result.b  # el estimador puntual debe caer dentro del IC


def test_ic_desvio_es_raiz_de_ic_varianza():
    s2, n, alpha = 25.0, 20, 0.05
    var_result = intervals.ic_varianza(s2, n, alpha)
    desvio_result = intervals.ic_desvio(s2, n, alpha)

    assert desvio_result.a == pytest.approx(math.sqrt(var_result.a))
    assert desvio_result.b == pytest.approx(math.sqrt(var_result.b))


def test_ic_desvio_caso_real_de_la_guia():
    # TEMA II, problema 11b: n=20, S=25 U$s, IC del 80% -> Entre 20,89 y 31,93 U$s
    result = intervals.ic_desvio(25.0 ** 2, 20, 0.20)
    assert result.a == pytest.approx(20.89, abs=1e-2)
    assert result.b == pytest.approx(31.93, abs=1e-2)


@pytest.mark.parametrize(
    "xbar, sigma, n, alpha, a_esperado, b_esperado",
    [
        # TEMA I de la guía de problemas de la cátedra, casos con sigma conocido.
        (246.0, 15.0, 10, 0.10, 238.19, 253.81),   # problema 1a
        (15.0, 5.0, 42, 0.01, 13.01, 16.99),       # problema 2b
        (38.0, 4.2, 20, 0.05, 36.15, 39.85),       # problema 5a
    ],
)
def test_ic_media_sigma_conocido_casos_reales_de_la_guia(xbar, sigma, n, alpha, a_esperado, b_esperado):
    result = intervals.ic_media_sigma_conocido(xbar, sigma, n, alpha)
    assert result.a == pytest.approx(a_esperado, abs=1e-2)
    assert result.b == pytest.approx(b_esperado, abs=1e-2)


def test_ic_media_sigma_desconocido_caso_real_de_la_guia():
    # TEMA I, problema 4a: ventas semanales, n=4, xbar=17.35, S=1.793507, 95% confianza
    result = intervals.ic_media_sigma_desconocido(17.35, 1.793507, 4, 0.05)
    assert result.a == pytest.approx(14.4961, abs=1e-2)
    assert result.b == pytest.approx(20.2039, abs=1e-2)


def test_n_media_sigma_desconocido_caso_real_de_la_guia():
    # TEMA I, problema 4b: mismo enunciado, error deseado e=1 -> n=15 (se verifica
    # además el camino de iteración documentado en la guía: 100 -> 13 -> 16 -> 15 -> 15)
    result = intervals.n_media_sigma_desconocido(s=1.793507, e=1, alpha=0.05)
    assert result.n == 15
    assert result.converged_values == [13, 16, 15, 15]


# ---------------------------------------------------------------------------
# 4. intervals.py — proporción
# ---------------------------------------------------------------------------

def test_ic_proporcion_normal_sin_warning_cuando_se_cumple_condicion():
    p_hat, n, alpha = 0.3, 100, 0.05
    result = intervals.ic_proporcion_normal(p_hat, n, alpha)

    z = dist.z_two_tailed(alpha)
    e_esperado = z * math.sqrt(p_hat * (1 - p_hat) / (n - 1))

    assert result.error == pytest.approx(e_esperado)
    assert result.warnings == []


def test_ic_proporcion_normal_advierte_cuando_np_menor_a_5():
    p_hat, n, alpha = 0.02, 100, 0.05  # n*p_hat = 2 < 5
    result = intervals.ic_proporcion_normal(p_hat, n, alpha)
    assert len(result.warnings) == 1


@pytest.mark.parametrize(
    "r, n, alpha, a_esperado, b_esperado",
    [
        # TEMA III de la guía de problemas de la cátedra (todos calculados "de
        # manera exacta" según la aclaración de esa sección — no aproximación normal).
        (150, 600, 0.10, 0.2210, 0.2808),  # problema 1
        (3, 25, 0.05, 0.0254, 0.3122),      # problema 2a
        (1, 10, 0.10, 0.0051, 0.3942),      # problema 3a
        (0, 10, 0.10, 0.0, 0.2589),         # problema 3b
        (60, 600, 0.05, 0.0771, 0.1269),    # problema 4
        (198, 1000, 0.05, 0.1737, 0.2241),  # problema 5
        (9, 30, 0.05, 0.1473, 0.4940),      # problema 6
        (14, 100, 0.10, 0.0866, 0.2102),    # problema 8a
    ],
)
def test_ic_proporcion_exacto_casos_reales_de_la_guia(r, n, alpha, a_esperado, b_esperado):
    result = intervals.ic_proporcion_exacto(r, n, alpha)
    assert result.a == pytest.approx(a_esperado, abs=1e-3)
    assert result.b == pytest.approx(b_esperado, abs=1e-3)


def test_ic_proporcion_exacto_r_igual_a_n():
    result = intervals.ic_proporcion_exacto(10, 10, 0.05)
    assert result.b == 1.0


def test_ic_total_poblacional_multiplica_limites_por_n():
    xbar, sigma, n, alpha, N = 50.0, 10.0, 25, 0.05, 1000
    result = intervals.ic_media_sigma_conocido(xbar, sigma, n, alpha, N=N)
    total = intervals.ic_total_poblacional(result, N)

    assert total.a == pytest.approx(result.a * N)
    assert total.b == pytest.approx(result.b * N)
    assert total.point_estimate == pytest.approx(xbar * N)
    assert total.error == pytest.approx(result.error * N)


def test_n_proporcion():
    p_hat, e, alpha = 0.5, 0.05, 0.05
    result = intervals.n_proporcion(p_hat, e, alpha)

    z = dist.z_two_tailed(alpha)
    n_esperado = math.ceil((z ** 2 * p_hat * (1 - p_hat)) / e ** 2 + 1)

    assert result.n == n_esperado


# ---------------------------------------------------------------------------
# Validación de inputs (Fase 5 — Pulido)
# ---------------------------------------------------------------------------

def test_ic_media_sigma_conocido_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        intervals.ic_media_sigma_conocido(100, 15, 30, 1.5)

    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        intervals.ic_media_sigma_conocido(100, 15, 30, -0.05)


def test_ic_media_sigma_desconocido_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        intervals.ic_media_sigma_desconocido(100, 15, 30, 1.5)


def test_n_media_sigma_conocido_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        intervals.n_media_sigma_conocido(15, 5, 1.1)


def test_n_media_sigma_desconocido_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        intervals.n_media_sigma_desconocido(15, 5, 0.0)


def test_ic_varianza_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        intervals.ic_varianza(225, 30, 1.5)


def test_ic_desvio_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        intervals.ic_desvio(225, 30, -0.1)


def test_ic_proporcion_exacto_error_r_mayor_a_n():
    """Validar que r no puede ser mayor a n."""
    with pytest.raises(ValueError, match="r debe estar entre 0 y n"):
        intervals.ic_proporcion_exacto(15, 10, 0.05)


def test_ic_proporcion_exacto_error_r_negativo():
    """Validar que r no puede ser negativo."""
    with pytest.raises(ValueError, match="r debe estar entre 0 y n"):
        intervals.ic_proporcion_exacto(-1, 10, 0.05)


def test_ic_proporcion_exacto_error_n_menor_a_1():
    """Validar que n debe ser al menos 1."""
    with pytest.raises(ValueError, match="n debe ser al menos 1"):
        intervals.ic_proporcion_exacto(0, 0, 0.05)


def test_ic_proporcion_exacto_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        intervals.ic_proporcion_exacto(5, 10, 1.5)


def test_ic_proporcion_normal_error_p_hat_fuera_de_rango():
    """Validar que p_hat debe estar entre 0 y 1 (exclusivo)."""
    with pytest.raises(ValueError, match="p_hat debe estar entre 0 y 1"):
        intervals.ic_proporcion_normal(0.0, 30, 0.05)

    with pytest.raises(ValueError, match="p_hat debe estar entre 0 y 1"):
        intervals.ic_proporcion_normal(1.0, 30, 0.05)


def test_ic_proporcion_normal_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        intervals.ic_proporcion_normal(0.5, 30, -0.05)


def test_n_proporcion_error_p_hat_fuera_de_rango():
    """Validar que p_hat debe estar entre 0 y 1 (exclusivo)."""
    with pytest.raises(ValueError, match="p_hat debe estar entre 0 y 1"):
        intervals.n_proporcion(0.0, 0.05, 0.05)


def test_n_proporcion_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        intervals.n_proporcion(0.5, 0.05, 2.0)
