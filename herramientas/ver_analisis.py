"""Muestra por consola el análisis de ejercicios de la guía (para calibrar reglas).

    python herramientas/ver_analisis.py I-1 II-4 III-9
    python herramientas/ver_analisis.py --tema I
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from interprete.analizador import analizar  # noqa: E402

GUIA = json.loads((RAIZ / "datos" / "guia_ejercicios.json").read_text(encoding="utf-8"))


def mostrar(ej, resolver_tambien=False):
    an = analizar(ej["planteo"], [(i["letra"], i["texto"]) for i in ej["incisos"]])
    print(f"=== {ej['id']}  tema={an.tema}  criterio={an.criterio}")
    print("   datos:", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in an.datos.items()})
    for a in an.avisos:
        print("   AVISO:", a)
    for inc in an.incisos:
        print(f"   {inc.letra}) {inc.tipo:12s} {inc.params}")
    if resolver_tambien:
        from interprete.resolver import resolver
        for inc, res in zip(an.incisos, resolver(an)):
            print(f"   -> {inc.letra}) {res.resumen}")
            for e in res.errores:
                print("      ERROR:", e)
    print("   RESP:", ej["respuesta"][:300])


def main():
    args = sys.argv[1:]
    resolver_tambien = "--resolver" in args
    args = [a for a in args if a != "--resolver"]
    if args and args[0] == "--tema":
        sel = [e for e in GUIA if e["tema"] == args[1]]
    else:
        sel = [e for e in GUIA if e["id"] in args] if args else GUIA
    for ej in sel:
        mostrar(ej, resolver_tambien)


if __name__ == "__main__":
    main()
