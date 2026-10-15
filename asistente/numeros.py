"""Números del enunciado que el planteo no usa (sin IA).

Si un número del enunciado no aparece en ningún dato ni parámetro del planteo (ni como algo que se deduce
directamente de él: 95% → α = 0,05, 'aumenta 10' → μ₁ = μ₀ + 10, '15% menos' → φ₀ = 0,85...), es una señal fuerte
de que el planteo leyó mal algo: un total en vez de una media (T: 8.160 g de 16 bolsas), un 'de cada 50' tomado
como μ₀ = 1, una diferencia de referencia ignorada ('al menos 2 unidades más').

    sin_usar(analisis, textos_incisos) -> [NumeroSinUsar]
"""

import math
import re
from dataclasses import dataclass
from itertools import combinations
from typing import Any, Iterable, List, Optional, Sequence, Set

from interprete.modelo import Analisis
from interprete.texto import Numero, buscar_listas, buscar_numeros, normalizar


@dataclass
class NumeroSinUsar:
    valor: Optional[float]
    crudo: str
    donde: str          # "planteo" o la letra del inciso
    contexto: str       # el fragmento del enunciado alrededor del número
    lista: bool = False  # es una lista de datos entera que no se usó (no se pregunta número por número)


def _escalares(v: Any) -> Iterable[float]:
    if isinstance(v, bool):
        return
    if isinstance(v, (int, float)):
        yield float(v)
    elif isinstance(v, str):                            # celdas de las tablas del enunciado
        for n in buscar_numeros(v):
            yield n.valor
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _escalares(x)
    elif isinstance(v, dict):
        for x in v.values():
            yield from _escalares(x)


def _largos(v: Any) -> Iterable[float]:
    """Cantidad de datos de listas y tablas (n = 12 cuando vienen 12 valores)."""
    if isinstance(v, (list, tuple)) and v:
        yield float(len(v))
        for x in v:
            yield from _largos(x)
    elif isinstance(v, dict):
        for x in v.values():
            yield from _largos(x)


def valores_del_planteo(an: Analisis) -> List[float]:
    fuentes = [an.datos] + [inc.params for inc in an.incisos] + list(an.tablas or [])
    vals = []
    for f in fuentes:
        vals += list(_escalares(f)) + list(_largos(f))
    return vals


def _igual(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-9)


def _candidatos(n: Numero) -> Set[float]:
    """Formas en que un número del enunciado puede quedar en el planteo."""
    v = n.valor
    c = {v, v / 100, v ** 2, math.sqrt(v) if v >= 0 else v}
    if n.pct or v < 100:
        c |= {1 - v / 100, 1 + v / 100}                  # '15% menos' → 0,85; 'un 10% más' → 1,10
    if abs(v) >= 1000:
        c |= {v / 1000, v / 10 ** 6}                     # '$9.000' con la tabla 'en miles' → 9
    c |= {v * 1000, v * 10 ** 6}                         # datos 'en miles de unidades' → 607.000
    c |= {-x for x in c}
    if 0 < v < 1:
        c |= {1 - v, 1 + v}
    return c


_REFERENCIAS = re.compile(r"(pagina|pag\.|tema|ejercicio|problema|capitulo|figura|tabla|modelo|decada|ano)\s*"
                          r"(del\s*)?['’]?\s*$")


def _irrelevante(texto: str, n: Numero) -> bool:
    """Números que no son datos: años, códigos de modelo ('AX–2'), referencias ('página 28', 'década del '70')."""
    if n.es_entero and 1900 <= n.valor <= 2100:
        return True
    antes = texto[max(0, n.ini - 25):n.ini]
    if re.search(r"[A-Za-z][-–—]\s*$", antes) or re.search(r"['’]\s*$", antes):
        return True
    return bool(_REFERENCIAS.search(normalizar(antes)))


def sin_usar(an: Analisis, incisos: Sequence = ()) -> List[NumeroSinUsar]:
    """Números del planteo y de los incisos que no se usaron (ni directa ni indirectamente)."""
    base = list(set(valores_del_planteo(an)))
    # relaciones de a dos (μ₁ = μ₀ + 10, δ = x̄₁ - x̄₂, n_total = n + Δn, φ = σ₁/σ₂): solo con el número tal cual
    # (o como porcentaje); combinadas con las escalas encuentran coincidencias casuales (3,5 - 1 = 2,5 = 250%)
    unicos = sorted({round(x, 9) for x in base})[:60]
    derivados = []
    for a, b in combinations(unicos, 2):
        derivados += [abs(a - b), a + b] + ([a / b, b / a] if a and b else [])

    def usado(n: Numero) -> bool:
        if any(_igual(c, x) for c in _candidatos(n) for x in base):
            return True
        if any(_igual(c, x) for c in {n.valor, n.fraccion} for x in derivados):
            return True
        if n.pct:                                        # 'el costo baja un 10%': μ₁ = 0,90·μ₀
            f = n.valor / 100
            return any(_igual(x * k, y) for x in base for y in base for k in (1 - f, 1 + f, f) if x)
        return False

    textos = [("planteo", an.planteo)]
    for k, it in enumerate(incisos or []):
        letra, texto = (it[0], it[1]) if isinstance(it, (tuple, list)) else (chr(ord("a") + k), it)
        textos.append((str(letra), str(texto)))
    if not incisos:
        textos += [(i.letra, i.texto) for i in an.incisos if i.texto]

    salida = []
    for donde, texto in textos:
        nums = buscar_numeros(texto)
        # una lista de datos sin usar es UN aviso (no uno por número)
        en_lista = set()
        for li in buscar_listas(texto):
            dentro = [n for n in nums if li.ini <= n.ini < li.fin]
            en_lista |= {n.ini for n in dentro}
            if dentro and 2 * sum(usado(n) for n in dentro) < len(dentro):     # alguno puede coincidir de casualidad
                crudo = " - ".join(n.crudo.strip() for n in dentro[:6]) + (" …" if len(dentro) > 6 else "")
                salida.append(NumeroSinUsar(None, crudo, donde, texto[max(0, li.ini - 50):li.fin][:160], lista=True))
        # intervalos de clase 'a – b': el planteo guarda el punto medio
        en_rango = set()
        for a, b in zip(nums, nums[1:]):
            if re.fullmatch(r"\s*[-–—]\s*", texto[a.fin:b.ini]) and any(_igual((a.valor + b.valor) / 2, x) for x in base):
                en_rango |= {a.ini, b.ini}
        for n in nums:
            if n.ini in en_rango or n.ini in en_lista:
                continue
            if _irrelevante(texto, n):
                continue
            if usado(n):
                continue
            ini, fin = max(0, n.ini - 50), min(len(texto), n.fin + 40)
            salida.append(NumeroSinUsar(n.valor, n.crudo.strip(), donde, texto[ini:fin].replace("\n", " ").strip()))
    return salida


def valores_del_texto(texto: str, datos: Iterable[float] = ()) -> List[float]:
    """Valores que se leen DIRECTAMENTE del texto: cada número tal cual, como %, confianza, escala o 1/x ('1 de
    cada 50'). Ver `derivados_del_texto` para los que salen de una sola cuenta."""
    salida = []
    for n in buscar_numeros(texto):
        salida += list(_candidatos(n))
        salida.append(n.fraccion)
        if n.valor > 1:
            salida.append(1 / n.valor)
    return salida


def derivados_del_texto(texto: str, datos: Iterable[float] = ()) -> List[float]:
    """Además de los directos, lo que sale de UNA cuenta entre números del texto o con un dato del planteo:
    un total dividido por n (8.160/16 = 510), un porcentaje de otro valor (2% de 80 = 1,6)."""
    nums = buscar_numeros(texto)[:40]
    salida = valores_del_texto(texto)
    base = [n.valor for n in nums] + [float(x) for x in datos if isinstance(x, (int, float)) and not isinstance(x, bool)]
    for n in nums:
        for x in base:
            if x and x != n.valor:
                salida += [n.valor / x, n.valor * x]
            if n.pct:
                salida.append(n.fraccion * x)
    return salida
