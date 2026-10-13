"""Datos de DOS muestras a partir de tablas (TEMAS IV y V).

Reconoce las formas en que la guía (y los enunciados parecidos) presentan dos grupos:

- datos crudos con un grupo por FILA ('Proceso Viejo | 6 | 4 | 5 ...') o por COLUMNA ('Muestra Nº | Con | Sin');
  columnas con el mismo encabezado se juntan (la tabla partida en dos bloques);
- resúmenes n / x̄ / S con los estadísticos por fila ('Media: x̄ = | 428 kg | 432 kg') o por columna
  ('Variedad A | 25 | 3,4' bajo 'Promedio (x̄) | Desvío std. (S)');
- datos agrupados: intervalos de clase + frecuencias de cada grupo ('1,2 – 1,3 | 8 | 1,6 – 1,7 | 8').

También arma esas tablas desde texto aplanado (renglones numerados 'k: a / b', clases 'a – b: f | c – d: g',
resúmenes 'Media: x̄ = 428 kg | 432 kg'). No depende del analizador.
"""

import re
from dataclasses import dataclass, field
from math import sqrt
from typing import Dict, List, Optional

from .texto import normalizar, parse_num

Tabla = Dict[str, list]

RE_INTERVALO = re.compile(r"^\s*(-?\d[\d.,]*)\s*[-–]\s*(-?\d[\d.,]*)\s*$")
RE_NUM_CELDA = re.compile(r"^\s*([−-])?\s*(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?)")

# encabezado de la columna / fila que identifica la UNIDAD medida con ambos tratamientos → apareadas
RE_UNIDAD = (r"(finca|persona|trabajador|operari|paciente|individuo|sujeto|muestra|parcela|alumno|empleado|"
             r"caso|par\b|n[º°o]\b|nro|numero|lote|dia\b|vehiculo|auto\b|planta\b|campo\b)")
# encabezado que nombra al GRUPO (no a la unidad) → independientes
RE_GRUPO = (r"(proceso|racion|marca|grupo|maquina|variedad|metodo|tratamiento|tipo|establecimiento|"
            r"aleacion|formula|torno|equipo|producto|proveedor)")

ROMANOS = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii", "xiii", "xiv", "xv"]


@dataclass
class Grupos:
    """Dos (o más) grupos leídos de una tabla."""
    nombres: List[str]
    listas: List[List[float]] = field(default_factory=list)              # datos crudos por grupo
    resumen: Dict[str, List[Optional[float]]] = field(default_factory=dict)  # 'n', 'xbar', 's' por grupo
    apareadas: Optional[bool] = None   # pista de la forma de la tabla (None = no dice)
    agrupados: bool = False
    origen: str = ""


# ---------------------------------------------------------------------------
# Celdas
# ---------------------------------------------------------------------------

def _num(c) -> Optional[float]:
    """Número de una celda: 12, '12 kg', '−0,01653', '1.470'. None si no empieza con un número."""
    if isinstance(c, bool) or c is None:
        return None
    if isinstance(c, (int, float)):
        return float(c)
    s = str(c).strip()
    if RE_INTERVALO.match(s):
        return None
    m = RE_NUM_CELDA.match(s)
    if not m:
        return None
    try:
        v = parse_num(m.group(2))
    except ValueError:
        return None
    return -v if m.group(1) else v


def _es_intervalo(c) -> bool:
    return isinstance(c, str) and RE_INTERVALO.match(c) is not None


def _marca(c: str) -> float:
    m = RE_INTERVALO.match(c)
    return (parse_num(m.group(1)) + parse_num(m.group(2))) / 2


def _es_indice(valores) -> bool:
    """1, 2, 3, ... (o I, II, III ...): numera las unidades, no son datos."""
    if not valores:
        return False
    if all(isinstance(v, str) for v in valores):
        return [normalizar(v).strip() for v in valores] == ROMANOS[:len(valores)]
    nums = [_num(v) for v in valores]
    if any(v is None for v in nums):
        return False
    return len(nums) >= 2 and nums == [float(nums[0] + i) for i in range(len(nums))] and nums[0] in (0.0, 1.0)


def nombre_corto(nombre: str) -> str:
    """'Cant. días observados de Máquina “A”' → 'Máquina “A”'; '“Casablanca”' → 'Casablanca'."""
    nombre = re.sub(r"\s+", " ", str(nombre or "")).strip(" :;,.")
    m = re.search(r"([A-Za-zÁÉÍÓÚáéíóúñ]+\s+)?[“\"]([^”\"]{1,30})[”\"]", nombre)
    if m and len(nombre) > 25:
        return (m.group(1) or "") + "“" + m.group(2) + "”"
    if re.fullmatch(r"[“\"][^”\"]+[”\"]", nombre):
        return nombre[1:-1]
    return nombre[-40:].strip()


def tipo_estadistico(etiqueta) -> Optional[str]:
    """'Media: x̄ =' → 'xbar'; 'Desvío std. (S)' → 's'; 'Muestra: n =' → 'n'."""
    e = normalizar(str(etiqueta or "")).replace("̄", "")
    if re.search(r"desvio|desviacion|\(s\)|\bs\s*=|^\s*s\s*$|\bsd\b", e):
        return "s"
    if re.search(r"media|promedio|\(x\)|\bx\s*=|^\s*x\s*$", e):
        return "xbar"
    if re.search(r"\bn\s*=|^\s*n\s*$|tamano|cantidad de (datos|observaciones|unidades)|^\s*muestra\s*:?\s*$|\(n\)", e):
        return "n"
    return None


# ---------------------------------------------------------------------------
# Tabla estructurada → grupos
# ---------------------------------------------------------------------------

def _columna(tabla: Tabla, j: int) -> list:
    return [f[j] if j < len(f) else None for f in tabla["filas"]]


def _agrupados(tabla: Tabla) -> Optional[Grupos]:
    cols = tabla["columnas"]
    k = max(len(cols), max((len(f) for f in tabla["filas"]), default=0))
    interv = [j for j in range(k) if all(_es_intervalo(c) for c in _columna(tabla, j) if c is not None)
              and any(c is not None for c in _columna(tabla, j))]
    if not interv:
        return None
    nombres, ns, medias, desvios = [], [], [], []
    for j in range(k):
        if j in interv:
            continue
        izq = [i for i in interv if i < j]
        if not izq:
            continue
        marcas_col = _columna(tabla, izq[-1])
        frec = _columna(tabla, j)
        pares = [(_marca(m), _num(f)) for m, f in zip(marcas_col, frec) if m is not None and _num(f) is not None]
        if len(pares) < 2:
            continue
        n = sum(f for _, f in pares)
        xbar = sum(m * f for m, f in pares) / n
        s = sqrt(sum(f * (m - xbar) ** 2 for m, f in pares) / (n - 1))
        nombres.append(nombre_corto(cols[j] if j < len(cols) else f"Grupo {len(nombres) + 1}"))
        ns.append(n)
        medias.append(xbar)
        desvios.append(s)
    if len(nombres) < 2:
        return None
    return Grupos(nombres, resumen={"n": ns, "xbar": medias, "s": desvios}, apareadas=False, agrupados=True,
                  origen="datos agrupados: marcas de clase (punto medio) × frecuencias de cada grupo")


def _resumen(tabla: Tabla) -> Optional[Grupos]:
    cols, filas = tabla["columnas"], tabla["filas"]
    # estadísticos por fila: la 1ª celda dice qué es ('Media: x̄ =') y cada columna es un grupo
    tipos_fila = [tipo_estadistico(f[0]) if f and isinstance(f[0], str) else None for f in filas]
    if sum(1 for x in tipos_fila if x) >= 2:
        k = len(cols) - 1
        res: Dict[str, List[Optional[float]]] = {}
        for f, tipo in zip(filas, tipos_fila):
            if tipo and tipo not in res:
                res[tipo] = [_num(c) for c in f[1:1 + k]]
        nombres = [nombre_corto(c) for c in cols[1:]]
        if k >= 2 and any(v is not None for vals in res.values() for v in vals):
            return Grupos(nombres, resumen=res, origen="tabla resumen: una columna por grupo (n, x̄, S por fila)")
    # estadísticos por columna: cada fila es un grupo
    tipos_col = [tipo_estadistico(c) for c in cols]
    if sum(1 for x in tipos_col if x) >= 2 and len(filas) >= 2:
        res = {}
        for j, tipo in enumerate(tipos_col):
            if tipo and tipo not in res:
                res[tipo] = [_num(f[j]) if j < len(f) else None for f in filas]
        nombres = [nombre_corto(f[0]) if f and isinstance(f[0], str) else f"Grupo {i + 1}" for i, f in enumerate(filas)]
        return Grupos(nombres, resumen=res, origen="tabla resumen: una fila por grupo (n, x̄, S por columna)")
    return None


def _pista_apareadas(encabezado: str) -> Optional[bool]:
    e = normalizar(encabezado or "")
    if re.search(RE_GRUPO, e):
        return False
    if re.search(RE_UNIDAD, e):
        return True
    return None


def _filas_como_grupos(tabla: Tabla) -> Optional[Grupos]:
    filas = tabla["filas"]
    grupos = []
    for f in filas:
        if not f or not isinstance(f[0], str) or _num(f[0]) is not None:
            continue
        vals = [_num(c) for c in f[1:] if c is not None]
        if len(vals) >= 2 and all(v is not None for v in vals) and not _es_indice(vals):
            grupos.append((nombre_corto(f[0]), vals))
    if len(grupos) < 2:
        return None
    pista = _pista_apareadas(tabla["columnas"][0] if tabla["columnas"] else "")
    if pista and len({len(v) for _, v in grupos}) > 1:
        pista = False
    return Grupos([g[0] for g in grupos], listas=[g[1] for g in grupos], apareadas=pista,
                  origen="datos crudos: una fila por grupo")


def _columnas_como_grupos(tabla: Tabla) -> Optional[Grupos]:
    cols = tabla["columnas"]
    orden: List[str] = []
    datos: Dict[str, List[float]] = {}
    nombres: Dict[str, str] = {}
    hay_indice = False
    for j, nom in enumerate(cols):
        col = _columna(tabla, j)
        presentes = [c for c in col if c is not None]
        if not presentes:
            continue
        vals = [_num(c) for c in presentes]
        if any(v is None for v in vals):
            continue
        clave = normalizar(str(nom)).strip()
        if _es_indice(presentes) or (re.search(RE_UNIDAD, clave) and not re.search(RE_GRUPO, clave)
                                     and all(float(v).is_integer() for v in vals)):
            hay_indice = True
            continue
        if clave not in datos:
            orden.append(clave)
            datos[clave] = []
            nombres[clave] = nombre_corto(nom)
        datos[clave] += vals
    if len(orden) < 2:
        return None
    listas = [datos[c] for c in orden]
    pista = True if hay_indice and len({len(l) for l in listas}) == 1 else None
    return Grupos([nombres[c] for c in orden], listas=listas, apareadas=pista,
                  origen="datos crudos: una columna por grupo" + (" (cada fila es una unidad)" if hay_indice else ""))


def grupos_de_tabla(tabla: Tabla) -> Optional[Grupos]:
    if not tabla or not tabla.get("filas") or not tabla.get("columnas"):
        return None
    for f in (_agrupados, _resumen, _filas_como_grupos, _columnas_como_grupos):
        g = f(tabla)
        if g:
            return g
    return None


def grupos_de_tablas(tablas: List[Tabla]) -> Optional[Grupos]:
    """El primer conjunto de >= 2 grupos que se pueda leer de las tablas (si hay varias tablas resumen
    parciales se combinan)."""
    for tabla in tablas or []:
        g = grupos_de_tabla(tabla)
        if g:
            return g
    return None


# ---------------------------------------------------------------------------
# Texto aplanado → tabla
# ---------------------------------------------------------------------------

_NUM_TXT = r"[−-]?\d+(?:[.,]\d+)?"


def _valor_txt(tok: str) -> float:
    tok = tok.strip()
    neg = tok[:1] in "−-"
    v = parse_num(tok.lstrip("−-"))
    return -v if neg else v


def tabla_filas_numeradas(texto: str) -> Optional[Tabla]:
    """'(Muestra Nº: Propuesto / Clásico): 1: 164,65 / 165,20; 2: 178,60 / 179,20; ...' → tabla con una columna
    por grupo y una fila por unidad (k = 1, 2, 3 ... consecutivos)."""
    patron = re.compile(r"(?:(?<=[;:(])|^)\s*(\d{1,3})\s*:\s*((?:" + _NUM_TXT + r"\s*[/|]?\s*){2,})(?=;|\.\s|\.$|$)")
    filas, ini = [], None
    for m in patron.finditer(texto):
        k = int(m.group(1))
        if filas and k != filas[-1][0] + 1:
            if len(filas) >= 3:
                break
            filas, ini = [], None
        if not filas and k != 1:
            continue
        vals = [_valor_txt(x) for x in re.findall(_NUM_TXT, m.group(2))]
        if filas and len(vals) != len(filas[0][1]):
            break
        if ini is None:
            ini = m.start()
        filas.append((k, vals))
    if len(filas) < 3:
        return None
    previo = texto[max(0, ini - 300):ini]
    m = re.search(r"\(([^():]{0,40}):\s*([^()]*(?:\([^()]*\)[^()]*)*)\)\s*:?\s*$", previo)
    k = len(filas[0][1])
    nombres = []
    indice = "Nº"
    if m:
        indice = m.group(1).strip()
        nombres = [p.strip() for p in re.split(r"\s*/\s*|\s*,\s*", m.group(2)) if p.strip()]
    if len(nombres) != k:
        nombres = [f"Grupo {i + 1}" for i in range(k)]
    return {"columnas": [indice] + nombres, "filas": [[i] + v for i, v in filas]}


def tabla_clases_texto(texto: str) -> Optional[Tabla]:
    """'Máquina “A” | ... Máquina “B”: 1,2 – 1,3: 8 | 1,6 – 1,7: 8; 1,3 – 1,4: 12 | 1,7 – 1,8: 13; ...' →
    tabla de clases con (intervalo, frecuencia) de cada grupo."""
    celda = r"(\d+(?:,\d+)?)\s*[–-]\s*(\d+(?:,\d+)?)\s*:\s*(\d+)"
    fila_re = re.compile(celda + r"(?:\s*\|\s*" + celda + r")*")
    filas, ini = [], None
    for m in fila_re.finditer(texto):
        celdas = re.findall(celda, m.group(0))
        if filas and len(celdas) != len(filas[0]):
            break
        if ini is None:
            ini = m.start()
        filas.append(celdas)
    if len(filas) < 3:
        return None
    k = len(filas[0])
    previo = texto[max(0, ini - 400):ini]
    nombres = []
    for m in re.finditer(r"([A-Za-zÁÉÍÓÚáéíóúñ]+\s+)?[“\"]([^”\"]{1,30})[”\"]", previo):
        nom = (m.group(1) or "") + "“" + m.group(2) + "”"
        if nom not in nombres:
            nombres.append(nom)
    nombres = nombres[-k:] if len(nombres) >= k else [f"Grupo {i + 1}" for i in range(k)]
    columnas, cuerpo = [], []
    for i in range(k):
        columnas += ["Clase", nombres[i]]
    for f in filas:
        fila = []
        for a, b, fr in f:
            fila += [f"{a}-{b}", int(fr)]
        cuerpo.append(fila)
    return {"columnas": columnas, "filas": cuerpo}


def tabla_resumen_texto(texto: str) -> Optional[Tabla]:
    """'Establecimiento: “LP” | “Ca”; Muestra: n = 50 | 50; Media: x̄ = 428 kg | 432 kg; Desvío: S = 12 kg | 18 kg'."""
    segmentos = [s for s in re.split(r";|\.\s", texto) if "|" in s and ":" in s]
    filas, encabezado = [], None
    for seg in segmentos:
        corte = seg.split("|")[0].rfind(":")
        if corte < 0:
            continue
        etq, resto = seg[:corte], seg[corte + 1:]
        etq = re.split(r"[:,]", etq)[-1].strip()[-40:]
        m = re.match(r"\s*([A-Za-zx̄σ̄]{1,3}\s*=)\s*(.*)$", resto, re.S)
        if m:
            etq, resto = etq + ": " + m.group(1), m.group(2)
        celdas = [c.strip() for c in resto.split("|")]
        if all(_num(c) is None for c in celdas) and encabezado is None:
            encabezado = [etq] + celdas
        elif tipo_estadistico(etq):
            filas.append([etq] + celdas)
    if len(filas) < 2:
        return None
    k = len(filas[0]) - 1
    if not encabezado or len(encabezado) != k + 1:
        encabezado = [""] + [f"Grupo {i + 1}" for i in range(k)]
    return {"columnas": encabezado, "filas": filas}


def tablas_de_texto(texto: str) -> List[Tabla]:
    """Tablas de dos muestras escritas en una sola línea (las que no detecta `tablas.buscar_tablas`)."""
    salida = []
    for f in (tabla_clases_texto, tabla_filas_numeradas, tabla_resumen_texto):
        t = f(texto)
        if t:
            salida.append(t)
    return salida
