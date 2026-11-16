"""Reglas generales que salieron de la 2ª tanda de ejercicios nuevos (datos/ejercicios_nuevos_2.json, 16/11/2026).

Cada test usa el enunciado de la tanda tal cual; lo que se controla es la regla, no el ejercicio."""

import json
from pathlib import Path

import pytest

from asistente import revisar as rev
from interprete.analizador import analizar
from interprete.resolver import resolver

TANDA = {e["id"]: e for e in json.loads((Path(__file__).resolve().parent.parent / "datos" /
                                         "ejercicios_nuevos_2.json").read_text(encoding="utf-8"))}


def _resolver(ident):
    e = TANDA[ident]
    an = analizar(e["planteo"], [tuple(i) for i in e["incisos"]], tablas=e["tablas"])
    return an, resolver(an)


def test_con_r_y_n_un_porcentaje_que_no_es_r_sobre_n_es_el_de_referencia():
    an, res = _resolver("S1")             # 'sostiene que, como mucho, el 8%' … 'revisó 200 y encontró 23'
    assert an.datos["p0"] == pytest.approx(0.08) and "p_hat" not in an.datos
    assert "H0: p ≤ 0.08" in res[0].resumen and "rc = 24" in res[0].resumen


def test_plan_sobre_p_hacia_abajo_la_cola_sale_de_p1_menor_que_p0():
    an, res = _resolver("S2")             # 'el porcentaje sigue en el 20%' es p₀, no una probabilidad
    assert an.datos["beta"] == pytest.approx(0.10) and an.datos["alpha"] == pytest.approx(0.05)
    assert an.incisos[0].params["tail"] == "izquierda"
    assert "n = 112; rc = 15" in res[0].resumen
    assert "β = 0,624" in res[1].resumen


def test_al_uno_por_ciento_suelto_es_el_alfa():
    an, res = _resolver("S3")             # 'Al 1%, ¿tiene razón…?'
    assert an.incisos[0].params["alpha"] == pytest.approx(0.01)
    assert "Jc = 2,3691" in res[0].resumen                              # √F(0,99; 7; 9)


def test_tamano_de_muestra_lejos_del_promedio_sin_otro_numero_en_el_medio():
    an, res = _resolver("S4")             # 'En 12 turnos con la línea actual se envasaron en promedio 184'
    assert {an.datos["n1"], an.datos["n2"]} == {12, 15}
    assert "≤ 5" in res[0].resumen and "RECHAZA" in res[0].resumen


def test_tabla_de_dos_columnas_de_la_misma_variable_es_comparacion_apareada():
    an, res = _resolver("S5")
    assert an.tema == "dos_medias" and an.datos["apareadas"] is True
    assert res[1].resumen == "IC δ: [0,9770 ; 2,3630]"                  # mismo orden que el ensayo: el aumento


def test_la_pregunta_por_un_modelo_de_distribucion_es_bondad_de_ajuste():
    an, res = _resolver("S6")             # '¿… tiene distribución normal?'
    assert an.tema == "chi_ajuste" and "5,5397" in res[0].resumen


def test_tabla_de_conteos_y_porcentajes_iguales_entre_grupos_es_contingencia():
    an, res = _resolver("S7")             # '¿… los porcentajes … son los mismos en las tres sucursales?'
    assert an.tema == "chi_contingencia" and "22,1936" in res[0].resumen


def test_porcentajes_que_suman_cien_y_sus_conteos_son_un_ajuste_a_proporciones_dadas():
    an, res = _resolver("S8")
    assert an.tema == "chi_ajuste" and "7,8533" in res[0].resumen and "RECHAZA" in res[0].resumen


def test_estimar_la_recta_es_ajustar_el_modelo():
    an, res = _resolver("S9")
    assert an.incisos[0].tipo == "recta" and "0,0884" in res[0].resumen


def test_reduccion_porcentual_minima_sale_del_h_maximo():
    an, res = _resolver("S10")            # 'reduce el consumo medio en más de un 5%'
    assert "0,95·μ(sin aditivo)" in res[0].resumen and "RECHAZA" in res[0].resumen
    assert "h = 0,925 (reducción mínima 7,5%)" in res[1].resumen


def test_canon_no_confunde_grupos_numerados_al_reves():
    a = analizar("La máquina nueva produjo en 15 horas un promedio de 48,5 unidades con un desvío de 3,1; la vieja, "
                 "en 12 horas, un promedio de 44,9 unidades con un desvío de 2,8.", [("a", "¿Produce más la nueva?")])
    b = analizar("La máquina vieja produjo en 12 horas un promedio de 44,9 unidades con un desvío de 2,8; la nueva, "
                 "en 15 horas, un promedio de 48,5 unidades con un desvío de 3,1.", [("a", "¿Produce más la nueva?")])
    h = "H0: δ = μ({0}) - μ({1}) ≤ 0  vs  H1: δ = μ({0}) - μ({1}) > 0"
    na, va = a.datos["nombre1"], a.datos["nombre2"]                     # en a: nueva primero
    nb, vb = b.datos["nombre2"], b.datos["nombre1"]                     # en b: vieja primero
    assert rev._canon(h.format(na, va), a) == rev._canon(h.format(nb, vb), b)
    assert rev._canon(h.format(na, va), a) != rev._canon(h.format(vb, nb), b)
