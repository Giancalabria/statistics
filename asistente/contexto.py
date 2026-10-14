"""Búsqueda en los apuntes del repo para darle contexto al modelo (sin embeddings: TF-IDF, igual que el buscador
de ejercicios). Los documentos son pocos y conocidos, así que alcanza y no hace falta una base vectorial.
"""

import math
import re
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from interprete.buscador import _tokens, _vector

RAIZ = Path(__file__).resolve().parent.parent

# nombre corto -> (archivo, nivel de título por el que se corta, peso en la búsqueda)
FUENTES = {
    "convenciones": ("CONVENCIONES_CATEDRA.md", 6, 1.3),
    "redaccion": ("Guía Definitiva de Planteo y Redacción para Exámenes de Estadística Aplicada.md", 6, 1.3),
    "teoria": ("esquema_teorico_examen_estadistica.md", 6, 1.2),
    "tutorial": ("tutorial_guia_app_estadistica.md", 6, 1.0),
    "ejemplo": ("Resolucion Problemas - Sistema Productivo y Faena de Conejos.md", 6, 0.9),
    "guia": ("Guia_resuelta.md", 3, 1.0),     # un fragmento por ejercicio resuelto
}
MAX_CHARS = 2500


@dataclass
class Fragmento:
    fuente: str
    titulo: str
    texto: str
    puntaje: float = 0.0

    def cita(self) -> str:
        return f"[{self.fuente}: {self.titulo}]"


def _partir(texto: str, nivel: int) -> List[tuple]:
    """(título, cuerpo) cortando en los títulos de nivel <= `nivel`; los largos se parten en pedazos."""
    patron = re.compile(r"^(#{1,%d})\s+(.+)$" % nivel, re.MULTILINE)
    cortes = list(patron.finditer(texto))
    secciones = []
    if cortes and cortes[0].start() > 0:
        secciones.append(("Introducción", texto[: cortes[0].start()]))
    for i, m in enumerate(cortes):
        fin = cortes[i + 1].start() if i + 1 < len(cortes) else len(texto)
        secciones.append((m.group(2).strip().replace("\\", ""), texto[m.end():fin]))
    salida = []
    for titulo, cuerpo in secciones:
        cuerpo = cuerpo.strip()
        if len(cuerpo) < 40:
            continue
        for k in range(0, len(cuerpo), MAX_CHARS):
            salida.append((titulo if k == 0 else f"{titulo} (cont.)", cuerpo[k:k + MAX_CHARS]))
    return salida


@lru_cache(maxsize=1)
def _indice():
    frags: List[Fragmento] = []
    pesos: List[float] = []
    for nombre, (archivo, nivel, peso) in FUENTES.items():
        ruta = RAIZ / archivo
        if not ruta.exists():
            continue
        for titulo, cuerpo in _partir(ruta.read_text(encoding="utf-8"), nivel):
            frags.append(Fragmento(nombre, titulo, cuerpo))
            pesos.append(peso)
    docs = [Counter(_tokens(f.titulo + " " + f.titulo + " " + f.texto)) for f in frags]
    df = Counter()
    for d in docs:
        df.update(d.keys())
    n = len(docs)
    idf = {t: math.log((n + 1) / (c + 0.5)) for t, c in df.items()}
    return frags, [_vector(d, idf) for d in docs], idf, pesos


def buscar(texto: str, k: int = 4, fuentes: Optional[Sequence[str]] = None) -> List[Fragmento]:
    """Los k fragmentos de los apuntes más parecidos al texto (solo de `fuentes`, si se indican)."""
    frags, vecs, idf, pesos = _indice()
    q = _vector(Counter(_tokens(texto)), idf)
    puntajes = []
    for f, v, w in zip(frags, vecs, pesos):
        if fuentes and f.fuente not in fuentes:
            continue
        sim = sum(x * v.get(t, 0.0) for t, x in q.items()) * w
        if sim > 0:
            puntajes.append((sim, f))
    puntajes.sort(key=lambda x: -x[0])
    return [Fragmento(f.fuente, f.titulo, f.texto, s) for s, f in puntajes[:k]]


def como_texto(fragmentos: List[Fragmento], max_chars: int = 9000) -> str:
    """Los fragmentos para pegar en el prompt, con su cita."""
    partes, total = [], 0
    for f in fragmentos:
        bloque = f"{f.cita()}\n{f.texto.strip()}"
        if total + len(bloque) > max_chars:
            bloque = bloque[: max(0, max_chars - total)]
        if bloque:
            partes.append(bloque)
            total += len(bloque)
        if total >= max_chars:
            break
    return "\n\n---\n\n".join(partes)


def convenciones() -> str:
    """Las convenciones de la cátedra completas (son cortas y siempre aplican)."""
    ruta = RAIZ / FUENTES["convenciones"][0]
    return ruta.read_text(encoding="utf-8") if ruta.exists() else ""


def resumen_fuentes() -> Dict[str, int]:
    frags = _indice()[0]
    return dict(Counter(f.fuente for f in frags))
