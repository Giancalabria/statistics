"""Chat libre con la IA local: dudas, revisar lo que escribiste, material propio o resolver un ejercicio entero."""

import streamlit as st

from asistente import cliente, contexto
from asistente.explicar import (SISTEMA_LIBRE, SISTEMA_PREGUNTA, enunciado_texto, leer_adjunto,
                                numeros_sin_respaldo, resolucion_texto, resolver_enunciado, responder)
from asistente.ui import configuracion, descartar, en_curso, lanzar, recoger, seguir

PAGINA = "pages/8_Asistente_IA.py"

st.title("🤖 Asistente (IA local)")
st.write("Chat libre: preguntale lo que quieras, pasale tu material (archivos o texto) o pegale un ejercicio "
         "entero para que la app lo resuelva y la IA te lo explique.")
st.caption("Corre en esta computadora, sin internet. Para los números confiá en la app: con «Resolver con la app» "
           "las cuentas las hace el solver; lo que calcule la IA por su cuenta puede estar mal.")

ia_ok, modelo, pensar = configuracion()
if not ia_ok:
    st.warning("La IA local no está disponible. Pasos (una sola vez, con internet):")
    st.code(f"brew install ollama          # o el instalador de https://ollama.com\n"
            f"ollama pull {cliente.MODELO}\n"
            f"ollama serve                 # si no quedó abierto como app", language="bash")
    st.write("Detalles en `ASISTENTE_IA.md`.")
    st.stop()

ss = st.session_state
ss.setdefault("chat_ia", [])            # [{"role", "content", "fuentes", "dudosos", "resolucion"}]
ss.setdefault("chat_ejercicio", "")     # último ejercicio resuelto desde el chat

PRESETS = {"Libre": SISTEMA_LIBRE, "Responder con los apuntes": SISTEMA_PREGUNTA, "Personalizado": ""}

with st.expander("⚙️ Opciones del chat", expanded=False):
    preset = st.radio("Estilo", list(PRESETS), horizontal=True, key="chat_preset",
                      help="Libre: conversa de cualquier cosa y puede resolver. Apuntes: respuestas cortas basadas "
                           "en los apuntes del repo. Personalizado: escribís vos las instrucciones.")
    if ss.get("chat_preset_previo") != preset:
        ss["chat_sistema"] = PRESETS[preset] or ss.get("chat_sistema", SISTEMA_LIBRE)
        ss["chat_preset_previo"] = preset
    sistema = st.text_area("Instrucciones para la IA (podés editarlas)", key="chat_sistema", height=130)
    c1, c2 = st.columns(2)
    usar_apuntes = c1.toggle("Buscar en los apuntes del repo", value=True, key="chat_apuntes",
                             help="Agrega a cada pregunta los fragmentos más parecidos de las convenciones, el "
                                  "esquema teórico, la guía de redacción y la guía resuelta.")
    mantener = c2.toggle("Recordar el último ejercicio resuelto", value=True, key="chat_mantener")
    ejercicio_pag5 = ""
    if ss.get("resultados"):
        an5, res5 = ss["resultados"]
        if st.checkbox("Incluir el ejercicio de «Interpretar un enunciado»", value=True, help=an5.planteo[:200],
                       key="chat_incluir_ejercicio_interpretar"):
            ejercicio_pag5 = "ENUNCIADO:\n" + enunciado_texto(an5) + "\n\nRESOLUCIÓN:\n" + resolucion_texto(an5, res5)
    archivos = st.file_uploader("Material propio (txt, md, csv, json, pdf)", accept_multiple_files=True,
                                type=["txt", "md", "csv", "json", "pdf"], key="chat_archivos")
    extra = st.text_area("Texto extra para la IA (apuntes, tu resolución para que la revise, una tabla...)",
                         key="chat_extra", height=100)

adjuntos = "\n\n".join([f"[Archivo {a.name}]\n{leer_adjunto(a.name, a.getvalue())}" for a in archivos or []]
                       + ([f"[Texto del alumno]\n{extra}"] if extra.strip() else []))
if len(adjuntos) > 24000:
    st.caption(f"⚠️ El material tiene {len(adjuntos):,} caracteres: se usan los primeros 24.000.")

c1, c2, c3 = st.columns([3, 3, 1])
resolver_msg = c1.toggle("🧮 Resolver mi mensaje con la app", key="chat_resolver",
                         help="Tu próximo mensaje se toma como un ENUNCIADO: lo interpreta (reglas + IA), lo calcula el "
                              "solver y la IA te explica la resolución.")
if ss["chat_ejercicio"] and mantener:
    c2.caption("📌 Hay un ejercicio resuelto en la conversación.")
if c3.button("🗑 Limpiar"):
    ss["chat_ia"], ss["chat_ejercicio"] = [], ""
    descartar("chat")
    st.rerun()


def mostrar_resolucion(resolucion, informe):
    with st.expander("🧮 Resolución de la app (solver)"):
        st.markdown(resolucion)
        for x in informe:
            st.caption("🤖 " + x)


def mostrar_extra(m):
    if m.get("resolucion"):
        mostrar_resolucion(m["resolucion"], m.get("informe", []))
    if m.get("dudosos"):
        st.caption("⚠️ Números que no salen de la app, los apuntes ni el material (verificalos): "
                   + ", ".join(m["dudosos"]))
    if m.get("fuentes"):
        with st.expander("Fuentes consultadas"):
            for f in m["fuentes"]:
                st.markdown(f"**{f.cita()}**")
                st.caption(f.texto[:600] + ("…" if len(f.texto) > 600 else ""))


def responder_chat(t, mensaje, historial, resolver_msg, ejercicio_pag5, ejercicio_chat, mantener, modelo, pensar,
                   sistema, usar_apuntes, adjuntos):
    """Corre en segundo plano (sin Streamlit): -> (mensaje de la IA, ejercicio resuelto en el chat)."""
    m = {"role": "assistant"}
    pregunta = mensaje
    if resolver_msg:
        t.etapa = "Resolviendo con la app"
        r, resultados, ejercicio_chat = resolver_enunciado(mensaje, modelo, pensar)
        m["resolucion"] = resolucion_texto(r.analisis, resultados).replace("\n- ", "\n\n- ")
        m["informe"] = r.informe
        t.extra = m
        pregunta = ("Te pegué este enunciado y la app ya lo resolvió (te paso la resolución). Explicámelo "
                    "inciso por inciso y escribí la respuesta como la pondría en el examen. Si algún inciso "
                    "quedó con error o sin calcular, decime qué falta.\n\n" + mensaje)
    t.etapa = "Escribiendo la respuesta"
    ejercicio = "\n\n".join(x for x in (ejercicio_pag5, ejercicio_chat if mantener else "") if x)
    trozos, frags = responder(pregunta, historial, ejercicio, modelo=modelo, pensar=pensar,
                              sistema=sistema, apuntes=usar_apuntes, adjuntos=adjuntos)
    m["content"] = t.escribir(trozos)
    m["fuentes"] = frags
    respaldo = "\n".join([mensaje, ejercicio, adjuntos] + [f.texto for f in frags] + [x["content"] for x in historial])
    m["dudosos"] = numeros_sin_respaldo(m["content"], respaldo)
    return m, ejercicio_chat


def mostrar_parcial(t):
    if t.extra.get("resolucion"):
        mostrar_resolucion(t.extra["resolucion"], t.extra.get("informe", []))
    if t.texto:
        st.markdown(t.texto)


terminada = recoger("chat")
if terminada and isinstance(terminada.error, cliente.ErrorIA):
    st.error(str(terminada.error))
elif terminada and terminada.error:
    st.exception(terminada.error)
elif terminada:
    m, ss["chat_ejercicio"] = terminada.resultado
    ss["chat_ia"].append(m)

for m in ss["chat_ia"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        mostrar_extra(m)

pensando = en_curso("chat")
if pensando:
    with st.chat_message("assistant"):
        seguir("chat", mostrar_parcial)

placeholder = ("Pegá el enunciado completo (con sus incisos)" if resolver_msg else
               "Preguntá lo que quieras: «¿por qué acá es t y no Z?», «revisá mi conclusión», «explicame el β»…")
mensaje = st.chat_input("La IA está respondiendo…" if pensando else placeholder, disabled=pensando)
if mensaje:
    historial = [{"role": m["role"], "content": m["content"]} for m in ss["chat_ia"]]
    ss["chat_ia"].append({"role": "user", "content": mensaje})
    lanzar("chat", "Chat", PAGINA, responder_chat, mensaje, historial, resolver_msg, ejercicio_pag5,
           ss["chat_ejercicio"], mantener, modelo, pensar, sistema, usar_apuntes, adjuntos)
    st.rerun()
