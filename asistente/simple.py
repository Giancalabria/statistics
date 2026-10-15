"""IA en dos pasos: primero razona el planteo EN PALABRAS (como un alumno), después lo pasa a los campos del solver.

    from asistente.simple import plantear
    p = plantear(planteo, incisos)               # p.analisis va a interprete.resolver.resolver
    p.razonamiento                               # el planteo en palabras (para mostrar y discutir)
    p2 = plantear(planteo, incisos, conversacion=p.conversacion + [nota del usuario])   # "hablar" con la IA

La idea: pedirle de entrada un JSON con decenas de claves la distrae de LEER el enunciado. En el paso 1 solo lee y
razona (sin formato rígido); en el paso 2 traduce, viendo solo las claves del tema que eligió.
"""

import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from interprete.modelo import CAMPOS_PLANTEO, TEMAS, TIPOS, TIPOS_POR_TEMA, Analisis, Inciso

from . import cliente
from .esquema import CAMPOS_INC, CLAVES_TEMA, ENUMS, desde_dict
from .interpretar import _parsear, ejemplos, lista_incisos

RAZONAR = """Sos un docente de Estadística Aplicada (UADE, cátedra Dopazo – García). Leé el enunciado con mucho \
cuidado, como lo leería un alumno atento en el examen, y escribí el PLANTEO en palabras. NO hagas los cálculos \
estadísticos (los hace un programa): solo interpretá.

El profesor redacta a propósito de forma confusa. Antes de anotar cada dato preguntate:
- ¿Es un TOTAL de la muestra y no un promedio? (entonces x̄ = total / n)
- ¿Me dan los que CUMPLEN y me preguntan por los que NO (o al revés)? (entonces r = n − dato)
- ¿Es una frecuencia "por mil", "N de cada M", "la mitad", "uno de cada cuatro"? (pasala a proporción)
- ¿Es una VARIANZA (unidades al cuadrado, mm², cm²) o un DESVÍO? (desvío = √varianza)
- ¿Están todos los datos en la MISMA UNIDAD (horas/minutos, pesos/miles de pesos, km/miles de km)?
- ¿Piden el ANCHO o amplitud total de un intervalo? (el error es la mitad)
- ¿Los porcentajes son de cada grupo? (pasalos a cantidades: 12% de 400 = 48)
- ¿Las mediciones son sobre LOS MISMOS individuos antes/después? (muestras apareadas)
- ¿Quién es el sujeto de la frase? "B tarda X menos que A" ⇒ μA − μB; "al menos un 10% más" ⇒ μ1 > 1,10·μ2.
- Riesgo α = probabilidad de rechazar H0 por error, aunque lo digan como "detener sin necesidad", "reclamar \
injustamente", "cambiar innecesariamente". β = probabilidad de no detectar.
- Criterio: si se decide un CAMBIO / inversión / reclamo que solo se hará con evidencia, lo que se quiere probar va \
en H1 (criterio pesimista, unilateral). Si es un CONTROL DE RUTINA de un proceso con valor nominal ("se apartó", \
"detener y recalibrar"), H0 es que está bien y el ensayo es BILATERAL salvo que solo importe un lado.
- La igualdad siempre va en H0.

Escribí, en este orden y sin rodeos:
TEMA: uno de {temas}
VARIABLE: qué es X (con unidad)
DATOS: cada dato con su valor final ya convertido, y de dónde sale (ej.: "x̄ = 1237,5 / 25 = 49,5 kg (dan el peso total)")
INCISOS: para cada letra, qué pide (intervalo, ensayo, tamaño de muestra, β, pronóstico...), el riesgo o la \
confianza, y si es ensayo H0 y H1 con el valor de referencia.
DUDAS: lo que sea ambiguo (o "ninguna")."""

TRADUCIR = """Pasá este planteo (ya razonado) al JSON que lee el programa. NO lo reinterpretes: copiá los valores \
tal cual del planteo. Números decimales JSON (0.05, no "5%"). Porcentajes como fracción. Solo las claves de abajo.
Poné SOLO las claves que el planteo menciona con un valor: las demás se omiten (no pongas 0, null ni valores por \
defecto). Las opcionales (cota de un solo lado, prob, individual, etc.) van solo si el planteo lo dice explícitamente.

Formato: {{"tema": "{tema}", "datos": {{...}}, "incisos": [{{"letra": "a", "tipo": "...", "params": {{...}}}}]}}

El campo "tipo" de cada inciso tiene que ser EXACTAMENTE una de estas palabras (entre comillas): {tipos}

DATOS (objeto 'datos'):
{datos}

PARÁMETROS DE CADA INCISO (objeto 'params', solo lo que ese inciso agrega o cambia):
{params}"""


@dataclass
class Planteo:
    analisis: Analisis
    razonamiento: str
    conversacion: List[Dict[str, str]] = field(default_factory=list)   # paso 1, para seguir hablando
    avisos: List[str] = field(default_factory=list)


def _linea(clave: str, etiqueta: str, tipo: str) -> str:
    extra = f" — uno de: {', '.join(ENUMS[tipo])}" if tipo in ENUMS else ""
    return f"- {clave} ({tipo}): {etiqueta}{extra}"


def _catalogo(tema: str) -> Dict[str, str]:
    datos, params = CLAVES_TEMA.get(tema, (list(CAMPOS_PLANTEO), list(CAMPOS_INC)))
    return {
        "tema": tema,
        "tipos": "; ".join(f'"{t}" ({TIPOS.get(t, t)})' for t in TIPOS_POR_TEMA.get(tema, [])),
        "datos": "\n".join(_linea(k, *CAMPOS_PLANTEO[k]) for k in datos if k in CAMPOS_PLANTEO),
        "params": "\n".join(_linea(k, *CAMPOS_INC[k]) for k in params if k in CAMPOS_INC),
    }


# el modelo a veces escribe el tipo en palabras ("intervalo_confianza_proporcion"): se lleva al más parecido
_TIPO_PALABRAS = (("pronost", "pronostico"), ("prediccion", "pronostico"), ("recta", "recta"),
                  ("determinacion", "ic_rho2"), ("r2", "ic_rho2"), ("pendiente", "ensayo_coef"), ("beta1", "ensayo_coef"),
                  ("potencia", "beta"), ("beta", "beta"), ("operativa", "curva"), ("curva", "curva"),
                  ("diseno", "diseno"), ("disenar", "diseno"), ("tamano", "n"), ("muestra", "n"),
                  ("intervalo", "ic"), ("estima", "ic"), ("ensayo", "ensayo"), ("hipotesis", "ensayo"),
                  ("test", "ensayo"), ("prueba", "ensayo"))


def _normalizar_tipos(d: Dict) -> None:
    validos = TIPOS_POR_TEMA.get(d.get("tema"), [])
    for inc in d.get("incisos") or []:
        if not isinstance(inc, dict) or inc.get("tipo") in validos:
            continue
        t = str(inc.get("tipo") or "").lower().replace("ñ", "n").replace("ó", "o").replace("í", "i")
        inc["tipo"] = next((v for k, v in _TIPO_PALABRAS if k in t and v in validos), inc.get("tipo"))


def _tema_de(texto: str) -> str:
    m = re.search(r"TEMA:\s*([a-z_]+)", texto)
    if m and m.group(1) in TEMAS:
        return m.group(1)
    t = texto.lower()
    return next((k for k in TEMAS if k in t), "desconocido")


def enunciado(planteo: str, incisos=None) -> Tuple[str, List[Tuple[str, str]], str]:
    planteo, lista = lista_incisos(planteo, incisos)
    texto = planteo + "\n" + ("\n".join(f"{l}) {t}" for l, t in lista) if lista else "(Sin incisos: letra 'única'.)")
    return planteo, lista, texto


def plantear(planteo: str, incisos=None, tablas=None, modelo: Optional[str] = None,
             conversacion: Optional[List[Dict[str, str]]] = None, excluir=()) -> Planteo:
    """Paso 1 (razonar) + paso 2 (traducir). Con `conversacion` se continúa una charla anterior: el último mensaje
    del usuario es su corrección ("el 1.237,5 es el total, no la media")."""
    planteo, lista, texto = enunciado(planteo, incisos)
    if conversacion:
        msgs = list(conversacion)
    else:
        msgs = [{"role": "system", "content": RAZONAR.format(temas="; ".join(f"{k} ({v})" for k, v in TEMAS.items() if k != "desconocido"))},
                {"role": "user", "content": f"ENUNCIADO:\n{texto}"}]
    razonamiento = re.sub(r"<think>.*?</think>", "", cliente.chat(msgs, modelo=modelo, temperatura=0, max_tokens=1500),
                          flags=re.DOTALL).strip()
    msgs = msgs + [{"role": "assistant", "content": razonamiento}]
    tema = _tema_de(razonamiento)
    # ejemplos resueltos de la guía (enunciado → JSON de las reglas, verificado): muestran cómo se cargan las claves
    traducir = [{"role": "system", "content": TRADUCIR.format(**_catalogo(tema))}]
    for ej in ejemplos(texto, 2, excluir):
        traducir += [{"role": "user", "content": f"ENUNCIADO:\n{ej.enunciado}"}, {"role": "assistant", "content": ej.json}]
    traducir.append({"role": "user", "content": f"ENUNCIADO:\n{texto}\n\nPLANTEO RAZONADO (seguilo):\n{razonamiento}"})
    js = cliente.chat(traducir, modelo=modelo, formato="json", temperatura=0, max_tokens=1200)
    d = _parsear(js)
    d.setdefault("tema", tema)
    _normalizar_tipos(d)
    an, avisos = desde_dict(d, planteo, dict(lista))
    an.tablas = list(tablas) if tablas else []
    if not an.incisos:
        an.incisos = [Inciso(letra=l, texto=t) for l, t in (lista or [("única", planteo)])]
    an.razones_tema = ["Planteo armado por la IA (razonado en palabras)."]
    return Planteo(an, razonamiento, msgs, avisos)


def corregir(anterior: Planteo, nota: str, planteo: str, incisos=None, tablas=None,
             modelo: Optional[str] = None) -> Planteo:
    """El usuario le explica a la IA qué está mal; la IA rehace el planteo teniéndolo en cuenta."""
    msgs = anterior.conversacion + [{"role": "user", "content": f"Corrección del alumno: {nota}\n\nRehacé el "
                                                                "planteo completo con el mismo formato."}]
    return plantear(planteo, incisos, tablas, modelo, conversacion=msgs)
