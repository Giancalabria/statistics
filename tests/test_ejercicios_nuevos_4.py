"""Reglas generales que salieron de la 4ª tanda de ejercicios nuevos (datos/ejercicios_nuevos_4.json, 16/11/2026)."""

import json
from pathlib import Path

from interprete.analizador import analizar, tabla_vertical
from interprete.resolver import resolver

TANDA = {e["id"]: e for e in json.loads((Path(__file__).resolve().parent.parent / "datos" /
                                         "ejercicios_nuevos_4.json").read_text(encoding="utf-8"))}


def _resolver(ident):
    e = TANDA[ident]
    an = analizar(e["planteo"], [tuple(i) for i in e["incisos"]], tablas=e["tablas"])
    return an, resolver(an)


def test_riesgo_de_rechazarlo_es_una_probabilidad_pero_no_el_riesgo_del_cinco():
    an, res = _resolver("W2")
    assert an.incisos[1].tipo == "beta" and "0,0784" in res[1].resumen
    an2 = analizar("¿Un acelerante aumenta la dureza? Con acelerante: 75,3 – 76,7 – 70,8 – 72,7 – 69,1. Sin "
                   "acelerante: 69,3 – 75,4 – 71,3 – 69,5 – 72,8. ¿Qué se concluye con un riesgo del 5%?")
    assert an2.incisos[0].tipo == "ensayo"


def test_la_estimacion_sigue_el_orden_del_ensayo():
    _, res = _resolver("W4")              # 'reduce … en al menos 10 g' → la reducción mínima es de μ(anterior) - μ(nueva)
    assert "δ ≥ 8,911" in res[1].resumen


def test_cada_uno_de_n_con_n_igual_al_largo_de_las_listas_es_apareadas():
    an, res = _resolver("W5")
    assert an.datos["apareadas"] is True and "RECHAZA" in res[0].resumen


def test_tabla_de_clases_acostada_se_para_y_la_de_observaciones_no():
    an, res = _resolver("W6")
    assert an.tema == "chi_ajuste" and "0,5571" in res[0].resumen
    grupos = {"columnas": ["Proceso", "1", "2", "3", "4"], "filas": [["Viejo", 6, 4, 5, 5], ["Nuevo", 2, 1, 2, 2]]}
    assert tabla_vertical(grupos) is grupos


def test_binomial_con_n_de_la_frase_o_del_dominio_completo():
    _, res = _resolver("W7")              # 'cajas de 4 huevos cada una', valores 0 a 4
    assert "1,0508" in res[0].resumen


def test_porcentajes_por_zona_y_las_mismas_preferencias_es_contingencia():
    an, res = _resolver("W8")             # 'zona sur': palabra de 3 letras
    assert an.tema == "chi_contingencia" and "4,7724" in res[0].resumen
