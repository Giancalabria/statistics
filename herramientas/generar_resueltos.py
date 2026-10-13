"""Genera `Guia_resuelta.md`: todos los ejercicios de la guía resueltos paso a paso por la app.

    python herramientas/generar_resueltos.py            # todos
    python herramientas/generar_resueltos.py VII VI-15  # solo algunos temas / ejercicios (salida a stdout)

Para cada ejercicio: enunciado, tablas, y por inciso la resolución de la app (pasos en el orden de la
cátedra + conclusión), la respuesta de la guía y si coinciden:
  ✅ los valores de la guía aparecen en lo calculado (o la decisión coincide);
  ⚠️ no coinciden → se lista al final en "Discrepancias con la guía" para revisarlas;
  ℹ️ la guía no da valores para comparar.

Si el intérprete no entiende bien un enunciado, `datos/correcciones_interpretacion.json` permite
corregir lo detectado (como se haría en la pantalla): {"VI-20": {"incisos": {"a": {"tema": ..., "tipo": ...,
"params": {...}}}, "datos": {...}}}. Los ejercicios corregidos así quedan marcados con ✍️.
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "herramientas"))

from evaluar_guia import coincide, decision_de, decision_de_texto, emparejar, entradas  # noqa: E402
from interprete.analizador import analizar  # noqa: E402
from interprete.modelo import TEMAS, TIPOS  # noqa: E402
from interprete.resolver import resolver  # noqa: E402
from interprete.texto import fmt  # noqa: E402

GUIA = json.loads((RAIZ / "datos" / "guia_ejercicios.json").read_text(encoding="utf-8"))
CORR_PATH = RAIZ / "datos" / "correcciones_interpretacion.json"
CORRECCIONES = json.loads(CORR_PATH.read_text(encoding="utf-8")) if CORR_PATH.exists() else {}
SALIDA = RAIZ / "Guia_resuelta.md"

NOMBRES_TEMA = {
    "I": "Inferencia para medias", "II": "Inferencia sobre varianzas / desvíos",
    "III": "Procesos de Bernoulli (proporciones)", "IV": "Comparación de varianzas", "V": "Comparación de dos medias",
    "VI": "Contrastes chi-cuadrado", "VII": "Regresión y correlación simple", "VIII": "Modelo lineal general",
}


def _tabla_md(tb) -> str:
    def c(v):
        if v is None:
            return "—"
        if isinstance(v, float):
            return fmt(v, 6)
        return str(v)
    cols = tb.get("columnas") or []
    lineas = []
    if tb.get("titulo"):
        lineas.append(f"*{tb['titulo']}*\n")
    lineas.append("| " + " | ".join(cols) + " |")
    lineas.append("|" + "---|" * len(cols))
    for f in tb.get("filas", []):
        lineas.append("| " + " | ".join(c(v) for v in f) + " |")
    return "\n".join(lineas)


def aplicar_correcciones(ej, an):
    corr = CORRECCIONES.get(ej["id"])
    if not corr:
        return False
    if corr.get("tema"):
        an.tema = corr["tema"]
    an.datos.update(corr.get("datos", {}))
    for inc in an.incisos:
        ci = corr.get("incisos", {}).get(inc.letra)
        if not ci:
            continue
        if ci.get("tema"):
            inc.params["tema"] = ci["tema"]
        if ci.get("tipo"):
            inc.tipo = ci["tipo"]
        inc.params.update(ci.get("params", {}))
    return True


def resolver_ejercicio(ej):
    planteo, incisos = entradas(ej)
    an = analizar(planteo, incisos, tablas=ej.get("tablas") or None)
    corregido = aplicar_correcciones(ej, an)
    return an, resolver(an), corregido


def estado_inciso(guia_inc, res, numeros):
    esperado = guia_inc.get("valores") or []
    if esperado:
        faltan = [v for v in esperado if not coincide(v, numeros)]
        return ("✅" if not faltan else "⚠️"), faltan
    dec = guia_inc.get("decision") or (decision_de_texto(guia_inc.get("respuesta", "")) if decision_de(res) else "")
    if dec:
        return ("✅" if decision_de(res) == dec else "⚠️"), []
    return "ℹ️", []


def md_ejercicio(ej, discrepancias, resumen):
    an, resultados, corregido = resolver_ejercicio(ej)
    out = [f"### {ej['id']} · Problema {ej['numero']} (pág. {ej['pagina']}){' ✍️' if corregido else ''}", ""]
    out.append(f"**Enunciado.** {ej['planteo']}")
    out.append("")
    if ej["incisos"] and ej["incisos"][0]["letra"] != "única":
        for i in ej["incisos"]:
            out.append(f"- **{i['letra']})** {i['texto']}")
        out.append("")
    elif ej["incisos"] and ej["incisos"][0]["texto"] not in ej["planteo"]:
        out.append(f"*{ej['incisos'][0]['texto']}*")
        out.append("")
    for tb in ej.get("tablas") or []:
        out.append(_tabla_md(tb))
        out.append("")
    out.append(f"*Tema detectado por la app: {TEMAS.get(an.tema, an.tema)}.*")
    if corregido:
        out.append("*✍️ La interpretación automática se corrigió a mano (`datos/correcciones_interpretacion.json`).*")
    out.append("")
    for inc, res, guia_inc, nums in emparejar(ej, an, resultados):
        marca, faltan = estado_inciso(guia_inc, res, nums)
        resumen[marca] = resumen.get(marca, 0) + 1
        titulo = f"#### {inc.letra}) {TIPOS.get(inc.tipo, inc.tipo)} {marca}" if inc.letra != "única" else \
            f"#### Resolución ({TIPOS.get(inc.tipo, inc.tipo)}) {marca}"
        out.append(titulo)
        out.append("")
        if inc.que_pide:
            out.append(f"*Qué pide:* {inc.que_pide}")
            out.append("")
        for e in res.errores:
            out.append(f"> ❌ {e}")
        for a in res.avisos:
            out.append(f"> ⚠️ {a}")
        if res.errores or res.avisos:
            out.append("")
        for p in res.pasos:
            if "\n|" in p:
                texto, _, tabla = p.partition("\n\n")
                out.append(f"- {texto}")
                out.append("")
                out.append(tabla)
                out.append("")
            else:
                out.append(f"- {p}")
        if res.conclusion:
            out.append("")
            out.append(f"**Conclusión:** {res.conclusion}")
        out.append("")
        if guia_inc.get("respuesta"):
            out.append(f"**Respuesta de la guía:** {guia_inc['respuesta']}")
            out.append("")
        if marca == "⚠️":
            discrepancias.append((ej["id"], inc.letra, guia_inc.get("respuesta", ""), faltan,
                                  res.resumen or (res.errores[0] if res.errores else ""),
                                  ej.get("observaciones", "")))
            out.append(f"> ⚠️ **No coincide con la guía**" + (f" (no aparecen: {', '.join(fmt(v, 6) for v in faltan)})"
                                                              if faltan else "") + ". Ver la lista de discrepancias.")
            out.append("")
    if ej.get("observaciones"):
        out.append(f"> 📝 *Notas de la transcripción:* {ej['observaciones']}")
        out.append("")
    if ej.get("conclusiones"):
        out.append("<details><summary>Cómo lo concluye la guía</summary>\n")
        for c in ej["conclusiones"]:
            out.append(f"> {c}")
        out.append("\n</details>")
        out.append("")
    out.append("---")
    out.append("")
    return out


def main():
    filtros = [a for a in sys.argv[1:] if not a.startswith("-")]
    sel = [e for e in GUIA if not filtros or e["id"] in filtros or e["tema"] in filtros]
    discrepancias, resumen = [], {}
    cuerpo = []
    tema_actual = None
    for ej in sel:
        if ej["tema"] != tema_actual:
            tema_actual = ej["tema"]
            cuerpo += [f"## TEMA {tema_actual} — {NOMBRES_TEMA[tema_actual]}", ""]
        cuerpo += md_ejercicio(ej, discrepancias, resumen)
    cab = ["# Guía de Problemas de Estadística Aplicada 2026 — resuelta", "",
           "Generado con `python herramientas/generar_resueltos.py` a partir de `datos/guia_ejercicios.json` "
           "(transcripción verificada contra el PDF) y el intérprete + solver de la app. Cada inciso muestra los pasos "
           "en el orden de la cátedra, la conclusión, la respuesta de la guía y si coinciden.", "",
           f"**Resumen:** ✅ {resumen.get('✅', 0)} incisos coinciden · ⚠️ {resumen.get('⚠️', 0)} no coinciden · "
           f"ℹ️ {resumen.get('ℹ️', 0)} sin valores para comparar.", "",
           "Índice: " + " · ".join(f"[Tema {t}](#tema-{t.lower()}--{NOMBRES_TEMA[t].lower().replace(' ', '-').replace('/', '').replace('(', '').replace(')', '')})"
                                   for t in dict.fromkeys(e["tema"] for e in sel)), ""]
    pie = ["## Discrepancias con la guía", "",
           "Incisos donde lo calculado no coincide con la respuesta de la guía. Puede ser un error de la guía, "
           "un criterio distinto, o un error de interpretación de la app: hay que revisarlos uno por uno.", "",
           "| Ejercicio | Inciso | Respuesta de la guía | Valores que no aparecen | La app da | Notas |",
           "|---|---|---|---|---|---|"]
    for eid, letra, resp, faltan, app, obs in discrepancias:
        limpio = lambda s: (s or "").replace("|", "/").replace("\n", " ")[:220]
        pie.append(f"| {eid} | {letra} | {limpio(resp)} | {', '.join(fmt(v, 6) for v in faltan)} | {limpio(app)} | {limpio(obs)} |")
    texto = "\n".join(cab + cuerpo + pie) + "\n"
    if filtros:
        sys.stdout.reconfigure(encoding="utf-8")
        print(texto)
    else:
        SALIDA.write_text(texto, encoding="utf-8")
        print(f"Escrito {SALIDA.name}: {len(sel)} ejercicios; ✅ {resumen.get('✅', 0)} ⚠️ {resumen.get('⚠️', 0)} "
              f"ℹ️ {resumen.get('ℹ️', 0)}")


if __name__ == "__main__":
    main()
