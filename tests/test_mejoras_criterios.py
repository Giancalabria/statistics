"""Criterios de la cátedra y casos que antes no se resolvían (con redacciones distintas a la guía)."""

import pytest

from interprete.analizador import analizar
from interprete.resolver import resolver
from solver import hypothesis_one as hyp


def _res(planteo, incisos=None, tablas=None):
    an = analizar(planteo, incisos, tablas=tablas)
    return an, resolver(an)


# ---------------------------------------------------------------- planes de muestreo

def test_rango_de_planes_validos():
    planes = hyp.planes_factibles(0.02, 0.05, 0.15, 0.10)
    assert planes[0] == (7, 209, 218)          # la guía da 218: cualquier n del rango cumple
    assert hyp.planes_factibles(0.06, 0.04, 0.01, 0.10)[1] == (73, 1580, 1585)


def test_poisson_con_tabla_como_la_guia():
    assert hyp.n_plan_dado_poisson(0.01, 2, 0.95) == (30, 0.3)           # III-21 a
    assert hyp.plan_poisson_tabla(0.041, 5, 0.10, "izquierda") == (227, 9.3)  # III-17


def test_plan_dado_con_otra_redaccion():
    an, res = _res("Un lote se rechaza si en la muestra aparecen dos o más piezas falladas.",
                   ["¿Qué tamaño de muestra hace que un lote con 1% de falladas se acepte con probabilidad mayor a 0,95?",
                    "Con ese plan, ¿qué probabilidad hay de aceptar un lote con 11% de falladas?"])
    assert any(abs(v - 30) < 1e-9 for v in res[0].numeros)       # Poisson con tabla
    assert any(abs(v - 0.1586) < 1e-3 for v in res[1].numeros)


# ---------------------------------------------------------------- comparación: unilateral en el sentido de los datos

def test_comparacion_difieren_unilateral_sin_bilateral():
    an, res = _res("Se midió el rendimiento de dos máquinas. Máquina A: muestra de 15 piezas, media 20,4, desvío 1,1. "
                   "Máquina B: muestra de 15 piezas, media 19,6, desvío 1,2.",
                   ["¿Difieren los rendimientos medios? Riesgo 5%."])
    inc = an.incisos[0]
    assert inc.params["tail"] == "derecha" and inc.params["bilateral_pregunta"]
    # el profesor: «jamás me planteen una hipótesis bilateral en comparación» → ya no hay referencia bilateral
    assert not any("bilateral" in p and "Referencia" in p for p in res[0].pasos)
    assert any(p.startswith("**Orientación**") for p in res[0].pasos)


def test_beta_dos_medias():
    an, res = _res("Línea vieja: 30 piezas con media 12 y desvío 2. Línea nueva: 30 piezas con media 13 y desvío 2.",
                   ["¿Se puede asegurar con 5% de riesgo que la línea nueva produce piezas más largas?",
                    "¿Qué probabilidad hay de no detectar una diferencia real de 1,5?"])
    assert an.incisos[1].tipo == "beta" and an.incisos[1].params["delta1"] == 1.5
    # con desvíos desconocidos (t) la cátedra no calcula β (t no central): se avisa en lugar de inventarlo
    assert res[1].resumen == "fuera de la cátedra" and "t no central" in res[1].errores[0]


# ---------------------------------------------------------------- límites de control con medias por período

def test_medias_por_periodo_contra_limites():
    an, res = _res("Cada día se toman 4 botellas y se registra el contenido promedio. Los promedios de 6 días fueron: "
                   "Día: 1 - 2 - 3 - 4 - 5 - 6; Media: 500 - 498 - 507 - 501 - 499 - 492.",
                   ["Con un contenido nominal de 500 cm³ y σ = 6 cm³, hallar los límites de control con 5% de riesgo. "
                    "¿Hubo días fuera de control?",
                    "¿Cuál es la probabilidad de obtener una media diaria de 515 cm³?"])
    assert an.datos.get("medias_periodo")
    assert "fuera de control" in res[0].resumen
    assert "P(x̄ ≥ 515" in res[1].resumen


# ---------------------------------------------------------------- χ² con incisos de otro tema

def test_chi_con_comparacion_y_proporcion_desde_la_tabla():
    tabla = {"columnas": ["Duración (miles de h)", "Marca A", "Marca B"],
             "filas": [["10-12", 2, None], ["12-14", 6, 8], ["14-16", 13, 18], ["16-18", 18, 32], ["18-20", 30, 57],
                       ["20-22", 22, 39], ["22-24", 16, 26], ["24-26", 5, 13], ["26-28", 1, 10]]}
    an, res = _res("Ensayos de vida de dos marcas de equipos.",
                   ["¿Cuál marca conviene elegir?",
                    "¿Sigue la marca A un modelo normal? (5% de riesgo)",
                    "Si se exige una duración mínima de 14.000 hs, estimar con 95% de confianza el porcentaje de equipos "
                    "de la marca B que no la cumplen."], tablas=[tabla])
    a, b, c = an.incisos
    assert a.params["tema"] == "dos_medias" and a.tipo == "ensayo"
    assert b.tipo == "ensayo" and "normal" in b.params["modelos"]
    assert c.params["tema"] == "proporcion" and c.params["r"] == 8 and c.params["n"] == 203
    assert "cota" not in c.params
    assert res[2].numeros[0] == pytest.approx(0.0171, abs=2e-4)
