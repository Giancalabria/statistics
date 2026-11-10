"""Chat con la IA local. Un solo campo: si lo que mandás es un enunciado, la app lo resuelve por consenso (reglas + 2
lecturas de IA) y la IA lo redacta; si es una pregunta, la IA responde con los apuntes y el último ejercicio."""

import streamlit as st

from asistente import cliente
from asistente.explicar import (SISTEMA_LIBRE, enunciado_texto, leer_adjunto, numeros_sin_respaldo, parece_enunciado,
                                resolucion_texto, resolver_por_consenso, responder)
from asistente.explicar import COPIA_FIEL
from asistente.ui import configuracion, descartar, en_curso, lanzar, recoger, seguir

PAGINA = "pages/8_Asistente_IA.py"

PEDIDO_ENUNCIADO = (
    "Te pegué este enunciado y la app ya lo resolvió por consenso (te paso la resolución). Para cada inciso: en una o "
    "dos líneas por qué se eligió ese camino (distribución, H0, cola), y después la respuesta como la entregaría en "
    "el examen. Usá SOLO los números de la resolución: no recalcules ni agregues valores. Si un inciso no tiene "
    "consenso o quedó sin calcular, decilo al principio de ese inciso. " + COPIA_FIEL + "\n\n")

st.title("🤖 Asistente (IA local)")
st.caption("Pegá un **enunciado** y la app lo resuelve (🗳️ consenso: reglas + 2 lecturas de IA); hacé una "
           "**pregunta** y te responde con los apuntes. Los números, siempre del recuadro «Resolución de la app».")

ia_ok, modelo, _ = configuracion(opciones=False)
if not ia_ok:
    st.warning("La IA local no está disponible. Pasos (una sola vez, con internet):")
    st.code(f"brew install ollama          # o el instalador de https://ollama.com\n"
            f"ollama pull {cliente.MODELO}\n"
            f"ollama serve                 # si no quedó abierto como app", language="bash")
    st.write("Detalles en `ASISTENTE_IA.md`.")
    st.stop()

ss = st.session_state
ss.setdefault("chat_ia", [])            # [{"role", "content", "fuentes", "dudosos", "resolucion", "consenso"}]
ss.setdefault("chat_ejercicio", "")     # último ejercicio resuelto (desde el chat o desde «Interpretar»)

if ss["chat_ia"] and st.button("🗑 Nueva conversación"):
    ss["chat_ia"], ss["chat_ejercicio"] = [], ""
    descartar("chat")
    st.rerun()


def mostrar_resolucion(m, abierta):
    if m.get("consenso"):
        st.markdown("\n".join(f"- **{l})** {marca}" + (f" · {res}" if res else "") for l, marca, res in m["consenso"]))
    with st.expander("🧮 Resolución de la app (de acá salen los números)", expanded=abierta):
        st.markdown(m["resolucion"])


def mostrar_extra(m, abierta=False):
    if m.get("aviso"):
        st.caption("ℹ️ " + m["aviso"])
    if m.get("dudosos"):
        st.caption("⚠️ Números que no salen de la app, los apuntes ni lo que pegaste (no los copies): "
                   + ", ".join(m["dudosos"]))
    if m.get("fuentes"):
        with st.expander("Fuentes consultadas"):
            for f in m["fuentes"]:
                st.markdown(f"**{f.cita()}**")
                st.caption(f.texto[:600] + ("…" if len(f.texto) > 600 else ""))


def responder_chat(t, mensaje, adjuntos, historial, ejercicio_previo, modelo):
    """Corre en segundo plano (sin Streamlit): -> (mensaje de la IA, ejercicio que queda en la conversación)."""
    m = {"role": "assistant"}
    pregunta, ejercicio = mensaje, ejercicio_previo
    if parece_enunciado(mensaje):
        t.etapa = "Resolviendo por consenso: reglas + 2 lecturas de IA (~1 min)"
        an, resultados, ejercicio_nuevo, filas = resolver_por_consenso(mensaje, modelo)
        if any(res for _, _, res in filas):
            m["resolucion"] = resolucion_texto(an, resultados).replace("\n- ", "\n\n- ")
            m["consenso"] = filas
            t.extra = m
            pregunta, ejercicio = PEDIDO_ENUNCIADO + mensaje, ejercicio_nuevo
        else:
            # no salió ningún inciso: no era un enunciado para resolver (o le faltan datos), se responde como pregunta
            m["aviso"] = ("La app no pudo resolver ningún inciso: lo tomé como una pregunta. Si era un enunciado, "
                          "cargalo en «Interpretar un enunciado» para ver qué dato falta.")
    t.etapa = "Escribiendo la respuesta"
    trozos, frags = responder(pregunta, historial, ejercicio, modelo=modelo, sistema=SISTEMA_LIBRE, apuntes=True,
                              adjuntos=adjuntos)
    m["content"] = t.escribir(trozos)
    m["fuentes"] = frags
    respaldo = "\n".join([mensaje, ejercicio, adjuntos] + [f.texto for f in frags] + [x["content"] for x in historial])
    m["dudosos"] = numeros_sin_respaldo(m["content"], respaldo)
    return m, ejercicio


def mostrar_parcial(t):
    if t.extra.get("resolucion"):
        mostrar_resolucion(t.extra, abierta=True)
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

ultimo = max((k for k, m in enumerate(ss["chat_ia"]) if m.get("resolucion")), default=None)
for k, m in enumerate(ss["chat_ia"]):
    with st.chat_message(m["role"]):
        if m.get("resolucion"):
            mostrar_resolucion(m, abierta=(k == ultimo))
        st.markdown(m["content"])
        for nombre in m.get("archivos", []):
            st.caption(f"📎 {nombre}")
        mostrar_extra(m)

pensando = en_curso("chat")
if pensando:
    with st.chat_message("assistant"):
        seguir("chat", mostrar_parcial)

envio = st.chat_input("La IA está respondiendo…" if pensando else
                      "Pegá un enunciado completo (con incisos y tabla) o preguntá lo que quieras · 📎 para adjuntar "
                      "material o tu resolución",
                      disabled=pensando, accept_file="multiple", file_type=["txt", "md", "csv", "json", "pdf"])
if envio and (envio.text.strip() or envio.files):
    archivos = list(envio.files or [])
    adjuntos = "\n\n".join(f"[Archivo {a.name}]\n{leer_adjunto(a.name, a.getvalue())}" for a in archivos)[:24000]
    mensaje = envio.text.strip() or "Leé el material que te adjunto y decime qué tiene."
    # el ejercicio que se está trabajando en «Interpretar un enunciado», si no hay uno del chat
    ejercicio = ss["chat_ejercicio"]
    if not ejercicio and ss.get("resultados"):
        an5, res5 = ss["resultados"]
        ejercicio = "ENUNCIADO:\n" + enunciado_texto(an5) + "\n\nRESOLUCIÓN:\n" + resolucion_texto(an5, res5)
    historial = [{"role": m["role"], "content": m["content"]} for m in ss["chat_ia"]]
    ss["chat_ia"].append({"role": "user", "content": mensaje, "archivos": [a.name for a in archivos]})
    lanzar("chat", "Chat", PAGINA, responder_chat, mensaje, adjuntos, historial, ejercicio, modelo)
    st.rerun()
