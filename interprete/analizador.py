"""Analizador por reglas: enunciado -> Analisis (tema, datos, incisos).

No "entiende" el texto: busca las frases típicas de la cátedra (las mismas de la
Guía de Problemas) y ubica cada número según las palabras que lo rodean. Por
eso cada dato guarda la evidencia (el fragmento del que salió) y todo es
editable en la pantalla antes de calcular.
"""

import re
from math import sqrt
from typing import Dict, List, Optional, Sequence, Tuple, Union

from .modelo import Analisis, Evidencia, Inciso, TEMAS
from .texto import ListaDatos, Numero, buscar_listas, buscar_numeros, fmt, normalizar, oraciones, parse_num

# ---------------------------------------------------------------------------
# Separación de incisos
# ---------------------------------------------------------------------------

RE_INCISO = re.compile(r"(?:(?<=[\s.?:;])|^)([a-h])\)\s")


def separar_incisos(texto: str) -> Tuple[str, List[Tuple[str, str]]]:
    """Parte un enunciado completo en planteo + [(letra, texto)] (a, b, c... consecutivas)."""
    esperado = "a"
    cortes = []
    for m in RE_INCISO.finditer(texto):
        if m.group(1) == esperado:
            cortes.append((m.start(1), m.end(), esperado))
            esperado = chr(ord(esperado) + 1)
    if not cortes:
        return texto.strip(), []
    planteo = texto[: cortes[0][0]].strip()
    incisos = []
    for i, (ini, fin_marca, letra) in enumerate(cortes):
        fin = cortes[i + 1][0] if i + 1 < len(cortes) else len(texto)
        incisos.append((letra, texto[fin_marca:fin].strip()))
    return planteo, incisos


# ---------------------------------------------------------------------------
# Contexto de un texto: números, oraciones y búsquedas por ventana
# ---------------------------------------------------------------------------

class Texto:
    def __init__(self, texto: str):
        self.texto = texto
        self.norm = normalizar(texto)
        self.nums: List[Numero] = buscar_numeros(texto)
        self.usados = set()   # índices de self.nums ya asignados a un dato
        self.listas: List[ListaDatos] = buscar_listas(texto)
        self._oraciones = oraciones(texto)

    def oracion(self, pos: int) -> str:
        for ini, fin in self._oraciones:
            if ini <= pos < fin:
                return self.norm[ini:fin]
        return self.norm

    def oracion_cruda(self, pos: int) -> str:
        for ini, fin in self._oraciones:
            if ini <= pos < fin:
                return self.texto[ini:fin].strip()
        return self.texto

    def antes(self, n: Numero, k: int = 60) -> str:
        s = self.norm[max(0, n.ini - k):n.ini]
        # no cruzar oraciones
        m = list(re.finditer(r"[.?!;:]\s", s))
        return s[m[-1].end():] if m else s

    def despues(self, n: Numero, k: int = 45) -> str:
        s = self.norm[n.fin:n.fin + k]
        m = re.search(r"[.?!;]\s|[.?!]$", s)
        return s[:m.start()] if m else s

    def fragmento(self, n: Numero, k: int = 70) -> str:
        ini = max(0, n.ini - k)
        fin = min(len(self.texto), n.fin + 25)
        return ("…" if ini else "") + self.texto[ini:fin].strip() + ("…" if fin < len(self.texto) else "")

    def libres(self):
        for i, n in enumerate(self.nums):
            if i not in self.usados and not self._en_lista(n):
                yield i, n

    def _en_lista(self, n: Numero) -> bool:
        return any(l.ini <= n.ini < l.fin and len(l.valores) >= 3 for l in self.listas)

    def usar(self, i: int):
        self.usados.add(i)


def _hay(patron: str, texto: str) -> bool:
    return re.search(patron, texto) is not None


def _cuenta(patrones: Sequence[str], texto: str) -> int:
    return sum(len(re.findall(p, texto)) for p in patrones)


# ---------------------------------------------------------------------------
# Palabras clave
# ---------------------------------------------------------------------------

P_PROPORCION = [r"porcentaje", r"proporci", r"fraccion", r"defectuos", r"rating", r"puntos porcentuales",
                r"ausentismo", r"plan de muestreo", r"\baql\b", r"\bltpd\b", r"compradores", r"televidentes",
                r"inscript", r"penetracion", r"exitos?\b", r"se presento \d+ veces", r"frecuencia excesiva",
                r"probabilidad de(l)? cero"]
P_VARIANZA = [r"varianza", r"variabilidad", r"volatilidad", r"regularidad", r"dispersion", r"parejos",
              r"(estimar|limites|intervalo|estimacion)[^.]{0,40}(desvio|desviacion)",
              r"(desvio|desviacion)[^.]{0,30}(no debe superar|menor que|mayor que|superior a|inferior a|difieren|reduc|disminu)"]
P_MEDIA = [r"\bmedi[oa]s?\b", r"promedio"]
P_DOS = [r"\bdos (maquinas|tornos|raciones|variedades|procesos|marcas|metodos|grupos|enconadoras|"
         r"establecimientos|tratamientos|areas|equipos|poblaciones|aleaciones|formulas)",
         r"\bambos (tornos|procesos|metodos|grupos|establecimientos|tratamientos|equipos)",
         r"\bambas (maquinas|variedades|raciones|marcas|muestras|areas|aleaciones|enconadoras|formulas|pruebas)",
         r"\bn1\b|\bn 1\s*=|\bs1\s*=|\bs 1\s*=", r"\bcon (el )?aditivo\b[^.]*\bsin\b|\bsin (el )?aditivo",
         r"sin reacondicionar", r"proceso viejo", r"\bsin acelerante", r"con albumina",
         r"\b(variedad|racion|maquina|marca|metodo|proceso|establecimiento)\s*[“\"][^”\"]{1,15}[”\"][^.]{0,120}"
         r"\b(variedad|racion|maquina|marca|metodo|proceso|establecimiento)\s*[“\"]",
         r"\botras \d+ (parcelas|piezas|maquinas)", r"\botra prueba", r"producto tradicional",
         r"mientras que de \d", r"respecto de (la|el|los|las) (variedad|metodo|maquina|proceso)\b",
         r"con respecto a las ventas anteriores", r"con el proveedor habitual",
         r"variedad (actual|nueva)", r"metodo (propuesto|clasico)", r"\([a-z]{1,3}\)\s*:[^.]{0,80}\([a-z]{1,3}\)\s*:"]
P_APAREADAS = [r"apareadas", r"un par de", r"cada (finca|persona|trabajador)", r"ambos procesos",
               r"mismos? (trabajadores|individuos|personas)", r"en parcelas experimentales de cada finca",
               r"se les pidio", r"dividiendo al material", r"el material se dividio", r"trabajador\s*:"]
P_CHI_AJUSTE = [r"se ajusta", r"bondad de ajuste", r"\bajuste (a|al|de)\b", r"modelo (normal|de poisson|log-?normal|"
                r"de weibull|weibull|de pareto|pareto|gumbel|uniforme)", r"\b(un|el) dado\b", r"dado (esta )?cargado",
                r"ruleta[^?]{0,400}(negro|colorado)", r"igualmente distribuid", r"patron historico", r"se comporta",
                r"distribucion (poissoniana|de poisson)", r"cumple con la especificacion del fabricante"]
P_CHI_CONT = [r"independ", r"estan asociad", r"\basociadas\b", r"asociacion entre", r"existe asociacion",
              r"\bdepende de la\b", r"tabla de contingencia", r"homogene", r"difieren entre",
              r"(proporciones|niveles|porcentajes?)[^.]{0,60}(difieren|diferentes|variado)",
              r"(variado|variacion|difieren|diferentes)[^.]{0,40}(porcentaje|proporci)",
              r"relacion entre el color",
              r"\b([3-9]|tres|cuatro|cinco) (plantas|turnos|locales|zonas|areas|grupos|semanas|localidades)\b"]
P_REGRESION = [r"regresion", r"correlacion", r"minimos cuadrados", r"\brecta\b", r"pronostic", r"relacion lineal",
               r"linealmente", r"asociacion lineal", r"en funcion de", r"variables? (independiente|dependiente|a explicar)",
               r"combinacion lineal", r"\bx\s*1\b.{0,200}\bx\s*2\b", r"relacionada con", r"predecir",
               r"relacion entre (el|la|los|las) [a-z ]{3,60} y (el|la|los|las|su)\b", r"ecuacion para"]

# Dirección del ensayo
P_MAS = [r"\bmayor(es)?\b", r"superior", r"\bsupera", r"\bexced", r"aument", r"increment", r"\bmas de\b",
         r"\bmejor", r"efectiv"]
P_MENOS = [r"\bmenor(es)?\b", r"inferior", r"disminu", r"\breduc", r"\bmenos de\b", r"\bbaj[aoe]\b"]
P_DISTINTO = [r"diferente", r"distint", r"difier", r"modificad", r"\bcambi", r"desajust", r"fuera de control",
              r"bajo control", r"\balter", r"variado", r"significativ"]

P_PESIMISTA = [r"invers", r"compra", r"cambiar", r"\bnuev[oa]", r"aditivo", r"modificacion", r"lanzar",
               r"implementar", r"campana", r"justific", r"reacondicion", r"adoptar"]
P_OPTIMISTA = [r"control de recepcion", r"recepcion", r"partida", r"\blote\b", r"especificacion", r"contrato",
               r"proveedor", r"bajo control", r"control"]

MUESTRA = r"(muestra|arroj|obtuv|obteni|registr|result[oa]|\bdio\b|se tomo|prueba|ensayo|experiment|se realizo|se encontr|comprueba|se hallaron|se detecta|se observ|se midieron|midiendose)"



# ---------------------------------------------------------------------------
# Detección del tema
# ---------------------------------------------------------------------------

RE_IMPERATIVO = (r"(estimar|calcular|determinar|indicar|establecer|verificar|ensayar|obtener|hallar|describir|"
                 r"plantear|disenar|probar|investigue|analizar|realizar|efectuar|decidir)\b")


def pregunta_de(texto: str) -> str:
    """La parte del planteo que pregunta (desde la 1ª oración con '¿' o con verbo en infinitivo)."""
    norm = normalizar(texto)
    partes = oraciones(texto)

    def pregunta(ini, fin):
        o = norm[ini:fin].strip()
        return ("¿" in o or re.match(RE_IMPERATIVO, o) is not None
                or re.search(r"(se pide|se desea conocer|se quiere)[^.]{0,20}", o) is not None)

    idx = [k for k, (ini, fin) in enumerate(partes) if pregunta(ini, fin)]
    if not idx:
        return texto[partes[-1][0]:].strip() if partes else texto
    k = idx[-1]
    while k - 1 in idx:
        k -= 1
    return texto[partes[k][0]:].strip()


def _dos_estructural(norm: str, listas: List[ListaDatos]) -> bool:
    """Dos muestras aunque no se nombren: dos 'muestra de n', o dos pares media+desvío, o 2 listas etiquetadas."""
    if _hay(r"sistema (periodico )?de muestreo|plan de muestreo", norm):
        return False
    if len(re.findall(r"muestras? (aleatoria )?(de|con) \d", norm)) >= 2 and _hay(r"(otr[oa]|habitual|mientras|ademas)", norm):
        return True
    medias = len(re.findall(r"(media|promedio|medio)[^0-9.;]{0,30}\d", norm))
    desvios = len(re.findall(r"(desvio|desviacion)[^0-9.;]{0,30}\d", norm))
    if medias >= 2 and desvios >= 2:
        return True
    etiquetadas = [l for l in listas if len(l.valores) >= 3 and re.search(r"[a-zA-Z]{3,}", l.etiqueta or "")
                   and not re.search(r"(cantidad|frecuencia|ocurrencia|^\(|local|semana|muestra n)", normalizar(l.etiqueta))]
    return len(etiquetadas) >= 2 and len({l.etiqueta for l in etiquetadas}) >= 2


def detectar_tema(norm: str, listas: List[ListaDatos], pregunta: str = "") -> Tuple[str, List[str]]:
    razones = []
    q = pregunta or norm
    # menciones del desvío que NO lo convierten en el parámetro pedido
    q = re.sub(r"(si no se conociera el desvio[a-z ]*|(el )?desvio[a-z ]{0,30}(no se conoce|no se modifica|se mantiene|"
               r"desconocido)|considerando que el desvio[a-z ]*)", " ", q)
    reg_fuerte = _cuenta(P_REGRESION[:3], norm)
    reg = _cuenta(P_REGRESION, norm)
    s_aj = 2 * _cuenta(P_CHI_AJUSTE, norm)
    s_ct = _cuenta(P_CHI_CONT, norm)
    dos = _cuenta(P_DOS, norm) > 0 or _dos_estructural(norm, listas)
    prop = _cuenta(P_PROPORCION, norm)
    var = _cuenta(P_VARIANZA, norm)
    med = _cuenta(P_MEDIA, norm)
    var_q = _cuenta([r"varianza", r"\bdesvio", r"desviacion", r"variabilidad", r"volatilidad"], q)
    med_q = _cuenta([r"\bmedi[oa]s?\b", r"promedio"], q)
    prop_q = _cuenta([r"porcentaje", r"proporci", r"fraccion", r"defectuos", r"rating", r"\d\s*%"], q)

    if reg_fuerte >= 1 or reg >= 2:
        razones.append("Habla de regresión / correlación / relación entre dos variables (recta de mínimos cuadrados).")
        return "regresion", razones
    if s_aj >= 1 and s_aj >= s_ct:
        razones.append("Pregunta si los datos siguen un modelo teórico (dado, ruleta, 'se ajusta a', "
                       "'igualmente distribuidas', patrón histórico): es bondad de ajuste χ².")
        return "chi_ajuste", razones
    if s_ct >= 1 and (prop >= 1 or s_ct >= 2 or _hay(r"independ|asociad|asociacion|contingencia|depende", norm)):
        razones.append("Pregunta si hay asociación / independencia o si las proporciones difieren entre "
                       "varios grupos: tabla de contingencia χ².")
        return "chi_contingencia", razones

    if dos:
        if prop >= 1 and prop_q >= 1 and med_q == 0 and var == 0:
            razones.append("Compara porcentajes de 2 grupos: la guía lo resuelve como tabla de contingencia χ² "
                           "(comparación de procesos de Bernoulli).")
            return "chi_contingencia", razones
        foco_var = _hay(r"(desvios?|desviacion(es)?|varianzas?|variabilidad|regularidad|parejos)[^.?]{0,60}"
                        r"(difieren|diferentes|reduc|disminu|mayor|menor|relacion|igual)|"
                        r"(reduccion|disminuir|disminucion)[^.?]{0,40}(desvio|desviacion|varianza)|"
                        r"relacion entre (las varianzas|los desvios)", q) or \
            _hay(r"(reduccion|disminuir|disminucion)[^.?]{0,40}(desvio|desviacion|varianza)", norm) or (var_q > med_q and var_q > 0)
        if foco_var:
            razones.append("Compara la variabilidad (desvíos / varianzas) de 2 poblaciones: test F.")
            return "dos_varianzas", razones
        razones.append("Hay dos muestras / grupos para comparar (dos máquinas, variedades, con y sin aditivo...): "
                       "comparación de 2 medias.")
        return "dos_medias", razones

    if prop >= 1 and (prop_q >= 1 or prop >= 2) and not (med_q > prop_q and _hay(r"rendimiento|valor medio", norm)):
        if not (med_q > 0 and prop_q == 0 and _hay(r"desvio", norm)):
            razones.append("El parámetro es un porcentaje / proporción / fracción defectuosa: proceso de "
                           "Bernoulli (binomial).")
            return "proporcion", razones
    if (var_q > 0 and var_q >= med_q) or (var_q == 0 and med_q == 0 and var >= 1):
        razones.append("Lo que se pregunta es sobre la variabilidad (varianza / desvío estándar), no sobre la media.")
        return "varianza", razones
    razones.append("El parámetro es un valor medio / promedio de una variable.")
    return "media", razones


# ---------------------------------------------------------------------------
# Extracción de datos (1 población)
# ---------------------------------------------------------------------------

def _es_prob(n: Numero) -> bool:
    return (n.pct and n.valor <= 100) or (not n.pct and 0 < n.valor < 1)


RE_CONF = r"(confianza|seguridad)"
# 'error muestral / de muestreo / de estimación' es el e del IC, no el riesgo α
RE_ALPHA = (r"(riesgo|significacion|\berror\b(?! (muestral|de muestreo|de (la )?estimacion|admitido|maximo))|"
            r"equivocad|erronea|errone|indebidamente|incorrect|tipo i\b)")

# relleno sin números ni cortes de oración entre la palabra clave y el número
_R = r"[^0-9.;?]"


def _alpha_de(t: Texto, i: int, n: Numero) -> Optional[Tuple[float, str]]:
    """Si el número es un nivel de confianza o de riesgo, devuelve (alpha, motivo)."""
    if not _es_prob(n):
        return None
    a, d = t.antes(n, 45), t.despues(n, 55)
    m_conf = re.search(RE_CONF + "(" + _R + r"{0,32})$", a)
    if (m_conf and not _hay(r"(cuyo|limite|sea )", m_conf.group(2))) or _hay(r"^\s*(de )?" + RE_CONF, d):
        return 1 - n.fraccion, "nivel de confianza → α = 1 - confianza"
    if n.fraccion > 0.5:
        return None
    if _hay(r"(baj|aument|disminu|reduc|increment|sub)[a-z]* (en )?(un |el |del )?$", a):
        return None   # 'el costo baje en un 10%' es un valor alternativo, no un riesgo
    if _hay(RE_ALPHA + _R + r"{0,35}$", a) or _hay(r"^" + _R + r"{0,45}" + RE_ALPHA, d):
        return n.fraccion, "riesgo / nivel de significación α"
    ora = t.oracion(n.ini)
    if _hay(r"probabilidad" + _R + r"{0,90}$", t.antes(n, 100)) and _hay(
            r"(equivocad|erronea|indebid|incorrect|rechazar una partida que cumple|revisarlo? equivocadamente)", ora):
        return n.fraccion, "probabilidad de equivocarse al rechazar H0 → α"
    return None


def _set(an: Analisis, clave: str, valor, t: Texto, n: Optional[Numero], motivo: str, pisar=False):
    if clave in an.datos and not pisar:
        return False
    an.datos[clave] = valor
    frag = t.fragmento(n) if n is not None else ""
    an.evidencias = [e for e in an.evidencias if e.clave != clave]
    an.evidencias.append(Evidencia(clave, valor, frag, motivo))
    return True


def extraer_alpha(t: Texto) -> Optional[Tuple[float, Numero, str]]:
    for i, n in t.libres():
        r = _alpha_de(t, i, n)
        if r:
            t.usar(i)
            return r[0], n, r[1]
    return None


RE_INTERVALO = r"(\d+(?:,\d+)?)\s*[–-]\s*(\d+(?:,\d+)?)"


def _agrupados(t: Texto) -> Optional[Tuple[List[float], str]]:
    """Tabla de frecuencias: 'a – b' repetido k veces + 'Cantidad' con k frecuencias,
    o pares 'valor frecuencia' bajo encabezados 'Cantidad de X  Número de Y'."""
    m = re.search(r"((?:" + RE_INTERVALO + r"\s+){3,}" + RE_INTERVALO + r")\s*[A-Za-zÁÉÍÓÚáéíóú .]{0,40}?"
                  r"(cantidad|frecuencia|observaciones|numero)[^0-9]{0,40}((?:\d+\s+){2,}\d+)", t.norm)
    if m:
        marcas = [(float(a.replace(",", ".")) + float(b.replace(",", "."))) / 2
                  for a, b in re.findall(RE_INTERVALO, m.group(1))]
        frec = [int(x) for x in m.group(m.lastindex).split()]
        if len(frec) >= len(marcas):
            frec = frec[:len(marcas)]
            datos = [x for x, f in zip(marcas, frec) for _ in range(f)]
            return datos, "datos agrupados: marcas de clase (punto medio de cada intervalo) × frecuencias"
    m = re.search(r"(cantidad|numero|valor)( de [a-z]+)?\s+(numero|cantidad|frecuencia)( de [a-z]+)?\s+((?:\d+(?:,\d+)?\s+){3,}\d+(?:,\d+)?)",
                  t.norm)
    if m:
        nums = [float(x.replace(",", ".")) for x in m.group(5).split()]
        if len(nums) % 2 == 0 and all(float(f).is_integer() for f in nums[1::2]):
            datos = [x for x, f in zip(nums[0::2], nums[1::2]) for _ in range(int(f))]
            return datos, "tabla de frecuencias: cada valor repetido según su frecuencia"
    return None


def extraer_datos_lista(an: Analisis, t: Texto):
    """Si el enunciado trae los datos crudos (o una tabla de frecuencias), calcula n, x̄ y S."""
    ag = _agrupados(t)
    if ag:
        an.datos["datos"] = ag[0]
        an.evidencias.append(Evidencia("datos", f"{len(ag[0])} datos", "", ag[1]))
        return
    listas = [l for l in t.listas if len(l.valores) >= 3]
    if not listas:
        return
    lista = max(listas, key=lambda l: len(l.valores))
    valores = lista.valores
    previo = t.norm[max(0, lista.ini - 120):lista.ini]
    if _hay(r"en miles", previo):
        an.datos["_escala_miles"] = True
    an.datos["datos"] = valores
    an.evidencias.append(Evidencia("datos", valores, t.texto[lista.ini:lista.fin],
                                   "lista de datos crudos → se calculan n, x̄ y S"))


def ajustar_escala(an: Analisis):
    """Datos 'en miles' y μ₀ en unidades (o al revés): se pasan los datos a la escala de μ₀."""
    if not an.datos.pop("_escala_miles", False):
        return
    datos, mu0 = an.datos.get("datos"), an.datos.get("mu0")
    if datos and mu0 and mu0 / (sum(datos) / len(datos)) > 100:
        an.datos["datos"] = [x * 1000 for x in datos]
        an.avisos.append("Los datos estaban 'en miles' y μ₀ en unidades: se multiplicaron los datos por 1.000.")


UNIDADES_MUESTRA = (r"(envases|unidades|piezas|rollos|tarjetas|ovillos|tablas|medidores|corridas|dias|meses|"
                    r"semanas|horas|personas|familias|paquetes|cerdos|tubos|laminas|cojinetes|supermercados|clientes|"
                    r"observaciones|hogares|catalogos|arboles|televidentes|tornillos|llantas|bolas|conos|muestras|"
                    r"maquinas|parcelas|animales|potrillos|operarios|ensayos|datos|botellas|suelas|conjuntos|"
                    r"hombres|mujeres|usuarios|bielas|establecimientos|negocios|alambres|lamparas|baterias|"
                    r"recorridos|mediciones|pilas|bolsas|latas|cajas|articulos|vehiculos|autos|lotes|tomas|jornadas)")
VERBOS_MUESTRA = (r"(muestra|se tomaron|se eligieron|se seleccionaron|se midieron|se pesaron|se registr|se analiz|"
                  r"se enviaron|se atendieron|sobre|durante|panel|se trabajo|arroj|obtuv|obteni|prueba|experiment|"
                  r"comprueba|se realizo|se examin|examinar|se inspeccion|se controla|obtiene|en los primeros|se envian)")


def extraer_n(an: Analisis, t: Texto, clave="n"):
    mejor = None
    for i, n in t.libres():
        if n.pct or not n.es_entero or n.valor < 2:
            continue
        a, d = t.antes(n, 50), t.despues(n, 30)
        ora = t.oracion(n.ini)
        score = 0
        if _hay(r"\bn\s*=\s*$", a):
            score = 5
        elif _hay(r"muestras? (aleatoria |al azar )?(de|con) $|muestras? (aleatoria )?de tamano $", a):
            score = 4
        elif _hay(r"^\s*[\"“]?([a-z]+ )?" + UNIDADES_MUESTRA, d) and _hay(VERBOS_MUESTRA, ora):
            score = 3
        if _hay(r"(poblacion total|poblacion|lote|partida|total) de $|(media|promedio|desvio|error)" + _R + r"{0,40}$", a) \
                and score < 4:
            score = 0
        if score and (mejor is None or score > mejor[0]):
            mejor = (score, i, n)
    if mejor:
        _, i, n = mejor
        t.usar(i)
        _set(an, clave, int(n.valor), t, n, "tamaño de la muestra")
        return n
    return None


def extraer_N(an: Analisis, t: Texto):
    for i, n in t.libres():
        a = t.antes(n, 40)
        if n.es_entero and not n.pct and _hay(r"(poblacion (total )?(compuesta )?de|lote( de produccion)? de|partida de|"
                                              r"sobre un lote de|poblacion de) $", a):
            if "n" in an.datos and n.valor <= an.datos["n"]:
                continue
            t.usar(i)
            _set(an, "N", n.valor, t, n, "tamaño de la población (finita) → corrección por finitud")
            return


def extraer_totales(an: Analisis, t: Texto):
    """'40 personas en 68 minutos' / '25 horas ... un total de 4 horas y 30 minutos' -> x̄ = total / n."""
    if "xbar" in an.datos or "n" not in an.datos:
        return
    n = an.datos["n"]
    m = re.search(r"un total de (\d+) horas? y (\d+) minutos", t.norm)
    if m:
        total = int(m.group(1)) * 60 + int(m.group(2))
        an.datos["xbar"] = total / n
        an.evidencias.append(Evidencia("xbar", total / n, t.texto[m.start():m.end()],
                                       f"total {total} minutos / n = {n} → x̄"))
        return
    m = re.search(r"\b" + str(n) + r" [a-z]+ en (\d+(?:,\d+)?) (minutos|horas|segundos|dias)", t.norm)
    if m:
        total = float(m.group(1).replace(",", "."))
        an.datos["xbar"] = total / n
        an.evidencias.append(Evidencia("xbar", total / n, t.texto[m.start():m.end()],
                                       f"total {m.group(1)} {m.group(2)} / n = {n} → x̄"))


RE_MEDIA_ANTES = r"(media|medio|promedio|valor estandar)" + _R + r"{0,50}?(\bde|\bdel|\bes|\bfue|=|\bdio|\bresulto|\ben|\bvale)\s*(los |las |el |la |un |una |aproximadamente )?$"
RE_UMBRAL_ANTES = (r"(mayor|menor|superior|inferior|supera|excede|\bmas|\bmenos|minima|maxima|minimo|maximo|"
                   r"igual|debe ser|deberia ser|no debe superar|no supera|a lo sumo|por lo menos|al menos|"
                   r"admisible|especificacion|estandar|nominal|actualmente|actual|habitual|historic|diferente|distint|"
                   r"aproximadamente)"
                   + _R + r"{0,30}(que|a|de|del|es|las|los|el|la)?\s*$")
POBLACION_FUERTE = (r"(parametros poblacionales|pueden considerarse|en condiciones normales|actualmente|son variables con|"
                    r"en la actualidad|historicamente|por investigaciones|registros historicos|valor estandar|"
                    r"con las maquinas actuales|si el torno esta bien ajustado|se considera aceptable|"
                    r"importante cantidad de datos)")


def _es_umbral(t: Texto, n: Numero) -> bool:
    a, d = t.antes(n, 45), t.despues(n, 40)
    ora = t.oracion(n.ini)
    if _hay(RE_UMBRAL_ANTES, a):
        return True
    if _hay(r"^" + _R + r"{0,15}(por lo menos|como minimo|como maximo|a lo sumo)", d):
        return True
    if _hay(POBLACION_FUERTE, ora):
        return True
    if _hay(r"(se sabe que|debe ser|es una variable|variable aleatoria con|es variable con)", ora) \
            and not _hay(r"arroj|obtuv|obteni|registrandose|resulto|se registra\b", ora):
        return True
    return False


def extraer_media(an: Analisis, t: Texto, solo_mu0: bool = False):
    """x̄ (dato muestral) y μ₀ (valor de referencia / umbral). En un diseño solo hay μ₀ (y μ₁)."""
    for i, n in t.libres():
        if solo_mu0 and "mu0" in an.datos:
            return
        ora = t.oracion(n.ini)
        if n.pct and not _hay(r"rendimiento", ora):
            continue
        a = t.antes(n, 70)
        if _hay(r"(desvio|desviacion|varianza)" + _R + r"{0,30}$", a) or _hay(RE_CONF + r"|riesgo|probabilidad", a[-25:]):
            continue
        if _hay(r"^\s*(semanas|anos|meses|dias|horas)\b" + _R + r"{0,12}(de edad )?(es|fue|era)\b", t.despues(n, 30)):
            continue
        es_media = _hay(RE_MEDIA_ANTES, a) or _hay(r"(promedio|media)[^.;?]{0,90}(fue de|resulto de|resulto|dio)\s*$", t.antes(n, 110))
        umbral = _es_umbral(t, n)
        if not es_media and not umbral:
            continue
        if not es_media and (_es_prob(n) and not n.pct):
            continue
        muestral = _hay(r"(muestra|arroj|obtuv|obteni|registrandose|resulto|se registra|se obtuvo|\bdio\b|en los primeros|"
                        r"prueba|se trabajo|se realizo)", ora) and not _hay(POBLACION_FUERTE, ora)
        # un umbral explícito pegado al número ('debe ser de', 'mayor de', 'por lo menos') manda sobre el contexto
        umbral_fuerte = _hay(RE_UMBRAL_ANTES, t.antes(n, 45)) or _hay(r"^" + _R + r"{0,15}(por lo menos|como minimo|como maximo|a lo sumo)", t.despues(n, 40))
        if umbral_fuerte:
            t.usar(i)
            if "mu0" not in an.datos:
                _set(an, "mu0", n.valor, t, n, "valor de referencia / especificación / umbral de la media (μ₀)")
            continue
        if umbral and not muestral and "mu0" not in an.datos:
            t.usar(i)
            _set(an, "mu0", n.valor, t, n, "valor de referencia / especificación / media poblacional (μ₀)")
        elif es_media and muestral and "xbar" not in an.datos:
            t.usar(i)
            _set(an, "xbar", n.valor, t, n, "media obtenida en la muestra (x̄)")
        elif umbral and "mu0" not in an.datos:
            t.usar(i)
            _set(an, "mu0", n.valor, t, n, "valor de referencia / umbral de la media (μ₀)")
        elif es_media and "mu0" not in an.datos and "xbar" in an.datos:
            t.usar(i)
            _set(an, "mu0", n.valor, t, n, "media de la población / valor histórico (μ₀)")
        elif es_media and "xbar" not in an.datos and "mu0" in an.datos:
            t.usar(i)
            _set(an, "xbar", n.valor, t, n, "media obtenida en la muestra (x̄)")
        elif es_media and "mu0" not in an.datos:
            t.usar(i)
            _set(an, "mu0", n.valor, t, n, "media de la variable (μ₀)")


RE_DESVIO_ANTES = (r"((desvio|desviacion)" + _R + r"{0,75}?(\bde|\bes|\bfue|=|\bvale|\bdio|\bresulto|\bsido|superar( los| las)?|"
                   r"\bdel)\s*(los |las |un |una )?$|σ\s*=?\s*$|\bun\s*=\s*$|\bs\s*=\s*$|(desvio|desviacion) (estandar )?$)")
CONOCIDO = (r"(poblacional|historic|se sabe|se conoce|conocid|registros|experiencia|parametros poblacionales|"
            r"distribucion normal (con un |de )?(desvio|desviacion)|se distribuye|se mantiene|no se modifica|no ha de modificarse|"
            r"estable|variable (aleatoria )?(con|cuya|cuyo)|es una variable|tiene un desvio|variabilidad del proceso|"
            r"sin modificar el desvio|no se modificara|pueden considerarse|valor este que|es variable con|"
            r"con las maquinas actuales)")


def extraer_desvio(an: Analisis, t: Texto, clave="desvio"):
    for i, n in t.libres():
        a = t.antes(n, 95)
        if n.pct and not _hay(r"(desvio|desviacion)", a[-30:]):
            continue
        es_var = _hay(r"varianza( muestral| poblacional)?" + _R + r"{0,20}(dio|de|es|fue|=)\s*$", a)
        largo = _hay(r"(desvio|desviacion)[^.;?]{0,100}(fue de|resulto de|resulto|dio|ha sido de)\s*$", t.antes(n, 130))
        umbral_sig = _hay(r"(desvio|desviacion)" + _R + r"{0,70}(menor|mayor|superior|inferior)( que| a)( los| las)?\s*$", a)
        if not (_hay(RE_DESVIO_ANTES, a) or es_var or largo or umbral_sig):
            continue
        ora = t.oracion(n.ini)
        valor = sqrt(n.valor) if es_var else n.valor
        umbral = umbral_sig or _hay(r"(no debe superar|maximo|minimo|mayor|menor|superior|inferior|como maximo|especificacion|"
                      r"estipulado|nominal|no supere)" + _R + r"{0,25}$", a) or \
            _hay(r"^" + _R + r"{0,15}(como maximo|como minimo)", t.despues(n))
        if clave == "desvio" and an.tema == "varianza" and umbral:
            if "sigma0" not in an.datos:
                t.usar(i)
                _set(an, "sigma0", valor, t, n, "valor de referencia del desvío (σ₀)")
            continue
        if clave in an.datos:
            continue
        t.usar(i)
        muestral = _hay(r"(arroj|obtuv|obteni|resulto|registrandose|\bdio\b|se obtuvo|muestra|ha sido)", ora)
        conocido = _hay(CONOCIDO, ora) and (not muestral or _hay(POBLACION_FUERTE + r"|historic|poblacional", ora))
        if an.tema == "varianza" and muestral:
            conocido = False
        motivo = ("varianza muestral → S = √S²" if es_var else
                  ("desvío poblacional σ (lo dice el enunciado: histórico / se sabe / registros)" if conocido
                   else "desvío calculado en la muestra (S)"))
        _set(an, clave, valor, t, n, motivo)
        if clave == "desvio":
            _set(an, "sigma_conocido", conocido, t, None,
                 "σ conocido → se usa Z" if conocido else "σ desconocido → se usa S y t de Student")
        return


def extraer_error(t: Texto) -> Optional[Tuple[str, float, Numero]]:
    """Error admitido (e) o reducción pedida del error / de la relación entre límites."""
    for i, n in t.libres():
        a, d = t.antes(n, 70), t.despues(n, 50)
        if n.pct and (_hay(r"(reduc|disminu)[a-z]*( en)?( un| el)?\s*$", a) or
                      _hay(r"(reduc|disminu)[a-z]*[^0-9.;?]{0,50}(error|relacion|amplitud)[^0-9.;?]{0,40}(en )?(un |el )?$", a) or
                      (_hay(r"(reduc|disminu)[a-z]*" + _R + r"{0,20}$", a) and _hay(r"^\s*(el|la) (error|relacion|amplitud)", d))):
            t.usar(i)
            return "reduccion", n.fraccion, n
        if _hay(r"error" + _R + r"{0,40}(de|sea|a|=)\s*(±\s*)?$|±\s*$|reducir el error a\s*$", a) and not _hay(r"tipo", a[-20:]):
            if not (n.pct and not _hay(r"rating|porcentaje|proporci|%", t.oracion(n.ini))) or _hay(r"±\s*$", a):
                t.usar(i)
                return "e", n.fraccion if n.pct and _hay(r"rating|porcentaje|proporci", t.norm) else n.valor, n
    s = t.norm
    for patron, valor in ((r"(a la mitad|en la mitad|la mitad del|la mitad de la|sea la mitad)", 0.5),
                          (r"a la tercera parte", 2 / 3), (r"a la cuarta parte", 0.75)):
        if _hay(r"(reduc|disminu|amplitud|error)[^.?]{0,60}" + patron, s):
            return "reduccion", valor, None
    return None


def extraer_mu1(t: Texto, base: Optional[float], pct_valor: bool = False) -> Optional[Tuple[float, Numero, str]]:
    """Valor alternativo del parámetro en un planteo de diseño: 'si vale 37', 'baja al 75%',
    'se incrementa en 10 kg', 'disminución del 10%', 'partidas malas ... inferior a 1.100'."""
    for i, n in t.libres():
        a, d = t.antes(n, 60), t.despues(n, 30)
        ora = t.oracion(n.ini)
        if _hay(r"(probabilidad|riesgo|confianza|seguridad)" + _R + r"{0,15}$", a) or _hay(r"^\s*(de )?probabilidad", d):
            continue
        if _hay(r"(desvio|desviacion)" + _R + r"{0,30}$", a):
            continue
        if base is not None and n.pct and not pct_valor and _hay(
                r"(disminucion|reduccion|aumento|incremento|disminuy|aument|increment|baj|sub|superior)[a-z]*( del| de| en| un)*\s*$", a):
            signo = -1 if _hay(r"(disminu|reduc|baj)", a[-30:]) else 1
            t.usar(i)
            return base * (1 + signo * n.fraccion), n, f"{'+' if signo > 0 else '−'}{fmt(n.valor)}% sobre μ₀"
        if base is not None and not n.pct and _hay(r"(incrementa|aumenta|disminuye|reduce|baja|sube)[a-z]* en\s*$", a):
            signo = -1 if _hay(r"(disminu|reduc|baj)", a[-25:]) else 1
            t.usar(i)
            return base + signo * n.valor, n, f"{'+' if signo > 0 else '−'}{fmt(n.valor)} respecto de μ₀"
        if _hay(r"(vale|es de|es del|baja al|baja a|sube al|sube a|sea de|inferior a|superior a|es inferior a|"
                r"es superior a|de)\s*$", a) and _hay(r"(\bsi\b|cuando|malas|aquellas|dicho parametro)", ora):
            if n.pct and not pct_valor:
                continue
            if _es_prob(n) and not n.pct and base is not None and base >= 1:
                continue
            t.usar(i)
            return n.valor, n, "valor alternativo de la media (μ₁)"
    return None


def extraer_proporcion(an: Analisis, t: Texto):
    """r (éxitos), p̂ (porcentaje muestral) y p₀ (porcentaje de referencia)."""
    for i, n in t.libres():
        a, d = t.antes(n, 60), t.despues(n, 50)
        ora = t.oracion(n.ini)
        if n.pct or (_hay(r"rating", a) and _hay(r"puntos", d)):
            valor = n.fraccion if n.pct else n.valor / 100
            if _hay(r"(probabilidad|riesgo|confianza|seguridad|significacion)", a[-25:] + d[:25]):
                continue
            ref = _hay(r"(actualmente|en la actualidad|se sabe|era del|es del|trabaja|establecido|supera|superior|"
                       r"inferior|mayor|menor|maximo|minimo|historic|normales|admitid|debe|se supone|con un|con el catalogo)",
                       ora) and not _hay(r"(muestra|se obtuvo|se ha registrado|se registro|encontr|se detecta|arroj|"
                                         r"registrado)", ora)
            if _hay(r"(supera|superior a|mayor que|menor que|inferior a|no supera)( el| al| los)?\s*$", a):
                ref = True
            clave = "p0" if ref else "p_hat"
            if clave not in an.datos:
                t.usar(i)
                _set(an, clave, valor, t, n, "proporción de referencia (p₀)" if ref else "proporción observada en la muestra (p̂)")
            continue
        if n.es_entero and not _es_prob(n) and "r" not in an.datos:
            if _hay(r"(encontr[a-z]*|hallaron|registr[a-z]*|reciben|comprobando que|detectaron|obtuvieron|se obtuvo)\s*$", a) or \
                    _hay(r"^\s*(unidad(es)? |piezas )?(defectuos|de ellos|mayores|pedidos|veces|inscript|exitos)", d) or \
                    _hay(r"se presento $", a):
                t.usar(i)
                _set(an, "r", int(n.valor), t, n, "cantidad de casos favorables / defectuosos en la muestra (r)")


# ---------------------------------------------------------------------------
# Extracción (2 poblaciones)
# ---------------------------------------------------------------------------

def _etiqueta_limpia(etq: str) -> str:
    etq = re.sub(r"[\s:]+$", "", etq)
    return etq[-40:].strip()


def extraer_dos_muestras(an: Analisis, t: Texto):
    listas = [l for l in t.listas if len(l.valores) >= 3]
    if len(listas) >= 2:
        l1, l2 = listas[0], listas[1]
        an.datos["datos1"], an.datos["datos2"] = l1.valores, l2.valores
        an.datos["nombre1"] = _etiqueta_limpia(l1.etiqueta) or "Muestra 1"
        an.datos["nombre2"] = _etiqueta_limpia(l2.etiqueta) or "Muestra 2"
        an.evidencias.append(Evidencia("datos1", l1.valores, t.texto[max(0, l1.ini - 30):l1.fin], "datos de la muestra 1"))
        an.evidencias.append(Evidencia("datos2", l2.valores, t.texto[max(0, l2.ini - 30):l2.fin], "datos de la muestra 2"))
        apareadas = _cuenta(P_APAREADAS, t.norm) > 0 and len(l1.valores) == len(l2.valores)
        _set(an, "apareadas", apareadas, t, None,
             "mismos individuos / pares medidos con ambos tratamientos → muestras apareadas" if apareadas
             else "grupos distintos → muestras independientes")
        return

    # Resumenes: n, x̄, S de cada muestra en orden de aparición (o con subíndice 1 / 2)
    ns, medias, desvios = [], [], []
    for i, n in enumerate(t.nums):
        a = t.antes(n, 45)
        if n.pct:
            continue
        if _hay(r"\bn\s*[12]?\s*=\s*$|\bn\s*=\s*\d+\s*$|muestras? (de|con) $|(sobre|con|en|de) (otras )?$", a) and n.es_entero \
                and (_hay(r"\bn\s*[12]?\s*=|\bn\s*=\s*\d+\s*$|muestra", a) or _hay(
                    r"^\s*(corridas|parcelas|piezas|ensayos|maquinas|animales|operarios|observaciones|meses|"
                    r"automoviles|potrillos|botellas|dias|muestras|conos)", t.despues(n))):
            ns.append((i, n))
        elif _hay(r"(media|promedio|medio)[^0-9]{0,40}$|\bx\s*[12]?\s*=\s*$|x\s*=\s*\d+(,\d+)?( [a-z]+)?\s*$|"
                  r"\)\s*:\s*$|\bx\s*\)?\s*:?\s*$", a) and not _hay(r"(desvio|desviacion)[^0-9]{0,15}$", a):
            medias.append((i, n))
        elif _hay(r"(desvio|desviacion)[^0-9]{0,40}$|\bs\s*[12]?\s*=\s*$|s\s*=\s*\d+(,\d+)?( [a-z]+)?\s*$", a):
            desvios.append((i, n))
    # tablas tipo 'Variedad “A”: 25 kg 3,4 kg' -> media y desvío en la misma fila
    if "cada uno" in t.norm or "cada una" in t.norm:
        m = re.search(r"(\d+) [a-z]+ cada un[oa]", t.norm)
        if m and len(ns) < 2:
            v = int(m.group(1))
            ns = [(None, Numero(v, m.start(1), m.end(1), False, m.group(1)))] * 2
    for k, (lista, clave) in enumerate(((ns, "n"), (medias, "xbar"), (desvios, "s"))):
        for j, (i, n) in enumerate(lista[:2]):
            if i is not None:
                t.usar(i)
            valor = int(n.valor) if clave == "n" else n.valor
            _set(an, f"{clave}{j + 1}", valor, t, n, f"{clave} de la muestra {j + 1}")
    if "n1" in an.datos and "n2" not in an.datos and _hay(r"\bn\s*=\s*\d+\s+\d+", t.norm):
        m = re.search(r"\bn\s*=\s*(\d+)\s+(\d+)", t.norm)
        an.datos["n1"], an.datos["n2"] = int(m.group(1)), int(m.group(2))
    an.datos.setdefault("nombre1", "Muestra 1")
    an.datos.setdefault("nombre2", "Muestra 2")
    an.datos.setdefault("apareadas", False)


# ---------------------------------------------------------------------------
# Extracción (chi-cuadrado)
# ---------------------------------------------------------------------------

def _filas_etiquetadas(texto: str) -> List[Tuple[str, List[float]]]:
    """Filas 'Etiqueta: n1 n2 n3' o 'Local 1 32 45 23 28' (mismo largo)."""
    filas = []
    for m in re.finditer(r"([A-Za-zÁÉÍÓÚáéíóúñ“”\"'.°º ]{2,40}?(?:\s\d{1,2})?)\s*:?\s+((?:\d[\d.,]*\s+){1,15}\d[\d.,]*)", texto):
        etq = m.group(1).strip(" :")
        nums = [n.valor for n in buscar_numeros(m.group(2))]
        if len(nums) >= 2:
            filas.append((etq, nums, m.start(), m.end()))
    return filas


def extraer_chi(an: Analisis, t: Texto):
    filas = _filas_etiquetadas(t.texto)
    # descartar filas índice (1 2 3 4 5 6)
    filas = [f for f in filas if f[1] != [float(i) for i in range(int(f[1][0]), int(f[1][0]) + len(f[1]))]]
    if an.tema == "chi_contingencia":
        # grupo de >= 2 filas consecutivas con el mismo largo
        mejor = []
        for f in filas:
            if mejor and len(f[1]) == len(mejor[-1][1]):
                mejor.append(f)
            elif len(mejor) < 2:
                mejor = [f]
        if len(mejor) >= 2:
            an.datos["tabla"] = [f[1] for f in mejor]
            an.evidencias.append(Evidencia("tabla", an.datos["tabla"], t.texto[mejor[0][2]:mejor[-1][3]],
                                           "filas de la tabla: " + ", ".join(f[0] for f in mejor)))
            return
        # dos proporciones narradas: 'muestra de 250 ... 20 defectuosos', '32 postes de cada uno ... 10 y 20'
        tot = [n for n in t.nums if n.es_entero and not n.pct and _hay(r"(muestra|muestras|total)[^0-9]{0,15}$|cada un", t.antes(n, 30) + t.despues(n, 20))]
        cuentas = [n for n in t.nums if n.es_entero and not n.pct and n not in tot
                   and _hay(r"(arroj[a-z]* un resultado de|reponer|encontr[a-z]*|y)\s*$", t.antes(n, 30))]
        if tot and len(cuentas) >= 2:
            n1 = tot[0].valor
            n2 = tot[1].valor if len(tot) > 1 else n1
            r1, r2 = cuentas[0].valor, cuentas[1].valor
            an.datos["tabla"] = [[r1, n1 - r1], [r2, n2 - r2]]
            an.evidencias.append(Evidencia("tabla", an.datos["tabla"], "",
                                           f"2 grupos: {fmt(r1)} de {fmt(n1)} y {fmt(r2)} de {fmt(n2)} "
                                           "(filas: grupo; columnas: sí / no)"))
            an.avisos.append("Revisá la tabla: se armó con (éxitos, fracasos) de cada grupo a partir del texto.")
        return
    # bondad de ajuste
    cand = [f for f in filas if _hay(r"(ocurrencias|observad|cantidad|frecuencia|instalaciones|observaciones)", normalizar(f[0]))]
    if cand:
        etq, obs, ini, fin = cand[0]
        an.datos["observados"] = obs
        an.evidencias.append(Evidencia("observados", obs, t.texto[ini:fin], "frecuencias observadas"))
    else:
        cuentas = [n for n in t.nums if n.es_entero and not n.pct and _hay(r"(encuentra|resultados)[^.]{0,80}$", t.antes(n, 90))]
        if len(cuentas) >= 2:
            an.datos["observados"] = [n.valor for n in cuentas]
    obs = an.datos.get("observados")
    k = len(obs) if obs else 0
    if _hay(r"ruleta", t.norm) and k == 3:
        an.datos["proporciones"] = [1 / 37, 18 / 37, 18 / 37]
        an.evidencias.append(Evidencia("proporciones", "1/37, 18/37, 18/37", "", "ruleta equilibrada: 0, negro, colorado"))
    elif _hay(r"igualmente|uniforme|dado|por igual|equilibrad", t.norm) and k:
        an.datos["proporciones"] = [1 / k] * k
        an.evidencias.append(Evidencia("proporciones", f"1/{k} cada una", "", "modelo uniforme (todas las categorías iguales)"))
    else:
        pcts = [n for n in t.nums if n.pct]
        if k and len(pcts) == k and abs(sum(n.valor for n in pcts) - 100) < 0.5:
            an.datos["proporciones"] = [n.fraccion for n in pcts]
            an.evidencias.append(Evidencia("proporciones", an.datos["proporciones"], "",
                                           "porcentajes del patrón teórico / histórico"))
        elif k:
            an.avisos.append("El modelo teórico no es uniforme ni viene dado en %: calculá las frecuencias "
                             "esperadas Fe con el modelo (Normal, Poisson, ...) y cargalas a mano.")
    an.datos.setdefault("p_estimados", 0)


# ---------------------------------------------------------------------------
# Clasificación de incisos
# ---------------------------------------------------------------------------

def clasificar_inciso(norm: str, tema: str, contexto: str) -> Tuple[str, str]:
    """Devuelve (tipo, razón)."""
    if tema in ("regresion", "desconocido"):
        return "no_soportado", "La app no resuelve este tema; mirá los ejercicios parecidos de la guía."
    if _hay(r"(dibujar|trazar|grafic|curvas?|tablas? de valores para las curvas)", norm) and \
            _hay(r"(curva|caracteristica operativa|potencia|oc\b)", norm) and \
            _hay(r"(calcular|cual|hallar)[^.?]{0,20}probabilidad", norm):
        return "beta", "Pide una probabilidad (β / potencia) y además la curva: se calculan ambas."
    if _hay(r"(dibujar|trazar|grafic|curvas?|tablas? de valores para las curvas)", norm) and \
            _hay(r"(curva|caracteristica operativa|potencia|oc\b)", norm):
        return "curva", "Pide dibujar la curva OC / de potencia: se arma la tabla de puntos (μ, β, 1-β)."
    if _hay(r"justificar conceptualmente|explicar|por que|que se puede decir del", norm) and len(norm) < 80:
        return "no_soportado", "Pregunta conceptual: respondé con la teoría (criterio del planteo de H0)."
    if tema in ("chi_contingencia", "chi_ajuste"):
        return "ensayo", "Es un contraste χ²: se compara χ² calculado contra el crítico."
    if _hay(r"(hipotesis nula apropiada|condicion de rechazo|regla de decision|plan de muestreo|sistema de muestreo|"
            r"valor critico|limites de control|cuantas defectuosas se deberan|cual es la resistencia media muestral minima)",
            norm) or (_hay(r"(indicar|establecer|plantear) la hipotesis", norm) and not _hay(r"(realizar|efectuar) el ensayo", norm)):
        if not _hay(r"(realizar|efectuar) el ensayo|que decision|se aconseja|determinar si", norm):
            return "diseno", ("Pide diseñar el ensayo: H0 (criterio), condición de rechazo (valor crítico), "
                              "n y regla de decisión.")
    if _hay(r"(cuant[oa]s? [a-z ]{0,40}(mas|habria que|deberan|deberian|se deberan)|tamano (adecuado |necesario )?de "
            r"(la )?muestra|que tamano|cuantas? [a-z]+ habria|calcular (el )?(nuevo )?tamano|recalcular tamano|"
            r"durante cuantos|a cuantos|como se disminuye el error|tamano de muestra (es|extraido))", norm):
        return "n", "Pregunta cuántas unidades hacen falta: tamaño de muestra (y Δn si ya hay una muestra)."
    if _hay(r"(maxim[oa]|minim[oa])", norm) and _hay(r"(con una probabilidad de|confianza|estimar|con (un )?\d+ ?% de riesgo)", norm) \
            and not _hay(r"(tamano|cuant)", norm):
        return "ic", "Pide un valor máximo / mínimo del parámetro con cierta confianza: límite de confianza UNILATERAL."
    if _hay(r"^\W*(se considera|se puede|puede|se aconseja|aconseja|es correct|existe|se recomienda|asumiendo|"
            r"si se establece|con un|se justifica)", norm) and not _hay(r"(cual|calcular|hallar)[^.?]{0,30}probabilidad", norm):
        return "ensayo", "Pide tomar una decisión sobre una afirmación: ensayo de hipótesis."
    if _hay(r"(cual|que) (seria|sera|es) la (conclusion|decision)", norm):
        return "ensayo", "Pide la conclusión / decisión: ensayo de hipótesis."
    if _hay(r"(cual|calcular|hallar|determinar|que)[^.?]{0,30}(probabilidad|error de tipo ii|potencia)|error de tipo ii|"
            r"probabilidad de (no )?(detectar|aceptar|rechazar|detener|revisar)", norm):
        return "beta", "Pide una probabilidad de error: β (no detectar) o potencia 1-β (detectar)."
    if _hay(r"(estimar|intervalo|limites de confianza|entre que (valores|limites)|dentro de que limites|"
            r"diferencia (de aumento de peso )?minima|incremento porcentual|desviacion estandar maxima|"
            r"cual es el incremento|cual es la diferencia)", norm):
        return "ic", "Pide estimar el parámetro: intervalo de confianza P(A ≤ θ ≤ B) = 1-α."
    if _hay(r"(se puede|puede|se aconseja|aconseja|se recomienda|recomendaria|es correct|se considera|considera|"
            r"existe|hay (razon|evidencia)|asegurar|afirmar|aseguraria|decision|concluyente|se continuaria|"
            r"es posible|se justifica|se rechaza|ensayar|verificar|determinar si|comprobar|cumple|se arriba|"
            r"indique las conclusiones|que se puede decir|cual sera la conclusion|que decision)", norm + " " + contexto):
        return "ensayo", "Pide tomar una decisión sobre una afirmación: ensayo de hipótesis."
    return "no_soportado", "No se reconoció qué pide: elegí el tipo a mano."


def detectar_cola(norm: str, planteo_norm: str, tema: str, datos: dict) -> Tuple[str, str]:
    """Dirección de H1 según las palabras del inciso (y, si no alcanza, del planteo)."""
    for texto, donde in ((norm, "inciso"), (planteo_norm, "planteo")):
        # especificaciones de control (criterio optimista)
        if _hay(r"(mayor o igual|por lo menos|como minimo|minimo admisible|minima es de|resistencia media minima|"
                r"no menos de)", texto) and donde == "planteo" and not _hay(r"(aument|increment)", texto):
            return "izquierda", "La especificación es un mínimo (≥ μ₀): se rechaza si la muestra da BAJO → cola izquierda."
        if _hay(r"(menor o igual|como maximo|a lo sumo|no debe superar|no mas de)", texto) and donde == "planteo" \
                and not _hay(r"(disminu|reduc)", texto):
            return "derecha", "La especificación es un máximo (≤ valor): se rechaza si la muestra da ALTO → cola derecha."
        mas, menos, dist = _cuenta(P_MAS, texto), _cuenta(P_MENOS, texto), _cuenta(P_DISTINTO, texto)
        if _hay(r"limites de control|dentro de que limites|aumentando o disminuyendo|\bdiferente de\b", texto):
            return "bilateral", "Pide límites de control / si difiere del valor nominal (sin dirección) → bilateral."
        if tema == "media" and datos.get("mu1") is not None and datos.get("mu0") is not None and not \
                _hay(r"(diferente|distint|difier|desajust|aumentando o disminuyendo|se altera|limites de control)",
                     norm + " " + planteo_norm):
            if datos["mu1"] < datos["mu0"]:
                return "izquierda", "La alternativa (μ₁) está por debajo de μ₀ → H1: μ < μ₀ → cola izquierda."
            return "derecha", "La alternativa (μ₁) está por encima de μ₀ → H1: μ > μ₀ → cola derecha."
        if dist and not (mas or menos):
            return "bilateral", "Pregunta si el parámetro cambió / es distinto (sin decir hacia dónde) → bilateral."
        if mas > menos:
            return "derecha", "Lo que se quiere probar es un AUMENTO (mayor, supera, excede...) → H1: > → cola derecha."
        if menos > mas:
            return "izquierda", "Lo que se quiere probar es una DISMINUCIÓN (menor, reduce...) → H1: < → cola izquierda."
        if mas and menos and tema == "media" and datos.get("mu1") is not None and datos.get("mu0") is not None:
            if datos["mu1"] < datos["mu0"]:
                return "izquierda", "La alternativa (μ₁) está por debajo de μ₀ → cola izquierda."
            return "derecha", "La alternativa (μ₁) está por encima de μ₀ → cola derecha."
    # sin pistas: hacia donde apunta la muestra
    ref = {"media": ("xbar", "mu0"), "varianza": ("desvio", "sigma0"), "proporcion": ("p_hat", "p0")}.get(tema)
    if ref and ref[0] in datos and ref[1] in datos:
        obs, val = datos[ref[0]], datos[ref[1]]
        if tema == "proporcion" and "p_hat" not in datos and "r" in datos and datos.get("n"):
            obs = datos["r"] / datos["n"]
        return ("derecha" if obs > val else "izquierda"), "Sin palabras de dirección: se toma el lado hacia el que apunta la muestra."
    if _hay(r"(debe ser|valor estandar|nominal|bajo control)", planteo_norm):
        return "bilateral", "Valor nominal a controlar sin dirección → bilateral."
    return "bilateral", "Sin pistas de dirección → bilateral (revisalo)."


def detectar_criterio(norm: str) -> Tuple[Optional[str], str]:
    pes, opt = _cuenta(P_PESIMISTA, norm), _cuenta(P_OPTIMISTA, norm)
    if pes == 0 and opt == 0:
        return None, ""
    if pes >= opt:
        return "pesimista", ("Hay una inversión / cambio / producto nuevo en juego: criterio PESIMISTA, H0 supone "
                             "que el cambio NO funciona y se exige evidencia para rechazarla.")
    return "optimista", ("Es un control de recepción / de proceso: criterio OPTIMISTA, H0 supone que el lote o "
                         "proceso CUMPLE la especificación.")


# ---------------------------------------------------------------------------
# Parámetros de cada inciso
# ---------------------------------------------------------------------------

def _valor_alternativo(t: Texto, base: Optional[float], tema: str) -> Optional[Tuple[float, Numero, str]]:
    """μ₁ / σ₁ / p₁ del inciso: 'si la media es de 11', 'aumenta en 5 kg', 'un 8% superior'."""
    for i, n in t.libres():
        a, d = t.antes(n, 60), t.despues(n, 40)
        if _hay(r"(probabilidad|riesgo|confianza|valga)[^0-9]{0,12}$", a):
            continue
        rel = _hay(r"(aument|increment|disminu|reduc|baj|desplazamiento|mejor)[a-z]*( la [a-z]+ media)?( en| de| del)?( un| el)?"
                   r"( mas de)?\s*$", a) or _hay(r"^\s*(superior|mayor|inferior|menor|mas|menos)", d)
        if n.pct and tema != "proporcion" and rel and base is not None:
            signo = -1 if _hay(r"(disminu|reduc|baj|inferior|menor|menos)", a[-30:] + d[:15]) else 1
            t.usar(i)
            return base * (1 + signo * n.fraccion), n, f"{'+' if signo > 0 else '−'}{fmt(n.valor)}% sobre el valor de referencia"
        if tema == "proporcion" and _hay(r"punto", d) and base is not None:
            signo = -1 if _hay(r"(disminu|reduc|baj)", a) else 1
            t.usar(i)
            return base + signo * n.valor / 100, n, f"{'+' if signo > 0 else '−'}{fmt(n.valor)} puntos porcentuales"
        if not n.pct and rel and base is not None and _hay(r"(aument|increment|disminu|reduc|baj)[a-z]* (en|de)\s*$", a):
            signo = -1 if _hay(r"(disminu|reduc|baj)", a) else 1
            t.usar(i)
            return base + signo * n.valor, n, f"{'+' if signo > 0 else '−'}{fmt(n.valor)} respecto del valor de referencia"
        if _hay(r"(es|sea|fuera|fuese|vale|valiera|de|a|al|tuviera una probabilidad de|en promedio|promedio)\s*$", a) or n.pct:
            valor = n.fraccion if (tema == "proporcion" and (n.pct or n.valor < 1)) else n.valor
            if tema == "proporcion" and not n.pct and n.valor >= 1:
                continue
            t.usar(i)
            return valor, n, "valor alternativo del parámetro"
    return None


def _prob_pedida(norm: str) -> str:
    if _hay(r"(no detectar|no efectuar|no concretar|no iniciar|no detener|no implementar|no cambiar|no revisarlo|"
            r"no efectuar el ajuste|aceptar|de que el lote sea aceptado|error de tipo ii|no adoptar|no comprar)", norm):
        return "beta"
    return "potencia"


def extraer_params_inciso(inc: Inciso, an: Analisis, previo: Dict):
    t = Texto(inc.texto)
    norm = t.norm
    p = inc.params
    tema = an.tema

    if inc.tipo in ("n", "diseno") and tema in ("media", "varianza", "proporcion"):
        probs = _probs_diseno(t)
        if len(probs) >= 2:
            a_, b_ = _asignar_alpha_beta(t, probs)
            p["alpha"], p["beta"] = a_, b_
            inc.tipo = "diseno"
            inc.razones.append(f"El inciso fija dos probabilidades: α = {fmt(a_)} y β = {fmt(b_)} → se diseña el ensayo.")

    r = extraer_alpha(t) if "alpha" not in p else None
    if r:
        p["alpha"] = r[0]
        inc.razones.append(f"α = {fmt(r[0])} ({r[2]}).")

    # 'si no se conociera el desvío' / 'considerando que el desvío no se conoce' -> usar S y t
    if _hay(r"(no se conociera|no se conoce|se considera desconocido|desconocido)", norm) and _hay(r"desvio", norm):
        p["usar_S"] = True
        inc.razones.append("El inciso pide suponer σ DESCONOCIDO: se usa el desvío muestral S y t de Student.")

    # datos base que aparecen recién en el inciso (p. ej. 'se obtuvo una media de 15')
    if tema == "media" and inc.tipo in ("ic", "ensayo", "n") and not _hay(r"probabilidad", norm):
        sub = Analisis(inc.texto, tema=tema)
        extraer_media(sub, t)
        extraer_desvio(sub, t)
        for k in ("xbar", "desvio", "sigma_conocido"):
            if k in sub.datos and k not in an.datos:
                an.datos[k] = sub.datos[k]
                an.evidencias += [e for e in sub.evidencias if e.clave == k]
        if "mu0" in sub.datos:
            p["mu0"] = sub.datos["mu0"]
    if tema == "proporcion" and inc.tipo in ("ic", "n", "ensayo"):
        sub = Analisis(inc.texto, tema=tema)
        extraer_proporcion(sub, t)
        for k in ("r", "p_hat"):
            if k in sub.datos:
                p[k] = sub.datos[k]
                inc.razones.append(f"Dato del inciso: {k} = {fmt(sub.datos[k])}.")
    if tema == "varianza":
        for i, n in t.libres():
            if _hay(r"(mayor|menor|superior|inferior|mayor de|varianza de|desvio de)[a-z ]{0,10}\s*$", t.antes(n, 30)) \
                    and inc.tipo == "ensayo":
                t.usar(i)
                es_var = _hay(r"varianza", t.antes(n, 40)) or _hay(r"^\s*mm\s*2|cm\s*2", t.despues(n, 8)) and _hay("varianza", norm)
                p["sigma0"] = sqrt(n.valor) if es_var else n.valor
                inc.razones.append(f"Valor de referencia del desvío en el inciso: σ₀ = {fmt(p['sigma0'])}.")
                break

    if inc.tipo in ("ensayo", "beta", "diseno", "curva"):
        cola, razon = detectar_cola(norm, normalizar(an.planteo), tema, an.datos)
        sin_pistas = _cuenta(P_MAS + P_MENOS + P_DISTINTO, norm) == 0
        if inc.tipo in ("beta", "curva") and "tail" in previo or (sin_pistas and "tail" in previo and
                                                                   _hay(r"misma conclusion|idem|anterior", norm)):
            cola, razon = previo["tail"], "Se mantiene la cola del ensayo del inciso anterior."
        p["tail"] = cola
        inc.razones.append(razon)

    if inc.tipo == "ic":
        if _hay(r"(total|peso total|produccion total)", norm) and "N" in an.datos:
            p["total"] = True
            inc.razones.append("Pide el TOTAL poblacional: se multiplica el IC de la media por N.")
        if _hay(r"(maxim[oa])", norm):
            p["cota"] = "sup"
            inc.razones.append("Pide un valor MÁXIMO: límite de confianza unilateral superior (α entero en una cola).")
        elif _hay(r"(minim[oa])", norm):
            p["cota"] = "inf"
            inc.razones.append("Pide un valor MÍNIMO: límite de confianza unilateral inferior (α entero en una cola).")

    if inc.tipo == "n":
        r = extraer_error(t)
        if r:
            clave, valor, n = r
            p[clave] = valor
            inc.razones.append(f"{'Error admitido e' if clave == 'e' else 'Reducción pedida'} = {fmt(valor)}.")
        if tema == "varianza":
            m = re.search(r"(doble|triple)", norm)
            if m:
                p["relacion"] = 2.0 if m.group(1) == "doble" else 3.0
                inc.razones.append(f"El límite superior debe ser el {m.group(1)} del inferior → R' = {fmt(p['relacion'])}.")
            else:
                m2 = [n for n in t.nums if n.pct and _hay(r"mayor", t.despues(n, 20))]
                if m2:
                    p["relacion"] = 1 + m2[0].fraccion
                    inc.razones.append(f"Límite superior {fmt(m2[0].valor)}% mayor que el inferior → R' = {fmt(p['relacion'])}.")
        if _hay(r"(probabilidad|valga|potencia)", norm):
            # n para una potencia fijada: 'si se pretende que la probabilidad anterior valga 0,10'
            for i, n in t.libres():
                if _es_prob(n):
                    t.usar(i)
                    prob_prev = previo.get("prob", "beta")
                    p["beta"] = round(n.fraccion if prob_prev == "beta" else 1 - n.fraccion, 10)
                    inc.razones.append(f"Pide n para que la probabilidad anterior valga {fmt(n.fraccion)} → "
                                       f"β = {fmt(p['beta'])}.")
                    inc.tipo = "diseno"
                    break

    if inc.tipo in ("beta", "diseno", "curva"):
        base = {"media": an.datos.get("mu0"), "varianza": an.datos.get("sigma0"),
                "proporcion": an.datos.get("p0")}.get(tema)
        r = _valor_alternativo(t, base, tema)
        clave = {"media": "mu1", "varianza": "sigma1", "proporcion": "p1"}.get(tema, "mu1")
        if r:
            valor, n, motivo = r
            if tema == "varianza" and _hay(r"varianza", norm):
                valor = sqrt(valor)
            p[clave] = valor
            inc.razones.append(f"{clave.replace('1', '₁')} = {fmt(valor)} ({motivo}).")
        if inc.tipo == "beta":
            if _hay(r"(dibujar|trazar|grafic)[^.?]{0,40}curva", norm):
                p["con_curva"] = True
            p["prob"] = _prob_pedida(norm)
            inc.razones.append("Pide β (no rechazar H0 siendo falsa)." if p["prob"] == "beta"
                               else "Pide la potencia 1-β (detectar / rechazar H0 siendo falsa).")

    if an.datos.get("doble"):
        nombra_los_dos = _hay(r"(promedio|media)", norm) and _hay(r"(desvio|desviacion|varianza)", norm)
        if (inc.tipo == "ensayo" and not _hay(r"(desvio|desviacion|varianza)", norm)) or \
                (inc.tipo == "ic" and nombra_los_dos):
            p["ambos"] = True
            inc.razones.append("Se piden los dos parámetros (doble condición): se calcula para la media y para el desvío."
                               if inc.tipo == "ic" else
                               "Doble condición: se hacen los dos ensayos (μ y σ); la recomendación exige rechazar ambas H0.")

    if tema == "dos_medias" and inc.tipo in ("ensayo",):
        for i, n in t.libres():
            a, d = t.antes(n, 50), t.despues(n, 40)
            if n.pct and _hay(r"(en|un)\s*$", a):
                p["delta0_pct"] = n.fraccion
                inc.razones.append(f"La diferencia a probar es un {fmt(n.valor)}% del valor de la muestra de referencia.")
                break
            if _hay(r"(en|de|superior en|mayor|minima de|por mas de|mas de)\s*$", a) or \
                    _hay(r"^\s*[a-z]*\s*(al menos|como minimo|por lo menos)", d):
                t.usar(i)
                p["delta0"] = n.valor
                inc.razones.append(f"Diferencia de referencia δ₀ = {fmt(n.valor)}.")
                break


# ---------------------------------------------------------------------------
# Diseño de ensayos (dos probabilidades en el planteo)
# ---------------------------------------------------------------------------

def extraer_diseno(an: Analisis, t: Texto):
    """Planteos tipo 'detener con probabilidad 0,1 si μ=38; con 0,95 si μ=37'.

    Toma las probabilidades en orden: la primera es α (condición de H0), la
    segunda es β (o la potencia si es > 0,5). Las medias: μ₀ y μ₁.
    """
    probs = []
    for i, n in enumerate(t.nums):
        if i in t.usados or not _es_prob(n):
            continue
        a, d = t.antes(n, 60), t.despues(n, 50)
        ctx = a[-70:] + " " + d[:40]
        if _hay(r"^\s*(kg|g|gr|gramos|cm|mm|m|metros|litros|hs|horas|minutos|segundos|u\$s|dolares|watts?|kwh|unidades)\b", d):
            continue
        if _hay(r"(incrementa|aumenta|disminuye|reduce|baja|sube)[a-z]* (en|al|a)\s*$|(baja|sube) (al|a)\s*$|\bes del\s*$", a):
            continue
        if _hay(r"(probabilidad|riesgo|rechac|rechaz|deten|seguridad|detect|implement|adopt|concret|equivocad|"
                r"erronea|indebid)", ctx) and \
                not _hay(r"(defectuos|de unidades|confianza)", d[:25]):
            probs.append((i, n))
    return probs


def _probs_diseno(t: Texto):
    return extraer_diseno(None, t)


def _asignar_alpha_beta(t: Texto, probs):
    """De dos probabilidades, cuál es α (riesgo si H0 es cierta) y cuál es β / potencia."""
    (i1, n1), (i2, n2) = probs[0], probs[1]
    es_a1 = _alpha_de(t, i1, n1) is not None
    es_a2 = _alpha_de(t, i2, n2) is not None
    if es_a2 and not es_a1:
        (i1, n1), (i2, n2) = (i2, n2), (i1, n1)
    t.usar(i1)
    t.usar(i2)
    v1, v2 = n1.fraccion, n2.fraccion
    return round(v1 if v1 <= 0.5 else 1 - v1, 10), round(v2 if v2 <= 0.5 else 1 - v2, 10)


RE_COND_CONTROL = re.compile(
    r"(?:media|promedio|parametro|rendimiento)[^0-9;]{0,40}?(\d+(?:[.,]\d+)?)[^;]{0,60}?\b(no )?deten[a-z]*"
    r"[^0-9;]{0,50}?probabilidad (?:de |del )?(\d+(?:[.,]\d+)?\s*%?)")


RE_DOBLE = re.compile(
    r"(promedio|media)[^.;]{0,60}?(inferior|superior|menor|mayor|supera|exced|no mas|como maximo|como minimo)"
    r"[^.;]{0,50}?\by\b[^.;]{0,30}?(desvio|desviacion|varianza|variabilidad)[^.;]{0,40}?"
    r"(inferior|superior|menor|mayor|supera|exced|no mas|como maximo|como minimo)"
    r"|(desvio|desviacion|varianza|variabilidad)[^.;]{0,60}?(inferior|superior|menor|mayor|supera|exced|no mas|como maximo)"
    r"[^.;]{0,50}?\by\b[^.;]{0,30}?(promedio|media)[^.;]{0,40}?(inferior|superior|menor|mayor|supera|exced|no mas|como maximo)")


def doble_condicion(an: Analisis, t: Texto) -> bool:
    """'si el tiempo promedio es inferior a 1,5 y su desvío es inferior a 0,09 se compra': son DOS ensayos
    (uno sobre μ y otro sobre σ) y la decisión exige rechazar las dos H0."""
    m = RE_DOBLE.search(t.norm)
    if not m or not an.datos.get("datos") and "xbar" not in an.datos:
        return False
    if an.tema == "media" and "sigma0" not in an.datos and "desvio" in an.datos and an.datos.get("datos"):
        an.datos["sigma0"] = an.datos.pop("desvio")
        an.datos.pop("sigma_conocido", None)
        for e in an.evidencias:
            if e.clave == "desvio":
                e.clave, e.motivo = "sigma0", "umbral del desvío (σ₀) de la segunda condición"
        an.tema = "varianza"
    if an.tema != "varianza" or "sigma0" not in an.datos:
        return False
    extraer_media(an, t, solo_mu0=True)
    if "mu0" not in an.datos:
        return False
    an.datos["doble"] = True
    an.evidencias.append(Evidencia("doble", True, t.norm[m.start():m.end()],
                                   "la decisión depende de la media Y del desvío: hay que hacer los dos ensayos"))
    an.razones_tema.append("Doble condición (media y desvío): se ensayan μ y σ por separado y la decisión exige "
                           "rechazar las dos H0.")
    return True


def diseno_control(an: Analisis, planteo: str) -> bool:
    """Sistemas de control: 'si μ = a, (no) detener con probabilidad p; si μ = b, (no) detener con probabilidad q'.

    Criterio de la cátedra (optimista, guía I-16): H0 = el proceso funciona bien y
    RECHAZAR H0 = DETENER el proceso. Por eso H0 es el valor de μ con el que
    detener es poco probable, α = P(detener | μ₀) y β = P(no detener | μ₁). Así no
    importa en qué orden el enunciado da las condiciones ni si las da como
    'detener' o 'no detener'.
    """
    norm = normalizar(planteo)
    conds = []
    for clausula in re.split(r";|\bpero\b", norm):
        m = RE_COND_CONTROL.search(clausula)
        if not m:
            continue
        mu = parse_num(m.group(1))
        prob_txt = m.group(3).strip()
        prob = parse_num(prob_txt.rstrip("% ").strip()) / (100 if prob_txt.endswith("%") else 1)
        if mu is None or prob is None or not 0 < prob < 1:
            continue
        p_detener = 1 - prob if m.group(2) else prob
        conds.append((mu, p_detener, m.group(0)))
    if len(conds) != 2 or conds[0][0] == conds[1][0]:
        return False
    (mu0, pd0, f0), (mu1, pd1, f1) = sorted(conds, key=lambda c: c[1])
    if not (pd0 < 0.5 < pd1):
        return False
    an.datos.update(mu0=mu0, mu1=mu1, alpha=round(pd0, 10), beta=round(1 - pd1, 10), control=True,
                   accion_rechazo="se detiene el proceso", accion_no_rechazo="el proceso sigue")
    an.evidencias = [e for e in an.evidencias if e.clave not in ("alpha", "beta", "mu0", "mu1")]
    an.evidencias += [
        Evidencia("mu0", mu0, f0, "con esta media el proceso anda bien: detener sería un error → H0"),
        Evidencia("alpha", pd0, f0, f"α = P(detener | μ = {fmt(mu0)}) = {fmt(pd0)}"),
        Evidencia("mu1", mu1, f1, "con esta media hay que detener → alternativa μ₁"),
        Evidencia("beta", 1 - pd1, f1, f"β = P(no detener | μ = {fmt(mu1)}) = 1 - {fmt(pd1)} = {fmt(1 - pd1)}"),
    ]
    an.criterio = "optimista"
    an.criterio_razon = (f"Sistema de control: H0 supone que el proceso funciona bien (μ = {fmt(mu0)}) y RECHAZAR H0 = "
                         f"DETENER el proceso. α es la probabilidad de detenerlo cuando anda bien ({fmt(pd0)}) y β la "
                         f"de no detenerlo cuando μ = {fmt(mu1)} ({fmt(1 - pd1)}). Ojo: no importa el orden en que el "
                         f"enunciado da las condiciones.")
    return True


PARES_REF = (("mu0", "mu1"), ("sigma0", "sigma1"), ("p0", "p1"))
SIMBOLO = {"mu0": "μ₀", "mu1": "μ₁", "sigma0": "σ₀", "sigma1": "σ₁", "p0": "p₀", "p1": "p₁"}
VERBOS_ACCION = r"(deten|compr|acept|implement|adopt|concret|inici|cambi|revis)"


def cambiar_criterio(an: Analisis, nuevo: str) -> List[str]:
    """Pasa el planteo de H0 de optimista a pesimista (o al revés). Devuelve qué se cambió.

    - Si el planteo fija las DOS condiciones (α y β), se intercambian el valor de H0
      con el alternativo y α con β: H0 pasa a ser la otra condición.
    - Las colas unilaterales se invierten (H1 apunta al otro lado).
    - Si hay una acción atada a la decisión ('detener', 'comprar'...), rechazar H0
      pasa a significar la acción contraria, así que las probabilidades pedidas en
      términos de esa acción cambian de β a potencia (y al revés).
    """
    if nuevo not in ("optimista", "pesimista") or nuevo == an.criterio:
        return []
    cambios: List[str] = []
    d = an.datos
    if d.get("alpha") is not None and d.get("beta") is not None:
        for a, b in PARES_REF:
            if d.get(a) is not None and d.get(b) is not None:
                d[a], d[b] = d[b], d[a]
                cambios.append(f"H0 pasa a ser {SIMBOLO[a]} = {fmt(d[a])} y la alternativa {SIMBOLO[b]} = {fmt(d[b])}.")
                for e in an.evidencias:
                    if e.clave in (a, b):
                        e.clave = b if e.clave == a else a
        d["alpha"], d["beta"] = d["beta"], d["alpha"]
        for inc in an.incisos:  # los incisos del diseño guardaron su copia de α / β
            p = inc.params
            viejo = {"alpha": d["beta"], "beta": d["alpha"]}
            for k in ("alpha", "beta"):
                if p.get(k) is not None and abs(p[k] - viejo[k]) < 1e-12:
                    p[k] = d[k]
        cambios.append(f"α y β se intercambian: α = {fmt(d['alpha'])}, β = {fmt(d['beta'])}.")
        for e in an.evidencias:
            if e.clave in ("alpha", "beta"):
                e.clave = "beta" if e.clave == "alpha" else "alpha"
    if d.get("control"):
        acciones = (d.get("accion_rechazo", "se detiene el proceso"), d.get("accion_no_rechazo", "el proceso sigue"))
        d["accion_rechazo"], d["accion_no_rechazo"] = acciones[1], acciones[0]
        cambios.append(f"Ahora rechazar H0 significa: {d['accion_rechazo']}.")
    giro = {"derecha": "izquierda", "izquierda": "derecha"}
    for inc in an.incisos:
        p = inc.params
        if p.get("tail") in giro:
            p["tail"] = giro[p["tail"]]
            cambios.append(f"{inc.letra}) la cola pasa a ser {p['tail']}.")
        if inc.tipo == "beta" and p.get("prob") and _hay(VERBOS_ACCION, normalizar(inc.texto)):
            p["prob"] = "potencia" if p["prob"] == "beta" else "beta"
            cambios.append(f"{inc.letra}) lo que pide ahora es {'β' if p['prob'] == 'beta' else 'la potencia 1-β'} "
                           f"(la acción del enunciado quedó del otro lado de la decisión).")
        inc.que_pide = explicar(inc, an)
    an.criterio = nuevo
    an.criterio_razon = ("Elegido a mano. " + ("PESIMISTA: H0 supone lo desfavorable (el cambio no funciona / el valor "
                                               "malo) y se exige evidencia para rechazarla." if nuevo == "pesimista" else
                                               "OPTIMISTA: H0 supone que el proceso / lote cumple (el valor bueno)."))
    return cambios


def completar_diseno(an: Analisis, t: Texto) -> bool:
    """Si el planteo fija dos probabilidades (α y β), es un problema de diseño del ensayo."""
    probs = _probs_diseno(t)
    if len(probs) < 2:
        return False
    a_, b_ = _asignar_alpha_beta(t, probs)
    an.datos["alpha"] = a_
    an.datos["beta"] = b_
    an.evidencias = [e for e in an.evidencias if e.clave not in ("alpha", "beta")]
    an.evidencias.append(Evidencia("alpha", a_, "", "probabilidad de rechazar H0 siendo cierta → α"))
    an.evidencias.append(Evidencia("beta", b_, "", "probabilidad de no detectar la alternativa → β "
                                                   "(si el enunciado da la potencia, β = 1 - potencia)"))
    return True


# ---------------------------------------------------------------------------
# Qué pide cada inciso (explicación en castellano)
# ---------------------------------------------------------------------------

PARAM = {"media": "la media poblacional μ", "varianza": "la varianza σ² / el desvío σ",
         "proporcion": "la proporción poblacional p", "dos_varianzas": "la relación de varianzas σ₁²/σ₂²",
         "dos_medias": "la diferencia de medias δ = μ₁ - μ₂"}


def explicar(inc: Inciso, an: Analisis) -> str:
    tema, p, d = an.tema, inc.params, an.datos
    alpha = p.get("alpha", d.get("alpha"))
    par = PARAM.get(tema, "el parámetro")
    if p.get("ambos") and inc.tipo == "ic":
        conf = f" con un {fmt((1 - alpha) * 100)}% de confianza" if alpha else ""
        return (f"Estimar LOS DOS parámetros{conf}: la media μ (σ desconocido → t de Student, ν = n-1) y el desvío σ "
                f"(χ² con ν = n-1, intervalo no simétrico).")
    if p.get("ambos") and inc.tipo == "ensayo":
        cola = {"derecha": ">", "izquierda": "<", "bilateral": "≠"}.get(p.get("tail"), "?")
        return (f"Doble condición: hacer DOS ensayos, uno sobre la media μ (t de Student) y otro sobre el desvío σ (χ²), "
                f"ambos con H1 '{cola}'. Solo se recomienda si se rechazan las DOS hipótesis nulas.")
    if inc.tipo == "ic":
        conf = f" con un {fmt((1 - alpha) * 100)}% de confianza" if alpha else ""
        extra = ""
        if tema == "media":
            extra = (" Como σ es conocido se usa Z." if d.get("sigma_conocido") else " Como σ no se conoce se usa S y t de Student (ν = n-1).")
        elif tema == "varianza":
            extra = " Se usa χ² con ν = n-1 (el intervalo NO es simétrico)."
        elif tema == "proporcion":
            extra = " La cátedra usa el modelo exacto (Beta / F)."
        total = " Se pide el TOTAL: multiplicá los límites por N." if p.get("total") else ""
        return f"Estimar {par}{conf} mediante un intervalo de confianza.{extra}{total}"
    if inc.tipo == "n":
        if "e" in p:
            obj = f"para un error máximo e = {fmt(p['e'])}"
        elif "reduccion" in p:
            obj = f"para reducir un {fmt(p['reduccion'] * 100)}% el error (o la relación entre límites)"
        elif "relacion" in p:
            obj = f"para que la relación entre límites sea R' = {fmt(p['relacion'])}"
        else:
            obj = "(completá el error e o la reducción pedida)"
        delta = " Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual." \
            if _hay(r"\bmas\b", normalizar(inc.texto)) or "n" in d else ""
        return f"Calcular el tamaño de muestra {obj}.{delta}"
    if inc.tipo == "ensayo":
        if tema.startswith("chi"):
            return ("Contrastar con χ² si las frecuencias observadas difieren significativamente de las esperadas "
                    "(H0: " + ("las variables son independientes / los grupos son homogéneos" if tema == "chi_contingencia"
                              else "los datos siguen el modelo propuesto") + ").")
        cola = {"derecha": ">", "izquierda": "<", "bilateral": "≠"}.get(p.get("tail"), "?")
        return (f"Decidir con un ensayo de hipótesis sobre {par}: H1 con signo '{cola}'. "
                f"Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.")
    if inc.tipo == "beta":
        qp = "β = P(no rechazar H0 | H0 falsa)" if p.get("prob") == "beta" else "la potencia 1-β = P(rechazar H0 | H0 falsa)"
        return f"Calcular {qp} para el valor alternativo del parámetro, con la región crítica del ensayo."
    if inc.tipo == "diseno":
        return ("Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las "
                "dos condiciones (α y β) y escribir la regla de decisión.")
    if inc.tipo == "curva":
        return "Tabular β y 1-β para varios valores del parámetro y graficar la curva OC (β) y la de potencia (1-β)."
    return "Esta parte no la calcula la app: revisá la teoría o los ejercicios parecidos de la guía."


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

IncisosIn = Union[Sequence[str], Sequence[Tuple[str, str]]]


def _expandir_idem(lista: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """'c) Ídem a) y b) considerando que σ no se conoce' -> se repiten a) y b) con la nueva condición."""
    salida = []
    textos = dict(lista)
    for letra, texto in lista:
        m = re.match(r"^\W*[ií]dem\s+((?:[a-h]\)\s*(?:,|y)?\s*)+)(.*)$", texto, flags=re.IGNORECASE)
        if m:
            refs = re.findall(r"([a-h])\)", m.group(1))
            extra = m.group(2).strip()
            for ref in refs:
                if ref in textos:
                    salida.append((f"{letra}.{ref}", f"{textos[ref]} ({extra})"))
            continue
        salida.append((letra, texto))
    return salida


def analizar(planteo: str, incisos: Optional[IncisosIn] = None) -> Analisis:
    planteo = (planteo or "").strip()
    lista: List[Tuple[str, str]] = []
    if incisos:
        for k, it in enumerate(incisos):
            if isinstance(it, (tuple, list)):
                lista.append((it[0], it[1]))
            elif str(it).strip():
                lista.append((chr(ord("a") + k), str(it).strip()))
    if not lista:
        planteo, lista = separar_incisos(planteo)
    if not lista:
        # sin incisos: la pregunta está en el mismo planteo
        lista = [("única", pregunta_de(planteo))]

    an = Analisis(planteo=planteo)
    total = planteo if lista[0][0] == "única" else planteo + " " + " ".join(tx for _, tx in lista)
    t_total = Texto(total)
    pregunta = " ".join(tx for _, tx in lista) if lista[0][0] != "única" else pregunta_de(planteo)
    an.tema, an.razones_tema = detectar_tema(t_total.norm, t_total.listas, normalizar(pregunta))
    an.criterio, an.criterio_razon = detectar_criterio(t_total.norm)

    t = Texto(planteo)
    diseno = False
    if an.tema in ("media", "varianza", "proporcion"):
        diseno = completar_diseno(an, t)
    if not diseno:
        r = extraer_alpha(t)
        if r:
            _set(an, "alpha", r[0], t, r[1], r[2])

    if an.tema in ("media", "varianza", "proporcion"):
        extraer_datos_lista(an, t)
        r = extraer_error(t)
        if r:
            an.datos[r[0]] = r[1]
            an.evidencias.append(Evidencia(r[0], r[1], t.fragmento(r[2]) if r[2] else "",
                                           "error admitido" if r[0] == "e" else "reducción pedida"))
        extraer_n(an, t)
        extraer_N(an, t)
        if an.tema == "proporcion":
            extraer_proporcion(an, t)
        else:
            extraer_desvio(an, t)
            if an.tema == "media":
                extraer_media(an, t, solo_mu0=diseno)
                extraer_totales(an, t)
        if "n" not in an.datos and "N" in an.datos and not diseno:
            an.datos["n"] = int(an.datos.pop("N"))
            for e in an.evidencias:
                if e.clave == "N":
                    e.clave, e.motivo = "n", "tamaño de la muestra (la 'partida' es la muestra observada)"
        if diseno and an.tema == "media" and "mu0" in an.datos:
            pct = any(e.clave == "mu0" and "%" in e.fragmento for e in an.evidencias)
            r = extraer_mu1(t, an.datos["mu0"], pct_valor=pct)
            if r:
                an.datos["mu1"] = r[0]
                an.evidencias.append(Evidencia("mu1", r[0], t.fragmento(r[1]), r[2]))
            an.datos.setdefault("sigma_conocido", True)
        if an.tema == "media" and diseno_control(an, planteo):
            diseno = True
            an.datos.setdefault("sigma_conocido", True)
        ajustar_escala(an)
        if an.tema == "varianza" and "desvio" in an.datos:
            an.datos.setdefault("sigma_conocido", False)
        doble_condicion(an, t)
    elif an.tema in ("dos_medias", "dos_varianzas"):
        extraer_dos_muestras(an, t)
    elif an.tema.startswith("chi"):
        extraer_chi(an, t)

    lista = _expandir_idem(lista)
    previo: Dict = {}
    for letra, texto_inc in lista:
        inc = Inciso(letra=letra, texto=texto_inc)
        norm = normalizar(texto_inc)
        inc.tipo, razon = clasificar_inciso(norm, an.tema, normalizar(planteo))
        if inc.tipo == "no_soportado" and len(norm) < 60 and lista[0][0] != "única":
            inc.tipo, razon = clasificar_inciso(normalizar(pregunta_de(planteo)), an.tema, "")
            razon = "El inciso solo agrega un dato; la pregunta está en el planteo. " + razon
        if an.tema == "media" and inc.tipo == "ensayo" and "beta" in an.datos and "xbar" not in an.datos:
            inc.tipo, razon = "diseno", "Hay dos condiciones (α y β): se diseña el ensayo."
        inc.razones.append(razon)
        extraer_params_inciso(inc, an, previo)
        # herencia: lo que no se dice en el inciso vale lo del inciso anterior (α, cola, μ₁...)
        for k in ("alpha", "tail", "mu1", "sigma1", "p1", "prob", "mu0", "sigma0", "p0"):
            if k not in inc.params and k in previo and not (k == "tail" and inc.tipo in ("ensayo", "diseno")):
                inc.params[k] = previo[k]
        if inc.tipo == "diseno" and "beta" not in inc.params and "beta" in an.datos:
            inc.params["beta"] = an.datos["beta"]
        inc.que_pide = explicar(inc, an)
        previo.update(inc.params)
        an.incisos.append(inc)

    if "alpha" not in an.datos and not any("alpha" in i.params for i in an.incisos) and an.tema not in ("regresion",):
        an.datos["alpha"] = 0.05
        an.avisos.append("No se encontró el riesgo α ni la confianza: se asume α = 0,05 (revisalo).")
    return an
