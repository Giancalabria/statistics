"""Intérprete en χ² (ajuste a modelos, contingencia desde tablas) y regresión, con redacciones alternativas.

Los textos imitan la guía pero cambian la redacción, el orden y los nombres, para comprobar que las
reglas generalizan y no dependen de un enunciado puntual.
"""

import pytest

from interprete.analizador import analizar
from interprete.resolver import resolver


def _resolver(planteo, incisos=None, tablas=None):
    an = analizar(planteo, incisos, tablas=tablas)
    return an, resolver(an)


# ---------------------------------------------------------------- bondad de ajuste

def test_poisson_con_otra_redaccion():
    planteo = ("Se registró durante 684 jornadas la cantidad de llamadas de reclamo que recibe un call center por día. "
               "Se cree que la cantidad diaria de llamadas responde a una distribución de Poisson. "
               "Tabla: Llamadas por día | Cantidad de jornadas; 0 | 26; 1 | 62; 2 | 120; 3 | 145; 4 | 131; 5 | 101; "
               "6 | 61; 7 | 27; 8 | 9; 9 | 1; 10 | 1. ¿Se puede aceptar ese supuesto con un riesgo del 5%?")
    an, res = _resolver(planteo)
    assert an.tema == "chi_ajuste"
    assert "NO rechaza" in res[0].resumen and "Poisson" in res[0].resumen


def test_normal_con_parametros_en_otra_escala():
    tabla = {"columnas": ["Duración (en miles de horas)", "Cantidad de equipos"],
             "filas": [["10-12", 2], ["12-14", 6], ["14-16", 13], ["16-18", 18], ["18-20", 30], ["20-22", 22],
                       ["22-24", 16], ["24-26", 5], ["26-28", 1]]}
    an, res = _resolver("Se midió la duración de 113 equipos de una marca.",
                        ["El proveedor garantiza que la duración es normal con media 20.000 horas y desvío estándar "
                         "2.500 horas; con un riesgo del 5%, ¿se ajusta a lo garantizado?"], tablas=[tabla])
    assert an.tema == "chi_ajuste"
    assert "RECHAZA" in res[0].resumen and "NO" not in res[0].resumen
    assert any("dividieron por 1000" in a for a in res[0].avisos)


def test_dos_modelos_en_un_inciso_y_el_mejor():
    tabla = {"columnas": ["Duración (h)", "Herramientas"],
             "filas": [["0-15", 8], ["15-30", 40], ["30-45", 30], ["45-60", 25], ["60-75", 18], ["75-90", 15], ["90-105", 7]]}
    an, res = _resolver("Se cree que la duración de las herramientas sigue un modelo Gumbel del mínimo.",
                        ["Con 1% de riesgo, ¿se rechaza el modelo Gumbel del mínimo?",
                         "Si se rechaza el Gumbel del mínimo, probar con Weibull y con Gumbel del máximo. ¿Cuál ajusta mejor?"],
                        tablas=[tabla])
    assert an.incisos[0].params.get("modelos") == ["gumbel_min"]
    assert set(an.incisos[1].params["modelos"]) == {"weibull", "gumbel_max"}
    assert "RECHAZA" in res[0].resumen
    assert res[1].resumen.count("NO rechaza") == 2
    assert "mejor" in res[1].conclusion


def test_contingencia_muestra_y_defectuosos():
    tabla = {"columnas": ["Proveedor", "Unidades revisadas", "Defectuosas"],
             "filas": [["A", 250, 20], ["B", 500, 75]]}
    an, res = _resolver("Se comparan dos proveedores de conos. ¿Se puede asegurar, con 5% de riesgo, que las "
                        "proporciones de defectuosos son diferentes?", tablas=[tabla])
    assert an.tema == "chi_contingencia"
    assert an.datos["tabla"] == [[20, 230], [75, 425]]


def test_contingencia_saca_totales_e_indice():
    tabla = {"columnas": ["Planta", "Baja", "Media", "Alta", "Total"],
             "filas": [[1, 10, 176, 14, 200], [2, 16, 178, 6, 200], [3, 17, 174, 9, 200], ["Total", 43, 528, 29, 600]]}
    an, _ = _resolver("¿Se puede asegurar que las proporciones de elongación difieren entre las 3 plantas?",
                      tablas=[tabla])
    assert an.datos["tabla"] == [[10, 176, 14], [16, 178, 6], [17, 174, 9]]


def test_contingencia_homogeneidad_con_tablas_y_nombres():
    tabla = {"columnas": ["Turno", "Buenas", "Defectuosas", "Muestra"],
             "filas": [["Mañana", 380, 20, 400], ["Noche", 360, 40, 400]]}
    an, res = _resolver("Se tomaron muestras de 400 piezas en cada turno. Con un riesgo del 5%, ¿se puede asegurar "
                        "que los porcentajes de calidad difieren entre turnos?", tablas=[tabla])
    pasos = "\n".join(res[0].pasos)
    assert "prueba de consistencia" in pasos and "1 = Mañana, 2 = Noche" in pasos
    # observados con totales, esperados y aportes, con los nombres del enunciado
    assert "*Frecuencias observadas Oᵢⱼ*" in pasos and "*Aportes (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ*" in pasos
    assert "| Mañana | 380 | 20 | **400** |" in pasos
    assert "| Mañana | 370 | 30 | **400** |" in pasos          # Eᵢⱼ = 400 · 750 / 800, 400 · 60 / 800
    assert "Mañana y Noche" in res[0].conclusion


def test_contingencia_independencia_si_pregunta_por_asociacion():
    tabla = {"columnas": ["Zona", "Marca A", "Marca B"], "filas": [["Norte", 30, 20], ["Sur", 15, 35]]}
    an, res = _resolver("Se registró la marca preferida por clientes de dos zonas. Con un riesgo del 5%, ¿la marca "
                        "preferida depende de la zona?", tablas=[tabla])
    pasos = "\n".join(res[0].pasos)
    assert "prueba de independencia" in pasos and "en cada zona (1 = Norte, 2 = Sur)" in pasos
    # independencia en palabras (profesor en clase): «… es independiente de …»
    assert "zona es independiente de" in res[0].conclusion
    assert "no es cierto que" not in res[0].conclusion            # sin doble negación


def test_contingencia_sin_nombres_usa_fila_y_columna():
    an, res = _resolver("Con un riesgo del 5%, ¿las variables están asociadas?",
                        tablas=[{"columnas": ["", "X", "Y"], "filas": [["a", 10, 20], ["b", 30, 40]]}])
    an.datos["tabla"] = [[10, 20, 5], [30, 40, 15]]   # editada a mano: las columnas ya no son las del enunciado
    pasos = "\n".join(resolver(an)[0].pasos)
    assert "| a | 10 | 20 | 5 |" in pasos                  # las filas siguen siendo las mismas
    assert "Columna 1, Columna 2 y Columna 3" in pasos and "| X |" not in pasos


# ---------------------------------------------------------------- regresión simple

PLANTEO_VENTAS = ("Una empresa quiere predecir sus ventas mensuales (en miles de unidades) a partir del gasto en "
                  "publicidad (en miles de pesos). Se registraron los siguientes datos:\n"
                  "Publicidad | Ventas\n5 | 72\n7,2 | 79\n6,3 | 73\n4,2 | 59\n5,4 | 67\n6,8 | 69")


def test_y_es_lo_que_se_quiere_predecir_aunque_este_primero():
    texto = ("Se desea pronosticar el consumo de combustible en función de la velocidad. "
             "[Tabla: Consumo (en litros) Velocidad (en km/h) ; 7 60 ; 8 80 ; 10 100 ; 13 120 ; 15 130]")
    an, _ = _resolver(texto, ["Hallar la recta de mínimos cuadrados."])
    assert an.datos["nombre_y"].startswith("Consumo")


def test_pronostico_minimo_unilateral_e_intervalo_promedio():
    tabla = {"columnas": ["Publicidad", "Ventas"], "filas": [[5, 72], [7.2, 79], [6.3, 73], [4.2, 59], [5.4, 67], [6.8, 69]]}
    an, res = _resolver("Una empresa quiere predecir sus ventas a partir del gasto en publicidad.",
                        ["¿Cuál es la venta mínima que se puede asegurar con 95% de confianza para un mes con un gasto de 6?",
                         "Estimar con un 90% de confianza las ventas promedio para un gasto de 6."], tablas=[tabla])
    a, b = an.incisos
    assert a.tipo == b.tipo == "pronostico"
    assert a.params["cola"] == "inferior" and a.params["individual"] is True
    assert b.params["individual"] is False and b.params["alpha"] == pytest.approx(0.10)
    assert "mínimo" in res[0].resumen


def test_afirmacion_por_unidad_en_miles():
    an, res = _resolver(PLANTEO_VENTAS + "\nEl gerente sostiene que por cada 1.000 pesos adicionales en publicidad las "
                        "ventas aumentan en más de 2.500 unidades.",
                        ["¿Se puede confirmar la afirmación del gerente con un riesgo del 5%?"])
    inc = an.incisos[0]
    assert inc.tipo == "ensayo_coef"
    assert inc.params["beta10"] == pytest.approx(2.5) and inc.params["tail"] == "derecha"


def test_disminuye_al_aumentar_x():
    tabla = {"columnas": ["Deformación (mm)", "Dureza"], "filas": [[6, 70], [9, 62], [12, 59], [15, 55], [18, 50], [21, 46]]}
    an, res = _resolver("Se estudia la relación lineal entre la deformación del acero y su dureza.",
                        ["¿Se puede afirmar que por cada milímetro de deformación la dureza disminuye en más de 1 unidad, "
                         "con un riesgo del 5%?"], tablas=[tabla])
    assert an.incisos[0].params["beta10"] == pytest.approx(-1) and an.incisos[0].params["tail"] == "izquierda"


def test_fuerza_y_influencia_porcentual():
    tabla = {"columnas": ["X", "Y"], "filas": [[3, 270], [3, 290], [6, 450], [6, 500], [9, 600], [9, 520], [3, 330], [6, 480]]}
    an, res = _resolver("Se analiza la relación entre la cantidad de anaqueles y las ventas.",
                        ["Estimar con 90% de confianza la fuerza de la relación entre ambas variables.",
                         "Estimar con 90% de confianza la influencia porcentual de los anaqueles en las ventas."],
                        tablas=[tabla])
    assert [i.tipo for i in an.incisos] == ["ic_rho", "ic_rho2"]


def test_modelo_doble_logaritmico():
    tabla = {"columnas": ["Consumo (en Kwh)", "Potencia (en Kw)"], "filas": [[110, 0.7], [568, 2.41], [245, 1.19], [324, 1.53], [76, 0.53]]}
    an, res = _resolver("Se estudia la relación entre el consumo de los usuarios y su potencia máxima.",
                        ["Si se supone que y = α·x^β, donde la variable y es la potencia, estimar α y β."], tablas=[tabla])
    assert an.incisos[0].tipo == "transformado" and an.incisos[0].params["modelo"] == "loglog"
    assert an.datos["nombre_y"].startswith("Potencia")


def test_sumatorias_en_el_texto():
    an, res = _resolver("Se quiere predecir la demanda diaria de gas (medida en 10^5 m³) a partir de la temperatura media "
                        "(en ºC). Con datos de 10 días se obtuvo: Σx = 97 ; Σx² = 1.169 ; Σy = 21,16 ; Σy² = 48,68 ; "
                        "Σy·x = 180,9326",
                        ["Si la temperatura prevista es de 5ºC, ¿qué demanda mínima se puede asegurar con un 90% de confianza?"])
    assert an.tema == "regresion"
    assert any(abs(v - 199813.14) < 1 for v in res[0].numeros)


# ---------------------------------------------------------------- regresión múltiple

def test_multiple_detecta_y_por_encabezado():
    tabla = {"columnas": ["X1", "X2", "Y"],
             "filas": [[1, 5, 10.1], [2, 3, 11.9], [3, 6, 15.2], [4, 2, 15.8], [5, 7, 20.1], [6, 1, 19.9], [7, 4, 23.2]]}
    an, res = _resolver("Se registraron tres variables.", ["Estime los parámetros del modelo lineal general y valídelo."],
                        tablas=[tabla])
    assert an.tema == "regresion_multiple" and an.incisos[0].tipo == "multiple"
    assert len(an.datos["xs"]) == 2


def test_multiple_seleccion_de_modelos():
    import random
    random.seed(3)
    filas = []
    for _ in range(15):
        a, b, c = random.random() * 10, random.random() * 10, random.random() * 10
        filas.append([a, b, c, 3 + 2 * a + random.random()])
    tabla = {"columnas": ["X1", "X2", "X3", "Y"], "filas": filas}
    an, res = _resolver("Se cree que Y depende de tres variables.", ["Determinar cuál es el mejor modelo candidato."],
                        tablas=[tabla])
    assert an.incisos[0].tipo == "seleccion"
    assert "mejor: x1 →" in res[0].resumen.lower()
