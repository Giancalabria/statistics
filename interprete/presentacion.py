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
         "proporcion": ("p", "la proporción poblacional")}
REF = {"media": "mu0", "varianza": "sigma0", "proporcion": "p0"}
ALT = {"media": "mu1", "varianza": "sigma1", "proporcion": "p1"}
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
           f"el factor √((N-n)/(N-1)).") if finita else ""
    if d.get("sigma_conocido"):
        lineas = ["La variable X se supone Normal: X ~ N(μ; σ²) con σ conocido (si no fuera Normal, con n grande vale "
                  "el Teorema Central del Límite).",
                  "Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n)." + fpc,
                  "Se estandariza con Z = (x̄ - μ)/(σ/√n) ~ N(0; 1) y se usan los fractiles de la Normal estándar."]
    else:
        lineas = ["La variable X se supone Normal: X ~ N(μ; σ²), con σ DESCONOCIDO.",
                  "Al estimar σ con el desvío muestral S, el estadístico t = (x̄ - μ)/(S/√n) sigue una t de Student con "
                  "ν = n - 1 grados de libertad (más \"ancha\" que la Normal por la incertidumbre de S)." + fpc]
    if tipo in ("beta", "curva", "diseno"):
        lineas.append("Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: "
                      "β = P(x̄ en la zona de no rechazo | μ = μ₁).")
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
        lineas.append("Para el n se usa la aproximación Normal: p̂ ~ N(p; p(1-p)/n), válida con n grande.")
    else:
        lineas.append("El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero).")
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
        lineas = ["Las dos poblaciones se suponen Normales e independientes.",
                  "El cociente (S₁²/σ₁²)/(S₂²/σ₂²) sigue una F de Snedecor con (n₁-1; n₂-1) grados de libertad."]
    elif tema == "dos_medias":
        lineas = ["Las poblaciones se suponen Normales. Si las muestras son apareadas se trabaja con las diferencias "
                  "dᵢ (una sola muestra, t con ν = n-1).",
                  "Si son independientes, primero un test F decide si las varianzas pueden considerarse iguales: si sí, "
                  "t con S combinado (ν = n₁ + n₂ - 2); si no, t de Welch (ν aproximado)."]
    elif tema == "chi_contingencia":
        lineas = ["Con las frecuencias esperadas Fe = (total fila · total columna)/total, el estadístico "
                  "Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = (filas - 1)(columnas - 1).",
                  "La aproximación exige Fe ≥ 5 en cada celda (si no, se agrupan categorías)."]
    elif tema == "chi_ajuste":
        lineas = ["El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = k - 1 - (parámetros estimados).",
                  "La aproximación exige Fe ≥ 5 en cada clase (si no, se agrupan clases)."]
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
