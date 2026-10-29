"""TEMAS IV y V: lectura de dos muestras (tablas, resúmenes, apareadas) y comparación de medias.

Cada patrón se prueba con redacciones distintas de las de la guía (mismos números o números nuevos)."""

import pytest

from interprete.analizador import analizar
from interprete.dos_tablas import grupos_de_tabla, tablas_de_texto
from interprete.resolver import resolver
from solver import two_samples as two


def _num(res, valor, tol=1e-3):
    return any(x is not None and abs(x - valor) <= tol for x in res.numeros)


# ---------------------------------------------------------------------------
# Tablas → grupos
# ---------------------------------------------------------------------------

def test_tabla_resumen_estadisticos_por_fila_y_por_columna():
    por_fila = {"columnas": ["", "Planta Norte", "Planta Sur"],
                "filas": [["Tamaño: n =", 30, 25], ["Promedio: x̄ =", "10,2 kg", "11 kg"], ["Desvío: S =", "2 kg", "3 kg"]]}
    g = grupos_de_tabla(por_fila)
    assert g.nombres == ["Planta Norte", "Planta Sur"]
    assert g.resumen == {"n": [30, 25], "xbar": [10.2, 11], "s": [2, 3]}
    por_col = {"columnas": ["Grupo", "n", "Media", "Desviación estándar"],
               "filas": [["Turno mañana", 12, 40.1, 3.2], ["Turno tarde", 15, 38.0, 2.9]]}
    g = grupos_de_tabla(por_col)
    assert g.nombres == ["Turno mañana", "Turno tarde"] and g.resumen["s"] == [3.2, 2.9]


def test_tabla_columnas_repetidas_se_juntan_y_el_indice_marca_apareadas():
    t = {"columnas": ["Paciente", "Antes", "Después", "Paciente", "Antes", "Después"],
         "filas": [[1, 120, 118, 4, 135, 130], [2, 128, 121, 5, 140, 139], [3, 131, 129, 6, 126, 120]]}
    g = grupos_de_tabla(t)
    assert g.nombres == ["Antes", "Después"] and g.listas[0] == [120, 128, 131, 135, 140, 126]
    assert g.apareadas is True


def test_texto_resumen_con_barras_y_clases_en_una_linea():
    txt = ("Se obtuvo: Sucursal: “Centro” | “Oeste”; Muestra: n = 40 | 36; Media: x̄ = 52,3 min | 49,8 min; "
           "Desvío: S = 6,1 min | 4,2 min.")
    g = grupos_de_tabla(tablas_de_texto(txt)[0])
    assert g.nombres == ["Centro", "Oeste"] and g.resumen["n"] == [40, 36] and g.resumen["s"] == [6.1, 4.2]
    clases = ("Peso (kg): Lote “X” | Peso (kg): Lote “Y”: 10 – 12: 5 | 11 – 13: 4; 12 – 14: 9 | 13 – 15: 10; "
              "14 – 16: 6 | 15 – 17: 6.")
    g = grupos_de_tabla(tablas_de_texto(clases)[0])
    assert g.agrupados and g.resumen["n"] == [20, 20]
    assert g.resumen["xbar"][0] == pytest.approx((11 * 5 + 13 * 9 + 15 * 6) / 20)


def test_texto_renglones_numerados_con_barra():
    txt = ("Se midió cada pieza con los dos calibres (Pieza Nº: Calibre viejo / Calibre nuevo): 1: 10,2 / 10,4; "
           "2: 9,8 / 9,9; 3: 10,5 / 10,9; 4: 10,1 / 10,0.")
    g = grupos_de_tabla(tablas_de_texto(txt)[0])
    assert g.nombres == ["Calibre viejo", "Calibre nuevo"] and g.listas[1] == [10.4, 9.9, 10.9, 10.0]
    assert g.apareadas is True


# ---------------------------------------------------------------------------
# TEMA IV con tabla resumen
# ---------------------------------------------------------------------------

def test_tema_iv_tabla_resumen_por_texto():
    an = analizar("Se compara la regularidad de dos establecimientos lecheros. Resultados: Establecimiento: “El Ombú” | "
                  "“La Esperanza”; Muestra: n = 31 | 31; Media: x̄ = 21 l | 22 l; Desvío: S = 2,5 l | 4 l.",
                  ["¿Se puede asegurar, con 5% de riesgo, que los desvíos difieren?",
                   "Establecer los límites de confianza del 90% para la relación de los desvíos."])
    assert an.tema == "dos_varianzas"
    assert an.datos["nombre1"] == "La Esperanza" and an.datos["s1"] == 4   # arriba el de mayor desvío
    a, b = resolver(an)
    assert "RECHAZA" in a.resumen
    lo, hi = two.ic_ratio_varianzas(4, 31, 2.5, 31, 0.10)[0].a ** 0.5, two.ic_ratio_varianzas(4, 31, 2.5, 31, 0.10)[0].b ** 0.5
    assert _num(b, lo) and _num(b, hi)


def test_tema_iv_n_por_relacion_informa_nu():
    an = analizar("Se tienen dos tornos: S1 = 3,6 con n1 = 13 piezas y S2 = 5,4 con n2 = 25 piezas.",
                  ["Calcular los límites de confianza del 90% para la relación entre las varianzas poblacionales.",
                   "¿Cuál sería el tamaño de muestra en cada torno para reducir la relación entre límites a la mitad?"])
    res = resolver(an)
    assert res[1].numeros[:2] == [45, 44]


# ---------------------------------------------------------------------------
# TEMA V: lectura del planteo
# ---------------------------------------------------------------------------

def test_n_en_palabras_y_con_cada():
    an = analizar("Para evaluar una promoción se registraron las ventas durante los cinco meses que duró la promoción, "
                  "con un promedio de 320 unidades y un desvío de 40 unidades. De los meses anteriores a la promoción "
                  "se tienen los últimos 10 meses, con una media de 290 unidades y un desvío de 35 unidades.",
                  ["¿Se puede asegurar, con 5% de riesgo, que la promoción aumentó las ventas medias?"])
    assert an.tema == "dos_medias" and (an.datos["n1"], an.datos["n2"]) == (5, 10)
    an = analizar("Se sembraron 12 parcelas con cada híbrido. Híbrido viejo: promedio de 30 qq con un desvío de 4 qq; "
                  "híbrido nuevo: promedio de 33 qq con un desvío de 5 qq.",
                  ["¿Se puede asegurar con un riesgo del 5% que el híbrido nuevo rinde más?"])
    assert (an.datos["n1"], an.datos["n2"]) == (12, 12)
    assert an.datos["nombre2"] == "híbrido nuevo"   # rótulo 'Híbrido nuevo: promedio de ...'
    assert an.incisos[0].params["sujeto"] == 2 and an.incisos[0].params["tail"] == "derecha"


def test_se_realizaron_n_ensayos_y_otra_muestra():
    an = analizar("Se realizaron 16 ensayos con el catalizador, con una media de 72 % de conversión... ".replace("72 %", "72")
                  + "y un desvío de 3. Sin el catalizador se realizaron 25 ensayos, con una media de 69 y un desvío de 4.",
                  ["¿Se puede asegurar, con un riesgo del 5%, que el catalizador aumenta la conversión media?"])
    assert (an.datos["n1"], an.datos["n2"]) == (16, 25)
    assert an.incisos[0].params["sujeto"] == 1 and an.incisos[0].params["tail"] == "derecha"


def test_apareadas_por_indicio_del_texto_e_independientes():
    lista = "Método I: 12 15 11 14 13; Método II: 11 14 12 12 12."
    pareada = analizar("A cada operario se le pidió que armara una pieza con ambos métodos. " + lista,
                       ["¿Hay diferencias significativas entre los tiempos medios? (riesgo 5%)"])
    assert pareada.datos["apareadas"] is True
    indep = analizar("Se tomaron muestras de ambos métodos con operarios distintos. " + lista,
                     ["¿Hay diferencias significativas entre los tiempos medios? (riesgo 5%)"])
    assert indep.datos["apareadas"] is False
    # criterio de la cátedra: "¿difieren?" en una comparación → unilateral en el sentido de los datos
    assert indep.incisos[0].params["tail"] == "derecha" and indep.incisos[0].params["bilateral_pregunta"]


# ---------------------------------------------------------------------------
# TEMA V: resolución
# ---------------------------------------------------------------------------

def test_test_f_previo_al_10_por_ciento_decide_welch():
    """Mismos datos que la hiladora (V-3) contados de otra forma: el F previo al 10% rechaza → Welch, ν = 14."""
    an = analizar("Se quiere saber si el nuevo regulador aumenta la producción media por telar. Con el nuevo regulador "
                  "se observaron 4 telares: media 1.470 m, desvío 132 m. Sin el regulador se observaron 16 telares: "
                  "media 1.208 m, desvío 354 m.",
                  ["¿Se puede afirmar con un riesgo del 5% que el regulador aumenta la producción media?",
                   "Calcular los límites de confianza del 90% para la diferencia entre las producciones medias.",
                   "Con igual cantidad de telares en cada grupo, ¿cuántos habría que observar para reducir a la mitad "
                   "el error de estimación anterior?"])
    a, b, c = resolver(an)
    assert "RECHAZA" in a.resumen and "NO" not in a.resumen
    assert _num(a, 2.2804) and _num(a, 14.2641) and _num(a, 14) and _num(a, 194.4494)
    assert _num(b, 67.5506) and _num(b, 456.4494)
    assert c.numeros[:3] == [43, 39, 27]


def test_hipotesis_proporcional_y_porcentaje_minimo():
    an = analizar("Se comparan dos hornos. Horno “A”: 40 hornadas, media 1,50 t, desvío 0,15 t. Horno “B”: 40 hornadas, "
                  "media 1,90 t, desvío 0,16 t.",
                  ["¿Se puede asegurar con un riesgo del 5% que el horno “B” produce como mínimo un 20% más que el “A”?",
                   "¿Qué incremento porcentual mínimo se puede garantizar para el horno “B” con un 5% de riesgo?"])
    a, b = resolver(an)
    r = two.ensayo_dos_medias(1.9, 0.16, 40, 1.5, 0.15, 40, 0.05, "derecha", h=1.2)
    assert an.incisos[0].params["sujeto"] == 2 and an.incisos[0].params["delta0_pct"] == pytest.approx(0.2)
    assert _num(a, r.critical_value) and _num(a, 1.9 - 1.2 * 1.5)
    h = two.h_limite_dos_medias(1.9, 0.16, 40, 1.5, 0.15, 40, 0.05)
    assert _num(b, h) and h > 1.2


def test_sujeto_es_el_grupo_que_afirma_el_inciso():
    an = analizar("Ración “A”: 1,5 – 2,5 – 3,5 – 2,0 – 3,0 – 3,5; Ración “B”: 2,5 – 2,0 – 4,5 – 4,0 – 3,5 – 4,0.",
                  ["Solo se adoptaría la ración “B” si se puede asegurar, con un riesgo del 10%, que con ella el aumento "
                   "medio supera al de la “A” en 0,5 cm al menos. ¿Qué se decide?"])
    p = an.incisos[0].params
    assert p["sujeto"] == 2 and p["tail"] == "derecha" and p["delta0"] == 0.5
    assert "μ(Ración “B”) - μ(Ración “A”) ≤ 0,5" in resolver(an)[0].resumen


def test_minimo_garantizado_para_el_grupo_nombrado():
    an = analizar("Se compararon dos dietas en dos grupos de 15 animales cada uno. Dieta “A”: Promedio (x̄) = 25 kg, "
                  "Desvío std. (S) = 3,4 kg; Dieta “B”: Promedio (x̄) = 26,2 kg, Desvío std. (S) = 2,8 kg.",
                  ["¿Qué diferencia mínima de aumento de peso puede garantizarse para la dieta “B” con 95% de confianza?"])
    assert (an.datos["s1"], an.datos["s2"]) == (3.4, 2.8)
    assert _num(resolver(an)[0], -0.7346)


def test_sigmas_conocidos_z_y_afirmados_verificados():
    conocido = analizar("Se sabe que los desvíos poblacionales son σ1 = 2 g y σ2 = 3 g. Se pesaron 25 frascos de la "
                        "línea 1 con una media de 101 g y 30 frascos de la línea 2 con una media de 99,5 g.",
                        ["¿Difieren los pesos medios de ambas líneas? (riesgo 5%)"])
    assert conocido.datos["sigma_pob1"] == 2 and conocido.datos["sigma_afirmado"] is False
    r = resolver(conocido)[0]
    se = (4 / 25 + 9 / 30) ** 0.5
    # sin bilaterales en comparaciones (profesor en clase): unilateral orientado por los datos, Z(0,95)
    assert _num(r, 1.644854 * se) and "RECHAZA" in r.resumen and "NO" not in r.resumen
    afirmado = analizar("Se cree que ambas llenadoras trabajan con el mismo volumen medio y con desvíos σA = 0,015 cm³ y "
                        "σB = 0,018 cm³. Llenadora “A”: 16,03 – 16,04 – 16,05 – 16,05 – 16,02 – 16,01 – 15,96 – 15,98 – "
                        "16,02 – 15,99; Llenadora “B”: 16,02 – 15,97 – 15,96 – 16,01 – 15,99 – 16,03 – 16,04 – 16,02 – "
                        "16,01 – 16,00.", ["¿Está en lo cierto? (riesgo 5%)"])
    r = resolver(afirmado)[0]
    assert afirmado.datos["sigma_afirmado"] is True and afirmado.incisos[0].params["tail"] == "derecha"  # criterio de la cátedra (V-21)
    assert _num(r, 0.0206) and _num(r, 0.0247) and _num(r, 1.5622) and _num(r, 0.028)


def test_una_media_dentro_de_dos_muestras():
    an = analizar("Durante los seis meses de la campaña se vendió un promedio de 500 unidades con un desvío de 60 "
                  "unidades; en los últimos 12 meses anteriores a la campaña el promedio fue de 450 unidades con un "
                  "desvío de 50 unidades.",
                  ["Alguien sostuvo la hipótesis de que las ventas medias con la campaña eran menores a 460 unidades y "
                   "la rechazó; ¿cuál es la probabilidad de que se haya equivocado?"])
    inc = an.incisos[0]
    assert inc.params["tema"] == "media" and inc.params["mu0"] == 460 and inc.params["n"] == 6
    from scipy import stats
    pv = 1 - stats.t.cdf((500 - 460) / (60 / 6 ** 0.5), 5)
    assert _num(resolver(an)[0], pv, 1e-4)


def test_delta_en_otra_escala_que_los_datos():
    an = analizar("Producción de dos líneas (en miles de litros): Línea “A”: 40 días, media 1,53, desvío 0,15; "
                  "Línea “B”: 40 días, media 1,93, desvío 0,16.",
                  ["¿Se puede asegurar con 5% de riesgo que la línea “B” produce como mínimo 300 litros más que la “A”?"])
    assert an.incisos[0].params["delta0"] == pytest.approx(0.3)


def test_varios_pares_con_y_sin():
    tabla = {"columnas": ["Nº", "Frío Sin aditivo", "Frío Con aditivo", "Calor Sin aditivo", "Calor Con aditivo"],
             "filas": [[1, 5.1, 5.3, 6.0, 6.8], [2, 4.8, 5.0, 6.2, 7.0], [3, 5.5, 5.4, 5.9, 6.9], [4, 5.0, 5.6, 6.1, 7.2]]}
    an = analizar("Se dividió cada muestra en dos partes y a una se le agregó el aditivo.",
                  ["¿Hay diferencias significativas con y sin aditivo en cada condición? (riesgo 5%)"], tablas=[tabla])
    assert len(an.datos["comparaciones"]) == 2 and an.datos["apareadas"] is True
    r = resolver(an)[0]
    assert r.resumen.count("rechaza") + r.resumen.count("RECHAZA") == 2 and "2) RECHAZA" in r.resumen


def test_solver_n_welch_y_z():
    assert two.n_dos_medias_para_error(132, 354, 194.4494 / 2, 0.10, "welch").n == 43
    assert two.n_dos_medias_para_error(1.0, 0.96531, 0.689 / 2, 0.10, "pooled").n == 45
    assert two.n_dos_medias_para_error(2, 3, 1, 0.05, "z").n == 50   # ⌈1,96²·(2² + 3²)/1²⌉ = ⌈49,94⌉
