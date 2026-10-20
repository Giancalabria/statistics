"""Piezas de Streamlit compartidas por las páginas que usan el asistente (estado de Ollama, configuración y
consultas en segundo plano)."""

from typing import Callable, Dict, Optional, Tuple

import streamlit as st

from . import cliente, tareas
from .tareas import Tarea


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


# ---------------------------------------------------------------------------
# Consultas en segundo plano (ver tareas.py): una por clave y por sesión
# ---------------------------------------------------------------------------

def _tareas() -> Dict[str, Tarea]:
    return st.session_state.setdefault("_tareas_ia", {})


def lanzar(clave: str, titulo: str, pagina: str, funcion: Callable, *args, **kwargs) -> Tarea:
    """Arranca `funcion(tarea, *args, **kwargs)` en segundo plano; `pagina` es el archivo de la página que la lanza."""
    t = tareas.lanzar(Tarea(titulo, pagina), funcion, *args, **kwargs)
    _tareas()[clave] = t
    return t


def en_curso(clave: str) -> bool:
    t = _tareas().get(clave)
    return t is not None and not t.terminada


def descartar(clave: str) -> None:
    """Olvida la tarea (si sigue corriendo, termina sola y su resultado no se usa)."""
    _tareas().pop(clave, None)


def recoger(clave: str) -> Optional[Tarea]:
    """La tarea terminada (y la saca de la lista), o None si no hay o todavía corre."""
    t = _tareas().get(clave)
    return _tareas().pop(clave) if t is not None and t.terminada else None


def _mostrar_texto(t: Tarea) -> None:
    if t.texto:
        st.markdown(t.texto)


@st.fragment(run_every=0.5)
def seguir(clave: str, mostrar: Callable[[Tarea], None] = _mostrar_texto) -> None:
    """Muestra la tarea mientras corre (se actualiza sola) y recarga la página cuando termina, para recogerla."""
    t = _tareas().get(clave)
    if t is None or t.terminada:
        st.rerun()
    st.caption(f"⏳ {t.etapa or 'La IA está trabajando'}… ({t.segundos():.0f} s). Podés cambiar de página: "
               "sigue en segundo plano.")
    mostrar(t)


def aviso_tareas(pagina_actual: str) -> None:
    """En la barra lateral: las consultas de otras páginas que siguen corriendo o ya terminaron."""
    if any(t.pagina != pagina_actual for t in _tareas().values()):
        with st.sidebar:
            _aviso(pagina_actual)


@st.fragment(run_every=2)
def _aviso(pagina_actual: str) -> None:
    for t in [t for t in _tareas().values() if t.pagina != pagina_actual]:
        if t.terminada:
            st.success(f"✅ {t.titulo}: {'terminó con un error' if t.error else 'lista'}.")
        else:
            st.info(f"🤖 {t.titulo}: {t.etapa or 'trabajando'}… ({t.segundos():.0f} s)")
        st.page_link(t.pagina, label="Ir a verla", icon="↩️")
