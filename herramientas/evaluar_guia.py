"""Evalúa el intérprete contra la Guía de Problemas (respuestas verificadas).

Para cada ejercicio: analiza el enunciado (como si se pegara el texto), resuelve cada inciso y
compara los números obtenidos con los `valores` de la respuesta de la guía de ese inciso
(`datos/guia_ejercicios.json`, armado con `herramientas/armar_guia.py`). En los contrastes cuya
respuesta es solo verbal se compara la decisión (rechaza / no rechaza).

    python herramientas/evaluar_guia.py              # resumen, temas I a VIII
    python herramientas/evaluar_guia.py -v           # detalle por inciso
    python herramientas/evaluar_guia.py -v I-5 VII   # solo algunos ejercicios / temas
    python herramientas/evaluar_guia.py --fallas     # solo los incisos que no coinciden

Métricas:
- tema: el tema detectado coincide con el TEMA de la guía.
- valores: cuántos de los valores de la respuesta aparecen (con tolerancia de redondeo) en lo calculado.
- exactos: de esos, cuántos coinciden en todos los dígitos que informa la guía (redondeo común o hacia
  afuera). Los que solo coinciden «aprox.» delatan una convención de la cátedra que no se aplica.
- decisiones: en incisos sin valores, si la decisión coincide.
"""

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from interprete.analizador import analizar  # noqa: E402
from interprete.resolver import resolver  # noqa: E402

GUIA = json.loads((RAIZ / "datos" / "guia_ejercicios.json").read_text(encoding="utf-8"))

TEMA_ESPERADO = {"I": {"media"}, "II": {"varianza"}, "III": {"proporcion"}, "IV": {"dos_varianzas"},
                 "V": {"dos_medias"}, "VI": {"chi_contingencia", "chi_ajuste"}, "VII": {"regresion"},
                 "VIII": {"regresion", "regresion_multiple"}}


def coincide(v: float, calculados) -> bool:
    """v (de la guía, redondeado) coincide con algún calculado: mismo redondeo, ±0,2% o como porcentaje."""
    for c in calculados:
        if c is None:
            continue
        for cand in (c, c * 100):
            tol = max(0.011 if abs(v) >= 0.1 else 0.0006, abs(v) * 0.003)
            if abs(cand - v) <= tol:
                return True
    return False


def _decimales(v: float) -> int:
    s = repr(float(v))
    if "e" in s:
        return 6
    return len(s.split(".")[1].rstrip("0")) if "." in s else 0


def coincide_exacto(v: float, calculados) -> bool:
    """v coincide dígito a dígito con algún calculado redondeado a los decimales de v (común o hacia afuera)."""
    import math
    d = _decimales(v)
    k = 10 ** d
    for c in calculados:
        if c is None:
            continue
        for cand in (c, c * 100):
            for r in (round(cand, d), math.floor(cand * k + 1e-9) / k, math.ceil(cand * k - 1e-9) / k):
                if abs(r - v) < 10 ** -(d + 3):
                    return True
    return False


def numeros_de(an, inc, res):
    """Lo calculado + los datos escalares cargados (la guía a veces repite n, x̄, S en la respuesta)."""
    extra = [v for fuente in (an.datos, inc.params) for v in fuente.values()
             if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return list(res.numeros) + extra


def emparejar(ej, an, resultados):
    """[(inciso, resultado, inciso de la guía, números)] — si el intérprete partió un inciso de la guía en
    sub-incisos ("c" → "c.a", "c.b" por un 'Ídem a) y b)'), los valores de "c" se buscan en todos ellos juntos y
    se cuentan en el primero."""
    por_letra = {i["letra"]: i for i in ej["incisos"]}
    union = {}
    for inc, res in zip(an.incisos, resultados):
        union.setdefault(inc.letra.split(".")[0], []).extend(numeros_de(an, inc, res))
    salida, vistos = [], set()
    for k, (inc, res) in enumerate(zip(an.incisos, resultados)):
        base = inc.letra.split(".")[0]
        if inc.letra in por_letra:
            guia, nums = por_letra[inc.letra], numeros_de(an, inc, res)
        elif base in por_letra:
            guia, nums = (por_letra[base], union[base]) if base not in vistos else ({}, [])
            vistos.add(base)
        else:
            guia = ej["incisos"][k] if k < len(ej["incisos"]) else {}
            nums = numeros_de(an, inc, res)
        salida.append((inc, res, guia, nums))
    return salida


def entradas(ej):
    """Lo que pegaría el usuario: planteo + incisos (o el enunciado entero si no tiene incisos)."""
    if ej["incisos"] and ej["incisos"][0]["letra"] == "única":
        return ej["enunciado"], None
    return ej["planteo"], [(i["letra"], i["texto"]) for i in ej["incisos"]]


def decision_de_texto(respuesta: str) -> str:
    """Decisión de una respuesta verbal de la guía ('Se puede asegurar...' / 'No se puede asegurar...')."""
    import unicodedata
    t = "".join(c for c in unicodedata.normalize("NFD", respuesta or "") if unicodedata.category(c) != "Mn").lower()
    t = re.sub(r"^\s*[a-h](\.[a-h])?\)\s*", "", t.strip())
    # la frase de la decisión manda sobre el "Sí / No" que contesta la pregunta ("No, porque se puede asegurar...")
    m = re.search(r"(no )?(se puede (asegurar|afirmar)|se tiene seguridad|hay (motivo|razon|razones|evidencia)|"
                  r"se rechaza)", t)
    if m:
        return "no_rechaza" if m.group(1) else "rechaza"
    if re.match(r"(no[ ,]|no se (puede|rechaza)|no hay (motivo|razon|evidencia))", t):
        return "no_rechaza"
    if re.match(r"(si[ ,]|se puede (asegurar|afirmar|considerar)|se rechaza|hay (motivo|razon|evidencia))", t):
        return "rechaza"
    return ""


def decision_de(res) -> str:
    txt = (res.resumen or "").upper()
    if "NO RECHAZA" in txt or "NO SE RECHAZA" in txt:
        return "no_rechaza"
    if "RECHAZA" in txt:
        return "rechaza"
    return ""


def evaluar(ej, verbose=False, solo_fallas=False):
    planteo, incisos = entradas(ej)
    an = analizar(planteo, incisos, tablas=ej.get("tablas") or None)
    resultados = resolver(an)
    tot = ok = exactos = dtot = dok = 0
    lineas = []
    for inc, res, guia, nums in emparejar(ej, an, resultados):
        esperado = guia.get("valores", []) or []
        hits = [v for v in esperado if coincide(v, nums)]
        aprox = [v for v in hits if not coincide_exacto(v, nums)]
        tot += len(esperado)
        ok += len(hits)
        exactos += len(hits) - len(aprox)
        marca = "OK " if esperado and len(hits) == len(esperado) else ("-- " if not esperado else "XX ")
        dec = guia.get("decision") or (decision_de_texto(guia.get("respuesta", "")) if decision_de(res) else "")
        if not esperado and dec:
            dtot += 1
            if decision_de(res) == dec:
                dok += 1
                marca = "OKd"
            else:
                marca = "XXd"
        if marca == "OK " and aprox:
            marca = "OK~"
        falla = marca.startswith("XX") or marca == "OK~" or bool(res.errores)
        if verbose and (not solo_fallas or falla):
            err = f" ERR: {res.errores[0]}" if res.errores else ""
            faltan = [v for v in esperado if v not in hits]
            lineas.append(f"  {marca} {inc.letra}) {inc.tipo:10s} {res.resumen[:90]}"
                          f"{'  | faltan ' + str(faltan) if faltan else ''}{'  | aprox. ' + str(aprox) if aprox else ''}{'  | guía: ' + dec if marca == 'XXd' else ''}{err}")
    tema_ok = an.tema in TEMA_ESPERADO[ej["tema"]]
    if verbose and (lineas or not tema_ok):
        print(f"=== {ej['id']} tema={an.tema}{'' if tema_ok else ' (!! guía ' + ej['tema'] + ')'}")
        print("\n".join(lineas))
    return tema_ok, tot, ok, exactos, dtot, dok


def main():
    args = sys.argv[1:]
    verbose = "-v" in args or "--fallas" in args
    solo_fallas = "--fallas" in args
    filtros = [a for a in args if not a.startswith("-")]
    sel = [e for e in GUIA if not filtros or e["id"] in filtros or e["tema"] in filtros]
    por_tema = {}
    for ej in sel:
        r = evaluar(ej, verbose, solo_fallas)
        t = por_tema.setdefault(ej["tema"], [0] * 7)
        for i, v in enumerate((1,) + r):
            t[i] += v
    print("\nTEMA   ejerc  tema_ok   valores    exactos     decisiones")
    g = [0] * 7
    for tema, (n, tok, tot, ok, ex, dtot, dok) in por_tema.items():
        print(f"{tema:5s} {n:5d}  {tok:5d}     {ok:4d}/{tot:<4d}  {ex:4d}/{tot:<4d}   {dok:3d}/{dtot}")
        g = [a + b for a, b in zip(g, (n, tok, tot, ok, ex, dtot, dok))]
    print(f"TOTAL {g[0]:5d}  {g[1]:5d}     {g[3]:4d}/{g[2]:<4d}  {g[4]:4d}/{g[2]:<4d}   {g[6]:3d}/{g[5]}   "
          f"({100 * g[3] / max(1, g[2]):.0f}% · exactos {100 * g[4] / max(1, g[2]):.0f}%)")


if __name__ == "__main__":
    main()
