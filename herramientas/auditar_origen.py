"""Números de la resolución del solver que aparecen sin origen (ni dato del enunciado ni fórmula), en toda la guía.

    python herramientas/auditar_origen.py [ID ...] [--detalle]
"""

import json
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from asistente.explicar import enunciado_texto, resolucion_texto  # noqa: E402
from interprete.analizador import analizar  # noqa: E402
from interprete.origen import resultados, sin_origen  # noqa: E402
from interprete.resolver import resolver  # noqa: E402

GUIA = json.loads((RAIZ / "datos" / "guia_ejercicios.json").read_text(encoding="utf-8"))


def resolver_ej(ej):
    if ej["incisos"] and ej["incisos"][0]["letra"] == "única":
        an = analizar(ej["enunciado"], None, tablas=ej.get("tablas") or None)
    else:
        an = analizar(ej["planteo"], [(i["letra"], i["texto"]) for i in ej["incisos"]],
                      tablas=ej.get("tablas") or None)
    return an, resolver(an)


def main():
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    prefijos = tuple(a + "-" for a in ids if "-" not in a)       # «V» = todo el tema V
    detalle = "--detalle" in sys.argv
    total, con_falta, frases = 0, 0, Counter()
    for ej in GUIA:
        if ids and ej["id"] not in ids and not ej["id"].startswith(prefijos or ("#",)):
            continue
        try:
            an, res = resolver_ej(ej)
        except Exception:
            continue
        enun = enunciado_texto(an)
        previos = []
        for inc, r in zip(an.incisos, res):
            if r.errores:
                continue
            total += 1
            texto = "\n".join(r.pasos) + "\n" + r.conclusion
            faltan = sin_origen(texto, enun, previos=previos)
            previos += resultados(texto)
            if faltan:
                con_falta += 1
                print(f"{ej['id']} {inc.letra}) [{inc.tipo}]: {', '.join(faltan)}")
                if detalle:
                    for linea in texto.split("\n"):
                        if any(f in linea for f in faltan):
                            print("    ", linea[:300])
    print(f"\n{con_falta}/{total} incisos con números sin origen")


if __name__ == "__main__":
    main()
