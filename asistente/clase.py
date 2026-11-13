"""Ejercicios resueltos por el profesor en clase (datos/clase_resueltos.json) como BASE.

Dos usos:
- La IA recibe ejemplos parecidos de la guía (`interpretar.ejemplos`, `por_tema.ejemplos_tema`). Los que el profesor
  resolvió en clase tienen el planteo verificado contra lo que él hizo, así que se prefieren: su parecido se multiplica
  por FACTOR. Al medir a ciegas, el ejercicio evaluado se excluye igual que antes (`excluir`).
- En la pantalla, `parecidos(texto)` da los resueltos en clase más parecidos al enunciado con cómo los planteó el
  profesor, para usarlos de referencia en el examen.
"""

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

BANCO = Path(__file__).resolve().parent.parent / "datos" / "clase_resueltos.json"

# cuánto más pesa un resuelto en clase al elegir ejemplos (1 = como cualquier ejercicio de la guía)
FACTOR = float(os.environ.get("ASISTENTE_FACTOR_CLASE", "1.25"))


@lru_cache(maxsize=1)
def banco() -> Dict[str, Dict]:
    try:
        return {e["guia"]: e for e in json.loads(BANCO.read_text(encoding="utf-8"))["ejercicios"]}
    except (OSError, ValueError, KeyError):
        return {}


def priorizar(candidatos: Sequence[Tuple[float, Dict]]) -> List[Tuple[float, Dict]]:
    """(parecido, ejercicio de la guía) reordenados con los resueltos en clase adelante (a igual parecido)."""
    ids = banco()
    return sorted(((s * (FACTOR if ej["id"] in ids else 1.0), ej) for s, ej in candidatos), key=lambda x: -x[0])


def parecidos(texto: str, k: int = 2, excluir: Sequence[str] = (), tema=None) -> List[Tuple[Dict, Dict]]:
    """Los k resueltos en clase más parecidos: (entrada del banco, ejercicio de la guía)."""
    from interprete import buscador
    ids = banco()
    romano = buscador.TEMA_A_GUIA.get(tema or "")
    candidatos = [ej for _, ej in buscador.buscar(texto, k=200, tema=tema)
                  if ej["id"] in ids and ej["id"] not in excluir]
    # con el tema detectado, primero los del mismo tema de la guía (la búsqueda por palabras sola se confunde)
    candidatos.sort(key=lambda ej: romano is not None and ej["tema"] != romano)
    return [(ids[ej["id"]], ej) for ej in candidatos[:k]]
