"""Consenso: tres lecturas independientes del mismo enunciado y se vota el RESULTADO de cada inciso.

Medido con exámenes reales (final 15/12/25 y 2° parcial 23/06/25): las reglas, la IA que arma el JSON con ejemplos de
la guía (`interpretar.pedir_ia`) y la IA que primero razona en palabras (`simple.plantear`) se equivocan en lugares
distintos. Cuando dos llegan al mismo resultado es muy probable que esté bien; cuando no, se muestran las lecturas en
palabras (qué pide, H0/H1, resultado) para que decida el alumno. Sin 'pensar': en el examen no hay tiempo.

    from asistente.consenso import consenso
    c = consenso(planteo, incisos, tablas)
    for i in c.incisos:
        i.letra, i.estado, i.elegido.resumen      # estado: 'consenso' | 'sin_consenso' | 'una_sola' | 'ninguna'
"""

import copy
import re
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from interprete.analizador import analizar, explicar
from interprete.modelo import Analisis, Inciso
from interprete.resolver import Resultado, resolver
from interprete.texto import buscar_numeros

from . import cliente, simple
from .comparar import _cerca, _decision, _resuelto
from .interpretar import completar_con_reglas, lista_incisos, pedir_ia

# orden de preferencia cuando hay empate (medido: la IA con ejemplos acertó más que la razonada en lo no visto)
FUENTES = ("reglas", "ia", "ia_razonada")
NOMBRES = {"reglas": "Reglas (solver)", "ia": "IA con ejemplos de la guía", "ia_razonada": "IA razonando en palabras"}


@dataclass
class Lectura:
    fuente: str
    analisis: Optional[Analisis] = None
    resultados: List[Resultado] = field(default_factory=list)
    error: str = ""
    segundos: float = 0.0


@dataclass
class Voto:
    fuente: str
    resultado: Resultado
    que_pide: str             # el planteo de esa lectura en palabras
    hipotesis: str = ""


@dataclass
class IncisoConsenso:
    letra: str
    votos: List[Voto]
    grupos: List[List[Voto]]  # votos con el mismo resultado, el más votado primero
    estado: str               # 'consenso' (2+ iguales) | 'sin_consenso' | 'una_sola' | 'ninguna'

    @property
    def elegido(self) -> Optional[Voto]:
        return self.grupos[0][0] if self.grupos else None


@dataclass
class Consenso:
    lecturas: List[Lectura]
    incisos: List[IncisoConsenso]
    segundos: float = 0.0

    @property
    def todos_de_acuerdo(self) -> bool:
        return bool(self.incisos) and all(i.estado == "consenso" for i in self.incisos)


def _numeros(r: Resultado) -> List[float]:
    return [n.valor for n in buscar_numeros(r.resumen or "")]


def igual(a: Resultado, b: Resultado) -> bool:
    """Más estricto que `comparar.mismo_resultado`: en un ensayo, además de la decisión, tienen que coincidir los
    números del resumen (la H0 y el crítico); si no, 'RECHAZA' con otra hipótesis contaría como un acuerdo."""
    if not (_resuelto(a) and _resuelto(b)) or _decision(a) != _decision(b):
        return False
    na, nb = _numeros(a), _numeros(b)
    if not na or not nb:
        return _decision(a) is not None and not na and not nb
    return all(any(_cerca(x, y) for y in nb) for x in na) and all(any(_cerca(y, x) for x in na) for y in nb)


_RE_HIP = re.compile(r"H0:\s*([^|]*?)\s+vs\s+H1:\s*([^.(|]*)")


def _hipotesis(r: Resultado) -> str:
    m = _RE_HIP.search(re.sub(r"\*\*", "", " ".join(r.pasos)))
    return f"H0: {m.group(1).strip()}  vs  H1: {m.group(2).strip()}" if m else ""


def _que_pide(an: Analisis, inc: Inciso) -> str:
    try:
        return explicar(inc, an)
    except Exception:          # la descripción es solo para mostrar
        return inc.que_pide or ""


def _leer(fuente: str, planteo: str, incisos, tablas, modelo) -> Lectura:
    t0 = time.time()
    lec = Lectura(fuente)
    try:
        if fuente == "reglas":
            lec.analisis = analizar(planteo, incisos, tablas=tablas)
        elif fuente == "ia":
            an, _ = pedir_ia(planteo, incisos, tablas, modelo)
            pl, lista = lista_incisos(planteo, incisos)
            completar_con_reglas(an, pl, lista, an.tablas or None)
            lec.analisis = an
        else:
            lec.analisis = simple.plantear(planteo, incisos, tablas, modelo).analisis
        lec.resultados = resolver(lec.analisis)
    except cliente.ErrorIA as e:
        lec.error = str(e)
    lec.segundos = time.time() - t0
    return lec


def votar(lecturas: List[Lectura]) -> List[IncisoConsenso]:
    base = next((l for l in lecturas if l.analisis is not None), None)
    if base is None:
        return []
    salida = []
    for k, inc in enumerate(base.analisis.incisos):
        votos = []
        for lec in lecturas:
            if lec.analisis is None:
                continue
            j = next((i for i, x in enumerate(lec.analisis.incisos) if x.letra.lower() == inc.letra.lower()), None)
            if j is None and len(lec.analisis.incisos) == len(base.analisis.incisos):
                j = k                       # 'única' vs 'a': misma cantidad de incisos → por orden
            if j is None or j >= len(lec.resultados):
                continue
            r = lec.resultados[j]
            votos.append(Voto(lec.fuente, r, _que_pide(lec.analisis, lec.analisis.incisos[j]), _hipotesis(r)))
        grupos: List[List[Voto]] = []
        for v in votos:
            if not _resuelto(v.resultado):
                continue
            g = next((g for g in grupos if igual(g[0].resultado, v.resultado)), None)
            g.append(v) if g is not None else grupos.append([v])
        grupos.sort(key=lambda g: (-len(g), min(FUENTES.index(v.fuente) for v in g)))
        if not grupos:
            estado = "ninguna"
        elif len(grupos[0]) >= 2:
            estado = "consenso"
        elif len(grupos) == 1:
            estado = "una_sola"
        else:
            estado = "sin_consenso"
        salida.append(IncisoConsenso(inc.letra, votos, grupos, estado))
    return salida


def consenso(planteo: str, incisos=None, tablas=None, modelo: Optional[str] = None) -> Consenso:
    t0 = time.time()
    lecturas = [_leer(f, planteo, incisos, tablas, modelo) for f in FUENTES]
    return Consenso(lecturas, votar(lecturas), time.time() - t0)


def _indice(an: Analisis, letra: str, k: int) -> Optional[int]:
    j = next((i for i, x in enumerate(an.incisos) if x.letra.lower() == letra.lower()), None)
    return j if j is not None else (k if k < len(an.incisos) else None)


def combinado(c: Consenso, elecciones: Optional[Dict[str, str]] = None) -> Optional[Analisis]:
    """Un solo planteo para la pantalla: cada inciso tomado de la lectura elegida (la más votada, o la que eligió el
    alumno en `elecciones`: letra -> fuente). Se controla que dé los mismos resultados que se votaron."""
    elecciones = elecciones or {}
    lects = {l.fuente: l for l in c.lecturas if l.analisis is not None}
    if not lects:
        return None

    def fuente_de(ic: IncisoConsenso) -> Optional[str]:
        f = elecciones.get(ic.letra)
        return f if f in lects else (ic.elegido.fuente if ic.elegido else None)

    cuenta = Counter(fuente_de(ic) for ic in c.incisos if fuente_de(ic))
    base = max(lects, key=lambda f: (cuenta.get(f, 0), -FUENTES.index(f)))
    an = copy.deepcopy(lects[base].analisis)
    for k, ic in enumerate(c.incisos):
        f = fuente_de(ic)
        i_an = _indice(an, ic.letra, k)
        if f is None or f == base or i_an is None:
            continue
        otra = lects[f].analisis
        j = _indice(otra, ic.letra, k)
        if j is None:
            continue
        nuevo = copy.deepcopy(otra.incisos[j])
        nuevo.letra = an.incisos[i_an].letra
        for clave, v in otra.datos.items():         # el inciso lleva los datos de SU lectura
            if v is not None:
                nuevo.params.setdefault(clave, v)
        if (nuevo.params.get("tema") or otra.tema) != an.tema:
            nuevo.params["tema"] = nuevo.params.get("tema") or otra.tema
        nuevo.razones = [f"Inciso tomado de: {NOMBRES[f]}."] + list(nuevo.razones)
        an.incisos[i_an] = nuevo
    an.avisos = [a for a in an.avisos if not a.startswith("🗳️")]
    an.avisos.append(f"🗳️ Planteo armado por consenso (base: {NOMBRES[base]}).")
    res = resolver(an)
    for k, ic in enumerate(c.incisos):
        f = fuente_de(ic)
        voto = next((v for v in ic.votos if v.fuente == f), None)
        i_an = _indice(an, ic.letra, k)
        if voto is not None and i_an is not None and i_an < len(res) and not igual(res[i_an], voto.resultado):
            an.avisos.append(f"🗳️ Inciso {ic.letra}): al juntar las lecturas el resultado cambió; revisalo o usá el "
                             f"planteo completo de {NOMBRES[f]}.")
    return an
