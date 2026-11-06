"""IA con un prompt POR TEMA: la tercera lectura del consenso.

En dos pasos: (1) una consulta corta clasifica el tema del planteo y el de cada inciso; (2) el JSON del planteo se pide
con un prompt que trae solo las reglas, los tipos de inciso y las claves de esos temas, y ejemplos de la guía del mismo
tema. El prompt queda en ~4-5 mil caracteres (el de `interpretar.pedir_ia` lleva el catálogo de todos los temas,
~14,5 mil).

Medido el 04/11/2026 con qwen3:8b en los exámenes del 2° parcial (30 incisos con referencia): sola acierta menos que
la IA con ejemplos (23 contra 27), pero se equivoca en OTROS incisos, y en el consenso reemplaza con ventaja a la IA
razonada (`simple.plantear`): consenso 30/30 en lugar de 29/30 (Q1c), y ~32 s por problema en lugar de ~104 s.

    from asistente.por_tema import pedir_ia_tema
    an, avisos = pedir_ia_tema(planteo, incisos, tablas)
"""

import json
from typing import Dict, List, Optional, Sequence, Tuple

from interprete import buscador
from interprete.analizador import analizar
from interprete.modelo import CAMPOS_PLANTEO, TEMAS, TIPOS, TIPOS_POR_TEMA, Analisis, Inciso

from . import cliente
from .esquema import CAMPOS_INC, ENUMS, a_dict, desde_dict
from .interpretar import MAX_EJEMPLO, MAX_TOKENS_JSON, _enunciado, _parsear, con_tablas, lista_incisos

CLASIFICAR = """Clasificá un enunciado de Estadística Aplicada (UADE). NO resuelvas nada.

Temas posibles:
- proporcion: proporción / porcentaje de UNA población (defectuosos, aprobados, «x de las n unidades», «penetración \
en el mercado», «el 40% de los habitantes»).
- media: media de UNA población (μ, x̄, promedio de una sola muestra).
- varianza: varianza o desvío de UNA población (dispersión, «el desvío no supere…», relación entre los límites de σ).
- dos_varianzas: comparar la variabilidad / dispersión / desvío / homogeneidad de DOS grupos (test F, φ = σ1/σ2).
- dos_medias: comparar promedios / rendimientos / performance de DOS grupos (independientes o apareadas, «supera en \
X», «diferencia de más del X%», «diferencia mínima/máxima esperada»).
- chi_ajuste: ¿los datos se ajustan a / siguen un modelo o ley (Normal, Poisson, Exponencial, Gamma, Weibull…)? \
Frecuencias observadas contra un modelo.
- chi_contingencia: asociación / independencia entre dos variables categóricas, o si los porcentajes de varios grupos \
son homogéneos (tabla de doble entrada).
- regresion: relación lineal entre X e Y con pares de datos (recta, pronóstico, «por cada unidad de X», r²).
- regresion_multiple: varias variables explicativas o elegir entre modelos (R² ajustado, Cp, PRESS, DET).

Un problema puede mezclar temas: un inciso puede ser de otro tema que el planteo (por ejemplo, en un problema de \
comparación de medias con una tabla por clases, un inciso que pregunta si los datos de una máquina «se ajustan a un \
modelo Normal» es chi_ajuste). Clasificá cada inciso por lo que pregunta ESE inciso.

Respondé solo JSON: {"tema": "<tema del planteo>", "incisos": {"a": "<tema>", "b": "<tema>"}}"""

_UNA_POB_INC = ["tail", "alpha", "e", "reduccion", "beta", "prob", "n", "cota"]
# claves de cada tema: las mismas de esquema.CLAVES_TEMA, pero sin las de los otros temas (allá los incisos aceptan
# las de 1 y 2 poblaciones en todos los temas, y el prompt crece)
PARAMS = {
    "media": _UNA_POB_INC + ["usar_S", "mu0", "mu1", "total", "costo_fijo", "repeticiones", "comision"],
    "varianza": _UNA_POB_INC + ["sigma0", "sigma1", "relacion", "ambos"],
    "proporcion": _UNA_POB_INC + ["p0", "p1", "r", "p_hat", "costo_unitario", "prob_aceptar"],
    "dos_varianzas": ["tail", "alpha", "beta", "prob", "phi0", "phi1", "sobre", "relacion", "reduccion", "n", "cota"],
    "dos_medias": ["tail", "alpha", "delta0", "delta1", "delta0_pct", "sujeto", "porcentual", "beta", "prob", "n",
                   "e", "reduccion", "cota"],
    "chi_contingencia": ["alpha"],
    "chi_ajuste": ["alpha", "modelos"],
    "regresion": ["alpha", "x0", "individual", "cola", "beta10", "modelo", "origen", "tail", "validar", "rho2",
                  "x0_puntual"],
    "regresion_multiple": ["alpha", "variables", "modelos"],
}
DATOS = {
    "media": ["n", "xbar", "desvio", "sigma_conocido", "N", "mu0", "datos", "alpha", "e", "reduccion", "beta", "mu1",
              "control", "doble", "escala", "costo_fijo"],
    "varianza": ["n", "desvio", "sigma_conocido", "sigma0", "xbar", "mu0", "datos", "alpha", "beta", "e", "reduccion",
                 "doble", "control"],
    "proporcion": ["n", "r", "p_hat", "p0", "N", "alpha", "beta", "e", "reduccion", "rc", "control"],
    "dos_varianzas": ["n1", "n2", "s1", "s2", "xbar1", "xbar2", "datos1", "datos2", "nombre1", "nombre2", "apareadas",
                      "phi0", "phi1", "sujeto", "alpha", "beta"],
    "dos_medias": ["n1", "n2", "xbar1", "xbar2", "s1", "s2", "datos1", "datos2", "nombre1", "nombre2", "apareadas",
                   "sujeto", "sigma_pob1", "sigma_pob2", "sigma_afirmado", "alpha_var", "alpha", "beta"],
    "chi_contingencia": ["tabla", "alpha"],
    "chi_ajuste": ["observados", "esperados", "proporciones", "p_estimados", "clases", "valores_var", "modelos",
                   "alpha"],
    "regresion": ["x", "y", "nombre_x", "nombre_y", "escala_x", "escala_y", "alpha"],
    "regresion_multiple": ["xs", "y", "nombre_y", "escala_y", "alpha"],
}
_UNA_O_DOS = {"media", "varianza", "proporcion", "dos_varianzas", "dos_medias"}

COMUNES = """Sos un asistente que INTERPRETA un enunciado de Estadística Aplicada (UADE, cátedra Dopazo – García) y lo \
traduce a un JSON que resuelve un programa. NO calculás nada: anotás el tema, los datos que da el enunciado y qué pide \
cada inciso.

Reglas:
- Usá EXACTAMENTE las claves de abajo y poné solo lo que el enunciado dice (no inventes ni calcules; no pongas 0, \
null ni valores por defecto).
- Números decimales JSON (0.05, no "5%"). Porcentajes como fracción (5% → 0.05).
- alpha = 1 − confianza (95% → 0.05). «Riesgo», «significación», «probabilidad de concluir / rechazar por error» → \
alpha. «Probabilidad de no detectar» → beta; «probabilidad de detectar» = potencia = 1 − beta.
- Cada inciso lleva su letra (a, b, c…; «única» si no hay incisos) y en params solo lo que ese inciso agrega o \
cambia. Si un inciso es de otro tema que el planteo, poné params.tema con ese tema y sus datos en params.
- Si un inciso no lo resuelve el programa (teórico), tipo «no_soportado»."""

UNA_DOS_POB = """
Lectura (el profesor redacta confuso a propósito):
- ¿Me dan los que CUMPLEN y preguntan por los que NO (o al revés)? Entonces el parámetro es el del complemento.
- ¿Es un TOTAL y no un promedio? ¿Una VARIANZA (unidades²) o un desvío? ¿Están en la misma unidad?
- tail: «derecha» si H1 dice que el parámetro es MAYOR, «izquierda» si es MENOR, «bilateral» si es distinto. La \
igualdad va siempre en H0; lo que se quiere probar (un cambio, una mejora, que una política funcionó) va en H1.
- criterio: «pesimista» si se decide un cambio / inversión / reclamo que solo se hace con evidencia (lo bueno va en \
H1); «optimista» si es un control de rutina (H0 = el proceso está bien).
- «Como máximo» / «como mínimo» en una estimación: un solo límite (cota «sup» / «inf»), con α entero."""

DOS_POB = """
- ¿Quién es el sujeto? «B tarda X menos que A» ⇒ μA − μB; «A supera a B en más del 10%» ⇒ delta0_pct = 0.10 con A \
primero (sujeto = 1 si va primero la muestra 1).
- Apareadas solo si son los MISMOS individuos o unidades medidos dos veces (no porque los n sean iguales)."""

CHI = """
- Bondad de ajuste: «se ajusta a», «sigue la ley», «responde a un modelo» → chi_ajuste con modelos = el modelo \
nombrado (normal, poisson, binomial, weibull, gumbel_max, gumbel_min, pareto, lognormal, exponencial, gamma, \
uniforme). Las frecuencias de la tabla las carga el programa.
- Independencia / asociación o porcentajes de varios grupos → chi_contingencia (la tabla la carga el programa)."""

REGRESION = """
- Y es la variable a explicar y X la explicativa. Las listas x, y las carga el programa desde la tabla.
- «Por cada unidad de X, cuánto cambia Y / cuál es el máximo o mínimo» es el coeficiente β1 (ic_coef o \
ensayo_coef), NO un pronóstico en x = 1. «Influencia porcentual» = r² (ic_rho2). Un pronóstico necesita un valor de X \
(x0); para el promedio de Y, individual = false; para un valor individual, individual = true."""


def _linea(clave: str, etiqueta: str, tipo: str) -> str:
    extra = f" — uno de: {', '.join(ENUMS[tipo])}" if tipo in ENUMS else ""
    return f"- {clave} ({tipo}): {etiqueta}{extra}"


def sistema_para(tema: str, temas_inc: Sequence[str] = ()) -> str:
    """El prompt de sistema con solo lo que sirve para `tema` (y los temas de incisos que sean de otro)."""
    todos = [tema] + [t for t in dict.fromkeys(temas_inc) if t != tema and t in DATOS]
    partes = [COMUNES]
    if any(t in _UNA_O_DOS for t in todos):
        partes.append(UNA_DOS_POB)
    if any(t in ("dos_varianzas", "dos_medias") for t in todos):
        partes.append(DOS_POB)
    if any(t.startswith("chi") for t in todos):
        partes.append(CHI)
    if any(t.startswith("regresion") for t in todos):
        partes.append(REGRESION)
    partes.append(f"\nTema del planteo: \"{tema}\" ({TEMAS[tema]}).")
    for t in todos:
        tipos = "; ".join(f'"{x}" = {TIPOS.get(x, x)}' for x in TIPOS_POR_TEMA.get(t, []))
        partes.append(f"\nTIPOS de inciso en {t}: {tipos}")
    partes.append("\nDATOS DEL PLANTEO (objeto «datos»):\n"
                  + "\n".join(_linea(k, *CAMPOS_PLANTEO[k]) for k in DATOS[tema] if k in CAMPOS_PLANTEO))
    params = list(dict.fromkeys(k for t in todos for k in PARAMS.get(t, [])))
    if len(todos) > 1:
        params.append("tema")
    partes.append("\nPARÁMETROS DE CADA INCISO (objeto «params»):\n"
                  + "\n".join(_linea(k, *CAMPOS_INC[k]) for k in params if k in CAMPOS_INC))
    criterio = '"criterio": "optimista|pesimista|ninguno", ' if any(t in _UNA_O_DOS for t in todos) else ""
    partes.append(f'\nFormato: {{"tema": "...", {criterio}"datos": {{...}}, '
                  '"incisos": [{"letra": "a", "tipo": "...", "params": {...}}]}')
    return "\n".join(partes)


def ejemplos_tema(texto: str, tema: str, k: int = 2, excluir: Sequence[str] = ()) -> List[Tuple[str, str]]:
    """Ejercicios parecidos de la guía, solo del MISMO tema, con el JSON que arman las reglas (verificado)."""
    romano = buscador.TEMA_A_GUIA.get(tema)
    salida = []
    for _, ej in buscador.buscar(texto, k=20, tema=tema):
        if ej["id"] in excluir or (romano and ej["tema"] != romano):
            continue
        if ej["incisos"] and ej["incisos"][0]["letra"] == "única":
            pl, incs = ej["enunciado"], None
        else:
            pl, incs = ej["planteo"], [(i["letra"], i["texto"]) for i in ej["incisos"]]
        an = analizar(pl, incs, tablas=ej.get("tablas") or None)
        if an.tema != tema:
            continue
        js = json.dumps(a_dict(an), ensure_ascii=False)
        if len(js) > MAX_EJEMPLO:
            continue
        salida.append((_enunciado(pl, lista_incisos(pl, incs)[1]), js))
        if len(salida) >= k:
            break
    return salida


def clasificar(texto: str, letras: Sequence[str], modelo: Optional[str] = None) -> Dict:
    """-> {"tema": tema del planteo o None, "incisos": {letra: tema}}."""
    js = cliente.chat([{"role": "system", "content": CLASIFICAR},
                       {"role": "user", "content": f"ENUNCIADO:\n{texto}\n\nIncisos: {', '.join(letras)}"}],
                      modelo=modelo, formato="json", temperatura=0, max_tokens=200)
    d = _parsear(js)
    tema = d.get("tema") if d.get("tema") in TEMAS and d.get("tema") != "desconocido" else None
    incisos = d.get("incisos") if isinstance(d.get("incisos"), dict) else {}
    return {"tema": tema, "incisos": {str(k).lower().strip(") "): v for k, v in incisos.items()
                                      if v in TEMAS and v != "desconocido"}}


def pedir_ia_tema(planteo: str, incisos=None, tablas=None, modelo: Optional[str] = None,
                  excluir: Sequence[str] = ()) -> Tuple[Analisis, List[str]]:
    """El planteo completo armado por la IA con el prompt del tema (sin mezclar con las reglas, salvo que la
    clasificación falle: entonces el tema lo dan las reglas). Devuelve el análisis validado + avisos."""
    planteo, lista = lista_incisos(planteo, incisos)
    enun = _enunciado(con_tablas(planteo, tablas), lista)
    cl = clasificar(enun, [l for l, _ in lista] or ["única"], modelo)
    tema = cl["tema"] or analizar(planteo, lista or None, tablas=tablas).tema
    if tema not in DATOS:
        tema = "media"
    msgs = [{"role": "system", "content": sistema_para(tema, list(cl["incisos"].values()))}]
    for e_txt, e_js in ejemplos_tema(enun, tema, 2, excluir):
        msgs += [{"role": "user", "content": f"ENUNCIADO:\n{e_txt}"}, {"role": "assistant", "content": e_js}]
    msgs.append({"role": "user", "content": f"ENUNCIADO:\n{enun}"})
    d = _parsear(cliente.chat(msgs, modelo=modelo, formato="json", temperatura=0, max_tokens=MAX_TOKENS_JSON))
    if d.get("tema") not in TEMAS:
        d["tema"] = tema
    for inc in d.get("incisos") or []:          # el tema de cada inciso que dio la clasificación, si el JSON no lo trae
        if isinstance(inc, dict):
            t = cl["incisos"].get(str(inc.get("letra", "")).lower())
            if t and t != d["tema"]:
                if not isinstance(inc.get("params"), dict):
                    inc["params"] = {}
                inc["params"].setdefault("tema", t)
    an, avisos = desde_dict(d, planteo, dict(lista))
    an.tablas = list(tablas) if tablas else []
    if not an.incisos:
        an.incisos = [Inciso(letra=l, texto=t) for l, t in (lista or [("única", planteo)])]
    an.razones_tema = ["Tema identificado por la IA (prompt por tema)."]
    return an, avisos
