"""Contrastes χ² (TEMA VI) a partir de las tablas del enunciado.

- Tabla de contingencia / homogeneidad: arma la tabla de frecuencias observadas sacando columnas de
  etiquetas, índices (Planta 1, 2, 3...), filas/columnas de totales, y convirtiendo "muestra + defectuosas"
  en (defectuosas, no defectuosas).
- Bondad de ajuste: reconoce la tabla de frecuencias (clases "20-30" o valores 0, 1, 2...), el modelo
  pedido en cada inciso (Normal, Poisson, Gumbel, Weibull, Pareto, Log-Normal...) y sus parámetros
  dados en el texto; los que faltan se estiman con la muestra (cada uno resta un grado de libertad).
"""

import re
from typing import Dict, List, Optional, Tuple

from solver import ajuste as aj
from solver import wording

from .analizador import _hay, clasificar_inciso
from .modelo import DESPACHO_EXTRA, EXTENSIONES, Analisis, Evidencia, Inciso
from .tablas import RE_INTERVALO, es_tabla_de_clases, limites_de_clase
from .texto import Numero, buscar_numeros, fmt, normalizar

# ---------------------------------------------------------------- contingencia

RE_TOTAL = r"\btotal"
RE_COL_MUESTRA = r"(muestra|total|postes|unidades|tamano|inspeccionad|produccion|revisad|analizad|cantidad de piezas)"
RE_COL_INDICE = r"^(planta|semana|turno|local|zona|muestra n|n[º°o]|dia|lote|grupo|maquina|proveedor|area)\b"


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _etiquetas_filas(tabla: dict, filas: list) -> Tuple[Optional[str], Optional[List[str]]]:
    """(encabezado, nombre de cada fila): la primera columna de texto o la columna índice (Planta 1, 2, 3)."""
    for j, cab in enumerate(tabla["columnas"]):
        col = [f[j] if j < len(f) else None for f in filas]
        if all(isinstance(v, str) and v.strip() for v in col):
            return cab, [v.strip() for v in col]
        if _hay(RE_COL_INDICE, normalizar(cab or "")) and col == [float(i) for i in range(1, len(col) + 1)]:
            return cab, [f"{cab} {i}" for i in range(1, len(col) + 1)]
    return None, None


def _nombre_resto(cabeceras: List[str]) -> str:
    """Columna de los que NO tienen el atributo (muestra - resto)."""
    if len(cabeceras) == 1 and cabeceras[0]:
        c = cabeceras[0].strip()
        if c.startswith("Con "):
            return "Sin " + c[4:]
        return "No " + c[0].lower() + c[1:]
    return "Resto de la muestra"


def _nombre_atributo(cabecera: str) -> str:
    """'% de los 300 reclamos' → 'Con reclamo' (la columna de % pasada a cantidades); las demás quedan igual."""
    limpio = re.sub(r"^%\s*(de\s+)?(los|las)?\s*[\d.]*\s*", "", cabecera or "").strip()
    if limpio == (cabecera or "").strip() or not limpio:
        return cabecera
    return "Con " + re.sub(r"(?<=[aeiou])s$", "", limpio.lower())


def tabla_contingencia_de(tabla: dict) -> Optional[dict]:
    """{"tabla", "nota", "filas", "columnas", "nombre_filas", "grupos"} o None.

    "grupos" dice qué dimensión son muestras separadas de tamaño fijado (prueba de homogeneidad): "filas" si hay
    una columna con el tamaño de cada muestra, "columnas" si hay una fila de totales de muestra."""
    cols = [normalizar(c or "") for c in tabla["columnas"]]
    totales = [f for f in tabla["filas"] if isinstance(f[0], str) and _hay(RE_TOTAL, normalizar(f[0]))]
    filas = [f for f in tabla["filas"] if f not in totales]
    if len(filas) < 2:
        return None
    k = len(cols)
    usar = []
    for j in range(k):
        col = [f[j] if j < len(f) else None for f in filas]
        if not all(_num(v) for v in col):
            continue  # etiquetas
        if _hay(RE_TOTAL, cols[j]):
            continue
        if _hay(RE_COL_INDICE, cols[j]) and col == [float(i) for i in range(1, len(col) + 1)]:
            continue  # columna índice (Planta 1, 2, 3, 4)
        usar.append(j)
    if len(usar) < 1:
        return None
    nombre_filas, etq_filas = _etiquetas_filas(tabla, filas)
    grupos = None
    if any(_hay(r"muestra", normalizar(f[0])) for f in totales):
        grupos = "columnas"   # 'Totales de Muestra': cada columna es una muestra
    elif any(_hay(RE_TOTAL, c) and _hay(r"muestra", c) for c in cols):
        grupos = "filas"
    nota = []
    # columna de tamaños de muestra: la que en cada fila es >= la suma de las otras
    muestra = [j for j in usar if _hay(RE_COL_MUESTRA, cols[j])]
    if muestra:
        jm = muestra[0]
        otras = [j for j in usar if j != jm]
        # porcentajes "de los 300 reclamos" → cantidades
        for j in otras:
            m = re.search(r"%[^0-9]*?(\d[\d.]*)", tabla["columnas"][j] or "")
            if m:
                base = float(m.group(1).replace(".", ""))
                for f in filas:
                    f[j] = f[j] * base / 100
                nota.append(f"la columna «{tabla['columnas'][j]}» se pasó de % a cantidades (× {fmt(base)} / 100)")
        if otras and all(f[jm] >= sum(f[j] for j in otras) - 1e-9 for f in filas):
            resto = [f[jm] - sum(f[j] for j in otras) for f in filas]
            hay_resto = any(r > 0 for r in resto)
            obs = [[f[j] for j in otras] + ([r] if hay_resto else []) for f, r in zip(filas, resto)]
            nota.append(f"la columna «{tabla['columnas'][jm]}» es el tamaño de cada muestra: se agrega la columna "
                        "de los que no tienen el atributo (muestra - resto)")
            etq_cols = [_nombre_atributo(tabla["columnas"][j]) for j in otras]
            etq_cols += [_nombre_resto(etq_cols)] if hay_resto else []
            return {"tabla": obs, "nota": "; ".join(nota), "filas": etq_filas, "columnas": etq_cols,
                    "nombre_filas": nombre_filas, "grupos": "filas"}
    obs = [[float(f[j]) for j in usar] for f in filas]
    if len(usar) < 2:
        return None
    return {"tabla": obs, "nota": "; ".join(nota), "filas": etq_filas, "columnas": [tabla["columnas"][j] for j in usar],
            "nombre_filas": nombre_filas, "grupos": grupos}


def guardar_etiquetas(an: Analisis, filas=None, columnas=None, nombre_filas=None, grupos=None):
    """Nombres de filas y columnas de la tabla observada (para las tablas de la resolución y la hipótesis)."""
    for clave, v in (("tabla_filas", filas), ("tabla_columnas", columnas), ("tabla_nombre_filas", nombre_filas),
                     ("chi_grupos", grupos)):
        if v:
            an.datos[clave] = v
        else:
            an.datos.pop(clave, None)


def completar_contingencia(an: Analisis, t):
    for tabla in an.tablas:
        r = tabla_contingencia_de({"columnas": list(tabla["columnas"]), "filas": [list(f) for f in tabla["filas"]]})
        if r:
            an.datos["tabla"] = r["tabla"]
            guardar_etiquetas(an, r["filas"], r["columnas"], r["nombre_filas"], r["grupos"])
            an.evidencias.append(Evidencia("tabla", r["tabla"], "", "tabla del enunciado" +
                                           (f" ({r['nota']})" if r["nota"] else "")))
            return


RE_DEPENDENCIA = r"(depend|independ|asocia|relacion entre)"
RE_MUESTRAS_POR_GRUPO = r"muestras? (aleatorias? |semanales |diarias )?(de|sobre) \d|sobre (una muestra de )?\d+ (piezas|unidades)"


def diseno_contingencia(texto_norm: str, grupos: Optional[str]) -> str:
    """'independencia' (una sola muestra clasificada por dos variables: H0 «son independientes») u
    'homogeneidad' (una muestra de tamaño fijado por grupo: H0 «las proporciones son iguales en todos los grupos»,
    las «Pruebas de Consistencia» de la guía). Si el enunciado pregunta por dependencia / asociación manda eso."""
    if _hay(RE_DEPENDENCIA, texto_norm):
        return "independencia"
    if grupos or _hay(RE_MUESTRAS_POR_GRUPO, texto_norm):
        return "homogeneidad"
    return "independencia"


# ---------------------------------------------------------------- bondad de ajuste

MODELOS = [
    ("gumbel_min", r"gumbel del? (minimo|min)\b"),
    ("gumbel_max", r"gumbel del? (maximo|max)\b"),
    ("weibull", r"weibull"),
    ("pareto", r"pareto"),
    ("lognormal", r"log[- ]?normal"),
    ("normal", r"(?<!log-)(?<!log )(?<!log)\bnormal(es|mente)?\b"),
    ("poisson", r"poisson"),
    ("binomial", r"binomial"),
    ("exponencial", r"exponencial"),
    ("gamma", r"\bgamma\b"),
    ("uniforme", r"uniforme|igualmente distribuid|por igual|equitativ|\bdado\b|ruleta"),
]

RE_SI_SE_RECHAZA = r"(si se rechaza|si no se ajusta|si no sigue|en caso de rechaz)[^,;:]*[,;:]"


def modelos_en(texto_norm: str) -> List[str]:
    texto_norm = re.sub(RE_SI_SE_RECHAZA, " ", texto_norm)
    out = []
    for m, pat in MODELOS:
        if _hay(pat, texto_norm) and m not in out:
            if m == "normal" and "lognormal" in out and not re.search(r"(?<!log)(?<!log-)(?<!log )normal", texto_norm):
                continue
            out.append(m)
    return out


def _valor_tras(texto: str, patron: str) -> Optional[Numero]:
    norm = normalizar(texto)
    for m in re.finditer(patron, norm):
        nums = [n for n in buscar_numeros(texto[m.end():m.end() + 40]) if not n.pct]
        if nums:
            return nums[0]
    return None


def conocidos_en(modelo: str, texto: str) -> Dict[str, float]:
    """Parámetros del modelo que da el enunciado (si no están, se estiman)."""
    c = {}
    if modelo == "normal":
        mu = _valor_tras(texto, r"(valor medio|media|promedio|\bmu\b|μ)\s*(poblacional )?(de|=|es)?\s*")
        sg = _valor_tras(texto, r"(desvio estandar|desviacion estandar|desvio|\bsigma\b|σ)\s*(poblacional )?(de|=|es)?\s*")
        if mu and sg:
            c["mu"], c["sigma"] = mu.valor, sg.valor
    elif modelo == "pareto":
        th = _valor_tras(texto, r"(salario minimo|valor minimo|minimo|costo estimado|θ|theta)\s*(es|de|=)?\s*(de\s*)?")
        if th:
            c["alpha"] = th.valor
    elif modelo == "poisson":
        m = _valor_tras(texto, r"(\bm\s*=|\blambda\s*=|λ\s*=|promedio de|media de)\s*")
        if m:
            c["m"] = m.valor
    elif modelo == "binomial":
        n = _valor_tras(texto, r"muestras? (aleatorias? )?de\s*")
        if n:
            c["n"] = n.valor
        p = re.search(r"\bp\s*=\s*(\d+(?:,\d+)?)", texto)
        if p:
            c["p"] = float(p.group(1).replace(",", "."))
    return c


def _tabla_frecuencias(an: Analisis):
    """(tipo, etiquetas/límites, observados, proporciones o None) de la primera tabla útil."""
    for tabla in an.tablas:
        cols = [normalizar(c or "") for c in tabla["columnas"]]
        filas = [f for f in tabla["filas"] if not (isinstance(f[0], str) and _hay(RE_TOTAL, normalizar(f[0])))]
        if not filas:
            continue
        numericas = [j for j in range(1, len(cols)) if all(_num(f[j]) for f in filas)]
        if not numericas:
            continue
        j_prop = next((j for j in numericas if _hay(r"(proporci|%|porcentaje|histor|teoric)", cols[j])), None)
        j_obs = next((j for j in numericas if j != j_prop and _hay(r"(observ|ocurrenc|cantidad|frecuenc|venta|"
                                                                    r"numero|instalac|dias|usuarios|empleados)", cols[j])),
                     next((j for j in numericas if j != j_prop), None))
        if j_obs is None:
            continue
        obs = [float(f[j_obs]) for f in filas]
        props = [f[j_prop] / (100 if _hay(r"(%|porcentaje)", cols[j_prop]) else 1) for f in filas] if j_prop else None
        if es_tabla_de_clases({"filas": filas}):
            return "clases", limites_de_clase({"filas": filas}), obs, props, tabla["columnas"][j_obs]
        etiquetas = [f[0] for f in filas]
        return "valores", etiquetas, obs, props, tabla["columnas"][j_obs]
    return None


def completar_ajuste(an: Analisis, t):
    tf = _tabla_frecuencias(an)
    if tf:
        tipo, etq, obs, props, nombre = tf
        an.datos["observados"] = obs
        an.datos.pop("esperados", None)
        if tipo == "clases":
            an.datos["clases"] = [list(x) for x in etq]
        else:
            an.datos["valores_var"] = etq
        if props:
            an.datos["proporciones"] = props
        an.evidencias.append(Evidencia("observados", obs, "", f"frecuencias observadas (columna «{nombre}»)"))
    mods = modelos_en(t.norm)
    if mods:
        an.datos["modelos"] = mods[:1]


def _sin_comillas(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[\"“”'«»]", " ", normalizar(s))).strip()


def _columnas_frecuencia(an: Analisis):
    """(tabla, límites de clase, [(nombre, frecuencias)]) si la tabla tiene clases y >= 1 columna de frecuencias."""
    for tabla in an.tablas:
        filas = [f for f in tabla["filas"] if not (isinstance(f[0], str) and _hay(RE_TOTAL, normalizar(f[0])))]
        if not filas or not es_tabla_de_clases({"filas": filas}):
            continue
        cols = []
        for j in range(1, len(tabla["columnas"])):
            col = [f[j] if j < len(f) else None for f in filas]
            if all(v is None or _num(v) for v in col) and any(_num(v) for v in col):
                cols.append((tabla["columnas"][j], [float(v or 0) for v in col]))
        if cols:
            return tabla, limites_de_clase({"filas": filas}), cols
    return None


def _columna_nombrada(cols, norm_inc: str):
    """La columna de frecuencias que nombra el inciso ('marca “B”' → columna 'Marca B')."""
    texto = _sin_comillas(norm_inc)
    for nombre, valores in cols:
        n = _sin_comillas(nombre)
        if n and re.search(r"\b" + re.escape(n) + r"\b", texto):
            return nombre, valores
    # 'Cantidad Observada de la "Marca B"': lo que está entre comillas es el nombre del grupo
    for nombre, valores in cols:
        q = re.findall(r'["“”«»]([^"“”«»]+)["“”«»]', nombre)
        n = _sin_comillas(normalizar(q[-1])) if q else ""
        if n and re.search(r"\b" + re.escape(n) + r"\b", texto):
            return nombre, valores
    return None


def _inciso_de_otro_tema(inc: Inciso, an: Analisis, norm: str) -> Optional[Tuple[str, str]]:
    """En un problema de χ² con una tabla de frecuencias de varios grupos, un inciso puede pedir comparar las medias de
    los grupos (datos agrupados) o estimar el porcentaje de unidades por debajo / encima de un límite."""
    cf = _columnas_frecuencia(an)
    if not cf:
        return None
    tabla, lim, cols = cf
    if len(cols) >= 2 and _hay(r"(que|cual)\s+(marca|maquina|proveedor|proceso|metodo|equipo|variedad)[a-z ]{0,20}"
                               r"(elegir|conviene|recomend|es mejor)|(mayor|menor) (duracion|rendimiento|media|promedio)|"
                               r"comparar (las|los) (medias|promedios)|"
                               # 'el tiempo de una marca es superior al de la otra por más del 10%' (final 15/12/25)
                               r"(superior|mayor|inferior|menor|supera)[^.?]{0,60}\b(de la otra|del otro|que la otra|que el otro)\b|"
                               # 'una diferencia de más del 1% en la performance del equipo A respecto del B' (2° parcial 10/11/25)
                               r"\bdiferencias?\b[^.?]{0,80}\b(respecto|entre)\b",
                               norm):
        from .dos_tablas import grupos_de_tablas
        g = grupos_de_tablas([tabla])
        if g and g.resumen.get("n"):
            r = g.resumen
            if _hay(r"(estim|intervalo|entre que)", norm):
                inc.params.update(tema="dos_medias", apareadas=False,
                                  nombre1=g.nombres[0], n1=r["n"][0], xbar1=r["xbar"][0], s1=r["s"][0],
                                  nombre2=g.nombres[1], n2=r["n"][1], xbar2=r["xbar"][1], s2=r["s"][1])
                if _hay(r"maxim[oa]", norm):
                    inc.params["cota"] = "sup"
                elif _hay(r"minim[oa]", norm):
                    inc.params["cota"] = "inf"
                inc.razones.append(f"Estima la diferencia de medias de los grupos de la tabla ({g.origen}): "
                                   f"{g.nombres[0]} n = {fmt(r['n'][0])}, x̄ = {fmt(r['xbar'][0], 4)}, S = {fmt(r['s'][0], 4)}; "
                                   f"{g.nombres[1]} n = {fmt(r['n'][1])}, x̄ = {fmt(r['xbar'][1], 4)}, S = {fmt(r['s'][1], 4)}"
                                   + {"sup": " (MÁXIMA → cota superior).", "inf": " (MÍNIMA → cota inferior)."}
                                   .get(inc.params.get("cota"), "."))
                return "ic", "IC de la diferencia de medias con datos agrupados (test F previo)."
            m_pct = re.search(r"(en|por|de) mas (del?|de un) (\d+(?:,\d+)?)\s*%", norm)
            if m_pct:
                inc.params.update(delta0_pct=float(m_pct.group(3).replace(",", ".")) / 100, direccion="mas")
            inc.params.update(tema="dos_medias", apareadas=False, tail="derecha", sujeto_por_datos=True,
                              **({} if m_pct else {"delta0": 0.0}),
                              nombre1=g.nombres[0], n1=r["n"][0], xbar1=r["xbar"][0], s1=r["s"][0],
                              nombre2=g.nombres[1], n2=r["n"][1], xbar2=r["xbar"][1], s2=r["s"][1])
            inc.razones.append(f"Compara los grupos de la tabla ({g.origen}): {g.nombres[0]} n = {fmt(r['n'][0])}, "
                               f"x̄ = {fmt(r['xbar'][0], 4)}, S = {fmt(r['s'][0], 4)}; {g.nombres[1]} n = {fmt(r['n'][1])}, "
                               f"x̄ = {fmt(r['xbar'][1], 4)}, S = {fmt(r['s'][1], 4)}. Se elige el de mayor media si se "
                               "puede asegurar que la supera (ensayo unilateral en el sentido de los datos).")
            return "ensayo", "Comparación de dos medias con datos agrupados (test F previo y t)."
    m = re.search(r"(minim[ao]|maxim[ao]|menor(es)? (a|que|de)|mayor(es)? (a|que|de)|por debajo de|por encima de|"
                  r"inferior(es)? a|superior(es)? a)[^0-9]{0,30}(\d[\d.,]*)", norm)
    if m and _hay(r"(porcentaje|porcentual|proporcion|fraccion)", norm) and _hay(r"(estim|intervalo|entre que)", norm):
        limite = [n.valor for n in buscar_numeros(m.group(8))][0]
        lo, hi = lim[0][0], lim[-1][1]
        if not lo <= limite <= hi:
            for f in (1000, 100, 10):
                if lo <= limite / f <= hi:
                    limite /= f
                    break
        col = _columna_nombrada(cols, norm) or cols[0]
        abajo = _hay(r"(minim|menor|debajo|inferior)", m.group(1))
        # 'duración mínima de 14' → no cumplen las unidades por debajo; 'máxima' → las de arriba
        r_ = sum(f for (a, b), f in zip(lim, col[1]) if (b <= limite + 1e-9 if abajo else a >= limite - 1e-9))
        n_ = sum(col[1])
        inc.params.update(tema="proporcion", n=int(n_), r=int(r_), p_hat=r_ / n_)
        inc.razones.append(f"Se cuentan en la columna «{col[0]}» las unidades {'por debajo' if abajo else 'por encima'} de "
                           f"{fmt(limite)} (clases completas): r = {fmt(r_)} de n = {fmt(n_)} → p̂ = {fmt(r_ / n_, 4)}.")
        return "ic", "Estimar la proporción de unidades que no cumplen: IC exacto de p (binomial)."
    return None


def clasificar_ajuste(inc: Inciso, an: Analisis, norm: str) -> Tuple[str, str]:
    otro = _inciso_de_otro_tema(inc, an, norm)
    if otro:
        return otro
    cf = _columnas_frecuencia(an)
    if cf and len(cf[2]) >= 2:
        col = _columna_nombrada(cf[2], norm)
        if col:
            inc.params["observados"] = col[1]
            inc.razones.append(f"Se usa la columna de frecuencias «{col[0]}» que nombra el inciso.")
    mods = modelos_en(norm)
    if mods:
        inc.params["modelos"] = mods
    modelos = mods or an.datos.get("modelos") or []
    texto = inc.texto
    conocidos = {}
    for m in modelos:
        c = conocidos_en(m, texto)
        if not c and not mods:
            c = conocidos_en(m, an.planteo)
        if c:
            conocidos[m] = c
    if conocidos:
        inc.params["conocidos"] = conocidos
    if _hay(r"(cual|que modelo)[^?]{0,40}(mejor|ajusta mejor)|mejor de los ajustes|el mejor", norm):
        inc.params["mejor"] = True
    nombres = ("el modelo " + ", ".join(aj.NOMBRES[m] for m in modelos)) if modelos else "el modelo propuesto"
    return "ensayo", f"Bondad de ajuste χ² a{'l' + nombres[2:]}: se compara χ² calculado contra el crítico."


# ---------------------------------------------------------------- resolución

def _escala(conocidos: Dict[str, float], limites) -> Tuple[Dict[str, float], Optional[str]]:
    """'media de 20.000 horas' con la tabla en miles de horas → 20."""
    if "mu" not in conocidos or not limites:
        return conocidos, None
    lo, hi = limites[0][0], limites[-1][1]
    mu = conocidos["mu"]
    if not (lo <= mu <= hi):
        for f in (1000, 100, 10):
            if lo <= mu / f <= hi:
                return {k: v / f for k, v in conocidos.items()}, f"los parámetros dados se dividieron por {f} (la tabla está en otra escala)"
    return conocidos, None


def _params_txt(r: aj.AjusteResult) -> str:
    nom = {"mu": "μ", "sigma": "σ", "m": "m", "D": "D", "lambda": "λ", "r": "r", "w": "w (forma)", "beta": "β",
           "u": "θ (modo)", "alpha": "θ (mínimo)", "b": "b", "a": "a", "p": "p", "n": "n"}
    return ", ".join(f"{nom.get(k, k)} = {fmt(v, 4)}" + (" (estimado)" if k in r.estimados else " (dado)")
                     for k, v in r.parametros.items() if isinstance(v, (int, float)) and k not in ("k",))


def chi_ajuste_modelos(d, alpha, res, estado):
    from .resolver import FaltaDato, _coma, _regla
    obs = d.get("observados")
    if not obs:
        raise FaltaDato("Faltan las frecuencias observadas")
    modelos = d.get("modelos") or []
    if isinstance(modelos, str):  # editado a mano en la pantalla
        modelos = [m.strip().lower().replace("-", "").replace(" ", "_") for m in modelos.split(",") if m.strip()]
        modelos = [m for m in modelos if m in aj.NOMBRES]
    if not modelos:
        raise FaltaDato("No se reconoció el modelo a ajustar (Normal, Poisson, Weibull...)")
    conocidos_todos = d.get("conocidos") or {}
    resultados = []
    for m in modelos:
        conocidos = dict(conocidos_todos.get(m, {}))
        if m == "uniforme" and d.get("proporciones"):
            conocidos["probs"] = d["proporciones"]
        if m in aj.DISCRETOS:
            vals = d.get("valores_var") or list(range(len(obs)))
            if m != "uniforme":
                vals = [float(re.sub(r"[^\d.,]", "", str(v)).replace(",", ".") or i) for i, v in enumerate(vals)]
            r = aj.ajuste_discreto(m, vals, obs, alpha, conocidos)
        else:
            lim = [tuple(x) for x in (d.get("clases") or [])]
            if not lim:
                raise FaltaDato("Para un modelo continuo hace falta la tabla de clases (límites de cada intervalo)")
            conocidos, nota = _escala(conocidos, lim)
            if nota:
                res.avisos.append(nota)
            r = aj.ajuste_continuo(m, lim, obs, alpha, conocidos)
        resultados.append(r)
        nombre = aj.NOMBRES[m]
        res.pasos.append(f"**— Modelo {nombre} —**")
        params = _params_txt(r) if r.parametros else ""
        res.pasos.append(f"**Hipótesis**: H0: lo observado se ajusta al modelo {nombre}"
                         + (" con " + params if not r.estimados and params else "")
                         + f"  vs  H1: no lo sigue.  α = {fmt(alpha, 4)}.")
        if r.media is not None:
            res.pasos.append(f"**Estimación** (marcas de clase): x̄ = {fmt(r.media, 4)}"
                             + (f", S = {fmt(r.desvio, 4)}" if r.desvio else "") + ".")
        if params:
            res.pasos.append(f"**Parámetros del modelo**: {params}.")
        amalgamado = len(r.tabla_final) < len(r.tabla)
        res.pasos.append("**Frecuencias esperadas** Feᵢ = N·P(clase i) (se completa el dominio del modelo con "
                         "clases de Fo = 0 y probabilidad acumulada):\n\n" + _tabla_md(r.tabla, aportes=not amalgamado))
        if amalgamado:
            res.pasos.append("**Amalgamado** (Fe < 5 se une con la clase vecina):\n\n" +
                             _tabla_md(r.tabla_final, aportes=True))
        k = len(r.tabla_final)
        res.pasos.append(f"**Estadístico**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = {fmt(r.chi2_calc, 4)}; ν = clases efectivas - 1 - p = "
                         f"{k} - 1 - {len(r.estimados)} = {r.df}; χ²(1-α; ν) = {fmt(r.chi2_critico, 4)}.")
        res.pasos.append(f"**Condición de rechazo**: si χ² > {fmt(r.chi2_critico, 4)} ⇒ se rechaza H0.")
        res.pasos.append("**Decisión**: " + (f"χ² = {fmt(r.chi2_calc, 4)} > {fmt(r.chi2_critico, 4)} ⇒ se rechaza H0: "
                                             f"la variable NO sigue el modelo {nombre}." if r.rechaza else
                                             f"χ² = {fmt(r.chi2_calc, 4)} ≤ {fmt(r.chi2_critico, 4)} ⇒ no se rechaza H0: "
                                             f"el modelo {nombre} es un buen candidato."))
        res.avisos += r.avisos
        res.numeros += [r.chi2_calc, r.chi2_critico, float(r.df)] + [v for v in r.parametros.values()
                                                                    if isinstance(v, float)]
    partes = [f"{aj.NOMBRES[r.modelo]}: χ² = {fmt(r.chi2_calc, 4)} vs {fmt(r.chi2_critico, 4)} "
              + ("RECHAZA" if r.rechaza else "NO rechaza") for r in resultados]
    res.resumen = " | ".join(partes)
    concl = []
    for r in resultados:
        nombre = aj.NOMBRES[r.modelo]
        if r.rechaza:
            concl.append(f"Con α = {fmt(alpha, 4)} se rechaza H0: se puede asegurar que la variable no sigue el modelo "
                         f"{nombre}.")
        elif r.modelo in aj.DISCRETOS and r.modelo != "uniforme":
            # tres situaciones de las discretas (profesor, 22/10)
            concl.append(f"Con α = {fmt(alpha, 4)} no se rechaza H0. Si además se cumple el proceso físico del modelo "
                         f"{nombre} (p. ej. Poisson: sucesos puntuales e independientes en un medio continuo), se puede "
                         f"afirmar que la variable sigue el modelo {nombre}; si no se cumple, el modelo {nombre} es un "
                         "buen candidato.")
        else:
            concl.append(f"Con α = {fmt(alpha, 4)} no se rechaza H0: no hay evidencia suficiente para asegurar que la "
                         f"variable no siga el modelo {nombre}; el modelo {nombre} es un buen candidato.")
    if len(resultados) > 1 or d.get("mejor"):
        no_rech = [r for r in resultados if not r.rechaza] or resultados
        mejor = min(no_rech, key=lambda r: r.chi2_calc / r.chi2_critico)
        concl.append(f"El que mejor ajusta es el modelo {aj.NOMBRES[mejor.modelo]} (menor χ² relativo al crítico: "
                     f"{fmt(mejor.chi2_calc / mejor.chi2_critico, 3)}).")
    res.conclusion = _coma(" ".join(concl))
    res.regla = _regla(d, "calcula χ² con las frecuencias observadas y las esperadas del modelo",
                       f"χ² > {fmt(resultados[0].chi2_critico, 4)}", "la variable no sigue el modelo")


def _tabla_md(tabla, aportes: bool = False) -> str:
    """Tabla del ajuste; con `aportes`, la columna (Fo - Fe)²/Fe y la fila de totales (la que da el χ²)."""
    if not aportes:
        lineas = ["| Clase | Fo | P | Fe |", "|---|---|---|---|"]
        for c in tabla:
            lineas.append(f"| {c.etiqueta} | {fmt(c.fo)} | {fmt(c.prob, 4)} | {fmt(c.fe, 3)} |")
        return "\n".join(lineas)
    lineas = ["| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |", "|---|---|---|---|---|"]
    for c in tabla:
        lineas.append(f"| {c.etiqueta} | {fmt(c.fo)} | {fmt(c.prob, 4)} | {fmt(c.fe, 3)} | "
                      f"{fmt((c.fo - c.fe) ** 2 / c.fe, 4)} |")
    lineas.append(f"| **Total** | **{fmt(sum(c.fo for c in tabla))}** | **{fmt(sum(c.prob for c in tabla), 4)}** | "
                  f"**{fmt(sum(c.fe for c in tabla), 3)}** | "
                  f"**χ² = {fmt(sum((c.fo - c.fe) ** 2 / c.fe for c in tabla), 4)}** |")
    return "\n".join(lineas)


def _chi_ajuste_despacho(d, alpha, res, estado):
    from .resolver import chi_ajuste
    if d.get("modelos") and not (d["modelos"] == ["uniforme"] and not d.get("valores_var") and not d.get("clases")):
        return chi_ajuste_modelos(d, alpha, res, estado)
    return chi_ajuste(d, alpha, res, estado)


def _clasificar_contingencia(inc: Inciso, an: Analisis, norm: str):
    inc.params["chi_diseno"] = diseno_contingencia(norm + " " + normalizar(an.planteo), an.datos.get("chi_grupos"))
    return clasificar_inciso(norm, an.tema, normalizar(an.planteo))


EXTENSIONES["chi_ajuste"] = (completar_ajuste, clasificar_ajuste)
EXTENSIONES["chi_contingencia"] = (completar_contingencia, _clasificar_contingencia)
DESPACHO_EXTRA[("chi_ajuste", "ensayo")] = _chi_ajuste_despacho
