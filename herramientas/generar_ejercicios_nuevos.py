"""Ejercicios nuevos tipo examen, con redacciones distintas a las de la guía y los exámenes, para probar la app a ciegas.

    python -X utf8 herramientas/generar_ejercicios_nuevos.py      # escribe datos/ejercicios_nuevos.json

Los enunciados los escribió Claude (15/11/2026) siguiendo los temas del 2° parcial y las trampas que aparecen en los
exámenes: el grupo de referencia nombrado primero, sinónimos («más regular», «sostener», «alcanzan los resultados»),
complementos, cotas en porcentaje, datos «antes / después» de los mismos operarios, clases abiertas.

Las respuestas de referencia se calculan ACÁ, solo con scipy y las convenciones de la cátedra (REGLAS_PROFESOR.md),
sin importar nada de la app, y quedan fijas antes de correrla (evaluar_examenes.py --archivo …). Formato de
«esperado» igual que en examenes_reales.json: texto que aparece en el resumen, ["n", valor], ["d", "rechaza" |
"no_rechaza"] o ["alguno", [v1, v2]]; null = no se puntúa.
"""

import json
from math import ceil, sqrt
from pathlib import Path

from scipy import stats
from scipy.optimize import brentq

RAIZ = Path(__file__).resolve().parent.parent
A10 = 0.10      # α propio del test F auxiliar (profesor)


def r4(x):
    return round(float(x), 4)


# ---------------------------------------------------------------- referencias (convenciones de la cátedra)

def rc_binomial(n, p0, alpha):
    """Menor r con P(R ≥ r | n, p0) ≤ α (α real ≤ α)."""
    return next(r for r in range(n + 1) if stats.binom.sf(r - 1, n, p0) <= alpha)


def ic_exacto(r, n, alpha):
    a = stats.beta.ppf(alpha / 2, r, n - r + 1) if r > 0 else 0.0
    b = stats.beta.ppf(1 - alpha / 2, r + 1, n - r) if r < n else 1.0
    return a, b


def plan_binomial(p0, p1, alpha, beta):
    """Menor n con un r_c que cumple G(r_c | n; p0) ≤ α y F(r_c - 1 | n; p1) ≤ β (p1 > p0)."""
    for n in range(1, 5000):
        rc = rc_binomial(n, p0, alpha)
        if rc <= n and stats.binom.cdf(rc - 1, n, p1) <= beta:
            return n, rc


def test_f_aux(s1, n1, s2, n2):
    """True si los desvíos se suponen iguales (no se rechaza el F unilateral con α = 0,10, el mayor arriba)."""
    (sa, na), (sb, nb) = sorted(((s1, n1), (s2, n2)), reverse=True)
    return (sa / sb) ** 2 <= stats.f.ppf(1 - A10, na - 1, nb - 1)


def error_dos_medias(s1, n1, s2, n2, h=1.0):
    """(desvío de x̄1 - h·x̄2, ν) según el test F auxiliar: amalgamado o Welch truncado."""
    if test_f_aux(s1, n1, s2, n2):
        sa = sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
        return sa * sqrt(1 / n1 + h * h / n2), n1 + n2 - 2
    v1, v2 = s1 ** 2 / n1, h * h * s2 ** 2 / n2
    nu = (v1 + v2) ** 2 / (v1 ** 2 / (n1 - 1) + v2 ** 2 / (n2 - 1))
    return sqrt(v1 + v2), int(nu)


def media_s(xs):
    n = len(xs)
    m = sum(xs) / n
    return m, sqrt(sum((x - m) ** 2 for x in xs) / (n - 1)), n


def regresion(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    b1 = sxy / sxx
    b0 = my - b1 * mx
    s2 = (syy - b1 * sxy) / (n - 2)
    return dict(n=n, mx=mx, b0=b0, b1=b1, r2=sxy ** 2 / (sxx * syy), s=sqrt(s2), sb1=sqrt(s2 / sxx), sxx=sxx)


def chi_contingencia(tabla):
    filas, cols = [sum(f) for f in tabla], [sum(c) for c in zip(*tabla)]
    N = sum(filas)
    chi = sum((tabla[i][j] - filas[i] * cols[j] / N) ** 2 / (filas[i] * cols[j] / N)
              for i in range(len(filas)) for j in range(len(cols)))
    return chi, (len(filas) - 1) * (len(cols) - 1)


TANDAS = {1: ("ejercicios_nuevos.json", "15/11/2026", []), 2: ("ejercicios_nuevos_2.json", "16/11/2026", [])}
TANDA = 1


def ejercicio(ident, planteo, incisos, esperado, tablas=None, nota=""):
    _, fecha, lista = TANDAS[TANDA]
    lista.append(dict(id=ident, examen=f"Ejercicio nuevo (Claude, {fecha})", planteo=planteo,
                      incisos=incisos, tablas=tablas, esperado=esperado, nota=nota))


# ---------------------------------------------------------------- N1: proporción, decisión costosa + complemento

n, r = 150, 56
rc = rc_binomial(n, 0.30, 0.05)
a, b = ic_exacto(n - r, n, 0.10)
ejercicio("N1",
          "Una cadena de farmacias solo lanzará una línea propia de productos genéricos si más del 30% de sus clientes "
          "estaría dispuesto a comprarla. En una encuesta a 150 clientes elegidos al azar, 56 respondieron que la "
          "comprarían.",
          [["a", "Con un nivel de significación de 0,05, ¿alcanzan los resultados para lanzar la línea?"],
           ["b", "Con una confianza del 90%, ¿entre qué valores se encuentra la proporción de clientes que NO "
                 "comprarían la línea?"]],
          [[["d", "rechaza" if r >= rc else "no_rechaza"], ["n", rc]], [["n", r4(a)], ["n", r4(b)]]],
          nota=f"a) pesimista: H0 p ≤ 0,30, r_c = {rc}; b) complemento r = {n - r}")

# ---------------------------------------------------------------- N2: dos varianzas, «más regular», el que se quiere probar va segundo

sN, nN, sS, nS = 2.8, 16, 1.9, 21
j2 = (sN / sS) ** 2
fc = stats.f.ppf(0.95, nN - 1, nS - 1)
lo, hi = j2 / stats.f.ppf(0.975, nN - 1, nS - 1), j2 / stats.f.ppf(0.025, nN - 1, nS - 1)
ejercicio("N2",
          "Dos proveedores entregan rollos de film para envasar. Se midió el espesor (en micrones) de 16 rollos del "
          "proveedor Norte, con un desvío estándar de 2,8 micrones, y de 21 rollos del proveedor Sur, con un desvío "
          "estándar de 1,9 micrones. Compras solo pasará a trabajar con el proveedor Sur si se demuestra que su espesor "
          "es más regular que el del proveedor Norte.",
          [["a", "Con un riesgo del 5%, ¿qué decisión debería tomar Compras?"],
           ["b", "Estimar, con un nivel de confianza del 95%, el cociente entre la varianza del espesor del proveedor "
                 "Norte y la del proveedor Sur."]],
          [[["d", "rechaza" if j2 > fc else "no_rechaza"]], [["n", r4(lo)], ["n", r4(hi)]]],
          nota=f"a) H1: σ(Norte) > σ(Sur); j² = {r4(j2)} vs F = {r4(fc)}")

# ---------------------------------------------------------------- N3: apareadas «antes / después», cota mínima

antes = [12.4, 10.8, 13.1, 11.6, 12.9, 14.2, 11.1, 12.7]
despues = [10.9, 10.1, 11.2, 10.4, 11.5, 12.3, 10.6, 11.0]
d = [x - y for x, y in zip(antes, despues)]
dm, sd, nd = media_s(d)
tc = stats.t.ppf(0.95, nd - 1)
dc = 1 + tc * sd / sqrt(nd)
ejercicio("N3",
          "Para evaluar un curso de capacitación, se registró el tiempo (en minutos) que tardan los mismos ocho operarios "
          "en armar un tablero antes y después de hacer el curso:\n"
          "Antes: 12,4 - 10,8 - 13,1 - 11,6 - 12,9 - 14,2 - 11,1 - 12,7\n"
          "Después: 10,9 - 10,1 - 11,2 - 10,4 - 11,5 - 12,3 - 10,6 - 11,0",
          [["a", "¿Hay evidencia, al 5%, de que el curso reduce el tiempo medio de armado en más de 1 minuto?"],
           ["b", "¿Cuál es la reducción mínima del tiempo medio que se puede garantizar con un 95% de confianza?"]],
          [[["d", "rechaza" if dm > dc else "no_rechaza"]], [["n", r4(dm - tc * sd / sqrt(nd))]]],
          nota=f"apareadas: d̄ = {r4(dm)}, S_d = {r4(sd)}, d_c = {r4(dc)}")

# ---------------------------------------------------------------- N4: dos medias, %, la marca de referencia nombrada primero

xY, sY, nY = 1050, 95, 35
xX, sX, nX = 1250, 110, 40
se, nu = error_dos_medias(xX, 0, 0, 0) if False else error_dos_medias(sX, nX, sY, nY, 1.15)
dstar = xX - 1.15 * xY
dcrit = stats.t.ppf(0.99, nu) * se


def h_min(alpha):
    def g(h):
        e, v = error_dos_medias(sX, nX, sY, nY, h)
        return xX - h * xY - stats.t.ppf(1 - alpha, v) * e
    return brentq(g, 1.0, xX / xY)


ejercicio("N4",
          "Las lámparas LED de la marca Y, que la empresa usa hoy, duraron en promedio 1.050 horas, con un desvío de 95 "
          "horas, en un ensayo con 35 lámparas. En las mismas condiciones, 40 lámparas de la marca X duraron en promedio "
          "1.250 horas con un desvío de 110 horas. El proveedor de la marca X asegura que sus lámparas duran más de un "
          "15% más que las de la marca Y.",
          [["a", "Con un nivel de significación del 1%, ¿puede aceptarse lo que asegura el proveedor?"],
           ["b", "Con un 99% de confianza, ¿en qué porcentaje mínimo supera la duración media de la marca X a la de la "
                 "marca Y?"]],
          [["1,15·μ", ["d", "rechaza" if dstar > dcrit else "no_rechaza"]], [["n", r4(h_min(0.01))]]],
          nota=f"a) H1: μX > 1,15·μY; d* = {r4(dstar)} vs {r4(dcrit)} (ν = {nu}); b) h mínimo")

# ---------------------------------------------------------------- N5: χ² de independencia, pregunta indirecta

tabla5 = [[38, 22, 15], [30, 28, 22], [17, 25, 33]]
chi5, nu5 = chi_contingencia(tabla5)
ejercicio("N5",
          "Una empresa encuestó a 230 empleados sobre su conformidad con el nuevo sistema de turnos rotativos y registró "
          "el turno en el que trabaja cada uno:",
          [["a", "¿Depende el grado de conformidad del turno en el que se trabaja? Usar un riesgo del 5%."]],
          [[["n", r4(chi5)], ["d", "rechaza" if chi5 > stats.chi2.ppf(0.95, nu5) else "no_rechaza"]]],
          tablas=[{"titulo": "", "columnas": ["Turno", "Conforme", "Indiferente", "Disconforme"],
                   "filas": [["Mañana", 38, 22, 15], ["Tarde", 30, 28, 22], ["Noche", 17, 25, 33]]}],
          nota=f"χ² = {r4(chi5)}, ν = {nu5}")

# ---------------------------------------------------------------- N6: Poisson con clase abierta al final

vals6, fo6 = [0, 1, 2, 3, 4, 5], [18, 34, 30, 12, 4, 2]
N6 = sum(fo6)
lam = sum(v * f for v, f in zip(vals6, fo6)) / N6
p6 = [stats.poisson.pmf(v, lam) for v in vals6[:-1]] + [stats.poisson.sf(vals6[-2], lam)]
fe6 = [N6 * p for p in p6]
# amalgamado desde la cola: 3, 4 y ≥5 hasta llegar a Fe ≥ 5
fo_a, fe_a = fo6[:3] + [sum(fo6[3:])], fe6[:3] + [sum(fe6[3:])]
if fe6[3] >= 5 and fe6[4] + fe6[5] >= 5:
    fo_a, fe_a = fo6[:4] + [fo6[4] + fo6[5]], fe6[:4] + [fe6[4] + fe6[5]]
chi6 = sum((o - e) ** 2 / e for o, e in zip(fo_a, fe_a))
nu6 = len(fo_a) - 1 - 1
ejercicio("N6",
          "En una central de emergencias se contó la cantidad de llamadas recibidas en 100 intervalos de un minuto "
          "elegidos al azar:",
          [["a", "¿Es razonable suponer que la cantidad de llamadas por minuto se distribuye según la ley de Poisson? "
                 "Tomar α = 0,05."]],
          [[["d", "rechaza" if chi6 > stats.chi2.ppf(0.95, nu6) else "no_rechaza"]]],
          tablas=[{"titulo": "", "columnas": ["Llamadas por minuto", "Cantidad de intervalos"],
                   "filas": [["0", 18], ["1", 34], ["2", 30], ["3", 12], ["4", 4], ["5 o más", 2]]}],
          nota=f"λ = {r4(lam)}; χ² = {r4(chi6)} (amalgamado {len(fo_a)} clases), ν = {nu6}")

# ---------------------------------------------------------------- N7: regresión, predicción individual y ensayo de β1

x7 = [120, 140, 160, 180, 200, 220, 240, 260]
y7 = [0.21, 0.26, 0.30, 0.37, 0.40, 0.47, 0.50, 0.58]
g = regresion(x7, y7)
t975, t95 = stats.t.ppf(0.975, g["n"] - 2), stats.t.ppf(0.95, g["n"] - 2)
y0 = g["b0"] + g["b1"] * 210
ep = t975 * g["s"] * sqrt(1 + 1 / g["n"] + (210 - g["mx"]) ** 2 / g["sxx"])
b1c = 0.0015 + t95 * g["sb1"]
ejercicio("N7",
          "Un ingeniero de producción sospecha que la velocidad de corte (en m/min) influye en el desgaste del filo de la "
          "herramienta (en mm) al cabo de una jornada. Registró los siguientes valores:",
          [["a", "Ajustar el modelo lineal, interpretar los coeficientes en términos del problema y decidir si el "
                 "modelo es válido."],
           ["b", "Si mañana se trabaja una jornada a 210 m/min, ¿entre qué valores se espera el desgaste de esa "
                 "herramienta? (95% de confianza)"],
           ["c", "¿Se puede afirmar, al 5%, que por cada m/min adicional el desgaste aumenta en más de 0,0015 mm?"]],
          [[["n", r4(g["b1"])], ["n", r4(g["r2"])]], [["n", r4(y0 - ep)], ["n", r4(y0 + ep)]],
           [["d", "rechaza" if g["b1"] > b1c else "no_rechaza"]]],
          tablas=[{"titulo": "", "columnas": ["Velocidad de corte (m/min)", "Desgaste (mm)"],
                   "filas": [[x, y] for x, y in zip(x7, y7)], "variable_y": "Desgaste (mm)"}],
          nota=f"b1 = {r4(g['b1'])}, r² = {r4(g['r2'])}; b) predicción individual; c) b1c = {r4(b1c)}")

# ---------------------------------------------------------------- N8: diseño de un plan sobre p con α y β en palabras

n8, rc8 = plan_binomial(0.03, 0.10, 0.05, 0.10)
ejercicio("N8",
          "Un comprador recibe lotes grandes de conectores. Un lote con a lo sumo un 3% de conectores defectuosos se "
          "considera bueno. El comprador quiere que un lote bueno, con un 3% de defectuosos, sea rechazado como mucho el "
          "5% de las veces, y que un lote con un 10% de defectuosos sea rechazado por lo menos el 90% de las veces.",
          [["a", "Diseñar el plan de muestreo: tamaño de la muestra, condición de rechazo y regla de decisión."]],
          [[["alguno", [n8]], ["alguno", [rc8]]]],
          nota=f"optimista: H0 p ≤ 0,03, α = 0,05, β = 0,10 en p = 0,10 → n = {n8}, r_c = {rc8}")

# ---------------------------------------------------------------- N9: dos medias con datos crudos, «seca más rápido» (cola izquierda)

nueva = [42, 45, 39, 41, 44, 40, 43, 38, 41, 42]
vieja = [48, 55, 44, 51, 58, 46, 53, 49, 60, 47]
mN, sN9, nN9 = media_s(nueva)
mV, sV9, nV9 = media_s(vieja)
se9, nu9 = error_dos_medias(sV9, nV9, sN9, nN9)
dc9 = stats.t.ppf(0.95, nu9) * se9
ejercicio("N9",
          "Un fabricante de pinturas desarrolló una fórmula nueva y quiere saber si seca más rápido que la actual. Se "
          "midió el tiempo de secado (en minutos) en paneles elegidos al azar:\n"
          "Fórmula nueva: 42 - 45 - 39 - 41 - 44 - 40 - 43 - 38 - 41 - 42\n"
          "Fórmula actual: 48 - 55 - 44 - 51 - 58 - 46 - 53 - 49 - 60 - 47",
          [["a", "Con un riesgo del 5%, ¿se puede sostener que la fórmula nueva seca más rápido?"],
           ["b", "Estimar con un 95% de confianza la diferencia entre los tiempos medios de secado de ambas fórmulas."]],
          [[["d", "rechaza" if (mV - mN) > dc9 else "no_rechaza"]],
           [["n", r4(mV - mN - stats.t.ppf(0.975, nu9) * se9)], ["n", r4(mV - mN + stats.t.ppf(0.975, nu9) * se9)]]],
          nota=f"Welch si el F aux rechaza: ν = {nu9}; d = {r4(mV - mN)} vs {r4(dc9)}")

# ---------------------------------------------------------------- N10: p de control (optimista), el dato en porcentaje

n10 = 400
r10 = round(0.0625 * n10)        # «un 6,25% de las piezas»
rc10 = rc_binomial(n10, 0.04, 0.01)
ejercicio("N10",
          "La especificación de un proceso de inyección admite como máximo un 4% de piezas con rebabas. En el último "
          "control se revisaron 400 piezas y un 6,25% de ellas presentó rebabas.",
          [["a", "Con un riesgo del 1%, ¿debe detenerse el proceso para ajustarlo?"],
           ["b", "Estimar, con un 99% de confianza, el porcentaje de piezas con rebabas que está produciendo el proceso."]],
          [[["d", "rechaza" if r10 >= rc10 else "no_rechaza"], ["n", rc10]],
           [["n", r4(ic_exacto(r10, n10, 0.01)[0])], ["n", r4(ic_exacto(r10, n10, 0.01)[1])]]],
          nota=f"optimista: H0 p ≤ 0,04; r = {r10}, r_c = {rc10}")


# ================================================================ TANDA 2 (16/11/2026): escrita sin mirar cómo
# salió la primera en la app. Variantes que la tanda 1 no tenía: refutar al proveedor + cota superior unilateral,
# plan sobre p hacia abajo y β en otro p, dos varianzas con datos crudos y cociente de DESVÍOS, diferencia mínima
# en unidades, apareadas en una tabla, ajuste normal con clases, homogeneidad, proporciones dadas, IC de la media
# en regresión y una reducción porcentual (h < 1).

TANDA = 2

# ---------------------------------------------------------------- S1: p, refutar lo que sostiene el proveedor + cota superior

n, r = 200, 23
rc = rc_binomial(n, 0.08, 0.05)
cota_sup = stats.beta.ppf(0.95, r + 1, n - r)
ejercicio("S1",
          "Un proveedor de envases sostiene que, como mucho, el 8% de sus envases llega con fisuras. Al recibir un "
          "embarque, el área de calidad revisó 200 envases tomados al azar y encontró 23 con fisuras.",
          [["a", "Con α = 0,05, ¿hay motivos para reclamarle al proveedor?"],
           ["b", "Con un 95% de confianza, ¿cuál es, como máximo, la proporción de envases con fisuras del embarque?"]],
          [[["d", "rechaza" if r >= rc else "no_rechaza"], ["n", rc]], [["n", r4(cota_sup)]]],
          nota=f"a) H1 p > 0,08 (reclamar), r_c = {rc}; b) cota superior unilateral B = {r4(cota_sup)}")

# ---------------------------------------------------------------- S2: plan sobre p hacia abajo, β en otro p


def plan_binomial_izq(p0, p1, alpha, beta):
    """Menor n con r_c (se rechaza si R ≤ r_c) que cumple F(r_c | n; p0) ≤ α y P(R > r_c | n; p1) ≤ β (p1 < p0)."""
    for n_ in range(1, 5000):
        rc_ = int(stats.binom.ppf(alpha, n_, p0))
        while rc_ >= 0 and stats.binom.cdf(rc_, n_, p0) > alpha:
            rc_ -= 1
        if rc_ >= 0 and stats.binom.sf(rc_, n_, p1) <= beta:
            return n_, rc_


n2, rc2 = plan_binomial_izq(0.20, 0.10, 0.05, 0.10)
beta2 = stats.binom.sf(rc2, n2, 0.15)
ejercicio("S2",
          "Históricamente, el 20% de los clientes de una financiera paga la cuota con atraso. Se va a probar un sistema "
          "de recordatorios por mensaje y se quiere verificar si logra bajar ese porcentaje. Se acepta un riesgo de 0,05 "
          "de dar por efectivo el sistema cuando en realidad el porcentaje sigue en el 20%, y se quiere una "
          "probabilidad de 0,90 de detectar la mejora si el porcentaje bajara al 10%.",
          [["a", "Plantear las hipótesis, determinar el tamaño de la muestra, la condición de rechazo y la regla de "
                 "decisión."],
           ["b", "Si con el sistema el porcentaje bajara al 15%, ¿qué probabilidad hay de que el plan no lo detecte?"]],
          [[["alguno", [n2]], ["alguno", [rc2]]], [["n", r4(beta2)]]],
          nota=f"H0 p ≥ 0,20, se rechaza si R ≤ r_c: n = {n2}, r_c = {rc2}; β(0,15) = {r4(beta2)}")

# ---------------------------------------------------------------- S3: dos varianzas con datos crudos, cociente de desvíos

manual = [4.92, 5.10, 4.85, 5.15, 5.03, 4.88, 5.12, 4.95]
auto = [5.01, 4.98, 5.03, 4.99, 5.02, 5.00, 4.97, 5.04, 5.01, 4.99]
_, sM, nM = media_s(manual)
_, sA, nA = media_s(auto)
f3 = (sM / sA) ** 2
fc3 = stats.f.ppf(0.99, nM - 1, nA - 1)
lo3 = sqrt(f3 / stats.f.ppf(0.975, nM - 1, nA - 1))
hi3 = sqrt(f3 / stats.f.ppf(0.025, nM - 1, nA - 1))
ejercicio("S3",
          "Se comparan dos métodos de llenado de bidones de 5 litros. Los volúmenes (en litros) obtenidos fueron:\n"
          "Método manual: 4,92 - 5,10 - 4,85 - 5,15 - 5,03 - 4,88 - 5,12 - 4,95\n"
          "Método automático: 5,01 - 4,98 - 5,03 - 4,99 - 5,02 - 5,00 - 4,97 - 5,04 - 5,01 - 4,99\n"
          "El jefe de producción sostiene que el método automático llena con menos variabilidad que el manual.",
          [["a", "Al 1%, ¿tiene razón el jefe de producción?"],
           ["b", "Estimar con un 95% de confianza el cociente entre los desvíos estándar del método manual y del "
                 "automático."]],
          [[["d", "rechaza" if f3 > fc3 else "no_rechaza"]], [["n", r4(lo3)], ["n", r4(hi3)]]],
          nota=f"H1 σM > σA: F = {r4(f3)} vs {r4(fc3)}; IC de σM/σA = raíz del IC del cociente de varianzas")

# ---------------------------------------------------------------- S4: dos medias, diferencia mínima en unidades

xA, sA4, nA4 = 184, 9.5, 12
xN, sN4, nN4 = 196, 11, 15
se4, nu4 = error_dos_medias(sN4, nN4, sA4, nA4)
dc4 = 5 + stats.t.ppf(0.95, nu4) * se4
ejercicio("S4",
          "Una planta evalúa reemplazar su línea de envasado. En 12 turnos con la línea actual se envasaron en promedio "
          "184 cajas por hora, con un desvío de 9,5 cajas. En 15 turnos con una línea de prueba, el promedio fue de 196 "
          "cajas por hora, con un desvío de 11 cajas. La línea nueva solo se compra si envasa, en promedio, más de 5 "
          "cajas por hora más que la actual.",
          [["a", "Con un 5% de riesgo, ¿conviene comprar la línea nueva?"],
           ["b", "Con un 95% de confianza, ¿cuál es el aumento mínimo garantizado de la producción media por hora?"]],
          [[["d", "rechaza" if xN - xA > dc4 else "no_rechaza"]],
           [["n", r4(xN - xA - stats.t.ppf(0.95, nu4) * se4)]]],
          nota=f"H1 μN − μA > 5; ν = {nu4}; d = 12 vs d_c = {r4(dc4)}")

# ---------------------------------------------------------------- S5: apareadas en una tabla, IC bilateral

previa = [52.3, 48.1, 61.0, 45.7, 55.2, 50.8, 58.4, 47.9, 53.6, 49.2]
post = [55.1, 49.0, 64.2, 47.5, 56.0, 53.9, 59.1, 50.3, 55.0, 48.8]
d5 = [b_ - a_ for a_, b_ in zip(previa, post)]
dm5, sd5, n5 = media_s(d5)
t5 = stats.t.ppf(0.95, n5 - 1)
ejercicio("S5",
          "Para medir el efecto de una campaña publicitaria, se registraron las ventas semanales (en miles de pesos) de "
          "10 sucursales en la semana previa y en la semana posterior a la campaña:",
          [["a", "Al 5%, ¿aumentaron las ventas medias con la campaña?"],
           ["b", "Estimar con un 90% de confianza el aumento medio de las ventas semanales por sucursal."]],
          [[["d", "rechaza" if dm5 > t5 * sd5 / sqrt(n5) else "no_rechaza"]],
           [["n", r4(dm5 - t5 * sd5 / sqrt(n5))], ["n", r4(dm5 + t5 * sd5 / sqrt(n5))]]],
          tablas=[{"titulo": "", "columnas": ["Sucursal", "Semana previa", "Semana posterior"],
                   "filas": [[i + 1, a_, b_] for i, (a_, b_) in enumerate(zip(previa, post))]}],
          nota=f"apareadas: d̄ = {r4(dm5)}, S_d = {r4(sd5)}")

# ---------------------------------------------------------------- S6: ajuste normal con clases (dominio completo)

lim6 = [19.0, 19.4, 19.8, 20.2, 20.6, 21.0, 21.4, 21.8]
fo6b = [4, 17, 21, 36, 19, 17, 6]
N6b = sum(fo6b)
marcas = [(a_ + b_) / 2 for a_, b_ in zip(lim6, lim6[1:])]
m6 = sum(x * f for x, f in zip(marcas, fo6b)) / N6b
s6 = sqrt(sum(f * (x - m6) ** 2 for x, f in zip(marcas, fo6b)) / (N6b - 1))
cortes = [-float("inf")] + lim6 + [float("inf")]
fo_c = [0] + fo6b + [0]
fe_c = [N6b * (stats.norm.cdf(b_, m6, s6) - stats.norm.cdf(a_, m6, s6)) for a_, b_ in zip(cortes, cortes[1:])]
while fe_c[0] < 5:
    fo_c[:2], fe_c[:2] = [fo_c[0] + fo_c[1]], [fe_c[0] + fe_c[1]]
while fe_c[-1] < 5:
    fo_c[-2:], fe_c[-2:] = [fo_c[-2] + fo_c[-1]], [fe_c[-2] + fe_c[-1]]
chi6b = sum((o - e) ** 2 / e for o, e in zip(fo_c, fe_c))
nu6b = len(fo_c) - 1 - 2
ejercicio("S6",
          "Se midió el diámetro (en mm) de 120 ejes torneados en un centro de mecanizado. Los resultados se agruparon "
          "así:",
          [["a", "¿Puede admitirse, con un riesgo del 5%, que el diámetro de los ejes tiene distribución normal?"]],
          [[["d", "rechaza" if chi6b > stats.chi2.ppf(0.95, nu6b) else "no_rechaza"], ["n", r4(chi6b)]]],
          tablas=[{"titulo": "", "columnas": ["Diámetro (mm)", "Cantidad de ejes"],
                   "filas": [[f"{a_:.1f}-{b_:.1f}".replace(".", ","), f]
                             for a_, b_, f in zip(lim6, lim6[1:], fo6b)]}],
          nota=f"x̄ = {r4(m6)}, S = {r4(s6)}; {len(fo_c)} clases efectivas, ν = {nu6b}; χ² = {r4(chi6b)}")

# ---------------------------------------------------------------- S7: homogeneidad (consistencia) entre sucursales

tabla7 = [[60, 85, 55], [45, 70, 35], [30, 50, 70]]
chi7, nu7 = chi_contingencia(tabla7)
ejercicio("S7",
          "Un banco registró el medio de pago que usaron muestras de clientes de tres sucursales:",
          [["a", "Con un 1% de riesgo, ¿se puede afirmar que los porcentajes de uso de cada medio de pago son los mismos "
                 "en las tres sucursales?"]],
          [[["n", r4(chi7)], ["d", "rechaza" if chi7 > stats.chi2.ppf(0.99, nu7) else "no_rechaza"]]],
          tablas=[{"titulo": "", "columnas": ["Sucursal", "Efectivo", "Débito", "Crédito"],
                   "filas": [["Centro", 60, 85, 55], ["Norte", 45, 70, 35], ["Sur", 30, 50, 70]]}],
          nota=f"consistencia: χ² = {r4(chi7)}, ν = {nu7}")

# ---------------------------------------------------------------- S8: ajuste a proporciones dadas por un plan

fo8, p8 = [228, 104, 68], [0.50, 0.30, 0.20]
chi8 = sum((o - 400 * p) ** 2 / (400 * p) for o, p in zip(fo8, p8))
ejercicio("S8",
          "Según el plan comercial de una empresa de internet, el 50% de las ventas debería corresponder al plan básico, "
          "el 30% al plan estándar y el 20% al plan premium. En el último mes se registraron 400 ventas: 228 del plan "
          "básico, 104 del estándar y 68 del premium.",
          [["a", "Con α = 0,05, ¿se está cumpliendo el plan comercial?"]],
          [[["n", r4(chi8)], ["d", "rechaza" if chi8 > stats.chi2.ppf(0.95, 2) else "no_rechaza"]]],
          nota=f"proporciones dadas, ν = 2: χ² = {r4(chi8)}")

# ---------------------------------------------------------------- S9: regresión (econometría), IC de la media

x9 = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
y9 = [2.1, 2.6, 2.9, 3.6, 3.8, 4.5, 4.6, 5.3, 5.5, 6.2]
g9 = regresion(x9, y9)
y09 = g9["b0"] + g9["b1"] * 32
em9 = stats.t.ppf(0.975, g9["n"] - 2) * g9["s"] * sqrt(1 / g9["n"] + (32 - g9["mx"]) ** 2 / g9["sxx"])
ejercicio("S9",
          "Una cadena de electrodomésticos quiere saber si la inversión mensual en publicidad (en miles de pesos) "
          "explica las ventas del mes (en millones de pesos). Se tienen los datos de 10 meses:",
          [["a", "Estimar la recta de regresión, interpretar la pendiente y el coeficiente de determinación, y decidir "
                 "al 5% si el modelo es válido."],
           ["b", "Estimar con un 95% de confianza las ventas medias de los meses en que se inviertan 32 mil pesos en "
                 "publicidad."]],
          [[["n", r4(g9["b1"])], ["n", r4(g9["r2"])]], [["n", r4(y09 - em9)], ["n", r4(y09 + em9)]]],
          tablas=[{"titulo": "", "columnas": ["Publicidad (miles de $)", "Ventas (millones de $)"],
                   "filas": [[x, y] for x, y in zip(x9, y9)], "variable_y": "Ventas (millones de $)"}],
          nota=f"b1 = {r4(g9['b1'])}, r² = {r4(g9['r2'])}; b) IC de la media en x = 32")

# ---------------------------------------------------------------- S10: dos medias, reducción porcentual (h < 1)

xS, sS10, nS10 = 32.5, 2.1, 14
xC, sC10, nC10 = 28.9, 1.8, 16
se10, nu10 = error_dos_medias(sC10, nC10, sS10, nS10, 0.95)
dstar10 = xC - 0.95 * xS


def h_max(alpha):
    """Mayor h con x̄C − h·x̄S ≤ −t(1−α)·error(h): μC ≤ h·μS con confianza 1 − α."""
    def g(h):
        e, v = error_dos_medias(sC10, nC10, sS10, nS10, h)
        return xC - h * xS + stats.t.ppf(1 - alpha, v) * e
    return brentq(g, xC / xS, 1.0)


h10 = h_max(0.05)
ejercicio("S10",
          "Una empresa de transporte probó un aditivo para combustible. 14 camiones sin aditivo consumieron en promedio "
          "32,5 litros cada 100 km, con un desvío de 2,1 litros, y 16 camiones con aditivo consumieron en promedio 28,9 "
          "litros cada 100 km, con un desvío de 1,8 litros. El fabricante del aditivo afirma que reduce el consumo medio "
          "en más de un 5%.",
          [["a", "Con α = 0,05, ¿se puede aceptar la afirmación del fabricante?"],
           ["b", "Con un 95% de confianza, ¿cuál es la reducción porcentual mínima del consumo medio que se puede "
                 "garantizar?"]],
          [[["d", "rechaza" if dstar10 < -stats.t.ppf(0.95, nu10) * se10 else "no_rechaza"]],
           [["alguno", [r4(h10), r4(1 - h10), round(100 * (1 - h10), 2)]]]],
          nota=f"H1 μC < 0,95·μS; d* = {r4(dstar10)} vs −{r4(stats.t.ppf(0.95, nu10) * se10)} (ν = {nu10}); "
               f"b) h máx = {r4(h10)} (reducción {r4(1 - h10)})")


if __name__ == "__main__":
    for archivo, _, lista in TANDAS.values():
        salida = RAIZ / "datos" / archivo
        salida.write_text(json.dumps(lista, ensure_ascii=False, indent=1), encoding="utf-8")
        for e in lista:
            print(e["id"], "|", e["nota"], "|", e["esperado"])
        print(f"\n{len(lista)} ejercicios → {salida}\n")
