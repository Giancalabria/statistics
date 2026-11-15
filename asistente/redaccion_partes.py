"""Redacción por partes: el solver escribe la resolución y la IA solo escribe las palabras que dependen del contexto.

Por qué así: cuando la IA reescribe la resolución completa (≈100 números en un problema de χ²), un modelo de 8B
copia mal algunos aunque tenga todo el contexto (T1-b: e = 0,6107 sin el fractil t; una columna de χ² inventada;
«Total Fe = 123»). Partirlo por inciso achica el texto pero no saca el problema: cada parte seguiría recopiando
números. Acá la IA no toca ningún número del solver:

1. **Palabras del planteo** (una llamada, JSON): qué se mide o se cuenta, su unidad, qué se hace si se rechaza H0 y
   qué se mide en cada inciso (en T2-b se cuentan las no falladas). Se validan en código: sin números, cortas y con
   palabras del enunciado. Con eso se vuelve a correr el solver, que las pone en la variable, la RD y la conclusión.
2. **Textos por inciso** (una llamada chica por hueco, en paralelo): el contexto de H0, la justificación de α si el
   enunciado no lo fija y la respuesta a la pregunta del inciso. Se validan: los números tienen que estar en el
   enunciado o en la resolución de ese inciso, y en un ensayo otra llamada confirma que la respuesta dice lo mismo
   que la decisión del solver. Si algo no pasa, se reintenta una vez con el motivo y, si sigue, queda afuera (la
   resolución del solver ya es correcta sin ese texto).
3. **Armado** (sin IA): los pasos del solver sin las notas para el usuario de la app, más los textos validados.

Lo que la IA escribe es lo que el solver no puede saber (el contexto), y todo lo que se puede verificar se verifica.
"""

import json
import re
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from interprete.modelo import TEMAS, TIPOS, Analisis
from interprete.resolver import Resultado, resolver
from interprete.texto import normalizar

from . import cliente
from .explicar import enunciado_texto, numeros_sin_respaldo, resolucion_texto

ENSAYOS = ("ensayo", "diseno", "ensayo_coef", "validacion")
TEMAS_VARIABLE = ("media", "varianza", "dos_medias", "dos_varianzas", "proporcion", "chi_ajuste", "chi_contingencia")


@dataclass
class Redaccion:
    texto: str
    analisis: Analisis
    resultados: List[Resultado]
    huecos: Dict[str, str] = field(default_factory=dict)        # nombre -> texto aceptado
    descartados: List[str] = field(default_factory=list)        # hueco: motivo (lo que no pasó la validación)


# ---------------------------------------------------------------------------
# Validaciones (sin IA)
# ---------------------------------------------------------------------------

def _palabras(texto: str) -> List[str]:
    return re.findall(r"[a-zñü]{4,}", normalizar(texto))


def anclada(frase: str, enunciado: str, minimo: float = 0.6) -> bool:
    """Las palabras de la frase salen del enunciado (al menos el 60 %, comparando las primeras 5 letras).

    No es una lista de palabras: compara contra el enunciado de turno, así que vale para uno nuevo."""
    propias = _palabras(frase)
    if not propias:
        return False
    raices = {p[:5] for p in _palabras(enunciado)}
    return sum(p[:5] in raices for p in propias) >= minimo * len(propias)


def _frase_ok(frase: str, enunciado: str, max_palabras: int = 12, numeros: bool = False) -> Optional[str]:
    """None si la frase sirve; si no, el motivo."""
    if not frase:
        return "vacía"
    if not numeros and re.search(r"\d", frase):
        return "tiene números"
    if len(frase.split()) > max_palabras:
        return f"más de {max_palabras} palabras"
    if not anclada(frase, enunciado):
        return "sus palabras no salen del enunciado"
    return None


def rechaza(res: Resultado) -> Optional[bool]:
    """La decisión del solver (None si el inciso no decide nada).

    Sale del resumen, donde todo inciso que decide escribe «RECHAZA» o «NO rechaza» (así, en mayúsculas). La
    conclusión no sirve: en un diseño describe la regla («se rechaza H0 si r ≥ 233») sin decidir nada."""
    txt = res.resumen or ""
    if re.search(r"\bNO rechaza\b", txt):
        return False
    if re.search(r"\bRECHAZA\b", txt):
        return True
    return None


# ---------------------------------------------------------------------------
# 1. Palabras del planteo
# ---------------------------------------------------------------------------

_PALABRAS_SISTEMA = """Leés un enunciado de examen de Estadística y devolvés SOLO un JSON con palabras sacadas del enunciado. \
No resolvés nada ni escribís números. Usá las palabras del enunciado (podés acortarlas), en español."""


def _pedido_palabras(an: Analisis) -> str:
    proporcion = any((i.params.get("tema") or an.tema) == "proporcion" for i in an.incisos)
    ensayo = any(i.tipo in ENSAYOS for i in an.incisos) and an.criterio is not None
    claves = {
        "variable": ("lo que se cuenta, en plural (p. ej. «piezas defectuosas», «clientes que compran»)" if proporcion
                     else "qué se mide o se observa en UNA unidad, sin números (p. ej. «peso de un paquete», "
                          "«tiempo de atención de un cliente»)"),
        "unidad": "la unidad de medida del enunciado (p. ej. «gramos», «minutos por pieza»); \"\" si no tiene",
    }
    if ensayo:
        claves["accion_si_rechaza"] = ("qué se hace si el ensayo da que hay evidencia (en infinitivo, p. ej. «modificar "
                                       "el sistema», «detener el proceso»); \"\" si el enunciado no lo dice")
    incisos = "\n".join(f"{i.letra}) {i.texto}" for i in an.incisos if i.letra != "única")
    return (f"ENUNCIADO:\n{an.planteo.strip()}\n" + (f"\nINCISOS:\n{incisos}\n" if incisos else "") +
            f"\nTEMA: {TEMAS.get(an.tema, an.tema)}\n\nDevolvé un JSON con estas claves:\n" +
            "\n".join(f"- \"{k}\": {v}" for k, v in claves.items()))


def palabras_del_planteo(an: Analisis, modelo: Optional[str] = None) -> Tuple[Dict[str, object], List[str]]:
    """({variable, unidad, accion}, descartados). Solo lo que pasa la validación."""
    if an.tema not in TEMAS_VARIABLE and not any(i.params.get("tema") in TEMAS_VARIABLE for i in an.incisos):
        return {}, []
    crudo = cliente.chat([{"role": "system", "content": _PALABRAS_SISTEMA},
                          {"role": "user", "content": _pedido_palabras(an)}],
                         modelo=modelo, formato="json", temperatura=0.1, max_tokens=400)
    try:
        js = json.loads(crudo)
    except (json.JSONDecodeError, TypeError):
        return {}, ["palabras del planteo: la IA no devolvió un JSON"]
    enunciado = enunciado_texto(an)
    salida: Dict[str, object] = {}
    descartados = []
    for clave, destino, maximo in (("variable", "variable", 10), ("accion_si_rechaza", "accion", 8)):
        v = str(js.get(clave) or "").strip().strip(".«»\"")
        if not v:
            continue
        motivo = _frase_ok(v, enunciado, maximo)
        if motivo:
            descartados.append(f"{destino} «{v}»: {motivo}")
        else:
            salida[destino] = v[0].lower() + v[1:] if not v[:2].isupper() else v
    u = str(js.get("unidad") or "").strip().strip(".«»\"")
    if u:
        # la unidad tiene que estar escrita en el enunciado (puede tener números: cm3, m²)
        if normalizar(u) in normalizar(enunciado) and len(u.split()) <= 4:
            salida["unidad"] = u
        else:
            descartados.append(f"unidad «{u}»: no está en el enunciado")
    return salida, descartados


_CONTRARIO = """Devolvé SOLO un JSON {"que_pide": "…"}: qué unidades pide estimar o contar el inciso, copiando las palabras del inciso (con «no» si lo tiene), en plural y sin números."""


_OPUESTAS = """¿Las dos frases nombran cosas OPUESTAS (una es lo contrario de la otra, p. ej. «clientes que compran» y \
«clientes que no compran»)? Devolvé solo el JSON {"opuestas": true} o {"opuestas": false}."""


def _opuestas(a: str, b: str, modelo: Optional[str]) -> Optional[str]:
    """Control independiente (otra pregunta): None si son opuestas; si no, el motivo."""
    try:
        js = json.loads(cliente.chat([{"role": "system", "content": _OPUESTAS},
                                      {"role": "user", "content": f"1: «{a}»\n2: «{b}»"}],
                                     modelo=modelo, formato="json", temperatura=0, max_tokens=30))
        return None if js.get("opuestas") is True else f"no es lo contrario de «{a}»"
    except (json.JSONDecodeError, TypeError, AttributeError):
        return "no se pudo controlar que sea lo contrario"


def contrarios(an: Analisis, resultados: Sequence[Resultado], variable: str,
               modelo: Optional[str] = None) -> Tuple[Dict[str, str], List[str]]:
    """{letra: lo que se cuenta en el inciso} para los incisos en que el solver detectó que se pide el complemento
    (paso «Casos»: el enunciado cuenta 9 con fallas y el inciso pregunta por las no falladas)."""
    salida, descartados = {}, []
    if not variable:
        return salida, descartados
    enunciado = enunciado_texto(an)
    for inc, res in zip(an.incisos, resultados):
        if not any(p.startswith("**Casos**") for p in res.pasos):
            continue
        try:
            js = json.loads(cliente.chat([{"role": "system", "content": _CONTRARIO},
                                          {"role": "user", "content": f"El enunciado cuenta: «{variable}». "
                                                                      f"Inciso: «{inc.texto}»"}],
                                         modelo=modelo, formato="json", temperatura=0, max_tokens=60))
            v = str(js.get("que_pide") or "").strip(" .«»\"")
        except (json.JSONDecodeError, TypeError, AttributeError):
            v = ""
        motivo = _frase_ok(v, enunciado, 8) or ("es lo mismo que cuenta el enunciado"
                                                 if normalizar(v) == normalizar(variable) else None) \
            or _opuestas(variable, v, modelo)
        if motivo:
            descartados.append(f"lo contrario en {inc.letra}) «{v}»: {motivo}")
        else:
            salida[inc.letra.lower()] = v
    return salida, descartados


def con_palabras(an: Analisis, palabras: Dict[str, object]) -> Analisis:
    """Copia del análisis con las palabras puestas donde el solver las usa (lo que cargó el usuario manda)."""
    nuevo = deepcopy(an)
    for clave in ("variable", "unidad", "accion"):
        if palabras.get(clave) and not nuevo.datos.get(clave):
            nuevo.datos[clave] = palabras[clave]
    for inc in nuevo.incisos:
        que = (palabras.get("incisos") or {}).get(inc.letra.lower())
        if que and not inc.params.get("variable"):
            inc.params["variable"] = que
    return nuevo


# ---------------------------------------------------------------------------
# 2. Textos por inciso
# ---------------------------------------------------------------------------

_TEXTO_SISTEMA = """Escribís UNA parte de la resolución de un examen de Estadística (cátedra Dopazo, UADE). La resolución \
y todas las cuentas ya están hechas: vos solo escribís, en español rioplatense, lo que se te pide, en 1 o 2 oraciones, \
con el contexto del problema. Sin títulos, sin viñetas, sin introducción. No hagas cuentas: si usás un número, tiene \
que estar escrito en el enunciado o en la resolución. Nunca digas «se acepta H0»: «se rechaza» o «no se rechaza»."""


def _bloque(res: Resultado) -> str:
    return "\n".join([f"### {res.titulo}"] + [f"- {p}" for p in res.pasos] +
                     ([f"Conclusión: {res.conclusion}"] if res.conclusion else []))


def _pedidos(an: Analisis, inc, res: Resultado) -> Dict[str, str]:
    """hueco -> consigna, según el tipo de inciso."""
    pedidos = {}
    hip = next((p for p in res.pasos if "Planteo de hipótesis" in p or p.startswith("**Hipótesis")), "")
    if inc.tipo in ENSAYOS and hip and (inc.params.get("tema") or an.tema) not in ("chi_ajuste", "chi_contingencia"):
        pedidos["contexto_h0"] = (f"Explicá por qué las hipótesis quedan así, con el contexto del problema: {hip}. "
                                  "Decí qué representa H1 (lo que se quiere poder asegurar o detectar) y qué pasaría "
                                  "si se la afirmara sin que sea cierta. No repitas las hipótesis con símbolos.")
    if any("no lo fija" in p for p in res.pasos) or any("no fija el riesgo" in a for a in res.avisos):
        pedidos["alfa"] = ("El enunciado no fija el riesgo α y se usó α = 0,05. Justificá esa elección con el contexto "
                           "del problema (qué costaría equivocarse), sin decir «porque es el estándar».")
    if res.conclusion:
        pedidos["respuesta"] = (f"Respondé la pregunta del inciso «{inc.texto.strip()}» con el resultado de la "
                                "resolución, en los términos del problema (qué significa para quien decide). Si la "
                                "pregunta se responde por sí o por no, empezá con «Sí» o «No». "
                                "Mantené exactamente lo que dice la conclusión: si no se rechaza H0, no hay evidencia "
                                "suficiente; no lo des por probado. Si es una estimación, decí los límites con sus "
                                "unidades.")
    return pedidos


_CONSISTENCIA = """Leé esta respuesta de un ensayo de hipótesis. ¿Afirma que HAY evidencia suficiente para lo que \
se quería probar (es decir, que se rechaza H0)? Devolvé solo el JSON {"rechaza": true} o {"rechaza": false}."""


def _consistente(texto: str, decision: Optional[bool], modelo: Optional[str]) -> Optional[str]:
    if decision is None:
        return None
    try:
        js = json.loads(cliente.chat([{"role": "system", "content": _CONSISTENCIA},
                                      {"role": "user", "content": texto}],
                                     modelo=modelo, formato="json", temperatura=0, max_tokens=30))
        dice = bool(js.get("rechaza"))
    except (json.JSONDecodeError, TypeError, AttributeError):
        return None
    if dice != decision:
        return ("contradice la decisión del solver: " +
                ("se rechaza H0" if decision else "no se rechaza H0 (no hay evidencia suficiente)"))
    return None


def _validar(hueco: str, texto: str, fuentes: str, decision: Optional[bool], modelo) -> Optional[str]:
    if not texto or len(texto) < 15:
        return "vacío"
    if len(texto) > 600:
        return "demasiado largo (son 1 o 2 oraciones)"
    if re.search(r"\bacept\w*\s+(la\s+)?(h0|h₀|hip[oó]tesis nula)", texto, re.I):
        return "dice «acepta H0»"
    dudosos = numeros_sin_respaldo(texto, fuentes)
    if dudosos:
        return "números que no están en el enunciado ni en la resolución: " + ", ".join(dudosos)
    if hueco == "respuesta":
        return _consistente(texto, decision, modelo)
    return None


def _limpio(texto: str) -> str:
    texto = re.sub(r"<think>.*?</think>", "", texto or "", flags=re.S).strip()
    texto = re.sub(r"^\s*(?:[-•*]|\*\*[^*]+\*\*:?)\s*", "", texto)
    return " ".join(texto.split())


def texto_de_hueco(an: Analisis, inc, res: Resultado, hueco: str, consigna: str,
                   modelo: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """(texto aceptado o None, motivo del descarte o None). Un reintento con el motivo."""
    enunciado = enunciado_texto(an)
    fuentes = enunciado + "\n" + _bloque(res)
    msgs = [{"role": "system", "content": _TEXTO_SISTEMA},
            {"role": "user", "content": f"ENUNCIADO:\n{enunciado}\n\nRESOLUCIÓN DE ESTE INCISO:\n{_bloque(res)}\n\n"
                                        f"PEDIDO: {consigna}"}]
    motivo = None
    for _ in range(2):
        texto = _limpio(cliente.chat(msgs, modelo=modelo, temperatura=0.2, max_tokens=250))
        motivo = _validar(hueco, texto, fuentes, rechaza(res), modelo)
        if motivo is None:
            return texto, None
        msgs += [{"role": "assistant", "content": texto},
                 {"role": "user", "content": f"No sirve: {motivo}. Escribilo de nuevo corrigiendo eso."}]
    return None, motivo


# ---------------------------------------------------------------------------
# 3. Armado (sin IA)
# ---------------------------------------------------------------------------

# Notas que el solver escribe para el usuario de la app (no van en el examen): las imperativas dirigidas al alumno
# («completá», «revisá»), las citas de la regla del profesor y los ejemplos «p. ej.».
_NOTA_ITALICA = re.compile(r"(?:(?<=\s)|^)_[A-ZÁÉÍÓÚ¿«][^_\n]*?_(?=\s|$|[.,;])")
_PARENTESIS_APP = re.compile(r"\s*\((?:[^()]|\([^()]*\))*?(?:profesor|p\. ej\.|regla de)(?:[^()]|\([^()]*\))*\)", re.I)
# imperativos de voseo con tilde («completá», «revisá»): «se completa el dominio» es parte de la resolución
_ORACION_APP = re.compile(r"\b(profesor|complet[aá]l[ao]|complet[aá]\w*\s+«|completá|revisá|se elige y se justifica|"
                          r"en el examen|no me gusta)", re.I)


def para_el_examen(paso: str) -> str:
    """El paso sin las notas para el usuario de la app (las cuentas no se tocan)."""
    paso = _NOTA_ITALICA.sub("", paso)
    paso = _PARENTESIS_APP.sub("", paso)
    paso = paso.replace(" (paso 1)", "")
    lineas = []
    for linea in paso.split("\n"):
        if linea.lstrip().startswith("|"):            # tablas: tal cual
            lineas.append(linea)
            continue
        oraciones = re.split(r"(?<=[.!?»])\s+(?=[A-ZÁÉÍÓÚ«•*(])", linea)
        quedan = [o for o in oraciones if not _ORACION_APP.search(o)]
        texto = " ".join(quedan).rstrip()
        if texto.strip(" •") or not linea.strip():
            lineas.append(texto)
    return "\n".join(lineas).strip()


def _repite(a: str, b: str) -> bool:
    """La respuesta dice casi lo mismo que la conclusión (no se agrega)."""
    pa, pb = set(_palabras(a)), set(_palabras(b))
    return bool(pa) and len(pa & pb) >= 0.85 * len(pa)


def armar(an: Analisis, resultados: Sequence[Resultado], textos: Dict[Tuple[str, str], str]) -> str:
    bloques = []
    una = len(an.incisos) == 1 and an.incisos[0].letra == "única"
    for inc, res in zip(an.incisos, resultados):
        b = ["### Resolución" if una else f"### {res.titulo}"]
        for e in res.errores:
            b.append(f"⚠️ {e}")
        for paso in res.pasos:
            limpio = para_el_examen(paso)
            if not limpio or limpio.startswith("**Modelos y distribuciones") and limpio.count("\n") == 0:
                continue
            if "\n|" in limpio:                        # paso con tabla: la tabla fuera de la viñeta
                texto, _, tabla = limpio.partition("\n\n")
                b += [f"- {texto}", "", tabla, ""]
            else:
                b.append(f"- {limpio}")
            letra = inc.letra.lower()
            if limpio.startswith("**Justificación de H0") and textos.get((letra, "contexto_h0")):
                b.append(f"- **En este problema**: {textos[(letra, 'contexto_h0')]}")
            if "Nivel de significación" in limpio and textos.get((letra, "alfa")):
                b.append(f"- **Por qué ese α**: {textos[(letra, 'alfa')]}")
        if res.conclusion:
            b.append(f"\n**{'7 · Conclusión' if inc.tipo == 'ensayo' else 'Conclusión'}**: {para_el_examen(res.conclusion)}")
        resp = textos.get((inc.letra.lower(), "respuesta"))
        if resp and not _repite(resp, res.conclusion or ""):
            b.append(f"\n**Respuesta**: {textos[(inc.letra.lower(), 'respuesta')]}")
        bloques.append("\n".join(b))
    texto = "\n\n".join(bloques)
    if "⟨" in texto:
        texto += ("\n\n⚠️ Quedaron huecos «⟨…⟩» que la IA no pudo completar con palabras del enunciado: completalos a "
                  "mano («Variable en palabras», «Acción si se rechaza H0»).")
    return texto


# ---------------------------------------------------------------------------
# Todo junto
# ---------------------------------------------------------------------------

def redactar_por_partes(an: Analisis, modelo: Optional[str] = None, hilos: int = 3,
                        etapa: Callable[[str], None] = lambda _: None) -> Redaccion:
    etapa("Palabras del planteo (variable, unidad, acción)")
    palabras, descartados = palabras_del_planteo(an, modelo)
    an2 = con_palabras(an, palabras)
    resultados = resolver(an2)
    otros, desc = contrarios(an2, resultados, str(palabras.get("variable") or an2.datos.get("variable") or ""), modelo)
    descartados += desc
    sin_nombre = [inc for inc, res in zip(an2.incisos, resultados)
                  if any(p.startswith("**Casos**") for p in res.pasos) and inc.letra.lower() not in otros]
    for inc in sin_nombre:      # pide lo contrario y no hay un nombre validado: el de todo el problema diría lo opuesto
        inc.params["variable"] = ""
    if otros or sin_nombre:
        palabras["incisos"] = otros
        an2 = con_palabras(an2, palabras)
        resultados = resolver(an2)
    huecos = {f"palabras.{k}": (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
              for k, v in palabras.items()}
    trabajos = [(inc, res, h, c) for inc, res in zip(an2.incisos, resultados)
                for h, c in _pedidos(an2, inc, res).items()]
    etapa(f"Textos de cada inciso ({len(trabajos)} en paralelo)")
    textos: Dict[Tuple[str, str], str] = {}
    with ThreadPoolExecutor(max_workers=max(1, hilos)) as ex:
        futuros = {ex.submit(texto_de_hueco, an2, inc, res, h, c, modelo): (inc.letra.lower(), h)
                   for inc, res, h, c in trabajos}
        for fut, clave in futuros.items():
            texto, motivo = fut.result()
            if texto:
                textos[clave] = texto
                huecos[f"{clave[0]}.{clave[1]}"] = texto
            else:
                descartados.append(f"{clave[0]}) {clave[1]}: {motivo}")
    etapa("Armando la resolución")
    return Redaccion(armar(an2, resultados, textos), an2, resultados, huecos, descartados)


def fuentes(red: Redaccion) -> str:
    """Para el checklist: el enunciado y la resolución con la que se armó el texto."""
    return enunciado_texto(red.analisis) + "\n" + resolucion_texto(red.analisis, red.resultados)
