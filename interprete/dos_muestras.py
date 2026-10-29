"""TEMA V: comparación de dos medias (lectura del enunciado + resolución).

Se registra en `modelo.EXTENSIONES["dos_medias"]` (clasificación de incisos) y en `modelo.DESPACHO_EXTRA`
(ensayo, IC, n y diseño). El analizador llama a `completar_dos_medias` después de leer las muestras y a
`params_dos_medias` al final de los parámetros de cada inciso.

Convenciones de la cátedra (Guía, TEMA V):
- δ = μ(1º) - μ(2º): va primero el grupo del que se afirma algo ('con la máquina B se obtiene más que con la A',
  'el aditivo reduce...'); si el inciso no nombra a ninguno, el grupo con el cambio (nuevo, con aditivo,
  reacondicionadas, tratado, con la campaña...).
- Antes de comparar medias de muestras independientes se ensaya la igualdad de desvíos con F unilateral
  (desvío muestral mayor arriba) y riesgo 10 % (V-1, V-3, V-6 y V-21 de la guía): si no se rechaza se amalgama
  (Sa, ν = n₁+n₂-2); si se rechaza, Welch (ν de Aspin-Welch redondeado hacia abajo).
- Si se dan desvíos poblacionales σ₁, σ₂ conocidos se usa Z; si solo se 'considera' que valen eso y hay muestras,
  primero se los verifica con χ² (V-21) y si no se sostienen se trabaja con S.
- 'Supera en un 24%': H0: μ₁ ≤ 1,24·μ₂ con δ* = μ₁ - 1,24·μ₂ y σ(d*) = √(S₁²/n₁ + 1,24²·S₂²/n₂) (o con Sa).
- 'Diferencia porcentual mínima garantizada': el h tal que el ensayo de μ₁ ≤ h·μ₂ queda justo en el límite.
"""

import re
from math import sqrt
from typing import Dict, List, Optional, Tuple

from solver import two_samples as two
from solver import distributions as dist
from solver.muestra import resumen_muestra

from . import analizador as A
from . import redondeo
from .modelo import DESPACHO_EXTRA, EXTENSIONES, Analisis, Evidencia, Inciso
from .resolver import FaltaDato, Resultado, _coma, _cv, _ensayo_txt, _p, _regla, _signo
from .texto import Numero, buscar_numeros, fmt, normalizar

ALPHA_VARIANZAS = 0.10   # riesgo del test F previo (convención de la guía)

# ---------------------------------------------------------------------------
# Palabras clave
# ---------------------------------------------------------------------------

RE_REF = (r"(\bsin (el |la |los |las )?[a-z]+|\bactual(es)?\b|tradicional|\bviej[oa]s?\b|clasic[oa]|\banterior(es)?\b|"
          r"original|habitual|\bno se (le |les )?(aplico|aplica|suministr[oa]|trat[oa]|uso|uso)\b|\bantes de\b)")
RE_NUEVO_V = (r"(reacondicion|aditivo|acelerante|albumina|tratad[oa]s?\b|tratamiento|propuest|\bnuev[oa]s?\b|"
              r"modificad|modificacion|campana|inoculad|fertilizad|vacunad|capacitad|mejorad)")

P_MAS_V = (r"(\bmayor(es)?\b|superior|\bsuper[ae]|\bexced|aument|increment|\bmejor|\bmas (de|que)\b|maximiz|efectiv(?!amente)|"
           r"diferencia minima|\b(rinden?|producen?|duran?|venden?|pesan?|es|son) mas\b|\bmas\s*\??\s*$)")
P_MENOS_V = r"(\bmenor(es)?\b|inferior|disminu|\breduc|\bmenos (de|que)\b|minimiz|\bbaj[ae]n?\b|ahorr|acort)"
P_BILATERAL_V = (r"(difier|diferente|distint|diferencias? (significativ|en (la|el|los|las))|sin diferencias|influ|"
                 r"\bigual(es)?\b|\bmism[oa] [a-z ]{0,25}(promedio|media|medio|volumen|rendimiento|produccion|duracion)|"
                 r"se modific|(cambio|cambia) (la|el) (media|promedio))")


def _hay(p, s) -> bool:
    return re.search(p, s) is not None


def _cuenta(p, s) -> int:
    return len(re.findall(p, s))


# ---------------------------------------------------------------------------
# Análisis del planteo: roles (nuevo / referencia), σ conocidos
# ---------------------------------------------------------------------------

def _rol_texto(s: str) -> Optional[str]:
    if _hay(RE_REF, s):
        return "ref"
    if _hay(RE_NUEVO_V, s):
        return "nuevo"
    return None


def _ventana_muestra(t, n: Numero) -> str:
    """Lo que describe a la muestra que empieza en n: hasta el próximo número (o fin de oración)."""
    resto = t.norm[n.fin:n.fin + 160]
    m = re.search(r"\d|[.;]\s", resto)
    return resto[:m.start()] if m else resto


def _previo(t, n: Numero, k: int = 70) -> str:
    """Lo anterior al número dentro de la misma oración (corta en '.' o ';', no en ':')."""
    s = t.norm[max(0, n.ini - k):n.ini]
    m = list(re.finditer(r"[.;?!]\s", s))
    return s[m[-1].end():] if m else s


def _nombres_por_etiqueta(an: Analisis, t, posiciones: Dict[str, Numero]):
    """'Horno “A”: 40 hornadas, media 1,50' / 'Híbrido viejo: promedio de 30' → nombres de las muestras."""
    if not all(re.fullmatch(r"Muestra \d", an.datos.get(f"nombre{j}") or "Muestra 1") for j in (1, 2)):
        return
    nombres = []
    for j in (1, 2):
        n = posiciones.get(f"xbar{j}") or posiciones.get(f"n{j}")
        if n is None:
            return
        s = t.texto[max(0, n.ini - 90):n.ini]
        s = re.split(r"[.;?!]\s", s)[-1]
        etqs = re.findall(r"([^:;.,\d]{2,40}?)\s*:\s*(?=[^:]*$)", s)
        if not etqs:
            return
        nom = etqs[-1].strip(" ,()")
        if not nom or re.search(r"\d", nom):
            return
        nombres.append(nom)
    if nombres[0] != nombres[1]:
        an.datos["nombre1"], an.datos["nombre2"] = nombres
        an.evidencias.append(Evidencia("nombre1", nombres[0], "", "rótulo de la muestra 1 en el texto"))


def completar_dos_medias(an: Analisis, t, posiciones: Dict[str, Numero]):
    """Roles de las muestras, nombres, 'sujeto' por defecto y desvíos poblacionales σ₁, σ₂."""
    _nombres_por_etiqueta(an, t, posiciones)
    roles = {}
    mismo_n = posiciones.get("n1") is not None and posiciones.get("n1") is posiciones.get("n2")
    for j in (1, 2):
        rol = _rol_texto(normalizar(an.datos.get(f"nombre{j}") or ""))
        for clave in (("xbar",) if mismo_n else ("n", "xbar")):
            n = posiciones.get(f"{clave}{j}")
            if rol is None and n is not None:
                rol = _rol_texto(_ventana_muestra(t, n)) or _rol_texto(_previo(t, n))
        roles[j] = rol
    if roles[1] == roles[2]:
        roles = {1: None, 2: None} if roles[1] == "ref" or roles[1] is None else roles
        if roles[1] == "nuevo":   # las dos 'nuevas': no sirve
            roles = {1: None, 2: None}
    nuevo = 1 if roles[1] == "nuevo" or roles[2] == "ref" else 2 if roles[2] == "nuevo" or roles[1] == "ref" else None
    por_defecto = all(re.fullmatch(r"Muestra \d", an.datos.get(f"nombre{j}") or "Muestra 1") for j in (1, 2))
    if nuevo and por_defecto:
        # el cambio más específico que nombre el texto (aditivo antes que 'nuevo')
        grupos = [g for g in A.GRUPOS_CAMBIO if not g[0].startswith(r"\bnuev")] + \
            [(r"campana", "con la campaña", "sin la campaña"), (r"plaguicida|fertilizante|producto", "nuevo producto",
                                                                "producto tradicional")] + \
            [g for g in A.GRUPOS_CAMBIO if g[0].startswith(r"\bnuev")]
        etq = next(((nv, rf) for p, nv, rf in grupos if re.search(p, t.norm)), None)
        if etq and etq[1] == "actual":
            m_ref = re.search(r"\b(viej[oa]|anterior|tradicional|habitual|original)\b", t.norm)
            if m_ref:   # 'la máquina vieja': se la nombra como el texto
                etq = (etq[0], m_ref.group(1))
        if etq:
            an.datos[f"nombre{nuevo}"], an.datos[f"nombre{3 - nuevo}"] = etq
    if nuevo:
        an.datos["sujeto"] = nuevo
        an.razones_tema.append(f"δ = μ({an.datos.get(f'nombre{nuevo}')}) - μ({an.datos.get(f'nombre{3 - nuevo}')}): "
                               "primero el grupo con el cambio (salvo que el inciso afirme algo del otro).")
    _sigmas_conocidos(an, t)


def _sigmas_conocidos(an: Analisis, t):
    """'con desviaciones estándares de σA = 0,015 y σB = 0,018' / 'desvíos poblacionales de 3 y 4'."""
    pares = []
    for m in re.finditer(r"σ\s*([a-z0-9]{0,3})\s*=\s*", t.norm):
        n = next((x for x in t.nums if x.ini >= m.end() and x.ini - m.end() <= 2), None)
        if n is not None:
            pares.append((m.group(1), n))
    if len(pares) < 2:
        m = re.search(r"(desvios?|desviaciones?)( estandar(es)?)? poblacional(es)?[^0-9.;]{0,30}", t.norm)
        if m:
            nums = [x for x in t.nums if x.ini >= m.end() and x.ini - m.end() <= 40 and not x.pct][:2]
            if len(nums) == 2:
                pares = [("", nums[0]), ("", nums[1])]
    if len(pares) < 2:
        return
    asignados = {}
    for sub, n in pares[:2]:
        j = None
        if sub in ("1", "2"):
            j = int(sub)
        elif sub:
            for k in (1, 2):
                nom = normalizar(an.datos.get(f"nombre{k}") or "")
                if re.search(r"([“\"(]|\b(maquina|variedad|marca|proceso|metodo|grupo|tipo)\s+)" + re.escape(sub) +
                             r"([”\")]|\b)", nom):
                    j = k
        if j is None or j in asignados:
            j = 1 if 1 not in asignados else 2
        asignados[j] = n
    ora = t.oracion(pares[0][1].ini)
    afirmado = _hay(r"(considera|supone|cree|estima|afirma|sostiene|asegura|dice)", ora)
    for j, n in asignados.items():
        an.datos[f"sigma_pob{j}"] = n.valor
        an.evidencias.append(Evidencia(f"sigma_pob{j}", n.valor, t.fragmento(n),
                                       f"desvío poblacional σ de la muestra {j}" +
                                       (" (afirmado: se verifica con las muestras)" if afirmado else " (conocido)")))
        for e in list(an.evidencias):   # el σ no es el desvío muestral S
            if e.clave == f"s{j}" and an.datos.get(f"s{j}") == n.valor:
                an.datos.pop(f"s{j}", None)
                an.evidencias.remove(e)
    an.datos["sigma_afirmado"] = afirmado


# ---------------------------------------------------------------------------
# Incisos: tipo, sujeto, dirección, δ₀ / h
# ---------------------------------------------------------------------------

def clasificar_dos_medias(inc: Inciso, an: Analisis, norm: str) -> Tuple[str, str]:
    tipo, razon = A.clasificar_inciso(norm, "dos_medias", normalizar(an.planteo))
    if _hay(r"probabilidad de (que se haya|haberse|haber) equivocad|probabilidad de (haber cometido un )?error", norm) \
            and _hay(r"rechaz", norm):
        return "ensayo", ("Pide la probabilidad de haberse equivocado al rechazar H0: es el valor a posteriori α* "
                          "del ensayo.")
    if tipo in ("ic", "beta", "no_soportado") and re.match(
            r"^\W*(aseguraria|se puede asegurar|puede asegurar|se puede afirmar|puede afirmar|es posible (asegurar|afirmar)|"
            r"existe (alguna )?razon|hay (alguna )?razon|se considera|considera|hay (diferencia|evidencia)|"
            r"existen? diferencias?|difieren|son (diferentes|distint)|(esta|estan) en lo (cierto|correcto)|tiene razon)",
            norm):
        return "ensayo", "Pide decidir si se puede asegurar una afirmación: ensayo de hipótesis."
    if tipo == "beta":
        nums = [n for n in buscar_numeros(inc.texto) if not n.pct]
        if nums:
            inc.params["delta1"] = nums[-1].valor
        inc.params["prob"] = "potencia" if _hay(r"(detectar|rechazar|asegurar|potencia|adoptar|elegir)", norm) and             not _hay(r"no (detectar|rechazar|asegurar)", norm) else "beta"
        return "beta", ("Probabilidad de error / potencia para una diferencia real δ₁: β = P(no rechazar H0 | δ = δ₁) con "
                        "el valor crítico del ensayo y el mismo error estándar.")
    return tipo, razon


_SIN = r"\bsin (el |la |los |las )?"
_GENERICAS = {"muestra", "grupo", "datos", "humana", "humano"}


def _raiz(w: str) -> str:
    return w[:max(4, len(w) - 3)]


def _palabras(nom: str) -> List[str]:
    sin_citas = re.sub(r"[“\"(][^”\")]*[”\")]", " ", nom)
    return [w for w in re.findall(r"[a-z]{4,}", sin_citas) if w not in _GENERICAS]


def _claves_grupo(nombre: str, otro: str) -> List[Tuple[str, bool]]:
    """Patrones que nombran a un grupo en el texto: “A”, (A), 'variedad A', palabras propias del nombre.

    Devuelve (patrón, excluir_si_va_precedido_de_'sin'): 'Zapato tratado' no se nombra en 'sin tratar'."""
    nom, ot = normalizar(nombre or ""), normalizar(otro or "")
    pats: List[Tuple[str, bool]] = []
    for m in re.finditer(r"[“\"(]([a-z0-9 ]{1,25})[”\")]", nom):
        x = re.escape(m.group(1).strip())
        if len(m.group(1).strip()) <= 3:
            pats.append((r"[“\"(]" + x + r"[”\")]", False))
            pats.append((r"\b(maquina|variedad|racion|marca|proceso|metodo|establecimiento|tipo|grupo|aleacion|"
                         r"formula|torno|producto|tratamiento)s?\s+[“\"]?" + x + r"\b", False))
        else:
            pats.append((re.escape(m.group(1).strip()), False))
    m = re.fullmatch(r"\s*([a-z]{4,})\s+([a-z0-9]{1,3})\s*", nom)
    if m:   # 'marca B', 'máquina 2': la palabra genérica seguida de la letra
        pats.append((r"\b" + m.group(1) + r"s?\s+[“\"]?" + re.escape(m.group(2)) + r"\b", False))
    mias, otras = _palabras(nom), _palabras(ot)
    raices_otras = {_raiz(w) for w in otras}
    con_sin, otro_sin = _hay(r"\bsin\b", nom), _hay(r"\bsin\b", ot)
    for w in mias:
        r = re.escape(_raiz(w)) + r"[a-z]*"
        if con_sin:
            pats.append((_SIN + r"\b" + r, False))
        elif _raiz(w) not in raices_otras:
            pats.append((r"\b" + r, otro_sin))
        elif otro_sin:
            pats.append((r"\b" + r, True))
    return pats


def _menciones(texto: str, an: Analisis, d: Optional[Dict] = None) -> Dict[int, int]:
    """Posición de la primera mención de cada grupo en el texto."""
    d = d or an.datos
    n1, n2 = d.get("nombre1") or "", d.get("nombre2") or ""
    pos = {}
    for j, (nom, otro) in ((1, (n1, n2)), (2, (n2, n1))):
        for p, excluir_sin in _claves_grupo(nom, otro):
            for m in re.finditer(p, texto):
                if excluir_sin and _hay(_SIN + r"$", texto[max(0, m.start() - 8):m.start()]):
                    continue
                if j not in pos or m.start() < pos[j]:
                    pos[j] = m.start()
                break
    if len(pos) < 2 and d.get("sujeto"):   # menciones por el rol ('el aditivo', 'sin el aditivo', 'tradicional')
        nuevo = int(d["sujeto"])
        solo_falta = bool(pos)   # uno ya se nombró: el otro por su rol ('la vieja' cuando se llama 'actual')
        if 3 - nuevo not in pos:
            for m in re.finditer(RE_REF, texto):
                if not _hay(r"^sin (presencia|diferencia)", texto[m.start():m.start() + 20]):
                    if not (solo_falta and m.start() == pos.get(nuevo)):
                        pos.setdefault(3 - nuevo, m.start())
                    break
        if nuevo not in pos:
            for m in re.finditer(RE_NUEVO_V, texto):
                if not _hay(_SIN + r"$", texto[max(0, m.start() - 8):m.start()]):
                    if not (solo_falta and m.start() == pos.get(3 - nuevo)):
                        pos.setdefault(nuevo, m.start())
                    break
    return pos


def _direccion(s: str) -> Optional[str]:
    mas, menos = _cuenta(P_MAS_V, s), _cuenta(P_MENOS_V, s)
    if mas > menos:
        return "mas"
    if menos > mas:
        return "menos"
    if _hay(P_BILATERAL_V, s):
        return "bilateral"
    return None


def _afirmacion_del_planteo(planteo_norm: str, an: Analisis) -> Tuple[Optional[str], Optional[int], str]:
    """(dirección, sujeto, oración) de la última oración del planteo que afirma algo comparativo."""
    from .texto import oraciones
    mejor = (None, None, "")
    for ini, fin in oraciones(planteo_norm):
        o = planteo_norm[ini:fin]
        dr = _direccion(o)
        if dr is None:
            continue
        men = _menciones(o, an)
        suj = min(men, key=men.get) if men else None
        if mejor[0] is None or suj is not None or mejor[1] is None:
            mejor = (dr, suj, o)
    return mejor


def _magnitud(t, an: Analisis, solo_libres=True) -> Optional[Tuple[str, float, Numero]]:
    """δ₀ ('en 0,5 litros al menos', 'en más de 2 quintales') o proporción ('en un 10%')."""
    escala = re.search(r"en miles de ([a-z]+)", normalizar(an.planteo))
    for i, n in (t.libres() if solo_libres else enumerate(t.nums)):
        if A._alpha_de(t, i, n):
            continue
        a, d = t.antes(n, 50), t.despues(n, 40)
        if _hay(r"(riesgo|confianza|seguridad|probabilidad)[^0-9]{0,12}$", a):
            continue
        if n.pct:
            if _hay(r"(en|un|del|de|el)\s*$", a) and _hay(P_MAS_V + "|" + P_MENOS_V + r"|al menos|como minimo|por lo menos",
                                                       a[-40:] + " " + d[:30]):
                return "pct", n.fraccion, n
            continue
        if _hay(r"(\ben|\bde|superior en|mayor en|minima de|por mas de|mas de|en mas de|"
                r"en (por lo menos|al menos|como minimo))\s*$", a) and \
                _hay(P_MAS_V + "|" + P_MENOS_V + r"|al menos|como minimo|por lo menos|diferencia", a[-60:] + " " + d[:35]) or \
                _hay(r"^\s*[a-z.]*\s*(al menos|como minimo|por lo menos|o mas\b)", d) or \
                (_hay(r"(al menos|como minimo|por lo menos)\s*$", a) and _hay(P_MAS_V + "|" + P_MENOS_V, a[-60:])) or \
                (_hay(r"(como minimo|al menos|por lo menos|como maximo)\s*$", a) and
                 _hay(r"^\s*([a-z.]+\s+){0,4}(mas|menos)\b", d)):
            valor = n.valor
            if escala and _hay(r"^\s*" + escala.group(1) + r"\b", d) and not _hay(r"^\s*miles", d):
                valor = valor / 1000
            return "delta", valor, n
    return None


def _una_media(inc: Inciso, an: Analisis, t, previo: Dict) -> bool:
    """El inciso habla de la media de UN grupo contra un valor ('las ventas medias con la campaña eran inferiores a
    580.000', 'con el producto tradicional el rendimiento medio es de 19,5'): ensayo de una media."""
    norm = t.norm
    if inc.tipo != "ensayo" or not _hay(r"(media|medio|promedio)", norm) or _hay(r"diferencia", norm):
        return False
    medias = [an.datos.get("xbar1"), an.datos.get("xbar2")]
    for j in (1, 2):
        lista = an.datos.get(f"datos{j}")
        if medias[j - 1] is None and lista and len(lista) >= 2:
            medias[j - 1] = resumen_muestra(list(lista)).xbar
    if None in medias:
        return False
    for i, n in t.libres():
        if n.pct or A._alpha_de(t, i, n):
            continue
        if not any(m and 0.5 <= n.valor / m <= 2 for m in medias):
            continue
        a = t.antes(n, 120)
        men = _menciones(norm[:n.ini], an)
        if not men:
            continue
        g = max(men, key=men.get)   # el grupo nombrado más cerca antes del valor
        comparativo = re.search(r"(inferior|menor|superior|mayor)[a-z]* (a|que|de)\s*$", a)
        hipotesis = comparativo is not None or _hay(r"hipotesis", norm[:n.ini])
        probado = g if hipotesis else 3 - g
        if comparativo:
            tail = "derecha" if comparativo.group(1) in ("inferior", "menor") else "izquierda"
            razon = (f"La hipótesis ensayada es μ({an.datos.get(f'nombre{probado}')}) "
                     f"{'≤' if tail == 'derecha' else '≥'} {fmt(n.valor)}: si se la rechazó, la probabilidad de haberse "
                     "equivocado es el valor a posteriori α*.")
        else:
            arriba = previo.get("sujeto") == probado and previo.get("tail") != "izquierda" or \
                previo.get("sujeto") not in (None, probado) and previo.get("tail") == "izquierda" or \
                previo.get("sujeto") is None
            tail = "derecha" if arriba else "izquierda"
            razon = (f"Se da la media POBLACIONAL de {an.datos.get(f'nombre{g}')} (μ₀ = {fmt(n.valor)}): se ensaya "
                     f"una sola media, la de {an.datos.get(f'nombre{probado}')}.")
        lista = an.datos.get(f"datos{probado}")
        if lista and len(lista) >= 2:
            r = resumen_muestra(list(lista))
            xbar, s, nn = r.xbar, r.s, r.n
        else:
            xbar, s, nn = an.datos.get(f"xbar{probado}"), an.datos.get(f"s{probado}"), an.datos.get(f"n{probado}")
        if None in (xbar, s, nn):
            return False
        t.usar(i)
        inc.params.update(tema="media", mu0=n.valor, xbar=xbar, desvio=s, n=int(nn), sigma_conocido=False, tail=tail)
        inc.razones.append(razon)
        return True
    return False


def params_dos_medias(inc: Inciso, an: Analisis, t, previo: Dict):
    """Sujeto (quién va primero en δ), cola, δ₀ o h y si se pide un porcentaje."""
    p = inc.params
    norm = t.norm
    pl = normalizar(an.planteo)
    for k in ("delta0", "delta0_pct"):
        p.pop(k, None)
    if _una_media(inc, an, t, previo):
        return
    men = _menciones(norm, an)
    dr = _direccion(norm)
    dr_pl, suj_pl, _ = _afirmacion_del_planteo(pl, an)
    if men:
        sujeto, razon = min(men, key=men.get), "es el grupo del que el inciso afirma algo"
    elif suj_pl is not None and (dr is None or inc.tipo != "ensayo"):
        sujeto, razon = suj_pl, "es el grupo del que habla la afirmación del planteo"
    elif an.datos.get("sujeto"):
        sujeto, razon = int(an.datos["sujeto"]), "es el grupo con el cambio (nuevo / tratado / con aditivo)"
    else:
        sujeto, razon = None, ""
    if sujeto is not None:
        p["sujeto"] = sujeto
        inc.razones.append(f"δ = μ({an.datos.get(f'nombre{sujeto}')}) - μ({an.datos.get(f'nombre{3 - sujeto}')}): "
                           f"{an.datos.get(f'nombre{sujeto}')} va primero porque {razon}.")
    if inc.tipo in ("ensayo", "diseno"):
        direccion = dr or dr_pl
        if direccion is None and _hay(r"(idem|igual que|misma)", norm) and previo.get("direccion"):
            direccion = previo["direccion"]
        if direccion in (None, "bilateral"):
            # El profesor (01/10): «jamás me planteen una hipótesis bilateral en comparación»; la muestra orienta el
            # ensayo (unilateral en el sentido que muestran los datos). Así lo resuelve también la guía en V-2, V-13 y
            # V-21. Vale para el ensayo y para el planteo a priori.
            p["tail"] = "derecha"
            p["sujeto_por_datos"] = True
            p["bilateral_pregunta"] = True
            inc.razones.append("Pregunta si las medias difieren sin dirección. En comparaciones no hay ensayos bilaterales "
                               "(profesor en clase): se plantea unilateral en el sentido que muestran los datos (H1: el de "
                               "mayor media supera al otro).")
        else:
            nuevo = int(an.datos.get("sujeto") or 0)
            if direccion == "menos" and sujeto is not None and nuevo and sujeto == 3 - nuevo:
                # 'la máquina vieja produce al menos 2 menos que la nueva' ≡ 'la nueva produce al menos 2 MÁS que la
                # vieja': se plantea δ = μ(nuevo) - μ(referencia) > δ₀ (lo que se quiere probar en H1, en positivo)
                sujeto, direccion = nuevo, "mas"
                p["sujeto"] = nuevo
                inc.razones.append(f"La afirmación dice que {an.datos.get(f'nombre{3 - nuevo}')} da MENOS que "
                                   f"{an.datos.get(f'nombre{nuevo}')}: es lo mismo que {an.datos.get(f'nombre{nuevo}')} "
                                   f"da MÁS → δ = μ({an.datos.get(f'nombre{nuevo}')}) - "
                                   f"μ({an.datos.get(f'nombre{3 - nuevo}')}) y H1: δ > δ₀.")
            p["tail"] = "derecha" if direccion == "mas" else "izquierda"
            p["direccion"] = direccion
            if sujeto is None:
                p["sujeto_por_datos"] = True
                inc.razones.append("No se nombra qué grupo supera al otro: δ se orienta hacia donde apuntan las muestras.")
            inc.razones.append("Lo que se quiere probar es que el primero " +
                               ("SUPERA al segundo → H1: δ > δ₀ (cola derecha)." if direccion == "mas" else
                                "es MENOR que el segundo → H1: δ < δ₀ (cola izquierda)."))
        mag = None
        extra = re.search(r"\(([^()]*\d[^()]*)\)\s*$", inc.texto) if "." in inc.letra else None
        if extra:   # 'Ídem a), si se deseara asegurar un incremento del 10%': manda la condición nueva
            mag = _magnitud(A.Texto(extra.group(1)), an, solo_libres=False)
        mag = mag or _magnitud(t, an)
        if mag is None and not _hay(r"\d", re.sub(r"\d+\s*%|\bh\s*[01]\b", "", norm)):   # 'Plantear H0' no es un dato
            mag = _magnitud(A.Texto(_afirmacion_del_planteo(pl, an)[2]), an, solo_libres=False)
        if mag:
            clase, valor, _ = mag
            if clase == "pct":
                p["delta0_pct"] = valor
                inc.razones.append(f"La diferencia es proporcional ({fmt(valor * 100)}%): δ* = μ₁ - h·μ₂ con "
                                   f"h = 1 {'+' if p.get('tail') != 'izquierda' else '-'} {fmt(valor)}.")
            else:
                p["delta0"] = valor
                inc.razones.append(f"Diferencia de referencia |δ₀| = {fmt(valor, 6)}.")
    if inc.tipo == "ic" and _hay(r"porcentual|porcentaje|por ciento|%\s*(minimo|maximo)", norm) and \
            _hay(r"minim|maxim", norm):
        p["porcentual"] = True
        inc.razones.append("Pide la diferencia PORCENTUAL mínima / máxima: se busca h = μ₁/μ₂ garantizado "
                           "(el incremento es (h - 1)·100%).")


# ---------------------------------------------------------------------------
# Resolución
# ---------------------------------------------------------------------------

_LADOS = ("n", "xbar", "s", "datos", "nombre", "sigma_pob")


def _invertir(d: Dict) -> Dict:
    d = dict(d)
    for k in _LADOS:
        v1, v2 = d.get(k + "1"), d.get(k + "2")
        d[k + "1"], d[k + "2"] = v2, v1
    return d


def _orientar(d: Dict, tail: Optional[str]) -> Dict:
    """Muestra 'sujeto' primero. Sin sujeto y con dirección, se orienta hacia donde apuntan las medias."""
    if int(d.get("sujeto") or 1) == 2:
        d = _invertir(d)
    if d.get("sujeto_por_datos") and tail in ("derecha", "izquierda") and None not in (d.get("xbar1"), d.get("xbar2")):
        if (tail == "derecha") != (d["xbar1"] >= d["xbar2"]):
            d = _invertir(d)
    return d


def _plantear(d: Dict, alpha: float, res: Resultado) -> Dict:
    """Decide el modelo: apareadas, Z (σ conocidos), pooled o Welch (test F previo al 10%)."""
    a, b = d.get("nombre1") or "1", d.get("nombre2") or "2"
    if d.get("apareadas"):
        l1, l2 = d.get("datos1"), d.get("datos2")
        if not l1 or not l2 or len(l1) != len(l2):
            raise FaltaDato("Para muestras apareadas hacen falta las dos listas de datos, del mismo largo")
        return {"metodo": "apareadas", "l1": list(l1), "l2": list(l2)}
    s1, n1, s2, n2 = d.get("s1"), d.get("n1"), d.get("s2"), d.get("n2")
    sig1, sig2 = d.get("sigma_pob1"), d.get("sigma_pob2")
    faltan = [k for k in ("n1", "xbar1", "n2", "xbar2") if d.get(k) in (None, "")]
    if faltan:
        raise FaltaDato("Falta cargar: " + ", ".join(faltan))
    if sig1 and sig2:
        if s1 and s2 and d.get("sigma_afirmado"):
            sc1, r1 = two.verificar_desvio_afirmado(float(s1), int(n1), float(sig1), alpha)
            sc2, r2 = two.verificar_desvio_afirmado(float(s2), int(n2), float(sig2), alpha)
            res.numeros += [sc1, sc2]
            res.pasos.append(f"**Modelo**: ¿valen los desvíos afirmados? H0: σ ≤ σ₀ (χ², α = {fmt(alpha, 4)}). "
                             f"{a}: Sc = σ₀·√(χ²({fmt(1 - alpha, 4)}; {int(n1) - 1})/{int(n1) - 1}) = {fmt(sc1, 4)} vs "
                             f"S = {fmt(s1, 4)} → {'se rechaza: σ no es ' + fmt(sig1) if r1 else 'no se rechaza'}. "
                             f"{b}: Sc = {fmt(sc2, 4)} vs S = {fmt(s2, 4)} → "
                             f"{'se rechaza: σ no es ' + fmt(sig2) if r2 else 'no se rechaza'}.")
            if not (r1 or r2):
                return {"metodo": "z", "s1": float(sig1), "s2": float(sig2)}
            res.pasos.append("Los desvíos poblacionales no son los afirmados: se los considera desconocidos y se "
                             "trabaja con S.")
        else:
            res.pasos.append(f"**Modelo**: desvíos poblacionales conocidos, σ({a}) = {fmt(sig1)}, σ({b}) = {fmt(sig2)} → "
                             "σ(d) = √(σ₁²/n₁ + σ₂²/n₂) y distribución Z.")
            return {"metodo": "z", "s1": float(sig1), "s2": float(sig2)}
    if s1 in (None, "") or s2 in (None, ""):
        raise FaltaDato("Falta cargar: " + ", ".join(k for k in ("s1", "s2") if d.get(k) in (None, "")))
    s1, s2, n1, n2 = float(s1), float(s2), int(n1), int(n2)
    alpha_f = float(d.get("alpha_var") or ALPHA_VARIANZAS)
    f = two.f_test_equal_variances(s1, n1, s2, n2, alpha_f)
    may, men = (a, b) if s1 >= s2 else (b, a)
    nmay, nmen = (n1, n2) if s1 >= s2 else (n2, n1)
    j2, j2c = f.observed_value, f.critical_value
    iguales = not f.rejects_h0
    res.numeros += [j2c, sqrt(j2c), j2, sqrt(j2)]
    res.pasos.append(("" if res.pasos and res.pasos[-1].startswith("Los desvíos") else "**Modelo**: ") +
                     f"**ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S({may}) > "
                     f"S({men}), lo único que se puede sospechar es σ({may}) > σ({men}) → unilateral, H0: "
                     f"φ = σ({may})/σ({men}) ≤ 1, con un α propio y grande α = {fmt(alpha_f, 4)} (no el del problema: "
                     f"si no se rechaza se quiere poder suponerlos iguales). Jc = √F({fmt(1 - alpha_f, 4)}; ν₁ = "
                     f"{nmay - 1}; ν₂ = {nmen - 1}) = √{fmt(j2c, 4)} = {fmt(sqrt(j2c), 4)}; J = S({may})/S({men}) = "
                     f"{fmt(sqrt(j2), 4)} → " +
                     (f"J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y "
                      "se amalgaman (Sa)." if iguales else
                      f"J > Jc: se rechaza H0 → los desvíos son DISTINTOS → Welch."))
    metodo = "pooled" if iguales else "welch"
    err = two.error_dos_medias(s1, n1, s2, n2, metodo)
    if metodo == "pooled":
        res.numeros += [err.s_a, err.df]
        res.pasos.append(f"Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = {fmt(err.s_a, 6)}; ν = n₁ + n₂ - 2 = {err.df}.")
    else:
        res.numeros += [err.df_raw, err.df]
        res.pasos.append(f"ν de Aspin-Welch = (S₁²/n₁ + S₂²/n₂)²/[(S₁²/n₁)²/(n₁-1) + (S₂²/n₂)²/(n₂-1)] = "
                         f"{fmt(err.df_raw, 4)} → ν = {err.df}.")
    return {"metodo": metodo, "s1": s1, "s2": s2}


def _txt_metodo(c: Dict) -> str:
    return {"pooled": "t con Sa (desvíos iguales)", "welch": "t de Welch (desvíos distintos)",
            "z": "Z (desvíos poblacionales conocidos)", "apareadas": "t sobre las diferencias (apareadas)"}[c["metodo"]]


def dos_medias_ensayo(d, alpha, res: Resultado, estado):
    """Ensayo sobre δ (o δ*); si la tabla trae varios pares (con / sin a distintas temperaturas) uno por par."""
    pares = d.get("comparaciones")
    if not pares:
        _ensayo_simple(d, alpha, res, estado)
        return
    from .presentacion import siete_pasos
    d["ambos"] = True   # varios ensayos en un inciso: cada uno ya va con sus 7 pasos (como la doble condición)
    resumenes, conclusiones = [], []
    for k, (nom1, l1, nom2, l2) in enumerate(pares, 1):
        dd = {c: v for c, v in d.items() if not re.fullmatch(r"(n|xbar|s|datos|nombre|sigma_pob)[12]", c)}
        dd.update(nombre1=nom1, datos1=list(l1), nombre2=nom2, datos2=list(l2), comparaciones=None)
        for j, lista in ((1, l1), (2, l2)):
            r = resumen_muestra(list(lista))
            dd.update({f"n{j}": r.n, f"xbar{j}": r.xbar, f"s{j}": r.s})
        sub = Resultado()
        _ensayo_simple(dd, alpha, sub, estado)
        res.pasos.append(f"**— Comparación {k}: {nom1} vs {nom2} —**")
        res.pasos += siete_pasos(sub.pasos, alpha, sub.regla)
        res.numeros += sub.numeros
        resumenes.append(f"{k}) {sub.resumen.split('; ')[-1]}")
        conclusiones.append(f"{k}) {nom1} vs {nom2}: {sub.conclusion}")
    res.conclusion = " ".join(conclusiones)
    res.resumen = "; ".join(resumenes)


def _ensayo_simple(d, alpha, res: Resultado, estado):
    tail = d.get("tail") or "bilateral"
    if tail == "bilateral":
        # nunca bilaterales en comparaciones (profesor en clase): se orienta por los datos
        tail = "derecha"
        d = dict(d, sujeto_por_datos=True, bilateral_pregunta=True)
        res.avisos.append("En comparaciones no hay ensayos bilaterales (profesor en clase): se planteó el unilateral en el "
                          "sentido que muestran las muestras.")
    d = _orientar(d, tail)
    a, b = d.get("nombre1") or "1", d.get("nombre2") or "2"
    c = _plantear(d, alpha, res)
    pct = d.get("delta0_pct")
    h = 1.0 + (pct if tail != "izquierda" else -pct) if pct else 1.0
    delta0 = abs(float(d.get("delta0") or 0.0))
    delta0 = -delta0 if tail == "izquierda" else delta0
    param = f"δ = μ({a}) - μ({b})" if h == 1 else f"δ* = μ({a}) - {fmt(h, 4)}·μ({b})"
    if c["metodo"] == "apareadas":
        dif = [x - h * y for x, y in zip(c["l1"], c["l2"])]
        rs = resumen_muestra(dif)
        r = two.ensayo_media_apareada(dif, delta0, alpha, tail=tail)
        se, obs = rs.s / sqrt(rs.n), rs.xbar
        res.numeros += [rs.xbar, rs.s, rs.n - 1]
        res.pasos.append(f"**Modelo**: muestras apareadas, dᵢ = x({a}) - {'' if h == 1 else fmt(h, 4) + '·'}x({b}) → "
                         f"d̄ = {fmt(rs.xbar, 4)}, S_d = {fmt(rs.s, 4)}, n = {rs.n} pares (ν = {rs.n - 1}); "
                         f"σ(d̄) = S_d/√n = {fmt(se, 4)}.")
    else:
        r = two.ensayo_dos_medias(d["xbar1"], c["s1"], int(d["n1"]), d["xbar2"], c["s2"], int(d["n2"]), alpha,
                                  tail=tail, delta0=delta0, h=h, metodo=c["metodo"])
        se, obs = r.se, r.observed_value
        res.pasos.append(f"Diferencia observada ({_txt_metodo(c)}): d{'*' if h != 1 else ''} = x̄({a}) - "
                         f"{'' if h == 1 else fmt(h, 4) + '·'}x̄({b}) = {fmt(obs, 4)}; σ(d{'*' if h != 1 else ''}) = "
                         f"{fmt(se, 6)}" + (f", ν = {r.df}" if r.df else "") + ".")
    s0, s1 = {"derecha": ("≤", ">"), "izquierda": ("≥", "<"), "bilateral": ("=", "≠")}[tail]
    if h == 1:
        h0, h1 = f"{param} {s0} {fmt(delta0, 6)}", f"{param} {s1} {fmt(delta0, 6)}"
    else:
        h0 = f"μ({a}) {s0} {fmt(h, 4)}·μ({b}) ({param} {s0} 0)"
        h1 = f"μ({a}) {s1} {fmt(h, 4)}·μ({b})"
    res.pasos.insert(0, f"**Hipótesis**: H0: {h0}  vs  H1: {h1}  (α = {fmt(alpha, 4)}).")
    crit = r.critical_value
    if isinstance(crit, tuple):
        cond = f"d < {fmt(crit[0], 4)} o d > {fmt(crit[1], 4)}"
    else:
        cond = f"d {_signo(tail)} {fmt(crit, 4)}"
    q = "z" if c["metodo"] == "z" else "t"
    res.pasos.append(f"**Condición de rechazo**: d_c = δ₀ {'∓' if tail == 'bilateral' else '+' if tail == 'derecha' else '-'} "
                     f"{q}·σ(d) = {_cv(crit)}. Si {cond} ⇒ se rechaza H0.")
    res.pasos.append(f"**Decisión**: d = {fmt(obs, 4)} → " + ("se rechaza H0." if r.rejects_h0 else "no se rechaza H0."))
    if r.p_value is not None:
        res.pasos.append(f"Dato informativo (no es criterio de decisión): valor a posteriori α* = {fmt(r.p_value, 4)}. "
                         "La decisión se toma comparando el estimador con el valor crítico.")
    r.h0_text, r.h1_text = h0, h1
    res.conclusion = _ensayo_txt(r, alpha, f"d = {fmt(obs, 4)}", d)
    res.regla = _regla(d, f"calcula la diferencia d entre {'las medias muestrales' if c['metodo'] != 'apareadas' else 'los pares'}",
                       cond, h1)
    res.numeros += (list(crit) if isinstance(crit, tuple) else [crit]) + [obs]
    if h != 1:
        res.numeros += [h]
    res.resumen = f"H0: {h0}; dc = {_cv(crit)}; " + ("RECHAZA H0" if r.rejects_h0 else "NO rechaza H0")
    estado.update(metodo=c["metodo"], tail=tail)
    if d.get("bilateral_pregunta") and tail != "bilateral":
        res.pasos.append("**Orientación**: el enunciado no da dirección («¿difieren?»), pero en comparaciones no existen "
                         "ensayos bilaterales: la muestra orienta el ensayo y lo único que se puede intentar probar es que "
                         f"μ({a}), el de mayor media muestral, supera a μ({b}).")


def dos_medias_beta(d, alpha, res: Resultado, estado):
    """β y potencia del ensayo de δ para una diferencia real δ₁ (aproximación normal con el error estándar del ensayo)."""
    d1 = d.get("delta1")
    if d1 is None:
        raise FaltaDato("Falta la diferencia real δ₁ para la que se pide la probabilidad")
    tail = d.get("tail") or estado.get("tail") or ("derecha" if d1 >= 0 else "izquierda")
    d = _orientar(d, tail)
    c = _plantear(d, alpha, res)
    if c["metodo"] != "z":
        from .resolver import FueraDeCatedra
        raise FueraDeCatedra("En comparaciones de medias con desvíos desconocidos (amalgamado, Welch o apareadas) la "
                             "cátedra no calcula β, potencia ni n: hace falta la t no central («no lo vamos a generar "
                             "para ustedes», profesor en clase). Solo con σ₁ y σ₂ conocidos (Z).")
    delta0 = abs(float(d.get("delta0") or 0.0)) * (-1 if tail == "izquierda" else 1)
    if c["metodo"] == "apareadas":
        rs = resumen_muestra([x - y for x, y in zip(c["l1"], c["l2"])])
        se, df = rs.s / sqrt(rs.n), rs.n - 1
        q = dist.t_two_tailed(alpha, df) if tail == "bilateral" else dist.t_one_tailed(alpha, df)
    else:
        err = two.error_dos_medias(c["s1"], int(d["n1"]), c["s2"], int(d["n2"]), c["metodo"], 1.0)
        se, df = err.se, err.df
        if c["metodo"] == "z":
            q = dist.z_two_tailed(alpha) if tail == "bilateral" else dist.z_one_tailed(alpha)
        else:
            q = dist.t_two_tailed(alpha, df) if tail == "bilateral" else dist.t_one_tailed(alpha, df)
    d1 = abs(d1) * (-1 if tail == "izquierda" else 1)
    if tail == "bilateral":
        c1, c2 = delta0 - q * se, delta0 + q * se
        beta = dist.norm_cdf((c2 - d1) / se) - dist.norm_cdf((c1 - d1) / se)
        crit = f"[{fmt(c1, 4)} ; {fmt(c2, 4)}]"
        calc = f"β = P({fmt(c1, 4)} ≤ d ≤ {fmt(c2, 4)} | δ = {fmt(d1, 4)})"
    elif tail == "derecha":
        dc = delta0 + q * se
        beta = dist.norm_cdf((dc - d1) / se)
        crit, calc = fmt(dc, 4), f"β = P(d ≤ {fmt(dc, 4)} | δ = {fmt(d1, 4)}) = P(Z ≤ {fmt((dc - d1) / se, 4)})"
    else:
        dc = delta0 - q * se
        beta = 1 - dist.norm_cdf((dc - d1) / se)
        crit, calc = fmt(dc, 4), f"β = P(d ≥ {fmt(dc, 4)} | δ = {fmt(d1, 4)}) = P(Z ≥ {fmt((dc - d1) / se, 4)})"
    a, b = d.get("nombre1") or "1", d.get("nombre2") or "2"
    res.pasos.append(f"**Ensayo**: δ = μ({a}) - μ({b}); valor crítico d_c = {crit} ({_txt_metodo(c)}; σ(d) = {fmt(se, 6)}).")
    res.pasos.append(f"**Probabilidad**: {calc} = {fmt(beta, 4)}; potencia 1-β = {fmt(1 - beta, 4)}"
                     + (" (con t se usa la aproximación normal para β, como en una población)." if c["metodo"] != "z" else "."))
    res.numeros += [beta, 1 - beta]
    pide = d.get("prob") or "beta"
    res.resumen = f"β = {fmt(beta, 4)} ; 1-β = {fmt(1 - beta, 4)}"
    res.conclusion = (f"Si la diferencia real fuera δ = {fmt(d1, 4)}, la probabilidad de "
                      + (f"detectarla (rechazar H0) es 1-β = {fmt(1 - beta, 4)}." if pide == "potencia" else
                         f"no detectarla (no rechazar H0) es β = {fmt(beta, 4)}."))


def dos_medias_diseno(d, alpha, res: Resultado, estado):
    """Planteo a priori: H0 / H1, α y la condición de rechazo (con las muestras disponibles, si las hay)."""
    res.pasos.append("**Planteo a priori**: la hipótesis se fija antes de mirar los datos, a partir de la "
                     "afirmación que justificaría la decisión (criterio pesimista: H1 es lo que habilita el cambio).")
    try:
        dos_medias_ensayo(d, alpha, res, estado)
    except FaltaDato:
        tail = d.get("tail") or "bilateral"
        d = _orientar(d, tail)
        a, b = d.get("nombre1") or "1", d.get("nombre2") or "2"
        d0 = abs(float(d.get("delta0") or 0)) * (-1 if tail == "izquierda" else 1)
        signo0 = {"derecha": "≤", "izquierda": "≥", "bilateral": "="}[tail]
        res.pasos.append(f"**Hipótesis**: H0: δ = μ({a}) - μ({b}) {signo0} {fmt(d0, 4)} (α = {fmt(alpha, 4)}).")
        res.resumen = f"H0: δ {signo0} {fmt(d0, 4)}"


def _inecuacion_h(x1: float, c: Dict, n1: int, x2: float, n2: int, alpha: float, cota: str) -> Optional[str]:
    """Porcentaje mínimo / máximo como lo resuelve el profesor (V-8d): la CR como inecuación en h, al cuadrado, la
    cuadrática y la VERIFICACIÓN de cada raíz en la inecuación original (una de las dos no sirve).
    Solo con fractil constante (amalgamado o Z); con Welch ν depende de h y se itera."""
    from math import sqrt as raiz
    if c["metodo"] == "pooled":
        sa2 = ((n1 - 1) * c["s1"] ** 2 + (n2 - 1) * c["s2"] ** 2) / (n1 + n2 - 2)
        c1, c2, q = sa2 / n1, sa2 / n2, dist.t_one_tailed(alpha, n1 + n2 - 2)
        err = f"t(1-α; {n1 + n2 - 2})·Sa·√(1/n₁ + h²/n₂)"
    elif c["metodo"] == "z":
        c1, c2, q = c["s1"] ** 2 / n1, c["s2"] ** 2 / n2, dist.z_one_tailed(alpha)
        err = "Z(1-α)·√(σ₁²/n₁ + h²·σ₂²/n₂)"
    else:
        return None
    A, B, C = x2 ** 2 - q ** 2 * c2, -2 * x1 * x2, x1 ** 2 - q ** 2 * c1
    disc = B * B - 4 * A * C
    if A == 0 or disc < 0:
        return None
    raices = sorted(((-B - raiz(disc)) / (2 * A), (-B + raiz(disc)) / (2 * A)))
    signo = ">" if cota == "inf" else "<"
    lineas = [f"**Inecuación en h**: x̄₁ - h·x̄₂ {signo} {'' if cota == 'inf' else '-'}{err} (h² va en el término de la "
              f"población que lleva h). Con {fmt(x1, 4)} - {fmt(x2, 4)}·h y fractil {fmt(q, 4)}, al elevar al cuadrado: "
              f"{fmt(A, 4)}·h² {'+' if B >= 0 else '-'} {fmt(abs(B), 4)}·h {'+' if C >= 0 else '-'} {fmt(abs(C), 4)} = 0 → "
              f"raíces h = {redondeo.fijo(raices[0], 4)} y h = {redondeo.fijo(raices[1], 4)}. Verificación en la inecuación original:"]
    for h in raices:
        izq = x1 - h * x2
        der = q * raiz(c1 + h * h * c2)
        vale = izq >= 0 if cota == "inf" else izq <= 0
        lineas.append(f"h = {redondeo.fijo(h, 4)}: x̄₁ - h·x̄₂ = {fmt(izq, 4)}; {'sirve' if vale else 'NO sirve'} "
                      f"({'el lado izquierdo es negativo y no puede igualar a +' + fmt(der, 4) if not vale and cota == 'inf' else 'es raíz de la igualdad original' if vale else 'el lado izquierdo es positivo'}).")
    return " ".join(lineas)


def _cota_apareada(dif, alpha, cota):
    rs = resumen_muestra(dif)
    t = dist.t_one_tailed(alpha, rs.n - 1) if cota else dist.t_two_tailed(alpha, rs.n - 1)
    e = t * rs.s / sqrt(rs.n)
    a = rs.xbar - e if cota in (None, "inf") else float("-inf")
    b = rs.xbar + e if cota in (None, "sup") else float("inf")
    return a, b, e, rs


def dos_medias_ic(d, alpha, res: Resultado, estado):
    cota = d.get("cota")
    d = _orientar(d, None)
    a, b = d.get("nombre1") or "1", d.get("nombre2") or "2"
    c = _plantear(d, alpha, res)
    if d.get("porcentual") and cota:
        if c["metodo"] == "apareadas":
            raise FaltaDato("La diferencia porcentual garantizada con muestras apareadas no está implementada")
        h = two.h_limite_dos_medias(d["xbar1"], c["s1"], int(d["n1"]), d["xbar2"], c["s2"], int(d["n2"]), alpha,
                                    metodo=c["metodo"], cota=cota)
        lado = "mínima" if cota == "inf" else "máxima"
        res.pasos.append(f"**Relación {lado} garantizada** h = μ({a})/μ({b}) (h es una constante, no un parámetro: no se "
                         f"estima): es el h que deja en el límite la condición de rechazo de H0: μ({a}) "
                         f"{'≤' if cota == 'inf' else '≥'} h·μ({b}) con α = {fmt(alpha, 4)} (un solo límite: α entero).")
        cuad = _inecuacion_h(d["xbar1"], c, int(d["n1"]), d["xbar2"], int(d["n2"]), alpha, cota)
        if cuad:
            res.pasos.append(cuad)
        else:
            res.pasos.append(f"Con Welch ν depende de h (h² entra también en ν), así que se resuelve iterando: "
                             f"x̄({a}) - h·x̄({b}) {'=' if cota == 'inf' else '= -'} t(1-α; ν(h))·σ(d*(h)) → h = {fmt(h, 4)}.")
        res.conclusion = (f"Con un {fmt((1 - alpha) * 100, 2)}% de confianza, μ({a}) es como "
                          f"{'mínimo' if cota == 'inf' else 'máximo'} un "
                          f"{redondeo.fijo((h - 1) * 100, 2)}% {'mayor' if h >= 1 else 'menor'} que μ({b}) (h = {redondeo.fijo(h, 4)}).")
        res.numeros += [h, h - 1]
        res.resumen = f"h = {fmt(h, 4)} ({fmt((h - 1) * 100, 2)}%)"
        estado.update(metodo=c["metodo"])
        return
    if c["metodo"] == "apareadas":
        dif = [x - y for x, y in zip(c["l1"], c["l2"])]
        lo, hi, e, rs = _cota_apareada(dif, alpha, cota)
        estado["s_d"] = rs.s
        res.pasos.append(f"**Muestras apareadas**: dᵢ = x({a}) - x({b}) → d̄ = {fmt(rs.xbar, 4)}, S_d = {fmt(rs.s, 4)}, "
                         f"n = {rs.n} pares (ν = {rs.n - 1}); e = t({fmt(1 - (alpha if cota else alpha / 2), 4)}; "
                         f"{rs.n - 1})·S_d/√n = {fmt(e, 4)}.")
        centro = rs.xbar
    else:
        r = two.ic_dos_medias(d["xbar1"], c["s1"], int(d["n1"]), d["xbar2"], c["s2"], int(d["n2"]), alpha,
                              metodo=c["metodo"], cota=cota)
        lo, hi, e, centro = r.a, r.b, r.error, r.point_estimate
        q = "z" if c["metodo"] == "z" else f"t({fmt(1 - (alpha if cota else alpha / 2), 4)}; {r.df})"
        res.pasos.append(f"**{'Límite' if cota else 'IC'} para δ = μ({a}) - μ({b})** ({_txt_metodo(c)}): "
                         f"d = {fmt(centro, 4)}; e = {q}·σ(d) = {fmt(r.critical_value, 4)}·{fmt(e / r.critical_value, 6)} = "
                         f"{fmt(e, 4)}.")
    estado.update(e_actual=e, metodo=c["metodo"], alpha_ic=alpha)
    if cota == "inf":
        c = redondeo.cota(lo, False, 2)
        res.conclusion = (f"Con un {fmt((1 - alpha) * 100, 2)}% de confianza, μ({a}) - μ({b}) ≥ {c}: la diferencia "
                          f"mínima garantizada para {a} es {c} (redondeada hacia abajo; sin redondear {fmt(lo, 6)}).")
        res.numeros += [lo, e]
        res.resumen = f"δ ≥ {fmt(lo, 4)}"
    elif cota == "sup":
        c = redondeo.cota(hi, True, 2)
        res.conclusion = (f"Con un {fmt((1 - alpha) * 100, 2)}% de confianza, μ({a}) - μ({b}) ≤ {c} "
                          f"(redondeada hacia arriba; sin redondear {fmt(hi, 6)}).")
        res.numeros += [hi, e]
        res.resumen = f"δ ≤ {fmt(hi, 4)}"
    else:
        ia, ib, nota = redondeo.intervalo(-hi, -lo, 2)
        res.conclusion = (_p(f"μ({a}) - μ({b})", lo, hi, alpha, 2) + f" (e = {fmt(e, 4)}). Para μ({b}) - μ({a}): entre "
                          f"{ia} y {ib}. Límites redondeados hacia afuera; sin redondear: {fmt(lo, 6)} y {fmt(hi, 6)}.")
        res.numeros += [lo, hi, e, -hi, -lo]
        res.resumen = f"IC δ: [{fmt(lo, 4)} ; {fmt(hi, 4)}]"


def dos_medias_n(d, alpha, res: Resultado, estado):
    e = d.get("e")
    if e is None and d.get("reduccion") is not None:
        if estado.get("e_actual") is None:
            dos_medias_ic(dict(d, cota=None, porcentual=False), alpha, Resultado(), estado)
        e = estado["e_actual"] * (1 - d["reduccion"])
        res.pasos.append(f"**Error buscado**: e = {fmt(estado['e_actual'], 4)}·(1 - {fmt(d['reduccion'], 4)}) = {fmt(e, 4)}.")
    if e is None:
        raise FaltaDato("Falta el error e o la reducción pedida")
    res.numeros.append(e)
    a, b = d.get("nombre1") or "1", d.get("nombre2") or "2"
    tmp = Resultado()
    c = _plantear(d, alpha, tmp)
    if c["metodo"] == "apareadas":
        s_d = estado.get("s_d") or resumen_muestra([x - y for x, y in zip(c["l1"], c["l2"])]).s
        r = two.n_media_apareada_para_error(s_d, e, alpha)
        bases = [len(c["l1"])]
        res.pasos.append(f"Apareadas: n = [t(1-α/2; n-1)·S_d/e]², iterando: n = {r.n} pares {r.converged_values}.")
    else:
        r = two.n_dos_medias_para_error(c["s1"], c["s2"], e, alpha, metodo=c["metodo"])
        bases = [int(d["n1"]), int(d["n2"])]
        nu = {"pooled": "ν = 2n - 2", "welch": "ν de Welch con n₁ = n₂ = n", "z": "Z"}[c["metodo"]]
        res.pasos.append(f"Con n₁ = n₂ = n: e = fractil·√((S₁² + S₂²)/n) ({nu}); iterando: n = {r.n} "
                         f"{r.converged_values}.")
    deltas = []
    for base in bases:
        dn = max(0, r.n - base)
        if dn not in deltas:
            deltas.append(dn)
    res.numeros = [r.n] + deltas + res.numeros
    if len(bases) == 2:
        extra = (f" Hoy hay {bases[0]} de {a} y {bases[1]} de {b}: faltan {max(0, r.n - bases[0])} y "
                 f"{max(0, r.n - bases[1])} más.")
    else:
        extra = f" Hoy hay {bases[0]} pares: faltan {max(0, r.n - bases[0])} más."
    res.conclusion = f"Se necesitan n = {r.n} en cada muestra (e = {fmt(e, 4)})." + extra
    res.resumen = f"n = {r.n}"


EXTENSIONES["dos_medias"] = (lambda an, t: None, clasificar_dos_medias)
DESPACHO_EXTRA[("dos_medias", "ensayo")] = dos_medias_ensayo
DESPACHO_EXTRA[("dos_medias", "ic")] = dos_medias_ic
DESPACHO_EXTRA[("dos_medias", "n")] = dos_medias_n
DESPACHO_EXTRA[("dos_medias", "diseno")] = dos_medias_diseno
DESPACHO_EXTRA[("dos_medias", "beta")] = dos_medias_beta
