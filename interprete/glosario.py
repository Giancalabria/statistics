"""Frases típicas de los enunciados de la cátedra y qué significan / qué hay que hacer.

`buscar_frases(texto)` devuelve las que aparecen en el enunciado, para mostrarlas
como 'pistas de lectura'. `COMO_PRESENTAR` indica qué pasos espera ver la cátedra
en cada tipo de pregunta.
"""

import re
from typing import List, Tuple

from .texto import normalizar

# (patrón sobre texto normalizado, frase de ejemplo, qué significa)
FRASES: List[Tuple[str, str, str]] = [
    # --- datos
    (r"desvio (estandar )?(poblacional|historico)|registros historicos|se sabe[^.]{0,40}desvio|por experiencia",
     "desvío histórico / poblacional / 'se sabe que el desvío...'",
     "σ es CONOCIDO → se usa la normal Z (aunque la muestra sea chica)."),
    (r"(la|una) muestra[^.]{0,60}(arrojo|dio|se obtuvo|resulto)[^.]{0,40}desvio",
     "'la muestra arrojó un desvío de...'",
     "Es el desvío MUESTRAL S → si no hay σ conocido, se usa t de Student con ν = n-1."),
    (r"no se conoce|se considera desconocido|si no se conociera",
     "'si el desvío no se conociera'",
     "Rehacer con S (calculado de la muestra) y t de Student en lugar de σ y Z."),
    (r"varianza (dio|de|fue)", "'la varianza dio 456'", "Es S²: el desvío es S = √S²."),
    (r"poblacion (total )?de|sobre un lote de|partida de \d", "'población de 1.200' / 'lote de 1.400'",
     "Población FINITA: si n/N > 5% aplicá el factor √((N-n)/(N-1)) al error estándar (y n = N·n∞/(N+n∞))."),
    (r"en miles", "'en miles'", "Cuidado con las unidades: los datos pueden estar en miles y μ₀ en unidades."),
    # --- estimación
    (r"estimar|intervalo de confianza|limites de confianza|entre que valores",
     "'estimar...' / 'límites de confianza' / '¿entre qué valores...?'",
     "Intervalo de confianza. Presentación: P(A ≤ parámetro ≤ B) = 1-α."),
    (r"(\d+ ?% de riesgo|riesgo del \d)", "'con un 10% de riesgo'", "Riesgo = α (nivel de confianza 1-α)."),
    (r"error (muestral|de muestreo|de (la )?estimacion)", "'error muestral / de muestreo de ± e'",
     "Es e, la semiamplitud del intervalo (e = Z·σ/√n o t·S/√n). NO es α."),
    (r"cuant[oa]s? [a-z ]{0,30}mas", "'¿cuántos ... más habría que tomar?'",
     "Pide Δn = n_necesario - n_actual (no el n total)."),
    (r"(reducir|disminuir)[^.]{0,30}(\d+ ?%|mitad|tercera parte)", "'reducir el error en un 30%' / 'a la mitad'",
     "e_nuevo = e_actual·(1 - reducción) → recalcular n (iterando si se usa t)."),
    (r"relacion entre (ambos )?(los )?limites|limite superior sea (el doble|un \d)",
     "'relación entre límites' / 'límite superior el doble del inferior'",
     "Varianza: R' = B'/A' (cociente entre límites del desvío) → n por Ecuación de García."),
    (r"(maxim[oa]|minim[oa])[^.]{0,40}(con una probabilidad|confianza)|desviacion estandar maxima",
     "'el valor máximo ... con probabilidad 0,95'", "Límite de confianza UNILATERAL: todo α en una cola."),
    (r"total (de la poblacion|poblacional)|peso total|produccion total", "'estimar el total de la población'",
     "Total T = N·μ: multiplicar los límites del IC de la media por N."),
    # --- ensayos
    (r"se puede (asegurar|afirmar)|hay (razon|evidencia)|es concluyente",
     "'¿se puede asegurar que...?'", "Ensayo de hipótesis: lo que se quiere ASEGURAR va en H1."),
    (r"riesgo[^.]{0,40}(comprar|lanzar|implementar|cambiar|instalar|adoptar)[^.]{0,30}(equivocad|erronea|cuando no)",
     "'riesgo de comprar / lanzar equivocadamente'", "Esa probabilidad es α: rechazar H0 cuando es cierta."),
    (r"(inversion|compra|nuevo|nueva|aditivo|campana|lanzar|modificacion)",
     "cambio / inversión / producto nuevo", "Criterio PESIMISTA: H0 = 'no mejora' (el cambio no funciona)."),
    (r"(control de recepcion|partida|lote|especificacion|contrato|proveedor)",
     "control de recepción / especificación", "Criterio OPTIMISTA: H0 = 'el lote cumple la especificación'."),
    (r"por lo menos|como minimo|minimo admisible|mayor o igual",
     "'debe ser por lo menos...' / 'mínimo admisible'", "Especificación mínima: H0: μ ≥ μ₀, se rechaza si x̄ < x̄c (cola izquierda)."),
    (r"como maximo|a lo sumo|no debe superar|menor o igual",
     "'como máximo' / 'no debe superar'", "Especificación máxima: H0: μ ≤ μ₀ (o σ ≤ σ₀), se rechaza si da alto (cola derecha)."),
    (r"diferente de|desajust|fuera de control|bajo control|limites de control|aumentando o disminuyendo",
     "'es diferente de...' / 'límites de control'", "Ensayo BILATERAL: H0: μ = μ₀, dos valores críticos."),
    (r"probabilidad de no (detectar|efectuar|concretar|iniciar|detener)|aceptar una partida",
     "'probabilidad de NO detectar...' / 'de aceptar una partida mala'", "Es β (error de tipo II)."),
    (r"probabilidad de (detectar|rechazar|detener|implementar|comprar)",
     "'probabilidad de detectar...'", "Es la potencia 1-β (rechazar H0 cuando es falsa)."),
    (r"sistema de muestreo|condicion de rechazo|regla de decision|hipotesis nula apropiada",
     "'hipótesis nula apropiada, condición de rechazo y regla de decisión'",
     "Diseño del ensayo: H0 (criterio), x̄c (CR: si x̄ > / < x̄c se rechaza H0), n y la regla en palabras del problema."),
    (r"probabilidad anterior valga", "'¿cuántas ... si se pretende que la probabilidad anterior valga 0,10?'",
     "n para α y β fijados: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]²."),
    (r"curva (caracteristica|operativa|de potencia)|curvas", "'dibujar las curvas OC y de potencia'",
     "Tabla de μ vs β (curva OC) y μ vs 1-β (potencia); marcar al menos 3 puntos con sus valores."),
    # --- proporción
    (r"fraccion defectuosa|porcentaje de|proporcion de|rating", "porcentaje / fracción defectuosa",
     "Parámetro p (Bernoulli). IC exacto con Beta/F; n para estimar p por aproximación normal."),
    (r"puntos porcentuales", "'2 puntos porcentuales'", "Se suman al porcentaje: 5% + 2 puntos = 7% (no 5%·1,02)."),
]

COMO_PRESENTAR = {
    "ic": [
        "Definir la variable y el parámetro (X: ..., μ / σ² / p).",
        "Distribución: Z (σ conocido), t con ν = n-1 (σ desconocido), χ² (varianza), Beta/F (proporción).",
        "Fórmula de los límites con los valores reemplazados.",
        "Conclusión con la notación de la cátedra: P(A ≤ parámetro ≤ B) = 1-α, en las unidades del problema.",
    ],
    "n": [
        "Fórmula de n según el caso (Z directo, o t iterando porque t depende de n).",
        "Redondear SIEMPRE hacia arriba.",
        "Si ya había una muestra: responder Δn = n - n_actual ('hay que tomar X más').",
    ],
    "ensayo": [
        "Planteo de hipótesis: criterio (optimista / pesimista), H0 vs H1 (la igualdad siempre en H0).",
        "Nivel de significación α = P(rechazar H0 | H0 cierta).",
        "Estadístico de prueba: Z (σ conocido), t con ν = n-1 (solo se tiene S), χ² (varianza), binomial (proporción).",
        "Condición de rechazo (CR): valor crítico (x̄c, S²c, r_c) y zona de rechazo.",
        "Regla de decisión (RD) en lenguaje llano y ANTES de calcular: 'se toma una muestra de n..., si x̄ > x̄c se "
        "rechaza H0 → acción; si no → otra acción'.",
        "Cálculos: valor observado y si cae o no en la zona de rechazo.",
        "Conclusión formal: 'A un nivel de significación del α%, (no) existe evidencia estadística suficiente para "
        "rechazar H0... Por consiguiente, <acción>' (NUNCA 'se acepta H0').",
    ],
    "beta": [
        "Recordar la región crítica del ensayo (x̄c).",
        "β = P(no rechazar H0 | parámetro = valor alternativo); potencia = 1-β.",
        "Estandarizar con el valor alternativo: Z = (x̄c - μ₁)/(σ/√n).",
    ],
    "diseno": [
        "H0 según el criterio (optimista / pesimista) y H1.",
        "Plantear las dos condiciones: P(rechazar | μ₀) = α y P(no rechazar | μ₁) = β.",
        "Resolver n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² (redondear arriba) y x̄c.",
        "Condición de rechazo (CR) y regla de decisión (RD) en palabras del problema.",
    ],
    "curva": [
        "Tabla con varios valores del parámetro: β (curva OC) y 1-β (curva de potencia).",
        "Ejes: abscisa = parámetro (μ); ordenada = probabilidad. Marcar al menos 3 puntos.",
    ],
}


def buscar_frases(texto: str) -> List[Tuple[str, str]]:
    norm = normalizar(texto)
    salida = []
    for patron, frase, significado in FRASES:
        if re.search(patron, norm):
            salida.append((frase, significado))
    return salida
