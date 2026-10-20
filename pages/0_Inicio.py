"""Inicio: qué hace cada módulo y el manual de resolución paso a paso."""


import re
from pathlib import Path

import streamlit as st

GUIA = Path(__file__).resolve().parent.parent / "tutorial_guia_app_estadistica.md"

# Etiquetas cortas para las pestañas (se busca por prefijo del título de nivel 1).
ETIQUETAS = {
    "METODOLOGÍA": "⭐ Metodología",
    "MÓDULO I:": "I · Media (μ)",
    "MÓDULO II:": "II · Varianza (σ²)",
    "MÓDULO III:": "III · Proporción (p)",
    "MATRIZ": "Matriz α / β",
    "TABLA MASTER": "Tabla master",
}


def cargar_secciones(texto: str):
    """Parte la guía en secciones de nivel 1 (`# ...`), descartando el índice.

    Devuelve una lista de (titulo, cuerpo).
    """
    bloques = re.split(r"\n(?=# )", texto)
    secciones = []
    for bloque in bloques:
        if not bloque.startswith("# "):
            continue
        titulo, _, cuerpo = bloque.partition("\n")
        if "ÍNDICE DE MÓDULOS" in cuerpo:
            continue  # encabezado + índice del documento
        secciones.append((titulo[2:].strip(), cuerpo.strip()))
    return secciones


def etiqueta(titulo: str) -> str:
    for prefijo, corta in ETIQUETAS.items():
        if titulo.startswith(prefijo):
            return corta
    return titulo[:24]


def render_seccion(cuerpo: str):
    """Muestra cada subsección (`## ...`) en un expander plegable."""
    partes = re.split(r"\n(?=## )", cuerpo)
    intro = partes[0] if not partes[0].startswith("## ") else None
    if intro and intro.replace("-", "").strip():
        st.markdown(intro, unsafe_allow_html=True)
    for parte in partes:
        if not parte.startswith("## "):
            continue
        subtitulo, _, texto = parte.partition("\n")
        with st.expander(subtitulo[3:].strip(), expanded=False):
            st.markdown(texto.strip(), unsafe_allow_html=True)


st.title("Solver de Estadística Aplicada")
st.write(
    "Elegí un módulo en la barra lateral izquierda. Cada módulo pregunta lo que sabés "
    "del problema (no la fórmula a usar) y arma el camino correcto siguiendo el árbol "
    "de decisión de `esquema_teorico_examen_estadistica.md`."
)

st.markdown(
    """
- **Intervalos de Confianza**: media, varianza/desvío, proporción — IC y tamaño de muestra.
- **Ensayo de Hipótesis (1 población)**: media (Z y t), varianza (χ²), proporción (binomial exacto) — decisión, β/potencia y n para potencia fijada.
- **Comparación de 2 poblaciones**: test F (varianzas), pooled/Welch automático (medias, muestras independientes), muestras apareadas.
- **Contrastes chi-cuadrado**: ajuste a un modelo (Normal, Poisson, Weibull, Gumbel, Pareto, Log-Normal... con las Fe
  calculadas y clases amalgamadas), bondad de ajuste con Fe dadas, tablas de contingencia.
- **Regresión**: recta, validación, intervalos (β1, ρ, pronóstico promedio / individual), modelos linealizables,
  modelo lineal general y selección de modelos (DET, Cp, R² ajustado, PRESS).
- **Guía resuelta**: los 142 ejercicios de la guía resueltos paso a paso, con la respuesta de la guía al lado.
- **Interpretar un enunciado**: pegás el problema tal cual y te dice qué pide cada inciso, qué datos hay, cómo
  presentarlo y ejercicios parecidos de la guía; después corregís lo que haga falta y calcula todo.
- **Asistente IA (opcional, sin internet)**: con Ollama abierto, la IA completa lo que las reglas no entienden,
  explica la resolución y responde dudas de teoría con los apuntes. Los números los calcula siempre el solver
  (ver `ASISTENTE_IA.md`).
"""
)

st.divider()
st.header("📚 Manual y tutorial de resolución paso a paso")

if not GUIA.exists():
    st.error(f"No se encontró la guía en `{GUIA.name}`.")
else:
    secciones = cargar_secciones(GUIA.read_text(encoding="utf-8"))
    tabs = st.tabs([etiqueta(titulo) for titulo, _ in secciones])
    for tab, (titulo, cuerpo) in zip(tabs, secciones):
        with tab:
            st.subheader(titulo)
            render_seccion(cuerpo)
