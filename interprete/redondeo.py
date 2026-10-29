"""Redondeo de presentación de la cátedra (convenciones verificadas contra la guía).

- Intervalos: límite inferior hacia abajo y superior hacia arriba (redondeo «hacia afuera»), también en las
  cotas: la máxima hacia arriba, la mínima hacia abajo.
- Valores críticos: hacia afuera, alejándose de μ₀ (achica la región de rechazo): cola derecha hacia arriba,
  cola izquierda hacia abajo; bilateral (abajo, arriba). La decisión se toma siempre con el valor exacto.
- Decimales: una base por tipo de valor (medias y totales 2; σ 2; σ² 4; p, cocientes y coeficientes 4) y se
  agregan decimales hasta que el mayor valor muestre 3 cifras significativas (II-1: 0,00158; II-5: 1,56). En los
  intervalos de medias además el error e debe mostrar 3 cifras (I-36b: e = 0,1149 → 0,985 y 1,215).
Los cálculos encadenados usan siempre los valores sin redondear.

Esto es solo la EXPRESIÓN del resultado final («dependerá de la variable», profesor en clase). En el desarrollo el
profesor exige mínimo 4 decimales (fractiles, críticos, n y ν sin redondear): los pasos del resolver los muestran con
4 decimales y la nota de cada intervalo trae el valor exacto.
"""

from math import ceil, floor, log10
from typing import Tuple

from .texto import fmt


def fijo(v: float, d: int) -> str:
    """Formato argentino con exactamente d decimales (sin recortar ceros: 270,40)."""
    return f"{v:,.{d}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def decimales(*valores: float, base: int = 2, maximo: int = 6) -> int:
    """Base de decimales, ampliada hasta mostrar 3 cifras significativas del mayor valor."""
    m = max((abs(v) for v in valores if v is not None), default=0)
    if m == 0:
        return base
    return min(maximo, max(base, 2 - floor(log10(m))))


def abajo(v: float, d: int) -> float:
    k = 10 ** d
    return floor(v * k + 1e-9) / k


def arriba(v: float, d: int) -> float:
    k = 10 ** d
    return ceil(v * k - 1e-9) / k


def afuera(a: float, b: float, d: int) -> Tuple[float, float]:
    return abajo(a, d), arriba(b, d)


def intervalo(a: float, b: float, base: int = 2, por_error: bool = False) -> Tuple[str, str, str]:
    """(A, B, nota) con los límites redondeados hacia afuera y la nota con los valores exactos.
    `por_error`: los decimales también alcanzan para 3 cifras del error (B - A)/2 (intervalos de medias)."""
    d = decimales(a, b, base=base)
    if por_error and b > a:
        d = max(d, decimales((b - a) / 2, base=base))
    ar, br = afuera(a, b, d)
    nota = f" (límites redondeados hacia afuera; sin redondear: {fmt(a, max(6, d + 2))} y {fmt(b, max(6, d + 2))})"
    return fijo(ar, d), fijo(br, d), nota


def cota(v: float, superior: bool, base: int = 2) -> str:
    d = decimales(v, base=base)
    return fijo(arriba(v, d) if superior else abajo(v, d), d)


def critico(xc, tail: str, base: int = 2) -> str:
    """Valor crítico informado como la cátedra (hacia afuera de μ₀)."""
    if isinstance(xc, tuple):
        d = decimales(*xc, base=base)
        return f"{fijo(abajo(xc[0], d), d)} ; {fijo(arriba(xc[1], d), d)}"
    d = decimales(xc, base=base)
    return fijo(arriba(xc, d) if tail == "derecha" else abajo(xc, d), d)
