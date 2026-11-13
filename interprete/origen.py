"""¿De dónde sale cada número? (regla del profesor: «un resultado sin desarrollo lo sacaste de la galera»).

    from interprete.origen import sin_origen
    sin_origen(resolucion, enunciado)   # ['0,4111', '0,4769'] = números que aparecen sin fórmula ni dato

Un número tiene origen si:
- está en el enunciado (o es su complemento / porcentaje: 95 % → 0,95 y α = 0,05), o
- en algún lugar de la resolución aparece como resultado de una cuenta o de una tabla: a la derecha de un «=» cuyo
  lado izquierdo tiene operaciones, números o una función (Z(0,95) = 1,6449, (10,52 - 10,5)/0,41 = 0,0579,
  P(Z ≥ 0,0579) = 0,4769), o redondeado con «→» / «⇒» desde una cuenta (29,5365 → n = 30).

Un «β = 0,4769» suelto (solo el símbolo a la izquierda) NO es origen: es el resultado sin decir de dónde salió.
Se ignoran los enteros chicos (incisos, pasos, grados de libertad de una cuenta simple) y las tablas markdown
(las tablas son el desarrollo).
"""

import re
from typing import List, Sequence

from .texto import buscar_numeros

_CORTE = re.compile(r"(?:\.\s|;\s|\n|•|\*\*|:\s|,\s(?=[A-Za-zÁÉÍÓÚáéíóúñ]))")
_OPERACION = re.compile(r"[\d+·*/√²³^()\[\]Σ∛−]|(?<![A-Za-z])-|\b(?:máx|mín|max|min|ln|log|exp)\b")


def _decimales(crudo: str) -> int:
    crudo = crudo.replace("%", "").strip()
    sep = "," if "," in crudo else ("." if "." in crudo else None)
    if sep is None:
        return 0
    cola = crudo.rsplit(sep, 1)[1]
    return len(cola) if cola.isdigit() and len(cola) != 3 or sep == "," else 0


def _iguala(valor: float, crudo: str, base: Sequence[float], afuera: bool = False) -> bool:
    """`afuera`: también vale el redondeo hacia afuera de un resultado (238,197774 informado como 238,19)."""
    tol = (1.0 if afuera else 0.5) * 10 ** -_decimales(crudo) + 1e-9
    return any(abs(valor - k) <= max(tol, abs(k) * 1e-9) for k in base)


# umbrales y constantes de la cátedra que se citan como regla, no salen de una cuenta: n ≥ 30 (prohibida), n·p > 10,
# p ≤ 0,005, Mermoz 0,23, N ≥ 60 y Fe ≥ 5 en chi², fuerza de r² 0,4 / 0,6 / 0,8
# y la escala de α del profesor (chico 0,01, estándar 0,05, grande 0,10), que se elige y se justifica
CONSTANTES = (30, 10, 0.005, 0.23, 60, 5, 0.4, 0.6, 0.8, 0.01, 0.05, 0.1, 0.9, 0.95, 0.99, 0.5, 100)

# los argumentos de una función de tabla son su probabilidad y sus grados de libertad, no resultados
_ARGUMENTOS = re.compile(r"(?<![A-Za-zα-ω])(?:t|F|Z|z|χ²|chi²|G_b|F_b|G_p|F_p)\s*\(([^()]*)\)")


def _sin_tablas(texto: str) -> str:
    """Las filas de tablas markdown, las citas («…», «el profesor …») y los argumentos de las funciones de tabla
    (F(0,95; 4; 18)) se blanquean, conservando posiciones."""
    texto = "\n".join(" " * len(l) if l.lstrip().startswith("|") else l for l in texto.split("\n"))
    texto = re.sub(r"«[^»\n]*»|\(el profesor[^)\n]*\)", lambda m: " " * len(m.group(0)), texto)
    return _ARGUMENTOS.sub(lambda m: m.group(0)[:m.start(1) - m.start(0)] + "_" * len(m.group(1)) + ")", texto)


def _de_tablas(texto: str) -> List[float]:
    """Los números de las tablas markdown: la tabla es el desarrollo (Fo, Fe, aportes, sumatorias)."""
    return [n.valor for l in texto.split("\n") if l.lstrip().startswith("|") for n in buscar_numeros(l)]


_ABRE, _CIERRA = "([", ")]"
_FUNCION_TABLA = re.compile(r"^[√]?\s*(?:t|F|Z|z|χ²|chi²|G_b|F_b|G_p|F_p|P|Φ)\s*\(")


def _profundidades(texto: str) -> List[int]:
    """Profundidad de paréntesis / corchetes en cada posición (se reinicia en cada renglón)."""
    prof, d = [], 0
    for ch in texto:
        if ch == "\n":
            d = 0
        if ch in _CIERRA:
            d = max(0, d - 1)
        prof.append(d)
        if ch in _ABRE:
            d += 1
    return prof


def _inicio_tramo(texto: str, prof: List[int], ini: int) -> int:
    """Dónde empieza la frase del número: el último corte (. ; : salto, viñeta) fuera de paréntesis."""
    d0 = prof[ini] if ini < len(prof) else 0
    for m in reversed(list(_CORTE.finditer(texto, max(0, ini - 300), ini))):
        if prof[m.start()] <= d0:
            return m.end()
    return max(0, ini - 300)


def _terminos(expr: str) -> List[str]:
    """Términos de una expresión, separados por + - · / fuera de paréntesis."""
    salida, d, actual = [], 0, ""
    for i, ch in enumerate(expr):
        if ch in _ABRE:
            d += 1
        elif ch in _CIERRA:
            d -= 1
        if d == 0 and ch in "+·/*∓±−" or (d == 0 and ch == "-" and i and expr[i - 1] == " "):
            salida.append(actual.strip())
            actual = ""
        else:
            actual += ch
    salida.append(actual.strip())
    return [t.strip("()[]²√ ") for t in salida if t.strip("()[]²√ ")]


def _es_reemplazo_de_tabla(texto: str, ini: int, tramo_ini: int) -> bool:
    """«δ₀ + t(0,95; 7)·σ(d) = 2 + 1,8946·1,810189»: 1,8946 ocupa el lugar de t(0,95; 7), un valor de tabla."""
    prof = _profundidades(texto)
    d0 = prof[ini]
    iguales = [i for i in range(tramo_ini, ini) if texto[i] == "=" and prof[i] == d0]
    if not iguales:
        return False
    fin = len(texto)
    for j in range(ini, len(texto)):
        if (texto[j] in "=\n" or texto[j:j + 2] in (". ", "; ")) and prof[j] <= d0:
            fin = j
            break
    formula = texto[(iguales[-2] + 1) if len(iguales) > 1 else tramo_ini:iguales[-1]]
    reemplazo = texto[iguales[-1] + 1:fin]
    tf, tr = _terminos(formula), _terminos(reemplazo)
    if len(tf) != len(tr):
        return False
    pos = len(_terminos(texto[iguales[-1] + 1:ini] + "X")) - 1
    return 0 <= pos < len(tf) and bool(_FUNCION_TABLA.search(tf[pos]))


def _es_resultado(texto: str, ini: int) -> bool:
    """¿El número que empieza en `ini` es el resultado de una cuenta o de una tabla?"""
    prof = _profundidades(texto)
    d0 = prof[ini]
    if d0 > 0:      # dentro de corchetes: = [0,898 ; 4,9126] o = máx[854,7 ; 854,8]
        k = ini
        while k > 0 and not (texto[k - 1] in _ABRE and prof[k - 1] == d0 - 1):
            k -= 1
        if re.search(r"=\s*(?:máx|mín|max|min)?\s*$", texto[max(0, k - 12):k - 1]):
            return True
    if re.search(r"=\s*-?[\d.,]+\s*;\s*$", texto[max(0, ini - 40):ini]):   # A ; B = 3,25 ; 5,75
        return True
    t0 = _inicio_tramo(texto, prof, ini)
    tramo = texto[t0:ini].rstrip()
    if tramo.endswith(("-", "−")) and tramo[:-1].rstrip().endswith(("=", "≈")):   # = -3,75
        tramo = tramo[:-1].rstrip()
    if re.search(r"=\s*-?[\d.,]+\s*[∓±+-]$", tramo):                # = 246 ∓ 7,8022 (el error de la cuenta)
        return True
    if not tramo.endswith(("=", "≈")):
        return _es_reemplazo_de_tabla(texto, ini, t0)
    lhs = tramo[:-1]
    if re.search(r"[=≈→⇒]", lhs):        # cadena a = b = c, o un redondeo «29,5365 → n = 30»
        return True
    # el lado izquierdo tiene una cuenta o una función (Z(0,95), P(…), F_b(10 | …)); S² o σ² pelados no cuentan
    return bool(_OPERACION.search(re.sub(r"[Sσsφψ]²", "", lhs)))


def conocidos(enunciado: str) -> List[float]:
    base = []
    for n in buscar_numeros(enunciado):
        base.append(n.valor)
        if n.pct:
            base.append(n.valor / 100)
    base += [v - k for v in base if float(v).is_integer() and v > 2 for k in (1, 2)]   # ν = n − 1, n₁ + n₂ − 2
    base += [1 - v for v in base if 0 < v < 1]                 # 90 % de confianza → α = 0,1
    base += [v / 2 for v in base if 0 < v < 0.5] + [1 - v / 2 for v in base if 0 < v < 0.5]   # → 0,05 y 0,95
    return base + [v * 100 for v in base if 0 < v < 1] + list(CONSTANTES)


def resultados(texto: str) -> List[float]:
    """Los valores que `texto` obtiene con una cuenta, una tabla de distribución o una tabla markdown."""
    return [v for v, _ in _resultados(texto)]


def _resultados(texto: str) -> List[tuple]:
    """(valor, decimales con que se escribió): 0,898 informado con 3 respalda al 0,898031 «sin redondear»."""
    plano = _sin_tablas(texto)
    return [(n.valor, _decimales(n.crudo)) for n in buscar_numeros(plano) if _es_resultado(plano, n.ini)] +         [(v, 6) for v in _de_tablas(texto)]


def sin_origen(texto: str, enunciado: str, ignorar_hasta: int = 10, previos: Sequence[float] = ()) -> List[str]:
    """Números de `texto` que no están en el enunciado ni aparecen nunca como resultado de una cuenta.

    `previos`: resultados de los incisos anteriores (se pueden usar sin repetir la cuenta)."""
    plano = _sin_tablas(texto)
    base = conocidos(enunciado) + list(previos)
    todos = [(n.valor / 100 if n.pct else n.valor, n.crudo.strip(), n.ini, n.pct) for n in buscar_numeros(plano)]
    hechos = _resultados(texto)
    faltan = []
    for v, crudo, ini, pct in todos:
        if float(v).is_integer() and abs(v) <= ignorar_hasta and not pct:
            continue
        v = abs(v)                         # 3,75 es la misma cuenta que d = -3,75 (la diferencia al revés)
        if _iguala(v, crudo, [abs(k) for k in base]) or _iguala(v, crudo, [abs(k) for k, _ in hechos], afuera=True):
            continue
        if any(abs(v - abs(k)) <= 10 ** -dk + 1e-9 for k, dk in hechos if dk < _decimales(crudo)):
            continue                       # el mismo resultado, escrito con más decimales
        faltan.append(crudo)
    return list(dict.fromkeys(faltan))
