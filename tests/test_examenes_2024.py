"""Exámenes 2024 de la cátedra (recuperatorio del 2° parcial y final del 12/12/2024), transcriptos tal cual.

Se usaron como prueba CIEGA del consenso (sin ajustar nada antes de medir); después se corrigieron las reglas en lo
que fallaban. Valores controlados con una resolución independiente (scipy)."""

import pytest

from interprete.analizador import analizar
from interprete.resolver import resolver

EJ = {
 "R1": dict(planteo="El registro de la cantidad de vehículos particulares que llegan a una estación de peaje es el siguiente: (ver tabla) ¿Se verifica que la llegada de vehículos/minuto a la estación de peajes sigue la ley de distribuciones Poisson?",
    incisos=None,
    tablas=[{"titulo": "", "columnas": ["Vehículos/min", "Observaciones"],
             "filas": [[5, 1], [6, 2], [7, 3], [8, 5], [9, 7], [10, 9], [11, 6], [12, 6], [13, 3], [14, 4], [15, 2], [16, 2]]}]),
 "R3": dict(planteo=("Con base en los datos reportados en un artículo de 1979 que apareció en el Journal of Gerontology (\"Serum "
    "Ferritin in an Elderly Population\", págs. 521-524), los autores concluyeron que la distribución de ferritina en los "
    "adultos mayores tenía un varianza más pequeña en los adultos jóvenes (la ferritina en suero se utiliza para diagnosticar "
    "deficiencia de hierro). Para una muestra de 28 varones adultos mayores, la desviación estándar de ferritina en suero "
    "(mg/l) fue S1=52.6; para 26 adultos jóvenes, la desviación estándar fue S2=84.2. ¿Confirman estos datos la conclusión del \"paper\" citado a un nivel de significación de 1%?"),
    incisos=None, tablas=None),
 "R4": dict(planteo=("Se sugiere utilizar un Modelo Lineal para explicar la resistencia a la rotura en función del límite "
    "elástico de varillas de acero. Se midieron estas características de 5 varillas (ambas medidas en miles de lbs./pulg2) "
    "con los siguientes resultados:"),
    incisos=[("a", "Investigar la asociación lineal entre las variables. Testee el modelo."),
             ("b", "¿Qué concepto usaría para explicar la influencia porcentual del limite elástico de las varillas de acero en "
                   "el comportamiento de la resistencia a la rotura de las mismas? Calcule ese parámetro.")],
    tablas=[{"titulo": "", "columnas": ["Resistencia a la rotura", "Límite elástico"],
             "filas": [[78, 45.25], [79.5, 48], [82.5, 60.25], [93.5, 62], [98, 65]], "variable_y": "Resistencia a la rotura"}]),
 "F1": dict(planteo=("El volumen de huecos en una tela afecta las propiedades de comodidad, inflamabilidad y aislantes. La "
    "permeabilidad de una tela se refiere a la accesibilidad de los espacios huecos al flujo de un gas o líquido. El artículo "
    "\"The Relationship Between Porosity and Air Permeability of Woven Textile Fabrics\" (J. of Testing and Eval., 1997: "
    "108-114) contiene información resumida sobre permeabilidad al aire (cm3 /cm2 /s) de varios tipos diferentes de tela. "
    "Considere los siguientes datos sobre dos tipos diferentes de tela de tejido ordinario: (ver tabla). Suponiendo que la distribuciones de porosidad de ambos tipos de tela son normales, calcule:"),
    incisos=[("a", "Un intervalo de confianza para la diferencia entre la porosidad promedio verdadera de la tela de algodón y "
                   "la de la tela de triacetato, utilizando un intervalo de confianza de 95%."),
             ("b", "¿Puede afirmar, con un 5% de equivocarse, que la porosidad media de la tela de triacetato es mayor que la "
                   "de la tela de algodón?")],
    tablas=[{"titulo": "", "columnas": ["Tipo de tela", "Tamaño de muestra", "Media muestral", "Desviación estándar de muestra"],
             "filas": [["Algodón", 10, 51.71, 0.79], ["Triacetato", 10, 136.14, 3.59]]}]),
 "F2": dict(planteo=("Un fabricante de hilo de cobre esmaltado para bobinaje de motores especiales de baja revolución quiere "
    "adquirir una nueva máquina extrusora para la confección de ese tipo de hilado que le asegure una maleabilidad promedio "
    "mínima de 3,62 Tn/mm2. Para tomar dicha decisión se estipula correr un riesgo del 1% de adquirir la máquina si no se "
    "consigue la premisa estipulada, y en un 5% el riesgo de no adquirirla si la maleabilidad se encuentra en el orden de "
    "4,15 Tn/mm2 promedio. Se sabe por información histórica del fabricante que la variabilidad de la misma es de 0,45 Tn/mm2."),
    incisos=[("a", "Estipular la hipótesis adecuada al problema, determinar el tamaño de muestra adecuado, la condición de "
                   "rechazo y enunciar correctamente la regla de decisión correspondiente en términos del problema planteado."),
             ("b", "Se realizó la prueba con distintos equipos, obteniendo los siguientes resultados (medidos en Tn/mm2): "
                   "2,9 - 2,8 - 2,7 - 2,5 - 2,9 - 2,7 - 3,4 - 3,2 - 3,4 - 2,6 - 3,3 - 2,5. Informe la decisión que deberá "
                   "tomar la empresa en función de los datos obtenidos.")], tablas=None),
 "F3": dict(planteo=("Tomando los mismos datos del punto anterior: un fabricante evalúa una nueva máquina extrusora de hilo de "
    "cobre; se realizó la prueba con distintos equipos, obteniendo los siguientes resultados de maleabilidad (medidos en "
    "Tn/mm2): 2,9 - 2,8 - 2,7 - 2,5 - 2,9 - 2,7 - 3,4 - 3,2 - 3,4 - 2,6 - 3,3 - 2,5."),
    incisos=[("a", "Estimar la variabilidad de la máquina con un 95% de confianza."),
             ("b", "¿Cuántas pruebas más se deberán realizar si se quiere disminuir en un 30% la relación de estimación del "
                   "desvío obtenida en el punto anterior?")], tablas=None),
 "F4": dict(planteo=("Una compañía fabrica dispositivos semiconductores para ser usado en aplicaciones de gran amplitud térmica. "
    "La compañía sabe que el incremento de temperatura acorta el tiempo de vida de los dispositivos, y por lo tanto le "
    "solicita que determine un modelo que relaciones dichas variables. Se consiguieron los siguientes datos:"),
    incisos=[("a", "Encuentre un modelo lineal para los datos brindados. Calcule el coeficiente de determinación e "
                   "interprételo. Testee el modelo a un nivel de significación del 5%."),
             ("b", "¿Cuál sería el tiempo de vida del dispositivo a 85ºC? Estime un IC para el tiempo de vida medio del "
                   "dispositivo para 55ºC con un nivel de confianza del 95%.")],
    tablas=[{"titulo": "", "columnas": ["Temperatura (ºC)", "Tiempo de vida (hs)"],
             "filas": [[10, 420], [20, 365], [30, 285], [40, 220], [50, 176], [60, 117], [70, 69], [80, 34], [90, 5], [100, 5]],
             "variable_y": "Tiempo de vida (hs)"}]),
}


def _res(k):
    e = EJ[k]
    an = analizar(e["planteo"], e["incisos"], tablas=e["tablas"])
    return an, resolver(an)


def test_R1_ley_de_poisson_con_tabla_valor_frecuencia():
    an, (r,) = _res("R1")
    assert an.tema == "chi_ajuste" and r.resumen.startswith("Poisson") and "NO rechaza" in r.resumen
    assert "12,5916" in r.resumen        # dominio completo (≤ 4 y ≥ 17), λ estimado: ν = 8 - 1 - 1 = 6


def test_R3_solo_desvios_es_comparacion_de_varianzas_y_la_muestra_orienta():
    an, (r,) = _res("R3")
    assert an.tema == "dos_varianzas" and (an.datos["n1"], an.datos["n2"]) == (26, 28)
    assert "J = 1,6008" in r.resumen and "RECHAZA" in r.resumen and "NO" not in r.resumen


def test_R4_validacion_y_determinacion():
    an, (a, b) = _res("R4")
    assert "r = 0,8721" in a.resumen and "0,7606" in b.resumen


def test_F1_tabla_resumen_de_dos_grupos():
    an, (a, b) = _res("F1")
    assert an.tema == "dos_medias"
    assert "81,8004" in a.resumen and "87,0596" in a.resumen      # Welch con ν truncado (9)
    assert "RECHAZA" in b.resumen and "NO" not in b.resumen


def test_F2_diseno_y_ensayo_con_la_muestra_del_inciso():
    an, (a, b) = _res("F2")
    assert an.tema == "media" and an.datos["desvio"] == 0.45      # 'la variabilidad ... es de 0,45' es σ
    assert a.resumen == "n = 12; x̄c = 3,9222"
    assert an.incisos[1].params["tail"] == "derecha"              # el plan del inciso a)
    assert "x̄c = 3,9222" in b.resumen and "NO rechaza" in b.resumen


def test_F3_ic_del_desvio_y_pruebas_adicionales():
    an, (a, b) = _res("F3")
    assert "IC σ: [0,2387 ; 0,5722]" in a.resumen and b.resumen == "n = 31 (19 más)"


def test_F4_modelo_lineal_y_dos_pedidos_en_un_inciso():
    an, (a, b) = _res("F4")
    assert "437,0000 - 4,8618" in a.resumen and "r² = 0,9642" in a.resumen
    assert an.incisos[1].params["x0_puntual"] == 85 and an.incisos[1].params["x0"] == 55
    assert "ŷ(85) = 23,7455" in b.resumen and "[147,6734 ; 191,5266]" in b.resumen
