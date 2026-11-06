"""Punto de entrada: arma la navegación entre páginas y lo que vale para todas.

Corre en cada interacción, sea cual sea la página, así que acá se activa que los widgets conserven lo cargado al
cambiar de página y el aviso de las consultas a la IA que siguen corriendo en otra.
"""

import streamlit as st

import persistencia
from asistente.ui import aviso_tareas

st.set_page_config(page_title="Solver de Estadística Aplicada", layout="wide")
persistencia.activar()

# sección -> {archivo: (título, ícono)}; la primera página es la que abre la app
SECCIONES = {
    "Examen": {
        "pages/5_Interpretar_Enunciado.py": ("Interpretar un enunciado", "🧭"),
        "pages/8_Asistente_IA.py": ("Asistente IA", "🤖"),
    },
    "Resolver a mano, por tema": {
        "pages/1_Intervalos_de_Confianza.py": ("Intervalos de confianza", None),
        "pages/2_Ensayo_de_Hipotesis.py": ("Ensayo de hipótesis", None),
        "pages/3_Comparacion_2_Poblaciones.py": ("Comparación de 2 poblaciones", None),
        "pages/4_Chi_Cuadrado.py": ("Chi cuadrado", None),
        "pages/6_Regresion.py": ("Regresión", None),
    },
    "Estudio": {
        "pages/7_Guia_Resuelta.py": ("Guía resuelta", "📗"),
        "pages/0_Inicio.py": ("Manual (temas I–III)", "📚"),
    },
}
paginas = {}
for seccion in SECCIONES.values():
    for ruta, (titulo, icono) in seccion.items():
        paginas[ruta] = st.Page(ruta, title=titulo, icon=icono, default=not paginas)
actual = st.navigation({nombre: [paginas[r] for r in seccion] for nombre, seccion in SECCIONES.items()})
aviso_tareas(next(ruta for ruta, p in paginas.items() if p.url_path == actual.url_path))
actual.run()
