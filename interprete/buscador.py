"""Buscador de ejercicios parecidos de la Guía de Problemas (TF-IDF, sin dependencias).

Sirve para ver cómo pregunta la cátedra algo parecido y qué respuesta espera
(`Resp:`), y si el ejercicio está resuelto en la guía, sus conclusiones.
"""

import json
import math
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .texto import normalizar

GUIA = Path(__file__).resolve().parent.parent / "datos" / "guia_ejercicios.json"

# Temas que entran en el primer parcial (Tema III: solo estimación, problemas 1-8)
PARCIAL = {"I": range(1, 35), "II": range(1, 13), "III": range(1, 9)}

STOP = set("""
a al algo algun alguna algunos ante antes aquel asi aun cada como con contra cual cuales cuando de del desde
donde dos durante e el ella ellas ellos en entre era es esa ese eso esta estas este esto estos fue ha han hasta
hay la las le les lo los mas me mi muy no nos o otra otro para pero por que quien se sea segun ser si sin sobre
son su sus tal tambien tan tanto te tiene tienen todo todos tras un una uno unos y ya cuyo cuya dicho dicha
""".split())

TEMA_A_GUIA = {"media": "I", "varianza": "II", "proporcion": "III", "dos_varianzas": "IV", "dos_medias": "V",
               "chi_contingencia": "VI", "chi_ajuste": "VI", "regresion": "VII"}


def _tokens(texto: str) -> List[str]:
    palabras = re.findall(r"[a-zñ]{3,}", normalizar(texto))
    # 'stemming' pobre: los primeros 6 caracteres (defectuosas / defectuosos -> defect)
    return [p[:6] for p in palabras if p not in STOP]


@lru_cache(maxsize=1)
def cargar() -> Tuple[List[Dict], List[Dict[str, float]], Dict[str, float]]:
    if not GUIA.exists():
        return [], [], {}
    ejercicios = json.loads(GUIA.read_text(encoding="utf-8"))
    docs = [Counter(_tokens(e["enunciado"])) for e in ejercicios]
    df = Counter()
    for d in docs:
        df.update(d.keys())
    n = len(docs)
    idf = {t: math.log((n + 1) / (c + 0.5)) for t, c in df.items()}
    vecs = [_vector(d, idf) for d in docs]
    return ejercicios, vecs, idf


def _vector(conteo: Counter, idf: Dict[str, float]) -> Dict[str, float]:
    v = {t: (1 + math.log(c)) * idf.get(t, 1.0) for t, c in conteo.items()}
    norma = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {t: x / norma for t, x in v.items()}


def en_parcial(ej: Dict) -> bool:
    return ej["tema"] in PARCIAL and ej["numero"] in PARCIAL[ej["tema"]]


def buscar(texto: str, k: int = 4, tema: Optional[str] = None, solo_parcial: bool = False) -> List[Tuple[float, Dict]]:
    """Los k ejercicios más parecidos. Si se indica el tema detectado, se prioriza ese tema de la guía."""
    ejercicios, vecs, idf = cargar()
    if not ejercicios:
        return []
    q = _vector(Counter(_tokens(texto)), idf)
    tema_guia = TEMA_A_GUIA.get(tema or "")
    puntajes = []
    for ej, v in zip(ejercicios, vecs):
        if solo_parcial and not en_parcial(ej):
            continue
        sim = sum(q[t] * v.get(t, 0.0) for t in q)
        if tema_guia and ej["tema"] == tema_guia:
            sim *= 1.25
        puntajes.append((sim, ej))
    puntajes.sort(key=lambda x: -x[0])
    return puntajes[:k]
