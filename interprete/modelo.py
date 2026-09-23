"""Estructuras del análisis de un enunciado y catálogo de campos editables.

Todo lo que detecta el analizador queda en diccionarios simples (`datos`,
`params`) para que la pantalla pueda mostrarlos y el usuario corregirlos antes
de calcular.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Temas (qué tipo de problema es) y tipos de pregunta por inciso
# ---------------------------------------------------------------------------

TEMAS = {
    "media": "Media de 1 población (μ)",
    "varianza": "Varianza / desvío de 1 población (σ², σ)",
    "proporcion": "Proporción de 1 población (p)",
    "dos_varianzas": "Comparación de 2 varianzas (test F)",
    "dos_medias": "Comparación de 2 medias",
    "chi_contingencia": "Chi² — tabla de contingencia (independencia / homogeneidad)",
    "chi_ajuste": "Chi² — bondad de ajuste",
    "regresion": "Regresión / correlación (no lo calcula la app)",
    "desconocido": "No identificado",
}

TIPOS = {
    "ic": "Intervalo de confianza (estimar)",
    "n": "Tamaño de muestra",
    "ensayo": "Ensayo de hipótesis (decidir)",
    "beta": "Probabilidad de error / potencia (β, 1-β)",
    "diseno": "Diseñar el ensayo (H0, n, valor crítico, regla de decisión)",
    "curva": "Curva característica operativa / de potencia",
    "no_soportado": "No lo resuelve la app (teórico / otro tema)",
}

# Tipos que tienen sentido en cada tema (para los desplegables de la pantalla).
TIPOS_POR_TEMA = {
    "media": ["ic", "n", "ensayo", "beta", "diseno", "curva", "no_soportado"],
    "varianza": ["ic", "n", "ensayo", "beta", "diseno", "no_soportado"],
    "proporcion": ["ic", "n", "ensayo", "beta", "diseno", "curva", "no_soportado"],
    "dos_varianzas": ["ensayo", "ic", "no_soportado"],
    "dos_medias": ["ensayo", "ic", "n", "no_soportado"],
    "chi_contingencia": ["ensayo", "no_soportado"],
    "chi_ajuste": ["ensayo", "no_soportado"],
    "regresion": ["no_soportado"],
    "desconocido": ["no_soportado"],
}

COLAS = {
    "derecha": "Unilateral derecha (H1: parámetro > valor)",
    "izquierda": "Unilateral izquierda (H1: parámetro < valor)",
    "bilateral": "Bilateral (H1: parámetro ≠ valor)",
}

# ---------------------------------------------------------------------------
# Catálogo de campos: clave -> (etiqueta, tipo)
# tipo: "float" | "int" | "bool" | "lista" | "tabla"
# ---------------------------------------------------------------------------

CAMPOS_PLANTEO = {
    # 1 población
    "n": ("Tamaño de muestra n", "int"),
    "xbar": ("Media muestral x̄", "float"),
    "desvio": ("Desvío (σ si es poblacional, S si es muestral)", "float"),
    "sigma_conocido": ("¿El desvío es poblacional (σ conocido)?", "bool"),
    "N": ("Tamaño de la población N (población finita)", "float"),
    "mu0": ("Valor de referencia de la media μ₀", "float"),
    "sigma0": ("Valor de referencia del desvío σ₀", "float"),
    "r": ("Cantidad de éxitos / defectuosos r", "int"),
    "p_hat": ("Proporción muestral p̂", "float"),
    "p0": ("Proporción de referencia p₀", "float"),
    "datos": ("Datos crudos de la muestra", "lista"),
    "alpha": ("Riesgo α (1 - confianza)", "float"),
    "e": ("Error muestral admitido e", "float"),
    "reduccion": ("Reducción pedida (fracción, 0,30 = 30%)", "float"),
    "beta": ("β (prob. de no detectar la alternativa)", "float"),
    "mu1": ("Media alternativa μ₁", "float"),
    "control": ("¿Sistema de control? (rechazar H0 = detener el proceso)", "bool"),
    "doble": ("¿Doble condición (media Y desvío)? → dos ensayos", "bool"),
    # 2 poblaciones
    "n1": ("n₁", "int"), "xbar1": ("x̄₁", "float"), "s1": ("S₁", "float"),
    "n2": ("n₂", "int"), "xbar2": ("x̄₂", "float"), "s2": ("S₂", "float"),
    "datos1": ("Datos muestra 1", "lista"), "datos2": ("Datos muestra 2", "lista"),
    "nombre1": ("Nombre muestra 1", "texto"), "nombre2": ("Nombre muestra 2", "texto"),
    "apareadas": ("¿Muestras apareadas (mismos individuos)?", "bool"),
    # chi-cuadrado
    "tabla": ("Tabla de frecuencias observadas", "tabla"),
    "observados": ("Frecuencias observadas Fo", "lista"),
    "esperados": ("Frecuencias esperadas Fe", "lista"),
    "proporciones": ("Proporciones teóricas de cada categoría", "lista"),
    "p_estimados": ("Parámetros estimados de la muestra (p)", "int"),
}

CAMPOS_INCISO = {
    "tail": ("Cola del ensayo", "cola"),
    "alpha": ("Riesgo α de este inciso", "float"),
    "e": ("Error muestral admitido e", "float"),
    "reduccion": ("Reducción pedida (fracción, 0,30 = 30%)", "float"),
    "relacion": ("Relación entre límites R' = B/A buscada", "float"),
    "mu1": ("Media alternativa μ₁", "float"),
    "sigma1": ("Desvío alternativo σ₁", "float"),
    "p1": ("Proporción alternativa p₁", "float"),
    "beta": ("β objetivo (prob. de no detectar)", "float"),
    "prob": ("¿Qué probabilidad pide?", "prob"),
    "delta0": ("Diferencia de referencia δ₀", "float"),
    "total": ("¿Pide el total poblacional (N·μ)?", "bool"),
    "mu0": ("μ₀ de este inciso", "float"),
    "sigma0": ("σ₀ de este inciso", "float"),
    "p0": ("p₀ de este inciso", "float"),
    "n": ("n de este inciso", "int"),
    "r": ("r (casos) de este inciso", "int"),
    "p_hat": ("p̂ de este inciso", "float"),
    "ambos": ("¿Calcular para la media y para el desvío?", "bool"),
}


@dataclass
class Evidencia:
    """Por qué se tomó un dato: el fragmento del enunciado que lo justifica."""
    clave: str
    valor: Any
    fragmento: str
    motivo: str = ""


@dataclass
class Inciso:
    letra: str
    texto: str
    tipo: str = "no_soportado"
    params: Dict[str, Any] = field(default_factory=dict)
    que_pide: str = ""
    razones: List[str] = field(default_factory=list)


@dataclass
class Analisis:
    planteo: str
    tema: str = "desconocido"
    datos: Dict[str, Any] = field(default_factory=dict)
    evidencias: List[Evidencia] = field(default_factory=list)
    razones_tema: List[str] = field(default_factory=list)
    criterio: Optional[str] = None       # "optimista" | "pesimista"
    criterio_razon: str = ""
    incisos: List[Inciso] = field(default_factory=list)
    avisos: List[str] = field(default_factory=list)
