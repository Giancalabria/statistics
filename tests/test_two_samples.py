"""Tests de solver/two_samples.py (M3 — Comparación de 2 poblaciones).

Validación contra ejercicios reales de TEMA IV y V de la guía de problemas.
"""

import math
import pytest

from solver import two_samples as ts
from solver import distributions as dist


# ---------------------------------------------------------------------------
# Test F — IC de razón de varianzas (dos tornos, TEMA IV problema 1)
# ---------------------------------------------------------------------------

def test_f_test_pooled_vs_welch_ndma():
    """Test F (decisión pooled/Welch): TEMA V problema 1 (NDMA).

    n_V=12, S_V=0.9653; n_N=12, S_N=1.0; α=0.10.
    Convención de cátedra: F_c = F_(1-alpha; df_num, df_den), alpha completo
    (verificado contra el desarrollo textual: F_(0.90;11,11) = 2.2269).
    j² = 1.0²/0.9653² = 1.0732 < 2.2269 → NO se rechaza (se asume pooled).
    """
    result = ts.f_test_equal_variances(s1=1.0, n1=12, s2=0.9653, n2=12, alpha=0.10)

    assert result.observed_value == pytest.approx(1.0732, rel=1e-3)
    assert result.critical_value == pytest.approx(2.2269, rel=1e-3)
    assert not result.rejects_h0


def test_f_test_pooled_vs_welch_hiladora():
    """Test F (decisión pooled/Welch): TEMA V problema 3 (hiladora).

    n_CR=4, S_CR=132; n_SR=16, S_SR=354; α=0.10.
    Verificado contra el desarrollo textual: F_(0.90;15,3) = 5.2003.
    j² = 354²/132² = 7.1922 > 5.2003 → SE RECHAZA (se usa Welch).
    """
    result = ts.f_test_equal_variances(s1=132, n1=4, s2=354, n2=16, alpha=0.10)

    assert result.observed_value == pytest.approx(7.1922, rel=1e-3)
    assert result.critical_value == pytest.approx(5.2003, rel=1e-3)
    assert result.rejects_h0


def test_ic_ratio_varianzas_dos_tornos():
    """IC para razón de varianzas: TEMA IV problema 1 (dos tornos).

    S1=3.6, n1=13, S2=5.4, n2=25, α=0.10
    IC para σ1²/σ2²: entre 0.2036 y 1.1135
    IC para σ2²/σ1²: entre 0.8980 y 4.9126
    """
    result_direct, result_inverse = ts.ic_ratio_varianzas(
        s1=3.6, n1=13, s2=5.4, n2=25, alpha=0.10
    )

    # IC directo σ1²/σ2²
    assert result_direct.a == pytest.approx(0.2036, abs=0.002)
    assert result_direct.b == pytest.approx(1.1135, abs=0.002)

    # IC inverso σ2²/σ1²
    assert result_inverse.a == pytest.approx(0.8980, abs=0.002)
    assert result_inverse.b == pytest.approx(4.9126, abs=0.002)


# ---------------------------------------------------------------------------
# Pooled — medias, varianzas iguales (NDMA, TEMA V problema 1)
# ---------------------------------------------------------------------------

def test_ic_media_diferencia_varianzas_iguales_ndma():
    """IC para μ_viejo - μ_nuevo (varianzas iguales, pooled): TEMA V problema 1.

    n1=12 (viejo), S1=0.9653, x̄1=5.25
    n2=12 (nuevo), S2=1.0, x̄2=1.5
    α=0.10
    Esperado: IC 90% entre 3.06 y 4.44 (e=0.689)
    """
    result = ts.ic_media_diferencia_varianzas_iguales(
        xbar1=5.25, s1=0.9653, n1=12,
        xbar2=1.5, s2=1.0, n2=12,
        alpha=0.10
    )

    assert result.a == pytest.approx(3.06, abs=0.01)
    assert result.b == pytest.approx(4.44, abs=0.01)
    assert result.error == pytest.approx(0.689, abs=0.005)


def test_ensayo_media_diferencia_varianzas_iguales_ndma():
    """Ensayo H0: δ ≤ 0 (cola derecha) α=0.01: TEMA V problema 1.

    n1=12 (viejo), S1=0.9653, x̄1=5.25
    n2=12 (nuevo), S2=1.0, x̄2=1.5
    Esperado: d_c=1.0064, d_observado=3.75 > d_c → se rechaza H0
    """
    result = ts.ensayo_media_diferencia_varianzas_iguales(
        xbar1=5.25, s1=0.9653, n1=12,
        xbar2=1.5, s2=1.0, n2=12,
        delta0=0.0, alpha=0.01, tail="derecha"
    )

    assert result.observed_value == pytest.approx(3.75, abs=0.001)
    assert result.critical_value == pytest.approx(1.0064, abs=0.001)
    assert result.rejects_h0


def test_n_media_diferencia_varianzas_iguales_ndma():
    """Cálculo de n para reducir error a la mitad: TEMA V problema 1.

    S1=0.9653, S2=1.0, e_actual=0.689, e_deseado=0.3445, α=0.10
    Esperado: n=45
    """
    result = ts.n_media_diferencia_varianzas_iguales_para_error(
        s1=0.9653, s2=1.0,
        e=0.3445, alpha=0.10
    )

    assert result.n == 45


# ---------------------------------------------------------------------------
# Welch — medias, varianzas distintas (hiladora, TEMA V problema 3)
# ---------------------------------------------------------------------------

def test_ensayo_media_diferencia_varianzas_distintas_hiladora():
    """Test F y ensayo Welch: TEMA V problema 3 (hiladora).

    n1=4 (CR), S1=132, x̄1=1470
    n2=16 (SR), S2=354, x̄2=1208

    IMPORTANTE: el enunciado usa dos niveles de riesgo distintos:
    - α=0.10 SOLO para decidir el método (Test F pooled vs Welch), convención
      de cátedra independiente del riesgo pedido en el enunciado.
    - α=0.05 para el ensayo de hipótesis en sí ("riesgo máximo del 5%" según
      el enunciado real de TEMA V problema 3).

    Test F: F_(0.90;15,3)=5.2003, j²=7.1922 > 5.2003 → rechaza → usar Welch
    Ensayo (α=0.05): d_c=194.4494, d_observado=262 > d_c → se rechaza H0
    """
    # Primero: Test F (confirma que corresponde usar Welch, ver test_f_test_pooled_vs_welch_hiladora)
    f_result = ts.f_test_equal_variances(s1=132, n1=4, s2=354, n2=16, alpha=0.10)
    assert f_result.observed_value == pytest.approx(7.1922, rel=1e-3)
    assert f_result.rejects_h0

    # Ensayo Welch: H0: δ ≤ 0, cola derecha, α=0.05 (riesgo del enunciado, no el del Test F)
    result = ts.ensayo_media_diferencia_varianzas_distintas(
        xbar1=1470, s1=132, n1=4,
        xbar2=1208, s2=354, n2=16,
        delta0=0.0, alpha=0.05, tail="derecha"
    )

    assert result.observed_value == pytest.approx(262, abs=0.001)
    assert result.critical_value == pytest.approx(194.4494, abs=0.01)
    assert result.df == 14  # truncado de 14.2641
    assert result.rejects_h0


def test_ic_media_diferencia_varianzas_distintas_hiladora():
    """IC 90% para μ_CR - μ_SR (Welch): TEMA V problema 3.

    Esperado: entre 67.55 y 456.45 (e=194.4494)
    """
    result = ts.ic_media_diferencia_varianzas_distintas(
        xbar1=1470, s1=132, n1=4,
        xbar2=1208, s2=354, n2=16,
        alpha=0.10
    )

    assert result.a == pytest.approx(67.55, abs=1.0)
    assert result.b == pytest.approx(456.45, abs=1.0)
    assert result.error == pytest.approx(194.4494, abs=0.5)


# ---------------------------------------------------------------------------
# Apareadas (armado de circuitos, TEMA V problema 17)
# ---------------------------------------------------------------------------

def test_ensayo_media_apareada_circuitos():
    """Ensayo apareado: TEMA V problema 17 (armado de circuitos).

    Diferencias por trabajador: [8, 0, 7, -2, 7, 6, 7, 5]
    n=8 pares, α=0.05
    H0: δ ≤ 2, cola derecha
    Esperado: d̄=4.75, S_d≈3.6936, ν=7, d_c=4.4741, d̄ > d_c → se rechaza H0
    """
    differences = [8, 0, 7, -2, 7, 6, 7, 5]
    result = ts.ensayo_media_apareada(
        differences=differences,
        delta0=2.0, alpha=0.05, tail="derecha"
    )

    assert result.observed_value == pytest.approx(4.75, abs=0.001)
    assert result.critical_value == pytest.approx(4.4741, abs=0.01)
    assert result.df == 7
    assert result.rejects_h0


def test_ic_media_apareada_circuitos():
    """IC 90% para δ (apareado): TEMA V problema 17.

    Diferencias: [8, 0, 7, -2, 7, 6, 7, 5]
    Esperado: entre 2.27 y 7.23 (e≈2.4741)
    (Guía redondeó manualmente; usamos tolerancia abs=0.02 para el redondeo)
    """
    differences = [8, 0, 7, -2, 7, 6, 7, 5]
    result = ts.ic_media_apareada(
        differences=differences,
        alpha=0.10
    )

    assert result.a == pytest.approx(2.27, abs=0.02)
    assert result.b == pytest.approx(7.23, abs=0.02)


def test_n_media_apareada_circuitos():
    """Cálculo de n para reducir error a un tercio: TEMA V problema 17.

    S_d≈3.6936, e_actual≈2.4741, e_deseado=0.8247, α=0.10
    Esperado: n=57
    """
    result = ts.n_media_apareada_para_error(
        s_d=3.6936, e=0.8247, alpha=0.10
    )

    assert result.n == 57


# ---------------------------------------------------------------------------
# Validación de inputs (Fase 5 — Pulido)
# ---------------------------------------------------------------------------

def test_f_test_equal_variances_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        ts.f_test_equal_variances(0.9828, 12, 1.0064, 12, 1.5)


def test_ic_ratio_varianzas_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        ts.ic_ratio_varianzas(0.9828, 12, 1.0064, 12, 0.0)


def test_ic_media_diferencia_varianzas_iguales_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        ts.ic_media_diferencia_varianzas_iguales(
            10.25, 0.9828, 12, 7.083, 1.0064, 12, -0.05
        )


def test_ensayo_media_diferencia_varianzas_iguales_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        ts.ensayo_media_diferencia_varianzas_iguales(
            10.25, 0.9828, 12, 7.083, 1.0064, 12, 0, 2.0
        )


def test_n_media_diferencia_varianzas_iguales_para_error_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        ts.n_media_diferencia_varianzas_iguales_para_error(0.9828, 1.0064, 1.0, 1.1)


def test_ic_media_diferencia_varianzas_distintas_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        ts.ic_media_diferencia_varianzas_distintas(
            200, 20.5, 16, 60, 25.3, 4, 0.0
        )


def test_ensayo_media_diferencia_varianzas_distintas_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        ts.ensayo_media_diferencia_varianzas_distintas(
            200, 20.5, 16, 60, 25.3, 4, 100, 1.5
        )


def test_ic_media_apareada_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        ts.ic_media_apareada([1, 2, 3, 4, 5], -0.1)


def test_ensayo_media_apareada_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        ts.ensayo_media_apareada([1, 2, 3, 4, 5], 0, 1.0)


def test_n_media_apareada_para_error_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        ts.n_media_apareada_para_error(3.6936, 0.8247, 0.0)
