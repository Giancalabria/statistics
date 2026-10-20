"""Punto de entrada: arma la navegación entre páginas y lo que vale para todas.

Corre en cada interacción, sea cual sea la página, así que acá se activa que los widgets conserven lo cargado al
cambiar de página y el aviso de las consultas a la IA que siguen corriendo en otra.
"""

import streamlit as st

import persistencia
from asistente.ui import aviso_tareas

st.set_page_config(page_title="Solver de Estadística Aplicada", layout="wide")
persistencia.activar()

PAGINAS = {
    "pages/0_Inicio.py": ("Inicio", "🏠"),
    "pages/1_Intervalos_de_Confianza.py": ("Intervalos de Confianza", None),
    "pages/2_Ensayo_de_Hipotesis.py": ("Ensayo de Hipótesis", None),
    "pages/3_Comparacion_2_Poblaciones.py": ("Comparación de 2 Poblaciones", None),
    "pages/4_Chi_Cuadrado.py": ("Chi Cuadrado", None),
    "pages/5_Interpretar_Enunciado.py": ("Interpretar Enunciado", None),
    "pages/6_Regresion.py": ("Regresión", None),
    "pages/7_Guia_Resuelta.py": ("Guía Resuelta", None),
    "pages/8_Asistente_IA.py": ("Asistente IA", None),
}
paginas = {ruta: st.Page(ruta, title=titulo, icon=icono, default=(i == 0))
           for i, (ruta, (titulo, icono)) in enumerate(PAGINAS.items())}
actual = st.navigation(list(paginas.values()))
aviso_tareas(next(ruta for ruta, p in paginas.items() if p.url_path == actual.url_path))
actual.run()
