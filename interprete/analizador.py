"""Analizador por reglas: enunciado -> Analisis (tema, datos, incisos).

No "entiende" el texto: busca las frases típicas de la cátedra (las mismas de la
Guía de Problemas) y ubica cada número según las palabras que lo rodean. Por
eso cada dato guarda la evidencia (el fragmento del que salió) y todo es
editable en la pantalla antes de calcular.
"""

import re
from math import sqrt
from typing import Dict, List, Optional, Sequence, Tuple, Union

from .dos_tablas import grupos_de_tablas, tablas_de_texto
from .glosario import unificar_redaccion
from .modelo import EXTENSIONES, Analisis, Evidencia, Inciso, TEMAS
from .tablas import buscar_tablas
from .texto import ListaDatos, Numero, buscar_listas, buscar_numeros, fmt, normalizar, oraciones, parse_num

# ---------------------------------------------------------------------------
# Separación de incisos
# ---------------------------------------------------------------------------

RE_INCISO = re.compile(r"(?:(?<=[\s.?:;])|^)([a-h])\)\s")


RE_PARRAFO_PREGUNTA = re.compile(
    r"^\W*(cual|cuales|cuanto|cuantos|cuantas|que|como|donde|considera|suponga|supongamos|suponiendo|si se|"
    r"estimar|estime|indicar|indique|calcular|calcule|determinar|determine|establecer|establezca|hallar|halle|"
    r"verificar|verifique|ensayar|obtener|plantear|plantee|disenar|probar|analizar|decidir|puede|se puede|"
    r"es posible|existe|hay)\b")


def _separar_parrafos(texto: str) -> Tuple[str, List[Tuple[str, str]]]:
    """Sin letras a), b)...: cada párrafo que pregunta (después del planteo) es un inciso."""
    parrafos = [p.strip() for p in re.split(r"\s*\n\s*", texto) if p.strip()]
    if len(parrafos) < 2:
        return texto.strip(), []

    def pregunta(p):
        return "¿" in p or p.rstrip().endswith("?") or RE_PARRAFO_PREGUNTA.match(normalizar(p)) is not None

    k = next((i for i in range(1, len(parrafos)) if pregunta(parrafos[i])), None)
    if k is None:
        return texto.strip(), []
    planteo = "\n".join(parrafos[:k])
    incisos = []
    for p in parrafos[k:]:
        if pregunta(p) or not incisos:
            incisos.append((chr(ord("a") + len(incisos)), p))
        else:  # un párrafo que no pregunta completa el inciso anterior (p. ej. una tabla)
            letra, previo = incisos[-1]
            incisos[-1] = (letra, previo + " " + p)
    return planteo, incisos


def separar_incisos(texto: str, parrafos: bool = False) -> Tuple[str, List[Tuple[str, str]]]:
    """Parte un enunciado completo en planteo + [(letra, texto)] (a, b, c... consecutivas).

    Con `parrafos`, si no hay letras prueba con párrafos: cada párrafo que pregunta es un inciso."""
    esperado = "a"
    cortes = []
    for m in RE_INCISO.finditer(texto):
        if m.group(1) == esperado:
            cortes.append((m.start(1), m.end(), esperado))
            esperado = chr(ord(esperado) + 1)
    if not cortes:
        return _separar_parrafos(texto) if parrafos else (texto.strip(), [])
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

    def _inicio(self, k: int) -> int:
        """Una oración que sigue a ':' es la continuación de la anterior ('datos históricos ...: la media es 11,2')."""
        ini = self._oraciones[k][0]
        while k > 0 and self.texto[:ini].rstrip().endswith(":"):
            k -= 1
            ini = self._oraciones[k][0]
        return ini

    def oracion(self, pos: int) -> str:
        for k, (ini, fin) in enumerate(self._oraciones):
            if ini <= pos < fin:
                return self.norm[self._inicio(k):fin]
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
            if i not in self.usados and not self._en_lista(n) and not self._es_codigo(n):
                yield i, n

    def _es_codigo(self, n: Numero) -> bool:
        """Parte del nombre de un modelo ('contactor AX–2', 'modelo B-12'): no es un dato."""
        return re.search(r"\b[a-z]{1,4}[–-]$", self.norm[max(0, n.ini - 5):n.ini]) is not None and \
            re.search(r"[A-Z]", self.texto[max(0, n.ini - 5):n.ini]) is not None

    def _en_lista(self, n: Numero) -> bool:
        return any(l.ini <= n.ini < l.fin and len(l.valores) >= 3 for l in self.listas)

    def usar(self, i: int):
        self.usados.add(i)


def _hay(patron: str, texto: str) -> bool:
    return re.search(patron, texto) is not None


def _cuenta(patrones: Sequence[str], texto: str) -> int:
    return sum(len(re.findall(p, texto)) for p in patrones)


# números escritos con palabras ('se detiene si hay cinco o más defectuosas')
PALABRAS_NUM = {"cero": 0, "un": 1, "una": 1, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6,
                "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "once": 11, "doce": 12, "quince": 15, "veinte": 20}
RE_PALABRA_NUM = r"(cero|una?|uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|quince|veinte|\d+)"


# ---------------------------------------------------------------------------
# Palabras clave
# ---------------------------------------------------------------------------

P_PROPORCION = [r"porcentaje", r"proporci", r"fraccion", r"defectuos", r"\b(piezas|unidades) (falladas|con fallas|malas)",
                r"rating", r"puntos porcentuales",
                r"ausentismo", r"plan de muestreo", r"\baql\b", r"\bltpd\b", r"compradores", r"televidentes",
                r"inscript", r"penetracion", r"exitos?\b", r"se presento \d+ veces", r"frecuencia excesiva",
                r"probabilidad de(l)? cero", r"(salio|aparecio|se presento) [a-z ]{0,15}\d+ veces",
                r"\d\s*%\s*de (los|las) (?!veces)[a-z]+",
                r"\b\d+ (de ellos |de ellas )?(dijeron|manifestaron|respondieron|declararon|afirmaron|contestaron|opinaron|"
                r"eligieron|prefirieron|prefieren|votaron)\b"]
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
         r"variedad (actual|nueva)", r"metodo (propuesto|clasico)", r"\([a-z]{1,3}\)\s*:[^.]{0,80}\([a-z]{1,3}\)\s*:",
         r"σ\s*1\s*=[^.]{0,60}σ\s*2\s*=",
         r"\b(actual|viej[oa]|tradicional|habitual|nuev[oa]|propuest[oa]|[a-z]+)\s*\(([a-z]{1,2})\)[^?]{0,200}?\b(actual|viej[oa]|"
         r"tradicional|habitual|nuev[oa]|propuest[oa]|[a-z]+)\s*\((?!\2\))[a-z]{1,2}\)",
         r"\b(linea|grupo|planta|turno|lote|proveedor|equipo|horno|sucursal) (1|a|“a”)\b[^?]{0,250}"
         r"\b(linea|grupo|planta|turno|lote|proveedor|equipo|horno|sucursal) (2|b|“b”)\b"]
P_APAREADAS = [r"apareadas", r"\bpareadas", r"un par de", r"\bcada (finca|persona|trabajador|operario|paciente|individuo|"
               r"sujeto|alumno|empleado|conductor|vehiculo|auto)\b",
               r"\b(con|en|a) (ambos|ambas|los dos|las dos) (procesos|metodos|tratamientos|tecnicas|productos)\b",
               r"mism[oa]s? (\d+ )?(trabajadores|individuos|personas|pacientes|sujetos|operarios|alumnos|empleados|unidades|"
               r"fincas|parcelas|maquinas|autos|automoviles|vehiculos|lotes|establecimientos|conductores|clientes)",
               r"\b(finca|persona|maquina|auto|vehiculo|operario|paciente|alumno|individuo|sujeto|empleado) por \1\b",
               r"se les pidio", r"dividiendo (al|el) material", r"(el material|cada muestra|cada unidad) se dividio",
               r"antes y despues", r"\b(finca|persona|trabajador|operario|paciente|individuo|sujeto)\s*:\s*(1|i)\s+(2|ii)\b"]
P_CHI_AJUSTE = [r"se ajusta", r"bondad de ajuste", r"\bajuste (a|al|de)\b", r"modelo (normal|de poisson|log-?normal|"
                r"de weibull|weibull|de pareto|pareto|gumbel|uniforme)", r"\b(un|el) dado\b", r"dado (esta )?cargado",
                r"ruleta[^?]{0,400}(negro|colorado)", r"igualmente distribuid", r"patron historico", r"se comporta",
                r"(reparte|reparten|distribuy|divid)[a-z]* (por igual|en partes iguales|equitativamente|uniformemente)",
                r"(cambi|modific|alter)[a-z]* [a-z ]{0,20}\bpatron\b|\bpatron (de|del) [a-z]+ (cambi|se modific|se alter)",
                r"distribucion (poissoniana|de poisson)", r"cumple con la especificacion del fabricante"]
P_CHI_CONT = [r"(?<!muestras )(?<!controles )(?<!ensayos )(?<!pruebas )independ", r"estan asociad", r"\basociadas\b", r"asociacion entre", r"existe asociacion",
              r"\bdepende de la\b", r"tabla de contingencia", r"homogene", r"difieren entre",
              r"(proporciones|niveles|porcentajes?)[^.]{0,60}(difieren|diferentes|variado)",
              r"(variado|variacion|difieren|diferentes)[^.]{0,40}(porcentaje|proporci)",
              r"relacion entre el color", r"de una? (semana|mes|turno|dia|planta|zona|local|sucursal|lote) a otr[ao]",
              r"\b([3-9]|tres|cuatro|cinco) (plantas|turnos|locales|zonas|areas|grupos|semanas|localidades)\b"]
P_REGRESION = [r"regresion|modelo lineal general|doble logaritmic|modelo logaritmico|σ\s*(x\s*[·.*]?\s*y|y\s*[·.*]?\s*x)\s*=",
               r"correlacion",
               r"minimos cuadrados", r"\brecta\b", r"pronostic", r"relacion lineal",
               r"linealmente", r"asociacion lineal", r"en funcion de", r"variables? (independiente|dependiente|a explicar)",
               r"combinacion lineal", r"\bx\s*1\b.{0,200}\bx\s*2\b", r"relacionada con", r"predecir",
               r"relacion entre (el|la|los|las) [a-z ]{3,60} y (el|la|los|las|su)\b", r"ecuacion para",
               r"relacion existente entre", r"por cada [0-9.]+ [a-z]+ que se invier", r"\bx\s*\^",
               r"\by\s*=\s*\S{1,3}\s*[·.*]?\s*x\b",
               r"variables? explicativas?|modelo lineal\b|(ajustar|estimar) (un|el) modelo|"
               r"\bcada (\d[\d.,]*|mil|cien) [a-z]+ (adicionales |mas )?(que se invier|invertid|gastad|adicional)"]

# Dirección del ensayo
P_MAS = [r"\bmayor(es)?\b", r"superior", r"\bsupera", r"\bexced", r"aument", r"increment", r"\bmas del?\b", r"por encima", r"\bsub(e|en|io|ieron|a|an|ir|ira|iria|ido)\b",
         r"\bmejor", r"efectiv(?!amente)", r"excesiv"]
P_MENOS = [r"\bmenor(es)?\b", r"inferior", r"disminu", r"\breduc", r"\bmenos de\b", r"\bbaj[aoe]\b(?! (control|medida|criterio|el|la|los|las|un|una|condiciones|ningun|ese|esa|este|esta|dicho|dicha))"]
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
    # un porcentaje ('la media y el desvío con un 95% de confianza') no es un dato de una muestra
    medias = len(re.findall(r"(media|promedio|medio)[^0-9.;]{0,30}(?!\d+(?:,\d+)?\s*%)\d", norm))
    desvios = len(re.findall(r"(desvio|desviacion)[^0-9.;]{0,30}(?!\d+(?:,\d+)?\s*%)\d", norm))
    if medias >= 2 and desvios >= 2:
        return True
    # dos dispersiones (varianza y/o desvío) de dos muestras medidas por separado: 'se midieron 16 chapas y la varianza
    # resultó 0,0441 ... se midieron 13 chapas y el desvío fue de 0,15'
    dispersiones = len(re.findall(r"(desvio|desviacion|varianza)[^0-9.;]{0,30}(?!\d+(?:,\d+)?\s*%)\d", norm))
    tamanos = len(re.findall(r"(se (midieron|tomaron|pesaron|eligieron|seleccionaron|ensayaron|probaron|analizaron|"
                             r"controlaron|inspeccionaron|revisaron)|muestras? (aleatoria )?de) \d", norm))
    if dispersiones >= 2 and tamanos >= 2 and medias == 0:
        return True
    # dos conteos de casos sobre dos muestras: 'se revisaron 500 conos y 75 resultaron defectuosos; ... se revisaron 250'
    distintos = len(set(re.findall(r"(?:se (?:revisaron|inspeccionaron|controlaron|tomaron|eligieron|seleccionaron|"
                                   r"analizaron|probaron)|muestras? (?:aleatoria )?de) (\d[\d.]*)", norm)))
    if distintos >= 2 and medias == 0 and dispersiones == 0 and not _hay(r"sistema|plan de muestreo|periodic", norm) and \
            _hay(r"(defectuos|fallad|con fallas|rechazad|aprobad|favorables|resultaron|fueron)", norm):
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
    if s_ct >= 1 and (prop >= 1 or s_ct >= 2 or _hay(r"independ|asociad|asociacion|contingencia|depende|relacionad", norm)):
        razones.append("Pregunta si hay asociación / independencia o si las proporciones difieren entre "
                       "varios grupos: tabla de contingencia χ².")
        return "chi_contingencia", razones

    if dos:
        if prop >= 1 and (prop_q >= 1 or med == 0) and med_q == 0 and var == 0:
            razones.append("Compara porcentajes de 2 grupos: la guía lo resuelve como tabla de contingencia χ² "
                           "(comparación de procesos de Bernoulli).")
            return "chi_contingencia", razones
        foco_var = _hay(r"(desvios?|desviacion(es)?|varianzas?|variabilidad|regularidad|parejos)[^.?]{0,60}"
                        r"(difieren|diferentes|reduc|disminu|mayor|menor|relacion|igual)|"
                        r"(reduccion|disminuir|disminucion)[^.?]{0,40}(desvio|desviacion|varianza)|"
                        r"relacion entre (las varianzas|los desvios)", q) or \
            _hay(r"(reduc|disminu)[a-z]*[^.?]{0,40}(desvio|desviacion|varianza)", norm) or (var_q > med_q and var_q > 0)
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


RE_CONF = r"(confianza|seguridad|certeza)"
# 'error muestral / de muestreo / de estimación' es el e del IC, no el riesgo α
RE_ALPHA = (r"(riesgo|significacion|α\s*=|\balfa\s*=|\berror\b(?! (muestral|de muestreo|de (la )?estimacion|admitido|maximo|de ±|de \+-))|"
            r"equivocad|erronea|errone|indebidamente|incorrect|tipo i\b|sin (necesidad|motivo|razon|causa|justificacion)|"
            r"innecesariamente|falsa alarma|en vano)")

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
    if _hay(r"(reduc|disminu|baj|llev)[a-z]* (el |dicho |ese |este )?error (muestral )?(a|al|en|hasta)\s*$", a):
        return None   # 'reducir el error a 0,01 kg' es el error muestral e buscado
    # 'mayor de 0,09 mm², para un riesgo del 5%': el riesgo es el número que sigue a la palabra
    riesgo_ajeno = _hay(r"^" + _R + r"{0,45}" + RE_ALPHA + _R + r"{0,12}\d", d)
    if _hay(RE_ALPHA + _R + r"{0,35}$", a) or (_hay(r"^" + _R + r"{0,45}" + RE_ALPHA, d) and not riesgo_ajeno):
        return n.fraccion, "riesgo / nivel de significación α"
    # 'si el proceso anda bien, solo un 5% de las veces se lo detiene': frecuencia de falsas alarmas → α
    if _hay(r"^\s*de las veces\b[^.;?]{0,40}(deten|rechaz|revis|interv|ajust|equivoc)", d) and \
            _hay(r"\b(si|cuando)\b[^.;?]{0,60}(anda bien|funciona (bien|normalmente|correctamente)|bajo control|cumple|"
                 r"en condiciones normales)", t.oracion(n.ini)):
        return n.fraccion, "veces que se detiene / rechaza estando todo bien → α"
    # 'el riesgo de pautar sin que se cumpla la condición se fija en 0,10': la palabra del riesgo queda lejos del número
    if _hay(RE_ALPHA + r"[^0-9;?]{0,90}\b(se fija|se establece|se estipula|se adopta|se asume|se toma|se acepta|"
            r"se admite|es|sea|sera|vale|debe ser)( en| de| del| igual a)?( un| el| del)?\s*$", t.antes(n, 120)):
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


RE_COL_FREC = r"(cantidad|frecuencia|numero|n°|observaciones|casos|\bfi\b|veces)"
# 'valor | frecuencia; valor | frecuencia; ...' o 'a – b | frecuencia; ...' (tabla aplanada en una línea)
RE_PARES_FREC = re.compile(r"(?:(?:\d+(?:,\d+)?\s*[–-]\s*)?\d+(?:,\d+)?\s*\|\s*\d+\s*(?:[;.]\s*|$)){3,}")
RE_PAR_FREC = re.compile(r"(\d+(?:,\d+)?)(?:\s*[–-]\s*(\d+(?:,\d+)?))?\s*\|\s*(\d+)")


def _num_celda(c) -> Optional[float]:
    if isinstance(c, (int, float)):
        return float(c)
    m = re.fullmatch(r"\s*(-?\d+(?:[.,]\d+)?)\s*[–-]\s*(-?\d+(?:[.,]\d+)?)\s*", str(c or ""))
    if m:   # intervalo de clase 'a-b' → marca de clase
        return (float(m.group(1).replace(",", ".")) + float(m.group(2).replace(",", "."))) / 2
    return None


def _agrupados_tabla(tablas: List[dict]) -> Optional[Tuple[List[float], str]]:
    """Tabla de frecuencias ya estructurada: [valor | frecuencia] o [desde | hasta | frecuencia].

    La última columna tiene que ser una frecuencia (encabezado 'Cantidad', 'Número de...', 'Frecuencia') con
    enteros; así una tabla 'Semana | Media' no se toma como frecuencias."""
    for tb in tablas or []:
        cols = [normalizar(str(c)) for c in tb.get("columnas") or []]
        filas = tb.get("filas") or []
        if len(cols) not in (2, 3) or len(filas) < 3 or not re.search(RE_COL_FREC, cols[-1]):
            continue
        frec = [f[-1] for f in filas]
        if not all(isinstance(f, (int, float)) and float(f).is_integer() and f >= 0 for f in frec):
            continue
        if len(cols) == 3:
            marcas = [(_num_celda(f[0]) + _num_celda(f[1])) / 2 if None not in (_num_celda(f[0]), _num_celda(f[1]))
                      else None for f in filas]
        else:
            marcas = [_num_celda(f[0]) for f in filas]
        if None in marcas:
            continue
        datos = [x for x, f in zip(marcas, frec) for _ in range(int(f))]
        intervalos = len(cols) == 3 or any(isinstance(f[0], str) for f in filas)
        return datos, ("datos agrupados: marcas de clase (punto medio de cada intervalo) × frecuencias" if intervalos
                       else "tabla de frecuencias: cada valor repetido según su frecuencia")
    return None


def _pares_frecuencia(t: Texto) -> Optional[Tuple[List[float], str, Tuple[int, int]]]:
    """Tabla aplanada 'Cantidad de X | Número de Y: 0 | 2; 1 | 4; ...' (o 'a – b | f; ...')."""
    m = RE_PARES_FREC.search(t.norm)
    if not m or not _hay(r"\|", t.norm[max(0, m.start() - 90):m.start()]) or \
            not _hay(RE_COL_FREC, t.norm[max(0, m.start() - 90):m.start()]):
        return None
    datos, intervalos = [], False
    for a, b, f in RE_PAR_FREC.findall(m.group(0)):
        x = float(a.replace(",", "."))
        if b:
            x, intervalos = (x + float(b.replace(",", "."))) / 2, True
        datos += [x] * int(f)
    motivo = ("datos agrupados: marcas de clase (punto medio de cada intervalo) × frecuencias" if intervalos
              else "tabla de frecuencias: cada valor repetido según su frecuencia")
    return datos, motivo, (m.start(), m.end())


def extraer_datos_lista(an: Analisis, t: Texto):
    """Si el enunciado trae los datos crudos (o una tabla de frecuencias), calcula n, x̄ y S."""
    pares = _pares_frecuencia(t)
    if pares:   # los números de la tabla no son n, x̄ ni μ₀
        for i, n in enumerate(t.nums):
            if pares[2][0] <= n.ini < pares[2][1]:
                t.usar(i)
    ag = _agrupados_tabla(an.tablas) or (pares[:2] if pares else None) or _agrupados(t)
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
    if _hay(r"(medias?|promedios?)\s*:?\s*$", normalizar(lista.etiqueta or "")) and \
            _hay(r"(cada|por|durante \d+|de \d+) (semana|dia|mes|turno|lote|hora|jornada)s?", t.norm):
        # 'Semana: 1 - 2 - ...; Media: 5,2 - 4,9 - ...' → son medias de distintos períodos, no datos de una muestra
        an.datos["medias_periodo"] = True
        an.evidencias.append(Evidencia("datos", valores, t.texto[lista.ini:lista.fin],
                                       "medias de cada período (cada una se compara con los límites de control)"))
        return
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
    elif datos:
        # se calcula en miles (así el error pedido '± 1' sigue en la misma escala) y el IC se informa también en unidades
        an.datos["escala"] = 1000
        an.evidencias.append(Evidencia("escala", 1000, "en miles", "los datos están en miles: los límites se "
                                                                  "informan también en unidades (× 1.000)"))


UNIDADES_MUESTRA = (r"(envases|unidades|piezas|rollos|tarjetas|ovillos|tablas|medidores|corridas|dias|meses|"
                    r"semanas|horas|personas|familias|paquetes|cerdos|tubos|laminas|cojinetes|supermercados|clientes|"
                    r"observaciones|hogares|catalogos|arboles|televidentes|tornillos|llantas|bolas|conos|muestras|"
                    r"maquinas|parcelas|animales|potrillos|operarios|ensayos|datos|botellas|suelas|conjuntos|"
                    r"hombres|mujeres|usuarios|bielas|establecimientos|negocios|alambres|lamparas|baterias|"
                    r"recorridos|mediciones|pilas|bolsas|latas|cajas|articulos|vehiculos|autos|lotes|tomas|jornadas|"
                    r"tiradas|tiros|lanzamientos|jugadas|encuestados|cartas|entrevistas|encuestas)")
VERBOS_MUESTRA = (r"(muestra|se tomaron|se eligieron|se seleccionaron|se midieron|se pesaron|se registr|se analiz|"
                  r"se enviaron|se atendieron|sobre|durante|panel|se trabajo|arroj|obtuv|obteni|prueba|experiment|"
                  r"comprueba|se realizo|se examin|examinar|se inspeccion|se controla|obtiene|en los primeros|se envian|"
                  r"revisando|inspeccionando|controlando|midiendo|requiere|registr|encuesta|revisad|inspeccionad|"
                  r"controlad|encuestad|analizad|medid|encuest|al azar|aleatoriamente|tomad[oa]s|elegid[oa]s|"
                  r"seleccionad[oa]s|pesad[oa]s|pes[oa] (junt|en conjunto)|cronometr|consultad|se hicieron|se hizo|"
                  r"se probaron|se ensayaron|\b(revisa|revisan|inspecciona|inspeccionan|examina|examinan|controla|"
                  r"controlan|analiza|analizan|mide|miden|pesa|pesan|extrae|extraen|toma|toman|encuesta|encuestan)\b)")


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
        elif _hay(r"\bse (midieron|pesaron|tomaron|eligieron|seleccionaron|inspeccionaron|controlaron|revisaron|analizaron|"
                  r"ensayaron|probaron|examinaron|encuestaron|entrevistaron|encuesto a|entrevisto a|cronometraron)"
                  r"( al azar)?\s*$", a) and \
                _hay(r"^\s*[a-z]+", d):
            score = 3   # 'se midieron 25 ejes': el verbo de muestreo pegado al número, aunque la unidad no esté en la lista
        elif _hay(r"^\s*de (los |las )?$", a) and _hay(r"^\s*[a-z]{3,}[^.;\d]{0,60},\s*\d", t.norm[n.fin:n.fin + 80]):
            score = 3   # 'De 1.500 envíos con el nuevo embalaje, 9 tuvieron reclamos': el total del que se cuentan casos
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


RE_TOTAL_DESPUES = r"^\s*[a-z$³²]{0,12}\.?\s*(en total|en conjunto|entre (todas|todos|ambas|ambos)|sumad[oa]s|juntas?|juntos)\b"
RE_TOTAL_ANTES = (r"(un total de|en total|en conjunto|\btotal(es)?\b" + _R + r"{0,40}(fue|es|de|resulto|marco|dio|arrojo|=|sumo)|"
                  r"sumaron|suman|sumo|acumul[a-z]*( un total de| en total)?)\s*(de )?$")


def _es_total(t: Texto, n: Numero) -> bool:
    """'la balanza marcó 8.160 g en total', 'pesaron en conjunto 8.160 g', 'el peso total fue 8.160 g'."""
    return not n.pct and (_hay(RE_TOTAL_DESPUES, t.despues(n, 40)) or _hay(RE_TOTAL_ANTES, t.antes(n, 60)))


def extraer_totales(an: Analisis, t: Texto):
    """'40 personas en 68 minutos' / '25 horas ... un total de 4 horas y 30 minutos' / '16 bolsas ... 8.160 g en total'
    -> x̄ = total / n."""
    if "xbar" in an.datos or "n" not in an.datos:
        return
    n = an.datos["n"]
    for i, num in t.libres():
        if _es_total(t, num) and num.valor > n and not _hay(r"(poblacion|lote|partida|produccion)" + _R + r"{0,20}$",
                                                             t.antes(num, 40)):
            t.usar(i)
            an.datos["xbar"] = num.valor / n
            an.evidencias.append(Evidencia("xbar", num.valor / n, t.fragmento(num),
                                           f"es el TOTAL de la muestra: x̄ = {fmt(num.valor)} / n = {n} = {fmt(num.valor / n)}"))
            an.avisos.append(f"El enunciado da el total de la muestra ({fmt(num.valor)}), no la media: se usó "
                             f"x̄ = {fmt(num.valor)} / {n} = {fmt(num.valor / n)}.")
            return
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


RE_COSTO_FIJO = re.compile(r"(cobra|cobrara|cobraria|cuesta|honorarios de|costo fijo de)\s*(u\$s|\$|usd)?\s*(\d[\d.,]*)\s*(u\$s|\$|usd|pesos|dolares)?"
                           r"\s*(por (sus )?servicios|por mes|mensuales|fijos?)")
RE_COMISION = re.compile(r"comision (del|de un|de)\s*(\d+(?:,\d+)?)\s*%")


def extraer_costos(destino: Dict, an: Analisis, t: Texto):
    """Lo que se descuenta de la media para decidir: 'la compañía cobra 5.000 U$s por sus servicios' (costo fijo:
    neto = bruto - c) o 'una comisión del 2% sobre lo recaudado' (neto = bruto·(1 - k))."""
    m = RE_COMISION.search(t.norm)
    if m:
        destino["comision"] = parse_num(m.group(2)) / 100
        destino["costo_fijo"] = 0.0
        for i, n in enumerate(t.nums):
            if m.start(2) <= n.ini < m.end(2):
                t.usar(i)
        return
    m = RE_COSTO_FIJO.search(t.norm)
    if m:
        c = parse_num(m.group(3))
        if c:
            destino["costo_fijo"] = c
            for i, n in enumerate(t.nums):
                if m.start(3) <= n.ini < m.end(3):
                    t.usar(i)
            if destino is an.datos:
                an.evidencias.append(Evidencia("costo_fijo", c, t.texto[m.start():m.end()],
                                               "costo que se descuenta de la media: se decide con el valor NETO"))


RE_MEDIA_ANTES = r"(media|medio|promedio|valor estandar)" + _R + r"{0,50}?(\bde|\bdel|\bes|\bfue|=|\bdio|\bresulto|\ben|\bvale)\s*(los |las |el |la |un |una |aproximadamente )?$"
RE_UMBRAL_ANTES = (r"(mayor|menor|superior|inferior|supera|excede|\bmas|\bmenos|minima|maxima|minimo|maximo|"
                   r"igual|debe ser|deberia ser|no debe superar|no supera|no supere|no exceda|a lo sumo|por lo menos|al menos|"
                   r"admisible|especificacion|estandar|nominal|actualmente|actual|habitual|historic|diferente|distint|"
                   r"aproximadamente|(calibrad|regulad|ajustad|programad|seteada|graduad)[oa]s? (para|en|a)\b)"
                   + _R + r"{0,30}(que|a|de|del|es|las|los|el|la)?\s*$")
POBLACION_FUERTE = (r"(parametros poblacionales|pueden considerarse|pueden tomarse como|parametros de la poblacion|en condiciones normales|actualmente|son variables con|"
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
    if _hay(r"^\s*[a-z]{0,6}\s*,?\s*(lo que|que|lo cual) (es|resulta|seria) (lo )?(correcto|adecuado|normal)", d):
        return True   # 'bolsas de 1 kg, lo que es correcto cuando el proceso está bajo control': valor nominal
    if _hay(POBLACION_FUERTE, ora):
        return True
    if _hay(r"(se sabe que|debe ser|es una variable|variable aleatoria con|es variable con)", ora) \
            and not _hay(r"arroj|obtuv|obteni|registrandose|resulto|se registra\b", ora):
        return True
    return False


# Frases que presentan el valor que se lograría con el cambio (μ₁ de un diseño), no un dato ni μ₀.
RE_ALTERNATIVO = (r"(se piensa|se cree|se supone que (el|la) nuev|aumentaria|disminuiria|mejoraria|reduciria|lograria|"
                  r"con la modificacion|con el nuevo|con la nueva)")


def extraer_media(an: Analisis, t: Texto, solo_mu0: bool = False):
    """x̄ (dato muestral) y μ₀ (valor de referencia / umbral). En un diseño solo hay μ₀ (y μ₁)."""
    for i, n in t.libres():
        if solo_mu0 and "mu0" in an.datos:
            return
        ora = t.oracion(n.ini)
        if solo_mu0 and _hay(RE_ALTERNATIVO, ora):
            continue   # 'el nuevo sistema aumentaría la productividad a 5,8' es μ₁, no μ₀
        if n.pct and not _hay(r"rendimiento", ora):
            continue
        if _es_total(t, n) and "n" in an.datos and n.valor > an.datos["n"]:
            continue   # el total de la muestra: x̄ = total / n (extraer_totales)
        a = t.antes(n, 70)
        if _hay(r"(desvio|desviacion|varianza)" + _R + r"{0,30}$", a) or _hay(RE_CONF + r"|riesgo|probabilidad", a[-25:]):
            continue
        if _hay(r"\berror\b" + _R + r"{0,40}$", a):
            continue   # 'que el error de la estimación no supere los 5 g' es el error admitido e, no μ₀
        if _hay(r"(jornada|turno|periodo|lapso|durante)[a-z ]{0,10}\bde\s*$", a) and \
                _hay(r"^\s*(horas|hs|minutos|min|dias|semanas)\b", t.despues(n, 15)):
            continue   # 'durante una jornada de 8 horas' es el período de control, no una media
        if _hay(r"^\s*(semanas|anos|meses|dias|horas)\b" + _R + r"{0,12}(de edad )?(es|fue|era)\b", t.despues(n, 30)):
            continue
        es_media = _hay(RE_MEDIA_ANTES, a) or _hay(r"(promedio|media)[^.;?]{0,90}(fue de|resulto de|resulto|dio)\s*$", t.antes(n, 110))
        umbral = _es_umbral(t, n)
        if not es_media and not umbral:
            continue
        if not es_media and (_es_prob(n) and not n.pct):
            continue
        muestral = _hay(r"(muestra|arroj|obtuv|obteni|registrandose|resulto|se registra|se obtuvo|\bdio\b|\bdieron\b|"
                        r"en los primeros|prueba|se trabajo|se realizo|se (pesaron|midieron|ensayaron|controlaron)|"
                        r"se (seleccionaron|eligieron|tomaron) \d)", ora) and not _hay(POBLACION_FUERTE, ora)
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
                   r"(no )?(debe |puede |deberia )?(supere|exceda|sobrepase|exceder|sobrepasar)( los| las)?|"
                   r"\bdel)\s*(los |las |un |una )?$|σ\s*=?\s*$|\bun\s*=\s*$|\bs\s*=\s*$|(desvio|desviacion) (estandar )?$)")
CONOCIDO = (r"(poblacional|historic|se sabe|se conoce|conocid|registros|experiencia|parametros poblacionales|"
            r"distribucion normal (con un |de )?(desvio|desviacion)|se distribuye|se mantiene|no se modifica|no ha de modificarse|"
            r"estable|variables? (aleatorias? )?(con|cuya|cuyo)|es una variable|tiene un desvio|variabilidad del proceso|"
            r"sin modificar el desvio|no se modificara|pueden considerarse|pueden tomarse como|parametros de la poblacion|"
            r"no altera|no cambia|no afecta|valor este que|es variable con|"
            r"con las maquinas actuales)")


def extraer_desvio(an: Analisis, t: Texto, clave="desvio"):
    for i, n in t.libres():
        a = t.antes(n, 95)
        if n.pct and not _hay(r"(desvio|desviacion)", a[-30:]):
            continue
        es_var = _hay(r"varianza( muestral| poblacional)?" + _R + r"{0,20}(dio|de|es|fue|=)\s*$", a) or \
            _hay(r"varianza" + _R + r"{0,60}?(\bdio|\bfue|\bresulto|\barrojo|\bvale|\bes)( de| igual a)?\s*(un valor de )?$", a) or \
            (_hay(r"^\s*[a-z]{1,3}\s*(²|2\b|\^\s*2|cuadrad)", t.despues(n, 12)) and _hay(r"varianza", a))
        largo = _hay(r"(desvio|desviacion)[^.;?]{0,100}(fue de|resulto de|resulto|dio|ha sido de)\s*$", t.antes(n, 130))
        umbral_sig = _hay(r"(desvio|desviacion)" + _R + r"{0,70}(menor|mayor|superior|inferior)( que| a)( los| las)?\s*$", a)
        if not (_hay(RE_DESVIO_ANTES, a) or es_var or largo or umbral_sig):
            continue
        ora = t.oracion(n.ini)
        valor = sqrt(n.valor) if es_var else n.valor
        umbral = umbral_sig or _hay(r"(no debe superar|maxim[oa]|minim[oa]|mayor|menor|superior|inferior|como maximo|"
                      r"a lo sumo|como mucho|por lo menos|como minimo|especificacion|"
                      r"estipulado|nominal|no supere|no exceda|no sobrepase|supere|exceda|sobrepase|exceder|sobrepasar)"
                      + _R + r"{0,25}$", a) or \
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
        if _hay(r"error" + _R + r"{0,40}(de|sea|a|=|no supere|no exceda|no sobrepase|no sea mayor que|no mayor a|"
                r"como maximo|a lo sumo|menor que|menor a|inferior a|hasta)( los| las| el| la| de)?\s*(±\s*)?$|±\s*$|"
                r"reducir el error a\s*$", a) and not _hay(r"tipo", a[-20:]):
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
        if base is not None and n.pct and not pct_valor and _hay(r"^\s*(superior|mayor|mas|inferior|menor|menos)\b", d):
            # 'una vida media un 10% superior a la actual'
            signo = -1 if _hay(r"^\s*(inferior|menor|menos)", d) else 1
            t.usar(i)
            return base * (1 + signo * n.fraccion), n, f"{'+' if signo > 0 else '−'}{fmt(n.valor)}% sobre μ₀"
        if base is not None and not n.pct and _hay(r"(incrementa|aumenta|disminuye|reduce|baja|sube)[a-z]* en\s*$", a):
            signo = -1 if _hay(r"(disminu|reduc|baj)", a[-25:]) else 1
            t.usar(i)
            return base + signo * n.valor, n, f"{'+' if signo > 0 else '−'}{fmt(n.valor)} respecto de μ₀"
        if _hay(r"(vale|es de|es del|baja al|baja a|sube al|sube a|sea de|inferior a|superior a|es inferior a|"
                r"es superior a|de)\s*$", a) and _hay(r"(\bsi\b|cuando|malas|aquellas|dicho parametro)|" + RE_ALTERNATIVO, ora):
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
            if _hay(r"(reduc|disminu|aument|increment)[a-z]*( en)?( un| el)?\s*$|±\s*$|error" + _R + r"{0,15}$", a):
                continue   # 'reducir en un 40% el error', 'error de ± 2%': no es un dato de la muestra
            ref = _hay(r"(actualmente|en la actualidad|se sabe|era del|es del|trabaja|establecido|supera|superior|admite|contrato|"
                       r"inferior|mayor|menor|maximo|minimo|historic|normales|admitid|debe|se supone|con un|con el catalogo)",
                       ora) and not _hay(r"(muestra|se obtuvo|se ha registrado|se registro|encontr|se detecta|arroj|"
                                         r"registrado)", ora)
            if _hay(r"(supera|superior a|mayor que|menor que|inferior a|no supera|\bmas (de|del)|\bmenos (de|del)|"
                    r"por (encima|debajo) (de|del))( el| al| los)?\s*$", a):
                ref = True
            clave = "p0" if ref else "p_hat"
            if clave not in an.datos:
                t.usar(i)
                _set(an, clave, valor, t, n, "proporción de referencia (p₀)" if ref else "proporción observada en la muestra (p̂)")
            continue
        if n.es_entero and not _es_prob(n) and "r" not in an.datos:
            if _hay(r"(encontr[a-z]*|hallaron|registr[a-z]*|reciben|comprobando que|detectaron|obtuvieron|se obtuvo)\s*$", a) or \
                    (an.datos.get("n") and n.valor < an.datos["n"] and _hay(
                        r"^\s*(de (ellos|ellas|los|las) [a-z ]{0,20}?)?(dijeron|manifestaron|respondieron|declararon|afirmaron|"
                        r"contestaron|indicaron|opinaron|eligieron|prefirieron|prefieren|votaron|compraron|aprobaron|"
                        r"reprobaron|admitieron|reconocieron|aseguraron|expresaron|tuvieron|presentaron|resultaron|"
                        r"salieron|fallaron|tienen|tenian|cumplen|cumplian|presentan|superan|superaban|miden|median|"
                        r"resultan|fueron|eran|estan|estaban|no\b)", d)) or \
                    _hay(r"^\s*(unidad(es)? |piezas )?(defectuos|de ellos|mayores|pedidos|veces|inscript|exitos)", d) or \
                    _hay(r"se presento $", a):
                t.usar(i)
                _set(an, "r", int(n.valor), t, n, "cantidad de casos favorables / defectuosos en la muestra (r)")


# Plan de muestreo ya fijado: 'rechazar si se encuentran 9 o más', 'número de aceptación ≤ 2', 'rc = 1'
RE_RC_DADO = [
    (r"\br\s*c\s*=\s*" + RE_PALABRA_NUM + r"\b", 0),
    (r"(rechaz|deten|detien|revis)[^.;]{0,90}?\b" + RE_PALABRA_NUM + r"(?: [a-z]+){0,2} o mas\b", 0),
    (r"(rechaz|deten|detien|revis)[^.;]{0,90}?\b(como minimo|por lo menos|al menos) " + RE_PALABRA_NUM + r"\b", 0),
    (r"numero de aceptacion (de |igual a |de menor o igual a |menor o igual a |c\s*=\s*)*" + RE_PALABRA_NUM + r"\b", 1),
    (r"acepta[a-z]*[^.;]{0,60}?\b(si|cuando)\b[^.;]{0,50}?\b(hay|se encuentran?|aparecen|encuentra|resultan) "
     + RE_PALABRA_NUM + r"(?: [a-z]+){0,2} o menos\b", 1),
]


def extraer_plan_dado(an: Analisis, t: Texto) -> bool:
    """Plan de muestreo dado en el enunciado: r_c (se rechaza H0 si r ≥ r_c). Con el número de aceptación c
    ('se acepta si hay c o menos') el plan rechaza desde r_c = c + 1."""
    for patron, suma in RE_RC_DADO:
        m = re.search(patron, t.norm)
        if not m:
            continue
        crudo = m.group(m.lastindex)
        valor = PALABRAS_NUM.get(crudo)
        if valor is None:
            valor = int(crudo)
        for i, n in enumerate(t.nums):   # el número del plan no es un r observado
            if m.start(m.lastindex) <= n.ini < m.end(m.lastindex):
                t.usar(i)
        an.datos["rc"] = valor + suma
        an.datos["rc_cola"] = "derecha"
        an.evidencias.append(Evidencia("rc", valor + suma, t.texto[m.start():m.end()],
                                       "plan de muestreo dado: se rechaza si r ≥ r_c" +
                                       (f" (número de aceptación c = {valor} → r_c = c + 1)" if suma else "")))
        return True
    return False


def riesgos_plan_dado(an: Analisis, t: Texto):
    """Con el plan ya fijado, el 'riesgo de aceptar un lote malo' (del comprador / consumidor) es β, no α."""
    for n in t.nums:
        if not _es_prob(n) or not n.pct and n.valor >= 1:
            continue
        if not _hay(r"(riesgo|probabilidad)[^0-9]{0,15}$", t.antes(n, 30)):
            continue   # 'un lote que contiene el 5% defectuoso' es p₀, no un riesgo
        ini, fin = _clausula(t, n.ini)
        txt = t.norm[max(ini, n.ini - 60):min(fin, n.fin + 60)]
        if _hay(r"(riesgo|probabilidad)", txt) and _hay(r"(acept[a-z]* (un|el|los|las|una) (lote|partida)s? \W?mal|"
                                                          r"comprador|consumidor|\(β\))", txt) \
                and not _hay(r"(proveedor|productor|\(α\))", t.norm[max(ini, n.ini - 25):n.ini]):
            an.datos["beta"] = n.fraccion
            if an.datos.get("alpha") is not None and abs(an.datos["alpha"] - n.fraccion) < 1e-12:
                an.datos.pop("alpha")
                an.evidencias = [e for e in an.evidencias if e.clave != "alpha"]
            an.evidencias.append(Evidencia("beta", n.fraccion, t.fragmento(n),
                                           "riesgo del comprador (aceptar un lote malo) → β"))
            return


def p0_de_referencia(an: Analisis, t_total: Texto):
    """p₀ que aparece recién en una nota de un inciso: '(en una ruleta equilibrada la probabilidad de cero es 1/37)'."""
    for n in t_total.nums:
        if not (0 < n.fraccion < 1):
            continue
        ora = t_total.oracion(n.ini)
        if _hay(r"probabilidad[^0-9;]{0,40}\b(es|vale|era)( de)?\s*$", t_total.antes(n, 60)) and \
                _hay(r"(equilibrad|convencional|normal|correct|teoric|legal|honest|no adulterad|habitual)", ora) and \
                not _hay(r"\bsi\b[^0-9]{0,40}$", t_total.antes(n, 60)):
            an.datos["p0"] = n.fraccion
            an.evidencias.append(Evidencia("p0", n.fraccion, t_total.fragmento(n),
                                           "valor de referencia (lo que pasaría si todo es normal) → p₀"))
            return


# ---------------------------------------------------------------------------
# Extracción (2 poblaciones)
# ---------------------------------------------------------------------------

def _etiqueta_limpia(etq: str) -> str:
    """'…partes por billón de NDMA: Proceso Viejo' → 'Proceso Viejo' (lo que sigue al último ':')."""
    etq = re.sub(r"[\s:]+$", "", etq)
    etq = re.split(r"[:;]", etq)[-1]
    return etq[-40:].strip(" ,.()")


def _apareadas(an: Analisis, t: Texto, l1: List[float], l2: List[float], pista: Optional[bool], origen: str):
    """Apareadas si las dos listas tienen el mismo largo y el texto (o la forma de la tabla) indica que cada
    unidad se midió con ambos tratamientos (cada finca / persona / trabajador, 'Muestra Nº' por fila...)."""
    if len(l1) != len(l2) or _hay(r"independientes", t.norm):
        apareadas, motivo = False, "listas de distinto largo o grupos distintos → muestras independientes"
    elif _cuenta(P_APAREADAS, t.norm) > 0:
        apareadas, motivo = True, "mismas unidades medidas con ambos tratamientos → muestras apareadas"
    elif pista is not None:
        apareadas = pista
        motivo = (f"la tabla tiene una fila / columna por unidad ({origen}) → muestras apareadas" if pista else
                  "la tabla nombra grupos distintos → muestras independientes")
    else:
        apareadas, motivo = False, "grupos distintos (no se indica que sean las mismas unidades) → muestras independientes"
    _set(an, "apareadas", apareadas, t, None, motivo, pisar=True)


def _grupos_de_tablas(an: Analisis, t: Texto):
    """Tablas del enunciado (estructuradas o escritas en una línea) con los datos de los dos grupos."""
    g = grupos_de_tablas(an.tablas)
    if g is None:
        g = grupos_de_tablas(tablas_de_texto(t.texto))
    if g and len(g.nombres) > 2:
        pares = _pares_de_grupos(g)
        if pares:   # '4 ºC Sin albúmina | 4 ºC Con albúmina | −20 ºC Sin ...': una comparación por par
            an.datos["comparaciones"] = pares
            an.avisos.append(f"La tabla tiene {len(g.nombres)} grupos que forman {len(pares)} pares (con / sin): "
                             "cada ensayo se hace para cada par.")
        else:
            an.avisos.append(f"La tabla tiene {len(g.nombres)} grupos ({', '.join(g.nombres)}): se comparan los dos "
                             "primeros. Para otras comparaciones cambiá los datos de las muestras.")
    return g


def _pares_de_grupos(g) -> Optional[List[list]]:
    """Grupos consecutivos que solo difieren en 'con' / 'sin' (u otra palabra) → [[nombre, datos, nombre, datos], ...]."""
    if not g.listas or len(g.listas) % 2:
        return None
    pares = []
    for k in range(0, len(g.listas), 2):
        b1 = re.sub(r"\b(con|sin)\b", "", normalizar(g.nombres[k])).split()
        b2 = re.sub(r"\b(con|sin)\b", "", normalizar(g.nombres[k + 1])).split()
        if b1 != b2:
            return None
        pares.append([g.nombres[k], g.listas[k], g.nombres[k + 1], g.listas[k + 1]])
    return pares


NUMEROS_PALABRA = {"tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
                   "once": 11, "doce": 12, "quince": 15, "veinte": 20, "treinta": 30}
UNIDADES_N = (r"(corridas|parcelas|piezas|ensayos|maquinas|animales|operarios|observaciones|automoviles|potrillos|"
              r"botellas|muestras|conos|unidades|personas|pacientes|alumnos|empleados|lotes|plantas|novillos|"
              r"mediciones|pruebas|vehiculos|autos|tubos|lamparas|envases|bolsas|cajas|fincas|trabajadores|"
              r"probetas|especimenes|ejemplares|familias|hogares|clientes|cerdos|pollos|vacas|arboles|de ell[oa]s)")
TIEMPOS_N = r"(dias|meses|semanas|anos|jornadas|turnos)"
VERBOS_N = (r"(eligieron|eligio|seleccionaron|selecciono|tomaron|tomo|realizaron|realizo|midieron|registraron|"
            r"sembraron|fumigaron|probaron|ensayaron|observaron|analizaron|inspeccionaron|controlaron|"
            r"trataron|usaron|utilizaron)( entonces| al azar)?")


def _es_n_de_muestra(t: Texto, n: Numero, a: str) -> bool:
    """Tamaño de una de las muestras: 'n1 = 13', 'muestra de 25', 'se realizaron 21 ensayos', '16 de ellas',
    'los últimos 12 meses', 'De 655 observaciones'."""
    if not n.es_entero or n.valor < 2:
        return False
    d = t.despues(n)
    if _hay(r"\bn\s*[12]?\s*=\s*$|\bn\s*=\s*\d+\s*$|muestras? (aleatoria )?(de|con) $", a):
        return True
    if _hay(r"(media|promedio|medio|desvio|desviacion|riesgo|confianza|probabilidad)[^0-9]{0,25}$", a):
        return False
    if _hay(r"^\s*" + UNIDADES_N + r"\b", d):
        return True
    # '40 hornadas, media 1,50' / '25 frascos de la línea 1 con una media de 101': la muestra que se describe
    if _hay(r"^\s*[a-z]{3,}s\b[^.;?]{0,35}\b(media|promedio|medio)\b", t.norm[n.fin:n.fin + 60]):
        return True
    if _hay(r"^\s*" + TIEMPOS_N + r"\b", d):
        return _hay(r"(ultim[oa]s|durante( el| la| los| las)?|" + VERBOS_N + r")\s*$", a)
    return _hay(VERBOS_N + r"\s*$", a) and _hay(r"^\s*[a-z]+s\b", d)


RE_RAZON_GRUPO = (r"(marca|maquina|variedad|metodo|proceso|tipo|grupo|linea|proveedor|turno|planta|sucursal|"
                  r"aleacion|formula|racion|torno|horno|modelo|operario|equipo|laboratorio|zona|region)")


def _paralelo_dos_muestras(an: Analisis, t: Texto, posiciones: Dict[str, Numero], vistos: set):
    """Redacción paralela con elipsis: 'con 50 latas de la marca B se cubrió en promedio 56 m² por lata con un desvío
    de 6 m²; con 50 latas de la marca A, 49 m² por lata con un desvío de 5 m²'. El segundo grupo no repite 'promedio':
    su n y su x̄ son los números con la MISMA unidad que los del primero."""
    def unidad(n: Numero) -> str:
        m = re.match(r"\s*([a-z²³]+\d?(?:\s+por\s+[a-z]+)?)", t.norm[n.fin:n.fin + 30])
        return m.group(1) if m else ""
    for clave in ("n", "xbar"):
        uno = posiciones.get(f"{clave}1")
        if uno is None or f"{clave}2" in an.datos or not unidad(uno):
            continue
        for i, n in t.libres():
            # misma unidad (alcanza la primera palabra: 'quintales por parcela' ... '17,1 quintales y S = 1,43')
            if i in vistos or n.pct or n.ini <= uno.ini or unidad(n).split()[:1] != unidad(uno).split()[:1] or \
                    _alpha_de(t, i, n):
                continue
            if clave == "n" and not (n.es_entero and n.valor >= 2):
                continue
            if clave == "xbar" and _hay(r"(desvio|desviacion|varianza)[^0-9]{0,40}$", t.antes(n, 45)):
                continue
            t.usar(i)
            vistos.add(i)
            _set(an, f"{clave}2", int(n.valor) if clave == "n" else n.valor, t, n,
                 f"{clave} de la muestra 2 (misma unidad que el de la muestra 1: redacción paralela)")
            posiciones[f"{clave}2"] = n
            break
    if all(re.fullmatch(r"Muestra \d", an.datos.get(f"nombre{j}") or "Muestra 1") for j in (1, 2)):
        # 'de la marca B' ... 'de la marca A': los nombres de los grupos
        noms = []
        for j in (1, 2):
            n = posiciones.get(f"n{j}") or posiciones.get(f"xbar{j}")
            if n is None:
                return
            base = n.ini
            ventana = re.split(r"[.;]\s|,\s*\d", t.norm[base:n.fin + 45])[0]
            m = re.search(r"\b" + RE_RAZON_GRUPO + r"\s+[“\"]?([a-z0-9]{1,3})\b", ventana)
            if not m:
                return
            noms.append(t.texto[base + m.start():base + m.end()].replace("“", "").replace('"', ""))
        if normalizar(noms[0]) != normalizar(noms[1]):
            an.datos["nombre1"], an.datos["nombre2"] = noms
            an.evidencias.append(Evidencia("nombre1", noms[0], "", "grupo de la muestra 1 nombrado en el texto"))


def extraer_dos_muestras(an: Analisis, t: Texto):
    g = _grupos_de_tablas(an, t)
    if g and g.listas:
        an.datos["datos1"], an.datos["datos2"] = g.listas[0], g.listas[1]
        an.datos["nombre1"], an.datos["nombre2"] = g.nombres[0], g.nombres[1]
        for j in (0, 1):
            an.evidencias.append(Evidencia(f"datos{j + 1}", g.listas[j], g.nombres[j], f"datos de la muestra {j + 1} "
                                                                                      f"({g.origen})"))
        _apareadas(an, t, g.listas[0], g.listas[1], g.apareadas, g.origen)
        return {}
    listas = [l for l in t.listas if len(l.valores) >= 3]
    if len(listas) >= 2 and not (g and g.resumen):
        l1, l2 = listas[0], listas[1]
        an.datos["datos1"], an.datos["datos2"] = l1.valores, l2.valores
        an.datos["nombre1"] = _etiqueta_limpia(l1.etiqueta) or "Muestra 1"
        an.datos["nombre2"] = _etiqueta_limpia(l2.etiqueta) or "Muestra 2"
        an.evidencias.append(Evidencia("datos1", l1.valores, t.texto[max(0, l1.ini - 30):l1.fin], "datos de la muestra 1"))
        an.evidencias.append(Evidencia("datos2", l2.valores, t.texto[max(0, l2.ini - 30):l2.fin], "datos de la muestra 2"))
        _apareadas(an, t, l1.valores, l2.valores, None, "")
        return {}

    # Resumenes: n, x̄, S de cada muestra en orden de aparición (o con subíndice 1 / 2)
    ns, medias, desvios = [], [], []
    for i, n in enumerate(t.nums):
        a = t.antes(n, 45)
        if n.pct:
            continue
        if _es_n_de_muestra(t, n, a):
            ns.append((i, n))
        elif _hay(r"(media|promedio|medio)[^0-9]{0,40}$|\bx\s*[12]?\s*=\s*$|x\s*=\s*\d+(,\d+)?( [a-z]+)?\s*$|"
                  r"\)\s*:\s*$|\bx\s*\)?\s*:?\s*$", a) and not _hay(r"(desvio|desviacion)[^0-9]{0,15}$", a):
            medias.append((i, n))
        elif _hay(r"(desvio|desviacion)[^0-9]{0,40}$|\bs\s*[12]?\s*=\s*$|s\s*=\s*\d+(,\d+)?( [a-z]+)?\s*$|"
                  r"\(s\)\s*=\s*$", a) and not _hay(r"(probabilidad|riesgo|confianza)[^0-9]{0,15}$", a):
            desvios.append((i, n))
        elif _hay(r"varianza[^0-9]{0,40}$", a) and not _hay(r"(probabilidad|riesgo|confianza)[^0-9]{0,15}$", a):
            # 'la varianza resultó 0,0441 mm²': S = √S² (se informa en la evidencia)
            desvios.append((i, Numero(sqrt(n.valor), n.ini, n.fin, False, n.crudo)))
            an.avisos.append(f"Una muestra da la VARIANZA ({n.crudo.strip()}): se usó el desvío S = √{n.crudo.strip()} = "
                             f"{fmt(sqrt(n.valor))}.")
    # tamaños en palabras: 'durante los cuatro meses que duró la campaña'
    for m in re.finditer(r"\b(" + "|".join(NUMEROS_PALABRA) + r")\s+(" + UNIDADES_N + "|" + TIEMPOS_N + r")\b", t.norm):
        a = t.norm[max(0, m.start() - 45):m.start()]
        if _hay(r"(durante( el| la| los| las)?|ultim[oa]s|" + VERBOS_N + r")\s*$", a):
            v = NUMEROS_PALABRA[m.group(1)]
            ns.append((None, Numero(float(v), m.start(1), m.end(1), False, m.group(1))))
    ns.sort(key=lambda x: x[1].ini)
    # el mismo tamaño para los dos grupos: '15 animales cada uno', '10 parcelas al azar con cada variedad'
    if len(ns) == 1 and _hay(r"(\bcada un[oa]\b(?! (de|para)\b)|\b(con|de|en|para|por|a) cada (?!un[oa]\b)[a-z]{4,})",
                             t.norm):
        ns = [ns[0], ns[0]]
    if "cada uno" in t.norm or "cada una" in t.norm:
        m = re.search(r"(\d+) [a-z]+ cada un[oa]", t.norm)
        if m and len(ns) < 2:
            v = int(m.group(1))
            ns = [(None, Numero(v, m.start(1), m.end(1), False, m.group(1)))] * 2
    posiciones: Dict[str, Numero] = {}
    for k, (lista, clave) in enumerate(((ns, "n"), (medias, "xbar"), (desvios, "s"))):
        for j, (i, n) in enumerate(lista[:2]):
            if i is not None:
                t.usar(i)
            valor = int(n.valor) if clave == "n" else n.valor
            _set(an, f"{clave}{j + 1}", valor, t, n, f"{clave} de la muestra {j + 1}")
            posiciones[f"{clave}{j + 1}"] = n
    _paralelo_dos_muestras(an, t, posiciones, {i for lst in (ns, medias, desvios) for i, _ in lst if i is not None})
    if "n1" in an.datos and "n2" not in an.datos and _hay(r"\bn\s*=\s*\d+\s+\d+", t.norm):
        m = re.search(r"\bn\s*=\s*(\d+)\s+(\d+)", t.norm)
        an.datos["n1"], an.datos["n2"] = int(m.group(1)), int(m.group(2))
    if g and g.resumen:   # tabla resumen (n, x̄, S por grupo): manda sobre lo leído en el texto
        for clave, vals in g.resumen.items():
            for j in (0, 1):
                if j < len(vals) and vals[j] is not None:
                    _set(an, f"{clave}{j + 1}", int(vals[j]) if clave == "n" else vals[j], t, None,
                         f"{clave} de la muestra {j + 1} ({g.origen})", pisar=True)
                    posiciones.pop(f"{clave}{j + 1}", None)
        if not any(re.fullmatch(r"Grupo \d", x) for x in g.nombres[:2]):
            an.datos["nombre1"], an.datos["nombre2"] = g.nombres[0], g.nombres[1]
    an.datos.setdefault("nombre1", "Muestra 1")
    an.datos.setdefault("nombre2", "Muestra 2")
    an.datos.setdefault("apareadas", False)
    return posiciones


# ---------------------------------------------------------------------------
# TEMA IV: relación de desvíos φ = σ₁/σ₂ (quién va arriba, φ₀, α y β del diseño)
# ---------------------------------------------------------------------------

# raíz de la palabra que marca el grupo con el cambio -> (nombre del grupo nuevo, nombre del de referencia)
GRUPOS_CAMBIO = [
    (r"reacondicion", "reacondicionadas", "sin reacondicionar"),
    (r"aditivo", "con aditivo", "sin aditivo"),
    (r"acelerante", "con acelerante", "sin acelerante"),
    (r"albumina", "con albúmina", "sin albúmina"),
    (r"tratad|tratamiento", "tratadas", "sin tratar"),
    (r"propuest", "propuesta", "actual"),
    (r"\bnuev[oa]", "nueva", "actual"),
    (r"modificad|modificacion", "modificada", "actual"),
]
RE_REFERENCIA = r"(\bsin [a-z]+|\bactual|tradicional|\bviej[oa]|clasic|anterior|original)"
RE_NUEVO = "(" + "|".join(p for p, _, _ in GRUPOS_CAMBIO) + ")"


def _rol_muestra(t: Texto, n: Numero) -> Tuple[Optional[str], str]:
    """¿La muestra que empieza en n es la del cambio ('nuevo') o la de referencia ('ref')?

    Mira primero lo que sigue al tamaño ('21 piezas del material actual (A)') y si no alcanza lo anterior
    ('las máquinas sin reacondicionar, se registró ... 16 de ellas')."""
    for ventana in (t.despues(n, 45), t.antes(n, 70)):
        if _hay(RE_REFERENCIA, ventana):
            return "ref", ventana
        if _hay(RE_NUEVO, ventana):
            return "nuevo", ventana
    return None, ""


def _nombres_grupos(t: Texto, posiciones: Dict[str, Numero], ventanas: Dict[int, str]) -> Optional[Tuple[str, str]]:
    """Nombres de las dos muestras en el orden en que aparecen: “entre comillas”, (letra) o por el cambio."""
    citas = []
    for m in re.finditer(r"[“\"]([^”\"]{1,30})[”\"]", t.texto):
        if m.group(1) not in citas:
            citas.append(m.group(1))
    if len(citas) == 2:
        return citas[0], citas[1]
    letras = []
    for j in (1, 2):
        n = posiciones.get(f"n{j}") or posiciones.get(f"s{j}")
        m = re.search(r"\(([a-z]{1,3})\)", t.despues(n, 50)) if n else None
        letras.append(m.group(1).upper() if m else None)
    if all(letras) and letras[0] != letras[1]:
        return letras[0], letras[1]
    return None


def _intercambiar_muestras(an: Analisis):
    for a, b in (("n1", "n2"), ("xbar1", "xbar2"), ("s1", "s2"), ("nombre1", "nombre2"), ("datos1", "datos2")):
        v1, v2 = an.datos.get(a), an.datos.get(b)
        for k, v in ((a, v2), (b, v1)):
            if v is None:
                an.datos.pop(k, None)
            else:
                an.datos[k] = v
    cambio = {"1": "2", "2": "1"}
    for e in an.evidencias:
        if re.fullmatch(r"(n|xbar|s|datos)[12]", e.clave):
            e.clave = e.clave[:-1] + cambio[e.clave[-1]]
            e.motivo = re.sub(r"muestra [12]", lambda m: "muestra " + cambio[m.group(0)[-1]], e.motivo)


def extraer_relacion_desvios(an: Analisis, t: Texto, posiciones: Dict[str, Numero]):
    """Orden de las muestras y φ₀ para el TEMA IV.

    - Si una muestra es la del cambio (reacondicionadas, aleación propuesta, con aditivo) va en el NUMERADOR:
      φ = σ_nuevo/σ_referencia, así 'reducir el desvío un 12%' es φ < 0,88.
    - Si no hay cambio (dos establecimientos, dos tornos) va arriba la de MAYOR desvío muestral.
    - φ₀: 'reducción del 12% en el desvío' → 0,88; 'si no hay reducción' → 1 (y el % es el φ₁ del diseño).
    """
    roles, ventanas = {}, {}
    for j in (1, 2):
        n = posiciones.get(f"n{j}") or posiciones.get(f"s{j}")
        if n is not None:
            roles[j], ventanas[j] = _rol_muestra(t, n)
    nombres = _nombres_grupos(t, posiciones, ventanas)
    if nombres:
        an.datos["nombre1"], an.datos["nombre2"] = nombres
    m = re.search(RE_NUEVO, t.norm)
    etiquetas = next(((nv, rf) for p, nv, rf in GRUPOS_CAMBIO if m and re.match(p, m.group(0))), None)
    con_roles = roles.get(1) is not None or roles.get(2) is not None
    if con_roles:
        nuevo = 1 if roles.get(1) == "nuevo" or roles.get(2) == "ref" else 2
        if etiquetas and not nombres:
            an.datos["nombre1" if nuevo == 1 else "nombre2"] = etiquetas[0]
            an.datos["nombre2" if nuevo == 1 else "nombre1"] = etiquetas[1]
        if nuevo == 2:
            _intercambiar_muestras(an)
        an.datos["orden"] = "cambio"
        an.razones_tema.append(f"φ = σ({an.datos['nombre1']})/σ({an.datos['nombre2']}): arriba la muestra con el cambio, "
                               "abajo la de referencia (así una reducción del desvío es φ < φ₀).")
    elif an.datos.get("s1") and an.datos.get("s2"):
        if an.datos["s2"] > an.datos["s1"]:
            _intercambiar_muestras(an)
        an.datos["orden"] = "mayor"
        an.razones_tema.append(f"φ = σ({an.datos['nombre1']})/σ({an.datos['nombre2']}): sin un grupo 'nuevo', va arriba el "
                               "de mayor desvío muestral (j² ≥ 1).")
    elif etiquetas:   # diseño sin datos (IV-5): φ = σ_con/σ_sin
        an.datos["nombre1"], an.datos["nombre2"] = etiquetas
        an.datos["orden"] = "cambio"

    # φ₀ (y φ₁ si es un diseño 'si no hay reducción ... si la reducción es de un 30%')
    an.datos["phi0"] = 1.0
    hallado = False
    sin_cambio = _hay(r"(si|cuando) no (hay|existe|se (obtiene|logra|produce)) (una )?(reduccion|disminucion|aumento|"
                      r"incremento|mejora)|(si|cuando) no (reduce|disminuye|mejora|aumenta|baja|cambia|modifica)\b", t.norm)
    for i, n in t.libres():
        if not n.pct:
            continue
        ctx = t.antes(n, 80) + " " + t.despues(n, 50)
        if not _hay(r"(desvio|desviacion|variab|dispersion|\bbaj|reduc|disminu|aument|increment)", t.oracion(n.ini)):
            continue
        signo = -1 if _hay(r"(reduc|disminu|menor|baj)", ctx) else 1 if _hay(r"(aument|increment|mayor|super)", ctx) else 0
        if not signo:
            continue
        valor = round(1 + signo * n.fraccion, 10)
        t.usar(i)   # 'en más de un 20% ... si disminuyera sólo en un 20%': los dos son el mismo φ₀, no probabilidades
        if hallado:
            continue
        hallado = True
        if sin_cambio:
            _set(an, "phi1", valor, t, n, f"desvío un {fmt(n.valor)}% {'menor' if signo < 0 else 'mayor'} → φ₁ = {fmt(valor)}")
        else:
            _set(an, "phi0", valor, t, n, f"desvío un {fmt(n.valor)}% {'menor' if signo < 0 else 'mayor'} que el de "
                                          f"referencia → φ₀ = {fmt(valor)}", pisar=True)

    # probabilidades del planteo: dos (α y β, diseño) o una sola ('0,1 la probabilidad de cambio si ...' → α)
    # (el riesgo α puede haber salido antes con extraer_alpha: 'riesgo máximo del 5% de adoptar...')
    probs = _probs_diseno(t)
    if len(probs) >= 2:
        completar_diseno(an, t)
    elif len(probs) == 1:
        i, n = probs[0]
        if n.fraccion > 0.5 and "alpha" in an.datos:
            t.usar(i)
            _set(an, "beta", round(1 - n.fraccion, 10), t, n,
                 f"probabilidad {fmt(n.fraccion)} de tomar la decisión cuando el cambio sí se logra (potencia) → β = 1 - "
                 f"{fmt(n.fraccion)}")
        elif n.fraccion <= 0.5 and "alpha" not in an.datos:
            t.usar(i)
            _set(an, "alpha", n.fraccion, t, n, "probabilidad de tomar la decisión (el cambio) cuando no se justifica → α")


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


def _enteros_dato(t: Texto) -> List[Numero]:
    """Enteros que pueden ser frecuencias: sin %, sin las etiquetas de categoría (24", 36") ni años."""
    salida = []
    for n in t.nums:
        if n.pct or not n.es_entero:
            continue
        if re.match(r"\s*(\"|”|''|pulgadas|°|º|ºc)", t.texto[n.fin:n.fin + 9]):
            continue
        salida.append(n)
    return salida


def _observados_por_suma(t: Texto) -> Optional[Tuple[List[float], float]]:
    """'De 200 ventas recientes, 85 fueron de 24", 65 de 36" y 50 de 40"': las frecuencias observadas son los enteros
    seguidos que suman el total de la muestra dicho antes."""
    nums = _enteros_dato(t)
    for i, tot in enumerate(nums):
        for j in range(i + 1, len(nums)):
            suma = 0.0
            for k in range(j, len(nums)):
                suma += nums[k].valor
                if suma == tot.valor and k - j >= 1:
                    return [x.valor for x in nums[j:k + 1]], tot.valor
                if suma > tot.valor:
                    break
            break   # el bloque tiene que empezar justo después del total
    return None


def _filas_narradas(t: Texto) -> List[Tuple[str, List[float]]]:
    """Renglones de una tabla de contingencia contados en prosa, cada uno con su total: 'Turno mañana (500 piezas):
    450, 45 y 5. Turno tarde (800 piezas): 680, 80 y 40.' → [450, 45, 5], [680, 80, 40] (el total se descarta)."""
    filas = []
    for seg in re.split(r"\.\s+|;\s*", t.texto):
        sub = Texto(seg)
        nums = [n.valor for n in _enteros_dato(sub)]
        if len(nums) < 3:
            continue
        resto = None
        for k, v in enumerate(nums):
            otros = nums[:k] + nums[k + 1:]
            if v == sum(otros):
                resto = otros
                break
        if resto is None:
            continue
        etq = re.split(r"[(\d:,]", seg.strip())[0].strip()[:40] or f"Fila {len(filas) + 1}"
        filas.append((etq, resto))
    largos = {len(f[1]) for f in filas}
    return filas if len(filas) >= 2 and len(largos) == 1 else []


RE_RESTO = r"\b(el resto|los restantes|las restantes|los demas|las demas|el restante|la restante)\b"


def tabla_porcentajes(t: Texto) -> Optional[Tuple[List[List[float]], List[str], List[str]]]:
    """Tabla de contingencia dada en PORCENTAJES por fila: 'Se encuestó a 120 hombres y 80 mujeres... De los hombres,
    el 30% eligió A, el 45% B y el resto C. De las mujeres, el 40%...' → frecuencias = total del grupo × %.
    Devuelve (tabla, nombres de las filas, avisos) o None."""
    totales = []   # (raíces que nombran al grupo, N, posición, nombre)
    for n in t.nums:
        if n.es_entero and not n.pct and n.valor >= 5:
            cola = re.split(r"[\d.,;:?!]|\b(y|e|o|sobre|que|para|con|acerca|respecto|elegid|tomad|al azar)\b",
                            t.norm[n.fin:n.fin + 40])[0]
            palabras = [w for w in re.findall(r"[a-z]{4,}", cola)][:3]
            if palabras and re.match(r"\s+[a-z]", t.norm[n.fin:n.fin + 3]):
                totales.append(([w[:5] for w in palabras], n.valor, n.ini, " ".join(palabras)))
    # lo que distingue a cada grupo ('200 piezas del turno mañana' / '150 piezas del turno noche' → mañana / noche)
    totales = [([r for r in x[0] if not any(r in y[0] for y in totales if y is not x)], *x[1:]) for x in totales]
    totales = [x for x in totales if x[0]]
    filas, nombres, usados = [], [], set()
    for ini, fin in t._oraciones:
        ora = t.norm[ini:fin]
        pcts = [n for n in t.nums if ini <= n.ini < fin and n.pct]
        if len(pcts) < 1 or (len(pcts) < 2 and not _hay(RE_RESTO, ora)):
            continue
        if _hay(RE_CONF + r"|riesgo|significacion|probabilidad", ora):
            continue
        valores = [n.valor for n in pcts]
        if _hay(RE_RESTO, ora):
            valores.append(100 - sum(valores))
        if abs(sum(valores) - 100) > 0.5 or min(valores) < 0:
            continue
        # el grupo: un total dentro de la misma oración o un grupo contado antes y nombrado acá
        propio = [x for x in totales if ini <= x[2] < fin and x[2] < pcts[0].ini]
        grupo = propio[-1] if propio else None
        if grupo is None:
            cands = []
            for x in totales:
                pos = [m.start() for r in x[0] for m in [re.search(r"\b" + r, ora)] if m]
                if x[2] < ini and pos:
                    cands.append((min(pos), x[2], x))
            grupo = min(cands)[2] if cands else None
        if grupo is None or grupo[2] in usados:
            continue
        usados.add(grupo[2])
        filas.append([grupo[1] * v / 100 for v in valores])
        nombres.append(grupo[3])
    if len(filas) < 2 or len({len(f) for f in filas}) != 1 or len(filas[0]) < 2:
        return None
    avisos = ["La tabla venía en PORCENTAJES por fila: se pasó a frecuencias (total del grupo × %): " +
              "; ".join(f"{nm}: " + " / ".join(fmt(x) for x in f) for nm, f in zip(nombres, filas)) + "."]
    if any(abs(x - round(x)) > 0.01 for f in filas for x in f):
        avisos.append("Algunas frecuencias no dan enteras (los % estarán redondeados): revisalas.")
    else:
        filas = [[float(round(x)) for x in f] for f in filas]
    return filas, nombres, avisos


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
            an.datos["tabla_filas"] = [f[0] for f in mejor]
            an.evidencias.append(Evidencia("tabla", an.datos["tabla"], t.texto[mejor[0][2]:mejor[-1][3]],
                                           "filas de la tabla: " + ", ".join(f[0] for f in mejor)))
            return
        narr = _filas_narradas(t)
        if narr:
            an.datos["tabla"] = [f[1] for f in narr]
            an.datos["tabla_filas"] = [f[0] for f in narr]
            an.evidencias.append(Evidencia("tabla", an.datos["tabla"], "", "filas narradas en el texto (sin el total de "
                                                                       "cada renglón): " + ", ".join(f[0] for f in narr)))
            an.avisos.append("Revisá la tabla: se armó con los renglones narrados en el texto.")
            return
        tp = tabla_porcentajes(t)
        if tp:
            an.datos["tabla"] = tp[0]
            an.datos["tabla_filas"] = tp[1]
            an.datos["chi_grupos"] = "filas"
            an.evidencias.append(Evidencia("tabla", tp[0], "", "filas (" + ", ".join(tp[1]) + "): total del grupo × "
                                                               "porcentaje de cada categoría"))
            an.avisos += tp[2]
            return
        # dos proporciones narradas: 'muestra de 250 ... 20 defectuosos', '32 postes de cada uno ... 10 y 20'
        tot = [n for n in t.nums if n.es_entero and not n.pct and (
            _hay(r"(muestra|muestras|total)[^0-9]{0,15}$|cada un", t.antes(n, 30) + t.despues(n, 20)) or
            (_hay(r"\b(se )?(revisaron|inspeccionaron|controlaron|tomaron|eligieron|seleccionaron|analizaron|examinaron|"
                  r"probaron|encuestaron|colocaron|trataron|fabricaron|produjeron|revisan|inspeccionan|controlan|toman|"
                  r"eligen|seleccionan|analizan|examinan|prueban|encuestan|de)\s*$", t.antes(n, 30)) and
             _hay(r"^\s*[a-z]{3,}", t.despues(n, 20)) and
             not _hay(r"^\s*[a-z]*\s*(resultaron|fueron|salieron|eran|tenian|presentaron|estaban)", t.despues(n, 30))))]
        cuentas = [n for n in t.nums if n.es_entero and not n.pct and n not in tot
                   and (_hay(r"(arroj[a-z]* un resultado de|reponer|encontr[a-z]*|y)\s*$", t.antes(n, 30)) or
                        _hay(r"^\s*[a-z]*\s*(resultaron|fueron|salieron|eran|tenian|presentaron|estaban)", t.despues(n, 30)))]
        if len(tot) == 1 and len(cuentas) < 3:
            # un mismo tamaño para todos los grupos ('cada semana se revisan 300 ... 21, 12, 14 y 11 defectuosas'):
            # los conteos son los demás enteros menores que ese total
            resto = [n for n in t.nums if n.es_entero and not n.pct and n not in tot and n.valor < tot[0].valor]
            if len(resto) >= 3:
                filas = [[n.valor, tot[0].valor - n.valor] for n in resto]
                an.datos["tabla"] = filas
                an.datos["tabla_filas"] = [f"Grupo {k + 1}" for k in range(len(filas))]
                an.datos["tabla_columnas"] = ["Con el atributo (r)", "Sin el atributo (n − r)"]
                an.datos["chi_grupos"] = "filas"
                an.evidencias.append(Evidencia("tabla", filas, "", f"{len(filas)} grupos de {fmt(tot[0].valor)}: "
                                               + ", ".join(fmt(n.valor) for n in resto) + " (columnas: sí / no)"))
                an.avisos.append("Revisá la tabla: se armó con (éxitos, fracasos) de cada grupo a partir del texto.")
                return
        if tot and len(cuentas) >= 2:
            n1 = tot[0].valor
            n2 = tot[1].valor if len(tot) > 1 else n1
            r1, r2 = cuentas[0].valor, cuentas[1].valor
            an.datos["tabla"] = [[r1, n1 - r1], [r2, n2 - r2]]
            an.datos["tabla_filas"] = [f"Grupo 1 (n = {fmt(n1)})", f"Grupo 2 (n = {fmt(n2)})"]
            an.datos["tabla_columnas"] = ["Con el atributo (r)", "Sin el atributo (n − r)"]
            an.datos["chi_grupos"] = "filas"
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
        por_suma = _observados_por_suma(t)
        if por_suma and (len(cuentas) < 2 or len(por_suma[0]) > len(cuentas)):
            an.datos["observados"] = por_suma[0]
            an.evidencias.append(Evidencia("observados", por_suma[0], "", f"frecuencias del texto que suman el total "
                                                                         f"de la muestra ({fmt(por_suma[1])})"))
        elif len(cuentas) >= 2:
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
            r"valor critico|limites de control|cuantas defectuosas se deberan|cual es la resistencia media muestral minima|"
            r"\baql\b|\bltpd\b|riesgo del (proveedor|productor|comprador|consumidor)|"
            r"(lote|partida)s? (que [a-z ]{0,30})?(definid|consider|llam|calific)[a-z]* (como )?\W?mal|"
            r"de (las|los) (partidas|lotes) (considerad[oa]s )?mal|a partir de cuant[oa]s|"
            r"probabilidad[^.?]{0,40}(rechac|rechaz)[a-z]* [a-z ]{0,25}(lote|partida)s? (bueno|buena|que cumple)|"
            r"hipotesis nula (se )?(esta|estan|se esta) (ensayando|poniendo a prueba|probando|contrastando)|"
            r"cuant[oa]s? [a-z ]{0,40}(habra que|hay que|hara falta|hacen falta) (deten|rechaz|aconsej|concluir|adopt|acept)|"
            r"cuant[oa]s? [a-z ]{0,40}(deberian|deberan|habria que|tendrian que|harian falta|haria falta|hacen falta|"
            r"se necesitan|se necesitarian)[a-z0-9 ]{0,40}para "
            r"(aconsejar|rechazar|detener|recomendar|concluir|adoptar|aceptar|explotar|cambiar))",
            norm) or (_hay(r"(indicar|establecer|plantear) la hipotesis", norm) and not _hay(r"(realizar|efectuar) el ensayo", norm)):
        if not _hay(r"(realizar|efectuar) el ensayo|que decision|se aconseja|determinar si|indicar si|es concluyente|"
                    r"(se puede|puede) (asegurar|afirmar)", norm):
            return "diseno", ("Pide diseñar el ensayo: H0 (criterio), condición de rechazo (valor crítico), "
                              "n y regla de decisión.")
    if _hay(r"(cuant[oa]s? [a-z ]{0,40}(mas|habria que|deberan|deberian|se deberan|adicionales|extra|hay que|hara falta|"
            r"hacen falta|harian falta|haria falta|se necesitan|se necesitarian|se requieren|se requeririan|en total)|"
            r"tamano (adecuado |necesario )?de "
            r"(la )?muestra|que tamano|cuantas? [a-z]+ habria|calcular (el )?(nuevo )?tamano|recalcular tamano|"
            r"durante cuantos|a cuantos|como se disminuye el error|tamano de muestra (es|extraido)|"
            r"que valor debe tener (el tamano )?n\b|cual (debe|deberia) ser (el valor de )?n\b|"
            r"(inversion|costo|gasto) (adicional|total|extra))", norm) and \
            not _hay(r"con (ese|este|dicho) tamano", norm):
        return "n", "Pregunta cuántas unidades hacen falta: tamaño de muestra (y Δn si ya hay una muestra)."
    if _hay(r"(maxim[oa]|minim[oa])", norm) and _hay(r"(con una probabilidad de|confianza|estimar|con (un )?\d+ ?% de riesgo)", norm) \
            and not _hay(r"(tamano|cuant)", norm):
        return "ic", "Pide un valor máximo / mínimo del parámetro con cierta confianza: límite de confianza UNILATERAL."
    if _hay(r"^\W*(se considera|se puede|puede|se aconseja|aconseja|es correct|existe|se recomienda|asumiendo|"
            r"si se establece|con un|se justifica)", norm) and not _hay(r"(cual|calcular|hallar)[^.?]{0,30}probabilidad", norm) \
            and not _hay(r"(entre que (valores|limites)|dentro de que limites|intervalo de confianza)", norm):
        return "ensayo", "Pide tomar una decisión sobre una afirmación: ensayo de hipótesis."
    if _hay(r"¿\s*(y )?(realmente |efectivamente )?(subio|subieron|aumento|aumentaron|disminuyo|disminuyeron|bajo|bajaron|"
            r"mejoro|mejoraron|empeoro|cambio|cambiaron|vario|variaron|se modifico|se redujo|se redujeron|crecio|"
            r"decrecio|influye|influyen|difiere|difieren|depende|dependen|hay diferencia|es (mayor|menor|distint|diferente)|"
            r"son (mayores|menores|distint|diferentes)|esta cargad|conviene|alcanza|alcanzan)\b", norm):
        return "ensayo", "Pregunta si el parámetro cambió / difiere: ensayo de hipótesis."
    # '¿el tratamiento aumenta el rinde?', '¿la tinta alarga la duración?': pregunta por sí o por no si hay un efecto
    if _hay(r"¿(?![^?]*probabilidad)(?!\s*(cuant|cual|que (valor|diferencia|porcentaje|aumento|incremento|reduccion|disminucion)|"
            r"entre que|con que|a partir))[^?]{0,60}\b(aumenta|aumentan|reduce|reducen|disminuye|disminuyen|mejora|mejoran|"
            r"empeora|influye|influyen|afecta|afectan|baja|bajan|sube|suben|supera|superan|difiere|difieren|depende|"
            r"dependen|cambia|cambian|alarga|alargan|acorta|incrementa|incrementan|rinde mas|rinden mas)\b", norm):
        return "ensayo", "Pregunta si hay un efecto (aumenta / reduce / influye): ensayo de hipótesis."
    if _hay(r"(cual|que) (seria|sera|es) la (conclusion|decision)", norm):
        return "ensayo", "Pide la conclusión / decisión: ensayo de hipótesis."
    if _hay(r"(cual|calcular|hallar|determinar|que)[^.?]{0,30}(probabilidad|error de tipo ii|potencia)|error de tipo ii|"
            r"probabilidad de (no )?(detectar|aceptar|rechazar|detener|revisar)|"
            r"(con que|que) probabilidad|^\W*(y )?(cual (es|seria) )?(la )?probabilidad\b", norm):
        return "beta", "Pide una probabilidad de error: β (no detectar) o potencia 1-β (detectar)."
    if _hay(r"(estimar|intervalo|limites de confianza|entre que (valores|limites)|dentro de que limites|"
            r"diferencia (de aumento de peso )?minima|incremento porcentual|desviacion estandar maxima|"
            r"cual es el incremento|cual es la diferencia)", norm):
        return "ic", "Pide estimar el parámetro: intervalo de confianza P(A ≤ θ ≤ B) = 1-α."
    if _hay(r"(se puede|puede|se aconseja|aconseja|se recomienda|recomendaria|es correct|se considera|considera|"
            r"existe|hay (algun |algún )?(razon|evidencia|motivo|fundamento)|asegurar|afirmar|aseguraria|decision|"
            r"concluyente|se continuaria|preocup|alarm|hay que (ajustar|detener|revisar|cambiar|corregir|rechazar)|"
            r"conviene|corresponde (ajustar|detener|revisar|rechazar)|tiene fundamento|"
            r"es posible|se justifica|se rechaza|ensayar|verificar|determinar si|comprobar|cumple|se arriba|"
            r"indique las conclusiones|que se puede decir|cual sera la conclusion|que decision|\bdecidir\b|"
            r"(hacer|realizar|efectuar) el (ensayo|contraste|test)|que se concluye|que puede concluirse|"
            r"que (conclusion|decision) (se )?(saca|toma|obtiene)|se puede refutar|refutar|que se decide|que decide|"
            r"que se recomienda|que recomienda)", norm + " " + contexto):
        return "ensayo", "Pide tomar una decisión sobre una afirmación: ensayo de hipótesis."
    # '¿Debe detenerse la máquina?', '¿Se debe mantener al proveedor?', '¿Se recalibra?': decidir una acción
    if _hay(r"\bdeb(e|en|eria|erian|era|eran) (se |la |lo |el |los |las )?(deten|par[ae]r|recalibr|ajust|rechaz|acept|"
            r"manten|cambi|revis|compr|adopt|lanz|continu|interven|correg|reemplaz|aprob|segui|implement)|"
            r"^\W*(se )?(detiene|detendra|rechaza|rechazara|acepta|aceptara|recalibra|ajusta|interviene|lanza|lanzara|"
            r"compra|comprara|adopta|adoptara|implementa|implementara|cambia|mantiene|continua|explota|aprueba)\b|"
            r"\bindicar si\b", norm):
        return "ensayo", "Pide decidir una acción (detener, aceptar, mantener...): ensayo de hipótesis."
    return "no_soportado", "No se reconoció qué pide: elegí el tipo a mano."


def detectar_cola(norm: str, planteo_norm: str, tema: str, datos: dict) -> Tuple[str, str]:
    """Dirección de H1 según las palabras del inciso (y, si no alcanza, del planteo)."""
    ref = {"media": ("xbar", "mu0"), "varianza": ("desvio", "sigma0"), "proporcion": ("p_hat", "p0")}.get(tema)
    # hipótesis planteada DESPUÉS de ver la muestra (I-32, I-36): unilateral hacia donde apunta la muestra, aunque el
    # problema sea de control (el bilateral no se usa a posteriori)
    if ref and ref[0] in datos and ref[1] in datos and datos[ref[0]] != datos[ref[1]] and \
            _hay(r"(a la luz de (los )?(datos|resultados)|luego de (evaluar|ver|analizar) (los )?(resultados|datos)|"
                 r"despues de (evaluar|ver|analizar) (los )?(resultados|datos))", norm + " " + planteo_norm):
        lado = "derecha" if datos[ref[0]] > datos[ref[1]] else "izquierda"
        return lado, ("La hipótesis se plantea «a la luz de los datos» (después de ver la muestra): unilateral hacia "
                      "donde apunta la muestra; el bilateral no se usa a posteriori.")
    # 'conviene cambiar de aleación', 'se debe cambiar el proveedor': 'cambiar' es la ACCIÓN que se decide, no la
    # dirección del parámetro (la dirección la da lo que se quiere lograr con el cambio)
    norm = re.sub(r"\bcambi(ar|arse|aria|ara)\s+(de|el|la|los|las|a|al|por)\b", " ", norm)
    for texto, donde in ((norm, "inciso"), (planteo_norm, "planteo")):
        # 'reduce el desvío en más de un 15%': 'en más de' mide CUÁNTO, la dirección la da el verbo
        texto = re.sub(r"\b(en|por) (mas|menos) de\b", " ", texto)
        # especificaciones de control (criterio optimista)
        if _hay(r"(mayor o igual|por lo menos|como minimo|minimo admisible|minima es de|resistencia media minima|"
                r"no menos de)", texto) and donde == "planteo" and not _hay(r"(aument|increment)", texto):
            return "izquierda", "La especificación es un mínimo (≥ μ₀): se rechaza si la muestra da BAJO → cola izquierda."
        if _hay(r"(menor o igual|como maximo|a lo sumo|no debe superar|no mas de|no supere|no exceda|no sobrepase|"
                r"no debe exceder|no puede (superar|exceder))", texto) and donde == "planteo" \
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
        if tema == "proporcion" and not (mas or menos) and _hay(r"defectuos", texto) and \
                _hay(r"(deten|detien|rechaz|revis)", norm + " " + planteo_norm):
            return "derecha", ("Control de la fracción defectuosa: se detiene / rechaza cuando aparecen MUCHAS defectuosas "
                               "→ H1: p > p₀ → cola derecha.")
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
    # control de rutina de un proceso (calibrar / detener / recalibrar) sin dirección: criterio optimista, bilateral
    if tema == "media" and _hay(r"(recalibr|\bcalibrad|reajust|regulad[oa] (para|en)|deten(er|erla|erlo|erse|ga)|"
                                r"parar la (maquina|linea|produccion)|periodicamente|control (periodico|de rutina|del proceso))",
                                planteo_norm + " " + norm):
        return "bilateral", ("Control de rutina de un proceso (se detiene / recalibra si se desajusta) sin decir hacia dónde: "
                             "criterio OPTIMISTA, H0: μ = μ₀ y se detiene tanto si la media sube como si baja → bilateral.")
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
    m = re.search(r"\b(efectuar|realizar|hacer|comprar|adoptar|implementar|lanzar|invertir|cambiar)[a-z]* "
                  r"equivocadamente( (el|la|los|las) [a-z]+)?", norm)
    if m:
        return "pesimista", (f"El riesgo que se fija es el de '{m.group(0)}': esa acción es la que se toma al rechazar "
                             "H0, así que H0 supone que NO conviene hacerlo y se exige evidencia (criterio PESIMISTA).")
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
        if _hay(r"(probabilidad|riesgo|confianza|valga)[^0-9]{0,12}$", a) and not (
                tema == "proporcion" and _hay(r"\b(si|cuando)\b[^0-9.;]{0,40}(tuviera|fuera|fuese|tiene|es) una probabilidad (de )?$", a)):
            continue   # en una proporción 'si el cero tuviera una probabilidad de 0,05' ES el valor alternativo
        if _hay(r"^\s*[a-z%]{0,8}\s*(a|al|hasta)\s+\d", d) and _hay(r"\bde\s*$", a):
            continue   # 'un desplazamiento de 5 ppm a 5,25 ppm': el alternativo es el segundo
        if _hay(r"(jornada|turno|periodo|lapso|durante)[a-z ]{0,10}\bde\s*$", a) and \
                _hay(r"^\s*(horas|hs|minutos|min|dias|semanas)\b", d):
            continue   # 'durante una jornada de 8 horas'
        if not n.pct and n.es_entero and _hay(r"^\s*" + UNIDADES_MUESTRA + r"\b", d) and \
                not _hay(r"\b(es|sea|fuera|fuese|vale|valiera|media|promedio)\b[a-z ]{0,5}\s*$", a):
            continue   # 'controles de 16 envases' es un tamaño de muestra
        rel = _hay(r"(aument|increment|disminu|reduc|baj|desplazamiento|mejor)[a-z]*( la [a-z]+ media)?( en| de| del)?( un| el)?"
                   r"( mas de)?\s*$", a) or _hay(r"^\s*(superior|mayor|inferior|menor|mas|menos)", d) or \
            (n.pct and _hay(r"(aumento|incremento|disminucion|reduccion|baja|suba|mejora)( [a-z]+){1,3}? (es|fue|sea|fuera|"
                            r"resulta|resulto) (del|de)( un)?\s*$", a))   # 'si la reducción lograda es del 20%'
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
    if _hay(r"\bno (detect|efectu|concret|inici|deten|implement|cambi|revis|adopt|compr|realic|realiz|modific|lanz|"
            r"pauta|explot|recomend|aconsej)[a-z]*\b|"
            r"(no detectar|no efectuar|no concretar|no iniciar|no detener|no implementar|no cambiar|no revisarlo|"
            r"no efectuar el ajuste|aceptar|de que el lote sea aceptado|error de tipo ii|no adoptar|no comprar|"
            r"no realizar|no modificar|no hacer|(ser|sea|sean) aceptad|se acepte|aceptarl[oa]|quedarse con)", norm):
        return "beta"
    return "potencia"


_NEG = r"\b(no|nunca|jamas)\b"
_QUE_PIDE_PROP = re.compile(r"(proporcion|porcentaje|fraccion|cuantos|cuantas|parte)\b[a-z ,]{0,50}?\b(que|quienes)\s+"
                            r"((?:si|no|nunca|jamas)\s+)?(?:(?:lo|la|los|las|se|le|les)\s+)?([a-z]{4,})")


def complemento_r(planteo_norm: str, r: int, inc_norm: str) -> Optional[str]:
    """'38 de ellos manifestaron que NO volverían' y se pide la proporción de los que SÍ volverían (o al revés):
    lo contado es el complemento de lo pedido → r = n - 38. Devuelve el verbo en común si hay que complementar."""
    m = re.search(r"(?<![\d.,])" + str(r) + r"(?![\d,])([^.;?]{0,90})", planteo_norm)
    q = _QUE_PIDE_PROP.search(inc_norm)
    if not m or not q:
        return None
    clausula, verbo = m.group(1), q.group(4)
    raiz = verbo[:5]
    w = re.search(r"((?:\b(?:no|nunca|jamas)\s+)?(?:(?:lo|la|los|las|se|le|les)\s+)?)\b(" + re.escape(raiz) + r"[a-z]*)", clausula)
    if not w:
        return None
    neg_r = _hay(_NEG, w.group(1))
    neg_q = bool(q.group(3)) and _hay(_NEG, q.group(3))
    return w.group(2) if neg_r != neg_q else None


def extraer_params_inciso(inc: Inciso, an: Analisis, previo: Dict):
    t = Texto(inc.texto)
    norm = t.norm
    p = inc.params
    tema = p.get("tema", an.tema)

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
    if tema == "media" and inc.tipo in ("ic", "ensayo", "n", "diseno") and not _hay(r"probabilidad", norm):
        sub = Analisis(inc.texto, tema=tema)
        extraer_media(sub, t, solo_mu0=inc.tipo == "diseno")
        extraer_desvio(sub, t)
        if "desvio" in sub.datos and _hay(r"σ\s*=", inc.texto):
            sub.datos["sigma_conocido"] = True   # 'con un σ = 0,5': desvío poblacional
        for k in ("xbar", "desvio", "sigma_conocido"):
            if k in sub.datos and k not in an.datos:
                an.datos[k] = sub.datos[k]
                an.evidencias += [e for e in sub.evidencias if e.clave == k]
        m = re.search(r"(jornada|turno|periodo|lapso)[a-z ]{0,10}\bde (\d+(?:,\d+)?) (horas|hs|minutos|min)\b", norm)
        mu0_ev = next((e for e in an.evidencias if e.clave == "mu0"), None)
        if m and an.datos.get("mu0") and mu0_ev and "n" not in an.datos:
            # 'tiempo estándar 360 segundos ... durante una jornada de 8 horas' → n = 8·3600/360 = 80 conjuntos
            seg = {"horas": 3600, "hs": 3600, "minutos": 60, "min": 60}
            u0 = re.search(r"(segundos|seg|minutos|min|horas|hs)\b", normalizar(mu0_ev.fragmento.split(fmt(an.datos["mu0"]))[-1]))
            if u0:
                total = parse_num(m.group(2)) * seg[m.group(3)]
                por_unidad = an.datos["mu0"] * {"segundos": 1, "seg": 1, "minutos": 60, "min": 60, "horas": 3600, "hs": 3600}[u0.group(1)]
                p["n"] = int(total // por_unidad)
                inc.razones.append(f"En el período ({m.group(2)} {m.group(3)}) se hacen n = {p['n']} unidades "
                                   f"(tiempo total / tiempo estándar).")
        if "mu0" in sub.datos:
            p["mu0"] = sub.datos["mu0"]
            if inc.tipo == "diseno" and "mu0" not in an.datos:
                # 'si se toma como valor nominal 5 ppm': vale para los incisos siguientes
                an.datos["mu0"] = sub.datos["mu0"]
                an.evidencias += [e for e in sub.evidencias if e.clave == "mu0"]
    if tema == "media":
        extraer_costos(p, an, t)   # 'si la compañía cobrara una comisión del 2%'
        if "comision" in p:
            inc.razones.append(f"Se descuenta una comisión del {fmt(p['comision'] * 100)}%: neto = bruto·(1 - k).")
        if an.datos.get("costo_fijo") and _hay(r"(sin descontar|bruto)", norm):
            p["mu1_bruto"] = True
    if tema in ("media", "varianza") and inc.tipo in ("beta", "curva"):
        sub = Analisis(inc.texto, tema=tema)
        if extraer_n(sub, t) is not None:   # 'si las muestras de control son de 20 conjuntos'
            p["n"] = sub.datos["n"]
            inc.razones.append(f"El inciso fija el tamaño de muestra: n = {p['n']}.")
    if tema == "proporcion" and inc.tipo in ("ic", "n", "ensayo"):
        sub = Analisis(inc.texto, tema=tema)
        # en un inciso de tamaño de muestra 'disminuir en un 30% la relación' es la reducción, no un dato
        ts = Texto(inc.texto) if inc.tipo == "n" else t
        extraer_proporcion(sub, ts)
        claves = ("r", "p_hat") + (("p0",) if inc.tipo == "ensayo" else ())
        for k in claves:
            if k in sub.datos:
                p[k] = sub.datos[k]
                inc.razones.append(f"Dato del inciso: {k} = {fmt(sub.datos[k])}.")
        # 'se encontraron 10 piezas SIN defectos' y se pregunta por las malas: r = n - 10
        ev_r = next((e for e in sub.evidencias if e.clave == "r"), None)
        if ev_r and _hay(r"\b" + str(p["r"]) + r" [a-z]* ?(sin defectos?|buen[oa]s|no defectuos|en buen estado|aprobad)", norm) \
                and _hay(r"(mal[oa]s|defectuos|con defectos?|fallad)", norm):
            p["r_buenas"] = True
            inc.razones.append(f"Los {p['r']} casos contados son los BUENOS y se pregunta por los malos: r = n - {p['r']}.")
    if tema == "proporcion" and inc.tipo in ("ic", "n", "ensayo", "beta", "diseno") and "r" not in p \
            and an.datos.get("r") is not None and not p.get("r_buenas"):
        verbo = complemento_r(normalizar(an.planteo), int(an.datos["r"]), norm)
        if verbo:
            p["r_buenas"] = True
            inc.razones.append(f"Los {an.datos['r']} casos contados son los del caso CONTRARIO al que se pregunta "
                               f"(uno con 'no {verbo}' y el otro sin la negación): r = n - {an.datos['r']}.")
    if tema == "proporcion" and inc.tipo in ("diseno", "beta", "curva", "n"):
        # 'AQL = p0 = 1,5% y LTPD = p1 = 4%'
        for clave, patron in (("p0", r"(aql|\bp\s*[0₀])\s*=\s*(p\s*[0₀]\s*=\s*)?$"), ("p1", r"(ltpd|\bp\s*[1₁])\s*=\s*(p\s*[1₁]\s*=\s*)?$")):
            for i, n in t.libres():
                if (n.pct or n.valor < 1) and _hay(patron, t.antes(n, 25)):
                    t.usar(i)
                    p[clave] = n.fraccion
                    inc.razones.append(f"{SIMBOLO[clave]} = {fmt(n.fraccion)} ({'AQL' if clave == 'p0' else 'LTPD'}).")
                    break
        if inc.tipo != "n" and "n" not in p:
            # 'si se eligieran 100 árboles', 'con una muestra de 200': el plan es para ese n
            sub = Analisis(inc.texto, tema=tema)
            if extraer_n(sub, t) is not None:
                p["n"] = sub.datos["n"]
                inc.razones.append(f"El inciso fija el tamaño de muestra: n = {p['n']}.")
            else:
                for i, n in t.libres():
                    if n.es_entero and not n.pct and n.valor >= 2 and \
                            _hay(r"(eligieran|tomaran|seleccionaran|revisaran|controlaran|inspeccionaran|enviaran|"
                                 r"\bse [a-z]+(aran|ieran|asen|iesen)|con una muestra de|si fueran)" + _R + r"{0,15}$",
                                 t.antes(n, 40)):
                        t.usar(i)
                        p["n"] = int(n.valor)
                        inc.razones.append(f"El inciso fija el tamaño de muestra: n = {p['n']}.")
                        break
        if an.datos.get("rc") is not None and "n" not in an.datos and _hay(r"acept", norm) and \
                _hay(r"(valor|cuanto|cual)[a-z ]{0,25}\bn\b|tamano", norm):
            # plan con r_c dado y n a buscar: 'probabilidad de aceptación (con el 1% defectuoso) mayor a 0,95'
            for i, n in enumerate(t.nums):
                # el % es la calidad del lote (p₀), aunque antes se haya tomado como α ('un lote con 1% de falladas')
                if n.pct and "p0" not in p and an.datos.get("p0") is None:
                    t.usar(i)
                    p["p0"] = n.fraccion
                    if p.get("alpha") == n.fraccion:
                        p.pop("alpha")
                elif not n.pct and 0.5 < n.valor < 1:
                    t.usar(i)
                    p["prob_aceptar"] = n.valor
            if "prob_aceptar" in p:
                p.pop("beta", None)
                inc.tipo = "n"
                inc.razones.append(f"Plan con r_c = {an.datos['rc']} dado: se busca el mayor n con P(aceptar | p₀) ≥ "
                                   f"{fmt(p['prob_aceptar'])}.")
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
        cola, razon = detectar_cola(norm, getattr(an, "_norm_cola", None) or normalizar(an.planteo), tema, an.datos)
        sin_pistas = _cuenta(P_MAS + P_MENOS + P_DISTINTO, norm) == 0
        if inc.tipo in ("beta", "curva") and "tail" in previo or (sin_pistas and "tail" in previo and
                                                                   _hay(r"misma conclusion|idem|anterior", norm)):
            cola, razon = previo["tail"], "Se mantiene la cola del ensayo del inciso anterior."
        p["tail"] = cola
        inc.razones.append(razon)

    if tema == "dos_varianzas" and inc.tipo in ("ic", "n"):
        if _hay(r"(desvios|desviaciones|desvio)", norm):
            p["sobre"] = "desvios"
        elif _hay(r"varianzas?", norm):
            p["sobre"] = "varianzas"
        if "sobre" in p:
            inc.razones.append("La relación es entre los " + ("DESVÍOS σ₁/σ₂ (raíz de la de varianzas)."
                                                              if p["sobre"] == "desvios" else "VARIANZAS σ₁²/σ₂²."))

    if inc.tipo == "ic":
        if _hay(r"(total|peso total|produccion total)", norm) and "N" in an.datos:
            p["total"] = True
            inc.razones.append("Pide el TOTAL poblacional: se multiplica el IC de la media por N.")
        # 'mínima de 14.000 hs' es una especificación (lleva un número), no un límite de la estimación
        norm_cota = re.sub(r"(maxim[oa]|minim[oa])s?\s+(de|es de|admisible de|permitid[oa] de)?\s*\d", " ", norm)
        if _hay(r"(maxim[oa])", norm_cota):
            p["cota"] = "sup"
            inc.razones.append("Pide un valor MÁXIMO: límite de confianza unilateral superior (α entero en una cola).")
        elif _hay(r"(minim[oa])", norm_cota):
            p["cota"] = "inf"
            inc.razones.append("Pide un valor MÍNIMO: límite de confianza unilateral inferior (α entero en una cola).")

    if inc.tipo == "n":
        r = extraer_error(t)
        if r:
            clave, valor, n = r
            if clave == "e" and tema == "proporcion" and n is not None and n.pct:
                valor = n.fraccion   # 'error de ± 2%' en una proporción es 0,02
            p[clave] = valor
            inc.razones.append(f"{'Error admitido e' if clave == 'e' else 'Reducción pedida'} = {fmt(valor)}.")
            if clave == "reduccion" and tema == "proporcion" and _hay(r"relacion", norm):
                p["reduce_relacion"] = True
                inc.razones.append("Lo que se reduce es la RELACIÓN entre límites B/A del intervalo anterior.")
        # 'cada people meter cuesta 320 U$s' / 'el costo por unidad es de 15 $': inversión = unidades × costo
        m = re.search(r"(cada [a-z ]{1,30}(cuesta|vale|tiene un costo de|sale)|costo (unitario|por unidad|de cada [a-z ]{1,25})"
                      r"( es)?( de)?)\s*(u\$s|\$|usd)?\s*(\d[\d.,]*)", normalizar(an.planteo + " " + inc.texto))
        if m:
            c = parse_num(m.group(m.lastindex))
            if c:
                p["costo_unitario"] = c
                inc.razones.append(f"Costo por unidad = {fmt(c)}: se calcula la inversión.")
        if tema in ("varianza", "dos_varianzas"):
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
                    if previo.get("tail"):   # es el mismo ensayo con otro n: misma cola ('reducir' habla de β)
                        p["tail"] = previo["tail"]
                    break

    if inc.tipo in ("beta", "diseno", "curva"):
        # en el tema IV el % es respecto del desvío de referencia: 'reducción del 30%' → φ₁ = 0,70
        base = {"media": an.datos.get("mu0"), "varianza": an.datos.get("sigma0"),
                "proporcion": an.datos.get("p0"), "dos_varianzas": 1.0}.get(tema)
        r = _valor_alternativo(t, base, tema)
        clave = {"media": "mu1", "varianza": "sigma1", "proporcion": "p1", "dos_varianzas": "phi1"}.get(tema, "mu1")
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
            # 'hacer el ensayo dos veces (muestras independientes): que ninguna / alguna / ambas lo detecten'
            m = re.search(r"\b(dos|tres|cuatro|cinco|\d+) (veces|muestras|ensayos|controles)\b", norm)
            if m and _hay(r"(ningun[oa]|alguna|al menos un[oa]|ambas|ambos|todas|todos|las dos|los dos)", norm):
                k = PALABRAS_NUM.get(m.group(1)) or int(m.group(1))
                if k >= 2:
                    p["repeticiones"] = k
                    p["combina"] = ("ninguna" if _hay(r"ningun[oa]", norm) else
                                    "alguna" if _hay(r"(alguna|al menos un[oa])", norm) else "todas")
                    inc.razones.append(f"El ensayo se repite {k} veces con muestras independientes: se combinan las "
                                       f"probabilidades (P de que {p['combina']} lo detecte"
                                       f"{'n' if p['combina'] == 'todas' else ''}).")

    if an.datos.get("doble"):
        nombra_los_dos = _hay(r"(promedio|\bmedi[oa]\b)", norm) and _hay(r"(desvio|desviacion|varianza)", norm)
        if (inc.tipo == "ensayo" and not _hay(r"(desvio|desviacion|varianza)", norm)) or \
                (inc.tipo == "ic" and nombra_los_dos):
            p["ambos"] = True
            inc.razones.append("Se piden los dos parámetros (doble condición): se calcula para la media y para el desvío."
                               if inc.tipo == "ic" else
                               "Doble condición: se hacen los dos ensayos (μ y σ); la recomendación exige rechazar ambas H0.")

    if an.datos.get("doble") and "tail" in p and not p.get("ambos"):
        propia = an.datos.get("tail_mu" if tema == "media" else "tail_sigma")
        if propia:
            p["tail"] = propia
            inc.razones.append(f"Doble condición: el ensayo sobre {'la media' if tema == 'media' else 'el desvío'} "
                               f"tiene su propia dirección → cola {propia}.")

    if tema == "dos_medias":
        from .dos_muestras import params_dos_medias   # TEMA V: sujeto, cola, δ₀ / h, porcentual
        params_dos_medias(inc, an, t, previo)


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
        # valores del parámetro, no probabilidades: 'disminuir dicho porcentaje al 10%', 'porcentaje ... del 6%',
        # 'un 10% superior al actual'
        if _hay(r"(baj|sub|disminu|reduc|aument|increment|llev|lleg)[a-z]*( [a-z]+){0,3} (al|a|en|hasta)\s*$|"
                r"(porcentaje|proporcion|fraccion|penetracion|presencia|tasa)( [a-z]+){0,3} (al|a|del|de|en|es del|es de)\s*$|"
                r"(se detecta|se detecto|se obtuvo|se observ|arroj|result)[a-z ]{0,30}\b(del|de)\s*$|"
                r"(aql|ltpd|\bp\s*[01₀₁]|\bmu\s*[01₀₁]|μ\s*[01₀₁]?)\s*=\s*$|(σ|desvio|desviacion)[^0-9]{0,20}$", a) or \
                _hay(r"^\s*(superior|inferior|mayor|menor|mas|menos)\b", d):
            continue
        if (_hay(r"(probabilidad|riesgo|rechac|rechaz|deten|seguridad|certeza|detect|implement|adopt|concret|equivocad|"
                 r"erronea|indebid|modific)", ctx) or _hay(r"probabilidad[^0-9;]{0,110}$", t.antes(n, 120))) and \
                not _hay(r"^[^,;]{0,12}(defectuos|de unidades|confianza)", d[:25]):
            probs.append((i, n))
    return probs


def _probs_diseno(t: Texto):
    return extraer_diseno(None, t)


def _asignar_alpha_beta(t: Texto, probs):
    """De dos probabilidades, cuál es α (riesgo si H0 es cierta) y cuál es β / potencia."""
    (i1, n1), (i2, n2) = probs[0], probs[1]
    es_a1 = _alpha_de(t, i1, n1) is not None
    es_a2 = _alpha_de(t, i2, n2) is not None
    previo = t.norm[max(0, n1.ini - 120):n1.ini]
    if _hay(r"^[^.;]{0,25}respectivamente", t.norm[n2.fin:]):
        # 'riesgos del consumidor (β) y del proveedor (α) del 10% y 5% respectivamente': manda el orden de los nombres
        pos_a = [m.start() for m in re.finditer(r"(proveedor|productor|\(α\)|\balfa\b|tipo i\b)", previo)]
        pos_b = [m.start() for m in re.finditer(r"(consumidor|comprador|\(β\)|\bbeta\b|tipo ii\b)", previo)]
        if pos_a and pos_b:
            es_a1, es_a2 = pos_a[0] < pos_b[0], pos_b[0] < pos_a[0]
    # la condición de cada probabilidad manda sobre las palabras pegadas al número ('detener con probabilidad 0,01
    # cuando funciona normalmente' es α aunque la otra diga 'con un 95% de seguridad')
    def _nula(n):
        ini, fin = _clausula(t, n.ini)
        return _hay(r"(funciona (bien|normalmente|correctamente)|condiciones normales|bajo control|anda bien|"
                    r"si no (hay|se (logra|obtiene|produce))|no (mejora|reduce|aumenta|cambia)\b|cumple)", t.norm[ini:fin])
    if _nula(n1) != _nula(n2):
        es_a1, es_a2 = _nula(n1), _nula(n2)
    if es_a2 and not es_a1:
        (i1, n1), (i2, n2) = (i2, n2), (i1, n1)
    t.usar(i1)
    t.usar(i2)
    v1, v2 = n1.fraccion, n2.fraccion
    return round(v1 if v1 <= 0.5 else 1 - v1, 10), round(v2 if v2 <= 0.5 else 1 - v2, 10)


RE_COND_CONTROL = re.compile(
    r"(?:media|promedio|parametro|rendimiento)[^0-9;]{0,40}?(\d+(?:[.,]\d+)?)[^;]{0,60}?\b(no )?deten[a-z]*"
    r"[^0-9;]{0,50}?probabilidad (?:de |del )?(\d+(?:[.,]\d+)?\s*%?)")


_DIR = (r"(inferior|superior|menor|mayor|supera|exced|no mas|como maximo|como minimo|mas de|menos de|"
        r"maxim[oa]|minim[oa])")
# relleno sin cortar oración ("4.6kg" no es un punto final)
_NP = r"(?:[^.;]|\.(?=\d))"
# 'promedio ... inferior a 1,5 y desvío inferior a 0,09' / 'promedio máximo de 1,5 con un desvío máximo de 0,015'
_Y = r"(?:\by\b|\bcon una?\b)"
RE_DOBLE = re.compile(
    r"(promedio|media)" + _NP + r"{0,60}?" + _DIR +
    _NP + r"{0,50}?" + _Y + _NP + r"{0,30}?(desvio|desviacion|varianza|variabilidad)" + _NP + r"{0,40}?" + _DIR +
    r"|(desvio|desviacion|varianza|variabilidad)" + _NP + r"{0,60}?" + _DIR +
    _NP + r"{0,50}?" + _Y + _NP + r"{0,30}?(promedio|media)" + _NP + r"{0,40}?" + _DIR)


def _cola_de(palabra: str) -> str:
    """Hacia dónde apunta H1 según cómo se expresa la condición buscada ('inferior a' → izquierda).

    Una especificación ('peso máximo de 1,5') se controla al revés: H0 = cumple (≤), H1 = la excede."""
    if re.match(r"maxim", palabra):
        return "derecha"
    if re.match(r"minim", palabra):
        return "izquierda"
    return "izquierda" if re.match(r"(inferior|menor|no mas|como maximo|menos)", palabra) else "derecha"


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
    # cada condición tiene su propia dirección ('media MAYOR a 4,6 y desvío MENOR a 0,55')
    g = m.groups()
    dir_mu, dir_sigma = (g[1], g[3]) if g[0] else (g[7], g[5])
    an.datos["tail_mu"], an.datos["tail_sigma"] = _cola_de(dir_mu), _cola_de(dir_sigma)
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
    for k in ("tail_mu", "tail_sigma"):
        if d.get(k) in giro:
            d[k] = giro[d[k]]
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
    t.probs_diseno = probs[:2]
    if len(probs) == 1 and _hay(r"equilibrio", t.norm):
        # 'el equilibrio económico es para un 2,5%': en el punto de equilibrio da lo mismo decidir una cosa u otra,
        # así que la cátedra toma β = 0,50 para ese valor alternativo
        i, n = probs[0]
        t.usar(i)
        a_ = round(n.fraccion if n.fraccion <= 0.5 else 1 - n.fraccion, 10)
        an.datos["alpha"], an.datos["beta"] = a_, 0.5
        an.evidencias = [e for e in an.evidencias if e.clave not in ("alpha", "beta")]
        an.evidencias.append(Evidencia("alpha", a_, t.fragmento(n), "probabilidad de equivocarse si H0 es cierta → α"))
        an.evidencias.append(Evidencia("beta", 0.5, "equilibrio", "en el punto de equilibrio económico se acepta "
                                                                  "β = 0,50 (indiferencia entre las dos decisiones)"))
        return True
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


# Cortes entre las condiciones de un diseño: 'si ..., probabilidad 0,95; pero si ..., 0,01'
RE_CORTE_COND = re.compile(r"[.;:?!]\s|\bpero\b|\ben cambio\b|\bmientras\b|\ba su vez\b|\by (en |un |una )?(?=\d)|"
                           r",\s*y (que )?(?=(si|cuando)\b)|"
                           r"\d°\s*-|\balternativa \d")
# Acciones que se toman según la decisión (la de rechazar H0 se deduce de la condición de α)
RE_ACCION = re.compile(r"\b(no )?(poner en el mercado|lanzar|recomendar|adopt[a-z]*|cambi[a-z]*|concret[a-z]*|"
                       r"implement[a-z]*|compr(?:ar|a|e|en|ara|ase)\b|explotar|deten[a-z]*|revis[a-z]*|rechaz[a-z]*|"
                       r"rechac[a-z]*|modific[a-z]*|invertir|efectu[a-z]*|realiz[a-z]*|hacer|continuar|contratar|"
                       r"recibir de vuelta|devolv[a-z]*|devuel[a-z]*|"
                       r"acept(?:ar|a|e|en|ara|ado|ada|ados|adas|o)\b)")
# Condición de H0 (todo sigue igual / el lote es bueno) y de H1 (el valor alternativo / el lote es malo)
RE_LADO_H0 = (r"(\bno (hubiera|hay|habia|se (ha )?(obtuviera|obtiene|obtuvo|consigue|consiguiera|conseguido|modifica|"
              r"modificara|logra|lograra|produce)|bajara|baja|bajo|aumento|aumentara|aumenta|disminuye|disminuyera|"
              r"cambia|mejora|supera)|resultado alguno|condiciones normales|bajo control|funciona (bien|normalmente)|"
              r"partidas? buenas?|lotes? buenos?|unidades buenas|es cierta|anda bien|bien ajustad|sin cambio|\baql\b|"
              r"riesgo del proveedor|exced[a-z]*)")
RE_LADO_H1 = (r"(\bmal[oa]s?\b|\bltpd\b|riesgo del (comprador|consumidor)|equilibrio|\bsi (se logra|lograra|bajara|baja|"
              r"subiera|sube|aumentara|aumenta|disminuyera|disminuye|hay un|hubiera un|se incrementa|se incrementara|"
              r"se reduce|se redujera)|en caso de que[^;]{0,40}\d+(,\d+)?\s*%?\s*(superior|inferior|mayor|menor)|"
              r"detectar que)")


def _clausula(t: Texto, pos: int) -> Tuple[int, int]:
    ini, fin = 0, len(t.norm)
    for m in RE_CORTE_COND.finditer(t.norm):
        if m.end() <= pos:
            ini = m.end()
        elif m.start() > pos:
            fin = m.start()
            break
    return ini, fin


def _accion_positiva(t: Texto, n: Numero, ini: int, fin: int) -> Optional[bool]:
    """¿La probabilidad es la de HACER la acción (True) o la de no hacerla / aceptar (False)?
    Primero mira lo que sigue al número ('0,90 de cambiar'), si no lo anterior ('detener ... con un riesgo del 1%')."""
    despues = t.norm[n.fin:fin]
    m = RE_ACCION.search(despues[:45]) if re.match(r"^\s*(la probabilidad )?(de|que|la)\b", despues) else None
    if m is None:
        antes = t.norm[ini:n.ini]
        # 'acepta un riesgo del 5%' / 'admite' no es la acción de la decisión
        ms = [x for x in RE_ACCION.finditer(antes)
              if not re.match(r"\s+(un|el|como)\s+(riesgo|maximo)", antes[x.end():])]
        m = ms[-1] if ms else None
    if m is None:
        return None
    negada, verbo = bool(m.group(1)), m.group(2)
    return negada == verbo.startswith("acept")


def _lado_condicion(t: Texto, n: Numero, ini: int, fin: int, ref: Optional[float], alt: Optional[float]) -> Optional[str]:
    txt = t.norm[ini:fin]
    valores = [x.fraccion if ref is not None and ref < 1 and x.pct else x.valor
               for x in t.nums if ini <= x.ini < fin and x is not n]
    h0 = _hay(RE_LADO_H0, txt) or (ref is not None and any(abs(v - ref) < 1e-9 for v in valores))
    h1 = _hay(RE_LADO_H1, txt) or (alt is not None and any(abs(v - alt) < 1e-9 for v in valores))
    if h0 and not h1:
        return "alpha"
    if h1 and not h0:
        return "beta"
    return None


def reasignar_alpha_beta(an: Analisis, t: Texto) -> bool:
    """Diseño con dos condiciones: cuál probabilidad es α y cuál β según la CONDICIÓN de cada una (no el orden).

    - α va con la condición de H0 (el valor de referencia, 'si no hubiera disminución', 'partidas buenas').
    - β va con la del valor alternativo ('si bajara al 4%', 'partidas malas', 'un 10% superior').
    - Cada probabilidad puede estar dada como la de equivocarse o la de acertar: si la condición de α nombra una
      acción ('cambiar', 'detener', 'concretar'), esa acción con probabilidad chica es la que se toma al rechazar H0;
      entonces en la condición de β la probabilidad de esa misma acción es la potencia (β = 1 - p). Si no hay
      acciones, una probabilidad mayor que 0,5 es la de acertar."""
    probs = getattr(t, "probs_diseno", [])
    if len(probs) != 2:
        return False
    ref = an.datos.get("mu0", an.datos.get("p0"))
    alt = an.datos.get("mu1", an.datos.get("p1"))
    lados = []
    for _, n in probs:
        ini, fin = _clausula(t, n.ini)
        lados.append((_lado_condicion(t, n, ini, fin, ref, alt), n, ini, fin))
    (l1, n1, i1, f1), (l2, n2, i2, f2) = lados
    if l1 == l2 or (l1 is None and l2 is None):
        return False
    if l1 == "beta" or l2 == "alpha":
        (l1, n1, i1, f1), (l2, n2, i2, f2) = (l2, n2, i2, f2), (l1, n1, i1, f1)
    x, y = n1.fraccion, n2.fraccion
    alpha = x if x <= 0.5 else 1 - x
    acc_a, acc_b = _accion_positiva(t, n1, i1, f1), _accion_positiva(t, n2, i2, f2)
    if acc_a is not None and acc_b is not None:
        rechazo = acc_a if x <= 0.5 else not acc_a     # qué acción corresponde a rechazar H0
        beta = 1 - y if acc_b == rechazo else y
        motivo_b = ("es la probabilidad de la misma acción que rechaza H0 → potencia, β = 1 - p" if acc_b == rechazo
                    else "es la probabilidad de no tomar la acción que rechaza H0 → β")
    else:
        beta = y if y <= 0.5 else 1 - y
        motivo_b = "probabilidad de equivocarse con el valor alternativo → β" if y <= 0.5 else \
            "probabilidad de acertar con el valor alternativo (potencia) → β = 1 - p"
    an.datos["alpha"], an.datos["beta"] = round(alpha, 10), round(beta, 10)
    an.evidencias = [e for e in an.evidencias if e.clave not in ("alpha", "beta")]
    an.evidencias.append(Evidencia("alpha", an.datos["alpha"], t.texto[i1:f1].strip(),
                                   "condición de H0 (valor de referencia): probabilidad de equivocarse → α"))
    an.evidencias.append(Evidencia("beta", an.datos["beta"], t.texto[i2:f2].strip(), "condición del valor alternativo: " + motivo_b))
    return True


def extraer_p_diseno(an: Analisis, t: Texto):
    """p₀ y p₁ de un diseño (plan de muestreo): el primer porcentaje es el de referencia y el alternativo es el que
    'baja al 4%', 'aumenta 2 puntos', 'partidas malas ... del 16%', 'equilibrio para un 2,5%'."""
    for i, n in t.libres():
        a, d = t.antes(n, 60), t.despues(n, 40)
        ora = t.oracion(n.ini)
        puntos = _hay(r"^\s*puntos?\b", d)
        if not (n.pct or puntos):
            continue
        if _hay(r"(probabilidad|riesgo|confianza|seguridad|significacion)" + _R + r"{0,20}$", a):
            continue
        p0 = an.datos.get("p0")
        if puntos and p0 is not None:
            signo = -1 if _hay(r"(disminu|reduc|baj)", a[-40:]) else 1
            t.usar(i)
            _set(an, "p1", round(p0 + signo * n.valor / 100, 10), t, n,
                 f"valor alternativo: {'+' if signo > 0 else '−'}{fmt(n.valor)} puntos porcentuales sobre p₀ (p₁)")
            continue
        if not n.pct:
            continue
        alternativo = _hay(r"(baj|sub|disminu|reduc|aument|increment|pas)[a-z]*( [a-z]+){0,3} (al|a|hasta)\s*$", a) or \
            _hay(r"(mal[oa]s|ltpd|equilibrio|riesgo del (comprador|consumidor))", ora)
        if alternativo and p0 is not None and "p1" not in an.datos:
            t.usar(i)
            _set(an, "p1", n.fraccion, t, n, "valor alternativo de la proporción (p₁)")
        elif p0 is None and not alternativo:
            t.usar(i)
            _set(an, "p0", n.fraccion, t, n, "proporción de referencia / actual (p₀)")


# ---------------------------------------------------------------------------
# Qué pide cada inciso (explicación en castellano)
# ---------------------------------------------------------------------------

PARAM = {"media": "la media poblacional μ", "varianza": "la varianza σ² / el desvío σ",
         "proporcion": "la proporción poblacional p", "dos_varianzas": "la relación de varianzas σ₁²/σ₂²",
         "dos_medias": "la diferencia de medias δ = μ₁ - μ₂"}


def explicar(inc: Inciso, an: Analisis) -> str:
    tema, p, d = inc.params.get("tema", an.tema), inc.params, an.datos
    alpha = p.get("alpha", d.get("alpha"))
    par = PARAM.get(tema, "el parámetro")
    if p.get("ambos") and inc.tipo == "ic":
        conf = f" con un {fmt((1 - alpha) * 100)}% de confianza" if alpha else ""
        return (f"Estimar LOS DOS parámetros{conf}: la media μ (σ desconocido → t de Student, ν = n-1) y el desvío σ "
                f"(χ² con ν = n-1, intervalo no simétrico).")
    if p.get("ambos") and inc.tipo == "ensayo":
        signo = {"derecha": ">", "izquierda": "<", "bilateral": "≠"}
        c_mu = signo.get(d.get("tail_mu") or p.get("tail"), "?")
        c_sigma = signo.get(d.get("tail_sigma") or p.get("tail"), "?")
        cola = (f"con H1: μ {c_mu} μ₀ y H1: σ {c_sigma} σ₀" if c_mu != c_sigma else f"ambos con H1 '{c_mu}'")
        return (f"Doble condición: hacer DOS ensayos, uno sobre la media μ (t de Student) y otro sobre el desvío σ (χ²), "
                f"{cola}. Solo se recomienda si se rechazan las DOS hipótesis nulas.")
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


RE_PROP_INCISO = (r"(porcentaje|proporcion|fraccion) de [a-z ]{0,30}(mal[oa]s|defectuos|fallad|con defectos?|"
                  r"buen[oa]s|sin defectos?|rechazad)")


def tema_de_inciso(norm: str, an: Analisis) -> str:
    """Un inciso puede preguntar por otro parámetro que el del planteo:
    - en un problema de media, 'estimar el porcentaje de piezas malas' es una proporción;
    - en una doble condición (media y desvío), un inciso que solo habla del promedio es de la media."""
    if an.tema in ("media", "varianza") and _hay(RE_PROP_INCISO, norm):
        return "proporcion"
    if an.tema == "varianza" and an.datos.get("doble") and _hay(r"(promedio|\bmedia\b)", norm) \
            and not _hay(r"(desvio|desviacion|varianza|variabilidad)", norm):
        return "media"
    return an.tema


def _tabla_de_conteos(tablas) -> bool:
    """Tabla de contingencia: >= 2 filas con nombre (texto) y >= 2 columnas de conteos enteros."""
    for tb in tablas or []:
        filas = tb.get("filas") or []
        if len(filas) < 2 or not all(f and isinstance(f[0], str) for f in filas):
            continue
        celdas = [c for f in filas for c in f[1:]]
        if len(filas[0]) >= 3 and celdas and all(isinstance(c, (int, float)) and float(c).is_integer() and c >= 0
                                                 for c in celdas):
            return True
    return False


def _tabla_de_variables(tablas, xy: bool = False) -> bool:
    """Alguna tabla con >= 2 columnas numéricas de >= 4 filas que no sea de frecuencias por clase.
    Con xy=True, además los encabezados tienen que nombrar las variables como Y, X1, X2..."""
    from .tablas import columnas_numericas, es_tabla_de_clases
    for tb in tablas or []:
        if es_tabla_de_clases(tb):
            continue
        nombres, cols = columnas_numericas(tb)
        nombres = [normalizar(n) for n in nombres]
        if any(re.search(r"(frecuencia|cantidad de (dias|veces|ocurrencias)|numero de (establecimientos|veces)|ocurrencias)", n)
               for n in nombres):
            continue
        if xy and not (any(re.match(r"^y\b|.*\(y\)", n) for n in nombres) and
                       any(re.match(r"^x\s*\d*\b|.*\(x\s*\d*\)", n) for n in nombres)):
            continue
        if len(cols) >= 2 and len(cols[0]) >= 4:
            return True
    return False


RE_ALTERNATIVA = re.compile(r"\balternativa\s*(\d|[ivx]+)\s*[:.)-]", re.IGNORECASE)


def separar_alternativas(an: Analisis):
    """'Alternativa 1: ... Alternativa 2: ...' (dos gerencias con criterios distintos): cada alternativa es un
    diseño propio (su H0, α, β y μ₁). Se analiza cada una por separado con el texto común y el inciso se
    resuelve para todas (params['alternativas'])."""
    marcas = list(RE_ALTERNATIVA.finditer(an.planteo))
    if len(marcas) < 2:
        return
    prefijo = an.planteo[:marcas[0].start()]
    segmentos = [an.planteo[m.end():(marcas[k + 1].start() if k + 1 < len(marcas) else len(an.planteo))]
                 for k, m in enumerate(marcas)]
    # lo que sigue a la última alternativa y no fija probabilidades es común ('Se sabe que el desvío es 5,5 hs')
    ult = segmentos[-1]
    partes = oraciones(ult)
    sufijo = ""
    if len(partes) > 1:
        corte = next((k for k in range(1, len(partes))
                      if not _hay(r"(probabilidad|riesgo)", normalizar(ult[partes[k][0]:partes[k][1]]))), None)
        if corte is not None:
            sufijo = ult[partes[corte][0]:]
            segmentos[-1] = ult[:partes[corte][0]]
    for inc in an.incisos:
        if inc.tipo not in ("diseno", "ensayo", "n", "beta", "curva"):
            continue
        alternativas = []
        for k, seg in enumerate(segmentos):
            sub = analizar(f"{prefijo} {seg} {sufijo}", [(inc.letra, inc.texto)], _en_alternativa=True)
            if not sub.incisos or sub.tema != an.tema:
                return
            params = {k2: v for k2, v in sub.datos.items() if not isinstance(v, list)}
            params.update(sub.incisos[0].params)
            params["_nombre"] = f"Alternativa {marcas[k].group(1)}"
            params["_criterio"] = sub.criterio
            alternativas.append(params)
            inc.tipo = sub.incisos[0].tipo
        inc.params["alternativas"] = alternativas
        inc.razones.append(f"El planteo da {len(alternativas)} alternativas con condiciones propias: se resuelve cada una.")


# ---------------------------------------------------------------------------
# Reescritura previa de frecuencias ('25 por cada mil', '1 de cada 50 veces', '3‰', '5 por ciento')
# ---------------------------------------------------------------------------

_DENOM_PALABRA = {"diez": 10, "cien": 100, "mil": 1000, "diez mil": 10000, "cien mil": 100000}
_NUMERADOR_PALABRA = {"un": 1, "una": 1, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6,
                      "siete": 7, "ocho": 8, "nueve": 9, "diez": 10}
# lo que sigue al denominador y lo convierte en una tasa por unidad de medida, no en una proporción
_UNIDAD_TASA = (r"(g|gr|grs|gramos?|kg|kilos?|kilogramos?|mg|l|lts?|litros?|ml|cc|cm3|m|metros?|km|kilometros?|cm|mm|"
                r"pesos|dolares|\$|u\$s|usd|horas?|hs|minutos?|min|segundos?|seg|dias?|anos?|meses|semanas?|"
                r"kwh|toneladas?|tn|m2|m3|hectareas?|ha)\b")
_RE_CADA = re.compile(
    r"(?<![\w.,])(\d+(?:,\d+)?|una?|uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)\s+"
    r"((?:[a-zñ]+\s+){0,3}?)"
    r"(de\s+cada|por\s+cada|cada|por)\s+"
    r"(\d{1,3}(?:\.\d{3})+|\d+|diez mil|cien mil|diez|cien|mil)(?!\w|[.,]\d|\s*%)")


# Números escritos con palabras ('diez latas', 'treinta y cinco', 'noventa por ciento', 'cinco y medio por ciento')
_UNIDADES_P = {"cero": 0, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9}
_ESPECIALES_P = {"diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciseis": 16,
                 "diecisiete": 17, "dieciocho": 18, "diecinueve": 19, "veinte": 20, "veintiun": 21, "veintiuno": 21,
                 "veintiuna": 21, "veintidos": 22, "veintitres": 23, "veinticuatro": 24, "veinticinco": 25,
                 "veintiseis": 26, "veintisiete": 27, "veintiocho": 28, "veintinueve": 29}
_DECENAS_P = {"treinta": 30, "cuarenta": 40, "cincuenta": 50, "sesenta": 60, "setenta": 70, "ochenta": 80,
              "noventa": 90}
_CENTENAS_P = {"cien": 100, "ciento": 100, "doscientos": 200, "doscientas": 200, "trescientos": 300,
               "trescientas": 300, "cuatrocientos": 400, "cuatrocientas": 400, "quinientos": 500, "quinientas": 500,
               "seiscientos": 600, "seiscientas": 600, "setecientos": 700, "setecientas": 700, "ochocientos": 800,
               "ochocientas": 800, "novecientos": 900, "novecientas": 900}
_W = lambda d: "|".join(sorted(d, key=len, reverse=True))   # noqa: E731
_RE_MENOR_100 = (r"(?:(?:" + _W(_DECENAS_P) + r")(?:\s+y\s+(?:" + _W(_UNIDADES_P) + r"|un|uno|una))?|"
                 r"(?:" + _W(_ESPECIALES_P) + r")|(?:" + _W(_UNIDADES_P) + r"))")
_RE_NUM_PALABRAS = re.compile(
    r"(?<![\w.,])("
    r"(?:(?:" + _W(_CENTENAS_P) + r")(?:\s+" + _RE_MENOR_100 + r")?(?:\s+mil(?:\s+(?:(?:" + _W(_CENTENAS_P) + r")(?:\s+"
    + _RE_MENOR_100 + r")?|" + _RE_MENOR_100 + r"))?)?)|"
    r"(?:" + _RE_MENOR_100 + r"(?:\s+mil(?:\s+(?:(?:" + _W(_CENTENAS_P) + r")(?:\s+" + _RE_MENOR_100 + r")?|"
    + _RE_MENOR_100 + r"))?)?)|"
    r"(?:un|uno|una)(?=\s+(?:y\s+medio\s+)?(?:por\s+ciento|puntos?\s+porcentual))"
    r")(\s+y\s+medio)?(?=\s+por\s+ciento\b|(?![\w]))")
# 'las dos máquinas', 'dos alternativas', 'tres turnos': cuentan grupos o categorías, no son datos (y otras reglas
# los leen con la palabra: 'dos (máquinas|procesos)...')
_GRUPOS_P = (r"(muestras?|maquinas|tornos|grupos|procesos|metodos|poblaciones|variedades|marcas|tratamientos|"
             r"alternativas|criterios|condiciones|colas|incisos|turnos|plantas|zonas|localidades|categorias|"
             r"establecimientos|raciones|equipos|aleaciones|formulas|areas|enconadoras|proveedores|lineas|"
             r"sucursales|tipos|clases|variables|parametros|productos|componentes|opciones|caras|partes|veces|"
             r"modelos|hipotesis|ensayos de|errores|riesgos|probabilidades|valores)\b")


def _valor_palabras(txt: str) -> Optional[float]:
    total, actual = 0, 0
    for w in re.findall(r"[a-z]+", txt):
        if w == "y":
            continue
        if w == "mil":
            total += (actual or 1) * 1000
            actual = 0
        elif w in ("un", "uno", "una"):
            actual += 1
        else:
            v = _UNIDADES_P.get(w, _ESPECIALES_P.get(w, _DECENAS_P.get(w, _CENTENAS_P.get(w))))
            if v is None:
                return None
            actual += v
    return float(total + actual)


def reescribir_numeros_palabras(texto: str) -> Tuple[str, List[str]]:
    """'se pesaron diez latas' → '10 latas'; 'el noventa por ciento' → '90%'; 'cinco y medio por ciento' → '5,5%'.

    No toca los artículos ('un', 'una') salvo en 'uno por ciento', ni las palabras que cuentan grupos o categorías
    ('las dos máquinas', 'tres turnos'), que otras reglas leen así."""
    notas = []
    # 'medio litro', 'medio punto' → 0,5 (solo pegado a una unidad: 'consumo medio' es otra cosa)
    norm = normalizar(texto)
    m_med = list(re.finditer(r"\b(un |una )?(medio|media) (litro|kilo|kilogramo|metro|gramo|punto|minuto|segundo|hora|"
                             r"quintal|centimetro|milimetro|grado|tonelada|dia|ano|mes)\b", norm))
    for m in reversed(m_med):
        notas.append(f"«{texto[m.start():m.end()]}» se leyó como 0,5 {texto[m.start(3):m.end(3)]}.")
        texto = texto[:m.start()] + "0,5 " + texto[m.start(3):]
    norm = normalizar(texto)
    partes, ult = [], 0
    for m in _RE_NUM_PALABRAS.finditer(norm):
        if m.start() < ult:
            continue
        valor = _valor_palabras(m.group(1))
        if valor is None or (valor == 0 and not norm[m.end():m.end() + 15].lstrip().startswith("por ciento")):
            continue
        if m.group(2):
            valor += 0.5
        pct = re.match(r"\s+por\s+ciento\b", norm[m.end():])
        if not pct:
            if (valor < 2 and not _hay(r"^\s+(y\s+medio\s+)?puntos?\s+porcentual", norm[m.end():m.end() + 30])) or _hay(r"^\s+(de\s+(los|las)\s+)?" + _GRUPOS_P, norm[m.end():m.end() + 40]) or \
                    _hay(r"\b(los|las|ambos|ambas|estos|estas|sus|esos|esas|cada uno de|entre)\s*$", norm[max(0, m.start() - 20):m.start()]) or \
                    _hay(r"^\s*(salio\s+|aparecio\s+)?\d", norm[m.end():m.end() + 12]):   # 'el dos 6': cara / categoría
                continue
        crudo = fmt(valor)
        reemplazo = crudo + ("%" if pct else "")
        partes.append(texto[ult:m.start()] + reemplazo)
        ult = m.end() + (pct.end() if pct else 0)
        notas.append(f"«{texto[m.start():ult].strip()}» se leyó como {reemplazo}.")
    return "".join(partes) + texto[ult:], notas


def reescribir_frecuencias(planteo: str) -> Tuple[str, List[str]]:
    """Pasa a porcentaje las frecuencias dichas 'N de cada M' / 'N por mil' / 'N ‰' / 'N por ciento', así el resto
    de las reglas las lee como cualquier '2,5%' (p₀, α, p̂...). Devuelve (texto, notas para el usuario).

    Antes pasa a cifras los números escritos con palabras ('diez latas', 'noventa por ciento')."""
    planteo, notas = reescribir_numeros_palabras(unificar_redaccion(planteo))
    norm = normalizar(planteo)
    if _cuenta(P_REGRESION, norm):
        return planteo, notas   # 'por cada 1.000 pesos que se invierten' es una pendiente, no una proporción
    partes, ult = [], 0
    for m in _RE_CADA.finditer(norm):
        num_txt, palabras, nexo, den_txt = m.group(1), m.group(2), m.group(3), m.group(4)
        cola = norm[m.end():m.end() + 25]
        if re.match(r"\s*(de\s+)?" + _UNIDAD_TASA, cola) or re.search(r"\b" + _UNIDAD_TASA, palabras):
            continue   # '5 g por cada 100 g', '3 fallas cada 100 horas': tasa, no proporción
        num = _NUMERADOR_PALABRA.get(num_txt)
        if num is None:
            if not num_txt[0].isdigit():
                continue
            num = parse_num(num_txt)
        den = _DENOM_PALABRA.get(den_txt) or parse_num(den_txt)
        if nexo.strip() == "por" and den not in (100, 1000, 10000, 100000):
            continue   # 'por' a secas solo con 'por cien / por mil' ('2 por 3' no es una frecuencia)
        if not num_txt[0].isdigit() and palabras.strip() not in ("", "vez", "veces"):
            continue   # 'una muestra de cada 100': con número en palabras, solo 'una de cada 50 (veces)'
        if _hay(r"(tom|extra|inspeccion|revis|elig|selecciona|control|muestre)[a-z]*\s*$", norm[max(0, m.start() - 25):m.start()]):
            continue   # 'se inspecciona 1 de cada 100 producidas': frecuencia de muestreo, no un parámetro
        if not den or num > den or den < 2:
            continue
        pct = num / den * 100
        reemplazo = f"un {fmt(pct, 6)}% de" + (f" {palabras.strip()}" if palabras.strip() else "")
        partes.append(planteo[ult:m.start()] + reemplazo)
        ult = m.end()
        notas.append(f"«{planteo[m.start():m.end()].strip()}» se leyó como {fmt(pct, 6)}% "
                     f"({fmt(num)}/{fmt(den)} = {fmt(num / den, 6)}).")
    texto = "".join(partes) + planteo[ult:]
    # '3‰' (por mil) y '5 por ciento'
    def _permil(m):
        v = parse_num(m.group(1)) / 10
        notas.append(f"«{m.group(0).strip()}» (por mil) se leyó como {fmt(v, 6)}%.")
        return f"{fmt(v, 6)}%"
    texto = re.sub(r"(\d+(?:,\d+)?)\s*‰", _permil, texto)
    texto = re.sub(r"(\d+(?:,\d+)?)\s+por\s+ciento\b", r"\1%", texto, flags=re.IGNORECASE)
    return texto, notas


def analizar(planteo: str, incisos: Optional[IncisosIn] = None, tablas: Optional[List[dict]] = None,
             _en_alternativa: bool = False, tema: Optional[str] = None) -> Analisis:
    """`tablas`: tablas de datos ya estructuradas (si no, se buscan en el texto).

    `tema`: si se indica (lo eligió el usuario o el asistente de IA), no se detecta: las reglas extraen los
    datos como si el problema fuera de ese tema."""
    planteo = (planteo or "").strip()
    lista: List[Tuple[str, str]] = []
    if incisos:
        for k, it in enumerate(incisos):
            if isinstance(it, (tuple, list)):
                lista.append((it[0], it[1]))
            elif str(it).strip():
                lista.append((chr(ord("a") + k), str(it).strip()))
    if not lista:
        planteo, lista = separar_incisos(planteo, parrafos=True)
    if not lista:
        # sin incisos: la pregunta está en el mismo planteo
        lista = [("única", pregunta_de(planteo))]

    original = planteo
    planteo, notas = reescribir_frecuencias(planteo)
    lista_r = []
    for letra_r, tx_r in lista:
        tx2, notas2 = reescribir_frecuencias(tx_r)
        notas += [x for x in notas2 if x not in notas]
        lista_r.append((letra_r, tx2))
    lista = lista_r

    an = Analisis(planteo=original)
    an.avisos += notas
    an.tablas = list(tablas) if tablas else buscar_tablas(planteo)
    total = planteo if lista[0][0] == "única" else planteo + " " + " ".join(tx for _, tx in lista)
    t_total = Texto(total)
    pregunta = " ".join(tx for _, tx in lista) if lista[0][0] != "única" else pregunta_de(planteo)
    if tema not in TEMAS or tema == "desconocido":
        tema = None
    if tema:
        an.tema, an.razones_tema = tema, [f"Tema indicado de antemano: {TEMAS[tema]}."]
    else:
        an.tema, an.razones_tema = detectar_tema(t_total.norm, t_total.listas, normalizar(pregunta))
    if not tema and an.tema == "media" and (_cuenta(P_REGRESION, t_total.norm) >= 1 or _tabla_de_variables(an.tablas, xy=True)) \
            and _tabla_de_variables(an.tablas):
        an.tema = "regresion"
        an.razones_tema = ["Hay una tabla con dos o más variables medidas sobre los mismos casos y el enunciado habla de "
                           "su relación: regresión / correlación."]
    if not tema and an.tema == "media" and _tabla_de_variables(an.tablas) and \
            _cuenta(P_MEDIA + [r"desvio", r"desviacion"], normalizar(planteo)) == 0 and \
            not _hay(r"\d", re.sub(r"\(?tabla\)?", "", normalizar(planteo))):
        # solo una tabla de dos o más variables numéricas (sin medias ni desvíos en el texto): regresión
        an.tema = "regresion"
        an.razones_tema = ["Los datos son una tabla de dos o más variables medidas sobre los mismos casos: "
                           "regresión / correlación."]
    if not tema and an.tema in ("media", "proporcion") and _tabla_de_conteos(an.tablas) and \
            _hay(r"(relacionad|depend|asociad|independ|difier|influ|homogene|varia)", t_total.norm):
        an.tema = "chi_contingencia"
        an.razones_tema = ["La tabla da conteos de categorías (filas con nombre, columnas de frecuencias) y se pregunta "
                           "si una variable depende de la otra: tabla de contingencia χ²."]
    if not tema and an.tema == "proporcion" and lista[0][0] != "única" and _cuenta(P_PROPORCION, normalizar(planteo)) == 0 \
            and _cuenta(P_MEDIA + P_VARIANZA + [r"desvio", r"desviacion"], normalizar(planteo)) > 0:
        # el porcentaje aparece recién en un inciso: el problema es de media / desvío y ese inciso es aparte
        t_pl = Texto(planteo)
        tema_pl, razones_pl = detectar_tema(t_pl.norm, t_pl.listas, t_pl.norm)
        if tema_pl in ("media", "varianza"):
            an.tema, an.razones_tema = tema_pl, razones_pl + [
                "El porcentaje / proporción aparece recién en un inciso: ese inciso se resuelve aparte como proporción."]
    if not tema and an.tema in ("media", "proporcion", "dos_medias", "varianza") and \
            _hay(r"(depend|asocia|independ|relacion|difier|influ|distint|homogene|varia (segun|con))", normalizar(pregunta)) \
            and tabla_porcentajes(Texto(planteo)):
        an.tema = "chi_contingencia"
        an.razones_tema = ["Da, para cada grupo, los PORCENTAJES de cada categoría y pregunta si la distribución depende "
                           "del grupo: tabla de contingencia χ² (los % se pasan a frecuencias)."]
    an.criterio, an.criterio_razon = detectar_criterio(t_total.norm)

    t = Texto(planteo)
    diseno = False
    if an.tema in ("media", "varianza", "proporcion"):
        diseno = completar_diseno(an, t)
    an._norm_cola = t.norm
    if not diseno:
        r = extraer_alpha(t)
        if r:
            _set(an, "alpha", r[0], t, r[1], r[2])
            # 'se acepta detenerla sin necesidad a lo sumo un 2% de las veces': ese 'a lo sumo' acota el RIESGO,
            # no es una especificación del parámetro (no define la cola)
            m = re.search(r"(a lo sumo|como maximo|como mucho|no mas (de|del)|hasta)\s*(un |el |del |de )?$", t.norm[:r[1].ini])
            if m:
                an._norm_cola = t.norm[:m.start()] + " " * (m.end() - m.start()) + t.norm[m.end():]

    if an.tema in ("media", "varianza", "proporcion"):
        extraer_datos_lista(an, t)
        r = extraer_error(t)
        if r:
            an.datos[r[0]] = r[1]
            an.evidencias.append(Evidencia(r[0], r[1], t.fragmento(r[2]) if r[2] else "",
                                           "error admitido" if r[0] == "e" else "reducción pedida"))
        # el número del plan dado ('se rechaza si hay 2 o más defectuosas') no es el tamaño de la muestra
        plan = extraer_plan_dado(an, t) if an.tema == "proporcion" else False
        extraer_n(an, t)
        extraer_N(an, t)
        if an.tema == "proporcion":
            if diseno:
                extraer_p_diseno(an, t)
            else:
                extraer_proporcion(an, t)
            if plan:
                riesgos_plan_dado(an, t)
            if "p0" not in an.datos:
                p0_de_referencia(an, t_total)
        else:
            extraer_desvio(an, t)
            if an.tema == "media" and an.datos.get("sigma_conocido") is False and _hay(
                    r"(desvio|desviacion)[a-z ]{0,20}(no se modificara|no se modifica|no cambia|no cambiara|se mantendra|"
                    r"se mantiene|no variara)", t.norm):
                an.datos["sigma_conocido"] = True
                for e in an.evidencias:
                    if e.clave == "desvio":
                        e.motivo = "desvío del proceso, que el enunciado dice que no cambia → σ conocido (Z)"
            if an.tema == "media":
                extraer_media(an, t, solo_mu0=diseno)
                extraer_totales(an, t)
                extraer_costos(an.datos, an, t)
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
        if diseno:
            reasignar_alpha_beta(an, t)
        if an.tema == "media" and diseno_control(an, planteo):
            diseno = True
            an.datos.setdefault("sigma_conocido", True)
        ajustar_escala(an)
        if an.tema == "varianza" and "desvio" in an.datos:
            an.datos.setdefault("sigma_conocido", False)
        doble_condicion(an, t)
    elif an.tema in ("dos_medias", "dos_varianzas"):
        posiciones = extraer_dos_muestras(an, t)
        if an.tema == "dos_varianzas":
            extraer_relacion_desvios(an, t, posiciones)
        else:
            from .dos_muestras import completar_dos_medias   # TEMA V: roles, sujeto, σ conocidos
            completar_dos_medias(an, t, posiciones)
    elif an.tema.startswith("chi"):
        extraer_chi(an, t)
    if an.tema in EXTENSIONES:
        EXTENSIONES[an.tema][0](an, t)

    lista = _expandir_idem(lista)
    previo: Dict = {}
    tema_previo = an.tema
    for letra, texto_inc in lista:
        inc = Inciso(letra=letra, texto=texto_inc)
        norm = normalizar(texto_inc)
        tema_inc = tema_de_inciso(norm, an)
        if tema_inc != an.tema:
            inc.params["tema"] = tema_inc
            inc.razones.append(f"Este inciso cambia de parámetro: se resuelve como {TEMAS[tema_inc]}.")
        if tema_inc in EXTENSIONES:
            inc.tipo, razon = EXTENSIONES[tema_inc][1](inc, an, norm)
        else:
            inc.tipo, razon = clasificar_inciso(norm, tema_inc, normalizar(planteo))
        if inc.tipo == "no_soportado" and len(norm) < 60 and lista[0][0] != "única":
            inc.tipo, razon = clasificar_inciso(normalizar(pregunta_de(planteo)), an.tema, "")
            razon = "El inciso solo agrega un dato; la pregunta está en el planteo. " + razon
        if an.tema == "media" and inc.tipo == "ensayo" and "beta" in an.datos and "xbar" not in an.datos:
            inc.tipo, razon = "diseno", "Hay dos condiciones (α y β): se diseña el ensayo."
        if inc.tipo == "no_soportado" and an.incisos and an.incisos[-1].tipo != "no_soportado" and \
                _hay(r"^\W*(y|e|o|idem|lo mismo|igual)\b", norm):
            ant = an.incisos[-1]
            inc.tipo, razon = ant.tipo, (f"Pregunta elíptica ('¿Y ...?'): repite la pregunta del inciso {ant.letra}) con "
                                         "otra condición.")
        m_ref = re.search(r"(respuesta|conclusion|decision) (a|de|para) (la pregunta|el inciso|el punto|lo pedido en)?\s*\(?([a-h])\)", norm)
        if m_ref:
            ref = next((x for x in an.incisos if x.letra == m_ref.group(4)), None)
            if ref is not None and ref.tipo != "no_soportado":
                inc.tipo, razon = ref.tipo, f"Repite la pregunta del inciso {ref.letra}) con otra condición."
                for k, v in ref.params.items():
                    if k not in ("tema",):
                        inc.params.setdefault(k, v)
        if tema_inc == "media" and inc.tipo == "ic" and "xbar" not in an.datos and not an.datos.get("datos") \
                and "mu0" in an.datos and _hay(r"(dentro de que limites|entre que (valores|limites)|limites)", norm) \
                and not _hay(r"(estimar|confianza)", norm):
            inc.tipo, razon = "diseno", ("No hay muestra que estimar: los límites entre los que variará la media son los "
                                         "LÍMITES DE CONTROL alrededor de μ₀ (valores críticos de un ensayo bilateral).")
            inc.params["tail"] = "bilateral"
        if tema_inc == "media" and inc.tipo == "beta" and \
                _hay(r"probabilidad de (tener|obtener|observar|encontrar|registrar|que (se obtenga|resulte|de))\s+"
                     r"(una|un)?[a-z ,]{0,40}(media|promedio)", norm) and not _hay(r"(detectar|desplaz|no detectar)", norm):
            inc.params["prob_xbar"] = True
            razon = ("Pide la probabilidad de OBSERVAR esa media con el proceso en su valor nominal: P(x̄ ≥ valor | μ₀) "
                     "(no es β ni potencia).")
        inc.razones.append(razon)
        extraer_params_inciso(inc, an, previo)
        # herencia: lo que no se dice en el inciso vale lo del inciso anterior (α, cola, μ₁...);
        # si el inciso es de otro parámetro, solo se hereda α
        tema_inc = inc.params.get("tema", an.tema)
        heredables = ("alpha", "tail", "mu1", "sigma1", "p1", "prob", "mu0", "sigma0", "p0", "phi1", "sobre") \
            if tema_inc == tema_previo else ("alpha",)
        for k in heredables:
            if k not in inc.params and k in previo and not (k == "tail" and inc.tipo in ("ensayo", "diseno")):
                inc.params[k] = previo[k]
        tema_previo = tema_inc
        if inc.tipo == "diseno" and "beta" not in inc.params and "beta" in an.datos:
            inc.params["beta"] = an.datos["beta"]
        inc.que_pide = razon if tema_inc in EXTENSIONES else explicar(inc, an)
        previo.update(inc.params)
        an.incisos.append(inc)

    if an.tema in ("media", "varianza", "proporcion") and not _en_alternativa:
        separar_alternativas(an)

    if an.tema == "media" and an.datos.get("sigma_conocido") is False and "xbar" not in an.datos \
            and not an.datos.get("datos") and not any(i.params.get("usar_S") for i in an.incisos):
        # sin ninguna muestra el desvío no puede ser muestral: es el del proceso (σ conocido → Z)
        an.datos["sigma_conocido"] = True
        for e in an.evidencias:
            if e.clave == "desvio":
                e.motivo = "desvío del proceso (no hay muestra de la que pueda salir S) → σ conocido (Z)"

    if "alpha" not in an.datos and not any("alpha" in i.params for i in an.incisos) :
        an.datos["alpha"] = 0.05
        an.avisos.append("No se encontró el riesgo α ni la confianza: se asume α = 0,05 (revisalo).")
    return an
