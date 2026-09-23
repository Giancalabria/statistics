"""Utilidades de texto: normalización, números en formato argentino y listas de datos."""

import re
import unicodedata
from dataclasses import dataclass
from typing import List, Optional


def _base(c: str) -> str:
    return unicodedata.normalize("NFD", c)[0].lower() if c else c


def normalizar(texto: str) -> str:
    """Minúsculas y sin tildes, conservando la longitud (las posiciones coinciden)."""
    return "".join(_base(c) for c in texto)


@dataclass
class Numero:
    valor: float
    ini: int
    fin: int          # fin incluye el '%' si lo hay
    pct: bool
    crudo: str

    @property
    def fraccion(self) -> float:
        """El valor como fracción (5% -> 0.05; 0,05 -> 0.05)."""
        return self.valor / 100 if self.pct else self.valor

    @property
    def es_entero(self) -> bool:
        return float(self.valor).is_integer()


# 1.250 | 1.167,88 | 2,5217 | 0.3222 | 15 | 1/37
RE_NUM = re.compile(
    r"(?<![\w.,/])"
    r"(\d+/\d+|\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+,\d+|\d+\.\d+|\d+)"
    r"(?![\w/]|[.,]\d)"
    r"(\s*%)?"
)


def parse_num(crudo: str) -> float:
    crudo = crudo.strip()
    if "/" in crudo:
        a, b = crudo.split("/")
        return float(a) / float(b)
    if "," in crudo:
        return float(crudo.replace(".", "").replace(",", "."))
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", crudo):
        return float(crudo.replace(".", ""))  # separador de miles
    return float(crudo)


def buscar_numeros(texto: str) -> List[Numero]:
    salida = []
    for m in RE_NUM.finditer(texto):
        try:
            valor = parse_num(m.group(1))
        except ValueError:
            continue
        salida.append(Numero(valor, m.start(1), m.end(), bool(m.group(2)), m.group(0)))
    return salida


def fmt(valor: Optional[float], dec: int = 4) -> str:
    """Formato argentino para mostrar (coma decimal)."""
    if valor is None:
        return "—"
    if isinstance(valor, int) or float(valor).is_integer():
        return f"{int(valor):,}".replace(",", ".")
    s = f"{valor:,.{dec}f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return s.rstrip("0").rstrip(",")


# ---------------------------------------------------------------------------
# Listas de datos crudos (x1 – x2 – x3 ...)
# ---------------------------------------------------------------------------

@dataclass
class ListaDatos:
    valores: List[float]
    ini: int
    fin: int
    etiqueta: str  # texto previo inmediato (p. ej. 'Ración “A”:')


_SEP = r"(?:\s*[–\-;]\s*|\s+y\s+|\s+)"


def buscar_listas(texto: str, minimo: int = 3) -> List[ListaDatos]:
    """Secuencias de >= `minimo` números separados por guiones, ';', 'y' o espacios.

    Descarta las filas que son un índice 1, 2, 3, ... (p. ej. 'Persona 1 2 3').
    """
    nums = [n for n in buscar_numeros(texto) if not n.pct]
    listas = []
    actual: List[Numero] = []

    def cerrar():
        if len(actual) >= minimo:
            valores = [n.valor for n in actual]
            es_indice = valores == [float(i) for i in range(int(valores[0]), int(valores[0]) + len(valores))]
            if not es_indice:
                ini = actual[0].ini
                previo = texto[max(0, ini - 40):ini]
                partes = [p.strip(" :–-,") for p in re.split(r"[\d.;]", previo)]
                etiqueta = next((p for p in reversed(partes) if p), "")
                listas.append(ListaDatos(valores, ini, actual[-1].fin, etiqueta))

    for n in nums:
        if actual and re.fullmatch(_SEP, texto[actual[-1].fin:n.ini] or " "):
            actual.append(n)
        else:
            cerrar()
            actual = [n]
    cerrar()
    return listas


def oraciones(texto: str) -> List[tuple]:
    """Parte en oraciones devolviendo (ini, fin). No corta en '1.250' ni '2,5'."""
    cortes = [0]
    for m in re.finditer(r"(?<=[.;?!:])\s+(?=[¿A-ZÁÉÍÓÚÑa-z(])", texto):
        cortes.append(m.end())
    cortes.append(len(texto))
    return [(cortes[i], cortes[i + 1]) for i in range(len(cortes) - 1) if cortes[i + 1] > cortes[i]]
