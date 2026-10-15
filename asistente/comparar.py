"""Dos lecturas independientes del mismo enunciado y se comparan los RESULTADOS.

Las reglas (verificadas contra la guía) leen bien los ejercicios con estructura conocida; la IA razonando en palabras
(`asistente.simple`) lee mejor las redacciones retorcidas (totales, complementos, "por mil", controles de rutina).
Se equivocan en lugares distintos, así que cuando los dos llegan al mismo resultado es muy probable que esté bien, y
cuando no, se muestran los dos planteos y decide el usuario (o le corrige la lectura a la IA).

    from asistente.comparar import comparar, corregir
    c = comparar(planteo, incisos)
    c.coinciden                 # True si todos los incisos dan lo mismo
    c.incisos                   # por inciso: letra, coincide, resumen de las reglas, resumen de la IA
    c2 = corregir(c, "el 1.237,5 es el peso total, no la media", planteo, incisos)
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional, Sequence

from interprete.analizador import analizar
from interprete.modelo import Analisis
from interprete.resolver import Resultado, resolver
from interprete.texto import buscar_numeros

from . import cliente, simple


@dataclass
class IncisoComparado:
    letra: str
    coincide: bool
    reglas: str               # resumen del resultado con el planteo de las reglas
    ia: str                   # resumen del resultado con el planteo de la IA
    reglas_ok: bool = True    # el planteo de las reglas se resuelve
    ia_ok: bool = True        # el planteo de la IA se resuelve

    @property
    def estado(self) -> str:
        """'coincide', 'distinto' (los dos resuelven y dan otra cosa), 'solo_reglas' o 'solo_ia' (el otro no pudo)."""
        if self.coincide:
            return "coincide"
        if self.reglas_ok and self.ia_ok:
            return "distinto"
        return "solo_reglas" if self.reglas_ok else ("solo_ia" if self.ia_ok else "ninguno")


@dataclass
class Comparacion:
    reglas: Analisis
    res_reglas: List[Resultado]
    ia: Optional[simple.Planteo] = None
    res_ia: List[Resultado] = field(default_factory=list)
    incisos: List[IncisoComparado] = field(default_factory=list)
    segundos: float = 0.0
    error: str = ""

    @property
    def coinciden(self) -> bool:
        return not self.error and bool(self.incisos) and all(i.coincide for i in self.incisos)

    @property
    def distintos(self) -> List[IncisoComparado]:
        return [i for i in self.incisos if not i.coincide]


def _decision(r: Resultado) -> Optional[str]:
    t = (r.resumen or "").upper()
    if "NO RECHAZA" in t:
        return "no_rechaza"
    if "RECHAZA" in t:
        return "rechaza"
    return None


def _numeros(r: Resultado) -> List[float]:
    return [n.valor for n in buscar_numeros(r.resumen or "")]


def _cerca(a: float, b: float) -> bool:
    return abs(a - b) <= max(1e-3, 0.005 * max(abs(a), abs(b)))


def mismo_resultado(a: Resultado, b: Resultado) -> bool:
    """Mismo resultado: los dos se resuelven, misma decisión (si es un ensayo) y los mismos números del resumen
    (con tolerancia de redondeo)."""
    if a.errores or b.errores or not a.resumen or not b.resumen:
        return False
    if _decision(a) != _decision(b):
        return False
    na, nb = _numeros(a), _numeros(b)
    if _decision(a) is not None:
        return True                       # en un ensayo manda la decisión (los estadísticos se escriben distinto)
    return bool(na) and all(any(_cerca(x, y) for y in nb) for x in na) and \
        all(any(_cerca(y, x) for x in na) for y in nb)


def _resuelto(r: Resultado) -> bool:
    return not r.errores and bool(r.resumen) and "faltan datos" not in r.resumen and "sin cálculo" not in r.resumen


def _emparejar(c: Comparacion) -> None:
    ia_por_letra = {}
    if c.ia is not None:
        for inc, r in zip(c.ia.analisis.incisos, c.res_ia):
            ia_por_letra[inc.letra.lower()] = r
    mismos = c.ia is not None and len(c.ia.analisis.incisos) == len(c.reglas.incisos)
    c.incisos = []
    for k, (inc, r) in enumerate(zip(c.reglas.incisos, c.res_reglas)):
        otro = ia_por_letra.get(inc.letra.lower())
        if otro is None and mismos and k < len(c.res_ia):
            otro = c.res_ia[k]            # 'única' vs 'a': con la misma cantidad de incisos se empareja por orden
        c.incisos.append(IncisoComparado(
            inc.letra, otro is not None and mismo_resultado(r, otro),
            r.resumen or "; ".join(r.errores) or "no se resolvió",
            "la IA no lo planteó" if otro is None else (otro.resumen or "; ".join(otro.errores) or "no se resolvió"),
            _resuelto(r), otro is not None and _resuelto(otro)))


def comparar(planteo: str, incisos=None, tablas=None, modelo: Optional[str] = None,
             analisis: Optional[Analisis] = None, excluir: Sequence[str] = ()) -> Comparacion:
    reglas = analisis if analisis is not None else analizar(planteo, incisos, tablas=tablas)
    c = Comparacion(reglas, resolver(reglas))
    t0 = time.time()
    try:
        c.ia = simple.plantear(planteo, incisos, tablas, modelo, excluir=excluir)
        c.res_ia = resolver(c.ia.analisis)
    except cliente.ErrorIA as e:
        c.error = str(e)
    c.segundos = time.time() - t0
    _emparejar(c)
    return c


def corregir(anterior: Comparacion, nota: str, planteo: str, incisos=None, tablas=None,
             modelo: Optional[str] = None) -> Comparacion:
    """El usuario le explica a la IA qué leyó mal; se rehace su planteo y se vuelve a comparar."""
    c = Comparacion(anterior.reglas, anterior.res_reglas)
    t0 = time.time()
    try:
        base = anterior.ia if anterior.ia is not None else simple.plantear(planteo, incisos, tablas, modelo)
        c.ia = simple.corregir(base, nota, planteo, incisos, tablas, modelo)
        c.res_ia = resolver(c.ia.analisis)
    except cliente.ErrorIA as e:
        c.error = str(e)
        c.ia = anterior.ia
        c.res_ia = anterior.res_ia
    c.segundos = time.time() - t0
    _emparejar(c)
    return c
