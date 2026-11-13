"""Consenso: tres lecturas independientes del mismo enunciado y se vota el RESULTADO de cada inciso.

Las reglas, la IA que arma el JSON con ejemplos de la guía (`interpretar.pedir_ia`) y la IA con un prompt corto POR
TEMA (`por_tema.pedir_ia_tema`) se equivocan en lugares distintos. Cuando dos llegan al mismo resultado es muy probable
que esté bien; cuando no, se muestran las lecturas en palabras (qué pide, H0/H1, resultado) para que decida el alumno.
Sin 'pensar': en el examen no hay tiempo.

Hasta el 04/11/2026 la tercera lectura era la IA que razona en palabras (`simple.plantear`). Medido con qwen3:8b en los
exámenes del 2° parcial (30 incisos): consenso 29/30 y ~130 s por problema; con la lectura por tema, 30/30 y ~60 s.

    from asistente.consenso import consenso
    c = consenso(planteo, incisos, tablas)
    for i in c.incisos:
        i.letra, i.estado, i.elegido.resumen      # estado: 'consenso' | 'ia_vs_reglas' | 'sin_consenso' | 'una_sola' | 'ninguna'
"""

import copy
from concurrent.futures import ThreadPoolExecutor
import re
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from interprete.analizador import analizar, explicar
from interprete.modelo import Analisis, Inciso
from interprete.resolver import Resultado, resolver
from interprete.texto import buscar_numeros

from . import cliente, simple
from .comparar import _cerca, _decision, _resuelto
from .interpretar import completar_con_reglas, lista_incisos, pedir_ia
from .por_tema import pedir_ia_tema

# las lecturas que se hacen, en orden de preferencia cuando hay empate (las reglas y la IA con ejemplos son las que más
# aciertan solas: 27/30 cada una en los exámenes del 2° parcial; la IA por tema 23/30)
FUENTES = ("reglas", "ia", "ia_tema")
ORDEN = FUENTES + ("ia_razonada",)          # la razonada ya no se corre, pero se puede votar con ella (tests, pruebas)
NOMBRES = {"reglas": "Reglas (solver)", "ia": "IA con ejemplos de la guía", "ia_tema": "IA por tema (prompt corto)",
           "ia_razonada": "IA razonando en palabras"}


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
    estado: str               # 'consenso' (2+ iguales) | 'ia_vs_reglas' | 'sin_consenso' | 'una_sola' | 'ninguna'

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


def _leer(fuente: str, planteo: str, incisos, tablas, modelo, excluir: Sequence[str] = ()) -> Lectura:
    t0 = time.time()
    lec = Lectura(fuente)
    try:
        if fuente == "reglas":
            lec.analisis = analizar(planteo, incisos, tablas=tablas)
        elif fuente in ("ia", "ia_tema"):
            an, _ = (pedir_ia if fuente == "ia" else pedir_ia_tema)(planteo, incisos, tablas, modelo, excluir=excluir)
            pl, lista = lista_incisos(planteo, incisos)
            completar_con_reglas(an, pl, lista, an.tablas or None)
            lec.analisis = an
        else:
            lec.analisis = simple.plantear(planteo, incisos, tablas, modelo).analisis
        lec.resultados = resolver(lec.analisis)
    except cliente.ErrorIA as e:
        lec.error = str(e)
    except Exception as e:      # noqa: BLE001 — una lectura que falla no puede tirar abajo las otras (ni las reglas)
        lec.error = f"falló la lectura ({type(e).__name__}: {e})"
        lec.analisis = lec.analisis if lec.resultados else None
    lec.segundos = time.time() - t0
    return lec


def _ia_contra_reglas(grupos: List[List[Voto]]) -> bool:
    """Las dos IA coinciden y las reglas resolvieron otra cosa. Se elige lo de las IA (en exámenes nuevos las reglas
    fallan más), pero NO se muestra como consenso: las dos IA son el mismo modelo y se equivocan juntas. Medido el
    05/11 en los enunciados trampa: con ✅ eran 4 de los 5 consensos equivocados; en el 2° parcial 23/06/25 (Q1), en
    cambio, las IA tenían razón."""
    return all(v.fuente != "reglas" for v in grupos[0]) and any(v.fuente == "reglas" for g in grupos[1:] for v in g)


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
        grupos.sort(key=lambda g: (-len(g), min(ORDEN.index(v.fuente) for v in g)))
        if not grupos:
            estado = "ninguna"
        elif len(grupos[0]) >= 2 and _ia_contra_reglas(grupos):
            estado = "ia_vs_reglas"
        elif len(grupos[0]) >= 2:
            estado = "consenso"
        elif len(grupos) == 1:
            estado = "una_sola"
        else:
            estado = "sin_consenso"
        salida.append(IncisoConsenso(inc.letra, votos, grupos, estado))
    return salida


def consenso(planteo: str, incisos=None, tablas=None, modelo: Optional[str] = None,
             excluir: Sequence[str] = ()) -> Consenso:
    """`excluir`: ids de la guía que la IA no puede recibir como ejemplo (para medir a ciegas un ejercicio de la guía)."""
    t0 = time.time()
    if not tablas:
        # la tabla pegada dentro del planteo: que las IA la reciban armada y no hagan cuentas con ella (2° parcial
        # 10/11/25, 1a: la IA por tema «resumió» la tabla de clases con n = 120/100 y x̄ inventados)
        from interprete.tablas import buscar_tablas
        tablas = buscar_tablas(planteo)[:1] or None
    # las dos lecturas de IA van a la vez (Ollama con OLLAMA_NUM_PARALLEL ≥ 2 las atiende juntas; si no, hace fila)
    with ThreadPoolExecutor(max_workers=len(FUENTES)) as pool:
        lecturas = list(pool.map(lambda f: _leer(f, planteo, incisos, tablas, modelo, excluir), FUENTES))
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
    base = max(lects, key=lambda f: (cuenta.get(f, 0), -ORDEN.index(f)))
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
