"""Interpretar un enunciado: pegás el problema, la app lo lee (reglas + 2 lecturas de IA, se vota), lo controlás,
lo corregís si hace falta y el solver calcula."""

import copy

import pandas as pd
import streamlit as st

from asistente import cliente as ia_cliente
from asistente.consenso import NOMBRES as NOMBRES_LECTURA, combinado, consenso
from asistente.explicar import explicar, numeros_sin_respaldo
from asistente.redactar import Control, controlar, corregir, problemas, redactar
from asistente.ui import configuracion as config_ia, descartar, en_curso, lanzar, recoger, seguir
from interprete import buscador, glosario
from interprete.analizador import analizar, cambiar_criterio, separar_incisos
from interprete.editor import a_texto, de_texto
from interprete.tablas import buscar_tablas, desde_texto_editado, a_texto as tabla_a_texto
from interprete.modelo import (CAMPOS_INCISO, CAMPOS_PLANTEO, COLAS, TEMAS, TIPOS, TIPOS_POR_TEMA, Analisis,
                               Inciso)
from interprete.resolver import resolver

PAGINA = "pages/5_Interpretar_Enunciado.py"
# Lo que se borra de la sesión al interpretar de nuevo.
NUEVA_INTERPRETACION = {"ia_explicacion": None, "cambios_criterio": None, "consenso": None, "consenso_elecciones": {}}


def interpretar_con_ia(t, planteo, incisos_txt, tablas_in, ia_modelo):
    """Corre en segundo plano (sin Streamlit): -> (valores nuevos de la sesión, error para mostrar o None)."""
    t.etapa = "Tres lecturas (reglas, IA con ejemplos, IA por tema) y votación (~1 min)"
    c = consenso(planteo, incisos_txt, tablas=tablas_in, modelo=ia_modelo)
    an = combinado(c) or analizar(planteo, incisos_txt, tablas=tablas_in)
    return {**NUEVA_INTERPRETACION, "consenso": c, "analisis": an, "resultados": (an, resolver(an))}, None


def redactar_ia(t, nuevo, resultados, pedido, ia_modelo):
    """Corre en segundo plano: la redacción con el estilo de la cátedra, con una vuelta de corrección si hace falta."""
    t.etapa = "Redactando como en el examen"
    trozos, fuentes = redactar(nuevo, resultados, pedido, modelo=ia_modelo)
    texto = t.escribir(trozos)
    controles = controlar(texto, nuevo, fuentes, resultados)
    fallan = problemas(controles)
    if fallan:
        t.etapa = "🔁 La redacción no cumple el checklist (" + "; ".join(fallan) + "): corrigiendo"
        texto2 = t.escribir(corregir(nuevo, resultados, texto, fallan, pedido, ia_modelo))
        controles2 = controlar(texto2, nuevo, fuentes, resultados)
        if len(problemas(controles2)) < len(fallan):
            texto, controles = texto2, controles2
    return texto, controles


def explicar_ia(t, nuevo, resultados, pedido, ia_modelo):
    """Corre en segundo plano: por qué se eligió cada camino."""
    t.etapa = "Explicando la resolución"
    trozos, fuentes = explicar(nuevo, resultados, pedido, modelo=ia_modelo)
    texto = t.escribir(trozos)
    return texto, numeros_sin_respaldo(texto, fuentes)


st.title("Interpretar un enunciado")
st.caption("Pegá el problema → **Interpretar** → controlá el planteo con `estudio/GUIA_CONTROL.md` (tema, parámetro, "
           "H0 y cola, α, datos) → si algo está mal, corregilo abajo y **Recalcular**. Los números los calcula siempre "
           "el solver; funciona sin internet.")
ia_ok, ia_modelo, _ = config_ia(opciones=False)

ss = st.session_state
ss.setdefault("incisos", [""])
ss.setdefault("ver", 0)          # versión del análisis (renueva las claves de los widgets)
ss.setdefault("analisis", None)
ss.setdefault("resultados", None)
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

interpretando = en_curso("interpretar")
c1, c2 = st.columns(2)
con_ia = c1.button("🗳️ Interpretar (reglas + IA, se vota · ~1 min)", type="primary", disabled=interpretando or not ia_ok,
                   help="Tres lecturas independientes: las reglas, la IA con ejemplos de la guía y la IA con un prompt "
                        "corto del tema. Se vota el RESULTADO de cada inciso: ✅ si dos o más coinciden; si no, ves cada "
                        "lectura y elegís. Un consenso también puede estar mal: controlalo igual.")
solo_reglas = c2.button("⚡ Solo reglas (al instante, sin IA)", disabled=interpretando,
                        type="secondary" if ia_ok else "primary")
if not ia_ok:
    st.caption("La IA local no está abierta (Ollama): se puede interpretar solo con las reglas.")
if con_ia or solo_reglas:
    if not ss.get("planteo", "").strip():
        st.error("Escribí el planteo.")
    else:
        tabla = desde_texto_editado(ss.get("tabla_txt", "")) if ss.get("tabla_txt", "").strip() else None
        incisos_txt = [tx for tx in ss["incisos"] if tx.strip()]
        tablas_in = [tabla] if tabla else None
        if solo_reglas:
            an_r = analizar(ss["planteo"], incisos_txt, tablas=tablas_in)
            ss.update({**NUEVA_INTERPRETACION, "analisis": an_r, "resultados": (an_r, resolver(an_r))})
            ss["ver"] += 1
            descartar("redaccion")
        else:
            lanzar("interpretar", "Interpretación", PAGINA, interpretar_con_ia, ss["planteo"], incisos_txt,
                   tablas_in, ia_modelo)
            descartar("redaccion")
            interpretando = True

terminada = recoger("interpretar")
if terminada and terminada.error:
    st.exception(terminada.error)
elif terminada:
    cambios, aviso = terminada.resultado
    ss.update(cambios)
    ss["ver"] += 1
    if aviso:
        st.error(aviso)
if interpretando:
    seguir("interpretar")
    st.stop()

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
        ss["analisis"], ss["resultados"] = nuevo_an, (nuevo_an, resolver(nuevo_an))
        ss["ver"] += 1
        st.rerun()
    if ss.get("cambios_criterio"):
        st.info("**Al cambiar el criterio:**\n" + "\n".join(f"- {c}" for c in ss["cambios_criterio"]))
for a in an.avisos:
    (st.info if a.startswith("🤖") else st.warning)(a)
cons = ss.get("consenso")
if cons:
    marca = {"consenso": "✅ consenso", "ia_vs_reglas": "⚠️ las 2 IA contra las reglas", "sin_consenso": "⚠️ sin consenso",
             "una_sola": "☝️ una sola lectura", "ninguna": "— ninguna"}
    n_ok = sum(i.estado == "consenso" for i in cons.incisos)
    (st.success if cons.todos_de_acuerdo else st.warning)(
        f"🗳️ {n_ok} de {len(cons.incisos)} inciso(s) con consenso ({cons.segundos:.0f} s)."
        + ("" if cons.todos_de_acuerdo else " En los marcados ⚠️/☝️ mirá las lecturas y elegí."))
    errores = [f"{NOMBRES_LECTURA[l.fuente]}: {l.error}" for l in cons.lecturas if l.error]
    for e in errores:
        st.error(f"🗳️ {e}")
    filas = []
    for i in cons.incisos:
        fila = {"Inciso": i.letra, "": marca[i.estado],
                "Elegido": NOMBRES_LECTURA[i.elegido.fuente] if i.elegido else "—"}
        for v in i.votos:
            fila[NOMBRES_LECTURA[v.fuente]] = v.resultado.resumen or "; ".join(v.resultado.errores) or "no se resolvió"
        filas.append(fila)
    st.dataframe(pd.DataFrame(filas), hide_index=True, width="stretch")
    dudosos = [i for i in cons.incisos if i.estado != "consenso" and len(i.votos) > 1]
    elecciones = dict(ss.get("consenso_elecciones") or {})
    for i in dudosos:
        with st.expander(f"⚠️ Inciso {i.letra}): cómo lo leyó cada uno", expanded=True):
            for v in i.votos:
                resultado = v.resultado.resumen or "; ".join(v.resultado.errores) or "no se resolvió"
                st.markdown(f"**{NOMBRES_LECTURA[v.fuente]}** — {v.que_pide}"
                            + (f"\n\n`{v.hipotesis}`" if v.hipotesis else "") + f"\n\n→ {resultado}")
            opciones = [v.fuente for v in i.votos if not v.resultado.errores]
            if opciones:
                actual = elecciones.get(i.letra) or (i.elegido.fuente if i.elegido else opciones[0])
                elegida = st.radio("Usar la lectura de", opciones, index=opciones.index(actual) if actual in opciones else 0,
                                   format_func=NOMBRES_LECTURA.get, key=f"v{V}_cons_{i.letra}", horizontal=True)
                elecciones[i.letra] = elegida
    if elecciones != (ss.get("consenso_elecciones") or {}):
        ss["consenso_elecciones"] = elecciones
        ss["analisis"] = combinado(cons, elecciones)
        ss["resultados"] = (ss["analisis"], resolver(ss["analisis"]))
        ss["ver"] += 1
        st.rerun()

frases = glosario.buscar_frases(an.planteo + " " + " ".join(i.texto for i in an.incisos))
if frases:
    with st.expander(f"📖 Pistas de lectura ({len(frases)} frases típicas encontradas)"):
        for frase, significado in frases:
            st.markdown(f"- *{frase}* → {significado}")

# ---------------------------------------------------------------------------
# 3) Datos (editables)
# ---------------------------------------------------------------------------

st.subheader("3 · Datos del planteo (corregí lo que esté mal)")
evid = {e.clave: e for e in an.evidencias}
claves = [k for k in an.datos if k in CAMPOS_PLANTEO] + [k for k in ss.get(f"v{V}_extra", []) if k not in an.datos]
# paso 1 del profesor: la variable en palabras con su unidad (se muestra siempre, aunque esté vacía)
_V = ["variable", "unidad", "accion"]
SIEMPRE = {"media": _V, "varianza": _V, "dos_medias": _V, "dos_varianzas": _V, "proporcion": ["variable", "accion"],
           "chi_contingencia": ["variable"], "chi_ajuste": ["variable"],
           "regresion": ["var_y", "unidad_y", "var_x", "unidad_x"]}
claves = [k for k in SIEMPRE.get(tema, []) if k not in claves] + claves
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

with st.expander("📚 Ejercicios parecidos de la guía"):
    solo_parcial = st.checkbox("Solo los que entraban en el primer parcial", value=False, key="solo_parcial")
    parecidos = buscador.buscar(an.planteo + " " + " ".join(i.texto for i in an.incisos), k=4, tema=tema,
                                solo_parcial=solo_parcial)
    if not parecidos:
        st.caption("No se encontró `datos/guia_ejercicios.json` (correr `python herramientas/extraer_guia.py`).")
    for sim, ej in parecidos:
        marca = " · ✅ resuelto en la guía" if ej["resuelto"] else ""
        st.markdown(f"**Tema {ej['tema']} – Problema {ej['numero']}** (pág. {ej['pagina']}) · similitud "
                    f"{sim:.0%}{marca}")
        st.markdown(ej["enunciado"])
        if ej["respuesta"]:
            st.markdown(f"**Respuesta de la guía:** {ej['respuesta']}")
        if ej["conclusiones"]:
            st.markdown("**Cómo lo concluye la guía:**")
            for c in ej["conclusiones"][:6]:
                st.markdown(f"> {c}")
        st.divider()

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


if st.button("🧮 Recalcular con lo que corregí", type="primary",
             help="La resolución de abajo ya está calculada con el planteo interpretado. Si cambiaste algún dato, el "
                  "tipo o los parámetros de un inciso, recalculá."):
    nuevo, errores = construir()
    for e in errores:
        st.error(e)
    ss["resultados"] = (nuevo, resolver(nuevo))
    ss["ia_explicacion"] = None
    descartar("redaccion")              # si había una redacción en curso, era de la resolución anterior

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
    redactando = en_curso("redaccion")
    c_red, c_exp = st.columns(2)
    if c_red.button("📝 Redactar como en el examen", type="primary", disabled=redactando,
                    help="La resolución completa con el estilo de la cátedra (ESTILO_CATEDRA.md): variable con su "
                         "unidad, 7 pasos, CR y RD, expresión formal de los intervalos. Los números son los del "
                         "solver; al final se pasa el checklist."):
        nuevo, resultados = ss["resultados"]
        lanzar("redaccion", "Redacción", PAGINA, redactar_ia, nuevo, resultados, pedido, ia_modelo)
        redactando = True
    if c_exp.button("💬 Explicar con IA", disabled=redactando,
                    help="Explica por qué se eligió cada camino (distribución, hipótesis, cola)."):
        nuevo, resultados = ss["resultados"]
        lanzar("redaccion", "Explicación", PAGINA, explicar_ia, nuevo, resultados, pedido, ia_modelo)
        redactando = True
    terminada = recoger("redaccion")
    if terminada and isinstance(terminada.error, ia_cliente.ErrorIA):
        st.error(str(terminada.error))
    elif terminada and terminada.error:
        st.exception(terminada.error)
    elif terminada:
        ss["ia_explicacion"] = terminada.resultado
    if redactando:
        seguir("redaccion")
    elif ss.get("ia_explicacion"):
        texto, dudosos = ss["ia_explicacion"]
        st.markdown(texto)
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
