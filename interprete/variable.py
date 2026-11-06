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
TEMAS_VARIABLE = ("media", "varianza", "dos_medias", "dos_varianzas")
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


def paso_variable(tema: str, d: Dict) -> Optional[str]:
    if tema not in TEMAS_VARIABLE:
        return None
    var, u = (d.get("variable") or "").strip(), (d.get("unidad") or "").strip()
    if tema in ("dos_medias", "dos_varianzas"):
        a, b = d.get("nombre1") or "1", d.get("nombre2") or "2"
        base = f"X₁ y X₂ = {var}" if var else "X₁ y X₂ = ⟨qué se mide, en palabras⟩"
        return (f"**Variable** (paso 1): {base}" + (f", en {u}" if u else ", ⟨unidad⟩") +
                f"; población 1 = {a}, población 2 = {b}." + ("" if var else _COMPLETAR))
    if var:
        return f"**Variable** (paso 1): X = {var}" + (f", en {u}" if u else "") + "."
    return ("**Variable** (paso 1): X = ⟨qué se mide, en palabras⟩" + (f", en {u}" if u else ", ⟨unidad⟩") + "." +
            _COMPLETAR)


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
