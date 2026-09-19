"""Utilidad para resumir una muestra de datos crudos (x1, x2, ..., xn).

Varios ejercicios de la guía (TEMA I y TEMA II) dan la lista de datos en vez del
resumen (x̄, S, n) ya calculado. Este módulo hace esa cuenta una sola vez para
que los módulos de intervals.py / hypothesis_one.py sigan recibiendo el resumen.
"""

from dataclasses import dataclass
from math import sqrt
from typing import List


@dataclass
class ResumenMuestra:
    n: int
    xbar: float
    s: float  # cuasidesvío muestral (denominador n-1)


def resumen_muestra(datos: List[float]) -> ResumenMuestra:
    n = len(datos)
    if n < 2:
        raise ValueError(f"Se necesitan al menos 2 datos para calcular S, no {n}")
    xbar = sum(datos) / n
    s2 = sum((x - xbar) ** 2 for x in datos) / (n - 1)
    return ResumenMuestra(n=n, xbar=xbar, s=sqrt(s2))
