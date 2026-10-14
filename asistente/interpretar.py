"""Interpretación híbrida: primero las reglas; la IA solo interviene donde las reglas fallan.

    from asistente.interpretar import interpretar
    r = interpretar(planteo, incisos)          # r.analisis va directo a interprete.resolver.resolver
    r.informe                                  # qué cambió la IA (y por qué se aceptó)
    r.sugerencias                              # en qué difiere la IA de las reglas (no se aplicó: revisalo vos)

Criterio para aceptar un cambio de la IA: tiene que hacer que el solver resuelva MÁS incisos sin errores que
antes, sin romper ninguno que ya se resolvía. Lo que las reglas ya resuelven no se toca (están verificadas
contra la guía); si la IA lee otra cosa queda como sugerencia.
"""

import copy
import json
import re
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from interprete import buscador
from interprete.analizador import analizar, separar_incisos
from interprete.modelo import CAMPOS_PLANTEO, TEMAS, TIPOS, Analisis, Inciso
from interprete.resolver import Resultado, resolver

from . import cliente
from .esquema import CAMPOS_INC, a_dict, catalogo_texto, desde_dict, json_schema

SISTEMA = """Sos un asistente que INTERPRETA enunciados de Estadística Aplicada (UADE, cátedra Dopazo - García) y \
los traduce a un JSON que después resuelve un programa. Vos NO calculás nada: solo leés el enunciado y anotás \
qué tema es, qué datos da y qué pide cada inciso.

Reglas:
- Usá EXACTAMENTE las claves del catálogo. Poné solo lo que el enunciado dice (no inventes datos ni calcules).
- Números en formato decimal JSON (0.05, no "5%" ni "0,05"). Porcentajes como fracción: 5% -> 0.05.
- alpha = 1 - confianza (95% de confianza -> alpha 0.05). "Riesgo", "significación" o "probabilidad de \
rechazar por error" -> alpha. "Probabilidad de no detectar" -> beta.
- desvio: si es de la población / del proceso ("se sabe", "históricamente", "la máquina tiene un desvío") \
sigma_conocido = true; si sale de la muestra, sigma_conocido = false.
- Si hay datos crudos de una muestra, van en 'datos' (lista) y no se calculan x̄ ni S.
- tail: 'derecha' si H1 dice que el parámetro es MAYOR, 'izquierda' si es MENOR, 'bilateral' si es distinto.
- criterio: 'optimista' si H0 es lo que se quiere que pase (se le da el beneficio de la duda), 'pesimista' si H0 \
es la situación a evitar y solo se acepta lo bueno con evidencia; 'ninguno' si no hay ensayo.
- Cada inciso lleva su letra (a, b, c...; 'única' si el problema no tiene incisos) y en params solo lo que ese \
inciso agrega o cambia respecto del planteo.
- Si no sabés qué tipo es un inciso usá 'no_soportado'.

""" + catalogo_texto()

ESQUEMA = json_schema()
MAX_EJEMPLO = 3000


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

def lista_incisos(planteo: str, incisos=None) -> Tuple[str, List[Tuple[str, str]]]:
    """Igual que analizar(): incisos como [(letra, texto)]; si no vienen, se separan del planteo."""
    lista: List[Tuple[str, str]] = []
    for k, it in enumerate(incisos or []):
        if isinstance(it, (tuple, list)):
            lista.append((str(it[0]), str(it[1])))
        elif str(it).strip():
            lista.append((chr(ord("a") + k), str(it).strip()))
    if not lista:
        planteo, lista = separar_incisos(planteo, parrafos=True)
    return planteo, lista


def _enunciado(planteo: str, lista: List[Tuple[str, str]]) -> str:
    if not lista:
        return planteo + "\n(Sin incisos: usá la letra 'única'.)"
    return planteo + "\n" + "\n".join(f"{letra}) {texto}" for letra, texto in lista)


@dataclass
class _Ejemplo:
    id: str
    enunciado: str
    json: str


def ejemplos(texto: str, k: int = 2, excluir: Sequence[str] = ()) -> List[_Ejemplo]:
    """Ejercicios parecidos de la guía con el JSON que arman las reglas (verificado contra la guía):
    le muestran al modelo el formato y las convenciones con casos reales."""
    salida = []
    for _, ej in buscador.buscar(texto, k=8):
        if ej["id"] in excluir:
            continue
        if ej["incisos"] and ej["incisos"][0]["letra"] == "única":
            pl, incs = ej["enunciado"], None
        else:
            pl, incs = ej["planteo"], [(i["letra"], i["texto"]) for i in ej["incisos"]]
        an = analizar(pl, incs, tablas=ej.get("tablas") or None)
        js = json.dumps(a_dict(an), ensure_ascii=False)
        if len(js) > MAX_EJEMPLO:
            continue                          # regresiones con tablas largas: no entran en el prompt
        salida.append(_Ejemplo(ej["id"], _enunciado(pl, lista_incisos(pl, incs)[1]), js))
        if len(salida) >= k:
            break
    return salida


def mensajes(planteo: str, lista: List[Tuple[str, str]], borrador: Optional[Analisis] = None,
             excluir: Sequence[str] = (), n_ejemplos: int = 2) -> List[Dict[str, str]]:
    enunciado = _enunciado(planteo, lista)
    msgs = [{"role": "system", "content": SISTEMA}]
    for ej in ejemplos(enunciado, n_ejemplos, excluir):
        msgs.append({"role": "user", "content": f"ENUNCIADO:\n{ej.enunciado}"})
        msgs.append({"role": "assistant", "content": ej.json})
    pedido = f"ENUNCIADO:\n{enunciado}"
    if borrador is not None:
        pedido += ("\n\nUn programa de reglas propuso este JSON y puede estar equivocado o incompleto "
                   "(tema 'desconocido' o incisos 'no_soportado' son los puntos donde falló). Corregilo y completalo:\n"
                   + json.dumps(a_dict(borrador), ensure_ascii=False))
    msgs.append({"role": "user", "content": pedido})
    return msgs


def _parsear(texto: str) -> Dict:
    texto = re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL).strip()
    try:
        return json.loads(texto)
    except ValueError:
        m = re.search(r"\{.*\}", texto, re.DOTALL)
        if m:
            return json.loads(m.group(0))
        raise cliente.ErrorIA(f"La IA no devolvió un JSON válido: {texto[:200]}")


def pedir_ia(planteo: str, incisos=None, tablas=None, modelo: Optional[str] = None, pensar: bool = False,
             borrador: Optional[Analisis] = None, excluir: Sequence[str] = ()) -> Tuple[Analisis, List[str]]:
    """Le pide al modelo el planteo completo (sin mezclar con las reglas). Devuelve el análisis validado + avisos."""
    planteo, lista = lista_incisos(planteo, incisos)
    salida = cliente.chat(mensajes(planteo, lista, borrador, excluir), modelo=modelo, formato=ESQUEMA,
                          pensar=pensar, temperatura=0)
    an, avisos = desde_dict(_parsear(salida), planteo, dict(lista))
    an.tablas = list(tablas) if tablas else (borrador.tablas if borrador else [])
    if not an.incisos:
        an.incisos = [Inciso(letra=letra, texto=texto) for letra, texto in (lista or [("única", planteo)])]
    an.razones_tema = ["Tema identificado por la IA."]
    return an, avisos


# ---------------------------------------------------------------------------
# Híbrido
# ---------------------------------------------------------------------------

def _resuelto(inc: Inciso, res: Resultado) -> bool:
    return inc.tipo != "no_soportado" and not res.errores


def puntaje(an: Analisis, resultados: List[Resultado]) -> int:
    """Cuántos incisos resuelve el solver sin errores."""
    return sum(_resuelto(i, r) for i, r in zip(an.incisos, resultados))


def fallas(an: Analisis, resultados: List[Resultado]) -> List[int]:
    return [k for k, (i, r) in enumerate(zip(an.incisos, resultados)) if not _resuelto(i, r)]


def _par(inc: Inciso, k: int, ia: Analisis) -> Optional[Inciso]:
    """El inciso de la IA que corresponde (por letra; si no, por posición)."""
    for x in ia.incisos:
        if x.letra == inc.letra:
            return x
    base = inc.letra.split(".")[0]
    for x in ia.incisos:
        if x.letra == base:
            return x
    return ia.incisos[k] if k < len(ia.incisos) else None


def _distinto(a, b) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(float(a) - float(b)) > 1e-6 * max(1.0, abs(float(a)))
    return a != b


def _mostrar(v) -> str:
    if isinstance(v, list):
        return f"[{len(v)} valores]"
    if isinstance(v, float):
        return f"{v:g}".replace(".", ",")
    return str(v)


def _etiqueta(clave: str) -> str:
    return (CAMPOS_PLANTEO.get(clave) or CAMPOS_INC.get(clave) or (clave,))[0]


@dataclass
class Interpretacion:
    analisis: Analisis
    reglas: Analisis
    ia: Optional[Analisis] = None
    usado_ia: bool = False
    informe: List[str] = field(default_factory=list)       # cambios aplicados
    sugerencias: List[str] = field(default_factory=list)   # diferencias no aplicadas
    avisos_ia: List[str] = field(default_factory=list)     # lo que se descartó del JSON del modelo
    segundos: float = 0.0
    error: str = ""


def interpretar(planteo: str, incisos=None, tablas=None, modelo: Optional[str] = None, pensar: bool = False,
                siempre: bool = False, excluir: Sequence[str] = ()) -> Interpretacion:
    """Reglas primero; si fallan (o `siempre`), consulta a la IA y aplica solo lo que mejora la resolución.

    Si la IA no está disponible devuelve el análisis de las reglas con `error` explicando por qué."""
    reglas = analizar(planteo, incisos, tablas=tablas)
    res_r = resolver(reglas)
    out = Interpretacion(analisis=reglas, reglas=reglas)
    if not siempre and reglas.tema != "desconocido" and not fallas(reglas, res_r):
        return out
    t0 = time.time()
    try:
        ia, out.avisos_ia = pedir_ia(planteo, incisos, tablas or None, modelo, pensar, borrador=reglas,
                                     excluir=excluir)
    except cliente.ErrorIA as e:
        out.error = str(e)
        return out
    finally:
        out.segundos = time.time() - t0
    out.ia, out.usado_ia = ia, True

    # 1) tema: si la IA dice otro, se vuelven a correr las reglas con ese tema y gana el que resuelve más
    base, res_b = reglas, res_r
    if ia.tema != "desconocido" and ia.tema != reglas.tema:
        forzado = analizar(planteo, incisos, tablas=tablas, tema=ia.tema)
        res_f = resolver(forzado)
        if reglas.tema == "desconocido" or puntaje(forzado, res_f) > puntaje(reglas, res_r):
            base, res_b = forzado, res_f
            out.informe.append(f"Tema: la IA lo identificó como **{TEMAS[ia.tema]}** (las reglas: "
                               f"{TEMAS[reglas.tema]}) y así se resuelven más incisos.")
        else:
            out.sugerencias.append(f"La IA cree que el tema es **{TEMAS[ia.tema]}**; se mantuvo el de las reglas "
                                   f"({TEMAS[reglas.tema]}) porque resuelve igual o más incisos.")

    # 2) incisos que siguen fallando: se prueba con el tipo y los datos que leyó la IA
    actual = copy.deepcopy(base)
    res_a = res_b
    for k in fallas(actual, res_a):
        inc = actual.incisos[k]
        par = _par(inc, k, ia)
        if par is None:
            continue
        for tipo in dict.fromkeys(([inc.tipo] if inc.tipo != "no_soportado" else []) + [par.tipo]):
            if tipo == "no_soportado":
                continue
            prueba = copy.deepcopy(actual)
            pi = prueba.incisos[k]
            agregados = [c for c in ia.datos if c not in prueba.datos]
            for c in agregados:
                prueba.datos[c] = ia.datos[c]
            nuevos = [c for c in par.params if c not in pi.params]
            for c in nuevos:
                pi.params[c] = par.params[c]
            cambio_tipo = tipo != pi.tipo
            pi.tipo = tipo
            res_p = resolver(prueba)
            antes = {j for j in range(len(actual.incisos)) if j not in fallas(actual, res_a)}
            despues = {j for j in range(len(prueba.incisos)) if j not in fallas(prueba, res_p)}
            if k in despues and antes <= despues:
                que = []
                if cambio_tipo:
                    que.append(f"tipo = {TIPOS.get(tipo, tipo)}")
                que += [f"{_etiqueta(c)} = {_mostrar(prueba.datos[c])}" for c in agregados]
                que += [f"{_etiqueta(c)} = {_mostrar(pi.params[c])}" for c in nuevos]
                pi.razones.append("Completado por la IA: " + "; ".join(que) + ".")
                if cambio_tipo:
                    pi.que_pide = f"Según la IA: {TIPOS.get(tipo, tipo)}."
                out.informe.append(f"{inc.letra}) lo completó la IA: " + ("; ".join(que) or "mismos datos") + ".")
                actual, res_a = prueba, res_p
                break
        else:
            out.informe.append(f"{inc.letra}) la IA tampoco logró resolverlo: revisá el tipo y los datos a mano.")

    # 3) si las reglas no sirvieron para nada, se prueba el planteo de la IA tal cual
    res_ia = resolver(ia)
    if puntaje(ia, res_ia) > puntaje(actual, res_a):
        out.informe.append("Se usó el planteo completo de la IA: las reglas no lograron resolver casi nada.")
        actual, res_a = ia, res_ia

    # 4) diferencias en lo que las reglas ya resolvían: sugerencias (no se aplican)
    if actual is not ia:
        for c, v in actual.datos.items():
            if c in ia.datos and c in CAMPOS_PLANTEO and _distinto(v, ia.datos[c]):
                out.sugerencias.append(f"{_etiqueta(c)}: la IA leyó {_mostrar(ia.datos[c])} (se usa {_mostrar(v)}).")
        for k, inc in enumerate(actual.incisos):
            par = _par(inc, k, ia)
            if par is None:
                continue
            if par.tipo != inc.tipo and par.tipo != "no_soportado":
                out.sugerencias.append(f"{inc.letra}) la IA lo ve como {TIPOS.get(par.tipo, par.tipo)} "
                                       f"(se usa {TIPOS.get(inc.tipo, inc.tipo)}).")
            for c, v in par.params.items():
                if c in inc.params and c != "tema" and _distinto(inc.params[c], v):
                    out.sugerencias.append(f"{inc.letra}) {_etiqueta(c)}: la IA leyó {_mostrar(v)} "
                                           f"(se usa {_mostrar(inc.params[c])}).")
    actual.avisos = list(actual.avisos) + [f"🤖 IA: {x}" for x in out.informe]
    out.analisis = actual
    return out


if __name__ == "__main__":       # prueba rápida: python -m asistente.interpretar "enunciado..."
    r = interpretar(" ".join(sys.argv[1:]), siempre=True)
    print(json.dumps(a_dict(r.analisis), ensure_ascii=False, indent=1))
    print("\n".join(["INFORME:"] + r.informe + ["SUGERENCIAS:"] + r.sugerencias + [r.error]))
