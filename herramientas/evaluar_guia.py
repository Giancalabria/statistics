"""Evalúa el intérprete contra la Guía de Problemas.

Para cada ejercicio: analiza el enunciado, resuelve cada inciso y compara los
números obtenidos con los de la respuesta (`Resp:`) de la guía.

    python herramientas/evaluar_guia.py            # resumen (alcance del primer parcial)
    python herramientas/evaluar_guia.py --todo     # temas I a VI completos
    python herramientas/evaluar_guia.py -v         # detalle por inciso
    python herramientas/evaluar_guia.py -v I-5     # solo algunos ejercicios

Métricas:
- tema: el tema detectado coincide con el TEMA de la guía.
- números: de los valores que figuran en la respuesta de cada inciso, cuántos
  aparecen (redondeados a 2 decimales, o como porcentaje) en lo calculado.
"""

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from interprete.analizador import analizar, separar_incisos  # noqa: E402
from interprete.resolver import resolver  # noqa: E402
from interprete.texto import buscar_numeros  # noqa: E402

GUIA = json.loads((RAIZ / "datos" / "guia_ejercicios.json").read_text(encoding="utf-8"))

TEMAS_EXAMEN = ("I", "II", "III", "IV", "V", "VI")

# Alcance del primer parcial: Tema I 1-34, Tema II 1-12, Tema III solo estimación (1-8).
PARCIAL = {"I": range(1, 35), "II": range(1, 13), "III": range(1, 9)}

TEMA_ESPERADO = {"I": {"media"}, "II": {"varianza"}, "III": {"proporcion"}, "IV": {"dos_varianzas"},
                 "V": {"dos_medias"}, "VI": {"chi_contingencia", "chi_ajuste"}, "VII": {"regresion"},
                 "VIII": {"regresion"}}


def numeros_respuesta(texto: str):
    """Números 'significativos' de una respuesta (descarta 0, 1, 2 sueltos del texto de fórmulas)."""
    texto = re.sub(r"problemas? \d+( y \d+)?|problema \d+", "", texto)
    out = []
    for n in buscar_numeros(texto):
        v = n.valor
        if n.es_entero and v <= 2:
            continue
        out.append(v)
    return out


def coincide(v: float, calculados) -> bool:
    for c in calculados:
        for cand in (c, c * 100):
            if abs(round(cand, 2) - v) <= 0.011 + 0.005 * abs(v) * 0 or abs(cand - v) <= max(0.006, abs(v) * 0.002):
                return True
            if float(v).is_integer() and round(cand) == v and abs(cand - v) < 0.5 and float(cand).is_integer():
                return True
    return False


def evaluar(ej, verbose=False):
    incisos = [(i["letra"], i["texto"]) for i in ej["incisos"]]
    an = analizar(ej["planteo"], incisos)
    resultados = resolver(an)
    _, resp_incisos = separar_incisos(ej["respuesta"])
    resp = dict(resp_incisos) if resp_incisos else ({"única": ej["respuesta"]} if ej["respuesta"] else {})
    tot = ok = 0
    detalle = []
    for inc, res in zip(an.incisos, resultados):
        esperado = numeros_respuesta(resp.get(inc.letra, ""))
        hits = [v for v in esperado if coincide(v, res.numeros)]
        tot += len(esperado)
        ok += len(hits)
        detalle.append((inc, res, esperado, hits))
    tema_ok = an.tema in TEMA_ESPERADO[ej["tema"]]
    if verbose:
        print(f"=== {ej['id']} tema={an.tema}{'' if tema_ok else ' (!!)'} datos={_corto(an.datos)}")
        for inc, res, esp, hits in detalle:
            marca = "OK " if esp and len(hits) == len(esp) else ("-- " if not esp else "XX ")
            print(f"  {marca}{inc.letra}) {inc.tipo:10s} {res.resumen[:90]}  | esperado {esp} {'ERR: ' + res.errores[0] if res.errores else ''}")
            print(f"        params={_corto(inc.params)}")
    return tema_ok, tot, ok


def _corto(d):
    return {k: (round(v, 4) if isinstance(v, float) else (v if not isinstance(v, list) or len(v) < 6 else f"[{len(v)} valores]"))
            for k, v in d.items()}


def main():
    args = sys.argv[1:]
    verbose = "-v" in args
    todo = "--todo" in args
    ids = [a for a in args if a not in ("-v", "--todo")]
    # Solo los temas del primer examen (los que resuelve la app): I a VI.
    sel = [e for e in GUIA if e["tema"] in TEMAS_EXAMEN and (not ids or e["id"] in ids or e["tema"] in ids)]
    if not todo:
        sel = [e for e in sel if e["tema"] in PARCIAL and e["numero"] in PARCIAL[e["tema"]]]
    por_tema = {}
    for ej in sel:
        tema_ok, tot, ok = evaluar(ej, verbose)
        t = por_tema.setdefault(ej["tema"], [0, 0, 0, 0])
        t[0] += 1
        t[1] += tema_ok
        t[2] += tot
        t[3] += ok
    print("\nTEMA  ejerc  tema_ok  números_ok")
    g = [0, 0, 0, 0]
    for tema, (n, tok, tot, ok) in por_tema.items():
        print(f"{tema:5s} {n:5d}  {tok:4d}     {ok}/{tot}")
        g = [a + b for a, b in zip(g, (n, tok, tot, ok))]
    print(f"TOTAL {g[0]:5d}  {g[1]:4d}     {g[3]}/{g[2]}  ({100 * g[3] / max(1, g[2]):.0f}%)")


if __name__ == "__main__":
    main()
