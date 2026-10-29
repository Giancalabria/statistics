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
     "Población FINITA: si el enunciado da N, aplicá (siempre, sin umbral) el factor √((N-n)/N) al error estándar (y n = N·n∞/(N+n∞))."),
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
        "Estadístico de prueba: Z si al estandarizar x̄ se divide por el parámetro σ (una constante: sigue normal); t con "
        "ν = n-1 si se divide por S (una variable aleatoria); χ² (varianza), binomial exacta (proporción).",
        "Condición de rechazo (CR): valor crítico (x̄c, S²c, r_c) y zona de rechazo.",
        "Regla de decisión (RD) en lenguaje llano y ANTES de calcular: 'se toma una muestra de n..., si x̄ > x̄c se "
        "rechaza H0 → acción; si no → otra acción'.",
        "Cálculos: el ESTIMADOR (x̄, S, r, J, D) contra el valor crítico, nunca contra el valor de H0.",
        "Conclusión: 'se rechaza H0: puedo asegurar que…' o 'no se rechaza H0: no hay evidencia suficiente para asegurar "
        "que…' (NUNCA 'se acepta H0'). α y β como probabilidades (0,05), nunca en %.",
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


# ---------------------------------------------------------------------------
# Sinónimos: otras redacciones (de examen) que se pasan a la palabra que leen las reglas
# ---------------------------------------------------------------------------

# (patrón sobre el texto normalizado, reemplazo). El reemplazo puede usar los grupos del patrón.
SINONIMOS: List[Tuple[str, str]] = [
    # 'chance' = probabilidad
    (r"\bchances?\b", "probabilidad"),
    # 'advertir / percibir' que cambió = detectar
    (r"\badvertir(la|lo)?\b", r"detectar\1"), (r"\badvierta\b", "detecte"), (r"\badviertan\b", "detecten"), (r"\badvierte\b", "detecta"),
    (r"\badvierten\b", "detectan"),
    (r"\badvertiria\b", "detectaría"), (r"\badvertira\b", "detectará"), (r"\bpercibir\b", "detectar"), (r"\bperciba\b", "detecte"),
    # 'parar' la máquina / el proceso / la línea = detener
    (r"\bparar(la|lo|las|los|se)?\b", r"detener\1"), (r"\bpare\b", "detenga"), (r"\bparen\b", "detengan"),
    (r"\bpararia\b", "detendría"), (r"\bparara\b", "detendrá"),
    # 'devolver' el lote = rechazarlo
    (r"\bdevuelve\b", "rechaza"), (r"\bdevuelven\b", "rechazan"), (r"\bdevolver(lo|la)?\b", r"rechazar\1"),
    (r"\bdevolvera\b", "rechazará"), (r"\bdevolveria\b", "rechazaría"),
    # 'descartar' la horneada / el lote = rechazarlo
    (r"\bdescarta\b", "rechaza"), (r"\bdescartan\b", "rechazan"), (r"\bdescartar(lo|la)?\b", r"rechazar\1"),
    (r"\bdescartara\b", "rechazará"), (r"\bdescartaria\b", "rechazaría"),
    # 'quedarse con' un lote / una partida = aceptarlo
    (r"\bquedarse con\b", "aceptar"), (r"\bse queda con\b", "acepta"),
    # 'desviación típica' = desvío estándar; 'significancia' = significación
    (r"\bdesviacion tipica\b", "desviación estándar"), (r"\bdesvio tipico\b", "desvío estándar"),
    (r"\bsignificancia\b", "significación"),
    # 'cociente' entre varianzas / desvíos = relación
    (r"\bcociente\b", "relación"),
]
_RE_MONEDA_ANTES = re.compile(r"(u\$s|u\$d|us\$|usd|\$)\s*(\d[\d.,]*\d|\d)", re.IGNORECASE)


def unificar_redaccion(texto: str) -> str:
    """Pasa sinónimos de examen a la palabra que leen las reglas ('chance' → 'probabilidad', 'parar la máquina' →
    'detener', 'devuelve el lote' → 'rechaza', 'desviación típica' → 'desvío estándar') y deja la moneda después del
    número ('U$S 1.100' → '1.100 U$S', como escribe la guía)."""
    texto = _RE_MONEDA_ANTES.sub(lambda m: f"{m.group(2)} {m.group(1)}", texto)
    for patron, reemplazo in SINONIMOS:
        norm = normalizar(texto)
        partes, ult = [], 0
        for m in re.finditer(patron, norm):
            partes.append(texto[ult:m.start()] + m.expand(reemplazo))
            ult = m.end()
        if partes:
            texto = "".join(partes) + texto[ult:]
    return texto
