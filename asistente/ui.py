"""Piezas de Streamlit compartidas por las páginas que usan el asistente (estado de Ollama y configuración)."""

from typing import Optional, Tuple

import streamlit as st

from . import cliente


@st.cache_data(ttl=20, show_spinner=False)
def _estado() -> Tuple[bool, list]:
    if not cliente.disponible():
        return False, []
    try:
        return True, cliente.modelos()
    except cliente.ErrorIA:
        return True, []


def configuracion() -> Tuple[bool, Optional[str], bool]:
    """Barra lateral: estado de la IA local, modelo y modo razonamiento. Devuelve (lista, modelo, pensar)."""
    ok, instalados = _estado()
    with st.sidebar:
        st.markdown("### 🤖 IA local")
        if not ok:
            st.caption(f"Ollama no está corriendo en {cliente.HOST}. La app funciona igual sin IA "
                       "(ver `ASISTENTE_IA.md`).")
            if st.button("Reintentar", key="ia_reintentar"):
                _estado.clear()
                st.rerun()
            return False, None, False
        if not instalados:
            st.caption(f"Ollama está abierto pero no hay modelos. Descargá uno: `ollama pull {cliente.MODELO}`")
            return False, None, False
        preferido = next((m for m in instalados if cliente.modelo_instalado(cliente.MODELO, [m])), instalados[0])
        modelo = st.selectbox("Modelo", instalados, index=instalados.index(preferido), key="ia_modelo")
        pensar = st.toggle("Razonar antes de responder", value=False, key="ia_pensar",
                           help="Qwen3 / DeepSeek-R1: más preciso en enunciados enredados, pero tarda bastante más.")
        st.caption("Sin internet: todo corre en esta computadora.")
        return True, modelo, pensar
