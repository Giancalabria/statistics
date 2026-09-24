"""Tests para solver/wording.py."""

from solver import intervals
from solver import wording


def test_texto_tamano_muestra_sin_preliminar_no_menciona_delta():
    n_result = intervals.SampleSizeResult(n=50)
    texto = wording.texto_tamano_muestra(n_result)
    assert "n = 50" in texto
    assert "adicionales" not in texto


def test_texto_tamano_muestra_con_preliminar_calcula_delta():
    n_result = intervals.SampleSizeResult(n=50)
    texto = wording.texto_tamano_muestra(n_result, n_preliminar=20)
    assert "Δn = 50 - 20 = 30" in texto


def test_texto_tamano_muestra_preliminar_mayor_a_n_da_delta_cero():
    n_result = intervals.SampleSizeResult(n=50)
    texto = wording.texto_tamano_muestra(n_result, n_preliminar=80)
    assert "Δn = 50 - 80 = 0" in texto


def test_conclusion_formal_no_rechazo_nunca_acepta_h0():
    texto = wording.conclusion_formal(0.05, False, "H0: μ ≤ 100", "μ > 100", "x̄ = 101")
    assert texto.startswith("A un nivel de significación del 5%, no existe evidencia")
    assert "no se puede afirmar que μ > 100" in texto and "se acepta" not in texto


def test_conclusion_formal_con_accion():
    texto = wording.conclusion_formal(0.1, True, "H0: μ ≥ 3", "μ < 3", "x̄ = 2", si_rechaza="se detiene el proceso")
    assert texto.endswith("Por consiguiente, se detiene el proceso.")
