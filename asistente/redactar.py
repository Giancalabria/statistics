"""Redactar la resolución completa como la quiere la cátedra, a partir de lo que calculó el solver.

    from asistente.redactar import redactar, controlar
    trozos, fuentes = redactar(analisis, resultados)      # streaming
    texto = "".join(trozos)
    controles = controlar(texto, analisis, fuentes)       # checklist de ESTILO_CATEDRA.md, sin IA

El estilo sale de ESTILO_CATEDRA.md (editable: ejemplos, frases que exige el profesor). La IA solo redacta: los
números son los del solver, y `controlar` marca cualquier número que no salga del enunciado ni de la resolución.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Optional, Sequence, Tuple

from interprete.modelo import TIPOS, Analisis
from interprete.resolver import Resultado

from . import cliente
from .explicar import enunciado_texto, numeros_sin_respaldo, resolucion_texto

ESTILO = Path(__file__).resolve().parent.parent / "ESTILO_CATEDRA.md"

SISTEMA = """Sos un alumno excelente de Estadística Aplicada (UADE, cátedra Dopazo - García) que escribe la \
resolución de un ejercicio de examen EXACTAMENTE con el estilo que pide el profesor, descripto abajo con ejemplos.

Reglas estrictas:
- Todos los NÚMEROS (fractiles, valores críticos, límites, n, probabilidades, estadísticos) salen de la \
RESOLUCIÓN DEL SOLVER o del ENUNCIADO, copiados tal cual. No hagas cuentas nuevas ni redondees distinto. Si un \
número que el formato pide no está en la resolución, no lo inventes: omitilo.
- Seguí el formato del estilo para cada tipo de inciso: definir la variable con su unidad, los 7 pasos en los \
ensayos (con CR y RD en lenguaje llano), la expresión formal P(A ≤ θ ≤ B) = 1 − α en los intervalos, n al \
entero superior con Δn si ya había muestra.
- Si el formato pide un paso intermedio (un fractil, un grado de libertad) que la resolución NO trae, no lo \
escribas: los ejemplos del estilo son para la forma, nunca copies sus números.
- En un DISEÑO del ensayo todavía no hay muestra: llegá hasta la condición de rechazo y la regla de decisión \
(pasos 1 a 5); no inventes un estimador ni una conclusión.
- Si un inciso usa lo de otro (la región crítica del a), la muestra del a)), no repitas la definición ni las \
hipótesis: remití a ese inciso.
- Lo que el solver no da (la definición de la variable, la justificación del criterio, la regla de decisión para \
el operario, las conclusiones en palabras) lo redactás vos, con el contexto del enunciado.
- Los límites de los intervalos van redondeados HACIA AFUERA, exactamente como los informa el solver (inferior \
hacia abajo, superior hacia arriba): copiá esos valores, no los vuelvas a redondear.
- Nunca escribas «acepto H0»: «se rechaza H0» o «no se rechaza H0».
- Español rioplatense, coma decimal (2,5), unidades del enunciado. Un título por inciso: «### a) …».

ESTILO DE LA CÁTEDRA:
"""


def estilo() -> str:
    try:
        return ESTILO.read_text(encoding="utf-8")
    except OSError:
        return ""


def mensajes(an: Analisis, resultados: Sequence[Resultado], pedido: str = ""):
    usuario = (f"ENUNCIADO:\n{enunciado_texto(an)}\n\nRESOLUCIÓN DEL SOLVER (números verificados):\n"
               f"{resolucion_texto(an, resultados)}\n\n"
               + (f"PEDIDO: {pedido.strip()}" if pedido.strip() else
                  "PEDIDO: escribí la resolución completa de todos los incisos, como en el examen."))
    return [{"role": "system", "content": SISTEMA + estilo()}, {"role": "user", "content": usuario}]


def redactar(an: Analisis, resultados: Sequence[Resultado], pedido: str = "", modelo: Optional[str] = None,
             pensar: bool = False) -> Tuple[Iterator[str], str]:
    """(trozos de la redacción, fuentes para verificar los números)."""
    fuentes = enunciado_texto(an) + "\n" + resolucion_texto(an, resultados)
    trozos = cliente.chat(mensajes(an, resultados, pedido), modelo=modelo, stream=True, pensar=pensar,
                          temperatura=0.2)
    return trozos, fuentes


def corregir(an: Analisis, resultados: Sequence[Resultado], texto: str, problemas: Sequence[str], pedido: str = "",
             modelo: Optional[str] = None, pensar: bool = False) -> Iterator[str]:
    """Segunda vuelta: se le devuelve lo que falló del checklist para que reescriba la resolución."""
    msgs = mensajes(an, resultados, pedido) + [
        {"role": "assistant", "content": texto},
        {"role": "user", "content": "Tu redacción no cumple estos puntos del checklist de la cátedra:\n"
                                    + "\n".join(f"- {p}" for p in problemas)
                                    + "\nReescribí la resolución completa corrigiéndolos. Usá solo los números de "
                                      "la resolución del solver (si un paso necesitaba uno que no está, omitilo) y "
                                      "los límites exactamente como los informa el solver."}]
    return cliente.chat(msgs, modelo=modelo, stream=True, pensar=pensar, temperatura=0.1)


def problemas(controles: Sequence["Control"]) -> List[str]:
    return [c.texto for c in controles if not c.ok]


# ---------------------------------------------------------------------------
# Checklist (sin IA)
# ---------------------------------------------------------------------------

@dataclass
class Control:
    ok: bool
    texto: str


ENSAYOS = {"ensayo", "diseno", "ensayo_coef", "validacion"}
INTERVALOS = {"ic", "ic_coef", "ic_rho", "ic_rho2", "pronostico"}

_ACEPTO = re.compile(r"\bacept(o|a|amos|ar|e|ando)\s+(la\s+(hip[oó]tesis\s+(nula\s+)?)?)?(h0|h₀|hip[oó]tesis nula)",
                     re.IGNORECASE)
_FORMAL = re.compile(r"P\s*\(\s*[^()]*?(≤|<=)[^()]*?(≤|<=)[^()]*?\)\s*=", re.IGNORECASE)


def _secciones(texto: str) -> dict:
    """letra -> texto de su sección («### a) ...»)."""
    partes = re.split(r"(?m)^#{2,4}\s*(?:inciso\s+)?(única|[a-h](?:\.[a-h])?)\)", texto, flags=re.IGNORECASE)
    secciones = {}
    for k in range(1, len(partes) - 1, 2):
        secciones[partes[k].lower()] = secciones.get(partes[k].lower(), "") + partes[k + 1]
    return secciones


def _limites(res: Resultado) -> List[str]:
    """Límites de un intervalo tal como los informa el solver (redondeados hacia afuera): '[0,5387 ; 0,9002]'."""
    return re.findall(r"-?\d[\d.]*,\d+", " ".join(re.findall(r"\[([^\]]+)\]", res.resumen or "")))


def controlar(texto: str, an: Analisis, fuentes: str, resultados: Sequence[Resultado] = ()) -> List[Control]:
    out: List[Control] = []
    secciones = _secciones(texto)
    if len(an.incisos) == 1 and an.incisos[0].letra.lower() not in secciones:
        secciones[an.incisos[0].letra.lower()] = texto          # un solo inciso: no hace falta el título
    out.append(Control(bool(re.search(r"\b[XYD](?:[₁₂12])?\s*:|definici[oó]n de (la )?variable", texto,
                                      re.IGNORECASE)), "Define la variable en palabras (X: …)"))
    if _ACEPTO.search(texto):
        out.append(Control(False, f"Dice «{_ACEPTO.search(texto).group(0)}»: tiene que ser «no se rechaza H0»"))
    for inc in an.incisos:
        sec = secciones.get(inc.letra.lower(), "")
        nombre = f"{inc.letra}) {TIPOS.get(inc.tipo, inc.tipo)}"
        if not sec:
            if inc.tipo != "no_soportado":
                out.append(Control(False, f"{nombre}: no encontré su sección («### {inc.letra}) …»)"))
            continue
        if inc.tipo in INTERVALOS:
            out.append(Control(bool(_FORMAL.search(sec)), f"{nombre}: expresión formal P(A ≤ θ ≤ B) = 1 − α"))
            res = resultados[an.incisos.index(inc)] if len(resultados) == len(an.incisos) else None
            limites = _limites(res) if res is not None else []
            if limites:
                faltan = [x for x in limites if not re.search(r"(?<![\d,.])" + re.escape(x) + r"(?![\d])", sec)]
                out.append(Control(not faltan, f"{nombre}: límites redondeados hacia afuera como el solver "
                                               f"({' ; '.join(limites)})" + (f" — faltan {', '.join(faltan)}"
                                                                             if faltan else "")))
        if inc.tipo in ENSAYOS:
            hay_cr = bool(re.search(r"\bCR\b|condici[oó]n de rechazo", sec, re.IGNORECASE))
            hay_rd = bool(re.search(r"\bRD\b|regla de decisi[oó]n", sec, re.IGNORECASE))
            out.append(Control(hay_cr and hay_rd, f"{nombre}: condición de rechazo y regla de decisión"))
            out.append(Control(bool(re.search(r"H0|H₀", sec)) and bool(re.search(r"H1|H₁", sec)),
                               f"{nombre}: H0 y H1"))
            if inc.tipo == "ensayo":
                out.append(Control(bool(re.search(r"(no\s+)?se\s+rechaza", sec, re.IGNORECASE)),
                                   f"{nombre}: conclusión con «se rechaza / no se rechaza H0»"))
    dudosos = numeros_sin_respaldo(texto, fuentes)
    out.append(Control(not dudosos, "Todos los números salen del enunciado o del solver" if not dudosos else
                       "Números que no salen del enunciado ni del solver: " + ", ".join(dudosos)))
    return out
