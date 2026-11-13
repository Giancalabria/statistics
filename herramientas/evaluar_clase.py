"""Evalúa la app A CIEGAS con los ejercicios que el profesor resolvió en clase (datos/clase_resueltos.json).

    python -X utf8 herramientas/evaluar_clase.py              # consenso: reglas + 2 lecturas de IA (necesita Ollama)
    python -X utf8 herramientas/evaluar_clase.py --reglas     # solo reglas (instantáneo)
    python -X utf8 herramientas/evaluar_clase.py --hilos 3    # ejercicios en paralelo (la GPU lo aguanta)
    python -X utf8 herramientas/evaluar_clase.py --solo V-8 IV-4

A ciegas quiere decir: la IA recibe solo el enunciado de la guía y NUNCA ese mismo ejercicio como ejemplo (`excluir`);
la resolución del profesor no entra en ningún lado. Los demás ejercicios de clase sí pueden ser base (como en el
examen, donde el problema es nuevo pero los resueltos están a mano).

Ojo: las REGLAS se ajustaron con toda la guía, así que en estos ejercicios no son ciegas; lo que mide algo nuevo es
la columna de las IA y el consenso. Se compara el número y la decisión, y el informe pone lado a lado la H0 que eligió
la app y el planteo del profesor para revisarlo a ojo.

El informe completo queda en herramientas/tmp/evaluar_clase.md.
"""

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "herramientas"))

from evaluar_examenes import cumple  # noqa: E402
from interprete.analizador import analizar  # noqa: E402
from interprete.resolver import resolver  # noqa: E402


def cargar():
    banco = json.loads((RAIZ / "datos" / "clase_resueltos.json").read_text(encoding="utf-8"))["ejercicios"]
    guia = {e["id"]: e for e in json.loads((RAIZ / "datos" / "guia_ejercicios.json").read_text(encoding="utf-8"))}
    return banco, guia


def entrada(ej_guia):
    """(planteo, incisos, tablas) como lo cargaría el alumno."""
    if ej_guia["incisos"] and ej_guia["incisos"][0]["letra"] == "única":
        return ej_guia["enunciado"], None, ej_guia.get("tablas") or None
    return (ej_guia["planteo"], [(i["letra"], i["texto"]) for i in ej_guia["incisos"]],
            ej_guia.get("tablas") or None)


def _hip(r) -> str:
    from asistente.consenso import _hipotesis
    return _hipotesis(r)


def evaluar(ej, guia, con_ia: bool, modelo=None):
    planteo, incisos, tablas = entrada(guia[ej["guia"]])
    t0 = time.time()
    if con_ia:
        from asistente.consenso import consenso
        c = consenso(planteo, incisos, tablas, modelo=modelo, excluir=[ej["guia"]])
        filas = [(ic.letra, {v.fuente: v.resultado for v in ic.votos}, ic) for ic in c.incisos]
    else:
        an = analizar(planteo, incisos, tablas=tablas)
        filas = [(inc.letra, {"reglas": r}, None) for inc, r in zip(an.incisos, resolver(an))]
    salida = []
    for k, (letra, votos, ic) in enumerate(filas):
        esp = ej["esperado"][k] if k < len(ej["esperado"]) else None
        prof = ej["profesor"][k] if k < len(ej["profesor"]) else ""
        bien = sorted(f for f, r in votos.items() if esp is not None and cumple(r, esp))
        elegido = ic.elegido.resultado if ic is not None and ic.elegido else votos.get("reglas")
        salida.append({
            "letra": letra, "esperado": esp, "profesor": prof, "aciertan": bien,
            "estado": ic.estado if ic is not None else "reglas",
            "ok": esp is not None and elegido is not None and cumple(elegido, esp),
            "app_h": _hip(elegido) if elegido is not None else "",
            "app_resumen": (elegido.resumen if elegido is not None else "") or "",
        })
    return ej["guia"], salida, time.time() - t0


def main():
    args = sys.argv[1:]
    con_ia = "--reglas" not in args
    modelo = args[args.index("--modelo") + 1] if "--modelo" in args else None
    hilos = int(args[args.index("--hilos") + 1]) if "--hilos" in args else 1
    banco, guia = cargar()
    if "--solo" in args:
        ids = set(args[args.index("--solo") + 1:])
        banco = [e for e in banco if e["guia"] in ids]
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=hilos) as pool:
        resultados = list(pool.map(lambda e: evaluar(e, guia, con_ia, modelo), banco))

    tot = {"incisos": 0, "ok": 0, "reglas": 0, "ia": 0, "ia_tema": 0, "consenso_mal": 0}
    md = ["# Ejercicios de clase a ciegas\n", f"Modo: {'consenso (reglas + IA)' if con_ia else 'solo reglas'}\n"]
    for gid, filas, seg in resultados:
        md.append(f"\n## {gid} ({seg:.0f} s)\n")
        for f in filas:
            if f["esperado"] is None:
                continue
            tot["incisos"] += 1
            tot["ok"] += f["ok"]
            for fu in f["aciertan"]:
                tot[fu] = tot.get(fu, 0) + 1
            tot["consenso_mal"] += f["estado"] == "consenso" and not f["ok"]
            marca = "OK " if f["ok"] else "MAL"
            print(f"{gid:7}{f['letra']:6} {marca} [{f['estado']}] aciertan: {', '.join(f['aciertan']) or '—'}",
                  flush=True)
            md += [f"**{f['letra']})** {'✅' if f['ok'] else '❌'} `{f['estado']}` · aciertan: "
                   f"{', '.join(f['aciertan']) or '—'}\n",
                   f"- App: {f['app_h'] or '(sin H0)'} — {f['app_resumen']}",
                   f"- Profesor: {f['profesor']}\n"]
    n = tot["incisos"]
    linea = (f"\nAcierta la app (lo que muestra) {tot['ok']}/{n} · reglas {tot['reglas']}/{n}"
             + (f" · IA con ejemplos {tot['ia']}/{n} · IA por tema {tot['ia_tema']}/{n} · consensos equivocados "
                f"{tot['consenso_mal']}" if con_ia else "") + f" · {time.time() - t0:.0f} s")
    print(linea)
    md.append(linea)
    out = RAIZ / "herramientas" / "tmp" / "evaluar_clase.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(md), encoding="utf-8")
    print(f"Informe: {out}")


if __name__ == "__main__":
    main()
