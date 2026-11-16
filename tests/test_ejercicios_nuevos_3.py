"""Reglas generales que salieron de la 3ª tanda de ejercicios nuevos (datos/ejercicios_nuevos_3.json, 16/11/2026)."""

import json
from pathlib import Path

import pytest

from interprete.analizador import analizar
from interprete.resolver import resolver

TANDA = {e["id"]: e for e in json.loads((Path(__file__).resolve().parent.parent / "datos" /
                                         "ejercicios_nuevos_3.json").read_text(encoding="utf-8"))}


def _resolver(ident):
    e = TANDA[ident]
    an = analizar(e["planteo"], [tuple(i) for i in e["incisos"]], tablas=e["tablas"])
    return an, resolver(an)


def test_dos_enteros_libres_en_una_proporcion_son_n_y_r():
    an, res = _resolver("U1")             # 'siguió 240 reparaciones … 19 equipos volvieron'
    assert an.datos["n"] == 240 and an.datos["r"] == 19
    assert "rc = 19" in res[0].resumen and "RECHAZA" in res[0].resumen


def test_riesgo_del_productor_y_del_consumidor_en_la_misma_oracion():
    an, res = _resolver("U2")
    assert an.datos["p0"] == pytest.approx(0.02) and an.datos["p1"] == pytest.approx(0.08)
    assert "n = 98; rc = 5" in res[0].resumen


def test_desvio_en_elipsis_y_el_porcentaje_manda_quien_va_arriba():
    an, res = _resolver("U3")             # 'el desvío de la vieja supera en más de un 20% al de la nueva'
    assert an.tema == "dos_varianzas"
    assert "σ(vieja)/σ(nueva) ≤ 1.2" in res[0].resumen and "NO rechaza" in res[0].resumen
    assert "[1,0781 ; 2,5638]" in res[1].resumen


def test_categorias_con_nombre_y_una_columna_de_conteos_es_ajuste_uniforme():
    an, res = _resolver("U7")
    assert an.tema == "chi_ajuste" and "10,0769" in res[0].resumen


def test_tabla_resumen_la_fila_de_enteros_que_queda_es_n():
    an, res = _resolver("U10")            # 'Operarios observados | 30 | 28'
    assert an.tema == "dos_medias" and {an.datos["n1"], an.datos["n2"]} == {30, 28}
    assert "RECHAZA" in res[0].resumen


def test_nombre_de_grupo_por_la_forma_sustantivo_y_letra():
    an, _ = _resolver("U4")
    assert {an.datos["nombre1"], an.datos["nombre2"]} == {"centro A", "centro B"}
