"""Interpretar un enunciado: pegás el problema, la app dice qué pide, lo corregís y calcula todo."""

import copy

import pandas as pd
import streamlit as st

from interprete import buscador, glosario
from interprete.analizador import analizar, cambiar_criterio, separar_incisos
from interprete.editor import a_texto, de_texto
from interprete.modelo import (CAMPOS_INCISO, CAMPOS_PLANTEO, COLAS, TEMAS, TIPOS, TIPOS_POR_TEMA, Analisis,
                               Inciso)
from interprete.resolver import resolver

st.title("Interpretar un enunciado")
st.write(
    "Pegá el planteo y agregá los incisos. **Interpretar** te dice qué pide cada parte, qué datos encontró "
    "y cómo presentarlo. Revisá y corregí lo que haga falta, y después **Calcular** resuelve todo con el solver."
)
st.caption("Funciona sin internet: son reglas armadas con el estilo de la Guía de Problemas, así que revisá "
           "siempre los datos detectados antes de calcular.")

ss = st.session_state
ss.setdefault("incisos", [""])
ss.setdefault("ver", 0)          # versión del análisis (renueva las claves de los widgets)
ss.setdefault("analisis", None)
ss.setdefault("resultados", None)

TEMAS_PARCIAL = {"media", "varianza", "proporcion"}

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
    plant, incs = separar_incisos(ss.get("planteo", ""))
    if incs:
        ss["planteo_nuevo"] = plant
        ss["incisos"] = [tx for _, tx in incs]
        for k in list(ss.keys()):
            if str(k).startswith("inc_txt_"):
                del ss[k]
        st.rerun()
    else:
        st.info("No encontré incisos a), b), c)... en el texto.")

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

if st.button("🔍 Interpretar", type="primary"):
    if not ss.get("planteo", "").strip():
        st.error("Escribí el planteo.")
    else:
        ss["analisis"] = analizar(ss["planteo"], [tx for tx in ss["incisos"] if tx.strip()])
        ss["resultados"] = None
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
if tema not in TEMAS_PARCIAL:
    st.info("Este tema no entra en el primer parcial (se calcula igual si la app lo soporta).")
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
    st.warning(a)

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
        opciones = TIPOS_POR_TEMA.get(tema, list(TIPOS))
        if inc.tipo not in opciones:
            opciones = opciones + [inc.tipo]
        tipo = st.selectbox("Tipo de pregunta", opciones, index=opciones.index(inc.tipo),
                            format_func=lambda t: TIPOS[t], key=f"v{V}_i{k}_tipo")
        if tema not in TEMAS_PARCIAL or (tema == "proporcion" and tipo in ("ensayo", "beta", "diseno", "curva")):
            st.caption("ℹ️ Esta parte no entra en el primer parcial.")
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
solo_parcial = st.checkbox("Solo los que entran en el primer parcial", value=True, key="solo_parcial")
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
            st.markdown("- " + p)
        if res.conclusion:
            st.success("**Conclusión:** " + res.conclusion)
        if res.tabla:
            df = pd.DataFrame(res.tabla)
            st.dataframe(df, hide_index=True)
            x = df.columns[0]
            if any("β" in c for c in df.columns):
                st.line_chart(df.set_index(x))
