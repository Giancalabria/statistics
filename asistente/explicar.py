"""Explicaciones y preguntas con el modelo local, siempre ancladas a lo que calculó el solver y a los apuntes.

El modelo no hace cuentas: recibe los pasos y resultados del solver y los explica / redacta. Después,
`numeros_sin_respaldo` revisa que cada número de la respuesta aparezca en el enunciado o en los resultados
(con el redondeo que tenga); los que no, se muestran como advertencia.
"""

from typing import Dict, Iterator, List, Optional, Sequence, Tuple

from interprete.modelo import TEMAS, Analisis
from interprete.resolver import Resultado
from interprete.texto import buscar_numeros

from . import cliente, contexto

APUNTES = ("convenciones", "redaccion", "teoria", "tutorial", "ejemplo")

SISTEMA_EXPLICAR = """Sos un profesor de Estadística Aplicada (UADE, cátedra Dopazo - García) que ayuda a un \
alumno a entender y redactar la resolución de un ejercicio. Respondé en español rioplatense, claro y ordenado.

Reglas estrictas:
- Los NÚMEROS salen únicamente del ENUNCIADO o de la RESOLUCIÓN DEL SOLVER que te paso. No hagas cuentas nuevas \
ni redondees distinto. Si algo no está calculado, decí que hay que calcularlo con la app.
- Seguí las convenciones de la cátedra (planteo de H0 con criterio optimista/pesimista, 7 pasos del ensayo, \
conclusión formal con el nivel de significación, límites redondeados hacia afuera).
- Usá coma decimal (2,5) como en el examen.
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


def numeros_sin_respaldo(respuesta: str, fuentes: str) -> List[str]:
    """Números de la respuesta que no aparecen en las fuentes (ni redondeados ni como porcentaje).

    Se ignoran los enteros chicos (pasos, letras, 'dos colas')."""
    conocidos = [v for v, _ in _valores(fuentes)]
    conocidos += [v * 100 for v in conocidos] + [1 - v for v in conocidos if 0 < v < 1]
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
        if not any(abs(c - k) <= max(tol, abs(k) * 1e-9) for c in candidatos for k in conocidos):
            dudosos.append(n.crudo.strip())
    return list(dict.fromkeys(dudosos))


# ---------------------------------------------------------------------------
# Pedidos al modelo
# ---------------------------------------------------------------------------

def mensajes_explicar(an: Analisis, resultados: Sequence[Resultado], pedido: str = "") -> List[Dict[str, str]]:
    enunciado = enunciado_texto(an)
    resolucion = resolucion_texto(an, resultados)
    apuntes = contexto.buscar(f"{TEMAS.get(an.tema, '')} {enunciado}", k=3, fuentes=("redaccion", "teoria"))
    pedido = pedido.strip() or ("Explicá la resolución inciso por inciso: por qué se eligió ese camino "
                                "(distribución, hipótesis, cola) y después escribí la respuesta como la pondría "
                                "en el examen.")
    usuario = (f"CONVENCIONES DE LA CÁTEDRA:\n{contexto.convenciones()}\n\n"
               f"APUNTES RELACIONADOS:\n{contexto.como_texto(apuntes, 5000)}\n\n"
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
