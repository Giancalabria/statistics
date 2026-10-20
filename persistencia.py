"""Conserva lo que cargaste en cada página cuando te vas a otra y volvés.

Streamlit borra el valor de un widget cuando deja de mostrarse (por ejemplo, al cambiar de página), salvo que se cree
con `persist_state="session"`. `activar()` hace que ése sea el comportamiento por defecto de todos los widgets de
entrada que tienen `key` (sin key no hay dónde guardarlo), así no hay que repetirlo en cada uno. Se llama una vez por
corrida desde app.py.
"""

import functools
import inspect

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

WIDGETS = ("text_input", "text_area", "number_input", "selectbox", "radio", "toggle", "checkbox", "slider",
           "select_slider", "multiselect", "pills", "segmented_control", "date_input", "time_input", "color_picker")


def _persistente(funcion):
    @functools.wraps(funcion)
    def envuelta(*args, **kwargs):
        if kwargs.get("key") is not None:
            kwargs.setdefault("persist_state", "session")
        return funcion(*args, **kwargs)

    envuelta._persistente = True
    return envuelta


def activar() -> None:
    for nombre in WIDGETS:
        metodo = getattr(DeltaGenerator, nombre, None)
        if metodo is None or getattr(metodo, "_persistente", False):
            continue
        if "persist_state" not in inspect.signature(metodo).parameters:
            continue                    # Streamlit viejo: queda como siempre
        setattr(DeltaGenerator, nombre, _persistente(metodo))     # c1.text_input(...), st.sidebar.toggle(...)
        setattr(st, nombre, _persistente(getattr(st, nombre)))    # st.text_input(...)
