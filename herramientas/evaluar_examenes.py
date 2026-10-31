"""Evalúa la app con exámenes reales de la cátedra (datos/examenes_reales.json), no con la guía.

    python herramientas/evaluar_examenes.py            # solo reglas (instantáneo)
    python herramientas/evaluar_examenes.py --ia       # consenso: reglas + 2 lecturas de IA (necesita Ollama)

Cada inciso tiene una referencia calculada aparte (scipy): un texto que tiene que aparecer en el resumen, ["n", valor]
(un número del resumen con tolerancia de redondeo) o ["d", "rechaza" | "no_rechaza"]. Los incisos ambiguos
(esperado = null) no se puntúan. Para medir sin sesgo, un examen nuevo se evalúa ANTES de corregir nada mirándolo.
"""

import json
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from asistente.comparar import _decision  # noqa: E402
from interprete.analizador import analizar  # noqa: E402
from interprete.resolver import resolver  # noqa: E402
from interprete.texto import buscar_numeros  # noqa: E402


def cumple(resultado, esperado) -> bool:
    texto = resultado.resumen or ""
    numeros = [abs(n.valor) for n in buscar_numeros(texto)]
    for e in esperado:
        if isinstance(e, str):
            if e not in texto:
                return False
        elif e[0] == "d":
            if _decision(resultado) != e[1]:
                return False
        elif not any(abs(x - abs(e[1])) <= max(6e-4, 6e-4 * abs(e[1])) for x in numeros):
            return False
    return True


def main():
    con_ia = "--ia" in sys.argv
    examenes = json.loads((RAIZ / "datos" / "examenes_reales.json").read_text(encoding="utf-8"))
    if con_ia:
        from asistente.consenso import consenso
    tot = {"incisos": 0, "reglas": 0, "ia": 0, "ia_razonada": 0, "consenso": 0, "consenso_mal": 0, "alguna": 0}
    for ex in examenes:
        incisos = [tuple(i) for i in ex["incisos"]] if ex["incisos"] else None
        t0 = time.time()
        if con_ia:
            c = consenso(ex["planteo"], incisos, ex["tablas"])
            filas = [(ic.letra, {v.fuente: v.resultado for v in ic.votos}, ic) for ic in c.incisos]
        else:
            an = analizar(ex["planteo"], incisos, tablas=ex["tablas"])
            filas = [(inc.letra, {"reglas": r}, None) for inc, r in zip(an.incisos, resolver(an))]
        for (letra, votos, ic), esp in zip(filas, ex["esperado"]):
            if esp is None:
                continue
            tot["incisos"] += 1
            bien = sorted(f for f, r in votos.items() if cumple(r, esp))
            for f in bien:
                tot[f] += 1
            tot["alguna"] += bool(bien)
            linea = f"{ex['id']}{letra:6} aciertan: {', '.join(bien) or '—'}"
            if ic is not None:
                elegido_ok = ic.elegido is not None and cumple(ic.elegido.resultado, esp)
                tot["consenso"] += elegido_ok
                tot["consenso_mal"] += ic.estado == "consenso" and not elegido_ok
                linea += f" | {ic.estado}: {'OK' if elegido_ok else 'MAL'}"
            print(linea)
        print(f"   {ex['id']} ({ex['examen']}, {time.time() - t0:.0f} s)")
    n = tot["incisos"]
    print(f"\nReglas {tot['reglas']}/{n}" + (f" · IA con ejemplos {tot['ia']}/{n} · IA razonada {tot['ia_razonada']}/{n}"
                                            f" · CONSENSO {tot['consenso']}/{n} (consensos equivocados: "
                                            f"{tot['consenso_mal']}) · alguna lectura bien {tot['alguna']}/{n}"
                                            if con_ia else ""))


if __name__ == "__main__":
    main()
