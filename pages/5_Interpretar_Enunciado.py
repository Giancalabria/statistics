"""Interpretar un enunciado: pegás el problema, la app dice qué pide, lo corregís y calcula todo."""

import copy
from dataclasses import replace

import pandas as pd
import streamlit as st

from asistente import cliente as ia_cliente
from asistente.explicar import explicar, numeros_sin_respaldo
from asistente.redactar import Control, controlar, corregir, problemas, redactar
from asistente.interpretar import interpretar, pedir_ia
from asistente.comparar import comparar, corregir as corregir_comparacion
from asistente.revisar import aplicar_sugerencias, revisar
from asistente.ui import configuracion as config_ia
from interprete import buscador, glosario
from interprete.analizador import analizar, cambiar_criterio, separar_incisos
from interprete.editor import a_texto, de_texto
from interprete.tablas import buscar_tablas, desde_texto_editado, a_texto as tabla_a_texto
from interprete.modelo import (CAMPOS_INCISO, CAMPOS_PLANTEO, COLAS, TEMAS, TIPOS, TIPOS_POR_TEMA, Analisis,
                               Inciso)
from interprete.resolver import resolver

st.title("Interpretar un enunciado")
st.write(
    "Pegá el planteo y agregá los incisos. **Interpretar** te dice qué pide cada parte, qué datos encontró "
    "y cómo presentarlo. Revisá y corregí lo que haga falta, y después **Calcular** resuelve todo con el solver."
)
st.caption("Funciona sin internet: son reglas armadas con el estilo de la Guía de Problemas, así que revisá "
           "siempre los datos detectados antes de calcular. Si tenés la IA local (Ollama) abierta, interviene "
           "donde las reglas no entienden; los números los calcula siempre el solver.")
ia_ok, ia_modelo, ia_pensar = config_ia()

ss = st.session_state
ss.setdefault("incisos", [""])
ss.setdefault("ver", 0)          # versión del análisis (renueva las claves de los widgets)
ss.setdefault("analisis", None)
ss.setdefault("resultados", None)
ss.setdefault("ia_info", None)
ss.setdefault("revision", None)
ss.setdefault("ia_explicacion", None)
if "tabla_txt_nueva" in ss:
    ss["tabla_txt"] = ss.pop("tabla_txt_nueva")


# ---------------------------------------------------------------------------
# 1) Enunciado
# ---------------------------------------------------------------------------

st.subheader("1 · Enunciado")
if "planteo_nuevo" in ss:  # viene de 'Separar incisos' (hay que setearlo antes de crear el widget)
    ss["planteo"] = ss.pop("planteo_nuevo")
planteo = st.text_area("Planteo (el texto inicial del problema)", key="planteo", height=150,
                       placeholder="Ej.: Una máquina llenadora de latas de café dosifica cantidades variables con "
                                   "distribución Normal de desvío estándar 15 gramos...")

if st.button("✂️ Separar incisos del texto pegado", help="Si pegaste el enunciado completo con a), b), c)... "
                                                        "los pasa a los campos de incisos."):
    plant, incs = separar_incisos(ss.get("planteo", ""), parrafos=True)
    if incs:
        ss["planteo_nuevo"] = plant
        ss["incisos"] = [tx for _, tx in incs]
        for k in list(ss.keys()):
            if str(k).startswith("inc_txt_"):
                del ss[k]
        st.rerun()
    else:
        st.info("No encontré incisos en el texto (ni letras a), b), c)... ni párrafos con preguntas).")

st.markdown("**Incisos**")
for i in range(len(ss["incisos"])):
    c1, c2 = st.columns([12, 1])
    letra = chr(ord("a") + i)
    ss["incisos"][i] = c1.text_input(f"{letra})", value=ss["incisos"][i], key=f"inc_txt_{i}_{len(ss['incisos'])}",
                                     label_visibility="visible")
    if c2.button("🗑", key=f"inc_del_{i}", help="Quitar este inciso") and len(ss["incisos"]) > 1:
        ss["incisos"].pop(i)
        st.rerun()
if st.button("➕ Agregar inciso"):
    ss["incisos"].append("")
    st.rerun()
st.caption("Si el problema no tiene incisos dejalos vacíos: la pregunta se toma del planteo.")

with st.expander("📋 Tabla de datos (regresión, frecuencias por clase, contingencia, muestras apareadas)",
                 expanded=bool(ss.get("tabla_txt"))):
    st.text_area("Pegá la tabla: primer renglón con los encabezados y una fila por renglón (separá con | ; o tab). "
                 "Si la dejás vacía, se busca la tabla dentro del planteo.", key="tabla_txt", height=150,
                 placeholder="Área sembrada (en 10^6 ha) | PBI (en millones de U$s)\n3,0402 | 8,014\n2,9819 | 7,891")
    if st.button("Buscar la tabla en el planteo"):
        encontradas = buscar_tablas(ss.get("planteo", ""))
        if encontradas:
            ss["tabla_txt_nueva"] = tabla_a_texto(encontradas[0])
            st.rerun()
        else:
            st.info("No encontré una tabla en el planteo.")

MODOS = {
    "comparar": "⚖️ Reglas y IA por separado, y se comparan (recomendado)",
    "revision": "🛡️ Solver + revisión IA",
    "solver": "🔍 Solo solver (reglas)",
    "hibrido": "🧩 Solver, y la IA completa lo que no entiende",
    "ia": "🤖 La IA arma el planteo, el solver calcula",
}
AYUDA_MODOS = {
    "comparar": "Las reglas resuelven al instante y, por separado, la IA lee el enunciado y razona el planteo en "
                "palabras (como un alumno). Se comparan los RESULTADOS de los dos: si coinciden, ✅; si no, ves los dos "
                "planteos lado a lado y elegís, o le explicás a la IA qué leyó mal. Las reglas aciertan más en los "
                "ejercicios de estructura conocida y la IA en las redacciones retorcidas. Tarda ~1-2 min.",
    "revision": "Las reglas arman el planteo y el solver calcula. Después la IA lo audita: busca números del enunciado "
                "que no se usaron, lo lee por su cuenta sin ver el de las reglas y, donde no coinciden, decide con una "
                "cita textual del enunciado. Si al planteo le falta algo para resolverse, lo completa (🛠️); si el planteo ya se "
                "resuelve, NO lo pisa: te sugiere el cambio (💡) y lo aplicás vos con un clic. Lo dudoso queda ⚠️. "
                "Tarda ~30 s.",
    "solver": "Solo las reglas (verificadas contra la guía). Instantáneo y sin IA.",
    "hibrido": "Las reglas primero; la IA solo interviene si algún inciso no se puede resolver.",
    "ia": "La IA lee el enunciado y arma el planteo sin las reglas; los números los calcula el solver. Sirve para "
          "comparar: en la guía rinde menos que las reglas.",
}
opciones_modo = list(MODOS) if ia_ok else ["solver"]
if ss.get("modo_interpretar") not in opciones_modo:
    ss["modo_interpretar"] = opciones_modo[0]
modo = st.radio("Cómo interpretar", opciones_modo, format_func=MODOS.get, key="modo_interpretar", horizontal=True,
                help="\n\n".join(f"**{MODOS[m]}**: {AYUDA_MODOS[m]}" for m in opciones_modo))
st.caption(AYUDA_MODOS[modo] + ("" if ia_ok else " (Para usar la IA abrí Ollama con un modelo descargado.)"))
if st.button("🔍 Interpretar", type="primary"):
    if not ss.get("planteo", "").strip():
        st.error("Escribí el planteo.")
    else:
        tabla = desde_texto_editado(ss.get("tabla_txt", "")) if ss.get("tabla_txt", "").strip() else None
        incisos_txt = [tx for tx in ss["incisos"] if tx.strip()]
        tablas_in = [tabla] if tabla else None
        ss["ia_info"] = ss["revision"] = ss["comparacion"] = None
        if modo == "comparar":
            with st.spinner("Resolviendo con las reglas y leyendo el enunciado con la IA (~1-2 min)…"):
                ss["comparacion"] = comparar(ss["planteo"], incisos_txt, tablas=tablas_in, modelo=ia_modelo)
            ss["analisis"] = ss["comparacion"].reglas
        elif modo == "revision":
            with st.spinner("Resolviendo con las reglas y revisando con la IA (~30 s)…"):
                rv = revisar(ss["planteo"], incisos_txt, tablas=tablas_in, modelo=ia_modelo, pensar=ia_pensar)
            ss["analisis"], ss["revision"] = rv.analisis, rv
        elif modo in ("hibrido", "ia"):
            with st.spinner("Interpretando con la IA (puede tardar)…"):
                if modo == "hibrido":
                    r = interpretar(ss["planteo"], incisos_txt, tablas=tablas_in, modelo=ia_modelo, pensar=ia_pensar)
                    ss["analisis"] = r.analisis
                    ss["ia_info"] = r if (r.usado_ia or r.error) else None
                else:
                    try:
                        ss["analisis"], avisos = pedir_ia(ss["planteo"], incisos_txt, tablas_in, ia_modelo, ia_pensar)
                        ss["analisis"].avisos += [f"🤖 IA: {a}" for a in avisos]
                    except ia_cliente.ErrorIA as e:
                        st.error(f"🤖 No se pudo consultar a la IA: {e}. Se usan las reglas.")
                        ss["analisis"] = analizar(ss["planteo"], incisos_txt, tablas=tablas_in)
        else:
            ss["analisis"] = analizar(ss["planteo"], incisos_txt, tablas=tablas_in)
        ss["resultados"] = None
        ss["ia_explicacion"] = None
        ss["cambios_criterio"] = None
        ss["ver"] += 1

an: Analisis = ss["analisis"]
if an is None:
    st.stop()
V = ss["ver"]

# ---------------------------------------------------------------------------
# 2) Qué es y qué pide
# ---------------------------------------------------------------------------

st.divider()
st.subheader("2 · Qué te piden")

temas = list(TEMAS)
tema = st.selectbox("Tema detectado", temas, index=temas.index(an.tema), format_func=lambda k: TEMAS[k],
                    key=f"v{V}_tema")
for r in an.razones_tema:
    st.caption("↳ " + r)
if an.criterio:
    criterios = ["optimista", "pesimista"]
    elegido = st.radio("Criterio para plantear H0", criterios, index=criterios.index(an.criterio), horizontal=True,
                       format_func=str.upper, key=f"v{V}_criterio",
                       help="Si lo cambiás se invierte el planteo: H0 pasa a ser la otra condición (en un diseño se "
                            "intercambian μ₀↔μ₁ y α↔β) y las colas unilaterales se dan vuelta. Cambialo antes de "
                            "corregir datos, porque se vuelven a cargar.")
    st.caption("↳ " + an.criterio_razon)
    if elegido != an.criterio:
        nuevo_an = copy.deepcopy(an)
        ss["cambios_criterio"] = cambiar_criterio(nuevo_an, elegido)
        ss["analisis"], ss["resultados"] = nuevo_an, None
        ss["ver"] += 1
        st.rerun()
    if ss.get("cambios_criterio"):
        st.info("**Al cambiar el criterio:**\n" + "\n".join(f"- {c}" for c in ss["cambios_criterio"]))
for a in an.avisos:
    if a.startswith("🛠️"):
        continue                                    # las correcciones de la revisión se muestran abajo, juntas
    (st.info if a.startswith("🤖") else st.warning)(a)
comp = ss.get("comparacion")
if comp:
    if comp.error:
        st.error(f"⚖️ No se pudo consultar a la IA: {comp.error}. Quedan las reglas.")
    elif comp.coinciden:
        st.success(f"⚖️ ✅ La IA leyó el enunciado por su cuenta y llega a los mismos resultados que las reglas "
                   f"({comp.segundos:.0f} s).")
    else:
        estados = [i.estado for i in comp.incisos]
        if "distinto" in estados:
            st.warning(f"⚖️ Las reglas y la IA **llegan a resultados distintos** en {estados.count('distinto')} de "
                       f"{len(estados)} inciso(s) ({comp.segundos:.0f} s). Mirá los dos planteos y decidí cuál es el "
                       "correcto.")
        if "solo_ia" in estados:
            st.warning(f"⚖️ En {estados.count('solo_ia')} inciso(s) las reglas no pudieron y **la IA sí**: revisá su "
                       "planteo y, si está bien, usalo.")
        if "solo_reglas" in estados and "distinto" not in estados and "solo_ia" not in estados:
            st.info(f"⚖️ La IA no pudo armar un planteo completo ({comp.segundos:.0f} s); quedan las reglas. Igual "
                    "controlá el planteo, o explicale a la IA qué no entendió.")
    if comp.incisos:
        marca = {"coincide": "✅ iguales", "distinto": "❌ distintos", "solo_ia": "🤖 solo la IA",
                 "solo_reglas": "📐 solo las reglas", "ninguno": "— ninguno"}
        st.dataframe(pd.DataFrame([{"Inciso": i.letra, "": marca[i.estado], "📐 Reglas": i.reglas, "🤖 IA": i.ia}
                                   for i in comp.incisos]), hide_index=True, width="stretch")
    if comp.ia is not None:
        with st.expander("🤖 Cómo lo planteó la IA (en palabras)", expanded=not comp.coinciden):
            st.markdown(comp.ia.razonamiento)
        usa_ia = an is comp.ia.analisis
        c1, c2 = st.columns(2)
        if c1.button("📐 Usar el planteo de las reglas", disabled=not usa_ia, key=f"v{V}_usar_reglas"):
            ss["analisis"], ss["resultados"] = comp.reglas, None
            ss["ver"] += 1
            st.rerun()
        if c2.button("🤖 Usar el planteo de la IA", disabled=usa_ia, key=f"v{V}_usar_ia"):
            ss["analisis"], ss["resultados"] = comp.ia.analisis, None
            ss["ver"] += 1
            st.rerun()
        st.caption("Ahora se usa el planteo de " + ("**la IA**." if usa_ia else "**las reglas**.")
                   + " Igual podés corregir cualquier dato abajo, a mano.")
        nota = st.text_area("💬 Corregile a la IA (qué leyó mal)", key=f"v{V}_nota_ia",
                            placeholder="Ej.: el 1.237,5 es el peso TOTAL de los 25 paquetes, no la media.")
        if st.button("Rehacer el planteo de la IA con mi corrección", disabled=not nota.strip(), key=f"v{V}_corregir"):
            tabla = desde_texto_editado(ss.get("tabla_txt", "")) if ss.get("tabla_txt", "").strip() else None
            with st.spinner("La IA está rehaciendo el planteo…"):
                ss["comparacion"] = corregir_comparacion(comp, nota, ss["planteo"],
                                                         [tx for tx in ss["incisos"] if tx.strip()],
                                                         [tabla] if tabla else None, ia_modelo)
            if ss["comparacion"].ia is not None and not ss["comparacion"].error:
                ss["analisis"] = ss["comparacion"].ia.analisis       # la corregiste: se pasa a su planteo
            ss["resultados"] = None
            ss["ver"] += 1
            st.rerun()
rv = ss.get("revision")
if rv:
    if rv.error:
        st.error(f"🛡️ {rv.veredicto}")
    elif rv.corregidos or rv.sugeridos or rv.a_revisar:
        st.warning(f"🛡️ {rv.veredicto} ({rv.segundos:.0f} s)")
    else:
        st.success(f"🛡️ {rv.veredicto} ({rv.segundos:.0f} s)")
    for i in rv.corregidos:
        lugar = "Planteo" if i.donde == "planteo" else f"Inciso {i.donde})"
        st.info(f"🛠️ **{lugar} · {i.que}**: {i.detalle}" + (f"\n\n> «{i.cita}»" if i.cita else ""))
    if rv.sugeridos:
        st.markdown("**💡 La IA leyó distinto y sugiere estos cambios** (el planteo de las reglas ya se resolvía, así "
                    "que no se aplicaron solos). Leé la cita y marcá los que correspondan:")
        marcados = []
        for k, i in enumerate(rv.sugeridos):
            lugar = "Planteo" if i.donde == "planteo" else f"Inciso {i.donde})"
            if st.checkbox(f"{lugar} · {i.que}: {i.detalle}", key=f"v{V}_sug{k}",
                           help=f"«{i.cita}»" if i.cita else None):
                marcados.append(i)
            if i.cita:
                st.caption(f"> «{i.cita}»")
        if st.button("Aplicar los marcados", disabled=not marcados, key=f"v{V}_aplicar_sug"):
            tabla = desde_texto_editado(ss.get("tabla_txt", "")) if ss.get("tabla_txt", "").strip() else None
            ss["analisis"] = aplicar_sugerencias(rv, marcados, ss["planteo"], [tx for tx in ss["incisos"] if tx.strip()],
                                                 [tabla] if tabla else None)
            rv.analisis = ss["analisis"]
            rv.items = [i for i in rv.items if i not in marcados] + [replace(i, estado="corregido") for i in marcados]
            ss["resultados"] = None
            ss["ver"] += 1
            st.rerun()
    for i in rv.a_revisar:
        lugar = "Planteo" if i.donde == "planteo" else f"Inciso {i.donde})"
        st.warning(f"⚠️ **{lugar} · {i.que}**: {i.detalle}" + (f"\n\n> «{i.cita}»" if i.cita else ""))
    confirmados = [i for i in rv.items if i.estado == "confirmado"]
    if confirmados:
        with st.expander(f"✅ Lo que la revisión confirmó ({len(confirmados)})"):
            for i in confirmados:
                st.markdown(f"- {'Planteo' if i.donde == 'planteo' else 'Inciso ' + i.donde + ')'} · {i.que}: "
                            f"{i.detalle}")
info = ss.get("ia_info")
if info:
    if info.error:
        st.error(f"🤖 No se pudo consultar a la IA: {info.error}")
    elif not info.informe:
        st.caption(f"🤖 La IA revisó el enunciado ({info.segundos:.0f} s) y no hizo falta cambiar nada.")
    if info.sugerencias or info.avisos_ia:
        with st.expander(f"🤖 La IA leyó distinto ({len(info.sugerencias)} diferencias, no aplicadas: revisalas)",
                         expanded=bool(info.sugerencias)):
            for x in info.sugerencias:
                st.markdown(f"- {x}")
            for x in info.avisos_ia:
                st.caption("↳ " + x)

frases = glosario.buscar_frases(an.planteo + " " + " ".join(i.texto for i in an.incisos))
if frases:
    with st.expander(f"📖 Pistas de lectura ({len(frases)} frases típicas encontradas)", expanded=True):
        for frase, significado in frases:
            st.markdown(f"- *{frase}* → {significado}")

# ---------------------------------------------------------------------------
# 3) Datos (editables)
# ---------------------------------------------------------------------------

st.subheader("3 · Datos del planteo (corregí lo que esté mal)")
evid = {e.clave: e for e in an.evidencias}
claves = [k for k in an.datos if k in CAMPOS_PLANTEO] + [k for k in ss.get(f"v{V}_extra", []) if k not in an.datos]
nuevos = {}
for clave in claves:
    etiqueta, tipo = CAMPOS_PLANTEO[clave]
    valor = an.datos.get(clave)
    key = f"v{V}_d_{clave}"
    cols = st.columns([4, 6])
    if tipo == "bool":
        nuevos[clave] = cols[0].checkbox(etiqueta, value=bool(valor), key=key)
    elif tipo in ("lista", "tabla"):
        nuevos[clave] = cols[0].text_area(etiqueta, value=a_texto(valor, tipo), key=key,
                                          help="Separá los valores con ';' o espacios" +
                                               (" y las filas con Enter." if tipo == "tabla" else "."))
    else:
        nuevos[clave] = cols[0].text_input(etiqueta, value=a_texto(valor, tipo), key=key)
    e = evid.get(clave)
    if e:
        cols[1].caption(f"**{e.motivo}**" + (f"  \n“{e.fragmento}”" if e.fragmento else ""))

c1, c2 = st.columns([4, 2])
faltantes = [k for k in CAMPOS_PLANTEO if k not in claves]
agregar = c1.selectbox("Agregar un dato que no detectó", [""] + faltantes, format_func=lambda k: CAMPOS_PLANTEO[k][0] if k else "—",
                       key=f"v{V}_agregar")
if c2.button("Agregar dato") and agregar:
    ss.setdefault(f"v{V}_extra", []).append(agregar)
    st.rerun()

# ---------------------------------------------------------------------------
# 4) Incisos
# ---------------------------------------------------------------------------

st.subheader("4 · Cada inciso")
editados = []
for k, inc in enumerate(an.incisos):
    with st.expander(f"**{inc.letra})** {inc.texto[:110]}{'…' if len(inc.texto) > 110 else ''}", expanded=True):
        st.markdown(f"🎯 **Qué te pide:** {inc.que_pide}")
        for r in inc.razones:
            st.caption("↳ " + r)
        if inc.params.get("tema") and inc.params["tema"] != tema:
            st.info(f"Este inciso se resuelve como **{TEMAS[inc.params['tema']]}** (distinto del tema del planteo).")
        opciones = TIPOS_POR_TEMA.get(inc.params.get("tema") or tema, list(TIPOS))
        if inc.tipo not in opciones:
            opciones = opciones + [inc.tipo]
        tipo = st.selectbox("Tipo de pregunta", opciones, index=opciones.index(inc.tipo),
                            format_func=lambda t: TIPOS[t], key=f"v{V}_i{k}_tipo")
        params = {}
        claves_p = [c for c in inc.params if c in CAMPOS_INCISO]
        if tipo in ("ensayo", "beta", "diseno", "curva") and "tail" not in claves_p:
            claves_p.append("tail")
        cols = st.columns(3)
        for j, c in enumerate(claves_p):
            etiqueta, t = CAMPOS_INCISO[c]
            key = f"v{V}_i{k}_{c}"
            col = cols[j % 3]
            if t == "cola":
                colas = list(COLAS)
                actual = inc.params.get("tail", "bilateral")
                params[c] = col.selectbox(etiqueta, colas, index=colas.index(actual) if actual in colas else 2,
                                          format_func=lambda x: COLAS[x], key=key)
            elif t == "prob":
                params[c] = col.radio(etiqueta, ["beta", "potencia"], index=0 if inc.params.get(c) == "beta" else 1,
                                      format_func=lambda x: "β (no detectar)" if x == "beta" else "1-β (detectar)",
                                      key=key, horizontal=True)
            elif t == "bool":
                params[c] = col.checkbox(etiqueta, value=bool(inc.params.get(c)), key=key)
            else:
                params[c] = col.text_input(etiqueta, value=a_texto(inc.params.get(c), t), key=key)
        extra_p = st.multiselect("Agregar parámetros a este inciso", [c for c in CAMPOS_INCISO if c not in claves_p],
                                 format_func=lambda c: CAMPOS_INCISO[c][0], key=f"v{V}_i{k}_extra")
        for c in extra_p:
            etiqueta, t = CAMPOS_INCISO[c]
            if t == "cola":
                params[c] = st.selectbox(etiqueta, list(COLAS), format_func=lambda x: COLAS[x], key=f"v{V}_i{k}_{c}")
            elif t == "prob":
                params[c] = st.radio(etiqueta, ["beta", "potencia"], key=f"v{V}_i{k}_{c}", horizontal=True)
            elif t == "bool":
                params[c] = st.checkbox(etiqueta, key=f"v{V}_i{k}_{c}")
            else:
                params[c] = st.text_input(etiqueta, key=f"v{V}_i{k}_{c}")
        pasos = glosario.COMO_PRESENTAR.get(tipo)
        if pasos:
            st.markdown("🧾 **Cómo presentarlo:**\n" + "\n".join(f"{n + 1}. {p}" for n, p in enumerate(pasos)))
        editados.append((inc, tipo, params))

# ---------------------------------------------------------------------------
# 5) Ejercicios parecidos de la guía
# ---------------------------------------------------------------------------

st.subheader("5 · Ejercicios parecidos de la guía")
solo_parcial = st.checkbox("Solo los que entraban en el primer parcial", value=False, key="solo_parcial")
parecidos = buscador.buscar(an.planteo + " " + " ".join(i.texto for i in an.incisos), k=4, tema=tema,
                            solo_parcial=solo_parcial)
if not parecidos:
    st.caption("No se encontró `datos/guia_ejercicios.json` (correr `python herramientas/extraer_guia.py`).")
for sim, ej in parecidos:
    marca = " · ✅ resuelto en la guía" if ej["resuelto"] else ""
    with st.expander(f"Tema {ej['tema']} – Problema {ej['numero']} (pág. {ej['pagina']}) · similitud "
                     f"{sim:.0%}{marca}"):
        st.markdown(ej["enunciado"])
        if ej["respuesta"]:
            st.markdown(f"**Respuesta de la guía:** {ej['respuesta']}")
        if ej["conclusiones"]:
            st.markdown("**Cómo lo concluye la guía:**")
            for c in ej["conclusiones"][:6]:
                st.markdown(f"> {c}")

# ---------------------------------------------------------------------------
# 6) Calcular
# ---------------------------------------------------------------------------

st.divider()


def construir():
    errores = []
    datos = {}
    for clave, crudo in nuevos.items():
        tipo = CAMPOS_PLANTEO[clave][1]
        if tipo == "bool":
            datos[clave] = crudo
            continue
        try:
            v = de_texto(crudo, tipo)
        except ValueError as e:
            errores.append(f"{CAMPOS_PLANTEO[clave][0]}: {e}")
            continue
        if v is not None:
            datos[clave] = v
    incisos = []
    for inc, tipo, params in editados:
        p = {}
        for c, crudo in params.items():
            t = CAMPOS_INCISO[c][1]
            if t in ("cola", "prob", "bool"):
                p[c] = crudo
                continue
            try:
                v = de_texto(crudo, t)
            except ValueError as e:
                errores.append(f"{inc.letra}) {CAMPOS_INCISO[c][0]}: {e}")
                continue
            if v is not None:
                p[c] = v
        # parámetros internos que no se editan (p. ej. usar S, curva combinada, cota unilateral)
        for c, v in inc.params.items():
            if c not in CAMPOS_INCISO and c not in p:
                p[c] = v
        incisos.append(Inciso(letra=inc.letra, texto=inc.texto, tipo=tipo, params=p))
    for c, v in an.datos.items():          # datos internos sin campo editable
        if c not in CAMPOS_PLANTEO and c not in datos:
            datos[c] = v
    nuevo = Analisis(planteo=an.planteo, tema=tema, datos=datos, incisos=incisos, criterio=an.criterio)
    return nuevo, errores


if st.button("🧮 Calcular", type="primary"):
    nuevo, errores = construir()
    for e in errores:
        st.error(e)
    ss["resultados"] = (nuevo, resolver(nuevo))
    ss["ia_explicacion"] = None

if ss.get("resultados"):
    nuevo, resultados = ss["resultados"]
    st.subheader("Resolución")
    for inc, res in zip(nuevo.incisos, resultados):
        st.markdown(f"### {res.titulo}")
        for e in res.errores:
            st.error(e)
        for a in res.avisos:
            st.warning(a)
        for p in res.pasos:
            if "\n|" in p:  # paso con una tabla: la tabla va fuera de la viñeta
                texto, _, tabla_md = p.partition("\n\n")
                st.markdown("- " + texto)
                st.markdown(tabla_md)
            else:
                st.markdown("- " + p)
        if res.conclusion:
            st.success(("**7 · Conclusión formal:** " if inc.tipo == "ensayo" else "**Conclusión:** ") + res.conclusion)
        if res.tabla:
            df = pd.DataFrame(res.tabla)
            st.dataframe(df, hide_index=True)
            x = df.columns[0]
            if any("β" in c for c in df.columns):
                st.line_chart(df.set_index(x))

# ---------------------------------------------------------------------------
# 7) Explicación con la IA local
# ---------------------------------------------------------------------------

if ss.get("resultados") and ia_ok:
    st.divider()
    st.subheader("🤖 Redacción y explicación de la IA")
    st.caption("La IA explica y redacta la resolución de arriba; no calcula. Los números que no salgan del "
               "enunciado ni de la resolución se marcan para que los revises.")
    pedido = st.text_input("Pedido (opcional)", key="ia_pedido",
                           placeholder="Ej.: explicame por qué es cola izquierda / redactá solo la conclusión del b)")
    c_red, c_exp = st.columns(2)
    if c_red.button("📝 Redactar como en el examen", type="primary",
                    help="La resolución completa con el estilo de la cátedra (ESTILO_CATEDRA.md): variable con su "
                         "unidad, 7 pasos, CR y RD, expresión formal de los intervalos. Los números son los del "
                         "solver; al final se pasa el checklist."):
        nuevo, resultados = ss["resultados"]
        try:
            trozos, fuentes = redactar(nuevo, resultados, pedido, modelo=ia_modelo, pensar=ia_pensar)
            caja = st.empty()
            texto = caja.write_stream(trozos)
            controles = controlar(texto, nuevo, fuentes, resultados)
            fallan = problemas(controles)
            if fallan:
                caja.empty()
                st.info("🔁 La redacción no cumple el checklist (" + "; ".join(fallan) + "): corrigiendo…")
                texto2 = st.write_stream(corregir(nuevo, resultados, texto, fallan, pedido, ia_modelo, ia_pensar))
                controles2 = controlar(texto2, nuevo, fuentes, resultados)
                if len(problemas(controles2)) < len(fallan):
                    texto, controles = texto2, controles2
            ss["ia_explicacion"] = (texto, controles, False)
            st.rerun()
        except ia_cliente.ErrorIA as e:
            st.error(str(e))
    if c_exp.button("💬 Explicar con IA", help="Explica por qué se eligió cada camino (distribución, hipótesis, "
                                               "cola)."):
        nuevo, resultados = ss["resultados"]
        try:
            trozos, fuentes = explicar(nuevo, resultados, pedido, modelo=ia_modelo, pensar=ia_pensar)
            texto = st.write_stream(trozos)
            ss["ia_explicacion"] = (texto, numeros_sin_respaldo(texto, fuentes), True)
        except ia_cliente.ErrorIA as e:
            st.error(str(e))
    if ss.get("ia_explicacion"):
        texto, dudosos, recien = ss["ia_explicacion"]
        if not recien:
            st.markdown(texto)
        ss["ia_explicacion"] = (texto, dudosos, False)
        if dudosos and isinstance(dudosos[0], Control):
            fallas = [c for c in dudosos if not c.ok]
            with st.expander(f"📋 Checklist de la cátedra: {len(dudosos) - len(fallas)}/{len(dudosos)} ✔",
                             expanded=bool(fallas)):
                for c in dudosos:
                    st.markdown(f"{'✅' if c.ok else '⚠️'} {c.texto}")
            st.caption("El estilo sale de ESTILO_CATEDRA.md: agregale ejemplos o frases del profesor y la próxima "
                       "redacción ya los usa.")
        elif dudosos:
            st.warning("⚠️ Estos números de la explicación no aparecen en el enunciado ni en la resolución del "
                       "solver (pueden ser cuentas inventadas): " + ", ".join(dudosos))
        else:
            st.caption("✔ Todos los números de la explicación salen del enunciado o de la resolución.")
