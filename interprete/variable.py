"""Paso 1 de toda resolución (profesor): «definir la variable en palabras, con su unidad, antes de escribir un número».

- `detectar_unidad`: busca la unidad pegada a los números del planteo (x̄, μ₀, σ, S, ...): «x̄ = 246 kg», «12,5 litros».
- `paso_variable`: el paso «Variable» que va primero en la resolución (si no está escrita, un recordatorio).
- `con_unidades`: agrega la unidad a los límites y cotas de la conclusión y el nombre de la variable al parámetro
  («la media poblacional del peso de un paquete estará entre 238,19 kg y 253,81 kg»). La expresión formal
  P(A ≤ μ ≤ B) = 1 - α queda sin unidades, como la escribe el profesor.

Los temas con parámetros sin unidad (p, φ, ρ, χ²) no llevan unidad en la conclusión, pero sí el paso «Variable».
"""

import re
from typing import Dict, Optional

from .texto import fmt, normalizar

# temas con una variable medida (la que se define en el paso 1)
TEMAS_VARIABLE = ("media", "varianza", "dos_medias", "dos_varianzas", "proporcion")
# temas cuya conclusión se expresa en unidades de la variable
TEMAS_UNIDAD = ("media", "dos_medias")

UNIDADES = (r"kg|kilos?|kilogramos?|g|gr|grs|gramos?|mg|miligramos?|toneladas?|tn|quintales?|"
            r"cm|cent[ií]metros?|mm|mil[ií]metros?|m|metros?|km|kil[oó]metros?|"
            r"litros?|lts?|l|ml|cc|cm3|cm³|m3|m³|"
            r"horas?|hs|hrs?|minutos?|min|segundos?|seg|s|d[ií]as?|meses|años?|semanas?|"
            r"\$|pesos|d[oó]lares|u\$s|us\$|euros?|"
            r"kwh|kw|watts?|w|voltios?|volts?|v|amperes?|ohms?|mpa|kpa|psi|bar|"
            r"°c|grados|calor[ií]as|kcal|ppm|mg/l|km/h|m/s|rpm|"
            r"puntos?|unidades|piezas|libras?|onzas?|pulgadas?")
_RE_UNIDAD = re.compile(r"^\s*((?:" + UNIDADES + r")(?:\s*(?:por|/)\s*(?:hora|h|d[ií]a|mes|semana|minuto|min|kg|litro|unidad|año|km|m2|m²|hect[aá]rea|ha)s?)?)(?![a-záéíóúñ])", re.I)
CLAVES_NUM = ("xbar", "mu0", "desvio", "sigma0", "mu1", "e", "xbar1", "xbar2", "s1", "s2")


def _formas(v: float):
    """Cómo puede aparecer el número en el texto: 246 / 246,5 / 246.5 / 1.250 / 1250."""
    if v is None:
        return []
    out = set()
    if float(v).is_integer():
        i = int(v)
        out |= {str(i), f"{i:,}".replace(",", ".")}
    else:
        for d in range(1, 5):
            t = f"{v:.{d}f}"
            if float(t) == round(v, 6):
                out |= {t.replace(".", ","), t}
                break
    return sorted(out, key=len, reverse=True)


def detectar_unidad(texto: str, datos: Dict) -> Optional[str]:
    """La unidad que sigue a alguno de los números del planteo (en el orden de CLAVES_NUM)."""
    for clave in CLAVES_NUM:
        v = datos.get(clave)
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            continue
        for forma in _formas(float(v)):
            for m in re.finditer(r"(?<![\d.,])" + re.escape(forma) + r"(?![\d]|,\d)", texto):
                u = _RE_UNIDAD.match(texto[m.end():m.end() + 30])
                if u:
                    unidad = u.group(1)
                    if unidad.lower() in ("s", "l", "v", "w", "m", "g") and not re.match(r"^\s*" + re.escape(unidad) +
                                                                                       r"\s*[\s.,;:)]", texto[m.end():m.end() + 6]):
                        continue   # una letra suelta solo si está aislada ('25 m.' sí; '25 muestras' no)
                    return unidad
    return None


_RE_MEDIDA = re.compile(r"\b(?:medid[oa]s?|se miden?|mid[eé]ndose|expresad[oa]s?|registrad[oa]s?|en unidades de)\b"
                        r"[^.;]{0,50}?\ben\s+((?:" + UNIDADES + r"))(?![a-záéíóúñ])", re.I)


def unidad_en_palabras(texto: str) -> Optional[str]:
    """«… y se mide su espesor en milímetros» → 'milímetros' (cuando la unidad no está pegada a un número)."""
    m = _RE_MEDIDA.search(texto)
    return m.group(1) if m else None


def paso_variable(tema: str, d: Dict) -> Optional[str]:
    if tema not in TEMAS_VARIABLE:
        return None
    var, u = (d.get("variable") or "").strip(), (d.get("unidad") or "").strip()
    if tema == "proporcion":
        que = var or "⟨qué se cuenta, p. ej. «piezas defectuosas»⟩"
        return (f"**Variable** (paso 1): r = cantidad de {que} en la muestra (cada unidad es o no es uno de ellos); "
                f"p = proporción de {que} en la población." + ("" if var else _COMPLETAR_P))
    if tema in ("dos_medias", "dos_varianzas"):
        a, b = d.get("nombre1") or "1", d.get("nombre2") or "2"
        base = f"X₁ y X₂ = {var}" if var else "X₁ y X₂ = ⟨qué se mide, en palabras⟩"
        return (f"**Variable** (paso 1): {base}" + (f", en {u}" if u else ", ⟨unidad⟩") +
                f"; población 1 = {a}, población 2 = {b}." + ("" if var else _COMPLETAR))
    if var:
        return f"**Variable** (paso 1): X = {var}" + (f", en {u}" if u else "") + "."
    return ("**Variable** (paso 1): X = ⟨qué se mide, en palabras⟩" + (f", en {u}" if u else ", ⟨unidad⟩") + "." +
            _COMPLETAR)


_COMPLETAR_P = (" _Completá «Variable en palabras» con lo que se cuenta (en plural) y queda en la regla de decisión "
                "y en la conclusión._")
_COMPLETAR = (" _El profesor exige definirla antes de escribir un número (p. ej. «X: peso de un paquete, en gramos»); "
              "completala en «Variable X en palabras» y queda en las conclusiones._")


def _num(t: str) -> str:
    return r"(-?\d[\d.]*(?:,\d+)?)"


def con_unidades(texto: str, tema: str, d: Dict) -> str:
    """Unidades en los límites / cotas / estimadores de la conclusión y el nombre de la variable en el parámetro."""
    if not texto or tema not in TEMAS_UNIDAD:
        return texto
    u, var = (d.get("unidad") or "").strip(), (d.get("variable") or "").strip()
    if var:
        de = "del" if re.match(r"(el)\b", var) else "de"
        nombre = re.sub(r"^el\s+", "", var) if de == "del" else var
        texto = re.sub(r"\b(la media poblacional|el total poblacional)\b(?! de)", lambda m: f"{m.group(1)} {de} {nombre}",
                       texto, count=1)
    if not u:
        return texto
    n = _num("")
    # 'entre A y B' (no la nota 'sin redondear: A y B', ni porcentajes)
    texto = re.sub(r"\bentre " + n + r" y " + n + r"(?!\s*%)", lambda m: f"entre {m.group(1)} {u} y {m.group(2)} {u}",
                   texto, count=1)
    # cotas: 'μ ≤ 253,81: P(...)' y 'la diferencia mínima garantizada ... es 0,378'
    texto = re.sub(r"([≤≥] )" + n + r"(: P\()", lambda m: f"{m.group(1)}{m.group(2)} {u}{m.group(3)}", texto, count=1)
    texto = re.sub(r"(garantizada[^.:]*? es )" + n, lambda m: f"{m.group(1)}{m.group(2)} {u}", texto, count=1)
    # el estimador de la conclusión de un ensayo: 'x̄ = 246', 'd = 0,9'
    texto = re.sub(r"((?:x̄|d̄|d\*?) = )" + n + r"(?! ?" + re.escape(u) + ")", lambda m: f"{m.group(1)}{m.group(2)} {u}",
                   texto, count=1)
    return texto


# ---------------------------------------------------------------------------
# Qué se hace si se rechaza H0 (la RD «en lenguaje de planta» y las 4 probabilidades en términos del problema)
# ---------------------------------------------------------------------------

VERBOS = (r"modificar|cambiar|comprar|adquirir|lanzar|implementar|incorporar|reemplazar|invertir|contratar|aprobar|"
          r"adoptar|instalar|introducir|iniciar|efectuar|realizar|hacer|utilizar|usar|aplicar|habilitar|autorizar|"
          r"construir|abrir|fabricar|comercializar|ampliar|agregar|incluir|sustituir|renovar|ejecutar|emprender|"
          r"aumentar|cambiarse|pasarse|mudarse|otorgar|recomendar|certificar|homologar|denunciar|sancionar|multar")
# criterio optimista (control): rechazar H0 = detener / rechazar el lote / intervenir
VERBOS_CONTROL = (r"detener(?:lo|la)?|parar(?:lo|la)?|revisar(?:lo|la)?|rechazar(?:lo|la)?|devolver(?:lo|la)?|"
                  r"ajustar(?:lo|la)?|intervenir(?:lo|la)?|calibrar(?:lo|la)?|reparar(?:lo|la)?|suspender(?:lo|la)?|"
                  r"reclamar|recalibrar|reprocesar|descartar(?:lo|la)?")


def _re_para(verbos: str):
    return re.compile(r"\b(?:de|para|si conviene|conviene|decidir|decide|deber[ií]a)\s+(" + verbos + r")\b"
                      r"((?:\s+[\wáéíóúñü%]+){0,6})", re.I)


_PARA = _re_para(VERBOS)
_PARA_CONTROL = _re_para(VERBOS_CONTROL)
_CORTE = re.compile(r"\s+\b(cuando|si|en caso|siempre|ya que|porque|pero|y no|o no|con una|con un|en un|en una|"
                    r"durante|mientras|debido|frente|antes|luego|a partir|debe|deber[aá]|deber[ií]a|es|sea|son|"
                    r"tiene|vale|valga|ser[aá]|resulte|resulta|supere|que|se|m[aá]s|[\wáéíóúñ]+(?:ando|endo|iendo)|"
                    r"\d)\b.*$", re.I)
_NO_DECISION = re.compile(r"(efectuar|realizar|hacer|ejecutar)\s+(el|la|los|las|un|una|dicho|dicha)?\s*"
                          r"(comparaci|prueba|estudio|ensayo|experiencia|an[aá]lisis|medici|muestreo|investigaci|"
                          r"relevamiento|encuesta|control|verificaci|c[aá]lculo|evaluaci)", re.I)
_COLGANTES = {"y", "o", "de", "del", "la", "el", "los", "las", "un", "una", "en", "con", "por", "a", "al", "otra",
              "otro", "otras", "otros", "su", "sus"}


def detectar_accion(texto: str, criterio: Optional[str] = "pesimista") -> Optional[str]:
    """«probabilidad de 0,95 de modificar el sistema cuando …» → 'modificar el sistema'. Solo verbos de decisión
    (no 'estimar' ni 'calcular'); se descartan los precedidos de 'no' («de no realizar la modificación»).
    Con criterio optimista, los verbos de control («la probabilidad de detenerlo y revisarlo»)."""
    for m in (_PARA_CONTROL if criterio == "optimista" else _PARA).finditer(texto):
        if re.search(r"\bno\s*$", texto[max(0, m.start() - 4):m.start()]):
            continue
        frase = (m.group(1) + m.group(2)).strip()
        if _NO_DECISION.match(frase):
            continue                                   # «para efectuar la comparación»: el propósito del muestreo
        frase = re.sub(r"\s+[\wáéíóúñ]+mente\b", "", frase)   # «comprar equivocadamente el equipo»
        frase = re.sub(r"^(\S+)\s+o\s+\S+(?:ar|er|ir)\b", r"\1", frase)   # «rechazar o aceptar una partida»
        frase = _CORTE.sub("", frase).strip(" ,.;:")
        palabras = frase.split()
        while len(palabras) > 1 and palabras[-1].lower() in _COLGANTES:
            palabras.pop()
        frase = " ".join(palabras)
        if len(palabras) >= 2 or (criterio == "optimista" and frase):
            return frase.lower() if not frase[:2].isupper() else frase
    return None


def acciones(d: Dict):
    """(qué pasa si se rechaza H0, si no) o None. Las del sistema de control mandan; si no, la del campo «accion»."""
    if d.get("accion_rechazo"):
        return d["accion_rechazo"], d.get("accion_no_rechazo") or "no se toma esa decisión"
    acc = (d.get("accion") or "").strip()
    if acc:
        return f"corresponde {acc}", f"no corresponde {acc}"
    return None


_REL = {">": "mayor que", "<": "menor que", "≠": "distinta de", "≥": "mayor o igual que", "≤": "menor o igual que"}
_NUM = r"(-?\d[\d.]*(?:,\d+)?(?:/\d+)?)"


def h1_en_palabras(texto: str, tema: str, d: Dict) -> str:
    """'Se puede asegurar que p > 1/37' → '… que p > 1/37 (la proporción de ceros es mayor que 1/37)'."""
    var = (d.get("variable") or "").strip()
    if not var or not texto:
        return texto
    u = (d.get("unidad") or "").strip()
    nombre = {"media": f"la media de {var}", "varianza": f"el desvío de {var}", "proporcion": f"la proporción de {var}"}
    if tema not in nombre:
        return texto
    sim = {"media": "μ", "varianza": "σ", "proporcion": "p"}[tema]

    def rep(m):
        if tema == "varianza" and m.group(1) == "σ²":
            return m.group(0)
        con_u = f" {u}" if u and tema != "proporcion" else ""
        return f"{m.group(0)} ({nombre[tema]} es {_REL[m.group(2)]} {m.group(3)}{con_u})"
    return re.sub(r"(?<=asegurar que )(" + re.escape(sim) + r"²?) ([<>≠≥≤]) " + _NUM, rep, texto)


def rd_en_palabras(texto: str, tema: str, d: Dict) -> str:
    """La regla de decisión del solver ('… se rechaza H0.') con la acción y lo que se cuenta, como la escribe el
    profesor: «Si en 1637 encuestados hay 229 o más interesados, se inicia una nueva campaña; si no, no.»"""
    if not texto:
        return texto
    var = (d.get("variable") or "").strip()
    if tema == "proporcion" and var:
        texto = re.sub(r"\bcasos\b", var, texto)
        texto = re.sub(r"[Ss]e encuentran r ([≥≤]) (\d+)(?: " + re.escape(var) + r")?",
                       lambda m: f"hay {m.group(2)} o {'más' if m.group(1) == '≥' else 'menos'} {var}", texto)
    if tema == "media" and (d.get("unidad") or "").strip():
        u = d["unidad"].strip()
        texto = re.sub(r"\b(superior|inferior|mayor|menor) (a|que) " + _NUM + r"(?! ?" + re.escape(u) + ")",
                       lambda m: f"{m.group(1)} {m.group(2)} {m.group(3)} {u}", texto)
    acc = acciones(d)
    if acc and not d.get("control"):
        si, no = acc
        texto = re.sub(r"se rechaza H0\.(?=\s|$)", f"se rechaza H0: {si}; si no, {no}.", texto)
    return texto
