"""Clase del 05/11/2026 (validación de regresión, VII-13 resuelto en clase) y presentación como el profesor."""

import json
from pathlib import Path

from interprete.analizador import analizar, separar_incisos
from interprete.editor import a_texto, de_texto
from interprete.regresion import nombre_unidad
from interprete.resolver import resolver

GUIA = {e["id"]: e for e in json.loads((Path(__file__).parent.parent / "datos" / "guia_ejercicios.json")
                                        .read_text(encoding="utf8"))}


def _resolver(id_, incisos=None, tema=None):
    ej = GUIA[id_]
    inc = incisos or [(i["letra"], i["texto"]) for i in ej["incisos"]]
    an = analizar(ej["planteo"], inc, tablas=ej.get("tablas") or None, tema=tema)
    return an, resolver(an)


def test_negativos_del_editor_conservan_el_signo():
    # el ensayo de β1 de VII-13 tiene β1₀ = -0,25: al pasar por la pantalla no puede volverse +0,25
    assert de_texto(a_texto(-0.25, "float"), "float") == -0.25
    assert de_texto("−3,5", "float") == -3.5
    assert de_texto("3 ; -2,5 ; 4", "lista") == [3.0, -2.5, 4.0]
    assert de_texto("-1 ; 2\n3 ; -4", "tabla") == [[-1.0, 2.0], [3.0, -4.0]]
    assert de_texto("10-20", "lista") == [10.0, 20.0]


def test_nombre_y_unidad_del_encabezado():
    assert nombre_unidad("X = Carbonatación (en mm)") == ("carbonatación", "mm")
    assert nombre_unidad("Y = Resistencia al quiebre (en MPa)") == ("resistencia al quiebre", "MPa")
    assert nombre_unidad("PBI (millones de U$s)") == ("PBI", "millones de U$s")


def test_vii13_como_en_el_pizarron():
    _, res = _resolver("VII-13")
    a, b, c, d, e, f, g = res
    texto_a = " ".join(a.pasos)
    # procesamiento, validación (|t_obs| = 8,0879 vs t(0,95;16) = 1,7459) y r² para uso técnico
    assert "x̄ = Σx/n = 659/18 = 36,611111" in texto_a and "Sb1 = S/√(Σx² - n·x̄²) = " in texto_a
    assert "= 0,03632" in texto_a
    assert "|t_obs|" in texto_a and "8,0879" in texto_a and "1,7459" in texto_a
    # interpretación en términos del problema, con unidades, y β0 solo «en teoría» (entorno 8 a 65 mm)
    assert "por cada mm adicional de carbonatación, la resistencia al quiebre disminuye en promedio 0,2938 MPa" in a.conclusion
    assert "entre 8 y 65 mm" in a.conclusion and "no se estima β0" in a.conclusion
    assert "80,35%" in a.conclusion
    # límites hacia afuera, como los escribió el profesor: ρ² ≤ 0,9237; β1 entre -0,3708 y -0,2167 MPa/mm
    assert "P(0,5455 ≤ ρ² ≤ 0,9237)" in c.conclusion
    assert "P(-0,3708 ≤ β1 ≤ -0,2167)" in e.conclusion and "MPa/mm" in e.conclusion
    # ensayo: b1c = -0,3134; no se puede asegurar que disminuya en más de 0,25 MPa
    assert "-0,3134" in " ".join(d.pasos)
    assert "no hay evidencia suficiente para asegurar que" in d.conclusion
    assert "disminuye en más de 0,25 MPa" in d.conclusion
    # promedio y predicción para 10 mm, con unidades
    assert "21,4769 MPa y 26,2905 MPa" in f.conclusion and "E(y | x₀ = 10)" in f.conclusion
    assert "18,0109 MPa y 29,7565 MPa" in g.conclusion


def test_vii13_pegado_entero_y_separado():
    """El camino de la pantalla: enunciado pegado, «Separar incisos», resolver."""
    plant, incs = separar_incisos(GUIA["VII-13"]["enunciado"], parrafos=True)
    res = resolver(analizar(plant, [tx for _, tx in incs]))
    assert "no se rechaza H0" in res[3].conclusion


def test_se_valida_aunque_no_lo_pidan():
    # solo el pronóstico: igual se valida el modelo antes de usarlo
    _, res = _resolver("VII-13", [("a", "Si la penetración fuese de 10 mm, hallar un intervalo de confianza del 95% "
                                         "para la resistencia al quiebre promedio.")], tema="regresion")
    pasos = " ".join(res[0].pasos)
    assert "Primero se valida el modelo" in pasos and "|t_obs|" in pasos


def test_extrapolar_avisa():
    _, res = _resolver("VII-13", [("a", "Hallar un intervalo de confianza del 95% para la resistencia al quiebre "
                                         "promedio, si la penetración fuese de 80 mm.")], tema="regresion")
    assert any("FUERA del entorno observado" in x for x in res[0].avisos)


def test_variable_en_porcentaje_es_punto_porcentual():
    _, res = _resolver("VII-9")
    assert "por cada punto porcentual adicional de la tasa de interés" in res[0].conclusion


def test_paso_variable_y_unidad_en_la_conclusion():
    an, res = _resolver("I-1")
    assert an.datos.get("unidad") == "gramos"
    assert res[0].pasos[0].startswith("**Variable** (paso 1)")
    assert "entre 238,19 gramos y 253,81 gramos" in res[0].conclusion
    assert "P(238,19 ≤ μ ≤ 253,81)" in res[0].conclusion        # la expresión formal, sin unidades
    assert not res[1].pasos[0].startswith("**Variable**")        # una sola vez por problema
    # con la variable escrita, la conclusión la nombra
    an.datos["variable"] = "peso de un paquete"
    assert "la media poblacional de peso de un paquete" in resolver(an)[0].conclusion
