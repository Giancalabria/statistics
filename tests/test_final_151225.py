"""Final del 15/12/25 (tema 1), transcripto tal cual: un examen real con redacciones que no están en la guía.

Valores controlados con una resolución independiente (scipy)."""

import pytest

from interprete.analizador import analizar
from interprete.resolver import resolver

EJ = {
    "P1": dict(
        planteo=("En el decapado del alambrón debido a la presencia de oxidación del material, se quiere estudiar la "
                 "influencia del Fosfato en la cuba de lavado por la inmersión del rollo del alambrón. Se cree que el "
                 "Fosfato influye sobre la rapidez en el decapado, a tal efecto se obtuvieron los siguientes resultados "
                 "de un experimento:"),
        incisos=[("a", "Hallar la recta de mínimos cuadrados, interpretar ambos estimadores (en términos del problema) e "
                       "investigar la asociación lineal entre las variables. ¿Qué concepto usaría para explicar y estimar "
                       "la influencia porcentual de la concentración de Fosfato en el comportamiento de la presencia final "
                       "de la película de óxido en el alambrón?"),
                 ("b", "Para un 5% de riesgo, por cada ppm de Fosfato, ¿cuál será la máxima presencia final de la película "
                       "de óxido en el alambrón que se puede esperar?")],
        tablas=[{"titulo": "", "columnas": ["Concentración del Fosfato (en ppm)", "Espesor final de la película de óxido (en μ)"],
                 "filas": [[2.5, 8.68], [5.03, 4.95], [7.6, 4.1], [11.6, 2.55], [13, 1.98], [19.6, 0.24], [16.2, 0.6],
                           [13, 2.4], [14, 1.28], [15, 1.05], [15, 1.1]],
                 "variable_y": "Espesor final de la película de óxido (en μ)"}],
    ),
    "P2": dict(
        planteo=("En el comportamiento de los disyuntores en un tablero eléctrico domiciliario, el tiempo de respuesta del "
                 "disyuntor es fundamental para la efectividad de respuesta de una determinada avería eléctrica. Un "
                 "laboratorio de estudios de calidad tiene en investigación dos marcas de disyuntores: \"Marca A\" y "
                 "\"Marca B\". El resultado de los tiempos de respuesta de estas dos marcas fue registrado en la siguiente tabla:"),
        incisos=[("a", "¿Se puede afirmar que el disyuntor de una marca tiene un tiempo de respuesta superior al de la otra "
                       "por más del 10%?"),
                 ("b", "Puede garantizar que el tiempo de respuesta del disyuntor \"Marca A\", se ajusta a la ley Exponencial."),
                 ("c", "La especificación técnica de un disyuntor estipula un tiempo de respuesta máximo de 3 mili-segundos, "
                       "estimar el porcentual de disyuntores de la \"Marca B\" que no cumplen con la especificación. "
                       "(Asumir un 99% de confianza).")],
        tablas=[{"titulo": "", "columnas": ["Tiempo de respuesta (en mili-segundos)", "Cantidad Observada de la \"Marca A\"",
                                            "Cantidad Observada de la \"Marca B\""],
                 "filas": [["2-3", 35, 11], ["3-4", 20, 16], ["4-5", 19, 26], ["5-6", 15, 28], ["6-7", 8, 18], ["7-8", 5, 9]]}],
    ),
    "P3": dict(
        planteo=("Una industria química quiere mejorar la rigidez de un determinado PVC cambiando la composición química "
                 "utilizada en la fabricación. Se realiza una prueba piloto con una nueva composición química con 12 piezas "
                 "prototipo, obteniendo los siguientes resultados de rigidez (medido en Kg/mm² de plasticidad del material): "
                 "55,1 - 55,8 - 56,0 - 54,9 - 55,0 - 56,9 - 55,2 - 55,2 - 55,9 - 56,1 - 56,2 - 55,7"),
        incisos=[("a", "Estimar la rigidez promedio y el desvío estándar en las piezas con la nueva composición química. "
                       "(Tomar un NC = 99%)"),
                 ("b", "¿Cuántas piezas prototipo más se deberán fabricar con la nueva composición química para reducir en "
                       "un 45% la relación entre los límites de estimación del desvío estándar calculado anteriormente?")],
        tablas=None,
    ),
}


def _res(k):
    e = EJ[k]
    an = analizar(e["planteo"], e["incisos"], tablas=e["tablas"])
    return an, resolver(an)


def test_P1_recta_validacion_y_contribucion_marginal_maxima():
    an, (a, b) = _res("P1")
    assert an.incisos[0].tipo == "recta" and an.incisos[0].params.get("validar") and an.incisos[0].params.get("rho2")
    assert "8,2249 - 0,4644" in a.resumen and "r² = 0,9093" in a.resumen
    # 'para un 5% de riesgo, por cada ppm ... la máxima': límite superior de β1, no un pronóstico en x = 5
    assert an.incisos[1].tipo == "ic_coef" and an.incisos[1].params["alpha"] == pytest.approx(0.05)
    assert b.resumen == "β1 ≤ -0,3748"


def test_P2_comparacion_ajuste_y_proporcion_desde_la_tabla():
    an, (a, b, c) = _res("P2")
    assert an.incisos[0].params["tema"] == "dos_medias" and an.incisos[0].params["delta0_pct"] == pytest.approx(0.1)
    assert "1,1·μ" in a.resumen and "RECHAZA" in a.resumen
    assert "χ² = 122,3748" in b.resumen
    # máximo de 3 ms: no cumplen los de la Marca B por ENCIMA de 3 → r = 97 de 108
    assert (an.incisos[2].params["r"], an.incisos[2].params["n"]) == (97, 108)
    assert c.numeros[0] == pytest.approx(0.8004, abs=1e-4) and c.numeros[1] == pytest.approx(0.9589, abs=1e-4)


def test_P3_nc_99_dos_intervalos_y_piezas_adicionales():
    an, (a, b) = _res("P3")
    assert an.incisos[0].params["alpha"] == pytest.approx(0.01)      # 'NC = 99%'
    assert "IC μ: [55,1283 ; 56,2051]" in a.resumen and "IC σ: [0,385 ; 1,2344]" in a.resumen
    assert b.resumen == "n = 44 (32 más)"
