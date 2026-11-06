"""Conversión entre los valores del análisis y el texto editable de la pantalla.

Todo se edita como texto en formato argentino (coma decimal, punto de miles),
así se puede copiar tal cual del enunciado.
"""

from typing import Any, List, Optional

from .texto import buscar_numeros


def _signo(texto: str, n) -> float:
    """-1 si el número viene con un menos pegado ('-0,25', '−3'), al principio o después de un separador
    (espacio, ';', '(', '['). '10-20' no es negativo. buscar_numeros devuelve siempre el valor absoluto."""
    i = n.ini - 1
    if i >= 0 and texto[i] in "-−–" and (i == 0 or texto[i - 1] in " 	;([|"):
        return -1.0
    return 1.0


def _numeros(texto: str) -> List[float]:
    return [_signo(texto, n) * n.valor for n in buscar_numeros(texto)]


def a_texto(valor: Any, tipo: str) -> str:
    if valor is None:
        return ""
    if tipo == "lista":
        return " ; ".join(_num(v) for v in valor)
    if tipo == "tabla":
        return "\n".join(" ; ".join(_num(v) for v in fila) for fila in valor)
    if tipo in ("float", "int"):
        return _num(valor)
    if isinstance(valor, (list, tuple)):
        return ", ".join(str(v) for v in valor)
    return str(valor)


def _num(v) -> str:
    if isinstance(v, str):
        return v
    v = float(v)
    if v.is_integer():
        return str(int(v))
    return f"{v:.10g}".replace(".", ",")


def de_texto(texto: str, tipo: str) -> Optional[Any]:
    """Texto -> valor. Vacío -> None (el dato no se usa)."""
    texto = (texto or "").strip()
    if not texto:
        return None
    if tipo == "texto":
        return texto
    if tipo == "tabla":
        filas = [_numeros(linea) for linea in texto.splitlines()]
        return [f for f in filas if f] or None
    nums = buscar_numeros(texto)
    if tipo == "lista":
        return _numeros(texto) or None
    if not nums:
        raise ValueError(f"No se entiende el número '{texto}'")
    n = nums[0]
    valor = _signo(texto, n) * (n.fraccion if n.pct else n.valor)
    if tipo == "int":
        return int(round(valor))
    return float(valor)


def lista_de_texto(texto: str) -> List[float]:
    return _numeros(texto or "")
