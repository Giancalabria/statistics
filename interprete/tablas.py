"""Tablas de datos de un enunciado (regresión, frecuencias por clase, contingencia).

Una tabla se representa como {"columnas": [...], "filas": [[...], ...]}: cada fila es una
observación (o una clase) y cada columna una variable. Las celdas son números, textos de
intervalo ("20-30") o None.

Se pueden obtener:
- de la guía (`datos/guia_ejercicios.json` ya trae `tablas` estructuradas);
- de texto pegado con saltos de línea (una fila por renglón, separadores espacio, tab, ';' o '|');
- de texto aplanado en una sola línea ("Tiempo 5 8 8 7 Cantidad 2 2 2 2"): series con etiqueta.
"""

import re
from typing import Dict, List, Optional, Sequence, Tuple

from .texto import buscar_numeros, normalizar, parse_num

Tabla = Dict[str, list]

RE_INTERVALO = re.compile(r"^\s*(-?\d[\d.,]*)\s*[-–a]\s*(-?\d[\d.,]*)\s*$")
RE_CELDA_NUM = re.compile(r"^-?(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+,\d+|\d+\.\d+|\d+)%?$")


def _celda(tok: str):
    tok = tok.strip()
    if tok in ("---", "--", "-", "—"):
        return None
    if RE_INTERVALO.match(tok):
        return tok.replace("–", "-").replace(" ", "")
    if RE_CELDA_NUM.match(tok):
        neg = tok.startswith("-")
        v = parse_num(tok.lstrip("-").rstrip("%"))
        return -v if neg else v
    return tok


def _tokens(linea: str) -> List[str]:
    if "|" in linea or "\t" in linea or ";" in linea:
        partes = [p for p in re.split(r"[|\t;]", linea) if p.strip()]
    else:
        # intervalos "20 - 30" se juntan antes de cortar por espacios
        linea = re.sub(r"(\d)(?:\s+[–-]\s+|[–-])(\d)", r"\1-\2", linea)  # '3 -13,1' es un negativo
        partes = linea.split()
    return [p.strip() for p in partes]


def _es_fila_numerica(celdas) -> bool:
    nums = [c for c in celdas if isinstance(c, (int, float)) or (isinstance(c, str) and RE_INTERVALO.match(c))]
    return len(nums) >= 2 and len(nums) >= len(celdas) - 1


def desde_lineas(texto: str) -> List[Tabla]:
    """Bloques de renglones numéricos consecutivos. La línea anterior al bloque es el encabezado."""
    lineas = [l for l in texto.splitlines()]
    tablas = []
    i = 0
    while i < len(lineas):
        celdas = [_celda(t) for t in _tokens(lineas[i])]
        if not _es_fila_numerica(celdas):
            i += 1
            continue
        bloque = []
        j = i
        while j < len(lineas):
            c = [_celda(t) for t in _tokens(lineas[j])]
            if not _es_fila_numerica(c):
                break
            bloque.append(c)
            j += 1
        encabezado = lineas[i - 1].strip() if i > 0 else ""
        tablas.append(_armar(bloque, encabezado))
        i = j
    return [t for t in tablas if t]


def _armar(bloque: List[list], encabezado: str) -> Optional[Tabla]:
    etiquetadas = all(isinstance(f[0], str) and not RE_INTERVALO.match(f[0]) for f in bloque)
    if etiquetadas:
        # series por renglón: "Tiempo 5 8 8 7" / "Presentaciones 2 2 2" → columnas = etiquetas
        series = [(f[0], f[1:]) for f in bloque]
        largo = len(series[0][1])
        if len(bloque) <= 4 and all(len(s) == largo for _, s in series) and largo > len(bloque):
            return {"columnas": [s[0] for s in series], "filas": [list(v) for v in zip(*[s for _, s in series])]}
        return {"columnas": [""] + _cols(encabezado, len(bloque[0]) - 1), "filas": bloque}
    ancho = max(len(f) for f in bloque)
    filas = [f + [None] * (ancho - len(f)) for f in bloque]
    return {"columnas": _cols(encabezado, ancho), "filas": filas}


def _cols(encabezado: str, k: int) -> List[str]:
    partes = [p.strip() for p in re.split(r"\s{2,}|[|\t;]", encabezado) if p.strip()]
    if len(partes) == k:
        return partes
    return [f"c{i + 1}" for i in range(k)]


def series_etiquetadas(texto: str) -> List[Tuple[str, List[float]]]:
    """Texto aplanado: 'Etiqueta n1 n2 n3 ... Otra etiqueta m1 m2 m3 ...' → [(etiqueta, valores)]."""
    salida = []
    patron = re.compile(r"([A-Za-zÁÉÍÓÚáéíóúñ“”\"'()/.°º$ 0-9]{2,80}?)\s+((?:-?\d[\d.,]*\s+){2,}-?\d[\d.,]*)(?=\s+[A-Za-zÁÉÍÓÚáéíóúñ(]|\s*$|\s*[.:])")
    for m in patron.finditer(texto):
        etq = re.sub(r"\s+", " ", m.group(1)).strip()
        etq = re.sub(r"^(\d[\d.,]*\s+)+", "", etq)
        vals = [n.valor * (-1 if texto[max(0, n.ini - 1)] == "-" else 1) for n in buscar_numeros(m.group(2))]
        salida.append((etq, vals))
    return salida


def pares_de_series(texto: str) -> Optional[Tabla]:
    """Dos (o más) series consecutivas del mismo largo → tabla de variables."""
    s = series_etiquetadas(texto)
    for i in range(len(s) - 1):
        grupo = [s[i]]
        for j in range(i + 1, len(s)):
            if len(s[j][1]) == len(s[i][1]):
                grupo.append(s[j])
            else:
                break
        if len(grupo) >= 2 and len(s[i][1]) >= 3:
            return {"columnas": [g[0] for g in grupo], "filas": [list(v) for v in zip(*[g[1] for g in grupo])]}
    return None


def columnas_numericas(tabla: Tabla) -> Tuple[List[str], List[List[float]]]:
    """Columnas cuyas celdas son todas numéricas (descarta columnas de etiquetas / índices de fila)."""
    nombres, cols = [], []
    for j, nom in enumerate(tabla["columnas"]):
        col = [f[j] if j < len(f) else None for f in tabla["filas"]]
        if all(isinstance(v, (int, float)) for v in col):
            nombres.append(nom)
            cols.append([float(v) for v in col])
    return nombres, cols


def es_tabla_de_clases(tabla: Tabla) -> bool:
    return bool(tabla["filas"]) and all(isinstance(f[0], str) and RE_INTERVALO.match(f[0]) for f in tabla["filas"])


def limites_de_clase(tabla: Tabla) -> List[Tuple[float, float]]:
    out = []
    for f in tabla["filas"]:
        m = RE_INTERVALO.match(f[0])
        out.append((parse_num(m.group(1)), parse_num(m.group(2))))
    return out


def a_texto(tabla: Tabla) -> str:
    """Para mostrar / editar: una fila por renglón separada por ' | '."""
    def c(v):
        if v is None:
            return "---"
        if isinstance(v, float):
            return f"{v:g}".replace(".", ",")
        return str(v)
    lineas = [" | ".join(tabla["columnas"])]
    lineas += [" | ".join(c(v) for v in f) for f in tabla["filas"]]
    return "\n".join(lineas)


def desde_texto_editado(texto: str) -> Optional[Tabla]:
    """Inversa de `a_texto`: primera línea encabezados, las demás filas."""
    lineas = [l for l in texto.strip().splitlines() if l.strip()]
    if len(lineas) < 2:
        return None
    cols = [p.strip() for p in re.split(r"[|\t;]", lineas[0]) if p.strip()]
    filas = [[_celda(t) for t in _tokens(l)] for l in lineas[1:]]
    if not cols or len(cols) != len(filas[0]):
        cols = [f"c{i + 1}" for i in range(len(filas[0]))]
    return {"columnas": cols, "filas": filas}


RE_TABLA_PIPES = re.compile(r"Tabla[^:|;]{0,60}:\s*((?:[^.]|\.(?=\d)|\.(?=[^;|]*\|))*)")


def desde_pipes(texto: str) -> List[Tabla]:
    """Formato aplanado 'Tabla: [título:] c1 | c2; v | v; v | v.' (el de `datos/guia_ejercicios.json`)."""
    tablas = []
    for m in RE_TABLA_PIPES.finditer(texto):
        filas = [f.strip() for f in m.group(1).split(";") if f.strip()]
        if len(filas) < 2 or "|" not in filas[0]:
            continue
        enc = filas[0]
        if ":" in enc.split("|")[0]:  # título antes del primer encabezado
            enc = enc.split(":", 1)[1]
        cols = [c.strip() for c in enc.split("|")]
        cuerpo = [[_celda(c) if c.strip() not in ("None", "null") else None for c in f.split("|")] for f in filas[1:]]
        cuerpo = [f for f in cuerpo if len(f) == len(cols)]
        if cuerpo:
            tablas.append({"columnas": cols, "filas": cuerpo})
    return tablas


RE_TABLA_CORCHETES = re.compile(r"\[Tabla([^\]]*)\]")
_PREP = {"de", "del", "la", "el", "los", "las", "en", "y", "a", "por", "con", "sin", "al"}


def partir_encabezado(enc: str, k: int) -> List[str]:
    """'Consumo (en Kwh) Potencia (en Kw)' con k = 2 → ['Consumo (en Kwh)', 'Potencia (en Kw)'].

    Cortes candidatos con prioridad: después de ')' / antes de 'X1:' 'Y:' > antes de una mayúscula
    precedida de minúscula > antes de cualquier mayúscula que no siga a una preposición."""
    palabras = enc.split()
    if k <= 1 or len(palabras) < k:
        return [enc.strip()] if k == 1 else [f"c{i + 1}" for i in range(k)]
    cand = []
    for i in range(1, len(palabras)):
        prev, w = palabras[i - 1], palabras[i]
        if not w[:1].isupper() and not re.match(r"^[xy]\d*\b", w, re.I):
            if prev.endswith(")") and not w.startswith("("):
                cand.append((0, i))
            continue
        if prev.strip(".,") in _PREP or prev.endswith(":") and not re.match(r"^[XY]\d*", w):
            continue
        if prev.endswith(")") or re.match(r"^[XY]\d*\b", w):
            cand.append((0, i))
        elif prev[:1].islower() or prev[-1:].isdigit():
            cand.append((1, i))
        else:
            cand.append((2, i))
    if len(cand) < k - 1:
        return [f"c{i + 1}" for i in range(k)]
    cortes = sorted(i for _, i in sorted(cand)[:k - 1])
    partes, ini = [], 0
    for c in cortes + [len(palabras)]:
        partes.append(" ".join(palabras[ini:c]))
        ini = c
    return partes


def desde_corchetes(texto: str) -> List[Tabla]:
    """'[Tabla: Encabezado A Encabezado B ; 1 2 ; 3 4]' (formato de la guía para regresión)."""
    tablas = []
    for m in RE_TABLA_CORCHETES.finditer(texto):
        cuerpo = m.group(1)
        primera = cuerpo.split(";")[0]
        if ":" in primera:  # '[Tabla Fuente: ...: Encabezados ; ...]' → lo que sigue al último ':'
            cuerpo = cuerpo[primera.rfind(":") + 1:]
        partes = [p.strip() for p in cuerpo.split(";") if p.strip()]
        if len(partes) < 3:
            continue
        filas = [[_celda(t) for t in _tokens(p)] for p in partes[1:]]
        k = max(len(f) for f in filas)
        filas = [f for f in filas if len(f) == k]
        if len(filas) >= 2:
            tablas.append({"columnas": partir_encabezado(partes[0], k), "filas": filas})
    return tablas


def buscar_tablas(texto: str) -> List[Tabla]:
    """Primero 'Tabla: a | b; ...', después por renglones; si el texto vino aplanado, por series etiquetadas."""
    tablas = desde_pipes(texto) or desde_corchetes(texto)
    if not tablas and "\n" in texto:
        tablas = desde_lineas(texto)
    if not tablas:
        t = pares_de_series(texto)
        if t:
            tablas = [t]
    return tablas


def nombre_norm(nombre: str) -> str:
    return normalizar(nombre or "")
