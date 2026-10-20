"""La Guía de Problemas resuelta paso a paso (generada con herramientas/generar_resueltos.py)."""

import re
from pathlib import Path

import streamlit as st

ARCHIVO = Path(__file__).resolve().parent.parent / "Guia_resuelta.md"

st.title("Guía de problemas resuelta")
if not ARCHIVO.exists():
    st.error("Falta `Guia_resuelta.md`: generalo con `python herramientas/generar_resueltos.py`.")
    st.stop()

texto = ARCHIVO.read_text(encoding="utf-8")
cabecera, _, resto = texto.partition("\n## TEMA ")
cuerpo, _, discrepancias = ("## TEMA " + resto).partition("\n## Discrepancias con la guía")
temas = re.split(r"\n(?=## TEMA )", cuerpo)
st.markdown(cabecera.split("Índice:")[0])

opciones = [t.splitlines()[0][3:] for t in temas if t.strip()] + ["Discrepancias con la guía"]
elegido = st.selectbox("Tema", opciones, key="guia_tema")
if elegido == "Discrepancias con la guía":
    st.markdown("## Discrepancias con la guía" + discrepancias)
    st.stop()
bloque = temas[opciones.index(elegido)]
ejercicios = re.split(r"\n(?=### )", bloque)[1:]
buscar = st.text_input("Buscar (palabra del enunciado o número, p. ej. 'VII-8')", "",
                       key="guia_buscar_palabra_enunciado")
solo = st.checkbox("Solo los que no coinciden con la guía (⚠️)", key="guia_solo_no_coinciden")
for ej in ejercicios:
    titulo = ej.splitlines()[0][4:]
    if buscar and buscar.lower() not in ej.lower():
        continue
    if solo and "⚠️ **No coincide" not in ej:
        continue
    marca = " ⚠️" if "⚠️ **No coincide" in ej else ""
    with st.expander(titulo + marca):
        st.markdown(ej.split("\n", 1)[1].replace("<details><summary>", "**").replace("</summary>", "**")
                    .replace("</details>", ""), unsafe_allow_html=False)
