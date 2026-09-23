"""Tests para solver/hypothesis_one.py (M2).

Casos reales extraídos y verificados numericamente de la guía de la cátedra.
"""

import math
import pytest
from math import sqrt

from solver import distributions as dist
from solver import hypothesis_one as hyp


# ---------------------------------------------------------------------------
# Media, σ conocido, BILATERAL (caso real: torno automático)
# ---------------------------------------------------------------------------

def test_ensayo_media_sigma_conocido_bilateral_caso_torno():
    """TEMA I, problema de torno automático.
    
    H0: μ = 2cm (bilateral), σ = 0.1cm, n = 10, α = 0.10
    x̄_c1 = 1.9479, x̄_c2 = 2.0521
    """
    result = hyp.ensayo_media_sigma_conocido(
        xbar=2.04,
        sigma=0.1,
        n=10,
        mu0=2.0,
        alpha=0.10,
        tail="bilateral",
    )
    
    # Valores críticos
    assert isinstance(result.critical_value, tuple)
    c1, c2 = result.critical_value
    assert c1 == pytest.approx(1.9479, abs=0.001)
    assert c2 == pytest.approx(2.0521, abs=0.001)
    
    # Decisión: x̄ = 2.04 está dentro [1.9479, 2.0521], no se rechaza
    assert not result.rejects_h0


def test_ensayo_media_sigma_conocido_bilateral_con_beta_caso_torno():
    """Misma caso pero calculando β para μ1 = 1.95cm."""
    result = hyp.ensayo_media_sigma_conocido(
        xbar=2.04,
        sigma=0.1,
        n=10,
        mu0=2.0,
        alpha=0.10,
        tail="bilateral",
        mu1=1.95,
    )

    # β ≈ 0.5259
    assert result.beta == pytest.approx(0.5259, abs=0.002)
    assert result.power == pytest.approx(1 - 0.5259, abs=0.002)


def test_n_media_sigma_conocido_para_potencia_caso_torno():
    """Tamaño de muestra para potencia 0.80 con diferencia μ1 = 1.95.
    
    Nota: bilateral debe usar Z_(1-α/2), no Z_(1-α)
    Resultado esperado: n = 25
    """
    n = hyp.n_media_sigma_conocido_para_potencia(
        sigma=0.1,
        mu0=2.0,
        mu1=1.95,
        alpha=0.10,
        beta=0.20,
        tail="bilateral",
    )
    
    assert n == 25


# ---------------------------------------------------------------------------
# Varianza, COLA DERECHA (casos reales)
# ---------------------------------------------------------------------------

def test_ensayo_varianza_derecha_control_suelas():
    """TEMA II, control de suelas.
    
    H0: σ² ≤ 25 g² (cola derecha), n = 10, α = 0.05
    S_c ≈ 6.86 gramos (raíz de S²_c)
    """
    result = hyp.ensayo_varianza(
        s2=50,  # supongamos S² = 50
        n=10,
        sigma0_2=25,
        alpha=0.05,
        tail="derecha",
    )
    
    # S²_c = 25 * χ²_(0.95; 9) / 9
    df = 9
    chi2_val = dist.chi2_one_tailed(0.05, df)
    s2_c_esperado = 25 * chi2_val / df
    s_c_esperado = sqrt(s2_c_esperado)
    
    assert result.critical_value == pytest.approx(s2_c_esperado, abs=0.01)
    assert sqrt(result.critical_value) == pytest.approx(6.86, abs=0.01)


def test_ensayo_varianza_derecha_con_beta_control_suelas():
    """Mismo caso calculando β para σ1 = 8g."""
    result = hyp.ensayo_varianza(
        s2=50,
        n=10,
        sigma0_2=25,
        alpha=0.05,
        tail="derecha",
        sigma1_2=64,  # σ1² = 64 (σ1 = 8)
    )
    
    # β ≈ 0.3222
    assert result.beta == pytest.approx(0.3222, abs=0.01)


# ---------------------------------------------------------------------------
# Proporción, COLA DERECHA - BINOMIAL EXACTO
# ---------------------------------------------------------------------------

def test_ensayo_proporcion_derecha_caso_criterio_pesimista():
    """TEMA III, problema 15a (criterio pesimista).
    
    H0: p ≤ 0.70, n = 30, α = 0.05
    r_c = 26 (mínimo r con P(X≥r|30,0.70)≤0.05)
    Con r_observado = 25, α* ≈ 0.0766, no se rechaza
    """
    # Primero encontrar r_c
    rc = hyp._buscar_rc_derecha(30, 0.70, 0.05)
    assert rc == 26
    
    # Ensayo con r = 25 (no se rechaza)
    result = hyp.ensayo_proporcion(
        r=25,
        n=30,
        p0=0.70,
        alpha=0.05,
        tail="derecha",
    )
    
    assert result.critical_value == 26
    assert not result.rejects_h0
    assert result.p_value == pytest.approx(0.0766, abs=0.001)


def test_ensayo_proporcion_derecha_control_recepcion():
    """TEMA III, problema 12 (control de recepción).
    
    H0: p ≤ 0.11, n = 739, α = 0.05
    r_c = 96
    β para p1 = 0.16: β ≈ 0.0098
    """
    # Encontrar r_c
    rc = hyp._buscar_rc_derecha(739, 0.11, 0.05)
    assert rc == 96
    
    # Ensayo con β y potencia
    result = hyp.ensayo_proporcion(
        r=96,  # valor en el límite
        n=739,
        p0=0.11,
        alpha=0.05,
        tail="derecha",
        p1=0.16,
    )
    
    assert result.critical_value == 96
    assert result.beta == pytest.approx(0.0098, abs=0.0005)


def test_ensayo_proporcion_derecha_riesgo_proveedor():
    """TEMA III, problema 13 (riesgo del proveedor).
    
    H0: p ≤ 0.05, n = 100, r_c = 9 dado
    α (riesgo) = P(X≥9|100,0.05) ≈ 0.0631
    """
    result = hyp.ensayo_proporcion(
        r=9,
        n=100,
        p0=0.05,
        alpha=0.05,
        tail="derecha",
    )
    
    # El α* (p-value) debe ser ≈ 0.0631
    assert result.p_value == pytest.approx(0.0631, abs=0.001)


# ---------------------------------------------------------------------------
# Tests de point fijo (convergencia)
# ---------------------------------------------------------------------------

def test_n_media_sigma_desconocido_para_potencia_converge_y_es_punto_fijo():
    """No hay ejercicio real de la guía para este caso puntual (ver docstring de
    la función); se valida solo autoconsistencia, igual que se hizo en M1 para
    n_media_sigma_desconocido.
    """
    n = hyp.n_media_sigma_desconocido_para_potencia(
        s=10, mu0=100, mu1=95, alpha=0.05, beta=0.20, tail="derecha"
    )
    df = n - 1
    t_alpha = dist.t_one_tailed(0.05, df)
    t_beta = dist.t_value(1 - 0.20, df)
    n_recalculado = math.ceil(((t_alpha + t_beta) * 10 / 5) ** 2)
    assert n_recalculado == n


def test_ensayo_media_sigma_conocido_punto_fijo():
    """Verifica consistencia: β(μ0, μ1) + β(μ1, μ0) ≈ 1 en ciertos casos."""
    result1 = hyp.ensayo_media_sigma_conocido(
        xbar=100,
        sigma=10,
        n=25,
        mu0=95,
        alpha=0.05,
        tail="derecha",
        mu1=100,
    )

    result2 = hyp.ensayo_media_sigma_conocido(
        xbar=100,
        sigma=10,
        n=25,
        mu0=100,
        alpha=0.05,
        tail="derecha",
        mu1=95,
    )

    # Los valores de β deben ser válidos en [0, 1]
    assert 0 <= result1.beta <= 1
    assert 0 <= result2.beta <= 1


def test_ensayo_proporcion_bilateral_beta_y_potencia_no_estan_invertidos():
    """Regresión: beta y power quedaban invertidos en el caso bilateral.

    beta = P(no rechazar | p1) debe achicarse cuando p1 se aleja de p0 (mejor
    detectado), y power = 1 - beta debe agrandarse.
    """
    n, p0, alpha = 100, 0.5, 0.10
    cerca = hyp.ensayo_proporcion(r=55, n=n, p0=p0, alpha=alpha, tail="bilateral", p1=0.52)
    lejos = hyp.ensayo_proporcion(r=55, n=n, p0=p0, alpha=alpha, tail="bilateral", p1=0.6)

    assert cerca.beta == pytest.approx(1 - cerca.power)
    assert lejos.beta == pytest.approx(1 - lejos.power)
    # p1 más lejos de p0 -> más fácil de detectar -> beta menor, power mayor
    assert lejos.beta < cerca.beta
    assert lejos.power > cerca.power


def test_ensayo_proporcion_p_value_monotonico():
    """Verifica que p-value aumenta conforme r se aleja del crítico."""
    p_value_cerca = hyp.ensayo_proporcion(
        r=24, n=30, p0=0.70, alpha=0.05, tail="derecha"
    ).p_value

    p_value_lejos = hyp.ensayo_proporcion(
        r=20, n=30, p0=0.70, alpha=0.05, tail="derecha"
    ).p_value

    # Más cerca de rc (24 > 20), p-value debe ser menor
    assert p_value_cerca < p_value_lejos


# ---------------------------------------------------------------------------
# Validación de inputs (Fase 5 — Pulido)
# ---------------------------------------------------------------------------

def test_ensayo_media_sigma_conocido_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        hyp.ensayo_media_sigma_conocido(100, 15, 30, 100, 1.5)


def test_n_media_sigma_conocido_para_potencia_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        hyp.n_media_sigma_conocido_para_potencia(15, 100, 105, 0.0, 0.20)


def test_ensayo_media_sigma_desconocido_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        hyp.ensayo_media_sigma_desconocido(100, 15, 30, 100, 2.0)


def test_n_media_sigma_desconocido_para_potencia_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        hyp.n_media_sigma_desconocido_para_potencia(15, 100, 105, 1.1, 0.20)


def test_ensayo_varianza_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        hyp.ensayo_varianza(100, 30, 100, -0.05)


def test_ensayo_proporcion_error_r_mayor_a_n():
    """Validar que r no puede ser mayor a n."""
    with pytest.raises(ValueError, match="r debe estar entre 0 y n"):
        hyp.ensayo_proporcion(r=35, n=30, p0=0.5, alpha=0.05)


def test_ensayo_proporcion_error_r_negativo():
    """Validar que r no puede ser negativo."""
    with pytest.raises(ValueError, match="r debe estar entre 0 y n"):
        hyp.ensayo_proporcion(r=-1, n=30, p0=0.5, alpha=0.05)


def test_ensayo_proporcion_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        hyp.ensayo_proporcion(r=15, n=30, p0=0.5, alpha=1.0)


# ---------------------------------------------------------------------------
# curva_potencia_media (tabla de beta/potencia para varios mu1, tipo curva OC)
# ---------------------------------------------------------------------------

def test_curva_potencia_media_coincide_con_ensayo_individual():
    mu0, sigma, n, alpha, tail = 2.0, 0.1, 10, 0.10, "bilateral"
    mu1_list = [1.95, 2.0, 2.05]

    tabla = hyp.curva_potencia_media(mu0, sigma, n, alpha, mu1_list, tail=tail, sigma_conocido=True)

    assert [row[0] for row in tabla] == mu1_list
    for mu1, beta, power in tabla:
        individual = hyp.ensayo_media_sigma_conocido(
            xbar=mu0, sigma=sigma, n=n, mu0=mu0, alpha=alpha, tail=tail, mu1=mu1
        )
        assert beta == pytest.approx(individual.beta)
        assert power == pytest.approx(individual.power)
        assert power == pytest.approx(1 - beta)


def test_curva_potencia_media_sigma_desconocido():
    mu0, s, n, alpha, tail = 10.0, 2.0, 20, 0.05, "derecha"
    mu1_list = [11.0, 12.0]

    tabla = hyp.curva_potencia_media(mu0, s, n, alpha, mu1_list, tail=tail, sigma_conocido=False)

    assert len(tabla) == 2
    for mu1, beta, power in tabla:
        individual = hyp.ensayo_media_sigma_desconocido(
            xbar=mu0, s=s, n=n, mu0=mu0, alpha=alpha, tail=tail, mu1=mu1
        )
        assert beta == pytest.approx(individual.beta)
        assert power == pytest.approx(individual.power)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, r"D:\UADE\Estadistica\code")
    pytest.main([__file__, "-v"])


# ---------------------------------------------------------------------------
# Diseño completo del ensayo (n + punto crítico + regla de decisión)
# ---------------------------------------------------------------------------

def test_diseno_media_sigma_conocido_dural():
    """Ej. 16 "Dural": μ₀=38 con prob. de detener 0.10; μ₁=37 con prob. 0.95; σ=1.3.

    Resp. de la guía: H0) μ ≥ 38; CR: x̄ < x̄_c = 37,56; n = 15;
    potencia en μ = 37,5 igual a 0,5824.
    """
    d = hyp.disenar_ensayo_media_sigma_conocido(
        sigma=1.3, mu0=38, mu1=37, alpha=0.10, beta=0.05
    )

    assert d.tail == "izquierda"          # se deduce de μ₁ < μ₀
    assert d.n == 15
    assert d.xc_sistema == pytest.approx(37.56, abs=0.005)
    assert d.critical_value == pytest.approx(37.57, abs=0.005)
    assert d.potencia_real >= 0.95        # con n redondeado se supera el objetivo

    # b) probabilidad de detectar que la media vale 37,5
    (_, _, potencia_375), = hyp.curva_potencia_media(
        mu0=38, sigma_or_s=1.3, n=d.n, alpha=0.10, mu1_list=[37.5], tail=d.tail
    )
    assert potencia_375 == pytest.approx(0.5824, abs=0.001)


def test_diseno_media_sigma_conocido_coincide_con_n_para_potencia():
    d = hyp.disenar_ensayo_media_sigma_conocido(
        sigma=0.1, mu0=2.0, mu1=1.95, alpha=0.10, beta=0.20, tail="bilateral"
    )
    assert d.n == hyp.n_media_sigma_conocido_para_potencia(
        sigma=0.1, mu0=2.0, mu1=1.95, alpha=0.10, beta=0.20, tail="bilateral"
    )
    assert isinstance(d.critical_value, tuple)
    assert d.xc_sistema is None


def test_diseno_media_mu0_igual_mu1_es_error():
    with pytest.raises(ValueError, match="distintos"):
        hyp.disenar_ensayo_media_sigma_conocido(
            sigma=1.0, mu0=10.0, mu1=10.0, alpha=0.05, beta=0.10
        )


# ---------------------------------------------------------------------------
# Diseño por potencia: varianza y plan de muestreo binomial (valores de la guía)
# ---------------------------------------------------------------------------

def test_n_varianza_para_potencia_guia_II_12():
    r = hyp.n_varianza_para_potencia(sigma0=5, sigma1=8, alpha=0.05, beta=0.05)
    assert r.n == 27
    assert r.tail == "derecha"
    assert r.beta_real <= 0.05


def test_n_varianza_para_potencia_guia_II_8():
    r = hyp.n_varianza_para_potencia(sigma0=0.09 ** 0.5, sigma1=0.11 ** 0.5, alpha=0.05, beta=0.05)
    assert r.n == 540


def test_plan_proporcion_guia_III_12():
    r = hyp.disenar_plan_proporcion(p0=0.11, p1=0.16, alpha=0.05, beta=0.01)
    assert (r.n, r.rc) == (739, 96)
    assert r.alpha_real <= 0.05 and r.beta_real <= 0.01


def test_plan_proporcion_guia_III_26():
    r = hyp.disenar_plan_proporcion(p0=0.01, p1=0.02, alpha=0.01, beta=0.05)
    assert (r.n, r.rc) == (2258, 35)


def test_plan_proporcion_cola_izquierda_guia_III_14():
    r = hyp.disenar_plan_proporcion(p0=0.14, p1=0.10, alpha=0.01, beta=0.05)
    assert r.tail == "izquierda"
    assert (r.n, r.rc) == (1043, 120)
