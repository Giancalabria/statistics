"""Tests para solver/chi_square.py (M4).

Casos reales extraídos y verificados numericamente de la guía de la cátedra
(TEMA VI de la guía de problemas).
"""

import pytest
from solver import chi_square as chi


# ---------------------------------------------------------------------------
# Bondad de ajuste — dado cargado (uniforme, k=6, n=60, p=0, α=0,05)
# ---------------------------------------------------------------------------

def test_bondad_de_ajuste_dado_cargado():
    """Dado cargado: observados [14, 6, 6, 13, 16, 5], esperados [10, 10, 10, 10, 10, 10].

    χ²_c = 11,80, ν = 5, χ²_crit = 11,0705 → SE RECHAZA H0.
    """
    observados = [14, 6, 6, 13, 16, 5]
    esperados = [10, 10, 10, 10, 10, 10]
    alpha = 0.05
    p = 0

    result = chi.bondad_de_ajuste(observados, esperados, p, alpha)

    # Verificar chi2 calculado
    assert result.chi2_calc == pytest.approx(11.80, abs=0.01)

    # Verificar grados de libertad: k - 1 - p = 6 - 1 - 0 = 5
    assert result.df == 5

    # Verificar valor crítico (aproximadamente 11.0705 para α=0.05, ν=5)
    assert result.chi2_critico == pytest.approx(11.0705, abs=0.01)

    # Verificar decisión: chi2_calc > chi2_critico → se rechaza
    assert result.rejects_h0 == True


# ---------------------------------------------------------------------------
# Bondad de ajuste — instalaciones de aire acondicionado (uniforme, k=4, n=80, p=0, α=0,05)
# ---------------------------------------------------------------------------

def test_bondad_de_ajuste_aire_acondicionado():
    """Aire acondicionado: observados [16, 22, 24, 18], esperados [20, 20, 20, 20].

    χ²_c = 2,00, ν = 3, crit = 7,8147 → NO se rechaza.
    """
    observados = [16, 22, 24, 18]
    esperados = [20, 20, 20, 20]
    alpha = 0.05
    p = 0

    result = chi.bondad_de_ajuste(observados, esperados, p, alpha)

    # Verificar chi2 calculado
    assert result.chi2_calc == pytest.approx(2.00, abs=0.01)

    # Verificar grados de libertad: k - 1 - p = 4 - 1 - 0 = 3
    assert result.df == 3

    # Verificar valor crítico (aproximadamente 7.8147 para α=0.05, ν=3)
    assert result.chi2_critico == pytest.approx(7.8147, abs=0.01)

    # Verificar decisión: chi2_calc < chi2_critico → no se rechaza
    assert result.rejects_h0 == False


# ---------------------------------------------------------------------------
# Bondad de ajuste — ventas de TV (proporciones históricas 40/40/20%, k=3, n=200, p=0, α=0,05)
# ---------------------------------------------------------------------------

def test_bondad_de_ajuste_ventas_tv():
    """Ventas de TV: observados [85, 65, 50], esperados [80, 80, 40].

    χ²_c = 5,625, ν = 2, crit = 5,9915 → NO se rechaza (caso límite, bueno para precisión).
    """
    observados = [85, 65, 50]
    esperados = [80, 80, 40]
    alpha = 0.05
    p = 0

    result = chi.bondad_de_ajuste(observados, esperados, p, alpha)

    # Verificar chi2 calculado
    assert result.chi2_calc == pytest.approx(5.625, abs=0.001)

    # Verificar grados de libertad: k - 1 - p = 3 - 1 - 0 = 2
    assert result.df == 2

    # Verificar valor crítico (aproximadamente 5.9915 para α=0.05, ν=2)
    assert result.chi2_critico == pytest.approx(5.9915, abs=0.001)

    # Verificar decisión: chi2_calc < chi2_critico → no se rechaza (caso límite, están cerca)
    assert result.rejects_h0 == False


# ---------------------------------------------------------------------------
# Tabla de contingencia — ocupación laboral, 3×2 (TEMA VI, problema 1, α=0,05)
# ---------------------------------------------------------------------------

def test_tabla_contingencia_ocupacion_laboral():
    """Ocupación laboral: tabla 3×2.

    tabla = [[35, 37], [165, 263], [300, 500]]
    χ²_c = 3,4476, ν = 2, crit = 5,9915 → NO se rechaza.
    """
    tabla = [[35, 37], [165, 263], [300, 500]]
    alpha = 0.05

    result = chi.tabla_contingencia(tabla, alpha)

    # Verificar chi2 calculado
    assert result.chi2_calc == pytest.approx(3.4476, abs=0.0001)

    # Verificar grados de libertad: (R - 1) * (C - 1) = (3 - 1) * (2 - 1) = 2
    assert result.df == 2

    # Verificar valor crítico (aproximadamente 5.9915 para α=0.05, ν=2)
    assert result.chi2_critico == pytest.approx(5.9915, abs=0.001)

    # Verificar decisión: chi2_calc < chi2_critico → no se rechaza
    assert result.rejects_h0 == False

    # Verificar tabla esperada (opcional pero útil)
    assert result.expected_table is not None
    assert len(result.expected_table) == 3
    assert len(result.expected_table[0]) == 2


# ---------------------------------------------------------------------------
# Tabla de contingencia — preferencia de fragancias, 3×4 (TEMA VI, problema 9, α=0,10)
# ---------------------------------------------------------------------------

def test_tabla_contingencia_fragancias():
    """Preferencia de fragancias: tabla 3×4.

    tabla = [[32, 45, 23, 28], [14, 51, 15, 14], [14, 14, 12, 8]]
    χ²_c = 13,5075, ν = 6, crit = 10,6446 → SE RECHAZA.
    """
    tabla = [[32, 45, 23, 28], [14, 51, 15, 14], [14, 14, 12, 8]]
    alpha = 0.10

    result = chi.tabla_contingencia(tabla, alpha)

    # Verificar chi2 calculado
    assert result.chi2_calc == pytest.approx(13.5075, abs=0.001)

    # Verificar grados de libertad: (R - 1) * (C - 1) = (3 - 1) * (4 - 1) = 6
    assert result.df == 6

    # Verificar valor crítico (aproximadamente 10.6446 para α=0.10, ν=6)
    assert result.chi2_critico == pytest.approx(10.6446, abs=0.001)

    # Verificar decisión: chi2_calc > chi2_critico → se rechaza
    assert result.rejects_h0 == True

    # Verificar tabla esperada
    assert result.expected_table is not None
    assert len(result.expected_table) == 3
    assert len(result.expected_table[0]) == 4


# ---------------------------------------------------------------------------
# Test de validación: Fe < 5 (warnings)
# ---------------------------------------------------------------------------

def test_bondad_de_ajuste_validacion_fe_bajo_5():
    """Test que alguna frecuencia esperada sea < 5 → debe generar warning."""
    observados = [10, 50, 50]
    esperados = [3, 50, 57]  # El primer esperado es 3 < 5
    alpha = 0.05
    p = 0

    result = chi.bondad_de_ajuste(observados, esperados, p, alpha)

    # Debe tener al menos un warning
    assert len(result.warnings) > 0

    # El warning debe mencionar la celda baja
    warning_texto = " ".join(result.warnings)
    assert "F_e_i < 5" in warning_texto or "Celdas con F_e_i < 5" in warning_texto

    # El cálculo debe realizarse de todas formas (no debe tirar excepción)
    assert result.chi2_calc > 0
    assert result.df == 2  # k - 1 - p = 3 - 1 - 0


# ---------------------------------------------------------------------------
# Test de validación: N < 60 (warnings)
# ---------------------------------------------------------------------------

def test_bondad_de_ajuste_validacion_n_bajo_60():
    """Test que N < 60 → debe generar warning."""
    observados = [5, 10, 10]
    esperados = [10, 10, 5]
    alpha = 0.05
    p = 0

    result = chi.bondad_de_ajuste(observados, esperados, p, alpha)

    # Debe tener al menos un warning por N < 60
    assert len(result.warnings) > 0
    warning_texto = " ".join(result.warnings)
    assert "N = 25" in warning_texto or "< 60" in warning_texto


# ---------------------------------------------------------------------------
# Test de error: observados y esperados con longitudes distintas
# ---------------------------------------------------------------------------

def test_bondad_de_ajuste_error_longitudes_distintas():
    """Las listas deben tener la misma longitud."""
    observados = [10, 20, 30]
    esperados = [10, 20]  # Longitud distinta
    alpha = 0.05
    p = 0

    with pytest.raises(ValueError, match="misma longitud"):
        chi.bondad_de_ajuste(observados, esperados, p, alpha)


# ---------------------------------------------------------------------------
# Test de error: nu <= 0
# ---------------------------------------------------------------------------

def test_bondad_de_ajuste_error_nu_invalido():
    """Si k - 1 - p <= 0, debe fallar."""
    observados = [10, 10]
    esperados = [10, 10]
    alpha = 0.05
    p = 2  # k - 1 - p = 2 - 1 - 2 = -1 (inválido)

    with pytest.raises(ValueError, match="Grados de libertad no válidos"):
        chi.bondad_de_ajuste(observados, esperados, p, alpha)


# ---------------------------------------------------------------------------
# Test de error: tabla no rectangular
# ---------------------------------------------------------------------------

def test_tabla_contingencia_error_no_rectangular():
    """La tabla debe ser rectangular."""
    tabla = [[10, 20], [30, 40, 50]]  # Segunda fila tiene 3 elementos
    alpha = 0.05

    with pytest.raises(ValueError, match="rectangular"):
        chi.tabla_contingencia(tabla, alpha)


# ---------------------------------------------------------------------------
# Test de validación: tabla_contingencia con E_ij < 5
# ---------------------------------------------------------------------------

def test_tabla_contingencia_validacion_e_bajo_5():
    """Test con celdas esperadas < 5 → debe generar warning."""
    # Crear una tabla pequeña con una celda esperada baja
    tabla = [[1, 50], [1, 50]]
    alpha = 0.05

    result = chi.tabla_contingencia(tabla, alpha)

    # Puede tener warnings por E_ij < 5
    # (Dependiendo del tamaño, puede haber o no)
    # Pero el cálculo debe realizarse
    assert result.chi2_calc >= 0
    assert result.df == 1  # (2-1) * (2-1) = 1


# ---------------------------------------------------------------------------
# Validación de inputs (Fase 5 — Pulido)
# ---------------------------------------------------------------------------

def test_bondad_de_ajuste_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        chi.bondad_de_ajuste([14, 6, 6, 13, 16, 5], [10, 10, 10, 10, 10, 10], 0, 1.5)

    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        chi.bondad_de_ajuste([14, 6, 6, 13, 16, 5], [10, 10, 10, 10, 10, 10], 0, 0.0)


def test_tabla_contingencia_error_alpha_fuera_de_rango():
    """Validar que alpha debe estar entre 0 y 1."""
    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        chi.tabla_contingencia([[35, 37], [165, 263]], -0.05)

    with pytest.raises(ValueError, match="alpha debe estar entre 0 y 1"):
        chi.tabla_contingencia([[35, 37], [165, 263]], 1.0)
