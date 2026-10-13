"""Patrones del intérprete para los TEMAS I (media), II (varianza) y III (proporción).

Cada test usa una redacción DISTINTA a la de la guía (otros números, otro orden, otras palabras) para
comprobar que la regla es general y no está atada a un ejercicio puntual.
"""

import pytest

from interprete.analizador import analizar
from interprete.resolver import resolver


def _una(planteo, incisos):
    an = analizar(planteo, incisos)
    return an, resolver(an)


# ---------------------------------------------------------------------------
# α: la palabra 'riesgo' pertenece al número que la sigue, no al anterior
# ---------------------------------------------------------------------------

def test_riesgo_pertenece_al_numero_siguiente():
    an, (a, b) = _una(
        "Una máquina corta varillas. Se midieron 10 varillas: 5,2 – 5,4 – 5,1 – 5,6 – 5,3 – 5,5 – 5,2 – 5,4 – 5,3 – 5,6.",
        ["Estimar la varianza con un 95% de confianza.",
         "Si no se tolera una varianza superior a 0,04 cm², con un riesgo del 1%, ¿hay motivo de preocupación?"])
    assert an.incisos[1].params["alpha"] == pytest.approx(0.01)
    assert an.incisos[1].params["sigma0"] == pytest.approx(0.2)


def test_reducir_el_error_a_no_es_alfa():
    an, res = _una("Se pesaron 16 paquetes y dieron una media de 502 g con un desvío de 8 g.",
                   ["Estimar el peso medio con un 95% de confianza.",
                    "¿Cuántos paquetes más hacen falta para bajar el error a 0,4 g?"])
    assert an.datos["xbar"] == 502                                     # 'dieron una media de' es dato muestral
    assert an.incisos[1].params.get("e") == pytest.approx(0.4)
    assert an.incisos[1].params["alpha"] == pytest.approx(0.05)         # el 0,4 no se tomó como α
    assert res[1].numeros[0] > 1500


# ---------------------------------------------------------------------------
# TEMA II: χ² equivalente, R' y doble condición expresada como especificación máxima
# ---------------------------------------------------------------------------

def test_ensayo_varianza_informa_chi2_calculado_y_de_tabla():
    an, (a,) = _una("El desvío del llenado no debe superar los 4 ml. Una muestra de 13 envases arrojó un desvío de 5 ml.",
                    ["¿Hay que ajustar la máquina? Riesgo del 5%."])
    assert pytest.approx(12 * 25 / 16, abs=1e-4) in a.numeros          # χ²calc = 18,75
    assert pytest.approx(21.0261, abs=1e-3) in a.numeros               # χ²(0,95; 12)


def test_doble_condicion_como_especificacion_maxima():
    an, (a, b) = _una(
        "La resistencia promedio máxima admitida es de 30 N con una desviación máxima de 2 N. Se ensayaron 8 probetas: "
        "31 – 33 – 30 – 34 – 29 – 35 – 32 – 33.",
        ["Con un riesgo del 5%, ¿se cumplen las especificaciones?",
         "Estimar la resistencia media y el desvío con un 95% de confianza."])
    assert an.datos["doble"] and (an.datos["tail_mu"], an.datos["tail_sigma"]) == ("derecha", "derecha")
    assert "μ ≤ 30" in a.resumen and "σ² ≤ 4" in a.resumen
    assert an.incisos[1].params.get("ambos")


# ---------------------------------------------------------------------------
# TEMA I: datos agrupados, escala 'en miles', ensayos repetidos, μ₁ que surge de β
# ---------------------------------------------------------------------------

def test_tabla_de_frecuencias_aplanada_con_barras():
    an, (a,) = _una("Se relevaron comercios de un barrio. Se sabe que el desvío es de 1 empleado. "
                    "Cantidad de empleados | Cantidad de comercios: 1 | 3; 2 | 5; 3 | 8; 4 | 4.",
                    ["Estimar con un 95% de confianza la cantidad media de empleados."])
    assert len(an.datos["datos"]) == 20
    assert a.numeros[0] + a.numeros[2] == pytest.approx(2.65, abs=1e-3)


def test_tabla_estructurada_por_intervalos():
    tablas = [{"columnas": ["Peso desde", "Peso hasta", "Frecuencia"], "filas": [[10, 12, 2], [12, 14, 6], [14, 16, 2]]}]
    an = analizar("Los pesos de una muestra de cajas se agruparon en la tabla. El desvío del proceso es 1,5 kg.",
                  ["Estimar el peso medio con un 90% de confianza."], tablas=tablas)
    assert sorted(set(an.datos["datos"])) == [11, 13, 15] and len(an.datos["datos"]) == 10


def test_datos_en_miles_se_informan_en_unidades():
    an, (a,) = _una("La producción diaria (en miles de unidades) de 5 días fue: 10,2 – 11,4 – 9,8 – 10,6 – 11,0.",
                    ["Estimar la producción media diaria con un 95% de confianza."])
    assert an.datos["escala"] == 1000
    assert a.numeros[3] == pytest.approx(a.numeros[0] * 1000)


def test_ensayo_repetido_al_menos_una_detecta():
    an, (a, b) = _una(
        "El peso de los envases es una variable con desvío de 4 g. Se controla con muestras de 16 envases, con un "
        "riesgo del 5%, que la media no supere los 500 g.",
        ["¿Cuál es la probabilidad de detectar que la media aumentó a 502 g?",
         "Si se hicieran tres controles independientes de 16 envases y la media fuera 502 g, ¿cuál es la probabilidad "
         "de que al menos uno de ellos lo detecte?"])
    pot = a.numeros[0]
    assert b.numeros[0] == pytest.approx(1 - (1 - pot) ** 3, abs=1e-6)


def test_media_alternativa_que_surge_de_beta_con_n_fijo():
    an, (a,) = _una(
        "En la recepción de rollos se toma una muestra de 25 rollos; la longitud media de cada partida debe ser por lo "
        "menos 100 m y se sabe que el desvío es 5 m. El proveedor admite un riesgo del 5% de que le devuelvan una "
        "partida buena y el comprador quiere rechazar el 90% de las partidas malas.",
        ["¿Cuál es la longitud media de las partidas consideradas malas?"])
    xc = 100 - 1.6449 * 1
    assert pytest.approx(xc, abs=1e-3) in a.numeros
    assert pytest.approx(xc - 1.2816, abs=1e-3) in a.numeros


# ---------------------------------------------------------------------------
# Diseño: α y β según la CONDICIÓN de cada probabilidad, no el orden
# ---------------------------------------------------------------------------

def test_alpha_beta_por_condicion_con_orden_invertido():
    an = analizar(
        "Se evalúa un nuevo proceso más caro. El rendimiento medio actual es 50 kg con un desvío de 6 kg. Si con el "
        "nuevo proceso el rendimiento sube a 54 kg se quiere una probabilidad de 0,95 de adoptarlo, pero si no "
        "hubiera mejora alguna la probabilidad de adoptarlo debe ser 0,02.",
        ["Indicar la hipótesis nula, el tamaño de muestra y la regla de decisión."])
    assert an.datos["alpha"] == pytest.approx(0.02) and an.datos["beta"] == pytest.approx(0.05)
    assert (an.datos["mu0"], an.datos["mu1"]) == (50, 54)


def test_riesgo_de_la_misma_accion_es_potencia():
    """'riesgo del 20% de lanzarlo si es un 5% mejor' es P(lanzar | μ₁) = potencia, no β."""
    an = analizar(
        "La duración media actual de un producto es de 400 horas con un desvío de 40 horas. Se acepta un riesgo del "
        "20% de lanzar el producto nuevo en caso de que su duración sea un 5% superior a la actual. La probabilidad "
        "de lanzarlo si la duración no aumentó debe ser como máximo 0,05.",
        ["Indicar la hipótesis nula, la condición de rechazo y la regla de decisión."])
    assert an.datos["alpha"] == pytest.approx(0.05) and an.datos["beta"] == pytest.approx(0.80)
    assert an.datos["mu1"] == pytest.approx(420)


def test_dos_alternativas_se_resuelven_por_separado():
    an, (a,) = _una(
        "Un proveedor asegura que la resistencia media de sus cables supera los 200 kg. Alternativa 1: fijar en 0,05 la "
        "probabilidad de rechazar la oferta cuando la resistencia supera los 200 kg, y en 0,10 la probabilidad de "
        "aceptarla si es de 190 kg. Alternativa 2: fijar en 0,05 la probabilidad de aceptar la oferta si la "
        "resistencia no supera los 200 kg, y en 0,90 la probabilidad de aceptarla si es de 210 kg. "
        "La resistencia tiene un desvío de 20 kg.",
        ["Para cada alternativa indicar la hipótesis nula y la regla de decisión."])
    alts = an.incisos[0].params["alternativas"]
    assert [x["mu1"] for x in alts] == [190, 210]
    assert "Alternativa 1" in a.resumen and "Alternativa 2" in a.resumen


def test_limites_de_control_sin_muestra_y_n_por_jornada():
    an, (a, b) = _una(
        "El tiempo estándar para armar una pieza es de 120 segundos con un desvío de 30 segundos.",
        ["¿Entre qué límites variará el tiempo medio durante un turno de 4 horas? (riesgo del 5%)",
         "¿Cuál es el error de tipo II si el tiempo medio real es 10% superior y las muestras son de 30 piezas?"])
    assert an.incisos[0].tipo == "diseno" and an.incisos[0].params["n"] == 120
    assert a.numeros[:2] == [pytest.approx(120 - 1.96 * 30 / 120 ** 0.5, abs=1e-2),
                             pytest.approx(120 + 1.96 * 30 / 120 ** 0.5, abs=1e-2)]
    assert an.incisos[1].params["n"] == 30 and an.incisos[1].params["tail"] == "bilateral"


def test_costo_fijo_y_comision_se_descuentan_de_la_media():
    an, (a, b) = _una(
        "Las ventas mensuales de un local son variables con una media de 50.000 $ y un desvío de 6.000 $. Una agencia "
        "de publicidad logra en los primeros 9 meses una media de 56.000 $ y cobra 3.000 $ por sus servicios.",
        ["Con un riesgo del 5%, ¿conviene seguir con la agencia?",
         "¿Cuál sería la respuesta a la pregunta a) si la agencia cobrara una comisión del 4% de las ventas?"])
    xc = 50000 + 1.6449 * 2000
    assert a.numeros[:2] == [pytest.approx(xc, abs=1), pytest.approx(xc + 3000, abs=1)]
    assert "NO rechaza" in a.resumen                                    # neto 53.000 < 53.290
    assert pytest.approx(xc / 0.96, abs=1) in b.numeros and "NO rechaza" not in b.resumen   # neto 53.760


# ---------------------------------------------------------------------------
# TEMA III: planes de muestreo
# ---------------------------------------------------------------------------

def test_plan_de_muestreo_con_aproximacion_normal():
    an, (a,) = _una(
        "Se quiere cambiar un insumo si baja el porcentaje de fallados, que hoy es del 10%. Si con el nuevo insumo "
        "el porcentaje baja al 6%, la probabilidad de cambiar debe ser 0,95; pero si no baja, la probabilidad de "
        "cambiar debe valer 0,05.",
        ["Indicar la hipótesis nula, el tamaño de muestra y la regla de decisión."])
    assert (an.datos["p0"], an.datos["p1"]) == (0.10, 0.06)
    assert (an.datos["alpha"], an.datos["beta"]) == (0.05, 0.05)
    n_normal = int(((1.6449 * (0.09 ** 0.5) + 1.6449 * (0.0564 ** 0.5)) / 0.04) ** 2) + 1
    assert a.numeros[2] == n_normal


def test_equilibrio_economico_es_beta_un_medio():
    an = analizar("El proceso actual tiene un 8% de defectuosas. Con una máquina nueva el equilibrio económico se "
                  "logra para un 5% de defectuosas. No se quiere más de 0,05 de probabilidad de comprar la máquina si "
                  "el porcentaje no cambia.", ["Establecer la hipótesis nula, el tamaño de muestra y la regla de decisión."])
    assert an.datos["beta"] == 0.5 and an.datos["p1"] == pytest.approx(0.05) and an.datos["p0"] == pytest.approx(0.08)


def test_plan_dado_con_numero_en_palabras():
    from scipy import stats
    an, (a,) = _una("Se supone un 3% de piezas defectuosas. Se toman muestras de 60 piezas y la máquina se detiene si "
                    "aparecen cuatro o más defectuosas.",
                    ["Si en realidad el porcentaje de defectuosas es del 6%, ¿cuál es la probabilidad de detenerla?"])
    assert an.datos["rc"] == 4
    assert a.numeros[0] == pytest.approx(stats.binom.sf(3, 60, 0.06), abs=1e-6)


def test_numero_de_aceptacion_y_riesgos_del_plan():
    from scipy import stats
    an, (a, b) = _una(
        "Un lote se acepta si en una muestra de 50 unidades hay 1 o menos defectuosas. El contrato admite un 2% de "
        "defectuosas y el comprador corre un riesgo del 10% de aceptar un lote malo.",
        ["Indicar la hipótesis nula y calcular el riesgo del proveedor.",
         "¿Cuál es el porcentaje defectuoso de los lotes considerados malos?"])
    assert an.datos["rc"] == 2 and an.datos["beta"] == pytest.approx(0.10)
    assert a.numeros[0] == pytest.approx(stats.binom.sf(1, 50, 0.02), abs=1e-6)
    assert stats.binom.cdf(1, 50, b.numeros[-1]) == pytest.approx(0.10, abs=1e-6)


def test_aql_ltpd_con_respectivamente_en_otro_orden():
    from scipy import stats
    an, (a,) = _una("Para el plan de muestreo: n = 20 y rc = 2.",
                    ["Calcular el AQL y el LTPD para riesgos del consumidor y del proveedor de 10% y 5% respectivamente."])
    aql, ltpd = a.numeros[:2]
    assert stats.binom.sf(1, 20, aql) == pytest.approx(0.05, abs=1e-6)
    assert stats.binom.cdf(1, 20, ltpd) == pytest.approx(0.10, abs=1e-6)


def test_inversion_adicional_por_costo_unitario():
    an, (a, b) = _una("Una encuesta a 400 personas dio que el 30% prefiere la marca.",
                      ["Estimar el porcentaje con un 95% de confianza.",
                       "Si cada encuesta cuesta 15 $, ¿cuál es el costo adicional para estimar con un error de ± 2%?"])
    n = b.numeros[0]
    assert b.numeros[1] == n - 400 and b.numeros[-1] == pytest.approx((n - 400) * 15)


def test_p0_en_una_nota_y_alternativa_como_probabilidad():
    an, (a, b) = _una(
        "Un apostador sospecha que una moneda está adulterada porque sale cara con frecuencia excesiva. Se registraron "
        "400 tiradas y salió cara 225 veces.",
        ["¿Tiene fundamento la sospecha? (riesgo del 5%)",
         "Si la cara tuviera una probabilidad de 0,6, ¿cuál sería con ese tamaño de muestra la probabilidad de "
         "detectarlo? (Nota: en una moneda equilibrada la probabilidad de cara es 0,5)."])
    assert an.datos["p0"] == pytest.approx(0.5) and an.datos["r"] == 225
    assert an.incisos[0].params["tail"] == "derecha" and an.incisos[1].params["p1"] == pytest.approx(0.6)
    assert "RECHAZA" in a.resumen and b.numeros[0] > 0.9


def test_reducir_error_y_relacion_de_la_estimacion_de_una_proporcion():
    an, res = _una("De 40 piezas revisadas, se encontraron 30 piezas aptas.",
                   ["Estimar con un 95% de confianza el porcentaje de piezas aptas.",
                    "¿Cuántas piezas habría que revisar para reducir en un 40% el error de la estimación anterior?",
                    "¿Cuántas piezas habría que revisar para reducir en un 20% la relación de la estimación anterior?"])
    a, b, c = res
    e_act = (a.numeros[1] - a.numeros[0]) / 2
    assert pytest.approx(e_act, abs=1e-6) in b.numeros and pytest.approx(e_act * 0.6, abs=1e-6) in b.numeros
    assert pytest.approx(a.numeros[1] / a.numeros[0] * 0.8, abs=1e-6) in c.numeros
