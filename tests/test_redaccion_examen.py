"""Redacciones de examen "raras" que las REGLAS tienen que leer bien sin IA.

Salen del banco `datos/enunciados_raros.json` (`python herramientas/evaluar_guia.py --raros`), pero cada test usa una
redacción DISTINTA a la del banco, para comprobar que el arreglo es general y no un parche para un texto.
"""

import pytest

from interprete.analizador import analizar, reescribir_frecuencias, reescribir_numeros_palabras
from interprete.glosario import unificar_redaccion
from interprete.resolver import resolver


def _plan(planteo, incisos=None, tablas=None):
    an = analizar(planteo, incisos, tablas=tablas)
    return an, resolver(an)


# --- números escritos con palabras ---------------------------------------------------------------------------------

@pytest.mark.parametrize("texto,esperado", [
    ("Se inspeccionaron doce piezas", "Se inspeccionaron 12 piezas"),
    ("con el ochenta por ciento de confianza", "con el 80% de confianza"),
    ("un dos y medio por ciento de fallas", "un 2,5% de fallas"),
    ("sobre trescientos veinte clientes", "sobre 320 clientes"),
    ("el uno por ciento de las veces", "el 1% de las veces"),
    ("subió un punto porcentual", "subió 1 punto porcentual"),
    ("lo baja medio litro por lo menos", "lo baja 0,5 litro por lo menos"),
])
def test_numeros_en_palabras_pasan_a_cifras(texto, esperado):
    assert reescribir_numeros_palabras(texto)[0] == esperado


@pytest.mark.parametrize("texto", [
    "Se comparan las dos máquinas de la planta.",      # cuenta grupos: otras reglas leen 'dos máquinas'
    "Hay tres turnos de trabajo.",
    "Se plantean dos alternativas.",
    "Una muestra de un lote.",                          # artículos
    "el tres salió 9 veces",                            # cara de un dado (etiqueta, no dato)
    "el consumo medio de nafta",                        # 'medio' = promedio
])
def test_numeros_en_palabras_que_no_son_datos_no_se_tocan(texto):
    assert reescribir_numeros_palabras(texto)[0] == texto


def test_media_con_numeros_en_palabras():
    an, res = _plan("Se sabe que el desvío del peso de los paquetes es de veinte gramos. Se pesaron dieciséis paquetes "
                    "al azar y el promedio fue de 498 g.", ["Estimar el peso medio con el noventa y cinco por ciento de "
                                                           "confianza."])
    assert an.datos["n"] == 16 and an.datos["desvio"] == 20 and an.datos["sigma_conocido"] is True
    assert an.incisos[0].params["alpha"] == pytest.approx(0.05)
    assert not res[0].errores


# --- sinónimos y moneda antes del número ---------------------------------------------------------------------------

@pytest.mark.parametrize("texto,esperado", [
    ("¿qué chance hay de aprobarlo?", "¿qué probabilidad hay de aprobarlo?"),
    ("se decide parar la línea", "se decide detener la línea"),
    ("el cliente devuelve la partida", "el cliente rechaza la partida"),
    ("que el control no advierta el cambio", "que el control no detecte el cambio"),
    ("la desviación típica fue 3", "la desviación estándar fue 3"),
    ("un ingreso de U$S 1.250 por mes", "un ingreso de 1.250 U$S por mes"),
])
def test_sinonimos_de_examen(texto, esperado):
    assert unificar_redaccion(texto) == esperado


def test_moneda_antes_del_numero_se_lee_como_media_y_desvio():
    an, res = _plan("Se abrirá una sucursal si el gasto medio mensual de los clientes supera los $ 5.000. En una "
                    "encuesta a 64 clientes el gasto medio resultó $ 5.300 con un desvío de $ 1.200.",
                    ["Con un riesgo del 5%, ¿conviene abrir la sucursal?"])
    assert an.datos["xbar"] == 5300 and an.datos["desvio"] == 1200 and an.datos["mu0"] == 5000
    assert an.incisos[0].params["tail"] == "derecha" and not res[0].errores


# --- riesgos dichos de otra forma -----------------------------------------------------------------------------------

def test_riesgo_lejos_del_numero_se_fija_en():
    an, _ = _plan("Se comprará la máquina si el tiempo medio de ciclo es menor que 40 s. El riesgo de comprarla sin "
                  "que realmente cumpla con lo pedido se establece en 0,02. Se cronometraron 25 ciclos: media 38,9 s y "
                  "desvío 3 s.", ["¿Se compra?"])
    assert an.datos["alpha"] == pytest.approx(0.02)


def test_porcentaje_de_las_veces_que_se_detiene_estando_bien_es_alfa():
    an, _ = _plan("Una envasadora se controla con muestras de 25 envases. Cuando funciona correctamente, se acepta que "
                  "solo un 2% de las veces se la detenga para revisarla. Su desvío es de 3 g y debe envasar 500 g.",
                  ["Indicar el valor crítico del control."])
    assert an.datos["alpha"] == pytest.approx(0.02)


def test_alfa_escrito_con_el_simbolo():
    an, _ = _plan("En una muestra de 30 unidades se encontraron 9 defectuosas. Con α = 0,10, ¿supera el porcentaje de "
                  "defectuosas el 20%?")
    assert an.datos["alpha"] == pytest.approx(0.10)


# --- TEMA III: dirección, plan dado, diseño --------------------------------------------------------------------------

def test_mas_del_porcentaje_es_p0_y_cola_derecha():
    an, res = _plan("Se lanzará el producto solo si más del 30% de los consumidores lo prefiere. De 200 consumidores "
                    "consultados, 75 dijeron preferirlo. El riesgo de lanzarlo por error es del 5%.",
                    ["¿Se lanza el producto?"])
    assert an.datos["p0"] == pytest.approx(0.30) and an.datos["n"] == 200 and an.datos["r"] == 75
    assert an.incisos[0].params["tail"] == "derecha"
    assert not res[0].errores


def test_plan_dado_con_palabras_entre_el_numero_y_o_mas():
    an, _ = _plan("De cada partida se revisan 80 unidades y se la rechaza si aparecen 6 unidades defectuosas o más. "
                  "Por contrato se admite hasta un 3% de defectuosas.", ["¿Cuál es el riesgo del proveedor?"])
    assert an.datos["rc"] == 6 and an.datos["n"] == 80


def test_numero_del_plan_no_es_el_tamano_de_muestra():
    an, _ = _plan("Un lote se rechaza si en la muestra aparecen como mínimo tres piezas falladas.",
                  ["¿Qué tamaño de muestra hace falta para que un lote con 2% de falladas se acepte con probabilidad "
                   "mayor a 0,90?"])
    assert an.datos["rc"] == 3 and "n" not in an.datos


def test_diseno_alfa_va_con_la_condicion_normal_aunque_la_otra_diga_seguridad():
    an, _ = _plan("Un proceso trabaja normalmente con un 2% de defectuosos. Se busca un plan tal que la probabilidad "
                  "de detenerlo cuando anda bien sea a lo sumo de 0,05, y que si los defectuosos suben al 5% se lo "
                  "detenga con un 90% de seguridad.", ["Determinar el plan de muestreo."])
    assert an.datos["alpha"] == pytest.approx(0.05) and an.datos["beta"] == pytest.approx(0.10)
    assert an.datos["p0"] == pytest.approx(0.02) and an.datos["p1"] == pytest.approx(0.05)


@pytest.mark.parametrize("texto,tipo", [
    ("¿A partir de cuántas fallas en la muestra habrá que detener la línea?", "diseno"),
    ("¿Con qué probabilidad se acepta un lote con 6% de defectuosas?", "beta"),
    ("¿Y la probabilidad de aceptar si el lote tiene un 8%?", "beta"),
    ("¿Cuántas unidades adicionales hacen falta para que el error sea de 2 g?", "n"),
])
def test_clasificacion_de_preguntas_indirectas(texto, tipo):
    an, _ = _plan("En una muestra de 60 unidades de un lote se hallaron 4 defectuosas. El contrato admite hasta un 3% "
                  "de defectuosas.", [texto])
    assert an.incisos[0].tipo == tipo


# --- incisos que dependen del anterior -----------------------------------------------------------------------------

def test_inciso_eliptico_repite_la_pregunta_anterior():
    an, res = _plan("Se probó un fertilizante en 12 parcelas, con un rinde medio de 31 qq y un desvío de 2,4 qq; en "
                    "otras 12 parcelas sin fertilizante el rinde medio fue de 28 qq con un desvío de 2,1 qq.",
                    [("a", "¿Puede asegurarse con un 5% de riesgo que el fertilizante aumenta el rinde en 1 qq por lo menos?"),
                     ("b", "¿Y en un 5% por lo menos?")])
    assert an.incisos[1].tipo == "ensayo"
    assert an.incisos[1].params.get("delta0_pct") == pytest.approx(0.05)
    assert not res[1].errores


@pytest.mark.parametrize("pregunta", [
    "Con α = 0,05, ¿el nuevo método reduce el tiempo medio?",
    "¿La capacitación mejora el rendimiento medio? Usar un riesgo del 5%.",
])
def test_pregunta_si_hay_efecto_es_un_ensayo(pregunta):
    an, _ = _plan("Con el método actual 15 operarios tardaron en promedio 42 min (desvío 5 min); con el método nuevo "
                  "otros 15 operarios tardaron en promedio 39 min (desvío 6 min).", [pregunta])
    assert an.tema == "dos_medias" and an.incisos[0].tipo == "ensayo"


# --- TEMA IV / V ---------------------------------------------------------------------------------------------------

def test_dos_grupos_nombrados_con_letra_entre_parentesis():
    an, _ = _plan("Con el proceso viejo (V) se midieron 25 piezas, con un desvío de 0,12 mm; con el proceso modificado "
                  "(M), 20 piezas, con un desvío de 0,08 mm.",
                  ["Con un riesgo del 5%, ¿el proceso modificado reduce el desvío?"])
    assert an.tema == "dos_varianzas"


def test_magnitud_o_mas_en_dos_medias():
    an, _ = _plan("Con el aditivo, 16 probetas dieron una resistencia media de 52 kg (desvío 4 kg); sin el aditivo, otras "
                  "16 dieron 48 kg (desvío 5 kg).",
                  ["Con 5% de riesgo, ¿se puede asegurar que el aditivo sube la resistencia media 2 kg o más?"])
    assert an.incisos[0].params.get("delta0") == 2


def test_series_con_dos_puntos_y_mismas_unidades_son_apareadas():
    an, res = _plan("Se midió el consumo de 6 autos con dos tipos de neumático, en los mismos 6 autos.\n"
                    "Neumático A: 7,1 6,8 7,4 6,9 7,0 7,3\nNeumático B: 6,8 6,7 7,0 6,9 6,6 7,0",
                    ["Con un riesgo del 5%, ¿el neumático B reduce el consumo medio?"])
    assert an.datos.get("apareadas") is True
    assert an.datos.get("nombre1", "").startswith("Neumático")
    assert not res[0].errores


# --- TEMA VI: tablas contadas en prosa ------------------------------------------------------------------------------

def test_contingencia_narrada_por_renglones_con_su_total():
    an, res = _plan("Se clasificaron las respuestas de tres sucursales. Sucursal Norte (200 clientes): 120 satisfechos, "
                    "50 neutrales y 30 insatisfechos. Sucursal Sur (150 clientes): 70, 50 y 30. Sucursal Oeste (100 "
                    "clientes): 60, 25 y 15. Con α = 0,05, ¿la satisfacción depende de la sucursal?")
    assert an.tema == "chi_contingencia"
    assert an.datos["tabla"] == [[120, 50, 30], [70, 50, 30], [60, 25, 15]]
    assert not res[0].errores


def test_ajuste_uniforme_con_frecuencias_que_suman_el_total():
    an, res = _plan("Un comercio afirma que sus ventas se reparten por igual entre los 5 días hábiles. De 250 ventas "
                    "registradas, 48 fueron el lunes, 55 el martes, 41 el miércoles, 52 el jueves y 54 el viernes. Con "
                    "un riesgo del 5%, ¿se puede refutar al comercio?")
    assert an.tema == "chi_ajuste"
    assert an.datos["observados"] == [48, 55, 41, 52, 54]
    assert an.datos["proporciones"] == pytest.approx([0.2] * 5)
    assert not res[0].errores


def test_dos_proporciones_narradas_en_presente():
    an, res = _plan("Se analizan 400 envases de la línea vieja y 52 resultan con fallas; de la línea nueva se analizan "
                    "300 envases y 21 resultan con fallas. Con un riesgo del 5%, ¿difieren los porcentajes de fallas?")
    assert an.tema == "chi_contingencia"
    assert an.datos["tabla"] == [[52, 348], [21, 279]]
    assert not res[0].errores


def test_varios_grupos_con_el_mismo_tamano():
    an, res = _plan("Cada día se controlan 200 tornillos y se cuentan los defectuosos. En la semana hubo 8 el lunes, 12 "
                    "el martes, 5 el miércoles y 11 el jueves. ¿Cambia el porcentaje de defectuosos de un día a otro? "
                    "Usar α = 0,05.")
    assert an.tema == "chi_contingencia"
    assert an.datos["tabla"] == [[8, 192], [12, 188], [5, 195], [11, 189]]
    assert not res[0].errores


def test_tabla_de_conteos_relacionada_con_es_contingencia():
    tablas = [{"titulo": "", "columnas": ["Edad", "Plan A", "Plan B", "Plan C"],
               "filas": [["Joven", 40, 25, 15], ["Adulto", 30, 35, 35]]}]
    an, _ = _plan("Se registró el plan elegido por clientes de dos franjas de edad (tabla). ¿El plan elegido está "
                  "relacionado con la edad?", tablas=tablas)
    assert an.tema == "chi_contingencia"


# --- TEMA VII ------------------------------------------------------------------------------------------------------

def test_pendiente_cada_mil_al_menos_y_variables_explicativas():
    tablas = [{"titulo": "", "columnas": ["Inversión", "Facturación"],
               "filas": [[2.0, 30], [3.1, 34], [4.2, 39], [5.0, 41], [6.3, 47]], "variable_y": "Facturación"}]
    an, _ = _plan("Un gerente sostiene que cada mil pesos adicionales de inversión generan al menos 3.000 pesos más de "
                  "facturación (datos en miles de pesos en la tabla).", [("a", "¿Los datos respaldan al gerente?")],
                  tablas=tablas)
    assert an.tema == "regresion"
    inc = an.incisos[0]
    assert inc.tipo == "ensayo_coef" and inc.params["beta10"] == pytest.approx(3) and inc.params["tail"] == "derecha"


def test_y_que_baja_no_es_x_que_baja():
    tablas = [{"titulo": "", "columnas": ["Temperatura", "Viscosidad"],
               "filas": [[20, 50], [30, 44], [40, 37], [50, 33], [60, 26]], "variable_y": "Viscosidad"}]
    an, _ = _plan("Se midió la viscosidad de un aceite a distintas temperaturas (tabla).",
                  [("a", "¿Se puede afirmar con un riesgo del 5% que cada grado más de temperatura baja la viscosidad en "
                         "más de 0,5 unidades?")], tablas=tablas)
    inc = an.incisos[0]
    assert inc.params["beta10"] == pytest.approx(-0.5) and inc.params["tail"] == "izquierda"


# --- cola: 'bajo criterio pesimista' no es una disminución -----------------------------------------------------------

def test_bajo_criterio_no_es_una_disminucion():
    an, _ = _plan("La duración media de unas lámparas es de 1.000 h con un desvío de 80 h (registros históricos). Con "
                  "un nuevo filamento se espera aumentarla. Se probaron 25 lámparas nuevas: duración media 1.030 h. "
                  "Riesgo del 5%.", ["Plantear la hipótesis bajo criterio pesimista e indicar si se adopta el filamento."])
    assert an.incisos[0].params["tail"] == "derecha"


def test_cada_grado_menos_es_x_que_baja():
    tablas = [{"titulo": "", "columnas": ["Temperatura", "Consumo"],
               "filas": [[5, 30], [10, 26], [15, 23], [20, 18], [25, 15]], "variable_y": "Consumo"}]
    an, _ = _plan("Se registró el consumo de gas según la temperatura (tabla).",
                  [("a", "¿Se puede asegurar que por cada grado menos de temperatura el consumo crece más de 0,5?")],
                  tablas=tablas)
    inc = an.incisos[0]
    assert inc.params["beta10"] == pytest.approx(-0.5) and inc.params["tail"] == "izquierda"
