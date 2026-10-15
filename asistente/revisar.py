"""Solver + revisión con IA: las reglas arman el planteo, el solver calcula y la IA AUDITA que el planteo sea el del
enunciado (no solo que se pueda calcular).

    from asistente.revisar import revisar
    rv = revisar(planteo, incisos)        # rv.analisis va directo a interprete.resolver.resolver
    rv.items                              # qué se controló: confirmado / corregido / a revisar
    rv.veredicto                          # una línea para mostrar arriba

Pasos, pensados para que la IA no se ancle en lo que hicieron las reglas:
1. Números sin usar (sin IA): todo número del enunciado tiene que estar en el planteo (asistente/numeros.py).
2. Lectura a ciegas: la IA arma su propio planteo SIN ver el de las reglas, y se comparan campo por campo.
3. Arbitraje: cada diferencia y cada número sin usar se pregunta por separado, con las opciones en orden neutro
   (no se dice cuál es de las reglas) y pidiendo la cita literal del enunciado, que se verifica en el texto.
   Lo que el arbitraje corrige con una cita válida se aplica (si no rompe la resolución); lo demás queda a revisar.
4. Auditoría: con el planteo final en palabras, la IA controla inciso por inciso que responda lo que se pregunta.
"""

import copy
import difflib
import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from interprete.analizador import analizar
from interprete.modelo import CAMPOS_PLANTEO, TEMAS, TIPOS, Analisis, Inciso
from interprete.resolver import resolver
from interprete.texto import normalizar

from . import cliente
from .esquema import CAMPOS_INC, CLAVES_TEMA, a_dict, desde_dict
from .interpretar import FORMATO, _mostrar, _par, _parsear, fallas, lista_incisos, pedir_ia, puntaje
from .numeros import NumeroSinUsar, derivados_del_texto, sin_usar, valores_del_texto

# Lo que se compara entre la lectura de las reglas y la de la IA (nombres y listas largas no: mismo dato, otro texto)
IGNORAR = {"nombre1", "nombre2", "nombre_x", "nombre_y", "modelos", "r_buenas", "direccion", "sujeto_por_datos"}
# Parámetros de inciso que, si solo los ve la IA, probablemente las reglas los pasaron por alto
CLAVE_INC = {"delta0", "delta0_pct", "mu0", "p0", "sigma0", "phi0", "mu1", "p1", "sigma1", "e", "reduccion", "x0",
             "beta10", "cota", "n", "r", "p_hat", "beta", "relacion", "individual", "porcentual", "total", "costo_fijo"}

# El "marco" de la hipótesis: cola, valor de referencia y qué muestra va primero dependen entre sí, así que se comparan
# juntos (como el texto H0/H1 que arma el solver) y, si gana la lectura de la IA, se copian juntos.
MARCO_INC = {"tail", "delta0", "delta0_pct", "sujeto", "porcentual", "mu0", "p0", "sigma0", "phi0", "sobre",
             "direccion", "beta10"}
MARCO_DATOS = {"sujeto", "mu0", "p0", "sigma0", "phi0"}
TIPOS_ENSAYO = {"ensayo", "diseno", "beta", "curva", "ensayo_coef", "validacion"}

CONFIRMADO, CORREGIDO, SUGERIDO, REVISAR = "confirmado", "corregido", "sugerido", "revisar"


@dataclass
class Item:
    estado: str                 # confirmado | corregido | sugerido | revisar
    donde: str                  # "planteo" o la letra del inciso
    que: str                    # etiqueta del dato / "número sin usar" / "auditoría"
    detalle: str                # texto para mostrar
    cita: str = ""
    cambio: Optional[Tuple[str, str, Any]] = None   # (lugar, clave, valor) de una sugerencia, para aplicarla


@dataclass
class Revision:
    analisis: Analisis
    reglas: Analisis
    ciega: Optional[Analisis] = None
    items: List[Item] = field(default_factory=list)
    segundos: float = 0.0
    error: str = ""

    @property
    def corregidos(self) -> List[Item]:
        return [i for i in self.items if i.estado == CORREGIDO]

    @property
    def sugeridos(self) -> List[Item]:
        return [i for i in self.items if i.estado == SUGERIDO]

    @property
    def a_revisar(self) -> List[Item]:
        return [i for i in self.items if i.estado == REVISAR]

    @property
    def veredicto(self) -> str:
        if self.error:
            return f"No se pudo revisar con la IA: {self.error}"
        c, s, r = len(self.corregidos), len(self.sugeridos), len(self.a_revisar)
        if not c and not s and not r:
            return "✅ La IA revisó el planteo y coincide con el enunciado."
        partes = []
        if c:
            partes.append(f"🛠️ aplicó {c} cambio{'s' * (c > 1)}")
        if s:
            partes.append(f"💡 sugiere {s} cambio{'s' * (s > 1)} (no aplicado{'s' * (s > 1)})")
        if r:
            partes.append(f"⚠️ {r} punto{'s' * (r > 1)} a revisar")
        return "La revisión de la IA " + " y ".join(partes) + "."


# ---------------------------------------------------------------------------
# Comparación de lecturas
# ---------------------------------------------------------------------------

def _etiqueta(clave: str) -> str:
    return (CAMPOS_PLANTEO.get(clave) or CAMPOS_INC.get(clave) or (clave,))[0]


def _igual(a, b) -> bool:
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(float(a) - float(b)) <= 1e-6 * max(1.0, abs(float(a)))
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_igual(x, y) for x, y in zip(a, b))
    return a == b


@dataclass
class _Duda:
    id: str
    donde: str                  # "planteo" | letra
    clave: str                  # clave del dato, "tipo", o "" para números sin usar
    reglas: Any = None
    ia: Any = None
    numero: Optional[NumeroSinUsar] = None


def _efectivo(an: Analisis, inc: Inciso, clave: str):
    return inc.params.get(clave, an.datos.get(clave))


_RE_HIP = re.compile(r"H0:\s*(.+?)\s+vs\s+H1:\s*(.+?)(?:\s+\(α|\.\s|\.$|$)")


def hipotesis(an: Analisis, resultados=None) -> Dict[str, str]:
    """letra -> 'H0: ... vs H1: ...' tal como lo plantea el solver (solo incisos con ensayo)."""
    salida = {}
    for inc, res in zip(an.incisos, resultados if resultados is not None else resolver(an)):
        if inc.tipo not in TIPOS_ENSAYO or res.errores:
            continue
        m = _RE_HIP.search(re.sub(r"\*\*", "", " ".join(res.pasos)))
        if m:
            salida[inc.letra] = f"H0: {m.group(1).strip()}  vs  H1: {m.group(2).strip()}"
    return salida


_COMP = {">": "MAYOR", "<": "MENOR", "≠": "DISTINTA", "≥": "mayor o igual", "≤": "menor o igual", "=": "igual"}
_PARAM = {"μ": "la media", "p": "la proporción", "σ²": "la varianza", "σ": "el desvío", "β1": "la pendiente β1"}


def _num(t: str) -> str:
    return re.sub(r"\.0+$", "", t.strip().rstrip(".")).replace(".", ",")


def en_palabras(hip: str) -> str:
    """'H0: ... vs H1: δ = μ(nueva) - μ(vieja) > 2' -> 'H1: la media de «nueva» supera a la de «vieja» en MÁS de 2'."""
    m = re.search(r"H1:\s*(.+)$", hip)
    h1 = m.group(1).strip() if m else hip
    d = re.match(r"δ\s*=\s*μ\((.+?)\)\s*-\s*μ\((.+?)\)\s*([<>≠])\s*(-?[\d.,]+)", h1)
    if d:
        a, b, op, v = d.groups()
        v = float(v.replace(",", "."))
        if op == "≠":
            return f"H1: la diferencia entre las medias de «{a}» y «{b}» es DISTINTA de {_num(str(v))}"
        if v == 0:
            return f"H1: la media de «{a}» es {'MAYOR' if op == '>' else 'MENOR'} que la de «{b}»"
        if (op == ">") == (v > 0):
            mas, menos = (a, b) if v > 0 else (b, a)
            return f"H1: la media de «{mas}» supera a la de «{menos}» en MÁS de {_num(str(abs(v)))}"
        mas, menos = (a, b) if v > 0 else (b, a)
        return f"H1: la media de «{mas}» supera a la de «{menos}» en MENOS de {_num(str(abs(v)))} (o no la supera)"
    d = re.match(r"μ\((.+?)\)\s*([<>])\s*([\d.,]+)·μ\((.+?)\)", h1)
    if d:
        a, op, k, b = d.groups()
        pct = round((float(k.replace(",", ".")) - 1) * 100, 4)
        return (f"H1: la media de «{a}» supera a la de «{b}» en {'MÁS' if op == '>' else 'MENOS'} de un "
                f"{_num(f'{pct:g}')}%")
    d = re.match(r"(φ = σ₁/σ₂|σ²|σ|μ|p|β1)\s*([<>≠])\s*(-?[\d.,]+)", h1)
    if d:
        par, op, v = d.groups()
        nombre = "la relación de desvíos σ₁/σ₂" if par.startswith("φ") else _PARAM.get(par, par)
        return f"H1: {nombre} es {_COMP[op]} que {_num(v)}" if op != "≠" else f"H1: {nombre} es DISTINTA de {_num(v)}"
    return hip


def _canon(texto: str, an: Analisis) -> str:
    """Para comparar hipótesis de dos lecturas: nombres de muestras → [1]/[2], 2.0 → 2, sin espacios."""
    for k, marca in (("nombre1", "[1]"), ("nombre2", "[2]")):
        if an.datos.get(k):
            texto = texto.replace(str(an.datos[k]), marca)
    texto = re.sub(r"(\d+)\.0+\b", r"\1", texto)
    return re.sub(r"\s+", "", texto)


def enunciado_de(an: Analisis) -> str:
    return an.planteo + "\n" + "\n".join(i.texto for i in an.incisos if i.texto)


def _leible(v, del_texto) -> bool:
    """¿El valor se puede leer del enunciado? Números: tal cual o como % / confianza / escala; listas y tablas: todos
    sus valores (si la IA hizo cuentas para armarlas, no se discute). Lo demás (sí/no, nombres), sí."""
    if isinstance(v, bool):
        return True
    if isinstance(v, (int, float)):
        return any(_igual(float(v), x) for x in del_texto)
    if isinstance(v, (list, tuple)):
        return all(_leible(x, del_texto) for x in v)
    return True


def diferencias(reglas: Analisis, ia: Analisis) -> List[_Duda]:
    dudas: List[_Duda] = []
    if ia.tema != reglas.tema and ia.tema != "desconocido":
        dudas.append(_Duda("", "planteo", "tema", reglas.tema, ia.tema))
        return dudas                      # con otro tema las claves no se pueden comparar
    hip_r, hip_ia = hipotesis(reglas), hipotesis(ia)
    con_marco = set()                     # incisos cuya hipótesis se arbitra entera
    for k, inc in enumerate(reglas.incisos):
        par = _par(inc, k, ia)
        if par is not None and inc.letra in hip_r and par.letra in hip_ia \
                and _canon(hip_r[inc.letra], reglas) != _canon(hip_ia[par.letra], ia):
            dudas.append(_Duda("", inc.letra, "hipotesis", hip_r[inc.letra], hip_ia[par.letra]))
            con_marco.add(inc.letra)
    del_texto = valores_del_texto(enunciado_de(reglas))
    for k, v in ia.datos.items():
        if k in IGNORAR or k == "alpha" or k == "sujeto" or (con_marco and k in MARCO_DATOS):
            continue
        if v is False and k not in reglas.datos:
            continue
        if not _leible(v, del_texto):
            continue                      # la IA lo calculó o lo inventó: lo de las reglas manda (x̄ de una tabla...)
        if k not in reglas.datos or not _igual(reglas.datos[k], v):
            dudas.append(_Duda("", "planteo", k, reglas.datos.get(k), v))
    for k, inc in enumerate(reglas.incisos):
        par = _par(inc, k, ia)
        if par is None:
            continue
        if par.tipo != inc.tipo and par.tipo != "no_soportado":
            dudas.append(_Duda("", inc.letra, "tipo", inc.tipo, par.tipo))
        for c in ("alpha",) if inc.letra in con_marco else ("alpha", "tail"):
            a, b = _efectivo(reglas, inc, c), _efectivo(ia, par, c)
            if c == "alpha":
                a, b = (0.05 if a is None else a), (0.05 if b is None else b)   # lo que usa el solver por defecto
            if b is not None and not _igual(a, b) and not (c == "tail" and inc.tipo in ("ic", "n") and a is None):
                dudas.append(_Duda("", inc.letra, c, a, b))
        for c, v in par.params.items():
            if c in IGNORAR or c in ("alpha", "tail", "tema") or c in reglas.datos or \
                    (inc.letra in con_marco and c in MARCO_INC):
                continue
            if not _leible(v, del_texto) or (v is False and c not in inc.params):
                continue
            if c in inc.params and not _igual(inc.params[c], v):
                dudas.append(_Duda("", inc.letra, c, inc.params[c], v))
            elif c not in inc.params and c in CLAVE_INC:
                dudas.append(_Duda("", inc.letra, c, None, v))
    return dudas


# ---------------------------------------------------------------------------
# Arbitraje
# ---------------------------------------------------------------------------

ARBITRO = """Sos un revisor MUY minucioso de planteos de Estadística Aplicada (UADE). Dos lectores independientes leyeron \
el mismo enunciado y no coinciden en algunos datos; además puede haber números del enunciado que nadie usó. \
Para cada pregunta decidí qué dice REALMENTE el enunciado. No supongas que alguna opción es la buena: releé el texto.

Reglas:
- Justificá cada respuesta con una CITA LITERAL y corta del enunciado (copiada tal cual, máximo 25 palabras).
- Si ninguna opción es correcta elegí "C" y poné el valor correcto en "valor".
- Números como decimales JSON; porcentajes como fracción (5% -> 0.05). alpha = 1 - confianza.
- Si un número no se usó y SÍ hace falta (un total que hay que dividir, un valor de referencia, una diferencia \
"al menos X más"), elegí "B" y decí en "clave" qué dato es (de la lista) y en "valor" cuánto vale ya expresado \
como lo pide la clave (p. ej. un total de 8160 en 16 unidades -> clave "xbar", valor 510).
- Si el número es un porcentaje DE otro valor ("un error del 2% del promedio"), el valor va ya calculado \
(2% de 80 -> 1.6), no 0.02.
- Si el número es contexto (edad, un nombre, cantidad de máquinas, una unidad), elegí "A".

Respondé SOLO con JSON: {"respuestas": [{"id": "...", "opcion": "A"|"B"|"C", "clave": "...", "valor": ..., \
"cita": "...", "motivo": "..."}]}"""


def _orden(semilla: str) -> bool:
    """Orden de las opciones estable pero sin patrón (que la IA no aprenda 'A = reglas')."""
    return hashlib.md5(semilla.encode()).digest()[0] % 2 == 0


def _texto_valor(clave: str, v) -> str:
    if v is None:
        return "no figura / no se usa"
    if clave == "tipo":
        return f"{v} ({TIPOS.get(v, v)})"
    if clave == "tema":
        return f"{v} ({TEMAS.get(v, v)})"
    if clave == "hipotesis":
        return en_palabras(str(v))
    if clave == "tail":
        return {"derecha": "H1: el parámetro es MAYOR", "izquierda": "H1: el parámetro es MENOR",
                "bilateral": "H1: el parámetro es DISTINTO"}.get(v, str(v))
    return _mostrar(v)


def _preguntas(dudas: List[_Duda], tema: str) -> Tuple[str, Dict[str, Dict[str, Any]]]:
    lineas, opciones = [], {}
    claves_tema = CLAVES_TEMA.get(tema, (list(CAMPOS_PLANTEO), list(CAMPOS_INC)))
    for d in dudas:
        lugar = "el planteo" if d.donde == "planteo" else f"el inciso {d.donde})"
        if d.numero is not None:
            n = d.numero
            lineas.append(f'{d.id}: el número «{n.crudo}» de {lugar} («…{n.contexto}…») no se usa en ningún dato. '
                          f"A) es contexto, no hace falta. B) hace falta (indicá clave y valor).")
            continue
        a, b = (d.reglas, d.ia) if _orden(d.id + d.clave) else (d.ia, d.reglas)
        opciones[d.id] = {"A": a, "B": b}
        if d.clave == "hipotesis":
            lineas.append(f"{d.id}: en {lugar}, ¿qué es lo que el ensayo tiene que DEMOSTRAR (H1) para responder la "
                          f"pregunta? A) {en_palabras(a)}.  B) {en_palabras(b)}.  C) ninguna de las dos")
            continue
        lineas.append(f"{d.id}: en {lugar}, {_etiqueta(d.clave)} ({d.clave}) — A) {_texto_valor(d.clave, a)}  "
                      f"B) {_texto_valor(d.clave, b)}  C) otro valor")
    lineas.append("\nClaves posibles para 'clave' (tema " + tema + "): datos = " + ", ".join(
        f"{k} ({_etiqueta(k)})" for k in claves_tema[0]) + "; incisos = " + ", ".join(claves_tema[1]))
    return "\n".join(lineas), opciones


def _cita_valida(cita: str, texto: str) -> bool:
    """La cita tiene que estar en el enunciado (se toleran tildes, espacios, puntuación y algún error de tipeo)."""
    def limpio(s):
        return re.sub(r"[^a-z0-9%]+", " ", normalizar(s)).strip()
    c, t = limpio(cita), limpio(texto)
    if len(c) < 4:
        return False
    if c in t:
        return True
    m = difflib.SequenceMatcher(None, t, c, autojunk=False).find_longest_match(0, len(t), 0, len(c))
    if m.size >= 0.6 * len(c):
        ini = max(0, m.a - m.b)
        return difflib.SequenceMatcher(None, t[ini:ini + len(c)], c).ratio() >= 0.85
    return False


def _valor_de(clave: str, v, avisos: List[str]):
    """Convierte el valor del árbitro con las mismas reglas que desde_dict."""
    if clave in ("tipo", "tema"):
        return v if isinstance(v, str) else None
    tipo = (CAMPOS_PLANTEO.get(clave) or CAMPOS_INC.get(clave) or (None, None))[1]
    if tipo is None:
        return None
    from .esquema import _valor
    return _valor(clave, v, tipo, avisos, "")


def _mismo_orden(a: Analisis, b: Analisis) -> bool:
    """¿Las dos lecturas tienen las muestras en el mismo orden (1 y 2)?"""
    for c1, c2 in (("n1", "n2"), ("xbar1", "xbar2"), ("s1", "s2")):
        if c1 in a.datos and c1 in b.datos and c2 in a.datos and c2 in b.datos:
            if _igual(a.datos[c1], b.datos[c2]) and _igual(a.datos[c2], b.datos[c1]) and \
                    not _igual(a.datos[c1], b.datos[c1]):
                return False
    return True


def aplicar_marco(an: Analisis, letra: str, ia: Analisis) -> bool:
    """Copia la hipótesis de la lectura de la IA (cola, referencia, sujeto...) al inciso `letra` de `an`."""
    k, inc = next(((k, i) for k, i in enumerate(an.incisos) if i.letra == letra), (None, None))
    if inc is None:
        return False
    par = _par(inc, k, ia)
    if par is None:
        return False
    for c in MARCO_INC:
        inc.params.pop(c, None)
        if c in par.params:
            inc.params[c] = par.params[c]
    for c in MARCO_DATOS:
        if c in ia.datos:
            an.datos[c] = ia.datos[c]
    if not _mismo_orden(an, ia):              # la IA numeró las muestras al revés
        for d in (an.datos, inc.params):
            if d.get("sujeto") in (1, 2):
                d["sujeto"] = 3 - d["sujeto"]
    return True


def _aplicar(an: Analisis, donde: str, clave: str, valor, ia: Optional[Analisis] = None) -> bool:
    if clave == "hipotesis":
        return ia is not None and aplicar_marco(an, donde, ia)
    if clave == "tema":
        return False                       # el tema se resuelve aparte (se re-analiza con ese tema)
    if donde == "planteo":
        if valor is None:
            an.datos.pop(clave, None)
        else:
            an.datos[clave] = valor
        return True
    inc = next((i for i in an.incisos if i.letra == donde), None)
    if inc is None:
        return False
    if clave == "tipo":
        inc.tipo = valor
    elif valor is None:
        inc.params.pop(clave, None)
    elif clave in CAMPOS_PLANTEO and clave not in CAMPOS_INC:
        an.datos[clave] = valor
    else:
        inc.params[clave] = valor
    return True


# ---------------------------------------------------------------------------
# Auditoría final
# ---------------------------------------------------------------------------

AUDITOR = """Sos un profesor de Estadística Aplicada (UADE) corrigiendo un planteo. Te doy el enunciado y lo que un \
programa va a resolver en cada inciso. Controlá con mucho cuidado, inciso por inciso, que el programa responda \
EXACTAMENTE lo que se pregunta: el parámetro correcto (proporción DE QUÉ, media o total, desvío o varianza), la \
población correcta, el sentido de H1 (quién tiene que ser mayor), el valor de referencia (incluida una diferencia \
"al menos X"), el riesgo, y que los datos sean los del enunciado (no un total en lugar de un promedio, ni la varianza \
en lugar del desvío). No juzgues las cuentas: solo el planteo. Si está bien, decilo; no inventes problemas.

Respondé SOLO con JSON: {"incisos": [{"letra": "a", "correcto": true|false, "problema": "...", "cita": "..."}]} \
("cita": fragmento literal del enunciado que muestra el problema)."""


def _describir(an: Analisis, resultados) -> str:
    lineas = [f"Tema: {TEMAS.get(an.tema, an.tema)}", "Datos:"]
    lineas += [f"- {_etiqueta(k)} = {_mostrar(v)}" for k, v in an.datos.items() if k not in IGNORAR]
    for inc, res in zip(an.incisos, resultados):
        lineas.append(f"\nInciso {inc.letra}) — {TIPOS.get(inc.tipo, inc.tipo)}")
        if inc.params.get("tema"):
            lineas.append(f"  (de otro parámetro: {TEMAS.get(inc.params['tema'])})")
        lineas += [f"  - {_etiqueta(k)} = {_mostrar(v)}" for k, v in inc.params.items() if k not in IGNORAR | {"tema"}]
        hip = [p for p in res.pasos if "H0" in p][:1]
        if hip:
            lineas.append("  " + re.sub(r"\*\*", "", hip[0])[:300])
        if res.resumen:
            lineas.append(f"  Resultado: {res.resumen[:200]}")
        if res.errores:
            lineas.append(f"  (no se pudo calcular: {res.errores[0][:120]})")
    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# Revisión completa
# ---------------------------------------------------------------------------

def _pedir_json(sistema: str, usuario: str, modelo, pensar) -> Dict:
    salida = cliente.chat([{"role": "system", "content": sistema}, {"role": "user", "content": usuario}],
                          modelo=modelo, formato=FORMATO, pensar=pensar, temperatura=0)
    return _parsear(salida)


def revisar(planteo: str, incisos=None, tablas=None, modelo: Optional[str] = None, pensar: bool = False,
            analisis: Optional[Analisis] = None, excluir: Sequence[str] = (), auditar: bool = False) -> Revision:
    """Resuelven las reglas (o `analisis`, si ya está armado) y la IA revisa el planteo."""
    reglas = analisis if analisis is not None else analizar(planteo, incisos, tablas=tablas)
    rv = Revision(analisis=reglas, reglas=reglas)
    t0 = time.time()
    texto_pl, lista = lista_incisos(planteo, incisos)
    enunciado = texto_pl + "\n" + "\n".join(f"{l}) {t}" for l, t in lista)
    try:
        # 1) números sin usar
        dudas: List[_Duda] = [_Duda("", n.donde, "", numero=n) for n in sin_usar(reglas, lista) if not n.lista]
        # 2) lectura a ciegas
        ciega, _ = pedir_ia(planteo, incisos, tablas, modelo, pensar, borrador=None, excluir=excluir)
        rv.ciega = ciega
        dudas += diferencias(reglas, ciega)
        for k, d in enumerate(dudas):
            d.id = f"P{k + 1}"
        # 3) arbitraje
        actual = copy.deepcopy(reglas)
        if any(d.clave == "tema" for d in dudas):
            d = next(x for x in dudas if x.clave == "tema")
            r = _pedir_json(ARBITRO, f"ENUNCIADO:\n{enunciado}\n\nPREGUNTAS:\n" + _preguntas([d], reglas.tema)[0],
                            modelo, pensar)
            elegido = _elegido(r, d, {"A": d.reglas, "B": d.ia} if _orden(d.id + d.clave) else
                               {"A": d.ia, "B": d.reglas}, enunciado)
            if elegido and elegido[0] == d.ia:
                forzado = analizar(planteo, incisos, tablas=tablas, tema=d.ia)
                p_ia, p_reglas = puntaje(forzado, resolver(forzado)), puntaje(reglas, resolver(reglas))
                if p_ia > p_reglas and not _resuelve_todo(reglas):
                    actual = forzado
                    rv.items.append(Item(CORREGIDO, "planteo", "Tema", f"{TEMAS[d.reglas]} → **{TEMAS[d.ia]}**",
                                         elegido[1]))
                elif p_ia >= p_reglas:
                    rv.items.append(Item(SUGERIDO, "planteo", "Tema", f"{TEMAS[d.reglas]} → **{TEMAS[d.ia]}**",
                                         elegido[1], ("planteo", "tema", d.ia)))
                else:
                    rv.items.append(Item(REVISAR, "planteo", "Tema", f"La IA cree que es **{TEMAS[d.ia]}**, pero "
                                         f"con ese tema se resuelve menos.", elegido[1]))
            else:
                rv.items.append(Item(CONFIRMADO, "planteo", "Tema", TEMAS[reglas.tema]))
            # con el tema decidido se vuelve a comparar (si la IA leyó otro tema, solo quedan los números)
            dudas = [_Duda("", n.donde, "", numero=n) for n in sin_usar(actual, lista) if not n.lista]
            dudas += [x for x in diferencias(actual, ciega) if x.clave != "tema"]
            for k, d in enumerate(dudas):
                d.id = f"P{k + 1}"
        if dudas:
            texto, opciones = _preguntas(dudas, actual.tema)
            r = _pedir_json(ARBITRO, f"ENUNCIADO:\n{enunciado}\n\nPREGUNTAS:\n{texto}", modelo, pensar)
            actual = _arbitrar(r, dudas, opciones, actual, enunciado, rv)
        # si el planteo no se resolvía y ninguna sugerencia sola alcanzaba (p. ej. x e y de una regresión van juntas),
        # se prueban todas juntas: si así se resuelve más, sin perder nada, se aplican
        if rv.sugeridos and fallas(actual, resolver(actual)) and not any(i.cambio[1] == "tema" for i in rv.sugeridos):
            rv.analisis = actual
            todo = aplicar_sugerencias(rv, rv.sugeridos)
            antes = set(range(len(actual.incisos))) - set(fallas(actual, resolver(actual)))
            despues = set(range(len(todo.incisos))) - set(fallas(todo, resolver(todo)))
            if antes < despues:
                todo.avisos = list(actual.avisos)
                actual = todo
                rv.items = [Item(CORREGIDO, i.donde, i.que, i.detalle, i.cita) if i.estado == SUGERIDO else i
                            for i in rv.items]
        rv.analisis = actual
        # listas de datos que siguen sin usarse: no se arbitran número por número, se avisan
        for n in sin_usar(actual, lista):
            if n.lista:
                rv.items.append(Item(REVISAR, n.donde, "Datos sin usar", f"La lista «{n.crudo}» del enunciado no se "
                                     f"usa en el planteo: cargala en el dato que corresponda."))
        # 4) auditoría del planteo final
        if auditar:
            res = resolver(actual)
            r = _pedir_json(AUDITOR, f"ENUNCIADO:\n{enunciado}\n\nLO QUE VA A RESOLVER EL PROGRAMA:\n"
                            f"{_describir(actual, res)}", modelo, pensar)
            for x in r.get("incisos") or []:
                if isinstance(x, dict) and x.get("correcto") is False and str(x.get("problema") or "").strip():
                    cita = str(x.get("cita") or "")
                    letra = str(x.get("letra") or "").strip(") ").lower() or "planteo"
                    nota = "" if _cita_valida(cita, enunciado) else " (sin cita verificable en el enunciado)"
                    rv.items.append(Item(REVISAR, letra, "Auditoría", str(x["problema"]).strip() + nota, cita))
    except cliente.ErrorIA as e:
        rv.error = str(e)
    finally:
        rv.segundos = time.time() - t0
    if rv.corregidos:
        rv.analisis.avisos = list(rv.analisis.avisos) + [f"🛠️ Revisión IA: {i.que}: {i.detalle}"
                                                         for i in rv.corregidos]
    return rv


def _resuelve_todo(an: Analisis) -> bool:
    return not fallas(an, resolver(an))


def aplicar_sugerencias(rv: Revision, items: Sequence[Item], planteo: str = "", incisos=None,
                        tablas=None) -> Analisis:
    """El planteo con las sugerencias elegidas aplicadas. Un cambio de tema re-analiza desde el enunciado (y descarta
    las demás sugerencias, que eran del otro tema)."""
    tema = next((i.cambio[2] for i in items if i.cambio and i.cambio[1] == "tema"), None)
    if tema is not None:
        return analizar(planteo, incisos, tablas=tablas, tema=tema)
    an = copy.deepcopy(rv.analisis)
    for i in items:
        if i.cambio:
            _aplicar(an, *i.cambio, rv.ciega)
    an.avisos = list(an.avisos) + [f"🛠️ Revisión IA: {i.que}: {i.detalle}" for i in items if i.cambio]
    return an


def _elegido(r: Dict, d: _Duda, opciones: Dict[str, Any], enunciado: str) -> Optional[Tuple[Any, str, str]]:
    """(valor elegido, cita, opción) si la respuesta trae una cita válida; None si no."""
    for x in r.get("respuestas") or []:
        if not isinstance(x, dict) or str(x.get("id")) != d.id:
            continue
        op = str(x.get("opcion") or "").strip().upper()[:1]
        cita = str(x.get("cita") or "")
        if not _cita_valida(cita, enunciado):
            return None
        if op in ("A", "B"):
            return opciones[op], cita, op
        if op == "C":
            return x.get("valor"), cita, op
    return None


def _arbitrar(r: Dict, dudas: List[_Duda], opciones: Dict, actual: Analisis, enunciado: str,
              rv: Revision) -> Analisis:
    respuestas = {str(x.get("id")): x for x in (r.get("respuestas") or []) if isinstance(x, dict)}
    base_res = resolver(actual)
    for d in dudas:
        x = respuestas.get(d.id)
        lugar = "planteo" if d.donde == "planteo" else d.donde
        if d.numero is not None:
            n = d.numero
            op = str((x or {}).get("opcion") or "").strip().upper()[:1]
            if x is None:
                rv.items.append(Item(REVISAR, lugar, "Número sin usar", f"«{n.crudo}» («…{n.contexto}…») no se usó "
                                     f"y la IA no respondió."))
                continue
            if op != "B":
                continue                    # contexto: no se informa (sería ruido)
            clave, avisos = str(x.get("clave") or ""), []
            if clave in MARCO_INC | MARCO_DATOS and any(o.clave == "hipotesis" for o in dudas):
                continue                    # lo decide la pregunta por la hipótesis completa
            valor = _valor_de(clave, x.get("valor"), avisos)
            cita = str(x.get("cita") or "")
            texto = f"«{n.crudo}» no se usaba: la IA dice que es {_etiqueta(clave)} = {_mostrar(valor)}."
            motivo = _motivo_numero(actual, lugar, clave, valor, enunciado)
            if motivo is None and not _cita_valida(cita, enunciado):
                motivo = "sin cita verificable"
            if motivo:
                rv.items.append(Item(REVISAR, lugar, "Número sin usar", f"«{n.crudo}» («…{n.contexto}…») no se usa"
                                     + (f"; la IA propone {_etiqueta(clave)} = {_mostrar(valor)}" if valor is not None
                                        else "") + f" (no se aplicó: {motivo}).", cita))
                continue
            actual, base_res = _probar(actual, base_res, lugar, clave, valor, rv, "Número sin usar", texto, cita)
            continue
        el = _elegido({"respuestas": [x]} if x else {}, d, opciones.get(d.id, {}), enunciado)
        etiqueta = {"tipo": "Tipo de inciso", "hipotesis": "Hipótesis"}.get(d.clave) or _etiqueta(d.clave)
        if el is None:
            # sin una cita del enunciado que la respalde, la otra lectura no alcanza para dudar de las reglas
            rv.items.append(Item(CONFIRMADO, lugar, etiqueta, f"{_texto_valor(d.clave, d.reglas)} (la IA leyó "
                                 f"{_texto_valor(d.clave, d.ia)}, sin respaldo en el enunciado)"))
            continue
        valor, cita, op = el
        if op != "C" and _igual(valor, d.reglas):
            rv.items.append(Item(CONFIRMADO, lugar, etiqueta, _texto_valor(d.clave, valor), cita))
            continue
        if d.clave == "tail":
            valor = _cola(valor)
        elif d.clave == "tipo":
            valor = valor if valor in TIPOS else None
        elif d.clave != "hipotesis":
            valor = _valor_de(d.clave, valor, [])
            if op == "C" and isinstance(valor, (int, float)) and not isinstance(valor, bool) and \
                    not _leible(valor, valores_del_texto(enunciado)):
                valor = None                # un "otro valor" que no está en el enunciado no se aplica
        if valor is None and d.clave != "hipotesis":
            rv.items.append(Item(REVISAR, lugar, etiqueta, f"Las lecturas no coinciden "
                                 f"({_texto_valor(d.clave, d.reglas)} vs {_texto_valor(d.clave, d.ia)}) y la IA "
                                 "propuso un valor que no se puede verificar.", cita))
            continue
        elif d.clave == "hipotesis" and op == "C":
            rv.items.append(Item(REVISAR, lugar, etiqueta, "Ninguna de las dos hipótesis convence a la IA: "
                                 f"{_texto_valor('hipotesis', d.reglas)} / {_texto_valor('hipotesis', d.ia)}.", cita))
            continue
        texto = f"{_texto_valor(d.clave, d.reglas)} → **{_texto_valor(d.clave, valor)}**"
        actual, base_res = _probar(actual, base_res, lugar, d.clave, valor, rv, etiqueta, texto, cita)
    return actual


def _motivo_numero(an: Analisis, lugar: str, clave: str, valor, enunciado: str) -> Optional[str]:
    """Por qué NO aplicar lo que propone el árbitro para un número sin usar (None = se puede aplicar)."""
    datos_tema, params_tema = CLAVES_TEMA.get(an.tema, (list(CAMPOS_PLANTEO), list(CAMPOS_INC)))
    tipo = (CAMPOS_PLANTEO.get(clave) or CAMPOS_INC.get(clave) or (None, None))[1]
    if clave not in set(datos_tema) | set(params_tema) or tipo not in ("float", "int"):
        return f"«{clave}» no es un dato numérico de este tema" if clave else "no dijo qué dato es"
    if valor is None:
        return "valor inválido"
    escalares = [v for v in an.datos.values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    if not any(_igual(float(valor), x) for x in derivados_del_texto(enunciado, escalares)):
        return "ese valor no sale del enunciado (la IA hizo una cuenta que no se puede verificar)"
    inc = next((i for i in an.incisos if i.letra == lugar), None)
    actual = inc.params.get(clave, an.datos.get(clave)) if inc is not None else an.datos.get(clave)
    if actual is not None and not _igual(actual, valor) and clave != "alpha":
        return f"ya hay {_etiqueta(clave)} = {_mostrar(actual)}: el enunciado tiene dos valores, decidí vos cuál va"
    return None


_COLA_TEXTO = (("distint", "bilateral"), ("≠", "bilateral"), ("bilateral", "bilateral"), ("menor", "izquierda"),
               ("izquierda", "izquierda"), ("<", "izquierda"), ("mayor", "derecha"), ("derecha", "derecha"),
               (">", "derecha"))


def _cola(v) -> Optional[str]:
    t = str(v or "").lower()
    return next((c for k, c in _COLA_TEXTO if k in t), None)


def _probar(actual: Analisis, base_res, lugar: str, clave: str, valor, rv: Revision, que: str, texto: str,
            cita: str):
    """Aplica una corrección solo si hace resolver algo que no se resolvía (sin romper nada). Si el planteo de las
    reglas ya resolvía todo, el cambio queda como sugerencia: en la guía, pisar planteos que resuelven rompía más
    ejercicios de los que arreglaba."""
    prueba = copy.deepcopy(actual)
    if not _aplicar(prueba, lugar, clave, valor, rv.ciega):
        rv.items.append(Item(REVISAR, lugar, que, texto + " (no se pudo aplicar)", cita))
        return actual, base_res
    res = resolver(prueba)
    antes = set(range(len(actual.incisos))) - set(fallas(actual, base_res))
    despues = set(range(len(prueba.incisos))) - set(fallas(prueba, res))
    if antes < despues:
        rv.items.append(Item(CORREGIDO, lugar, que, texto, cita))
        return prueba, res
    if antes <= despues:
        rv.items.append(Item(SUGERIDO, lugar, que, texto, cita, (lugar, clave, valor)))
        return actual, base_res
    rv.items.append(Item(REVISAR, lugar, que, texto + " (no se aplicó: con ese cambio deja de resolverse)", cita))
    return actual, base_res
