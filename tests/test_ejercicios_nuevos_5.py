"""Reglas generales que salieron de la 5ª tanda de ejercicios nuevos (datos/ejercicios_nuevos_5.json, 16/11/2026)."""

import json
from pathlib import Path

import pytest

from interprete.analizador import analizar
from interprete.resolver import resolver

TANDA = {e["id"]: e for e in json.loads((Path(__file__).resolve().parent.parent / "datos" /
                                         "ejercicios_nuevos_5.json").read_text(encoding="utf-8"))}


def _resolver(ident):
    e = TANDA[ident]
    an = analizar(e["planteo"], [tuple(i) for i in e["incisos"]], tablas=e["tablas"])
    return an, resolver(an)


def test_n_y_r_con_un_verbo_corto_y_el_porcentaje_pasa_a_p0():
    an, res = _resolver("Y1")             # '… de los 300 pacientes …, 24 se volvieron a internar'
    assert (an.datos["n"], an.datos["r"]) == (300, 24) and an.datos["p0"] == pytest.approx(0.12)
    assert "rc = 26" in res[0].resumen and "RECHAZA" in res[0].resumen


def test_facturas_con_errores_no_es_el_error_de_estimacion():
    an, res = _resolver("Y2")
    assert "e" not in an.datos and an.datos["p0"] == pytest.approx(0.04)
    assert "n = 239; rc = 17" in res[0].resumen


def test_dos_laboratorios_con_dos_desvios_y_hay_diferencias():
    an, res = _resolver("Y3")
    assert an.tema == "dos_varianzas" and (an.datos["n1"], an.datos["n2"]) == (12, 10)
    assert an.incisos[0].tipo == "ensayo" and "RECHAZA" in res[0].resumen
    assert "laboratorio 1" in res[0].resumen


def test_reduccion_minima_despues_de_un_ensayo_en_forma_menos():
    _, res = _resolver("Y4")
    assert res[1].resumen == "δ ≥ 2,6591"


def test_cambio_por_cada_unidad_adicional_es_el_ic_de_la_pendiente():
    an, res = _resolver("Y9")
    assert an.incisos[1].tipo == "ic_coef" and "[-0,7541 ; -0,6435]" in res[1].resumen
