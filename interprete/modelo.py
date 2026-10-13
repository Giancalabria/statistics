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
    "regresion": "Regresión y correlación simple (TEMA VII)",
    "regresion_multiple": "Modelo lineal general / regresión múltiple (TEMA VIII)",
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
    "dos_varianzas": ["ensayo", "ic", "n", "beta", "diseno", "no_soportado"],
    "dos_medias": ["ensayo", "ic", "n", "diseno", "beta", "no_soportado"],
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

# Temas resueltos en módulos aparte (interprete/chi_modelos.py, interprete/regresion.py):
# EXTENSIONES[tema] = (completar_planteo(an, t), clasificar(inc, an, norm) -> (tipo, razón))
# DESPACHO_EXTRA[(tema, tipo)] = función(d, alpha, res, estado), igual que en resolver.DESPACHO
EXTENSIONES: Dict[str, tuple] = {}
DESPACHO_EXTRA: Dict[tuple, Any] = {}

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
    "escala": ("Escala de los datos (1000 = vienen 'en miles')", "float"),
    "rc": ("Plan dado: se rechaza H0 si r ≥ r_c", "int"),
    "costo_fijo": ("Costo fijo que se descuenta de la media (neto = bruto - c)", "float"),
    # 2 poblaciones
    "n1": ("n₁", "int"), "xbar1": ("x̄₁", "float"), "s1": ("S₁", "float"),
    "n2": ("n₂", "int"), "xbar2": ("x̄₂", "float"), "s2": ("S₂", "float"),
    "datos1": ("Datos muestra 1", "lista"), "datos2": ("Datos muestra 2", "lista"),
    "nombre1": ("Nombre muestra 1", "texto"), "nombre2": ("Nombre muestra 2", "texto"),
    "apareadas": ("¿Muestras apareadas (mismos individuos)?", "bool"),
    "phi0": ("Relación de desvíos de referencia φ₀ = σ₁/σ₂ (0,88 = reducir 12%)", "float"),
    "phi1": ("Relación de desvíos alternativa φ₁ (diseño)", "float"),
    "sujeto": ("¿Qué muestra va primero en δ = μ(1º) - μ(2º)? (1 o 2)", "int"),
    "sigma_pob1": ("σ₁ poblacional conocido (Z)", "float"), "sigma_pob2": ("σ₂ poblacional conocido (Z)", "float"),
    "sigma_afirmado": ("¿Los σ solo se afirman? (se verifican con χ² antes de usarlos)", "bool"),
    "alpha_var": ("Riesgo del test F previo de desvíos (la guía usa 0,10)", "float"),
    # chi-cuadrado
    "tabla": ("Tabla de frecuencias observadas", "tabla"),
    "observados": ("Frecuencias observadas Fo", "lista"),
    "esperados": ("Frecuencias esperadas Fe", "lista"),
    "proporciones": ("Proporciones teóricas de cada categoría", "lista"),
    "p_estimados": ("Parámetros estimados de la muestra (p)", "int"),
    "clases": ("Clases (li ; ls por renglón)", "tabla"),
    "valores_var": ("Valores de la variable / categorías", "lista"),
    "modelos": ("Modelo(s) a ajustar (normal, poisson, binomial, weibull, gumbel_max, gumbel_min, pareto, lognormal, "
                "exponencial, gamma, uniforme)", "texto"),
    # regresión
    "x": ("Variable explicativa x (datos)", "lista"),
    "y": ("Variable a explicar y (datos)", "lista"),
    "nombre_x": ("Nombre de x", "texto"),
    "nombre_y": ("Nombre de y", "texto"),
    "escala_x": ("Escala de x en la tabla (1.000 = 'en miles')", "float"),
    "escala_y": ("Escala de y en la tabla (1.000 = 'en miles')", "float"),
    "xs": ("Variables explicativas (una por renglón)", "tabla"),
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
    "delta1": ("Diferencia real δ₁ (para β / potencia)", "float"),
    "delta0_pct": ("Diferencia proporcional (0,10 = 'supera en un 10%': μ₁ vs 1,10·μ₂)", "float"),
    "sujeto": ("¿Qué muestra va primero en δ? (1 o 2)", "int"),
    "porcentual": ("¿Pide la diferencia porcentual (h = μ₁/μ₂)?", "bool"),
    "phi0": ("φ₀ = σ₁/σ₂ de este inciso", "float"),
    "phi1": ("Relación de desvíos alternativa φ₁", "float"),
    "sobre": ("¿Relación entre desvíos o varianzas? ('desvios' / 'varianzas')", "texto"),
    "total": ("¿Pide el total poblacional (N·μ)?", "bool"),
    "mu0": ("μ₀ de este inciso", "float"),
    "sigma0": ("σ₀ de este inciso", "float"),
    "p0": ("p₀ de este inciso", "float"),
    "n": ("n de este inciso", "int"),
    "r": ("r (casos) de este inciso", "int"),
    "p_hat": ("p̂ de este inciso", "float"),
    "ambos": ("¿Calcular para la media y para el desvío?", "bool"),
    "repeticiones": ("Veces que se repite el ensayo (muestras independientes)", "int"),
    "costo_unitario": ("Costo por unidad muestreada (para la inversión)", "float"),
    "prob_aceptar": ("Probabilidad de aceptación pedida (plan con r_c dado)", "float"),
    "costo_fijo": ("Costo fijo a descontar de la media (neto = bruto - costo)", "float"),
    "comision": ("Comisión sobre lo recaudado (fracción: 0,02 = 2%)", "float"),
    # regresión
    "x0": ("x₀ para el pronóstico (en unidades de la tabla)", "float"),
    "individual": ("¿Pronóstico de un valor individual? (si no, del promedio)", "bool"),
    "cola": ("Límites: bilateral / inferior (mínimo) / superior (máximo)", "texto"),
    "beta10": ("β1₀ de la afirmación (cambio de y por unidad de x)", "float"),
    "modelo": ("Modelo: lineal / loglog / loglin / linlog", "texto"),
    "origen": ("¿Recta por el origen (b0 = 0)?", "bool"),
    "variables": ("Variables del modelo reducido (números: 1 3)", "lista"),
    "modelos": ("Modelo(s) a ajustar en este inciso (separados por coma)", "texto"),
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
    tablas: List[Dict[str, Any]] = field(default_factory=list)  # tablas de datos del enunciado
