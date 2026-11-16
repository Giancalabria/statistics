"""Sección «Teoría» de la app: los .md del repo que sirven para resolver un examen, para leer y buscar.

Cada documento es una página (se arman en app.py con `paginas()`). La página parte el documento por sus títulos
principales, cada parte en un desplegable, y tiene un buscador que deja solo las partes que tienen todas las
palabras buscadas (sin importar tildes ni mayúsculas).
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import streamlit as st

from interprete.texto import normalizar

RAIZ = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Documento:
    archivo: str          # relativo a la raíz del repo
    titulo: str
    icono: str
    descripcion: str
    desde: Optional[str] = None    # título desde el que empieza lo útil (se saltea el encabezado)


DOCUMENTOS = (
    Documento("estudio/GUIA_CONTROL.md", "Control del planteo", "✅",
              "Qué controlar de la app en cada inciso, cómo se reconoce cada tema y las fallas reales de la app."),
    Documento("estudio/REGLAS_PROFESOR.md", "Reglas del profesor", "📏",
              "Lo que Dopazo exige y penaliza, por tema (sale de las grabaciones de clase)."),
    Documento("estudio/TEORIA.md", "Teoría del 2° parcial", "💡",
              "Qué representa cada letra, la lógica del ensayo y los temas III a VII, con preguntas de control."),
    Documento("estudio/EJERCICIOS_EXPLICADOS.md", "Ejercicios explicados", "🧭",
              "Un ejercicio por tema (III a VII) paso a paso: qué se hace, por qué y de dónde sale cada número."),
    Documento("esquema_teorico_examen_estadistica.md", "Fórmulas y esquema teórico", "📐",
              "Fórmulas, distribuciones y casos de cada tema (intervalos, ensayos, dos poblaciones, χ², regresión)."),
    Documento("Guía Definitiva de Planteo y Redacción para Exámenes de Estadística Aplicada.md",
              "Planteo y redacción", "✍️",
              "Cómo plantear y redactar: variable, H0/H1 pesimista u optimista, pasos del ensayo, cierre."),
    Documento("ESTILO_CATEDRA.md", "Ejemplos resueltos en clase", "🧑‍🏫",
              "Criterios de redacción y los ejercicios que el profesor resolvió en clase, escritos como él los pide.",
              desde="## 1."),
    Documento("CONVENCIONES_CATEDRA.md", "Convenciones de la cátedra", "📌",
              "Redondeos y convenciones que aplica la app, y las diferencias conocidas con la guía."),
    Documento("Resolucion Problemas - Sistema Productivo y Faena de Conejos.md", "Problemas de examen resueltos",
              "📝", "Dos problemas de examen resueltos completos con todos los pasos (temas I y II)."),
)

_LINK_LOCAL = re.compile(r"\[([^\]]+)\]\((?!https?://)[^)]+\)")   # [REGLAS_PROFESOR.md](REGLAS_PROFESOR.md)


def _limpiar(texto: str) -> str:
    """Los links a otros .md no andan dentro de la app: queda el nombre en negrita."""
    return _LINK_LOCAL.sub(r"**\1**", texto)


def _nivel(texto: str) -> Optional[int]:
    """El nivel de título más alto que se repite (2 a 4), o None."""
    return next((n for n in (2, 3, 4) if len(re.findall(rf"^{'#' * n} ", texto, flags=re.M)) >= 2), None)


def secciones(texto: str) -> Tuple[str, List[Tuple[str, str]]]:
    """Parte por el nivel de título más alto que se repite (##, ### o ####).

    Devuelve (introducción, [(título, cuerpo), ...]); los títulos de nivel 1 sueltos quedan en la introducción.
    """
    nivel = _nivel(texto)
    if not nivel:
        return texto, []
    marca = "#" * nivel + " "
    partes = re.split(rf"\n(?={marca})", "\n" + texto)
    intro = partes[0] if not partes[0].lstrip().startswith(marca) else ""
    salida = []
    for parte in partes[1 if intro or not partes[0].strip() else 0:]:
        if not parte.lstrip().startswith(marca):
            continue
        titulo, _, cuerpo = parte.lstrip().partition("\n")
        salida.append((titulo[nivel + 1:].strip().replace("\\", ""), cuerpo.strip()))
    return intro.strip(), salida


def coincide(texto: str, busqueda: str) -> bool:
    palabras = normalizar(busqueda).split()
    base = normalizar(texto)
    return all(p in base for p in palabras)


def recortar(cuerpo: str, busqueda: str) -> str:
    """Con búsqueda, de una sección larga quedan solo las subsecciones que tienen las palabras.

    Si la sección no tiene subtítulos, o las palabras están solo en su introducción, se muestra entera.
    """
    intro, partes = secciones(cuerpo)
    elegidas = [(t, c) for t, c in partes if coincide(t + "\n" + c, busqueda)]
    if not elegidas or coincide(intro, busqueda):
        return cuerpo
    nivel = _nivel(cuerpo)
    omitidas = len(partes) - len(elegidas)
    pie = f"\n\n*({omitidas} subsecciones más sin «{busqueda}»: borrá la búsqueda para verlas)*" if omitidas else ""
    return "\n\n".join(f"{'#' * nivel} {t}\n\n{c}" for t, c in elegidas) + pie


def mostrar(doc: Documento) -> None:
    st.title(f"{doc.icono} {doc.titulo}")
    st.caption(f"{doc.descripcion} · `{doc.archivo}`")
    ruta = RAIZ / doc.archivo
    if not ruta.exists():
        st.error(f"Falta `{doc.archivo}`.")
        return
    texto = _limpiar(ruta.read_text(encoding="utf-8"))
    if doc.desde and doc.desde in texto:
        texto = texto[texto.index(doc.desde):]
    intro, partes = secciones(texto)

    clave = re.sub(r"\W+", "_", doc.titulo.lower())
    c1, c2 = st.columns([3, 1])
    busqueda = c1.text_input("Buscar", "", key=f"teoria_buscar_{clave}",
                             placeholder="p. ej. apareadas, Welch, α real, amalgamar, r²")
    abrir = c2.toggle("Abrir todo", key=f"teoria_abrir_{clave}")

    if not partes:
        st.markdown(texto, unsafe_allow_html=True)
        return
    if intro and not busqueda:
        st.markdown(re.sub(r"^#{1,6} .*\n?", "", intro, count=1), unsafe_allow_html=True)
    visibles = [(t, c) for t, c in partes if not busqueda or coincide(t + "\n" + c, busqueda)]
    if busqueda:
        st.caption(f"{len(visibles)} de {len(partes)} secciones tienen «{busqueda}».")
    for titulo, cuerpo in visibles:
        with st.expander(titulo, expanded=abrir or bool(busqueda)):
            st.markdown(recortar(cuerpo, busqueda) if busqueda else cuerpo, unsafe_allow_html=True)


def paginas() -> dict:
    """{url: st.Page} de la sección Teoría, para app.py."""
    salida = {}
    for doc in DOCUMENTOS:
        url = "teoria_" + re.sub(r"\W+", "_", normalizar(doc.titulo)).strip("_")
        salida[url] = st.Page(lambda d=doc: mostrar(d), title=doc.titulo, icon=doc.icono, url_path=url)
    return salida
