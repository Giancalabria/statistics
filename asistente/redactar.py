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

from interprete.buscador import TEMA_A_GUIA
from interprete.modelo import TEMAS, TIPOS, Analisis
from interprete.resolver import Resultado

from . import cliente
from .explicar import enunciado_texto, numeros_sin_respaldo, resolucion_texto

ESTILO = Path(__file__).resolve().parent.parent / "ESTILO_CATEDRA.md"

SISTEMA = """Redactás la resolución de un ejercicio de examen de Estadística a partir de una RESOLUCIÓN DEL SOLVER \
que ya tiene todas las cuentas hechas y verificadas. Tu trabajo es la redacción: ordenar los pasos como pide el \
FORMATO de abajo y escribir en palabras lo que el solver no dice.

Reglas:
1. Números: todos (fractiles, valores críticos, límites, n, frecuencias, estadísticos) se copian tal cual de la \
RESOLUCIÓN DEL SOLVER o del ENUNCIADO. No hagas cuentas nuevas ni redondees distinto. Si el formato pide un número \
que la resolución no trae, omitilo. Los números de los ejemplos del formato son de OTROS ejercicios: nunca los copies.
2. Tablas: si la resolución del solver trae una tabla, copiala completa en el paso de cálculos.
3. Incisos: respetá exactamente los incisos que indica DATOS DEL EJERCICIO. No agregues incisos ni subdividas la \
resolución en a), b), c) si el ejercicio tiene una sola consigna.
4. Pasos: numerá los pasos como el FORMATO (la numeración de la resolución del solver es interna, no la uses).
5. Lo que redactás vos, con el contexto del enunciado: la definición de la variable, las hipótesis en palabras, la \
regla de decisión para quien toma la decisión y la conclusión. La conclusión del solver es genérica: reescribila \
diciendo qué significa para el problema concreto (qué se puede o no se puede asegurar).
6. Criterio pesimista / optimista: solo si DATOS DEL EJERCICIO dice que corresponde. Si dice «no corresponde», no \
lo menciones.
7. Nunca escribas «acepto H0» ni des H0 por probada: «se rechaza H0» o «no se rechaza H0 (no hay evidencia \
suficiente para asegurar que…)».
8. Intervalos: límites exactamente como los informa el solver (ya están redondeados hacia afuera) y expresión formal \
P(A ≤ θ ≤ B) = 1 − α.
9. Español rioplatense, coma decimal (2,5), unidades del enunciado. Sin introducción ni comentarios finales: solo \
la resolución.
10. El FORMATO de abajo es material de referencia: describe cómo tiene que quedar la resolución y trae ejemplos de \
OTROS ejercicios. No lo copies, no repitas sus títulos, sus reglas ni sus ejemplos: escribí solo la resolución de \
este ejercicio.

FORMATO DE LA RESOLUCIÓN (referencia, no copiar):
"""

_TEMA_ROMANO = dict(TEMA_A_GUIA, regresion_multiple="VIII")
_RE_TEMAS = re.compile(r"<!--\s*temas:\s*([IVX ]+?)\s*-->")


def estilo() -> str:
    try:
        return ESTILO.read_text(encoding="utf-8")
    except OSError:
        return ""


def estilo_para(tema: Optional[str]) -> str:
    """ESTILO_CATEDRA.md sin el encabezado y sin las secciones (## / ###) marcadas para otros temas."""
    texto = estilo()
    if "\n## " not in texto:
        return texto
    texto = texto[texto.index("\n## ") + 1:]
    romano = _TEMA_ROMANO.get(tema or "")
    partes = re.split(r"(?m)^(?=#{2,3} )", texto)
    salida, saltar_nivel = [], None
    for parte in partes:
        nivel = len(parte) - len(parte.lstrip("#"))
        if saltar_nivel is not None and nivel > saltar_nivel:
            continue                      # subsección de una sección que no va
        saltar_nivel = None
        m = _RE_TEMAS.search(parte.split("\n\n", 1)[0])
        if m and romano and romano not in m.group(1).split():
            saltar_nivel = nivel
            continue
        salida.append(re.sub(r"<!--.*?-->\n?", "", parte, flags=re.S).replace("\n\n\n", "\n\n"))
    # una sección ## que quedó sin contenido (todos sus ejemplos eran de otros temas) no se manda, el checklist es
    # para quien revisa (las reglas ya están en el prompt) y los números de sección se sacan: el modelo los copiaba
    limpio = [x for i, x in enumerate(salida)
              if not (x.startswith("## ") and not x.split("\n", 1)[1].strip()
                      and (i + 1 == len(salida) or salida[i + 1].startswith("## ")))
              and "checklist" not in x.split("\n", 1)[0].lower()]
    limpio = [re.sub(r"^(#{2,3}) \d+(?:\.\d+)*\.? ", r"\1 ", x) for x in limpio]
    return "<<<FORMATO\n" + "".join(limpio).strip() + "\nFORMATO>>>\n"


def datos_del_ejercicio(an: Analisis) -> str:
    romano = _TEMA_ROMANO.get(an.tema, "")
    lineas = [f"- Tema: {TEMAS.get(an.tema, an.tema)}" + (f" (Tema {romano} de la guía)" if romano else "") + "."]
    if romano in ("I", "II", "III", "IV", "V"):
        lineas.append(f"- Criterio para plantear H0: {an.criterio} ({an.criterio_razon})." if an.criterio else
                      "- Criterio para plantear H0: el enunciado no lo fija; justificalo con el contexto solo si "
                      "hay un ensayo.")
    else:
        lineas.append("- Criterio pesimista / optimista: no corresponde en este tema (no lo menciones).")
    if len(an.incisos) == 1 and an.incisos[0].letra == "única":
        inc = an.incisos[0]
        lineas.append(f"- Una sola consigna ({TIPOS.get(inc.tipo, inc.tipo)}): no la dividas en incisos. Usá un solo "
                      "título «### Resolución».")
        if inc.que_pide:
            lineas.append(f"- Qué pide: {inc.que_pide}")
    else:
        lineas.append(f"- Incisos ({len(an.incisos)}), uno por título «### letra) …»:")
        lineas += [f"  - {i.letra}) {TIPOS.get(i.tipo, i.tipo)}" + (f": {i.que_pide}" if i.que_pide else "")
                   for i in an.incisos]
    return "\n".join(lineas)


def _sin_numeracion(texto: str) -> str:
    """'**3 · Estadístico de prueba**' → '**Estadístico de prueba**' (la numeración la pone el formato)."""
    return re.sub(r"\*\*\d+(?:[.,]\d+)? · ", "**", texto)


def mensajes(an: Analisis, resultados: Sequence[Resultado], pedido: str = ""):
    primero = "### Resolución" if len(an.incisos) == 1 and an.incisos[0].letra == "única" else \
        f"### {an.incisos[0].letra}) …" if an.incisos else "### Resolución"
    usuario = (f"ENUNCIADO:\n{enunciado_texto(an)}\n\nDATOS DEL EJERCICIO:\n{datos_del_ejercicio(an)}\n\n"
               f"RESOLUCIÓN DEL SOLVER (números verificados):\n{_sin_numeracion(resolucion_texto(an, resultados))}\n\n"
               + (f"PEDIDO: {pedido.strip()}" if pedido.strip() else
                  "PEDIDO: escribí la resolución completa, paso a paso, como en el examen.")
               + f"\nTu respuesta empieza directamente con «{primero}».")
    return [{"role": "system", "content": SISTEMA + estilo_para(an.tema)}, {"role": "user", "content": usuario}]


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
    out.append(Control(bool(re.search(r"\b[XYD](?:[₁₂12])?\s*:|definici[oó]n de (la )?variable|\bvariable\**\s*:", texto,
                                      re.IGNORECASE)), "Define la variable en palabras (X: …)"))
    if _ACEPTO.search(texto):
        out.append(Control(False, f"Dice «{_ACEPTO.search(texto).group(0)}»: tiene que ser «no se rechaza H0»"))
    letras = {i.letra.lower() for i in an.incisos}
    inventados = sorted(k for k in _secciones(texto) if k not in letras)
    out.append(Control(not inventados, "No agrega incisos que el ejercicio no tiene" if not inventados else
                       f"Agrega incisos que el ejercicio no tiene: {', '.join(x + ')' for x in inventados)}"))
    if _TEMA_ROMANO.get(an.tema) not in ("I", "II", "III", "IV", "V"):
        criterio = re.search(r"criterio\s+(pesimista|optimista)", texto, re.IGNORECASE)
        out.append(Control(not criterio, "No usa criterio pesimista / optimista (no corresponde en este tema)"
                           if not criterio else f"Menciona «{criterio.group(0)}», que no corresponde en este tema"))
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
