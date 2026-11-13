"""Regresión y correlación (TEMA VII) y modelo lineal general (TEMA VIII) en el intérprete.

Arma el planteo a partir de la tabla de datos (o de las sumatorias Σx, Σx², ...):
- qué columna es la variable a explicar "y" (encabezados "Y", "X1", y frases como "pronosticar el PBI
  en función del área", "regresión del fondo sobre la bolsa", "la variable y es la potencia");
- descarta columnas índice (Año, Observación, País);
- escala de cada variable ("en 10^6 hectáreas", "en cientos de km", "en miles de dólares") para pasar
  los valores del texto (5.401.000 hectáreas → 5,401) a las unidades de la tabla.

Tipos de pregunta (inciso): recta, validacion, pronostico (puntual / promedio / individual, unilateral),
ic_coef (β1), ic_rho, ic_rho2 (influencia porcentual), ensayo_coef ("por cada ... aumenta en más de ..."),
transformado (doble log / log-lineal), origen (recta por el origen), multiple (análisis completo),
seleccion (mejor modelo candidato), submodelo ("considere el modelo con X1 y X3").
"""

import re
from math import atanh, exp, log, sqrt
from typing import Dict, List, Optional, Tuple

from solver import regresion as rg

from . import redondeo
from .analizador import _hay
from .modelo import DESPACHO_EXTRA, EXTENSIONES, TIPOS, TIPOS_POR_TEMA, Analisis, Evidencia, Inciso
from .tablas import columnas_numericas
from .texto import Numero, buscar_numeros, fmt, normalizar

TIPOS.update({
    "recta": "Recta de mínimos cuadrados (b0, b1)",
    "validacion": "Validar el modelo (r, r², ensayo de β1 = 0)",
    "pronostico": "Pronóstico (puntual / intervalo para el promedio o para un valor individual)",
    "ic_coef": "Intervalo de confianza para β1 (contribución marginal)",
    "ic_rho": "Intervalo de confianza para ρ (fuerza de la relación)",
    "ic_rho2": "Intervalo para ρ² (influencia porcentual)",
    "ensayo_coef": "Ensayo sobre β1 ('por cada unidad aumenta en más de ...')",
    "transformado": "Modelo linealizable (doble logarítmico / logarítmico lineal)",
    "origen": "Recta por el origen (b0 = 0)",
    "multiple": "Modelo lineal general: estimación y validación (F global, t parciales, R²)",
    "seleccion": "Selección del mejor modelo candidato (DET, Cp, R² ajustado, S², PRESS)",
    "submodelo": "Comparar un modelo con algunas variables contra el completo",
})
TIPOS_POR_TEMA["regresion"] = ["recta", "validacion", "pronostico", "ic_coef", "ic_rho", "ic_rho2", "ensayo_coef",
                               "transformado", "origen", "no_soportado"]
TIPOS_POR_TEMA["regresion_multiple"] = ["multiple", "seleccion", "submodelo", "no_soportado"]

RE_INDICE = r"^(ano|anos|obs|observacion|observaciones|n[º°o]?|nro|numero de orden|periodo|mes|dia|pais|semana|item)\b"
STOP = {"de", "del", "la", "el", "los", "las", "en", "y", "por", "con", "para", "un", "una", "unidades", "cantidad",
        "valor", "valores", "total", "promedio", "medio", "media"}


# ---------------------------------------------------------------- planteo

def _palabras(nombre: str) -> List[str]:
    sin_par = re.sub(r"\([^)]*\)", " ", normalizar(nombre))
    return [w for w in re.findall(r"[a-z][a-z.]{2,}", sin_par) if w not in STOP]


def escala_de(nombre: str, planteo_norm: str = "") -> float:
    """Factor por el que hay que multiplicar el valor de la tabla para tener la unidad 'natural'."""
    n = normalizar(nombre)
    m = re.search(r"10\s*\^?\s*(\d)", n)
    if m:
        return 10.0 ** int(m.group(1))
    for pat, f in ((r"\bmillones\b", 1e6), (r"\bmiles\b", 1e3), (r"\bcientos\b", 100.0)):
        if _hay(pat, n):
            return f
    for pat, f in ((r"expresad[oa]s en miles", 1e3), (r"expresad[oa]s en millones", 1e6)):
        if _hay(pat, planteo_norm):
            return f
    return 1.0


def _sumatorias(texto: str) -> Optional[Dict[str, float]]:
    t = texto.replace("∑", "Σ")
    claves = {"sxy": r"Σ\s*(x\s*[·.*]?\s*y|y\s*[·.*]?\s*x)\s*=\s*", "sxx": r"Σ\s*x\s*(²|\^2)\s*=\s*",
              "syy": r"Σ\s*y\s*(²|\^2)\s*=\s*", "sx": r"Σ\s*x\s*=\s*", "sy": r"Σ\s*y\s*=\s*"}
    out = {}
    for k, pat in claves.items():
        m = re.search(pat, t)
        if m:
            nums = buscar_numeros(t[m.end():m.end() + 25])
            if nums:
                signo = -1 if t[m.end():m.end() + 3].lstrip().startswith("-") else 1
                out[k] = signo * nums[0].valor
    if len(out) < 5:
        return None
    m = re.search(r"(datos de|muestra de|n\s*=)\s*(\d+)", normalizar(texto))
    if not m:
        return None
    out["n"] = float(m.group(2))
    return out


def _elegir_y(nombres: List[str], texto_norm: str) -> Tuple[int, str]:
    puntos = [0.0] * len(nombres)
    motivo = [""] * len(nombres)
    for j, nom in enumerate(nombres):
        nn = normalizar(nom).strip()
        if re.match(r"^y\b|^y\s*[:=(]", nn) or re.search(r"\(y\)|\by\s*=", nn):
            puntos[j] += 10
            motivo[j] = "el encabezado la marca como Y"
        if re.match(r"^x\d*\b|^x\d*\s*[:=(]", nn) or re.search(r"\(x\d*\)", nn):
            puntos[j] -= 10
        pal = _palabras(nom)
        for w in pal:
            w = w.rstrip(".")
            if len(w) < 4:
                continue
            raiz = re.escape(w[:max(4, len(w) - 2)])
            if re.search(r"(pronosticar|predecir|explicar|variable a explicar|recta de regresion de|regresion de la|"
                         r"estimar|desea conocer)[^.;]{0,60}" + raiz, texto_norm):
                puntos[j] += 3
                motivo[j] = motivo[j] or "el enunciado quiere pronosticar / explicar esta variable"
            if re.search(raiz + r"[^.;]{0,50}(en funcion de|a partir de|segun|respecto de)", texto_norm):
                puntos[j] += 2
                motivo[j] = motivo[j] or "aparece antes de 'en función de'"
            if re.search(r"(en funcion de|a partir de|sobre la|sobre el|variable explicativa|depende de)[^.;]{0,50}"
                         + raiz, texto_norm):
                puntos[j] -= 3
            if re.search(r"(requeriria|requerira|tendria|tendra|generaria|generara|produciria|implicaria|provoca|"
                         r"influye en|afecta)\s*(de |en )?(un |una |el |la )?(mayor|menor|mas|menos)?\s*" + raiz, texto_norm):
                puntos[j] += 3
                motivo[j] = motivo[j] or "es la variable que cambia como consecuencia de la otra"
            if re.search(r"variable\s*[\"“”]?y[\"“”]?\s*es\s*(el|la|los|las)?\s*" + raiz, texto_norm):
                puntos[j] += 10
                motivo[j] = "el enunciado dice que esta es la variable y"
            if re.search(r"variable\s*[\"“”]?x[\"“”]?\s*es\s*(el|la|los|las)?\s*" + raiz, texto_norm):
                puntos[j] -= 10
    puntos[-1] += 0.5  # a igualdad, la última columna (como suele estar en las tablas)
    j = max(range(len(nombres)), key=lambda i: puntos[i])
    return j, motivo[j] or "por defecto, la última columna de la tabla"


def completar_planteo(an: Analisis, t):
    suma = _sumatorias(an.planteo)
    if suma:
        an.datos["sumatorias"] = suma
        an.evidencias.append(Evidencia("sumatorias", ", ".join(f"{k} = {fmt(v)}" for k, v in suma.items()), "",
                                       "sumatorias dadas en el enunciado"))
        an.datos["escala_y"] = escala_de(an.planteo)
        an.datos["mostrar_escala_y"] = an.datos["escala_y"] != 1
    tabla = None
    for tb in an.tablas:
        nombres, cols = columnas_numericas(tb)
        quedan = [(nom, c) for nom, c in zip(nombres, cols)
                  if not (_hay(RE_INDICE, normalizar(nom).strip()) or
                          (c == [float(i) for i in range(1, len(c) + 1)] and not re.match(r"^[xy]\s*\d*\b", normalizar(nom))))]
        if len(quedan) >= 2:
            tabla = quedan
            break
    if tabla is None:
        if not suma:
            an.avisos.append("No se encontró la tabla de datos: cargala en el editor de tablas (una fila por renglón).")
        return
    nombres = [n for n, _ in tabla]
    jy, motivo = _elegir_y(nombres, t.norm + " " + normalizar(" ".join(i.texto for i in an.incisos)))
    xs = [(n, c) for j, (n, c) in enumerate(tabla) if j != jy]
    an.datos["y"] = tabla[jy][1]
    an.datos["nombre_y"] = nombres[jy]
    an.datos["escala_y"] = escala_de(nombres[jy], t.norm)
    an.datos["mostrar_escala_y"] = bool(re.search(r"10\s*\^", nombres[jy]))
    an.evidencias.append(Evidencia("y", f"«{nombres[jy]}» ({len(tabla[jy][1])} datos)", "", "variable a explicar: " + motivo))
    if len(xs) >= 2:
        an.tema = "regresion_multiple"
        an.razones_tema.append(f"La tabla tiene {len(xs)} variables explicativas: modelo lineal general.")
        an.datos["xs"] = [c for _, c in xs]
        an.datos["nombres_x"] = [_corto(n, i) for i, (n, _) in enumerate(xs)]
        an.evidencias.append(Evidencia("xs", ", ".join(n for n, _ in xs), "", "variables explicativas"))
    else:
        an.datos["x"] = xs[0][1]
        an.datos["nombre_x"] = xs[0][0]
        an.datos["escala_x"] = escala_de(xs[0][0], t.norm)
        an.evidencias.append(Evidencia("x", f"«{xs[0][0]}»", "", "variable explicativa"))
    # paso 1 del profesor: Y y X en palabras, con su unidad (sale del encabezado de la tabla; se puede corregir)
    for eje, nombre in (("y", nombres[jy]), ("x", xs[0][0] if len(xs) == 1 else "")):
        if not nombre:
            continue
        palabra, unidad = nombre_unidad(nombre)
        if palabra:
            an.datos[f"var_{eje}"] = palabra
        if unidad:
            an.datos[f"unidad_{eje}"] = unidad
            an.evidencias.append(Evidencia(f"unidad_{eje}", unidad, nombre, "unidad del encabezado de la tabla"))


def nombre_unidad(nombre: str) -> Tuple[str, str]:
    """'X = Carbonatación (en mm)' → ('carbonatación', 'mm'); 'Dureza Brinell (en kg/mm²)' → ('dureza Brinell', 'kg/mm²')."""
    s = " ".join(nombre.split())
    unidad = ""
    m = re.search(r"\(([^()]*)\)", s)
    if m:
        unidad = re.sub(r"^(medid[oa]s?\s+)?en\s+", "", m.group(1).strip(), flags=re.I).strip()
        s = (s[:m.start()] + " " + s[m.end():]).strip()
    s = re.sub(r"^\s*[XxYy]\s*\d*\s*[:=]\s*", "", s).strip(" :=-")
    if re.fullmatch(r"[XxYy]\s*\d*", s):
        s = ""
    if len(s) > 1 and not s[:2].isupper():   # 'Resistencia' → 'resistencia'; 'PBI' queda
        s = s[0].lower() + s[1:]
    return s, unidad


def _corto(nombre: str, i: int) -> str:
    m = re.search(r"\b(x\s*\d+)\b", normalizar(nombre))
    return m.group(1).replace(" ", "") if m else (nombre if len(nombre) <= 18 else f"x{i + 1}")


# ---------------------------------------------------------------- incisos

RE_CONF = re.compile(r"(\d+(?:,\d+)?)\s*%\s*(de )?(confianza|seguridad|certeza)|"
                     r"(confianza|prediccion|limites?|intervalo|riesgo|significacion)[^0-9.;]{0,20}?(del|de)\s*(\d+(?:,\d+)?)\s*%|"
                     r"probabilidad de\s*(0,\d+)|riesgo (del|de)\s*(\d+(?:,\d+)?)\s*%|"
                     r"(\d+(?:,\d+)?)\s*%\s*de (riesgo|significacion)")   # 'para un 5% de riesgo' (final 15/12/25)


def _alpha_inciso(texto: str) -> Optional[Tuple[float, Tuple[int, int]]]:
    norm = normalizar(texto)
    m = RE_CONF.search(norm)
    if not m:
        return None
    if m.group(1):
        return 1 - float(m.group(1).replace(",", ".")) / 100, m.span()
    if m.group(6):
        v = float(m.group(6).replace(",", ".")) / 100
        return (v if _hay(r"riesgo|significacion", m.group(4)) else 1 - v), m.span()
    if m.group(7):
        return float(m.group(7).replace(",", ".")), m.span()
    if m.group(9):
        return float(m.group(9).replace(",", ".")) / 100, m.span()
    return float(m.group(10).replace(",", ".")) / 100, m.span()


def _numeros_libres(texto: str, excluir: List[Tuple[int, int]]) -> List[Numero]:
    out = []
    for n in buscar_numeros(texto):
        if any(a <= n.ini < b for a, b in excluir):
            continue
        if re.search(r"(x|β|beta|b)\s*\d?\s*$", texto[max(0, n.ini - 3):n.ini], re.I) and n.valor in (0, 1, 2):
            continue  # 'β1 = 0', 'x1'
        out.append(n)
    return out


RE_X0 = (r"(para (un|una|el|la)?\s*[a-z ]{0,40}?(de|igual a|es de|en)|si (la|el)[a-z ]{0,50}(fuese|fuera|es|resulta|sera)( de| del| igual a)?|"
         r"\ba\b|de|del|en|sera del|sera de|exhibidores de|es igual a)\s*$")


def _x0(inc_texto: str, excluir) -> Optional[Numero]:
    libres = _numeros_libres(inc_texto, excluir)
    norm = normalizar(inc_texto)
    for n in libres:
        if _hay(RE_X0, norm[max(0, n.ini - 60):n.ini]):
            return n
    return libres[-1] if libres else None


def _dos_x0(texto: str, excluir, norm: str) -> Optional[Tuple[float, Numero]]:
    """Dos valores de x en el mismo inciso: una pregunta puntual ('¿cuál sería ... a 85?') y después un intervalo
    ('estime un IC ... para 55')."""
    t_norm = normalizar(texto)
    libres = [n for n in _numeros_libres(texto, excluir)
              if _hay(RE_X0 + r"|\b(para|a)\s*$", t_norm[max(0, n.ini - 60):n.ini])]
    if len(libres) != 2 or libres[0].valor == libres[1].valor:
        return None
    entre = normalizar(texto)[libres[0].fin:libres[1].ini]
    if not (_hay(r"\?", entre) or _hay(r"[.;]", entre)) or not _hay(r"(intervalo|\bic\b|limites|estim)", entre):
        return None
    return libres[0].valor, libres[1]


def _pend_val(inc: Inciso, an: Analisis, norm: str, texto: str) -> Optional[Tuple[float, str, str]]:
    """'por cada 1.000 dólares ... aumento de 2.500 como mínimo' → (β10, cola, explicación)."""
    norm = re.sub(r"\bcada mil\b", "cada 1.000", re.sub(r"\bcada cien\b", "cada 100", norm))
    m = re.search(r"(?:por )?cada\s*(\d[\d.,]*)?\s*([a-z ºº°]{0,40}?)(adicional|que (se )?(desciende|baja|disminuye|aumenta|sube|incrementa)|"
                  r"que se invierte|que se invierten|en la|de|\b)", norm)
    if not m:
        return None
    resto = norm[m.end():]
    cant_x = float(m.group(1).replace(".", "").replace(",", ".")) if m.group(1) else 1.0
    # x baja solo si lo dice pegado a 'cada': 'por cada grado que desciende la temperatura' (en 'cada mm más de
    # deformación baja la dureza' el que baja es y)
    baja_x = _hay(r"(desciende|baja|disminuye|\bmenos\b)", m.group(0)) or \
        _hay(r"^\s*([a-z]+ )?(de [a-z]+ )?(menos|que (se )?(desciende|baja|disminuye|reduce))\b", resto[:40])
    m2 = re.search(r"(aument|increment|disminu|reduc|baj|sub|crec|decrec)[a-z]*[^0-9]{0,40}?(\d[\d.,]*)", resto)
    if not m2:
        m2 = re.search(r"(\d[\d.,]*)[^0-9]{0,30}?(como minimo|como maximo|por lo menos)", resto) or \
            re.search(r"(?:al menos|como minimo|por lo menos)\s+(\d[\d.,]*)", resto)
        if not m2:
            return None
        valor_txt, verbo = m2.group(1), "aument"
    else:
        valor_txt, verbo = m2.group(2), m2.group(1)
    cant_y = [n.valor for n in buscar_numeros(valor_txt)][0]
    sube_y = verbo.startswith(("aument", "increment", "sub", "crec"))
    signo = (1 if sube_y else -1) * (-1 if baja_x else 1)
    ex, ey = an.datos.get("escala_x", 1.0), an.datos.get("escala_y", 1.0)
    # el texto da cantidades en la unidad natural: se pasan a la de la tabla
    if ex != 1.0 and cant_x >= ex:
        cant_x /= ex
    if ey != 1.0 and cant_y >= ey / 100:
        cant_y /= ey
    b10 = signo * cant_y / cant_x
    estricto_mas = _hay(r"(mas de|como minimo|por lo menos|al menos|supera)", resto[:80] + norm[:m.start()])
    if signo > 0:
        cola = "derecha"
    else:
        cola = "izquierda"
    expl = (f"por cada {fmt(cant_x)} unidad(es) de x, y {'aumenta' if sube_y else 'disminuye'} "
            f"{fmt(cant_y)}{' (en las unidades de la tabla)' if ey != 1 or ex != 1 else ''}"
            f"{' ante un descenso de x' if baja_x else ''} → β1₀ = {fmt(b10, 4)}; se quiere probar que la pendiente "
            f"es {'mayor' if cola == 'derecha' else 'menor'} (H1)"
            + ("" if estricto_mas else " (la afirmación no dice 'más de': se toma igual como lo que hay que probar)"))
    return b10, cola, expl


def clasificar(inc: Inciso, an: Analisis, norm: str) -> Tuple[str, str]:
    texto = re.sub(r"(\d)\s*([º°])", r"\1 \2", inc.texto)  # '5ºC' → '5 ºC' (si no, no se lee el número)
    excl = []
    a = _alpha_inciso(texto)
    if a:
        inc.params["alpha"] = a[0]
        excl.append(a[1])
    if an.tema == "regresion_multiple":
        return _clasificar_multiple(inc, an, norm)
    # modelo transformado / origen
    if _hay(r"doble logaritmic|y\s*=\s*(α|alfa|a)\s*[·.*]?\s*x\s*\^|y = α·x|elasticidad|potencial", norm) or \
            _hay(r"\^\s*(β|beta|b)\b|x\^β", texto.lower()):
        inc.params["modelo"] = "loglog"
    elif _hay(r"logaritmico lineal|log[- ]?lineal|exponencial|semilogaritmic", norm):
        inc.params["modelo"] = "loglin"
    elif _hay(r"lineal[- ]logaritmic|lin[- ]log", norm):
        inc.params["modelo"] = "linlog"
    if _hay(r"intercepto igual a (0|cero)|pasa(r)? por el origen|ordenada (al origen )?(nula|igual a 0)|\bb0\s*=\s*0", norm):
        inc.params["origen"] = True
    if inc.params.get("modelo") and _hay(r"(analizar|investig|mejor|ajusta|compar|estimar los parametros|si se supone|"
                                         r"suponiendo|estimar|verificar|valid)", norm):
        return "transformado", "Pide probar un modelo linealizable: se ajusta la recta sobre las variables transformadas y se compara r²."
    if inc.params.get("origen") and not _hay(r"(intervalo|estimar con|prediccion)", norm):
        return "origen", "Pide el modelo con intercepto 0: b1 = Σxy / Σx²."
    # ensayo de la pendiente contra un valor
    pv = _pend_val(inc, an, norm, texto)
    if pv is None and _hay(r"(afirmacion|confirman|lo que (dice|afirma|sostiene)|es correct|respald|avalan|tiene razon)", norm):
        pv = _pend_val(inc, an, normalizar(an.planteo), an.planteo)  # la afirmación está en el planteo
    if pv and _hay(r"(se puede|puede|es correct|confirman|asegurar|afirmar|afirmacion|considerar|respald|avalan|"
                   r"tiene razon|sostiene)", norm + " " + normalizar(an.planteo)) \
            and not _hay(r"(estimar|intervalo)", norm):
        inc.params["beta10"], inc.params["tail"] = pv[0], pv[1]
        inc.razones.append(pv[2])
        return "ensayo_coef", "Afirmación sobre el cambio de y por unidad de x: ensayo de β1 contra un valor (caso I / II de la cátedra)."
    pide_rho2 = _hay(r"(influencia porcentual|coeficiente de determinacion|porcentaje de (la )?variabilidad)", norm) and \
        _hay(r"(estim|intervalo|confianza|calcul|concepto|cual es|que valor)", norm)   # 'Calcule ese parámetro' (rec 2024)
    # 'hallar la recta, interpretar ... e investigar la asociación lineal. ¿Qué concepto ... influencia porcentual?'
    # (final 15/12/25): un solo inciso que pide la recta, la validación y r² con su intervalo
    # 'Encuentre un modelo lineal ... Calcule el coeficiente de determinación ... Testee el modelo' (final 2024)
    if _hay(r"(hallar|calcular|obtener|determinar) la recta|(encuentre|encontrar|hallar|halle|obtener|obtenga|"
            r"determinar|determine|ajustar|ajuste) (un|el) modelo (lineal|de regresion)", norm):
        if _hay(r"(validar|valide|interpret|asociacion lineal|relacion lineal|test|ensay|coeficiente de determinacion)", norm):
            inc.params["validar"] = True
        if pide_rho2:
            inc.params["rho2"] = True
        return "recta", "Recta de mínimos cuadrados: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²), b0 = ȳ - b1·x̄."
    # 'por cada ppm de Fosfato, ¿cuál será la máxima ...?': cambio de y por unidad de x → límite unilateral de β1
    if _hay(r"\bpor cada (unidad|[a-z]{1,12}) (de|del|adicional|mas)\b", norm) and _hay(r"\b(maxim|minim)[ao]\b", norm) \
            and not _numeros_libres(texto, excl):
        inc.params["cola"] = "superior" if _hay(r"\bmaxim[ao]\b", norm) else "inferior"
        return "ic_coef", ("Pide el cambio máximo / mínimo de y por cada unidad de x (contribución marginal): límite "
                           "de confianza unilateral de β1, b1 ± t(1-α; n-2)·Sb1.")
    if pide_rho2:
        return "ic_rho2", "Influencia porcentual: r² y su intervalo (los límites del IC de ρ al cuadrado)."
    if _hay(r"(fuerza de la relacion|estime[^.?]{0,40}(dicho )?coeficiente|intervalo[^.?]{0,40}correlacion|"
            r"estimar[^.?]{0,40}correlacion)", norm):
        return "ic_rho", "Estimar ρ: transformación de Fisher Z = ½·ln((1+r)/(1-r)) ± z/√(n-3)."
    if _hay(r"(contribucion marginal|coeficiente de regresion|intervalo[^.?]{0,40}(pendiente|β1|beta))", norm):
        return "ic_coef", "Intervalo de confianza para β1: b1 ± t(1-α/2; n-2)·Sb1."
    x0 = None
    if _hay(r"(pronostic|predic|estim|estimador puntual|cual (es|sera|seria) (la|el)|que (demanda|venta|valor)|limites|"
            r"intervalo|\bic\b|minim[ao]|maxim[ao])", norm) and not _hay(r"(hallar|calcular) la recta", norm):
        if _hay(r"(ningun|no realizar|sin gast|nulo|igual a cero|no se gasta nada|no se invierte nada|sin invertir)", norm):
            inc.params["x0"] = 0.0
            x0 = 0.0
        else:
            n = _x0(texto, excl)
            dos = _dos_x0(texto, excl, norm)
            if dos:
                # '¿Cuál sería el tiempo a 85ºC? Estime un IC para el tiempo medio para 55ºC' (final 2024): el primero es
                # un pronóstico puntual y el segundo el intervalo pedido
                inc.params["x0_puntual"], n = dos
                inc.razones.append(f"El inciso pide dos cosas: el pronóstico puntual para x = {fmt(dos[0])} y el intervalo "
                                   f"para x = {fmt(dos[1].valor)}.")
            if n is not None:
                x0 = n.valor
                ex = an.datos.get("escala_x", 1.0)
                if ex != 1 and x0 >= ex / 10:
                    inc.razones.append(f"x₀ = {fmt(x0)} pasado a las unidades de la tabla (÷ {fmt(ex)}).")
                    x0 /= ex
                inc.params["x0"] = x0
    if x0 is not None or (_hay(r"(dicho pronostico|para dicho)", norm)):
        if _hay(r"(promedio|\bmedi[ao]s?\b|ley promedio)", norm) and not _hay(r"temperatura media", norm):
            inc.params["individual"] = False
        elif _hay(r"(prediccion|pronostico|individual|un mes|un ano|un dia|un usuario|un determinado|un acero|"
                  r"en un determinado|para un|durante la semana|el ano entrante|minim|maxim)", norm):
            inc.params["individual"] = True
        if _hay(r"\bminim[ao]\b", norm):
            inc.params["cola"] = "inferior"
        elif _hay(r"\bmaxim[ao]\b", norm):
            inc.params["cola"] = "superior"
        if _hay(r"estimador puntual|valor puntual|pronostico puntual", norm) and not _hay(r"(limites|intervalo|confianza)", norm):
            inc.params["puntual"] = True
        return "pronostico", "Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo."
    if _hay(r"(analizar el ajuste|validar|validez|asociacion lineal|linealmente relacionad|relacion lineal|"
            r"coeficiente de correlacion|grado de relacion|dos criterios|existe relacion|evidencia)", norm):
        return "validacion", "Validar el modelo: r, r² y ensayo de existencia (H0: β1 = 0, |t| > t(1-α; n-2))."
    if _hay(r"(recta|minimos cuadrados|estimar los parametros|ecuacion|estimador)", norm):
        if _hay(r"(validar|interpretar)", norm):
            inc.params["validar"] = True
        return "recta", "Recta de mínimos cuadrados: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²), b0 = ȳ - b1·x̄."
    return "no_soportado", "No se reconoció qué pide: elegí el tipo a mano."


def _clasificar_multiple(inc: Inciso, an: Analisis, norm: str) -> Tuple[str, str]:
    if inc.letra == "única":
        norm = norm + " " + normalizar(an.planteo)
    m = re.findall(r"\bx\s*(\d)\b", norm)
    if _hay(r"(considere|considerar|tome|con las variables|solamente|solo con)", norm) and len(set(m)) >= 1:
        inc.params["variables"] = sorted({int(v) for v in m})
        return "submodelo", "Compara el modelo con esas variables contra el completo (R² ajustado, S², tests t)."
    if _hay(r"(mejor modelo|modelo candidato|mejor modelo candidato|cual es el mejor|investigue cual|seleccion|"
            r"mejor se ajusta|determinar el mejor)", norm):
        return "seleccion", "Análisis exploratorio: tabla de todos los modelos candidatos (DET > 0,1, Cp/p < 5, R²aj, S², PRESS)."
    if _hay(r"(asociacion lineal|hay relacion|existe relacion)", norm):
        inc.params["solo_global"] = True
    return "multiple", "Modelo lineal general: b = (X'X)⁻¹X'y, F global, t parciales, R² y R² ajustado."


# ---------------------------------------------------------------- resolución (simple)

def _reg(d, modelo=None, origen=None) -> rg.RegresionSimple:
    from .resolver import FaltaDato
    modelo = modelo or d.get("modelo") or "lineal"
    origen = d.get("origen") if origen is None else origen
    if d.get("x") and d.get("y"):
        return rg.ajustar_simple(d["x"], d["y"], modelo=modelo, origen=bool(origen))
    s = d.get("sumatorias")
    if s and modelo == "lineal":
        return rg.desde_sumatorias(s["n"], s["sx"], s["sxx"], s["sy"], s["syy"], s["sxy"], origen=bool(origen))
    raise FaltaDato("Faltan los datos (x, y) o las sumatorias")


def _el(nombre: str) -> str:
    """Con artículo: 'carbonatación' → 'la carbonatación', 'consumo' → 'el consumo', 'ventas' → 'las ventas'.
    'x' / 'y' y siglas (PBI) quedan como están o con 'el'."""
    if nombre in ("x", "y") or re.match(r"^(el|la|los|las)\b", nombre, re.I):
        return nombre
    w = re.findall(r"[A-Za-zÁÉÍÓÚáéíóúñÑ]+", nombre)
    w = w[0].lower() if w else ""
    if w in ("área", "agua", "aula", "arma", "hambre", "ala"):
        return "el " + nombre
    if w.endswith(("as", "iones", "dades")):
        return "las " + nombre
    if w.endswith("s") and len(w) > 3 and not w.endswith(("is", "us")):
        return "los " + nombre
    if w.endswith(("a", "ión", "dad", "tud", "ez", "umbre")) and w not in ("día", "mapa", "sistema", "problema", "clima"):
        return "la " + nombre
    return "el " + nombre


def _pl(nombre: str) -> bool:
    return _el(nombre).startswith(("los ", "las "))


def _v(nombre: str, verbo: str) -> str:
    """Concordancia: 'las ventas' + 'aumenta' → 'aumentan'."""
    return verbo + "n" if _pl(nombre) else verbo


def _contraer(t: str) -> str:
    """'de el PBI' → 'del PBI'; 'a el' → 'al'."""
    return re.sub(r"\b(de|De|a|A) el\b", lambda m: {"de": "del", "De": "Del", "a": "al", "A": "Al"}[m.group(1)], t)


def _El(nombre: str) -> str:
    t = _el(nombre)
    return t[0].upper() + t[1:]


def _vars(d) -> Tuple[str, str, str, str]:
    """(Y en palabras, unidad de Y, X en palabras, unidad de X). Sin datos: 'y' y 'x'."""
    ny, uy = d.get("var_y") or "", d.get("unidad_y") or ""
    nx, ux = d.get("var_x") or "", d.get("unidad_x") or ""
    if not ny and d.get("nombre_y"):
        ny, u = nombre_unidad(d["nombre_y"])
        uy = uy or u
    if not nx and d.get("nombre_x"):
        nx, u = nombre_unidad(d["nombre_x"])
        ux = ux or u
    if not (uy and ux):
        # «(ambas medidas en miles de lbs./pulg2)»: la misma unidad para las dos variables (R4)
        m = re.search(r"\b(?:ambas|las dos)(?: variables)? (?:medidas|expresadas|en) (?:en )?([^);:]{2,40}?)\s*(?:[);:]|\.\s|$)",
                      d.get("_texto") or "")
        if m:
            uy, ux = uy or m.group(1).strip(), ux or m.group(1).strip()
    return ny or "y", uy, nx or "x", ux


def _con(v: str, u: str) -> str:
    return f"{v} {u}" if u else v


def _u_b1(uy: str, ux: str) -> str:
    if uy and uy == ux:     # misma unidad: «miles de lbs./pulg² por cada mil lbs./pulg²» (no «miles/miles»)
        return f"{uy} por {_una(ux)}"
    return f"{uy}/{ux}" if uy and ux else ""


def _una(u: str) -> str:
    """«miles de lbs./pulg2» → «cada mil lbs./pulg2»; «MPa» → «cada MPa»."""
    return "cada " + re.sub(r"^miles de\s+", "mil ", u)


def _por_cada(nx: str, ux: str) -> str:
    if ux.strip() == "%":   # la variable ya está en %: el cambio es de un PUNTO porcentual, no de un 1% (clase 05/11)
        return f"por cada punto porcentual adicional de {_el(nx)}"
    return f"por {_una(ux)} adicional de {nx}" if ux else f"por cada unidad adicional de {nx}"


def _entorno(d, reg) -> Optional[Tuple[float, float]]:
    """Entorno observado de x (en la escala de la tabla), si están los datos."""
    xs = d.get("x")
    if xs and len(xs) == reg.n:
        return min(xs), max(xs)
    return None


def _pasos_recta(reg: rg.RegresionSimple, res, d):
    yv, xv, desc = rg.TRANSFORMACIONES[reg.modelo]
    ny, uy, nx, ux = _vars(d)
    res.pasos.append(f"**Variables**: Y = {ny}" + (f" ({uy})" if uy else "") + " → variable explicada (aleatoria); "
                     f"X = {nx}" + (f" ({ux})" if ux else "") + " → variable explicativa. Y = f(X).")
    if reg.modelo != "lineal":
        res.pasos.append(f"**Modelo**: {desc}. Se trabaja con Y' = {yv} y X' = {xv}.")
    sx, sy = reg.xbar * reg.n, reg.ybar * reg.n
    res.pasos.append(f"**Procesamiento de los datos**: n = {reg.n}; Σx = {fmt(sx, 4)}; x̄ = {fmt(reg.xbar, 6)}; "
                     f"Σx² = {fmt(reg.sum_x2, 4)}; Σy = {fmt(sy, 4)}; ȳ = {fmt(reg.ybar, 6)}; Σy² = {fmt(reg.sum_y2, 4)}; "
                     f"Σxy = {fmt(reg.sum_xy, 4)}.")
    ub1 = _u_b1(uy, ux) if reg.modelo == "lineal" else ""
    if reg.origen:
        res.pasos.append(f"**Recta por el origen**: b1 = Σxy / Σx² = {_con(fmt(reg.b1, 6), ub1)}.")
    else:
        res.pasos.append(f"**Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = {fmt(reg.Sxy, 4)}/{fmt(reg.Sxx, 4)} = "
                         f"{_con(fmt(reg.b1, 6), ub1)}; b0 = ȳ - b1·x̄ = {fmt(reg.ybar, 4)} - ({fmt(reg.b1, 4)})·"
                         f"{fmt(reg.xbar, 4)} = {_con(fmt(reg.b0, 6), uy if reg.modelo == 'lineal' else '')}.")
    res.pasos.append(f"**Recta (modelo estimador)**: {_coma(reg.ecuacion())}.")
    n_par = 1 if reg.origen else 2
    formula = "(Σy² - b1·Σxy)" if reg.origen else "(Σy² - b0·Σy - b1·Σxy)"
    res.pasos.append(f"**Ajuste**: S² = {formula}/(n - {n_par}) = {fmt(reg.S2, 6)}; S = {fmt(reg.S, 6)}; "
                     f"Sb1 = S/√(Σx² - n·x̄²) = {fmt(reg.Sb1, 6)}; r = {fmt(reg.r, 6)}; r² = {fmt(reg.r2, 6)}.")
    res.numeros += [reg.b0, reg.b1, reg.S, reg.S2, reg.Sb1]
    if reg.modelo in ("loglog", "loglin"):
        res.numeros += [exp(reg.b0)] + ([exp(reg.b1)] if reg.modelo == "loglin" else [])
        forma = (f"y = {fmt(exp(reg.b0), 4)}·x^{fmt(reg.b1, 4)}" if reg.modelo == "loglog"
                 else f"y = {fmt(exp(reg.b0), 4)}·{fmt(exp(reg.b1), 4)}^x")
        res.pasos.append(f"**Volviendo a la escala original**: {forma}.")


def _coma(s: str) -> str:
    return re.sub(r"(\d)\.(\d)", r"\1,\2", s)


def _interpretar(reg: rg.RegresionSimple, d) -> str:
    """Interpretación de los estimadores EN TÉRMINOS DEL PROBLEMA, como en clase (05/11)."""
    ny, uy, nx, ux = _vars(d)
    sube = "aumenta" if reg.b1 >= 0 else "disminuye"
    if reg.modelo == "loglog":
        return (f"b1 = {fmt(reg.b1, 4)} es la elasticidad (modelo de elasticidad constante): si {_el(nx)} {_v(nx, 'aumenta')} un 1%, "
                f"{_el(ny)} {_v(ny, sube)} un {fmt(abs(reg.b1), 4)}% (cambio porcentual por cambio porcentual).")
    if reg.modelo == "loglin":
        return (f"b1·100 = {fmt(100 * reg.b1, 4)}: {_por_cada(nx, ux)}, {_el(ny)} {_v(ny, sube)} aproximadamente un "
                f"{fmt(abs(100 * reg.b1), 4)}% (cambio porcentual de Y por cambio absoluto de X; exacto: "
                f"(e^b1 - 1)·100 = {fmt(100 * (exp(reg.b1) - 1), 4)}%).")
    if reg.modelo == "linlog":
        return (f"b1/100 = {fmt(reg.b1 / 100, 4)}: si {_el(nx)} {_v(nx, 'aumenta')} un 1%, {_el(ny)} {_v(ny, sube)} {_con(fmt(abs(reg.b1) / 100, 4), uy)} "
                f"(cambio absoluto de Y por cambio porcentual de X).")
    if reg.modelo != "lineal":
        return f"b1 = {fmt(reg.b1, 4)} (modelo {reg.modelo})."
    txt = (f"b1 = {_con(fmt(reg.b1, 4), _u_b1(uy, ux))} (coeficiente de regresión o contribución marginal): "
           f"{_por_cada(nx, ux)}, {_el(ny)} {_v(ny, sube)} en promedio {_con(fmt(abs(reg.b1), 4), uy)}.")
    if not reg.origen:
        ent = _entorno(d, reg)
        txt += (f" b0 = {_con(fmt(reg.b0, 4), uy)}: en teoría, sería {_el(ny)} cuando {_el(nx)} {_v(nx, 'vale')} 0"
                + (f" {ux}" if ux else "") + ", pero no se puede asegurar")
        if ent:
            dentro = ent[0] <= 0 <= ent[1]
            txt += (f": el modelo vale solo en el entorno observado ({_el(nx)} entre {fmt(ent[0], 4)} y "
                    f"{_con(fmt(ent[1], 4), ux)})" + ("" if dentro else " y X = 0 queda afuera"))
        txt += ". Por eso no se estima β0."
    return txt


def _influencia(reg, d) -> str:
    ny, _, nx, _ = _vars(d)
    return (f"r² = {fmt(reg.r2, 4)}: {_el(nx)} {_v(nx, 'influye')} en un {fmt(100 * reg.r2, 2)}% (aprox.) en la explicación de {_el(ny)}; el "
            f"{fmt(100 * (1 - reg.r2), 2)}% restante lo explican la perturbación del entorno u otras variables que no "
            f"están en el modelo.")


# Uso del modelo → mínimo orientativo de r² (profesor, 05/11: «orientativos, no taxativos»). Se deduce del enunciado.
USOS = (
    ("técnico o industrial", 0.8,
     r"\b(acero|varillas?|aleacion|metal|materiales?|rotura|traccion|elastic|dureza|resistencia (a la|al|del|de la)|"
     r"mpa|kg/cm|pulg|soldadura|maquinas?|motor|horno|temperatura|presion|voltaje|tension electrica|piezas?|"
     r"hormigon|concreto|proceso (productivo|industrial|de fabricacion)|planta|fabrica|produccion|rendimiento del|"
     r"desgaste|corrosion|viscosidad|caudal|potencia|combustible|quimic|reactor|catalizador|fosfato|decapado)"),
    ("económico", 0.6,
     r"\b(ventas|precios?|ingresos?|demanda|oferta|pbi|gastos?|publicidad|costos?|salarios?|sueldos?|consumo|"
     r"inflacion|economi|mercado|empresa[s]? de|ganancias?|utilidad|inversion|dolares?|pesos|\$)"),
    ("sociología o psicología", 0.4,
     r"\b(encuestas?|actitud|satisfaccion|ansiedad|estres|opinion|alumnos|estudiantes|rendimiento academico|"
     r"psicolog|sociolog|conducta|autoestima|motivacion|test de aptitud)"),
)


def uso_del_modelo(d) -> Optional[Tuple[str, float, str]]:
    """(uso, r² mínimo, palabra del enunciado que lo indica) o None si no se reconoce o es ambiguo."""
    norm = normalizar(" ".join(str(d.get(k) or "") for k in ("_texto", "nombre_y", "nombre_x", "unidad_y", "unidad_x")))
    hallados = []
    for nombre, minimo, patron in USOS:
        m = [x.group(0).strip() for x in re.finditer(patron, norm)]
        if m:
            hallados.append((len(m), nombre, minimo, ", ".join(dict.fromkeys(m[:3]))))
    if not hallados:
        return None
    hallados.sort(reverse=True)
    if len(hallados) > 1 and hallados[0][0] == hallados[1][0]:
        return None
    _, nombre, minimo, palabra = hallados[0]
    return nombre, minimo, palabra


def _minimo_r2(d) -> float:
    u = uso_del_modelo(d or {})
    return u[1] if u else 0.4


def _fuerza_txt(reg, d) -> str:
    """La fuerza de la relación juzgada con el mínimo del USO del problema (si se reconoce)."""
    u = uso_del_modelo(d or {})
    if not u:
        return (f"{rg.validez_por_r2(reg.r2)}. ⚠️ No se reconoció el uso del modelo: decidí vos cuál es (técnico ⇒ 0,8; "
                f"económico ⇒ 0,6; social ⇒ 0,4) y si r² alcanza.")
    nombre, minimo, palabra = u
    if reg.r2 >= minimo:
        return (f"Es un problema de uso {nombre} («{palabra}» en el enunciado): mínimo orientativo r² ≥ "
                f"{fmt(minimo, 1)}. r² = {fmt(reg.r2, 4)} ≥ {fmt(minimo, 1)} ⇒ la relación es lo bastante fuerte para "
                f"este uso")
    return (f"Es un problema de uso {nombre} («{palabra}» en el enunciado): mínimo orientativo r² ≥ {fmt(minimo, 1)}. "
            f"r² = {fmt(reg.r2, 4)} < {fmt(minimo, 1)} ⇒ la relación NO es lo bastante fuerte para este uso: el modelo "
            f"NO se valida (el mínimo es orientativo, no taxativo: si el uso fuera otro, revisalo)")


def _validacion(reg, alpha, res, d=None):
    """Análisis confirmatorio de la cátedra: 1) existencia de la relación (H0: ρ = 0 ⇔ β1 = 0, |t_obs| vs t(1-α; n-2));
    2) fuerza de la relación (r² según el uso del modelo). Son condiciones necesarias, no suficientes."""
    d = d or {}
    ny, _, nx, _ = _vars(d)
    e = rg.ensayo_beta1(reg, alpha, 0.0, "existencia")
    elegido = (" (el enunciado no lo fija: se elige y se justifica antes de ver los datos, p. ej. «α = 0,05: no hay "
               "una decisión costosa que pida un riesgo más chico»)") if d.get("alpha_elegido") else ""
    res.pasos.append(f"**Validación del modelo (análisis confirmatorio)**, 1° existencia de la relación: H0: ρ = 0 "
                     f"(β1 = 0, no hay relación lineal)  vs  H1: ρ ≠ 0; α = {fmt(alpha, 4)}{elegido}. "
                     f"|t_obs| = |r|/√((1 - r²)/(n - 2)) = |b1|/Sb1 = {fmt(abs(e.t_c), 4)}; ν = n - 2 = {e.nu}; "
                     f"t(1-α; ν) = t({fmt(1 - alpha, 4)}; {e.nu}) = {fmt(e.t_critico, 4)}. CR: si |t_obs| > "
                     f"{fmt(e.t_critico, 4)} ⇒ se rechaza H0. "
                     + (f"{fmt(abs(e.t_c), 4)} > {fmt(e.t_critico, 4)} ⇒ se rechaza H0: existe relación lineal entre "
                        f"{_el(nx)} y {_el(ny)}." if e.rechaza else
                        f"{fmt(abs(e.t_c), 4)} ≤ {fmt(e.t_critico, 4)} ⇒ no se rechaza H0: no se puede asegurar que "
                        f"exista relación lineal: el modelo NO es válido."))
    res.pasos.append(f"**2° fuerza de la relación**: r² = {fmt(reg.r2, 4)} ({fmt(100 * reg.r2, 2)}%). Mínimos orientativos "
                     f"según el uso: 0,4 sociología o psicología; 0,6 económico; 0,8 técnico o industrial. "
                     f"{_fuerza_txt(reg, d)}.")
    res.numeros += [reg.r, abs(reg.r), reg.r2, e.t_c, e.t_critico]
    return e


def _valido(e, reg, d=None) -> bool:
    return e.rechaza and reg.r2 >= _minimo_r2(d)


def _veredicto(e, reg, d) -> str:
    """La conclusión de la validación: existencia + fuerza según el uso."""
    if not e.rechaza:
        return "El modelo NO es válido (no se puede asegurar que exista relación lineal): no se lo puede usar para estimar."
    u = uso_del_modelo(d or {})
    if _valido(e, reg, d):
        return ("Existe relación lineal y " + (f"r² = {fmt(reg.r2, 4)} ≥ {fmt(u[1], 1)} (uso {u[0]})" if u else
                                                 rg.validez_por_r2(reg.r2)) +
                ": el modelo se valida (solo para el entorno observado).")
    return (f"Existe relación lineal, pero r² = {fmt(reg.r2, 4)} < {fmt(u[1], 1)}, el mínimo orientativo para un uso "
            f"{u[0]}: el modelo NO se valida para este uso, así que las estimaciones que se hagan con él no tienen "
            f"sentido (según el profesor). Las cuentas se muestran solo como referencia.")


def _asegurar_validacion(reg, d, alpha, res, estado, medida: bool = False):
    """El profesor: «la validación la vas a tener que hacer aunque no te la pida». Si ningún inciso anterior validó
    esta recta, se valida acá antes de usarla. Si no es válida, la pregunta no tiene sentido."""
    if estado.get("validada") is not reg:
        res.pasos.append("**Primero se valida el modelo** (aunque el inciso no lo pida: un modelo no validado no sirve "
                         "para estimar).")
        e = _validacion(reg, alpha, res, d)
        estado["validada"], estado["valido"] = reg, _valido(e, reg, d)
    if not estado.get("valido", True) and medida:
        res.avisos.append("El modelo NO se valida, pero r² igual se informa: es la medida de la fuerza de la relación (la "
                          "que no alcanza el mínimo del uso). Decilo en la respuesta.")
    elif not estado.get("valido", True):
        res.avisos.append("El modelo NO es válido: según el profesor, entonces la pregunta no tiene sentido (las cuentas "
                          "se muestran solo como referencia).")


def recta(d, alpha, res, estado):
    reg = _reg(d)
    _pasos_recta(reg, res, d)
    estado["reg"] = reg
    res.resumen = _coma(reg.ecuacion())
    if d.get("alpha") is None:
        res.avisos.append("No fijan α para validar el modelo: se eligió α = 0,05 (en el examen, elegirlo y justificarlo).")
    e = _validacion(reg, alpha, res, d)
    estado["validada"], estado["valido"] = reg, _valido(e, reg, d)
    concl = _interpretar(reg, d) + " " + _influencia(reg, d) + " "
    concl += _veredicto(e, reg, d)
    res.resumen += f"; r = {fmt(reg.r, 4)}" + ("" if d.get("rho2") else f"; r² = {fmt(reg.r2, 4)}")
    if d.get("rho2"):
        resumen = res.resumen
        ic_rho2(d, alpha, res, estado)
        concl += " " + res.conclusion
        res.resumen = resumen + "; " + res.resumen
    res.conclusion = concl


def validacion(d, alpha, res, estado):
    reg = _reg(d)
    _pasos_recta(reg, res, d)
    e = _validacion(reg, alpha, res, d)
    estado["reg"] = reg
    estado["validada"], estado["valido"] = reg, _valido(e, reg, d)
    ny, _, nx, _ = _vars(d)
    res.resumen = f"r = {fmt(reg.r, 4)}; r² = {fmt(reg.r2, 4)}; tc = {fmt(e.t_c, 4)} vs {fmt(e.t_critico, 4)}: " + \
        ("RECHAZA H0 (hay relación)" if e.rechaza else "NO rechaza H0")
    res.pasos.append(f"**Interpretación en términos del problema**: {_interpretar(reg, d)} {_influencia(reg, d)}")
    res.conclusion = ((f"Con α = {fmt(alpha, 4)}, se puede asegurar que existe relación lineal entre {_el(nx)} y {_el(ny)}"
                       if e.rechaza else
                       f"Con α = {fmt(alpha, 4)}, no se puede asegurar que exista relación lineal entre {_el(nx)} y {_el(ny)}")
                      + f"; r = {fmt(reg.r, 4)}, r² = {fmt(reg.r2, 4)}. " + _veredicto(e, reg, d)
                      + " " + _interpretar(reg, d) + " " + _influencia(reg, d))


def _reg_estado(d, estado):
    """La recta del inciso anterior si la había (respeta el modelo transformado / por el origen)."""
    if d.get("modelo") or d.get("origen"):
        return _reg(d)
    return estado.get("reg") or _reg(d)


def pronostico(d, alpha, res, estado):
    xp = d.get("x0_puntual")
    if xp is None:
        return _pronostico(d, alpha, res, estado)
    # dos pedidos en el inciso: el pronóstico puntual para x0_puntual y el intervalo para x0
    reg = _reg_estado(d, estado)
    ny, uy, nx, ux = _vars(d)
    yp = reg.predecir(xp)
    res.pasos.append(f"**Pronóstico puntual** para x = {fmt(xp, 4)}: ŷ = b0 + b1·x = {fmt(reg.b0, 4)} + ({fmt(reg.b1, 4)})·"
                     f"{fmt(xp, 4)} = {fmt(yp, 4)}" + (f" (= {fmt(reg.a_original(yp), 4)} en la escala original)"
                                                       if reg.modelo != "lineal" else "") + ".")
    _pronostico(d, alpha, res, estado)
    res.numeros = [yp, reg.a_original(yp)] + res.numeros
    res.resumen = f"ŷ({fmt(xp)}) = {fmt(reg.a_original(yp), 4)} | x₀ = {fmt(d['x0'])}: {res.resumen}"
    res.conclusion = (f"El pronóstico puntual de {_el(ny)} para {_el(nx)} = {_con(fmt(xp, 4), ux)} es "
                      f"{_con(fmt(reg.a_original(yp), 4), uy)}. " + res.conclusion)


def _pronostico(d, alpha, res, estado):
    from .resolver import FaltaDato
    reg = _reg_estado(d, estado)
    x0 = d.get("x0", estado.get("x0"))
    if x0 is None:
        raise FaltaDato("Falta el valor x₀ para el pronóstico")
    _asegurar_validacion(reg, d, alpha, res, estado)
    ny, uy, nx, ux = _vars(d)
    estado["x0"] = x0
    estado["individual"] = d.get("individual", estado.get("individual", True))
    ey = d.get("escala_y", 1.0) if d.get("mostrar_escala_y") else 1.0  # 10^5 m³ → m³; 'millones' se deja así
    ent = _entorno(d, reg)
    if ent and not ent[0] <= x0 <= ent[1]:
        res.avisos.append(f"x₀ = {fmt(x0, 4)} está FUERA del entorno observado ({_el(nx)} entre {fmt(ent[0], 4)} y "
                          f"{_con(fmt(ent[1], 4), ux)}): es extrapolar. El modelo solo se validó en ese entorno y el error "
                          "crece mucho al alejarse; decirlo en la respuesta.")
    y0 = reg.predecir(x0)
    res.pasos.append(f"**Recta**: {_coma(reg.ecuacion())}.")
    res.pasos.append(f"**Estimador puntual**: ŷ₀ = b0 + b1·x₀ = {fmt(reg.b0, 4)} + ({fmt(reg.b1, 4)})·{fmt(x0, 4)} = {fmt(y0, 4)}"
                     + (f" (= {fmt(reg.a_original(y0), 4)} en la escala original)" if reg.modelo != "lineal" else "")
                     + (f" → {fmt(y0 * ey, 2)} en unidades" if ey != 1 else "") + ".")
    res.numeros += [y0, reg.a_original(y0), y0 * ey]
    if d.get("puntual"):
        res.resumen = f"ŷ₀ = {fmt(y0, 6)}"
        res.conclusion = (f"El pronóstico puntual de {_el(ny)} para {_el(nx)} = {_con(fmt(x0, 4), ux)} es "
                          f"ŷ₀ = {_con(fmt(reg.a_original(y0), 6), uy)}.")
        return
    individual = estado["individual"]
    cola = d.get("cola", "bilateral")
    f = rg.ic_prediccion if individual else rg.ic_media_y
    ic = f(reg, x0, alpha, cola)
    que = ("un valor individual de y (intervalo de predicción o pronóstico)" if individual else
           "el valor promedio de y, E(y | x₀) (ley promedio)")
    raiz = "1 + 1/n + (x₀ - x̄)²/(Σx² - n·x̄²)" if individual else "1/n + (x₀ - x̄)²/(Σx² - n·x̄²)"
    tq = "t(1-α/2; ν)" if cola == "bilateral" else "t(1-α; ν)"
    A, B = ic.A, ic.B
    uno = "1 + " if individual else ""
    res.pasos.append(f"**Intervalo para {que}**: ŷ₀ ± {tq}·S·√({raiz}); {tq} = {fmt(ic.critico, 4)} (ν = n - 2 = "
                     f"{reg.nu}); error = {fmt(ic.critico, 4)}·{fmt(reg.S, 6)}·√({uno}1/{reg.n} + ({fmt(x0, 4)} - "
                     f"{fmt(reg.xbar, 6)})²/{fmt(reg.Sxx, 4)}) = {fmt(ic.error, 4)}.")
    if cola == "bilateral" and A is not None and B is not None:
        res.pasos.append(f"**Límites**: ŷ₀ ∓ error = {fmt(y0, 4)} ∓ {fmt(ic.error, 4)} = {fmt(A, 4)} ; {fmt(B, 4)}.")
    A, B = ic.A, ic.B
    lim = [v for v in (A, B) if v is not None]
    res.numeros += lim + [ic.error] + [v * ey for v in lim]
    texto_lim = (f"[{fmt(A, 4)} ; {fmt(B, 4)}]" if cola == "bilateral" else
                 (f"mínimo {fmt(A, 4)}" if cola == "inferior" else f"máximo {fmt(B, 4)}"))
    transformada = reg.modelo != "lineal" and rg.TRANSFORMACIONES[reg.modelo][0].startswith("ln")
    if transformada:
        Ao, Bo = ic.A_orig, ic.B_orig
        res.numeros += [v for v in (Ao, Bo) if v is not None]
        res.pasos.append(f"**Antitransformando** (e^límite): " + (f"[{fmt(Ao, 4)} ; {fmt(Bo, 4)}]" if cola == "bilateral"
                                                                   else fmt(Ao if Ao is not None else Bo, 4)) + ".")
        texto_lim += " → " + (f"[{fmt(Ao, 4)} ; {fmt(Bo, 4)}]" if cola == "bilateral" else fmt(Ao if Ao is not None else Bo, 4))
    if ey != 1:
        res.pasos.append(f"**En unidades**: × {fmt(ey)} → " + " ; ".join(fmt(v * ey, 2) for v in lim) + ".")
    res.resumen = f"ŷ₀ = {fmt(y0, 4)}; {texto_lim}"
    conf = fmt(100 * (1 - alpha), 2)
    sujeto = f"el valor de {_el(ny)}" if individual else f"{_el(ny)} promedio"
    simbolo = f"y(x₀ = {fmt(x0, 4)})" if individual else f"E(y | x₀ = {fmt(x0, 4)})"
    donde = f"con {_el(nx)} en {_con(fmt(x0, 4), ux)}" if nx != "x" else f"para x₀ = {fmt(x0, 4)}"
    if cola == "bilateral":
        a_, b_ = (ic.A_orig, ic.B_orig) if transformada else (A, B)
        ar, br, nota = redondeo.intervalo(a_, b_, 4)
        res.conclusion = (f"Con un {conf}% de confianza, {sujeto} {donde} {_v(ny, 'estará') if not individual else 'estará'} entre {_con(ar, uy)} y "
                          f"{_con(br, uy)}: P({ar} ≤ {simbolo} ≤ {br}) = {fmt(1 - alpha, 4)}{nota}.")
    else:
        v = A if cola == "inferior" else B
        if transformada:
            v = ic.A_orig if cola == "inferior" else ic.B_orig
        res.conclusion = (f"Con un {conf}% de confianza el valor {'mínimo' if cola == 'inferior' else 'máximo'} de "
                          f"{sujeto} {donde} es {_con(redondeo.cota(v, cola != 'inferior', 4), uy)}" +
                          (f" ({redondeo.cota(v * ey, cola != 'inferior', 2)} en unidades)" if ey != 1 else "") +
                          f" (redondeado hacia {'abajo' if cola == 'inferior' else 'arriba'}; sin redondear {fmt(v, 6)}).")


def ic_coef(d, alpha, res, estado):
    reg = _reg_estado(d, estado)
    _asegurar_validacion(reg, d, alpha, res, estado)
    ny, uy, nx, ux = _vars(d)
    ub1 = _u_b1(uy, ux) if reg.modelo == "lineal" else ""
    conf = fmt(100 * (1 - alpha), 2)
    cola = d.get("cola")
    if cola in ("superior", "inferior"):
        ic = rg.ic_beta1(reg, alpha, cola)
        lim, op = (ic.B, "+") if cola == "superior" else (ic.A, "-")
        signo = "≤" if cola == "superior" else "≥"
        c = redondeo.cota(lim, cola == "superior", 4)
        res.pasos.append(f"**Recta**: {_coma(reg.ecuacion())}; Sb1 = {fmt(reg.Sb1, 4)}.")
        res.pasos.append(f"**Límite {cola} para β1** (unilateral, α entero en una cola): b1 {op} t(1-α; ν = {reg.nu})·Sb1 "
                         f"= {fmt(reg.b1, 4)} {op} {fmt(ic.critico, 4)}·{fmt(reg.Sb1, 4)} = {fmt(lim, 4)}.")
        res.numeros += [reg.b1, lim, ic.error, ic.critico]
        res.resumen = f"β1 {signo} {fmt(lim, 4)}"
        res.conclusion = (f"Con un {conf}% de confianza, {_por_cada(nx, ux)} el cambio de {_el(ny)} es como "
                          f"{'máximo' if cola == 'superior' else 'mínimo'} {_con(c, ub1)}: "
                          f"P(β1 {signo} {c}) = {fmt(1 - alpha, 4)} (sin redondear {fmt(lim, 6)}).")
        return
    ic = rg.ic_beta1(reg, alpha)
    res.pasos.append(f"**Recta**: {_coma(reg.ecuacion())}; Sb1 = {fmt(reg.Sb1, 4)}.")
    res.pasos.append(f"**IC para β1**: b1 ± t(1-α/2; ν = n - 2 = {reg.nu})·Sb1 = {fmt(reg.b1, 4)} ± {fmt(ic.critico, 4)}·"
                     f"{fmt(reg.Sb1, 4)} = [{fmt(ic.A, 4)} ; {fmt(ic.B, 4)}]"
                     + (" (con valores negativos, A es el MÁS negativo)" if ic.B < 0 else "") + ".")
    res.numeros += [reg.b1, ic.A, ic.B, ic.error, ic.critico]
    res.resumen = f"β1 ∈ [{fmt(ic.A, 4)} ; {fmt(ic.B, 4)}]"
    ar, br, nota = redondeo.intervalo(ic.A, ic.B, 4)
    if ic.B < 0:
        cambio = f"{_el(ny)} {_v(ny, 'disminuye')} entre {redondeo.cota(-ic.B, False, 4)} y {_con(redondeo.cota(-ic.A, True, 4), uy)}"
    elif ic.A > 0:
        cambio = f"{_el(ny)} {_v(ny, 'aumenta')} entre {ar} y {_con(br, uy)}"
    else:
        cambio = f"{_el(ny)} {_v(ny, 'cambia')} entre {ar} y {_con(br, uy)}"
    res.conclusion = (f"Con un {conf}% de confianza, {_por_cada(nx, ux)}, {cambio}: P({ar} ≤ β1 ≤ {br}) = "
                      f"{fmt(1 - alpha, 4)}" + (f" (β1 en {ub1})" if ub1 else "") + f"{nota}.")


def _ic_rho(reg, alpha, res):
    ic = rg.ic_rho(reg, alpha)
    z = atanh(reg.r)
    res.pasos.append(f"**Fisher** (r no es normal si ρ ≠ 0): Zρ = ½·ln((1+r)/(1-r)) = {fmt(z, 4)}; "
                     f"Z(1-α/2)·√(1/(n-3)) = {fmt(ic.critico, 4)}·√(1/{reg.n - 3}) = {fmt(ic.error, 4)}; "
                     f"Zρmín = {fmt(z - ic.error, 4)}; Zρmáx = {fmt(z + ic.error, 4)}.")
    res.pasos.append(f"**Límites del IC de ρ** (todavía no de ρ²): A = (e^(2Zρmín) - 1)/(e^(2Zρmín) + 1) = "
                     f"{fmt(ic.A, 4)}; B = (e^(2Zρmáx) - 1)/(e^(2Zρmáx) + 1) = {fmt(ic.B, 4)}.")
    res.numeros += [reg.r, z, 2 * z, ic.error, z - ic.error, z + ic.error, ic.A, ic.B]
    return ic


def ic_rho(d, alpha, res, estado):
    reg = _reg_estado(d, estado)
    _asegurar_validacion(reg, d, alpha, res, estado)
    ny, _, nx, _ = _vars(d)
    res.pasos.append(f"**Coeficiente de correlación**: r = {fmt(reg.r, 4)} (n = {reg.n}); lleva el signo de b1.")
    ic = _ic_rho(reg, alpha, res)
    ar, br, nota = redondeo.intervalo(ic.A, ic.B, 4)
    res.resumen = f"ρ ∈ [{fmt(ic.A, 4)} ; {fmt(ic.B, 4)}]"
    res.conclusion = (f"Con un {fmt(100 * (1 - alpha), 2)}% de confianza, la fuerza de la relación entre {_el(nx)} y {_el(ny)} "
                      f"(coeficiente de correlación poblacional) está entre {ar} y {br}: P({ar} ≤ ρ ≤ {br}) = "
                      f"{fmt(1 - alpha, 4)}{nota}.")


def ic_rho2(d, alpha, res, estado):
    reg = _reg_estado(d, estado)
    if not d.get("rho2"):   # dentro de la recta ya se validó
        _asegurar_validacion(reg, d, alpha, res, estado, medida=True)
    ny, _, nx, _ = _vars(d)
    res.pasos.append(f"**Coeficiente de determinación**: r² = {fmt(reg.r2, 4)} ({fmt(100 * reg.r2, 2)}% de influencia "
                     f"de {_el(nx)} en {_el(ny)}).")
    ic = _ic_rho(reg, alpha, res)
    a2, b2 = sorted((ic.A ** 2, ic.B ** 2)) if ic.A * ic.B > 0 else (0.0, max(ic.A ** 2, ic.B ** 2))
    ar, br, nota = redondeo.intervalo(a2, b2, 4)
    res.pasos.append(f"**IC para ρ²**: los límites del IC de ρ al cuadrado → [{fmt(a2, 4)} ; {fmt(b2, 4)}]"
                     + (f" (el IC de ρ incluye el 0, así que el mínimo de ρ² es 0; el máximo es "
                        f"{fmt(max(abs(ic.A), abs(ic.B)), 4)}² = {fmt(b2, 4)})" if ic.A * ic.B <= 0 else "") + ".")
    res.numeros += [reg.r2, a2, b2, 100 * a2, 100 * b2]
    res.resumen = f"r² = {fmt(reg.r2, 4)}; ρ² ∈ [{fmt(a2, 4)} ; {fmt(b2, 4)}]"
    pa, pb = redondeo.cota(100 * a2, False, 2), redondeo.cota(100 * b2, True, 2)
    res.conclusion = (f"{_El(nx)} {_v(nx, 'influye')} en un {fmt(100 * reg.r2, 2)}% (aprox.) en {_el(ny)}; con un "
                      f"{fmt(100 * (1 - alpha), 2)}% de confianza, la influencia real está entre el {pa}% y el {pb}%: "
                      f"P({ar} ≤ ρ² ≤ {br}) = {fmt(1 - alpha, 4)}{nota}."
                      + (" Ese r² no alcanza el mínimo del uso del problema: el modelo no se valida, y r² se informa "
                         "como la medida de la fuerza de la relación." if not estado.get("valido", True) else "")
                      + (f" El intervalo es muy ancho porque hay pocos datos (n = {reg.n})." if reg.n < 10 else ""))


def _afirmacion_b1(b10: float, tail: str, ny: str, nx: str, ux: str, uy: str) -> str:
    """'por cada mm adicional de x, y disminuye en más de 0,25 MPa' (lo que se quiere probar, en palabras)."""
    v = _con(fmt(abs(b10), 4), uy)
    dis, aum = _v(ny, "disminuye"), _v(ny, "aumenta")
    if tail == "izquierda":
        que = f"{dis} en más de {v}" if b10 <= 0 else f"{aum} en menos de {v}"
    else:
        que = f"{aum} en más de {v}" if b10 >= 0 else f"{dis} en menos de {v}"
    return f"{_por_cada(nx, ux)}, {_el(ny)} {que}"


def ensayo_coef(d, alpha, res, estado):
    from .resolver import FaltaDato
    reg = _reg_estado(d, estado)
    if d.get("beta10") is None:
        raise FaltaDato("Falta el valor de referencia β1₀ de la afirmación")
    _asegurar_validacion(reg, d, alpha, res, estado)
    ny, uy, nx, ux = _vars(d)
    ub1 = _u_b1(uy, ux) if reg.modelo == "lineal" else ""
    b10, tail = d["beta10"], d.get("tail", "derecha")
    if tail == "bilateral":
        res.avisos.append("En β1 no hay ensayo bilateral (profesor, 05/11): se prueba que la pendiente es mayor o menor "
                          "que un valor. Corregí la cola.")
    e = rg.ensayo_beta1(reg, alpha, b10, tail)
    afirmacion = _afirmacion_b1(b10, tail, ny, nx, ux, uy)
    res.pasos.append(f"**Recta**: {_coma(reg.ecuacion())}; Sb1 = {fmt(reg.Sb1, 4)}; ν = n - 2 = {reg.nu}.")
    res.pasos.append(f"**Hipótesis**: se quiere probar que {afirmacion} ⇒ va en H1. H0: {_coma(e.h0)}  vs  "
                     f"H1: {_coma(e.h1)}" + (f" (β1 en {ub1})" if ub1 else "") + f"; α = {fmt(alpha, 4)}."
                     + (" Ojo con el signo: «disminuye en más» es MÁS negativo." if b10 < 0 else ""))
    bc = e.b_critico[0] if e.b_critico else b10
    signo = "+" if tail == "derecha" else "-"
    res.pasos.append(f"**Valor crítico** (antes de mirar b1): b1c = β1₀ {signo} t(1-α; ν)·Sb1 = {fmt(b10, 4)} {signo} "
                     f"{fmt(e.t_critico, 4)}·{fmt(reg.Sb1, 4)} = {_con(fmt(bc, 4), ub1)}.")
    cond = ">" if tail == "derecha" else "<"
    res.pasos.append(f"**Condición de rechazo**: si b1 {cond} {fmt(bc, 4)} ⇒ se rechaza H0. b1 = {fmt(reg.b1, 4)} ⇒ "
                     + ("se rechaza H0." if e.rechaza else "no se rechaza H0."))
    res.numeros += [reg.b1, bc, e.t_critico, e.t_c, reg.Sb1]
    res.resumen = f"b1 = {fmt(reg.b1, 4)} vs b1c = {fmt(bc, 4)}: " + ("RECHAZA H0" if e.rechaza else "NO rechaza H0")
    res.conclusion = (f"Con α = {fmt(alpha, 4)}, b1 = {fmt(reg.b1, 4)} " +
                      ("cae en la zona de rechazo ⇒ se rechaza H0: se puede asegurar que " if e.rechaza else
                       "no cae en la zona de rechazo ⇒ no se rechaza H0: no hay evidencia suficiente para asegurar que ")
                      + afirmacion + ".")


def transformado(d, alpha, res, estado):
    modelo = d.get("modelo") or "loglog"
    lin = estado.get("reg") if estado.get("reg") and estado["reg"].modelo == "lineal" else _reg(d, modelo="lineal", origen=False)
    reg = _reg(d, modelo=modelo, origen=False)
    _pasos_recta(reg, res, d)
    res.pasos.append(f"**Comparación**: r lineal = {fmt(lin.r, 4)} (r² = {fmt(lin.r2, 4)}); r {modelo} = {fmt(reg.r, 4)} "
                     f"(r² = {fmt(reg.r2, 4)}).")
    e = _validacion(reg, alpha, res, d)
    mejor = reg.r2 > lin.r2
    estado["reg"] = reg
    estado["validada"], estado["valido"] = reg, _valido(e, reg, d)
    res.resumen = f"{_coma(reg.ecuacion())}; r = {fmt(reg.r, 4)} vs lineal {fmt(lin.r, 4)}"
    nombres = {"loglog": "doble logarítmico", "loglin": "logarítmico lineal", "linlog": "lineal logarítmico",
               "inversa": "inverso"}
    concl = (f"El modelo {nombres.get(modelo, modelo)} "
             f"{'ajusta mejor' if mejor else 'no ajusta mejor'} que el lineal (r² {fmt(reg.r2, 4)} vs {fmt(lin.r2, 4)}). "
             + _interpretar(reg, d))
    # si antes se pidió un pronóstico, se repite con este modelo
    if estado.get("x0") is not None:
        sub = type(res)()
        d2 = dict(d, x0=estado["x0"], individual=estado.get("individual", True))
        try:
            pronostico(d2, alpha, sub, estado)
            res.pasos.append("**Pronóstico con este modelo**:")
            res.pasos += sub.pasos
            res.numeros += sub.numeros
            concl += " " + sub.conclusion
        except Exception:  # noqa: BLE001
            pass
    res.conclusion = concl


def origen(d, alpha, res, estado):
    reg = _reg(d, origen=True)
    _pasos_recta(reg, res, d)
    res.resumen = _coma(reg.ecuacion())
    res.conclusion = (f"Con intercepto 0 el modelo es {_coma(reg.ecuacion())}. " + _interpretar(reg, d) +
                      " Solo conviene si el entorno de observación está cerca de x = 0.")
    estado["reg"] = reg


# ---------------------------------------------------------------- resolución (múltiple)

def _xs(d):
    from .resolver import FaltaDato
    if not d.get("xs") or not d.get("y"):
        raise FaltaDato("Faltan los datos de la tabla (variables explicativas e y)")
    nombres = d.get("nombres_x") or []
    if len(nombres) != len(d["xs"]):
        nombres = [f"x{i + 1}" for i in range(len(d["xs"]))]
    return d["xs"], d["y"], nombres


def _pasos_multiple(reg: rg.RegresionMultiple, alpha, res, titulo="Modelo"):
    g = rg.ensayo_global(reg, alpha)
    parc = rg.ensayos_parciales(reg, alpha)
    res.pasos.append(f"**{titulo}**: {_coma(reg.ecuacion())}  (n = {reg.n}, k = {reg.k}, p = {reg.p}).")
    res.pasos.append(f"**Ajuste**: S² = SCR/(n-p) = {fmt(reg.S2, 4)}; S = {fmt(reg.S, 4)}; R² = {fmt(reg.R2, 4)}; "
                     f"R² ajustado = 1 - (1-R²)·(n-1)/(n-p) = {fmt(reg.R2aj, 4)}.")
    res.pasos.append(f"**Análisis global** (dato informativo; H0: β1 = ... = βk = 0): Fc = (R²/k)/((1-R²)/(n-p)) = "
                     f"{fmt(g.F_c, 4)}; F(1-α; {g.nu1}; {g.nu2}) = {fmt(g.F_critico, 4)} ⇒ "
                     + ("se rechaza H0." if g.rechaza else "no se rechaza H0.")
                     + " El profesor (05/11): el análisis global «no sirve», no evalúa cada variable; lo que decide es "
                       "el análisis individual.")
    filas = ["| Variable | bi | Cii | Sbi = S·√Cii | tc = bi/Sbi | ¿aporta? |", "|---|---|---|---|---|---|"]
    for i, e in enumerate(parc):
        filas.append(f"| {e.nombre} | {fmt(e.b, 4)} | {fmt(reg.C[i + 1], 6)} | {fmt(e.Sb, 4)} | {fmt(e.t_c, 4)} | "
                     f"{'sí' if e.rechaza else 'no'} |")
    res.pasos.append(f"**Análisis individual** (H0: βi = 0; se rechaza si |tc| > t(1-α; n-p) = {fmt(parc[0].t_critico, 4)}):\n\n"
                     + "\n".join(filas))
    res.numeros += reg.b + [reg.S, reg.S2, reg.R2, reg.R2aj, g.F_c, g.F_critico, parc[0].t_critico] + reg.C[1:] + \
        [e.t_c for e in parc] + reg.Sb[1:]
    return g, parc


def multiple(d, alpha, res, estado):
    xs, y, nombres = _xs(d)
    reg = rg.ajustar_multiple(xs, y, nombres)
    g, parc = _pasos_multiple(reg, alpha, res)
    parciales = rg.determinacion_parcial(xs, y, nombres)
    res.pasos.append("**Coeficientes de determinación parcial** (aporte de cada variable cuando están las demás): "
                     + "; ".join(f"R²({k}) = {fmt(v, 4)}" for k, v in parciales.items()) + ".")
    res.numeros += list(parciales.values())
    simples = []
    for xi, nom in zip(xs, nombres):
        rs = rg.ajustar_simple(xi, y)
        simples.append(f"ŷ = {fmt(rs.b0, 4)} {'+' if rs.b1 >= 0 else '-'} {fmt(abs(rs.b1), 4)}·{nom} (r² = {fmt(rs.r2, 4)})")
        res.numeros += [rs.b0, rs.b1, rs.r2]
    res.pasos.append("**Modelos simples** (para los coeficientes parciales, R²(xi) = (R² - r²sin xi)/(1 - r²sin xi)): "
                     + "; ".join(simples) + ".")
    aportan = [e.nombre for e in parc if e.rechaza]
    estado["regm"] = reg
    res.resumen = f"{_coma(reg.ecuacion(4))}; R² = {fmt(reg.R2, 4)}; F {'RECHAZA' if g.rechaza else 'NO rechaza'}"
    no_aportan = [e.nombre for e in parc if not e.rechaza]
    if not no_aportan:
        concl = "Todas las variables aportan significativamente a la explicación de Y (análisis individual)."
    elif aportan:
        concl = (f"En el análisis individual solo {', '.join(aportan)} aporta(n) explicación; {', '.join(no_aportan)} "
                 "no: hay que sacarla(s) del modelo (análisis de sensibilidad / selección de modelos).")
    else:
        concl = "Ninguna variable aporta explicación en el análisis individual: el modelo no es adecuado para explicar Y."
    concl += f" (Análisis global: F {'rechaza' if g.rechaza else 'no rechaza'} H0, solo como dato.)"
    res.conclusion = concl + f" R² = {fmt(reg.R2, 4)}, R² ajustado = {fmt(reg.R2aj, 4)}."


def seleccion(d, alpha, res, estado):
    xs, y, nombres = _xs(d)
    cands = rg.seleccion_modelos(xs, y, nombres)
    filas = ["| Modelo | p | R² aj | S² | PRESS | DET | Cp | Cp/p | VIF máx | ¿pasa DET y Cp? |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for c in sorted(cands, key=lambda c: (len(c.variables), c.variables)):
        filas.append(f"| {', '.join(c.variables)} | {c.p} | {fmt(c.R2aj, 4)} | {fmt(c.S2, 4)} | {fmt(c.PRESS, 4)} | "
                     f"{fmt(c.DET, 4)} | {fmt(c.Cp, 3)} | {fmt(c.Cp_p, 3)} | {fmt(c.VIF_max, 3)} | {'sí' if c.cumple else 'no'} |")
    res.pasos.append(f"**Análisis exploratorio**: {len(cands)} modelos candidatos (2^k - 1). Se descartan los que tienen "
                     "DET ≤ 0,1 o Cp/p ≥ 5; entre los demás, R² ajustado alto, S² y PRESS bajos y el más simple "
                     "(parsimonia).\n\n" + "\n".join(filas))
    res.numeros += [float(len(cands))]
    # confirmatorio: el mejor cuyo análisis individual pase para todas sus variables
    validos = [c for c in cands if c.cumple]
    orden = sorted(validos or cands, key=lambda c: (-round(c.R2aj, 3), c.p, c.PRESS))
    elegido = None
    for c in orden:
        if all(e.rechaza for e in rg.ensayos_parciales(c.reg, alpha)):
            elegido = c
            break
    elegido = elegido or orden[0]
    descartados = [", ".join(c.variables) for c in cands if not c.cumple]
    if descartados:
        res.pasos.append("**Descartados por DET o Cp**: " + "; ".join(descartados) + ".")
    _pasos_multiple(elegido.reg, alpha, res, titulo="Modelo elegido (análisis confirmatorio)")
    estado["regm"] = elegido.reg
    res.resumen = f"mejor: {', '.join(elegido.variables)} → {_coma(elegido.reg.ecuacion(4))}"
    res.conclusion = (f"El modelo más adecuado es el que contiene a {', '.join(elegido.variables)}: "
                      f"{_coma(elegido.reg.ecuacion(4))} (R² ajustado = {fmt(elegido.R2aj, 4)}); sus variables aportan "
                      "significativamente a la explicación de Y.")


def submodelo(d, alpha, res, estado):
    from .resolver import FaltaDato
    xs, y, nombres = _xs(d)
    idx = [int(i) - 1 for i in d.get("variables", []) if 0 < i <= len(xs)]
    if not idx:
        raise FaltaDato("Indicá las variables del modelo reducido")
    comp = rg.ajustar_multiple(xs, y, nombres)
    red = rg.ajustar_multiple([xs[i] for i in idx], y, [nombres[i] for i in idx])
    _pasos_multiple(comp, alpha, res, titulo="Modelo completo")
    _, parc = _pasos_multiple(red, alpha, res, titulo="Modelo reducido")
    def valido(reg):
        return rg.ensayo_global(reg, alpha).rechaza and all(e.rechaza for e in rg.ensayos_parciales(reg, alpha))
    if valido(comp) != valido(red):
        mejor = comp if valido(comp) else red
        motivo = "es el único válido (análisis global y todas sus variables significativas)"
    else:
        mejor = red if (red.R2aj >= comp.R2aj or not valido(comp)) else comp
        motivo = ("tiene mayor R² ajustado" if mejor.R2aj >= max(red.R2aj, comp.R2aj) else
                  "es más simple (parsimonia) y el completo no es válido")
    no_aportan = [e.nombre for e in parc if not e.rechaza]
    concl = (f"R² ajustado: {fmt(red.R2aj, 4)} el reducido vs {fmt(comp.R2aj, 4)} el completo; S²: "
             f"{fmt(red.S2, 4)} vs {fmt(comp.S2, 4)}. Conviene el modelo {'reducido' if mejor is red else 'completo'} "
             f"porque {motivo}.")
    if no_aportan and mejor is red:
        quedan = [i for i, e in zip(idx, parc) if e.rechaza]
        concl += f" Pero {', '.join(no_aportan)} no aporta explicación"
        if quedan:
            fin = rg.ajustar_multiple([xs[i] for i in quedan], y, [nombres[i] for i in quedan])
            res.numeros += fin.b
            concl += f": el modelo válido es {_coma(fin.ecuacion(4))}."
        else:
            concl += "."
    res.resumen = f"reducido R²aj = {fmt(red.R2aj, 4)} vs completo {fmt(comp.R2aj, 4)}"
    res.conclusion = concl


# ---------------------------------------------------------------- registro

def _envolver(f):
    """Toda salida de regresión pasa por las contracciones del castellano ('de el PBI' → 'del PBI')."""
    def g(d, alpha, res, estado):
        f(d, alpha, res, estado)
        res.conclusion = _contraer(res.conclusion)
        res.pasos = [_contraer(x) for x in res.pasos]
        res.avisos = [_contraer(x) for x in res.avisos]
    g.__name__ = f.__name__
    return g


for tema in ("regresion", "regresion_multiple"):
    EXTENSIONES[tema] = (completar_planteo, clasificar)
for tipo, f in (("recta", recta), ("validacion", validacion), ("pronostico", pronostico), ("ic_coef", ic_coef),
                ("ic_rho", ic_rho), ("ic_rho2", ic_rho2), ("ensayo_coef", ensayo_coef),
                ("transformado", transformado), ("origen", origen)):
    DESPACHO_EXTRA[("regresion", tipo)] = _envolver(f)
for tipo, f in (("multiple", multiple), ("seleccion", seleccion), ("submodelo", submodelo)):
    DESPACHO_EXTRA[("regresion_multiple", tipo)] = _envolver(f)
