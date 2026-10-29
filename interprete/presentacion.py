"""Textos de presentación que pide el examen en cada problema:

    a) Justificar las hipótesis planteadas.
    b) Explicar el uso de las distribuciones o modelos estadísticos empleados.

Son plantillas por reglas (tema, tipo de inciso, criterio, cola, σ conocido,
población finita, sistema de control): sirven de guía para redactar, no
reemplazan leer el problema. Se arman con los datos efectivos del inciso.
"""

import re
from typing import Dict, List, Optional

from .texto import fmt

PARAM = {"media": ("μ", "la media poblacional"), "varianza": ("σ", "el desvío poblacional"),
         "proporcion": ("p", "la proporción poblacional"), "dos_varianzas": ("φ", "la relación de desvíos σ₁/σ₂")}
REF = {"media": "mu0", "varianza": "sigma0", "proporcion": "p0", "dos_varianzas": "phi0"}
ALT = {"media": "mu1", "varianza": "sigma1", "proporcion": "p1", "dos_varianzas": "phi1"}
SIGNO = {"derecha": ">", "izquierda": "<", "bilateral": "≠"}
OPUESTO = {"derecha": "≤", "izquierda": "≥", "bilateral": "="}


def _v(x) -> str:
    return fmt(x, 4) if isinstance(x, (int, float)) else str(x)


# ---------------------------------------------------------------------------
# a) Justificación de H0
# ---------------------------------------------------------------------------

def justificar_h0(tema: str, tipo: str, d: Dict, criterio: Optional[str], tail: Optional[str]) -> Optional[str]:
    if tema not in PARAM or tipo not in ("ensayo", "diseno") or tail not in SIGNO:
        return None
    sim, nombre = PARAM[tema]
    ref = d.get(REF[tema])
    if tema == "varianza" and ref is None:
        ref = d.get("sigma0")
    if tema == "dos_varianzas":
        ref = ref or 1.0
        a, b = d.get("nombre1") or "1", d.get("nombre2") or "2"
        sim = f"φ = σ({a})/σ({b})"
    if tema == "proporcion" and isinstance(ref, float):
        from solver.hypothesis_one import p_txt
        v0 = p_txt(ref).replace(".", ",")   # los periódicos como fracción (1/37), no truncados
    else:
        v0 = _v(ref) if ref is not None else f"{sim}₀"
    h0 = f"H0: {sim} {OPUESTO[tail]} {v0}"
    h1 = f"H1: {sim} {SIGNO[tail]} {v0}"
    if d.get("ambos") and d.get("mu0") is not None and d.get("sigma0") is not None:
        m0, s0 = _v(d["mu0"]), _v(d["sigma0"])
        h0 = f"H0: μ {OPUESTO[tail]} {m0} y σ {OPUESTO[tail]} {s0}"
        h1 = f"H1: μ {SIGNO[tail]} {m0} y σ {SIGNO[tail]} {s0}"
    lineas: List[str] = []
    if d.get("control"):
        si, no = d.get("accion_rechazo", "se detiene el proceso"), d.get("accion_no_rechazo", "el proceso sigue")
        lineas.append(f"Es un **sistema de control**: la decisión es entre dos acciones. Rechazar H0 ⇒ {si}; "
                      f"no rechazarla ⇒ {no}.")
    if criterio == "pesimista":
        lineas.append(f"**Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). {h0} supone "
                      f"lo desfavorable y solo se la rechaza con evidencia fuerte; {h1} es la situación favorable que "
                      f"habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.")
    elif criterio == "optimista":
        lineas.append(f"**Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). "
                      f"{h0} supone que cumple; {h1} es el incumplimiento que se quiere detectar. Se lo da por bueno "
                      f"salvo evidencia en contra.")
    else:
        lineas.append(f"{h1} recoge lo que el enunciado quiere probar; {h0} es el complemento y lleva la igualdad "
                      f"(el valor de referencia {v0}).")
    alpha, beta = d.get("alpha"), d.get("beta")
    alt = d.get(ALT[tema])
    if d.get("control") and alpha is not None:
        si, no = d.get("accion_rechazo", "se detiene el proceso"), d.get("accion_no_rechazo", "el proceso sigue")
        txt = f"α = P(error de tipo I) = P({si} | {sim} = {v0}) = {_v(alpha)}"
        if beta is not None and alt is not None:
            txt += f"; β = P(error de tipo II) = P({no} | {sim} = {_v(alt)}) = {_v(beta)}"
        lineas.append(txt + ".")
    elif alpha is not None:
        txt = f"α = P(rechazar H0 | H0 cierta) = {_v(alpha)} (error de tipo I)"
        if beta is not None and alt is not None and tipo == "diseno":
            txt += f"; β = P(no rechazar H0 | {sim} = {_v(alt)}) = {_v(beta)} (error de tipo II)"
        lineas.append(txt + ".")
    cola = {"derecha": "unilateral a la derecha", "izquierda": "unilateral a la izquierda",
            "bilateral": "bilateral (sin dirección)"}[tail]
    lineas.append(f"El ensayo es {cola}: la zona de rechazo está donde apunta H1.")
    return "**Justificación de H0**:  \n" + "  \n".join("• " + x for x in lineas)


# ---------------------------------------------------------------------------
# b) Distribuciones / modelos empleados
# ---------------------------------------------------------------------------

def _modelo_media(d: Dict, tipo: str) -> List[str]:
    finita = d.get("N")
    fpc = (f" Como la población es finita (N = {_v(finita)}) y se muestrea sin reposición, el error estándar lleva "
           f"el factor de corrección por finitud √((N-n)/N) (algunos autores usan N − 1: «el uno mucho no "
           f"hace»).") if finita else ""
    if d.get("sigma_conocido"):
        lineas = ["La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).",
                  "Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n)." + fpc,
                  "Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal "
                  "dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)"]
    else:
        lineas = ["La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).",
                  "Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE "
                  "ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t "
                  "de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)" + fpc]
    if tipo in ("beta", "curva", "diseno"):
        lineas.append("Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: "
                      "β = P(x̄ en la zona de no rechazo | μ = μ₁)." if d.get("sigma_conocido", True) else
                      "Con σ desconocido la cátedra no calcula β ni n (hace falta la t no central).")
    if tipo == "n":
        lineas.append("El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n" +
                      (" (con t se itera porque ν depende de n)." if not d.get("sigma_conocido") else "."))
    return lineas


def _modelo_varianza(d: Dict, tipo: str) -> List[str]:
    lineas = ["La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto "
              "si X no es Normal).",
              "Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo "
              "no es simétrico y en un ensayo bilateral hay dos valores críticos distintos."]
    if tipo in ("beta", "diseno"):
        lineas.append("Para β / potencia se usa que (n-1)·S²/σ₁² ~ χ²(n-1) cuando el desvío verdadero es σ₁.")
    if tipo == "n":
        lineas.append("El n sale de la relación entre límites R' = B'/A' (Ecuación de García para aproximar ν).")
    return lineas


def _modelo_proporcion(d: Dict, tipo: str) -> List[str]:
    lineas = ["Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.",
              "La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p)."]
    if tipo == "ic":
        lineas.append("El intervalo exacto usa la relación entre la Binomial y la distribución Beta (o F de Snedecor).")
    elif tipo == "n":
        lineas.append("Para el n se usa la aproximación Normal: p̂ ~ N(p; p(1-p)/n). La aproximación se justifica con el n "
                      "RESULTANTE: normal si n·p > 10 y n·(1-p) > 10; Poisson si p ≤ 0,005; si se cumplen las dos o "
                      "ninguna, criterio de Mermoz (n₀ = 0,23·(1-p)²/p³).")
    elif tipo == "diseno":
        lineas.append("El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de "
                      "Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y "
                      "n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).")
    else:
        lineas.append("El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). "
                      "No hay ensayos bilaterales sobre p.")
    return lineas


def explicar_distribuciones(tema: str, tipo: str, d: Dict) -> Optional[str]:
    if tipo == "no_soportado":
        return None
    if d.get("ambos") and tema in ("media", "varianza"):
        lineas = ["**Para la media**: " + " ".join(_modelo_media(dict(d, sigma_conocido=False), tipo)),
                  "**Para el desvío**: " + " ".join(_modelo_varianza(d, tipo))]
    elif tema == "media":
        lineas = _modelo_media(d, tipo)
    elif tema == "varianza":
        lineas = _modelo_varianza(d, tipo)
    elif tema == "proporcion":
        lineas = _modelo_proporcion(d, tipo)
    elif tema == "dos_varianzas":
        lineas = ["Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es "
                  "robusta si X no es Normal).",
                  "Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). "
                  "Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y "
                  "F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁)."]
        if tipo in ("ensayo", "beta", "diseno"):
            lineas.append("En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el "
                          "desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².")
        if tipo in ("beta", "diseno"):
            lineas.append("Para β / potencia se usa que j²/φ₁² ~ F(ν₁; ν₂) cuando la relación verdadera es φ₁.")
        if tipo == "n":
            lineas.append("Con n₁ = n₂ = n la relación entre límites B/A = F(1-α/2; ν; ν)/F(α/2; ν; ν) depende solo de "
                          "n: se itera sobre F hasta cumplirla.")
    elif tema == "dos_medias":
        lineas = ["Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad "
                  "experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).",
                  "Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la "
                  "varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa "
                  "amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).",
                  "En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n."]
    elif tema == "chi_contingencia":
        lineas = ["Con las frecuencias esperadas Fe = (total fila · total columna)/total (con decimales: no se "
                  "redondean), el estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = (filas - 1)(columnas - 1).",
                  "La aproximación exige N ≥ 60 y Fe ≥ 5 en cada celda (si no, se amalgaman categorías)."]
    elif tema == "chi_ajuste":
        lineas = ["El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros "
                  "estimados con la muestra).",
                  "La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene "
                  "un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual."]
    else:
        return None
    return "**Modelos y distribuciones empleados**:  \n" + "  \n".join("• " + x for x in lineas)


# ---------------------------------------------------------------------------
# Los 7 pasos de la cátedra para un ensayo de hipótesis
# ---------------------------------------------------------------------------

# prefijo del paso -> (número de paso al que pertenece, título nuevo o None si se deja)
PASOS_ENSAYO = {
    "**Hipótesis**": (1, "**1 · Planteo de hipótesis**"),
    "**Justificación de H0**": (1.5, None),  # va después del planteo
    "**Distribución**": (3, "**3 · Estadístico de prueba**"),
    "**Modelo**": (3, "**3 · Estadístico de prueba**"),
    "**Estadístico**": (3, "**3 · Estadístico de prueba**"),
    "**Modelos y distribuciones empleados**": (3.5, None),  # después de la línea del estadístico
    "**Población finita**": (3, None),
    "**Frecuencias esperadas**": (3, None),
    "**Condición de rechazo**": (4, "**4 · Condición de rechazo (CR)**"),
    "**Valor crítico**": (4, "**4 · Condición de rechazo (CR)**"),
    "**Decisión**": (6, "**6 · Cálculos y decisión**"),
}


def siete_pasos(pasos: List[str], alpha: float, regla: str = "") -> List[str]:
    """Ordena y numera los pasos de un ensayo como pide la cátedra:
    1 hipótesis, 2 nivel de significación, 3 estadístico, 4 condición de rechazo,
    5 regla de decisión (en lenguaje llano, ANTES de los cálculos), 6 cálculos.
    La 7 (conclusión formal) es `Resultado.conclusion`.

    Los pasos sin prefijo conocido quedan pegados al anterior (paso 0 si están al principio).
    """
    items = []
    actual = 0
    for p in pasos:
        for prefijo, (num, titulo) in PASOS_ENSAYO.items():
            if p.startswith(prefijo):
                actual = num
                if titulo:
                    p = titulo + p[len(prefijo):]
                if num == 1:
                    p = re.sub(r"\s*\(α = [\d.,]+\)", "", p)  # α va en el paso 2
                break
        items.append((actual, p))
    items.append((2, f"**2 · Nivel de significación**: α = {fmt(alpha, 4)} — riesgo máximo de cometer un error de "
                     f"tipo I (rechazar H0 siendo cierta)."))
    if regla:
        items.append((5, f"**5 · Regla de decisión (RD)**: {regla}"))
    items.sort(key=lambda x: x[0])  # estable: dentro de cada paso se mantiene el orden original
    return [p for _, p in items]


def agregar_presentacion(pasos: List[str], tema: str, tipo: str, d: Dict, criterio: Optional[str],
                         tail: Optional[str]) -> List[str]:
    """Inserta la justificación antes de las hipótesis y los modelos después (o al principio si no hay)."""
    pasos = list(pasos)
    just = justificar_h0(tema, tipo, d, criterio, tail)
    dist = explicar_distribuciones(tema, tipo, d)
    i_hip = next((i for i, p in enumerate(pasos) if p.startswith("**Hipótesis**")), None)
    if d.get("ambos"):
        i_hip = None  # dos ensayos: se explica una sola vez arriba
    if i_hip is None:
        inicio = 1 if pasos and pasos[0].startswith("**Procesar la muestra**") else 0
        pasos[inicio:inicio] = [x for x in (just, dist) if x]
    else:
        if dist:
            pasos.insert(i_hip + 1, dist)
        if just:
            pasos.insert(i_hip, just)
    return pasos
