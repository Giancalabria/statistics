"""El planteo en JSON: el formato que se le pide al modelo y su validación contra el catálogo del intérprete.

El modelo devuelve lo mismo que arma `interprete.analizador` (tema, datos del planteo, incisos con su tipo y
parámetros), con las MISMAS claves de `interprete/modelo.py`. Así lo que propone la IA se edita en la misma
pantalla y lo resuelve el mismo `resolver`. Nada de lo que devuelve se usa sin pasar por `desde_dict`, que
descarta claves desconocidas, convierte los tipos y corrige los errores típicos (α = 5 en vez de 0,05).
"""

from typing import Any, Dict, List, Optional, Tuple

import interprete  # noqa: F401  (registra los temas y tipos de chi² y regresión)
from interprete.editor import de_texto
from interprete.modelo import CAMPOS_INCISO, CAMPOS_PLANTEO, COLAS, TEMAS, TIPOS, TIPOS_POR_TEMA, Analisis, Inciso

# Parámetros internos del analizador que vale la pena que el modelo pueda indicar.
EXTRA_INCISO = {
    "tema": ("Tema de ESTE inciso si es de otro parámetro que el planteo (p. ej. un inciso de proporción en un "
             "problema de medias)", "tema"),
    "cota": ("Intervalo de un solo lado: 'sup' (cota superior, 'como máximo') o 'inf' (cota inferior, 'como mínimo')",
             "cota"),
    "usar_S": ("En este inciso el desvío es el MUESTRAL S (σ desconocido → t)", "bool"),
}
CAMPOS_INC = {**CAMPOS_INCISO, **EXTRA_INCISO}

ENUMS = {
    "cola": list(COLAS),
    "prob": ["beta", "potencia"],
    "cota": ["sup", "inf"],
    "tema": [t for t in TEMAS if t != "desconocido"],
}

# Valores que son probabilidades o fracciones: si vienen como porcentaje (5 en vez de 0,05) se dividen por 100.
FRACCIONES = {"alpha", "beta", "p0", "p1", "p_hat", "reduccion", "alpha_var", "delta0_pct", "comision",
              "prob_aceptar"}


def tipos_validos(tema: str) -> List[str]:
    return TIPOS_POR_TEMA.get(tema) or list(TIPOS)


def _json_tipo(tipo: str) -> Dict[str, Any]:
    if tipo == "float":
        return {"type": "number"}
    if tipo == "int":
        return {"type": "integer"}
    if tipo == "bool":
        return {"type": "boolean"}
    if tipo == "lista":
        return {"type": "array", "items": {"type": "number"}}
    if tipo == "tabla":
        return {"type": "array", "items": {"type": "array", "items": {"type": "number"}}}
    if tipo in ENUMS:
        return {"type": "string", "enum": ENUMS[tipo]}
    return {"type": "string"}


def json_schema() -> Dict[str, Any]:
    """JSON Schema de la respuesta (Ollama lo usa para restringir la salida: siempre es JSON válido)."""
    datos = {k: _json_tipo(t) for k, (_, t) in CAMPOS_PLANTEO.items()}
    params = {k: _json_tipo(t) for k, (_, t) in CAMPOS_INC.items()}
    todos_tipos = sorted({t for ts in TIPOS_POR_TEMA.values() for t in ts} | set(TIPOS))
    return {
        "type": "object",
        "properties": {
            "tema": {"type": "string", "enum": list(TEMAS)},
            "criterio": {"type": "string", "enum": ["optimista", "pesimista", "ninguno"]},
            "datos": {"type": "object", "properties": datos, "additionalProperties": False},
            "incisos": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "letra": {"type": "string"},
                        "tipo": {"type": "string", "enum": todos_tipos},
                        "params": {"type": "object", "properties": params, "additionalProperties": False},
                    },
                    "required": ["letra", "tipo", "params"],
                },
            },
        },
        "required": ["tema", "datos", "incisos"],
    }


def catalogo_texto() -> str:
    """El catálogo de claves explicado, para el prompt (el modelo no ve el JSON Schema)."""
    def linea(k, etiqueta, tipo):
        extra = f" — uno de: {', '.join(ENUMS[tipo])}" if tipo in ENUMS else ""
        return f"- {k} ({tipo}): {etiqueta}{extra}"

    partes = ["TEMAS (campo 'tema'):"]
    partes += [f"- {k}: {v}" for k, v in TEMAS.items()]
    partes.append("\nTIPOS DE INCISO por tema (campo 'tipo' de cada inciso):")
    for tema, tipos in TIPOS_POR_TEMA.items():
        partes.append(f"- {tema}: " + "; ".join(f"{t} = {TIPOS.get(t, t)}" for t in tipos))
    partes.append("\nDATOS DEL PLANTEO (objeto 'datos'; solo las claves que el enunciado da):")
    partes += [linea(k, e, t) for k, (e, t) in CAMPOS_PLANTEO.items()]
    partes.append("\nPARÁMETROS DE CADA INCISO (objeto 'params'; solo lo que el inciso agrega o cambia):")
    partes += [linea(k, e, t) for k, (e, t) in CAMPOS_INC.items()]
    return "\n".join(partes)


# ---------------------------------------------------------------------------
# Analisis <-> dict
# ---------------------------------------------------------------------------

def a_dict(an: Analisis) -> Dict[str, Any]:
    """El análisis en el formato JSON del modelo (solo las claves del catálogo)."""
    def num(v):
        if isinstance(v, float):
            return float(f"{v:.10g}")           # 0.09999999999999998 -> 0.1
        if isinstance(v, list):
            return [num(x) for x in v]
        return v

    def limpio(d, catalogo):
        return {k: num(v) for k, v in d.items() if k in catalogo and v is not None}

    return {
        "tema": an.tema,
        "criterio": an.criterio or "ninguno",
        "datos": limpio(an.datos, CAMPOS_PLANTEO),
        "incisos": [{"letra": i.letra, "tipo": i.tipo, "params": limpio(i.params, CAMPOS_INC)} for i in an.incisos],
    }


def _valor(clave: str, valor: Any, tipo: str, avisos: List[str], donde: str) -> Optional[Any]:
    """Convierte y controla un valor; None si no sirve (con aviso)."""
    if valor is None or valor == "" or valor == []:
        return None
    try:
        if tipo == "bool":
            if isinstance(valor, str):
                return valor.strip().lower() in ("true", "si", "sí", "1")
            return bool(valor)
        if tipo in ENUMS:
            v = str(valor).strip().lower()
            if v not in ENUMS[tipo]:
                raise ValueError(f"'{valor}' no es una opción válida")
            return v
        if tipo == "texto":
            return str(valor)
        if tipo == "lista":
            if isinstance(valor, str):
                return de_texto(valor, "lista")
            return [float(x) for x in valor] or None
        if tipo == "tabla":
            filas = [[float(x) for x in fila] for fila in valor if fila]
            return filas or None
        if isinstance(valor, str):
            v = de_texto(valor, tipo)
        else:
            v = float(valor)
        if clave in FRACCIONES and 1 < v <= 100:
            avisos.append(f"{donde}{clave} = {valor} parecía un porcentaje: se tomó {v / 100:g}.")
            v = v / 100
        if clave in FRACCIONES and not 0 <= v <= 1:
            raise ValueError("debe estar entre 0 y 1")
        if clave in ("n", "n1", "n2", "N", "desvio", "s1", "s2", "sigma0", "sigma1") and v <= 0:
            raise ValueError("debe ser positivo")
        return int(round(v)) if tipo == "int" else float(v)
    except (TypeError, ValueError) as e:
        avisos.append(f"{donde}se descartó {clave} = {valor!r} ({e}).")
        return None


def desde_dict(d: Dict[str, Any], planteo: str = "", textos: Optional[Dict[str, str]] = None) -> Tuple[Analisis, List[str]]:
    """JSON del modelo -> Analisis validado + avisos de lo que se corrigió o descartó.

    `textos`: letra -> texto del inciso (para que la pantalla muestre el enunciado de cada uno)."""
    avisos: List[str] = []
    textos = textos or {}
    tema = d.get("tema") if d.get("tema") in TEMAS else "desconocido"
    if d.get("tema") and d.get("tema") not in TEMAS:
        avisos.append(f"Tema desconocido '{d.get('tema')}'.")
    criterio = d.get("criterio") if d.get("criterio") in ("optimista", "pesimista") else None
    an = Analisis(planteo=planteo, tema=tema, criterio=criterio)
    for k, v in (d.get("datos") or {}).items():
        if k not in CAMPOS_PLANTEO:
            continue
        v = _valor(k, v, CAMPOS_PLANTEO[k][1], avisos, "")
        if v is not None:
            an.datos[k] = v
    for n, inc in enumerate(d.get("incisos") or []):
        if not isinstance(inc, dict):
            continue
        letra = str(inc.get("letra") or chr(ord("a") + n)).strip().rstrip(")").lower() or chr(ord("a") + n)
        params = {}
        for k, v in (inc.get("params") or {}).items():
            if k not in CAMPOS_INC:
                continue
            v = _valor(k, v, CAMPOS_INC[k][1], avisos, f"{letra}) ")
            if v is not None:
                params[k] = v
        if params.get("tema") == tema:
            params.pop("tema")
        tipo = inc.get("tipo")
        validos = tipos_validos(params.get("tema") or tema)
        if tipo not in validos:
            if tipo:
                avisos.append(f"{letra}) el tipo '{tipo}' no corresponde al tema: queda como no soportado.")
            tipo = "no_soportado"
        an.incisos.append(Inciso(letra=letra, texto=textos.get(letra, ""), tipo=tipo, params=params,
                                 que_pide=f"Según la IA: {TIPOS.get(tipo, tipo)}."))
    return an, avisos
