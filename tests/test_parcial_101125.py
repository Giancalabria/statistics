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


def test_ajuste_gamma_no_hereda_la_confianza_del_ic():
    """1c no fija el riesgo: no hereda α = 0,10 del «NC del 90%» del inciso b (otro tema, una estimación). Se elige
    α = 0,05 y se justifica: χ² = 4,6678 < 5,9915, no se rechaza (con 0,10 rechazaba por poco). Práctica del 10/11."""
    an, res = _resumenes("T1")
    assert "alpha" not in an.incisos[2].params
    assert res[2] == "Gamma: χ² = 4,6678 vs 5,9915 NO rechaza"


def test_lectura_ia_con_la_tabla_dentro_del_planteo():
    """Práctica del 10/11: tabla pegada en el planteo (sin «Tabla de datos»). La IA por tema había puesto n = 120/100,
    x̄ = 26,5/27,5 y S = 6,86 inventados, y arrastrado α = 0,10 del IC al ajuste Gamma. Las reglas, que leen la tabla
    del texto, pisan lo calculado; el α heredado de una estimación se saca."""
    from asistente.interpretar import completar_con_reglas
    from interprete.modelo import Analisis, Inciso
    ex = EX["T1"]
    filas = "\n".join(" | ".join(str(c) for c in f) for f in ex["tablas"][0]["filas"])
    planteo = ex["planteo"] + "\n\n" + " | ".join(ex["tablas"][0]["columnas"]) + "\n" + filas
    (a, ta), (b, tb), (c, tc) = [tuple(i) for i in ex["incisos"]]
    ia = Analisis(planteo, tema="dos_medias",
                  datos={"n1": 120, "n2": 100, "xbar1": 26.5, "xbar2": 27.5, "s1": 6.86, "s2": 6.86},
                  incisos=[Inciso(a, ta, "ensayo", {"delta0_pct": 0.01, "sujeto": 1, "alpha": 0.05}),
                           Inciso(b, tb, "ic", {"alpha": 0.1, "cota": "sup"}),
                           Inciso(c, tc, "ensayo", {"tema": "chi_ajuste", "modelos": ["gamma"], "alpha": 0.1})])
    completar_con_reglas(ia, planteo, [(a, ta), (b, tb), (c, tc)])
    assert (ia.datos["n1"], ia.datos["n2"]) == (128, 103)
    assert "alpha" not in ia.incisos[2].params
    assert [r.resumen for r in resolver(ia)][2] == "Gamma: χ² = 4,6678 vs 5,9915 NO rechaza"
