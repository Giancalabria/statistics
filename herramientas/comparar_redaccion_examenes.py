"""Redacción completa (la IA reescribe todo) vs. redacción por partes (el solver escribe, la IA llena palabras),
sobre los exámenes reales (datos/examenes_reales.json), que no se usaron para afinar ninguna de las dos.

    python -X utf8 herramientas/comparar_redaccion_examenes.py            # las dos, todos los exámenes del 2° parcial
    python -X utf8 herramientas/comparar_redaccion_examenes.py --solo T1 P2
    python -X utf8 herramientas/comparar_redaccion_examenes.py --solo-partes

Por problema: fallas del checklist, números que no salen del enunciado ni del solver (copiados mal o inventados),
números sin su cuenta y tiempo. Necesita Ollama. Informe: herramientas/tmp/comparar_redaccion_examenes.md
"""

import json
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from asistente.explicar import numeros_sin_respaldo  # noqa: E402
from asistente.redaccion_partes import fuentes as fuentes_de, redactar_por_partes  # noqa: E402
from asistente.redactar import controlar, corregir, problemas, redactar  # noqa: E402
from interprete.analizador import analizar  # noqa: E402
from interprete.resolver import resolver  # noqa: E402

PRIMER_PARCIAL = ("E1", "E2")


def completa(an):
    res = resolver(an)
    trozos, fuentes = redactar(an, res)
    texto = "".join(trozos)
    fallas = problemas(controlar(texto, an, fuentes, res))
    if fallas:
        texto2 = "".join(corregir(an, res, texto, fallas))
        fallas2 = problemas(controlar(texto2, an, fuentes, res))
        if len(fallas2) < len(fallas):
            texto, fallas = texto2, fallas2
    return texto, fallas, numeros_sin_respaldo(texto, fuentes), []


def por_partes(an):
    red = redactar_por_partes(an)
    f = fuentes_de(red)
    return red.texto, problemas(controlar(red.texto, red.analisis, f, red.resultados)), \
        numeros_sin_respaldo(red.texto, f), red.descartados


def main():
    args = sys.argv[1:]
    solo = [a for a in args[args.index("--solo") + 1:] if not a.startswith("--")] if "--solo" in args else []
    modos = [("partes", por_partes)] if "--solo-partes" in args else [("completa", completa), ("partes", por_partes)]
    examenes = json.loads((RAIZ / "datos" / "examenes_reales.json").read_text(encoding="utf-8"))
    examenes = [e for e in examenes if (e["id"] in solo if solo else e["id"] not in PRIMER_PARCIAL)]
    filas, detalle = [], []
    tot = {m: {"fallas": 0, "inventados": 0, "seg": 0.0} for m, _ in modos}
    for ex in examenes:
        incisos = [tuple(i) for i in ex["incisos"]] if ex["incisos"] else None
        an = analizar(ex["planteo"], incisos, tablas=ex["tablas"])
        celdas = [ex["id"]]
        detalle.append(f"\n## {ex['id']} · {ex['examen']}\n")
        for nombre, f in modos:
            t0 = time.time()
            texto, fallas, inventados, descartados = f(an)
            seg = time.time() - t0
            tot[nombre]["fallas"] += len(fallas)
            tot[nombre]["inventados"] += len(inventados)
            tot[nombre]["seg"] += seg
            celdas += [str(len(fallas)), str(len(inventados)), f"{seg:.0f} s"]
            detalle.append(f"### {nombre}\n\n**Checklist**: " + ("; ".join(fallas) or "todo ✔") +
                           f"\n\n**Números que no salen de ninguna fuente**: {', '.join(inventados) or '—'}" +
                           (f"\n\n**Descartados**: {'; '.join(descartados)}" if descartados else "") +
                           f"\n\n<details><summary>Redacción</summary>\n\n{texto}\n\n</details>\n")
            print(f"{ex['id']} {nombre}: {len(fallas)} fallas, {len(inventados)} inventados, {seg:.0f} s", flush=True)
        filas.append("| " + " | ".join(celdas) + " |")
    cab = ["# Redacción completa vs. por partes (exámenes reales)", "",
           "| Problema | " + " | ".join(f"{m}: fallas | {m}: inventados | {m}: tiempo" for m, _ in modos) + " |",
           "|---|" + "---|---|---|" * len(modos)]
    pie = ["", "**Totales**: " + " · ".join(f"{m}: {t['fallas']} fallas, {t['inventados']} números inventados, "
                                             f"{t['seg']:.0f} s" for m, t in tot.items())]
    informe = "\n".join(cab + filas + pie) + "\n" + "\n".join(detalle)
    salida = RAIZ / "herramientas" / "tmp" / "comparar_redaccion_examenes.md"
    salida.parent.mkdir(exist_ok=True)
    salida.write_text(informe, encoding="utf-8")
    print("\n".join(cab + filas + pie))
    print(f"\nInforme: {salida}")


if __name__ == "__main__":
    main()
