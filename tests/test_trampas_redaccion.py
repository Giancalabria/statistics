"""Redacciones confusas (estilo del profesor) que las REGLAS tienen que leer bien sin IA.

Cada test usa una redacción DISTINTA a la de los casos trampa con los que se encontró el problema (T-3, T-6, T-7, T-8,
T-11, T-12, S-1, S-3, S-4), para comprobar que el patrón es general y no un parche para un texto.
"""

import pytest

from interprete.analizador import analizar, reescribir_frecuencias
from interprete.resolver import resolver


def _plan(planteo, incisos):
    an = analizar(planteo, incisos)
    return an, resolver(an)


# --- 'en total' / 'sumaron': x̄ = total / n (T-3) ------------------------------------------------------------------

@pytest.mark.parametrize("planteo,n,xbar", [
    ("Se pesaron 20 paquetes elegidos al azar y entre todos sumaron 10.300 g. Por registros históricos el desvío es "
     "de 15 g.", 20, 515),
    ("Se cronometraron 25 operaciones tomadas al azar; el tiempo total de la muestra fue de 1.250 segundos. El desvío "
     "del proceso, por registros históricos, es de 8 segundos.", 25, 50),
    ("Se midieron 16 bolsas y pesaron 8.160 g en total. Se sabe que el desvío es de 20 g.", 16, 510),
])
def test_total_de_la_muestra_se_divide_por_n(planteo, n, xbar):
    an, res = _plan(planteo, ["Estimar la media con 95% de confianza."])
    assert an.datos["n"] == n and an.datos["xbar"] == pytest.approx(xbar)
    assert "mu0" not in an.datos
    assert any("total" in a for a in an.avisos)
    assert not res[0].errores


# --- frecuencias 'N de cada M' / 'por mil' / '‰' (T-7, T-12) --------------------------------------------------------

@pytest.mark.parametrize("texto,pct", [
    ("produce 25 piezas defectuosas por cada mil", "2,5%"),
    ("la proporción histórica de ventas con reclamo es de 12 por mil.", "1,2%"),
    ("uno de cada 40 envases sale mal sellado", "2,5%"),
    ("se equivoca 3 veces de cada 100", "3%"),
    ("una tasa de 4‰ de fallas", "0,4%"),
    ("el 5 por ciento de los casos", "5%"),
])
def test_frecuencias_se_leen_como_porcentaje(texto, pct):
    nuevo, notas = reescribir_frecuencias(texto)
    assert pct in nuevo and (notas or "ciento" in texto)


@pytest.mark.parametrize("texto", [
    "Un alimento contiene 5 g de proteína por cada 100 g de producto.",     # tasa por unidad de medida
    "Se registran 3 fallas cada 100 horas de uso.",
    "Se inspecciona 1 pieza de cada 100 producidas.",                      # frecuencia de muestreo
    "Se toma una muestra de cada 50 envases.",
    "La venta aumenta 3 unidades por cada 1.000 pesos que se invierten en publicidad (regresión).",
])
def test_frecuencias_que_no_son_proporciones_no_se_tocan(texto):
    assert reescribir_frecuencias(texto)[0] == texto


def test_por_mil_es_p0_y_la_mejora_va_en_h1():
    an, res = _plan("La proporción histórica de envíos con reclamo es de 12 por mil. Se cambió el embalaje con la idea "
                    "de reducirla, pero solo se lo mantendrá si hay pruebas de que efectivamente la redujo. De 1.500 "
                    "envíos con el nuevo embalaje, 9 tuvieron reclamos.",
                    ["Con un riesgo del 5%, ¿se mantiene el nuevo embalaje?"])
    assert an.tema == "proporcion"
    assert an.datos["p0"] == pytest.approx(0.012) and an.datos["n"] == 1500 and an.datos["r"] == 9
    assert an.incisos[0].params["tail"] == "izquierda"
    assert "p ≥ 0.012" in res[0].resumen


def test_control_de_rutina_calibrado_alpha_como_frecuencia_bilateral():
    an, res = _plan("Una dosificadora está regulada en 500 g y su desvío, conocido, es de 4 g. Cada hora se toma una "
                    "muestra de 16 envases para decidir si se la detiene para recalibrarla. Se acepta detenerla "
                    "innecesariamente 1 de cada 25 veces. El último control dio una media de 501,5 g.",
                    ["¿Hay que detener la dosificadora?"])
    assert an.datos["mu0"] == 500 and an.datos["alpha"] == pytest.approx(0.04) and an.datos["xbar"] == 501.5
    inc = an.incisos[0]
    assert inc.tipo == "ensayo" and inc.params["tail"] == "bilateral"   # 'a lo sumo'/'innecesariamente' no es la cola
    assert "NO rechaza" in res[0].resumen


def test_a_lo_sumo_del_riesgo_no_define_la_cola():
    an, _ = _plan("Una envasadora está calibrada para 1.000 cc, con un desvío conocido de 6 cc. Cada turno se controla "
                  "una muestra de 25 envases para decidir si se la detiene. Se admite detenerla sin necesidad a lo sumo "
                  "1 de cada 20 veces. El último control dio una media de 998 cc.",
                  ["¿Debe detenerse la envasadora?"])
    assert an.datos["mu0"] == 1000 and an.datos["alpha"] == pytest.approx(0.05)
    assert an.incisos[0].tipo == "ensayo" and an.incisos[0].params["tail"] == "bilateral"


# --- complemento: cuenta los que NO y pregunta por los que SÍ (T-6) -------------------------------------------------

def test_cuenta_los_que_no_y_pregunta_por_los_que_si():
    an, res = _plan("De 150 usuarios consultados al azar, 45 dijeron que no recomendarían el servicio.",
                    ["Estimar con 95% de confianza el porcentaje de usuarios que sí recomendarían el servicio."])
    assert an.datos["n"] == 150 and an.datos["r"] == 45
    assert an.incisos[0].params.get("r_buenas")
    lo, hi = [x for x in res[0].numeros if 0 < x < 1][:2]
    assert lo < 0.70 < hi                                   # p̂ = 105/150


def test_cuenta_los_que_no_y_pregunta_por_los_que_no():
    an, _ = _plan("De 150 usuarios consultados al azar, 45 dijeron que no recomendarían el servicio.",
                  ["Estimar con 95% de confianza la proporción de usuarios que no lo recomendarían."])
    assert not an.incisos[0].params.get("r_buenas")


# --- varianza con unidades al cuadrado y límite sobre el desvío (T-8) -----------------------------------------------

def test_varianza_en_unidades_cuadradas_y_desvio_que_no_debe_exceder():
    an, res = _plan("El desvío del peso de los paquetes no debe exceder 2 g. En una muestra de 20 paquetes la varianza "
                    "del peso fue de 5,3 g².", ["Con un riesgo del 5%, ¿el proceso está fuera de especificación?"])
    assert an.tema == "varianza"
    assert an.datos["sigma0"] == 2 and an.datos["desvio"] == pytest.approx(5.3 ** 0.5)
    assert an.incisos[0].params["tail"] == "derecha"
    assert not res[0].errores


def test_varianza_poblacional_en_unidades_cuadradas_es_sigma():
    an, _ = _plan("La varianza del tiempo de respuesta, por registros de muchos años, vale 9 s². Se midieron 36 "
                  "consultas y el tiempo medio resultó de 41 s.",
                  ["Con un 95% de confianza, ¿entre qué valores está el tiempo medio de respuesta?"])
    assert an.datos["desvio"] == pytest.approx(3) and an.datos["sigma_conocido"] is True
    assert an.incisos[0].tipo == "ic"


# --- dos medias: 'A da X menos que B' (T-11) y diferencia porcentual con el orden cambiado (S-3) --------------------

def test_referencia_da_menos_que_el_nuevo_se_plantea_nuevo_menos_referencia():
    an, res = _plan("Se compara un fertilizante nuevo con el tradicional. Con el nuevo se trataron 14 parcelas: "
                    "rendimiento promedio 42,1 quintales por hectárea, desvío 2,4. Con el tradicional se trataron 16 "
                    "parcelas: promedio 37,0, desvío 2,2.",
                    ["Con un riesgo del 5%, ¿puede afirmarse que con el fertilizante tradicional se cosechan, en "
                     "promedio, al menos 3 quintales por hectárea menos que con el nuevo?"])
    p = an.incisos[0].params
    assert p["tail"] == "derecha" and p["delta0"] == 3
    assert an.datos[f"nombre{p['sujeto']}"].startswith("nuevo")
    assert "≤ 3" in res[0].resumen


def test_diferencia_porcentual_con_el_grupo_afirmado_segundo_en_los_datos():
    an, res = _plan("Un comercio compara la duración de dos marcas de lámparas. Con 40 lámparas de la marca X se obtuvo "
                    "una duración promedio de 1.180 horas con un desvío de 90 horas; con 40 lámparas de la marca Y, "
                    "1.400 horas con un desvío de 110 horas.",
                    ["Con un 5% de riesgo, ¿puede afirmarse que la marca Y dura al menos un 15% más que la marca X?"])
    assert an.datos["n2"] == 40 and an.datos["xbar2"] == 1400            # redacción paralela, sin 'promedio'
    assert {an.datos["nombre1"], an.datos["nombre2"]} == {"marca X", "marca Y"}
    p = an.incisos[0].params
    assert an.datos[f"nombre{p['sujeto']}"] == "marca Y" and p["delta0_pct"] == pytest.approx(0.15)
    assert "1,15·μ(marca X)" in res[0].resumen


# --- dos varianzas mezclando varianza y desvío; 'en más de un X%' no es dirección (S-1) -----------------------------

def test_dos_varianzas_con_una_varianza_y_un_desvio():
    an, res = _plan("Se cambiará el método actual por uno propuesto solo si reduce el desvío del diámetro en más de un "
                    "20%. Con el método actual se midieron 21 piezas y el desvío fue de 0,4 mm. Con el método propuesto "
                    "se midieron 16 piezas y la varianza resultó 0,09 mm².",
                    ["Con un riesgo del 5%, ¿conviene adoptar el método propuesto?"])
    assert an.tema == "dos_varianzas"
    assert sorted([an.datos["s1"], an.datos["s2"]]) == [pytest.approx(0.3), pytest.approx(0.4)]
    assert an.datos["phi0"] == pytest.approx(0.8)
    assert an.incisos[0].params["tail"] == "izquierda"
    assert "0.8" in res[0].resumen


# --- tabla de contingencia en porcentajes por fila (S-4) ------------------------------------------------------------

def test_tabla_de_contingencia_en_porcentajes_por_fila():
    an, res = _plan("Se encuestó a 150 estudiantes de la mañana y 100 estudiantes de la noche sobre el medio de "
                    "transporte que usan. De los estudiantes de la mañana, el 40% usa colectivo, el 34% tren y el resto "
                    "auto. De los estudiantes de la noche, el 30% usa colectivo, el 30% tren y el resto auto.",
                    ["Con un 5% de significación, ¿el medio de transporte depende del turno?"])
    assert an.tema == "chi_contingencia"
    assert an.datos["tabla"] == [[60, 51, 39], [30, 30, 40]]
    assert not res[0].errores


def test_tabla_en_porcentajes_con_grupos_de_la_misma_unidad():
    an, _ = _plan("Se inspeccionaron 200 piezas del turno mañana y 150 piezas del turno noche. En el turno mañana, el "
                  "5% tuvo fallas leves, el 2% fallas graves y el resto ninguna falla; en el turno noche, el 8% tuvo "
                  "fallas leves, el 4% fallas graves y el resto ninguna.",
                  ["Con un 5% de significación, ¿el tipo de falla depende del turno?"])
    assert an.tema == "chi_contingencia"
    assert an.datos["tabla"] == [[10, 4, 186], [12, 6, 132]]
