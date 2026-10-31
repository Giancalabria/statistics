"""2° parcial del 10/11/2025 (tema 1, turno noche), transcripto tal cual.

Se usó como prueba CIEGA del consenso (2/5 sin ajustar nada); después se corrigieron las reglas en lo que fallaban.
Valores controlados con una resolución independiente (scipy)."""

import json
from pathlib import Path

from interprete.analizador import analizar
from interprete.resolver import resolver

EX = {x["id"]: x for x in json.loads((Path(__file__).resolve().parent.parent / "datos" / "examenes_reales.json")
                                     .read_text(encoding="utf-8")) if x["id"] in ("T1", "T2")}


def _resumenes(id_):
    ex = EX[id_]
    an = analizar(ex["planteo"], [tuple(i) for i in ex["incisos"]], tablas=ex["tablas"])
    return an, [r.resumen for r in resolver(an)]


def test_diferencia_respecto_de_otro_grupo_en_tabla_de_clases():
    an, res = _resumenes("T1")
    # 'una diferencia de más del 1% ... del equipo A respecto del B': dos medias con δ* = μA - 1,01·μB, no χ²
    assert an.incisos[0].params["tema"] == "dos_medias"
    assert "1,01·μ" in res[0] and "NO rechaza" in res[0]
    # 'estimar la diferencia máxima esperada (NC 90%)': cota superior del IC de μA - μB (S ponderada tras el test F)
    assert an.incisos[1].tipo == "ic" and an.incisos[1].params["cota"] == "sup"
    assert "1,2268" in res[1]
    assert "4,6678" in res[2]


def test_porcentaje_de_no_falladas_complementa_lo_contado():
    an, res = _resumenes("T2")
    # se contaron 9 unidades CON fallas y se pide el porcentaje de NO falladas: r = 95 - 9, IC exacto
    assert an.incisos[1].params.get("r_buenas")
    assert "0,8277" in res[1] and "0,9558" in res[1]
