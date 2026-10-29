"""Evalúa el intérprete contra la Guía de Problemas (respuestas verificadas).

Para cada ejercicio: analiza el enunciado (como si se pegara el texto), resuelve cada inciso y
compara los números obtenidos con los `valores` de la respuesta de la guía de ese inciso
(`datos/guia_ejercicios.json`, armado con `herramientas/armar_guia.py`). En los contrastes cuya
respuesta es solo verbal se compara la decisión (rechaza / no rechaza).

    python herramientas/evaluar_guia.py              # resumen, temas I a VIII
    python herramientas/evaluar_guia.py -v           # detalle por inciso
    python herramientas/evaluar_guia.py -v I-5 VII   # solo algunos ejercicios / temas
    python herramientas/evaluar_guia.py --fallas     # solo los incisos que no coinciden
    python herramientas/evaluar_guia.py --raros      # banco de enunciados "estilo examen raro"
    python herramientas/evaluar_guia.py --raros -v R-V-8 VI   # detalle de algunos (por id o tema)

`--raros` corre el intérprete sobre `datos/enunciados_raros.json`: ejercicios de la guía reescritos a mano con otra
redacción (sinónimos, números en palabras, datos en otro orden, tablas en prosa, incisos pegados en el texto...) y
enunciados de práctica, con la respuesta esperada. Mide tema, incisos clasificados, valores y decisiones. Los marcados
`"control": true` se escribieron después de ajustar las reglas y se informan aparte (miden si los arreglos generalizan).

Con la IA local (Ollama abierto, ver ASISTENTE_IA.md):

    python herramientas/evaluar_guia.py --ia I II       # la IA SOLA arma el planteo (sin reglas)
    python herramientas/evaluar_guia.py --ia-hibrido    # reglas + IA, como en la app
    python herramientas/evaluar_guia.py --revision      # reglas + solver, y la IA revisa el planteo
    opciones: --modelo qwen3:14b  --pensar  --limite 20

En los dos modos el ejercicio evaluado se excluye de los ejemplos que se le muestran al modelo (si no, copiaría
la respuesta). `--ia` mide cuánto entiende el modelo por sí mismo; `--ia-hibrido` cuenta además las
"sugerencias": diferencias de la IA con las reglas, que en la guía están verificadas, así que son falsas
alarmas (cuantas menos, mejor).

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


def analizar_reglas(ej, planteo, incisos):
    return analizar(planteo, incisos, tablas=ej.get("tablas") or None)


def evaluar(ej, verbose=False, solo_fallas=False, obtener=analizar_reglas):
    planteo, incisos = entradas(ej)
    an = obtener(ej, planteo, incisos)
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


RAROS = RAIZ / "datos" / "enunciados_raros.json"


def como_guia(raro):
    """Un enunciado del banco raro con la forma de un ejercicio de la guía (para reusar `emparejar`)."""
    esperado, decision = raro.get("esperado") or {}, raro.get("decision") or {}
    letras = [i["letra"] for i in raro["incisos"]] or list(esperado)
    return {"id": raro["id"], "tema": raro["tema"], "tablas": raro.get("tablas") or [],
            "incisos": [{"letra": l, "valores": esperado.get(l, []), "decision": decision.get(l, "")} for l in letras]}


def evaluar_raro(raro, verbose=False, solo_fallas=False):
    """(tema_ok, incisos esperados, incisos clasificados, valores, ok, decisiones, dok, incisos separados bien)."""
    ej = como_guia(raro)
    incisos = [(i["letra"], i["texto"]) for i in raro["incisos"]] or None
    an = analizar(raro["enunciado"], incisos, tablas=ej["tablas"] or None)
    resultados = resolver(an)
    letras_an = [i.letra.split(".")[0] for i in an.incisos]
    separados = all(i["letra"] in letras_an for i in ej["incisos"])
    tot = ok = dtot = dok = clas = 0
    lineas = []
    vistos = set()
    for inc, res, guia, nums in emparejar(ej, an, resultados):
        base = inc.letra.split(".")[0]
        if base not in vistos and inc.tipo != "no_soportado" and not res.errores:
            clas += 1
            vistos.add(base)
        esperado = guia.get("valores", []) or []
        hits = [v for v in esperado if coincide(v, nums)]
        tot += len(esperado)
        ok += len(hits)
        dec = guia.get("decision") or ""
        dmarca = ""
        if dec:
            dtot += 1
            if decision_de(res) == dec:
                dok += 1
            else:
                dmarca = f"  | decisión {decision_de(res) or '—'} (esperada {dec})"
        falla = len(hits) < len(esperado) or bool(dmarca) or bool(res.errores) or inc.tipo == "no_soportado"
        if verbose and (not solo_fallas or falla):
            marca = "XX " if falla else "OK "
            err = f" ERR: {res.errores[0]}" if res.errores else ""
            faltan = [v for v in esperado if v not in hits]
            lineas.append(f"  {marca} {inc.letra}) {inc.tipo:10s} {res.resumen[:90]}"
                          f"{'  | faltan ' + str(faltan) if faltan else ''}{dmarca}{err}")
    n_inc = len(ej["incisos"])
    clas = min(clas, n_inc)
    tema_ok = an.tema in TEMA_ESPERADO[raro["tema"]]
    if verbose and (lineas or not tema_ok or not separados):
        print(f"=== {raro['id']} ({raro['ejercicio_origen']}) tema={an.tema}"
              f"{'' if tema_ok else ' (!! esperado ' + raro['tema'] + ')'}"
              f"{'' if separados else ' (!! incisos ' + str(letras_an) + ')'}")
        print("\n".join(lineas))
    return tema_ok, n_inc, clas, tot, ok, dtot, dok, separados


def main_raros(args):
    verbose = "-v" in args or "--fallas" in args
    solo_fallas = "--fallas" in args
    filtros = [a for a in args if not a.startswith("-")]
    banco = json.loads(RAROS.read_text(encoding="utf-8"))
    sel = [r for r in banco if not filtros or r["id"] in filtros or r["tema"] in filtros]
    por_tema, control = {}, [0] * 9
    for r in sel:
        t = por_tema.setdefault(r["tema"], [0] * 9)
        fila = (1,) + evaluar_raro(r, verbose, solo_fallas)
        for i, v in enumerate(fila):
            t[i] += v
            if r.get("control"):
                control[i] += v
    print("\nTEMA   enunc  tema_ok  incisos_ok   valores    decisiones  separados")
    g = [0] * 9
    for tema in sorted(por_tema, key=lambda x: ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"].index(x)):
        n, tok, ninc, clas, tot, ok, dtot, dok, sep = por_tema[tema]
        print(f"{tema:5s} {n:5d}  {tok:5d}    {clas:4d}/{ninc:<4d}  {ok:4d}/{tot:<4d}   {dok:3d}/{dtot:<4d}   {sep:3d}/{n}")
        g = [a + b for a, b in zip(g, por_tema[tema])]
    print(f"TOTAL {g[0]:5d}  {g[1]:5d}    {g[3]:4d}/{g[2]:<4d}  {g[5]:4d}/{g[4]:<4d}   {g[7]:3d}/{g[6]:<4d}   {g[8]:3d}/{g[0]}   "
          f"(valores {100 * g[5] / max(1, g[4]):.0f}% · decisiones {100 * g[7] / max(1, g[6]):.0f}%)")
    if control[0]:
        c = control
        print(f"  de esos, CONTROL (escritos después de los arreglos, sin ajustar nada para ellos): {c[0]} enunciados, "
              f"tema {c[1]}/{c[0]}, incisos {c[3]}/{c[2]}, valores {c[5]}/{c[4]}, decisiones {c[7]}/{c[6]}")


def _opcion(args, nombre):
    if nombre in args:
        i = args.index(nombre)
        valor = args[i + 1]
        del args[i:i + 2]
        return valor
    return None


def con_ia(modo, modelo, pensar, stats):
    """Función de análisis que usa la IA (sola o híbrida) y va sumando tiempos, errores y sugerencias."""
    import time
    from asistente import cliente
    from asistente.interpretar import interpretar, pedir_ia

    if not cliente.disponible():
        sys.exit(f"Ollama no responde en {cliente.HOST}: abrilo (`ollama serve`) y descargá el modelo.")

    def obtener(ej, planteo, incisos):
        t0 = time.time()
        tablas = ej.get("tablas") or None
        try:
            if modo == "sola":
                an, _ = pedir_ia(planteo, incisos, tablas, modelo, pensar, excluir=[ej["id"]])
            elif modo == "revision":
                from asistente.revisar import revisar
                rv = revisar(planteo, incisos, tablas, modelo, pensar, excluir=[ej["id"]])
                if rv.error:
                    raise cliente.ErrorIA(rv.error)
                stats["cambios"] += len(rv.corregidos)
                stats["sugeridos"] += len(rv.sugeridos)
                stats["sugerencias"] += len(rv.a_revisar)
                stats["con_alarma"] += bool(rv.corregidos or rv.sugeridos or rv.a_revisar)
                stats["ultima"] = rv
                for i in rv.corregidos + rv.sugeridos + rv.a_revisar:
                    print(f"  ·· {ej['id']} {i.estado} {i.donde}) {i.que}: {i.detalle[:150]}")
                an = rv.analisis
            else:
                r = interpretar(planteo, incisos, tablas, modelo, pensar, siempre=True, excluir=[ej["id"]])
                stats["sugerencias"] += len(r.sugerencias)
                stats["cambios"] += len(r.informe)
                if r.error:
                    raise cliente.ErrorIA(r.error)
                an = r.analisis
        except cliente.ErrorIA as e:
            stats["errores"] += 1
            print(f"  !! {ej['id']}: {e}")
            an = analizar_reglas(ej, planteo, incisos) if modo != "sola" else analizar("", [("a", "")])
        stats["segundos"] += time.time() - t0
        stats["n"] += 1
        return an

    return obtener


def main():
    args = sys.argv[1:]
    if "--raros" in args:
        args.remove("--raros")
        return main_raros(args)
    modelo = _opcion(args, "--modelo")
    limite = _opcion(args, "--limite")
    pensar = "--pensar" in args
    modo = "sola" if "--ia" in args else ("hibrido" if "--ia-hibrido" in args else
                                          ("revision" if "--revision" in args else None))
    verbose = "-v" in args or "--fallas" in args
    solo_fallas = "--fallas" in args
    filtros = [a for a in args if not a.startswith("-")]
    sel = [e for e in GUIA if not filtros or e["id"] in filtros or e["tema"] in filtros]
    if limite:
        sel = sel[:int(limite)]
    stats = {"n": 0, "segundos": 0.0, "errores": 0, "sugerencias": 0, "cambios": 0, "con_alarma": 0,
             "sugeridos": 0}
    aceptando = [0] * 7          # revisión: cómo quedaría si se aceptaran todas las sugerencias
    obtener = con_ia(modo, modelo, pensar, stats) if modo else analizar_reglas
    por_tema = {}
    for ej in sel:
        stats["ultima"] = None
        r = evaluar(ej, verbose, solo_fallas, obtener)
        rv = stats.get("ultima")
        if rv is not None:
            from asistente.revisar import aplicar_sugerencias
            planteo, incisos = entradas(ej)
            todo = aplicar_sugerencias(rv, rv.sugeridos, planteo, incisos, ej.get("tablas") or None)
            r2 = evaluar(ej, False, False, lambda *a: todo)
            aceptando = [a + b for a, b in zip(aceptando, (1,) + r2)]
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
    if modo:
        if modo == "revision":
            print(f"\nRevisión IA: {stats['n']} ejercicios, {stats['segundos'] / max(1, stats['n']):.1f} s por ejercicio, "
                  f"{stats['errores']} errores de la IA, {stats['con_alarma']} ejercicios con alarma (en la guía son "
                  f"falsas), {stats['cambios']} completados (aplicados), {stats['sugeridos']} sugerencias 💡 (no "
                  f"aplicadas), {stats['sugerencias']} puntos a revisar ⚠️")
            print(f"Si se aceptaran TODAS las sugerencias: valores {aceptando[3]}/{aceptando[2]}, decisiones "
                  f"{aceptando[6]}/{aceptando[5]}")
            return
        print(f"\nIA ({'sola' if modo == 'sola' else 'híbrido'}): {stats['n']} ejercicios, "
              f"{stats['segundos'] / max(1, stats['n']):.1f} s por ejercicio, {stats['errores']} errores de la IA"
              + (f", {stats['cambios']} cambios aplicados, {stats['sugerencias']} sugerencias (falsas alarmas)"
                 if modo == "hibrido" else ""))


if __name__ == "__main__":
    main()
