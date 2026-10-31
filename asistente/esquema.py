"""El planteo en JSON: el formato que se le pide al modelo y su validación contra el catálogo del intérprete.

El modelo devuelve lo mismo que arma `interprete.analizador` (tema, datos del planteo, incisos con su tipo y
parámetros), con las MISMAS claves de `interprete/modelo.py`. Así lo que propone la IA se edita en la misma
pantalla y lo resuelve el mismo `resolver`. Nada de lo que devuelve se usa sin pasar por `desde_dict`, que
descarta claves desconocidas o de otro tema, convierte los tipos y corrige los errores típicos (α = 5 en vez de
0,05, 'xbar1' en un problema de una media, α anotado solo en el primer inciso).
"""

import re
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

# Claves que usa cada tema (las que arman las reglas en la guía, más las que lee el solver). El prompt las lista
# por tema y `desde_dict` traduce o descarta las de otro tema ('xbar1' en un problema de UNA media).
_UNA_POB_INC = ["tail", "alpha", "e", "reduccion", "beta", "prob", "n", "cota", "tema", "usar_S", "repeticiones",
                "mu0", "mu1", "total", "costo_fijo", "comision",               # media
                "sigma0", "sigma1", "relacion", "ambos",                       # varianza
                "p0", "p1", "r", "p_hat", "costo_unitario", "prob_aceptar"]    # proporción (r, p̂: incisos de p)
CLAVES_TEMA: Dict[str, Tuple[List[str], List[str]]] = {
    "media": (["n", "xbar", "desvio", "sigma_conocido", "N", "mu0", "datos", "alpha", "e", "reduccion", "beta",
               "mu1", "control", "doble", "escala", "costo_fijo"], _UNA_POB_INC),
    "varianza": (["n", "desvio", "sigma_conocido", "sigma0", "xbar", "mu0", "datos", "alpha", "beta", "e",
                  "reduccion", "doble", "control"], _UNA_POB_INC),
    "proporcion": (["n", "r", "p_hat", "p0", "N", "alpha", "beta", "e", "reduccion", "rc", "control"], _UNA_POB_INC),
    "dos_varianzas": (["n1", "n2", "s1", "s2", "xbar1", "xbar2", "datos1", "datos2", "nombre1", "nombre2",
                       "apareadas", "phi0", "phi1", "sujeto", "alpha", "beta"],
                      ["tail", "alpha", "beta", "prob", "phi0", "phi1", "sobre", "relacion", "reduccion", "n", "cota",
                       "tema"]),
    "dos_medias": (["n1", "n2", "xbar1", "xbar2", "s1", "s2", "datos1", "datos2", "nombre1", "nombre2", "apareadas",
                    "sujeto", "sigma_pob1", "sigma_pob2", "sigma_afirmado", "alpha_var", "alpha", "beta"],
                   ["tail", "alpha", "delta0", "delta1", "delta0_pct", "sujeto", "porcentual", "beta", "prob", "n",
                    "e", "reduccion", "cota", "tema"]),
    "chi_contingencia": (["tabla", "alpha"], ["alpha", "tail"]),
    "chi_ajuste": (["observados", "esperados", "proporciones", "p_estimados", "clases", "valores_var", "modelos",
                    "alpha"], ["alpha", "modelos", "tail"]),
    "regresion": (["x", "y", "nombre_x", "nombre_y", "escala_x", "escala_y", "alpha"],
                  ["alpha", "x0", "individual", "cola", "beta10", "modelo", "origen", "tail", "validar", "rho2", "x0_puntual"]),
    "regresion_multiple": (["xs", "y", "nombre_y", "escala_y", "alpha"], ["alpha", "variables", "modelos"]),
}

# Un inciso puede ser de otro parámetro (params.tema: uno de una media en un problema de dos, uno de proporción en
# un χ²...) y trae sus propios parámetros: en los incisos se permiten además los de 1 y 2 poblaciones. Los 'datos'
# del planteo sí quedan restringidos al tema.
_OTRO_TEMA_INC = list(dict.fromkeys(_UNA_POB_INC + CLAVES_TEMA["dos_medias"][1] + CLAVES_TEMA["dos_varianzas"][1]))
for _tema, (_datos, _params) in CLAVES_TEMA.items():
    CLAVES_TEMA[_tema] = (_datos, list(dict.fromkeys(_params + _OTRO_TEMA_INC)))

# Claves de otro tema que el modelo usa por error y equivalen a una del tema elegido.
_ALIAS_UNA_POB = {"xbar1": "xbar", "s1": "desvio", "n1": "n", "datos1": "datos", "sigma_pob1": "desvio"}
ALIAS: Dict[str, Dict[str, str]] = {"media": _ALIAS_UNA_POB, "varianza": _ALIAS_UNA_POB,
                                    "proporcion": {"n1": "n"},
                                    "regresion": {"datos1": "x", "datos2": "y"}}

# Lo que un inciso no dice vale lo del anterior (la misma herencia que aplica interprete.analizador).
HEREDABLES = ("alpha", "tail", "mu1", "sigma1", "p1", "prob", "mu0", "sigma0", "p0", "phi1", "sobre")


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
    """JSON Schema del planteo (documenta el formato y lo usan los tests).

    No se le pasa a Ollama: la gramática que arma con un esquema obliga a escribir las claves EN EL ORDEN del
    esquema, y el modelo, que las escribe en el orden en que aparecen en el enunciado, termina salteando 'xbar' o
    'mu0' y usando la siguiente clave parecida que le queda ('xbar1', 'sigma_pob1'). Se pide JSON libre y lo
    valida `desde_dict`."""
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
    partes.append("\nCLAVES PERMITIDAS SEGÚN EL TEMA (usá SOLO las del tema elegido; p. ej. en 'media' la media muestral "
                  "es 'xbar' y el desvío 'desvio', NUNCA 'xbar1', 's1' ni 'sigma_pob1', que son de dos poblaciones):")
    for tema, (datos, params) in CLAVES_TEMA.items():
        partes.append(f"- {tema}: datos = {', '.join(datos)} | params = {', '.join(params)}")
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


def _relacion_es_de_sigma(tipo, params: Dict[str, Any], tema: str, texto: str, avisos: List[str], letra: str) -> None:
    """'reducir un 15% la relación de la estimación del desvío': la relación entre límites existe solo en el IC de σ / σ²
    (en la media se habla del error). Si el modelo dejó el inciso en el tema media, se pasa a varianza (1er parcial
    29/04/25: las dos lecturas de IA calcularon el n de la media)."""
    from interprete.texto import normalizar
    norm = normalizar(texto)
    if tipo == "n" and (params.get("tema") or tema) == "media" and re.search(r"\brelacion\b", norm) and \
            re.search(r"(desvio|desviacion|varianza|variabilidad)", norm):
        params["tema"] = "varianza"
        avisos.append(f"{letra}) la relación entre límites es del IC del desvío: se calcula el n para σ.")


def _modelos_de_texto(d: Dict[str, Any], tema: str) -> None:
    """El modelo escribe los modelos a ajustar como texto ("['exponencial']", "normal y weibull"): se leen los nombres
    como en el enunciado."""
    if isinstance(d.get("modelos"), str) and tema == "chi_ajuste":
        from interprete.chi_modelos import modelos_en
        from interprete.texto import normalizar
        mods = modelos_en(normalizar(d.pop("modelos")))
        if mods:
            d["modelos"] = mods


def _beta_es_riesgo(d: Dict[str, Any], avisos: List[str], donde: str) -> None:
    """β es un riesgo (no detectar): nunca vale 0,99. Si el modelo anotó la probabilidad de DETECTAR (potencia) en β,
    se pasa a β = 1 - potencia."""
    b = d.get("beta")
    if isinstance(b, (int, float)) and 0.5 < b < 1:
        d["beta"] = round(1 - b, 10)
        avisos.append(f"{donde}β = {b} es la potencia (probabilidad de detectar): se tomó β = {d['beta']}.")


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
    permitidas = CLAVES_TEMA.get(tema, (list(CAMPOS_PLANTEO), []))[0]
    alias = ALIAS.get(tema, {})
    datos = d.get("datos") or {}
    for k, v in datos.items():
        if k not in CAMPOS_PLANTEO:
            continue
        if k not in permitidas:
            destino = alias.get(k)
            if destino and destino not in datos and destino not in an.datos:
                avisos.append(f"{k} no es una clave de {tema}: se tomó como {destino}.")
                if k == "sigma_pob1":
                    an.datos.setdefault("sigma_conocido", True)
                k = destino
            else:
                avisos.append(f"Se descartó {k} = {v!r}: no corresponde al tema {tema}.")
                continue
        v = _valor(k, v, CAMPOS_PLANTEO[k][1], avisos, "")
        if v is not None:
            an.datos[k] = v
    _beta_es_riesgo(an.datos, avisos, "")
    _modelos_de_texto(an.datos, tema)
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
        _beta_es_riesgo(params, avisos, f"{letra}) ")
        _modelos_de_texto(params, params.get("tema") or tema)
        tipo = inc.get("tipo")
        _relacion_es_de_sigma(tipo, params, tema, textos.get(letra, ""), avisos, letra)
        validos = tipos_validos(params.get("tema") or tema)
        if tipo not in validos:
            if tipo:
                avisos.append(f"{letra}) el tipo '{tipo}' no corresponde al tema: queda como no soportado.")
            tipo = "no_soportado"
        an.incisos.append(Inciso(letra=letra, texto=textos.get(letra, ""), tipo=tipo, params=params,
                                 que_pide=f"Según la IA: {TIPOS.get(tipo, tipo)}."))
    heredar(an)
    return an, avisos


def heredar(an: Analisis) -> None:
    """Lo que un inciso no repite vale lo del anterior (α, cola, μ₁...), como en interprete.analizador; si el inciso
    es de otro parámetro solo se hereda α. El modelo suele anotar α una sola vez, en el primer inciso."""
    previo: Dict[str, Any] = {}
    tema_previo = an.tema
    diseno_previo: Optional[Inciso] = None
    for inc in an.incisos:
        tema_inc = inc.params.get("tema", an.tema)
        for k in HEREDABLES if tema_inc == tema_previo else ("alpha",):
            if k not in inc.params and k in previo and not (k == "tail" and inc.tipo in ("ensayo", "diseno")):
                inc.params[k] = previo[k]
        # el ensayo que sigue al diseño usa ESE plan: H0 se fija antes de ver la muestra (el modelo suele reorientarla
        # mirando los datos del inciso)
        if inc.tipo == "ensayo" and diseno_previo is not None and diseno_previo.params.get("tail") and \
                tema_inc == diseno_previo.params.get("tema", an.tema):
            inc.params["tail"] = diseno_previo.params["tail"]
        if inc.tipo == "diseno":
            diseno_previo = inc
        if inc.tipo == "diseno" and "beta" not in inc.params and "beta" in an.datos:
            inc.params["beta"] = an.datos["beta"]
        tema_previo = tema_inc
        previo.update(inc.params)
