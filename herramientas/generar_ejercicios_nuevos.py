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


EJ = []


def ejercicio(ident, planteo, incisos, esperado, tablas=None, nota=""):
    EJ.append(dict(id=ident, examen="Ejercicio nuevo (Claude, 15/11/2026)", planteo=planteo,
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


if __name__ == "__main__":
    salida = RAIZ / "datos" / "ejercicios_nuevos.json"
    salida.write_text(json.dumps(EJ, ensure_ascii=False, indent=1), encoding="utf-8")
    for e in EJ:
        print(e["id"], "|", e["nota"], "|", e["esperado"])
    print(f"\n{len(EJ)} ejercicios → {salida}")
