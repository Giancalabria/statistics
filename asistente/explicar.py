"""Explicaciones y preguntas con el modelo local, siempre ancladas a lo que calculó el solver y a los apuntes.

El modelo no hace cuentas: recibe los pasos y resultados del solver y los explica / redacta. Después,
`numeros_sin_respaldo` revisa que cada número de la respuesta aparezca en el enunciado o en los resultados
(con el redondeo que tenga); los que no, se muestran como advertencia.
"""

import re
from functools import lru_cache
from typing import Dict, Iterator, List, Optional, Sequence, Tuple

from interprete.modelo import TEMAS, Analisis
from interprete.resolver import Resultado
from interprete.texto import buscar_numeros

from . import cliente, contexto

# fuentes del chat, en orden de autoridad (las reglas del profesor mandan). No va la «Guía Definitiva…» (redaccion):
# contradice al profesor en el factor de finitud.
APUNTES = ("profesor", "control", "convenciones", "teoria", "tutorial", "ejemplo")

# lo que la IA hacía mal al redactar la respuesta para entregar (práctica del 09/11, R1): cambiaba H0, mezclaba la tabla
# de esperados con la amalgamada y borraba avisos. Va en el sistema de «Explicar» y en el pedido del Asistente.
COPIA_FIEL = ("La respuesta para entregar va COMPLETA, con todos los pasos de la resolución en orden (variable, H0 y "
              "H1 con su justificación, α, estadístico y su distribución, CR, RD, cálculos y decisión, conclusión, y la "
              "«Interpretación en términos del problema» con sus unidades si la resolución la tiene), no solo la conclusión. Copia FIEL la resolución: la misma H0 (en bondad de ajuste, «lo observado se "
              "ajusta al modelo X», no «sigue»), la misma decisión y la conclusión del solver sin volverla condicional. "
              "Si hay una tabla antes y otra después de amalgamar, copiá SOLO la amalgamada (la de los aportes y el χ²), "
              "sin agregarle filas. No borres los avisos que cambian la redacción: α elegido (justificalo), N < 60, "
              "ajuste demasiado perfecto.")

SISTEMA_EXPLICAR = f"""Sos un profesor de Estadística Aplicada (UADE, cátedra Dopazo - García) que ayuda a un \
alumno a entender y redactar la resolución de un ejercicio. Respondé en español rioplatense, claro y ordenado.

Reglas estrictas:
- Los NÚMEROS salen únicamente del ENUNCIADO o de la RESOLUCIÓN DEL SOLVER que te paso. No hagas cuentas nuevas \
ni redondees distinto. Si algo no está calculado, decí que hay que calcularlo con la app.
- Seguí las reglas del profesor (Ing. Dopazo), que mandan sobre la guía: H0 justificada en palabras (lo que se \
quiere probar va en H1; pesimista u optimista), pasos del ensayo en orden, comparar el ESTIMADOR con el valor \
crítico (nunca contra el valor de H0 ni con estadísticos t/F/χ² observados), «se rechaza H0: puedo asegurar que…» o \
«no hay evidencia suficiente para asegurar que…» (nunca «acepto H0»), límites redondeados hacia afuera.
- Probabilidades (α, β, 1-β, P) siempre entre 0 y 1, NUNCA en %. Mínimo 4 decimales en el desarrollo.
- Z se justifica porque al estandarizar x̄ se divide por el parámetro σ (una constante); t porque se divide por S, \
una variable aleatoria. Nunca «uso Z porque conozco σ».
- No hay ensayos bilaterales sobre p, σ², σ ni en comparaciones. No se decide con el valor a posteriori α*. \
La estimación de p es siempre exacta (nunca por la normal). Con t no se calculan β ni n.
- Usá coma decimal (2,5) como en el examen.
- {COPIA_FIEL}
"""

SISTEMA_PREGUNTA = """Sos un profesor de Estadística Aplicada (UADE, cátedra Dopazo - García). Respondé las \
preguntas del alumno en español rioplatense, breve y preciso, basándote en los APUNTES que te paso (citá la \
fuente entre corchetes cuando la uses). Si los apuntes no alcanzan, decilo. No inventes valores de tablas \
(z, t, χ², F): para cualquier número concreto indicá que lo calcule con la app. Usá coma decimal.
"""


# ---------------------------------------------------------------------------
# Textos de contexto
# ---------------------------------------------------------------------------

def enunciado_texto(an: Analisis) -> str:
    partes = [an.planteo.strip()]
    partes += [f"{i.letra}) {i.texto}" for i in an.incisos if i.texto and i.letra != "única"]
    return "\n".join(partes)


def resolucion_texto(an: Analisis, resultados: Sequence[Resultado]) -> str:
    """La resolución del solver en texto plano (lo que el modelo puede citar)."""
    bloques = [f"Tema: {TEMAS.get(an.tema, an.tema)}" + (f" · criterio {an.criterio}" if an.criterio else "")]
    for inc, res in zip(an.incisos, resultados):
        b = [f"### {res.titulo}"]
        b += [f"ERROR: {e}" for e in res.errores]
        b += [f"Aviso: {a}" for a in res.avisos]
        b += [f"- {p}" for p in res.pasos]
        if res.tabla:                                  # curvas OC / potencia: sin la tabla el modelo la inventa
            cols = list(res.tabla[0])
            b.append("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols))
            b += ["| " + " | ".join(f"{float(f[c]):.4f}".replace(".", ",") for c in cols) + " |" for f in res.tabla]
        if res.conclusion:
            b.append(f"Conclusión: {res.conclusion}")
        bloques.append("\n".join(b))
    return "\n\n".join(bloques)


# ---------------------------------------------------------------------------
# Verificación de números
# ---------------------------------------------------------------------------

def _valores(texto: str) -> List[Tuple[float, str]]:
    """Números del texto; '1.250' puede ser mil doscientos cincuenta o 1,25 (el modelo a veces usa punto)."""
    salida = []
    for n in buscar_numeros(texto):
        salida.append((n.valor, n.crudo))
        crudo = n.crudo.replace("%", "").strip()
        if "." in crudo and "," not in crudo:
            try:
                salida.append((float(crudo), n.crudo))
            except ValueError:
                pass
        if n.pct:
            salida.append((n.valor / 100, n.crudo))
    return salida


def _decimales(crudo: str) -> int:
    crudo = crudo.replace("%", "").strip()
    sep = "," if "," in crudo else ("." if "." in crudo else None)
    return len(crudo.rsplit(sep, 1)[1]) if sep else 0


@lru_cache(maxsize=1)
def _fractiles() -> Tuple[float, ...]:
    """Fractiles de tabla que una redacción puede citar aunque el solver no los muestre: z y t (gl ≤ 200) para las
    probabilidades usuales, y χ² (gl ≤ 100) en las dos colas. F no: hay demasiadas combinaciones y cualquier número
    terminaría 'respaldado'."""
    from scipy import stats
    probs = (0.8, 0.9, 0.95, 0.975, 0.99, 0.995)
    salida = [float(stats.norm.ppf(q)) for q in probs]
    salida += [float(stats.t.ppf(q, gl)) for q in probs for gl in range(1, 201)]
    salida += [float(stats.chi2.ppf(q, gl)) for q in probs + (0.005, 0.01, 0.025, 0.05, 0.1)
               for gl in range(1, 101)]
    return tuple(salida + [-x for x in salida])


def numeros_sin_respaldo(respuesta: str, fuentes: str) -> List[str]:
    """Números de la respuesta que no aparecen en las fuentes (ni redondeados ni como porcentaje).

    Se ignoran los enteros chicos (pasos, letras, 'dos colas')."""
    conocidos = [v for v, _ in _valores(fuentes)]
    conocidos += [v * 100 for v in conocidos] + [1 - v for v in conocidos if 0 < v < 1]
    # pasos intermedios legítimos de una sola cuenta: cuadrados y raíces (S² ↔ S), α/2 y 1 − α/2, y fractiles de
    # tabla. Son muchos valores, así que solo respaldan números escritos con 3 decimales o más (un "7,9" casaría
    # con cualquiera)
    derivados = [v * v for v in conocidos if abs(v) < 1e4] + [v ** 0.5 for v in conocidos if v > 0]
    derivados += [v / 2 for v in conocidos if 0 < v < 0.5] + [1 - v / 2 for v in conocidos if 0 < v < 0.5]
    derivados += _fractiles()
    dudosos = []
    for n in buscar_numeros(respuesta):
        if n.es_entero and abs(n.valor) <= 10 and not n.pct:
            continue
        candidatos = [n.valor] + ([n.valor / 100] if n.pct else [])
        crudo = n.crudo.replace("%", "").strip()
        if "." in crudo and "," not in crudo:
            try:
                candidatos.append(float(crudo))
            except ValueError:
                pass
        tol = 0.5 * 10 ** -_decimales(n.crudo) + 1e-9
        base = conocidos + (derivados if _decimales(n.crudo) >= 3 else [])
        if not any(abs(c - k) <= max(tol, abs(k) * 1e-9) for c in candidatos for k in base):
            dudosos.append(n.crudo.strip())
    return list(dict.fromkeys(dudosos))


# ---------------------------------------------------------------------------
# Pedidos al modelo
# ---------------------------------------------------------------------------

def mensajes_explicar(an: Analisis, resultados: Sequence[Resultado], pedido: str = "") -> List[Dict[str, str]]:
    enunciado = enunciado_texto(an)
    resolucion = resolucion_texto(an, resultados)
    pedido = pedido.strip() or ("Explicá la resolución inciso por inciso: por qué se eligió ese camino "
                                "(distribución, hipótesis, cola) y después escribí la respuesta como la pondría "
                                "en el examen.")
    # solo lo del tema del ejercicio (prompts cortos y precisos rinden más con el modelo local)
    usuario = (f"REGLAS DEL PROFESOR (mandan sobre todo lo demás):\n{contexto.reglas_profesor(an.tema)}\n\n"
               f"CONVENCIONES DE LA APP:\n{contexto.convenciones()}\n\n"
               f"ENUNCIADO:\n{enunciado}\n\nRESOLUCIÓN DEL SOLVER (números verificados):\n{resolucion}\n\n"
               f"PEDIDO: {pedido}")
    return [{"role": "system", "content": SISTEMA_EXPLICAR}, {"role": "user", "content": usuario}]


def explicar(an: Analisis, resultados: Sequence[Resultado], pedido: str = "", modelo: Optional[str] = None,
             pensar: bool = False) -> Tuple[Iterator[str], str]:
    """(trozos de la explicación, texto de las fuentes para verificar los números al terminar)."""
    fuentes = enunciado_texto(an) + "\n" + resolucion_texto(an, resultados)
    trozos = cliente.chat(mensajes_explicar(an, resultados, pedido), modelo=modelo, stream=True, pensar=pensar,
                          temperatura=0.3)
    return trozos, fuentes



SISTEMA_LIBRE = """Sos un asistente experto en Estadística Aplicada (UADE, cátedra Dopazo - García) que charla \
libremente con el alumno: dudas, planteos, redacción, revisar lo que escribió, o resolver ejercicios completos. \
Respondé en español rioplatense y usá coma decimal. Si te paso una RESOLUCIÓN DE LA APP, sus números están \
verificados: usalos tal cual y no los recalcules. Si hacés alguna cuenta por tu cuenta, mostrala paso a paso y \
avisá que conviene verificarla con la app (los valores de tablas z, t, χ², F sacalos de la app, no de memoria)."""

MAX_ADJUNTOS = 24000


def mensajes_pregunta(pregunta: str, historial: Sequence[Dict[str, str]] = (), ejercicio: str = "",
                      sistema: Optional[str] = None, apuntes: bool = True,
                      adjuntos: str = "") -> Tuple[List[Dict[str, str]], List[contexto.Fragmento]]:
    """Mensajes del chat. `sistema`: instrucciones (por defecto las de preguntas con apuntes); `apuntes`: buscar
    en los .md del repo; `ejercicio`: una resolución de la app; `adjuntos`: texto que pegó / subió el alumno."""
    frags: List[contexto.Fragmento] = []
    sistema = sistema if sistema is not None else SISTEMA_PREGUNTA
    if apuntes:
        consulta = pregunta + " " + " ".join(m["content"] for m in list(historial)[-2:] if m["role"] == "user")
        frags = contexto.buscar(consulta, k=3, fuentes=APUNTES) + contexto.buscar(consulta, k=2, fuentes=("guia",))
        sistema += f"\n\nAPUNTES (citá la fuente entre corchetes si los usás):\n{contexto.como_texto(frags, 8000)}"
    if adjuntos.strip():
        sistema += f"\n\nMATERIAL QUE TE PASÓ EL ALUMNO:\n{adjuntos[:MAX_ADJUNTOS]}"
    if ejercicio:
        sistema += f"\n\nEJERCICIO RESUELTO POR LA APP (números verificados):\n{ejercicio}"
    msgs = [{"role": "system", "content": sistema}] + list(historial)[-10:] + [{"role": "user", "content": pregunta}]
    return msgs, frags


def responder(pregunta: str, historial: Sequence[Dict[str, str]] = (), ejercicio: str = "",
              modelo: Optional[str] = None, pensar: bool = False, sistema: Optional[str] = None,
              apuntes: bool = True, adjuntos: str = "") -> Tuple[Iterator[str], List[contexto.Fragmento]]:
    msgs, frags = mensajes_pregunta(pregunta, historial, ejercicio, sistema, apuntes, adjuntos)
    return cliente.chat(msgs, modelo=modelo, stream=True, pensar=pensar, temperatura=0.4), frags


def resolver_enunciado(texto: str, modelo: Optional[str] = None, pensar: bool = False):
    """Un enunciado pegado en el chat -> (interpretación, resultados, texto de la resolución): reglas + IA + solver."""
    from interprete.resolver import resolver
    from .interpretar import interpretar
    r = interpretar(texto, modelo=modelo, pensar=pensar)
    resultados = resolver(r.analisis)
    texto_res = ("ENUNCIADO:\n" + enunciado_texto(r.analisis) + "\n\nRESOLUCIÓN:\n"
                 + resolucion_texto(r.analisis, resultados))
    return r, resultados, texto_res


# Lo que el alumno le pide a la IA (una pregunta, que revise lo suyo), aunque traiga números de un ejercicio
_RE_PEDIDO = re.compile(
    r"^\W*(por ?que|porque|explica|explicame|que (es|significa|diferencia)|como (se|hago|planteo|redacto|justifico)|"
    r"cuando (se|uso|conviene)|cual(es)? es la diferencia|revisa|revisame|corregi|corregime|controla|mira|fijate|"
    r"te paso|esta bien|estaria bien|me (podes|explicas|ayudas)|ayudame|hola|necesito|quiero|dame|deci)\b|"
    r"\b(mi (respuesta|resolucion|conclusion|redaccion|planteo)|lo que escribi|como lo entregaria)\b")
# en cualquier parte del mensaje: el alumno le habla a la IA (voseo, «sin la app»), aunque haya pegado un enunciado
_RE_PEDIDO_EN_MEDIO = re.compile(
    r"\b(escribi|escribime|deci|decime|explicame|revisame|corregi|corregime|fijate|mandame|"
    r"respondeme|contestame|ayudame|sin hacer cuentas|sin la app|mi (respuesta|resolucion|planteo|conclusion))\b")
_RE_INCISO = re.compile(r"(^|\n)\s*([a-hA-H]|[ivx]{1,4})\s*[).-]\s+\S")


def parece_enunciado(texto: str) -> bool:
    """¿El mensaje del chat es un enunciado para resolver (y no una pregunta para la IA)? Un enunciado narra un
    problema con varios datos numéricos y trae incisos o una tabla, o es largo; un pedido ('explicame…', 'revisá mi
    respuesta…') nunca se resuelve aunque traiga números."""
    from interprete.tablas import buscar_tablas
    from interprete.texto import buscar_numeros, normalizar
    t = (texto or "").strip()
    norm = normalizar(t[:400])
    if len(t) < 60 or _RE_PEDIDO.search(norm) or _RE_PEDIDO_EN_MEDIO.search(normalizar(t)):
        return False
    numeros = [n for n in buscar_numeros(t) if not (n.es_entero and n.valor <= 3 and not n.pct)]
    if len(numeros) < 2:
        return False
    # consigna corta de la guía: 'Calcular los límites de confianza del 90%… si se tomó una muestra de 10 unidades'
    consigna = re.search(r"\b(calcular|estimar|determinar|hallar|ensayar|indicar|disenar|para el plan|se tomo|se tomaron|"
                         r"de un proceso|una muestra de)\b", norm)
    return bool(_RE_INCISO.search(t)) or bool(buscar_tablas(t)) or len(t) >= 250 or bool(consigna)


MARCAS_CONSENSO = {"consenso": "✅ consenso", "ia_vs_reglas": "⚠️ las 2 IA contra las reglas — controlalo",
                   "sin_consenso": "⚠️ sin consenso — controlalo",
                   "una_sola": "☝️ una sola lectura — controlalo", "ninguna": "— nadie lo resolvió"}


def resolver_por_consenso(texto: str, modelo: Optional[str] = None):
    """Un enunciado pegado en el chat, resuelto como en «Interpretar un enunciado» con el modo recomendado (reglas +
    2 lecturas de IA, se vota). -> (análisis, resultados, texto de la resolución, filas [(letra, marca, resumen)])."""
    from interprete.analizador import analizar, separar_incisos
    from interprete.resolver import resolver
    from interprete.tablas import buscar_tablas
    from .consenso import NOMBRES, combinado, consenso
    planteo, incs = separar_incisos(texto, parrafos=True)
    incisos = [tx for _, tx in incs] or None
    tablas = buscar_tablas(texto)[:1] or None
    c = consenso(planteo, incisos, tablas=tablas, modelo=modelo)
    an = combinado(c) or analizar(planteo, incisos, tablas=tablas)
    resultados = resolver(an)
    filas = [(i.letra, MARCAS_CONSENSO[i.estado] + (f" ({NOMBRES[i.elegido.fuente]})" if i.elegido and i.estado != "consenso" else ""),
              i.elegido.resultado.resumen if i.elegido else "") for i in c.incisos]
    texto_res = ("ENUNCIADO:\n" + enunciado_texto(an) + "\n\nRESOLUCIÓN:\n" + resolucion_texto(an, resultados)
                 + "\n\nCONSENSO POR INCISO:\n" + "\n".join(f"{l}) {m}" for l, m, _ in filas))
    return an, resultados, texto_res, filas


def leer_adjunto(nombre: str, datos: bytes) -> str:
    """Texto de un archivo subido (.txt, .md, .csv, .json o .pdf si está pypdf)."""
    if nombre.lower().endswith(".pdf"):
        try:
            import io
            from pypdf import PdfReader
        except ImportError:
            return f"[{nombre}: para leer PDF instalá pypdf]"
        return "\n".join(pag.extract_text() or "" for pag in PdfReader(io.BytesIO(datos)).pages)
    return datos.decode("utf-8", errors="replace")
