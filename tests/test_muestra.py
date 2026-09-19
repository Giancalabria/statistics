"""Tests para solver/muestra.py (resumen de datos crudos)."""

import math

import pytest

from solver import muestra


def test_resumen_muestra_calcula_n_xbar_s():
    datos = [10.0, 12.0, 11.0, 13.0, 9.0]
    result = muestra.resumen_muestra(datos)

    n_esperado = len(datos)
    xbar_esperado = sum(datos) / n_esperado
    s2_esperado = sum((x - xbar_esperado) ** 2 for x in datos) / (n_esperado - 1)

    assert result.n == n_esperado
    assert result.xbar == pytest.approx(xbar_esperado)
    assert result.s == pytest.approx(math.sqrt(s2_esperado))


def test_resumen_muestra_error_con_menos_de_2_datos():
    with pytest.raises(ValueError, match="al menos 2 datos"):
        muestra.resumen_muestra([5.0])
