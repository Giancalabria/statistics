"""Que no se pierda lo hecho al cambiar de página: los widgets conservan su valor y la IA sigue en segundo plano.

Las páginas se prueban con el AppTest de Streamlit (sin navegador) y la IA con un stream falso.
"""

import threading
import time
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from asistente.tareas import Tarea, lanzar

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def abrir_app():
    """Como el navegador: la primera corrida es la del punto de entrada (si no, AppTest corre la página suelta)."""
    return AppTest.from_file(APP, default_timeout=30).run()


def esperar(tarea, segundos=5):
    limite = time.time() + segundos
    while not tarea.terminada and time.time() < limite:
        time.sleep(0.01)
    assert tarea.terminada


def test_tarea_acumula_el_stream_y_devuelve_el_resultado():
    seguir = threading.Event()

    def trabajo(t, palabras):
        t.etapa = "Escribiendo"
        def trozos():
            yield palabras[0]
            seguir.wait(5)              # a mitad de camino: lo generado ya se ve en t.texto
            yield from palabras[1:]
        return t.escribir(trozos()).upper()

    t = lanzar(Tarea("Chat", "pages/8_Asistente_IA.py"), trabajo, ["hola ", "che"])
    limite = time.time() + 5
    while t.texto != "hola " and time.time() < limite:
        time.sleep(0.01)
    assert (t.texto, t.etapa, t.terminada) == ("hola ", "Escribiendo", False)
    seguir.set()
    esperar(t)
    assert (t.texto, t.resultado, t.error) == ("hola che", "HOLA CHE", None)


def test_tarea_guarda_el_error():
    def falla(t):
        raise ValueError("se cayó Ollama")

    t = lanzar(Tarea("Chat", "x.py"), falla)
    esperar(t)
    assert isinstance(t.error, ValueError) and t.resultado is None


@pytest.mark.parametrize("pagina, clave, valor", [
    ("pages/1_Intervalos_de_Confianza.py", "ic_nivel_confianza_1", 0.9),
    ("pages/2_Ensayo_de_Hipotesis.py", "eh_nivel_significacion", 0.01),
    ("pages/4_Chi_Cuadrado.py", "chi_nivel_significacion_alpha", 0.1),
])
def test_el_valor_cargado_sobrevive_al_cambio_de_pagina(pagina, clave, valor):
    at = abrir_app()
    at.switch_page(pagina).run()
    at.number_input(key=clave).set_value(valor).run()
    at.switch_page("pages/7_Guia_Resuelta.py").run()
    at.switch_page(pagina).run()
    assert not at.exception
    assert at.number_input(key=clave).value == valor


def test_texto_del_enunciado_sobrevive_al_cambio_de_pagina():
    at = abrir_app()
    at.switch_page("pages/5_Interpretar_Enunciado.py").run()
    at.text_area(key="planteo").input("Una máquina llenadora de latas...").run()
    at.switch_page("pages/0_Inicio.py").run()
    at.switch_page("pages/5_Interpretar_Enunciado.py").run()
    assert at.text_area(key="planteo").value == "Una máquina llenadora de latas..."


@pytest.fixture
def ollama_lento(monkeypatch):
    """Una IA falsa que responde de a trozos y se queda esperando a mitad de la respuesta hasta que el test la suelta."""
    from asistente import cliente
    from asistente.ui import _estado
    soltar = threading.Event()

    def chat(mensajes, stream=False, **kwargs):
        def trozos():
            yield "La media "
            soltar.wait(10)
            yield "es μ."
        return trozos() if stream else "{}"

    monkeypatch.setattr(cliente, "disponible", lambda timeout=2: True)
    monkeypatch.setattr(cliente, "modelos", lambda timeout=5: [cliente.MODELO])
    monkeypatch.setattr(cliente, "chat", chat)
    _estado.clear()
    yield soltar
    soltar.set()
    _estado.clear()


def textos(at):
    return [m.value for m in at.markdown] + [c.value for c in at.caption]


def test_el_chat_sigue_respondiendo_si_cambias_de_pagina(ollama_lento):
    at = abrir_app()
    at.switch_page("pages/8_Asistente_IA.py").run()
    at.chat_input[0].set_value("¿Qué es la media?").run()
    tarea = at.session_state["_tareas_ia"]["chat"]
    limite = time.time() + 5
    while tarea.texto != "La media " and time.time() < limite:
        time.sleep(0.01)

    at.switch_page("pages/1_Intervalos_de_Confianza.py").run()       # se va mientras la IA escribe
    assert not tarea.terminada
    at.switch_page("pages/8_Asistente_IA.py").run()
    assert "La media" in textos(at)                                  # al volver ve lo que lleva
    assert at.chat_input[0].disabled

    ollama_lento.set()
    esperar(tarea)
    at.run()
    assert [m["content"] for m in at.session_state["chat_ia"]] == ["¿Qué es la media?", "La media es μ."]
    assert "_tareas_ia" not in at.session_state or not at.session_state["_tareas_ia"]
    assert not at.exception
