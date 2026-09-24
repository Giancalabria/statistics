"""Intérprete de enunciados: se prueba con ejercicios reales de la Guía de Problemas.

Cada caso de punta a punta compara contra la respuesta (`Resp:`) o la resolución
de la guía, así que si una regla nueva rompe un ejercicio que ya andaba, salta acá.
"""

import pytest

from interprete.analizador import analizar, separar_incisos
from interprete.buscador import buscar
from interprete.editor import a_texto, de_texto
from interprete.glosario import buscar_frases
from interprete.resolver import resolver
from interprete.texto import buscar_listas, buscar_numeros, fmt, normalizar


# ---------------------------------------------------------------------------
# Texto y números
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("crudo, valor", [
    ("1.250", 1250.0), ("2,5217", 2.5217), ("1.167,88", 1167.88), ("0.3222", 0.3222), ("15", 15.0), ("1/37", 1 / 37),
])
def test_numeros_formato_argentino(crudo, valor):
    n = buscar_numeros(f"valor {crudo} kg")[0]
    assert n.valor == pytest.approx(valor)


def test_porcentaje_como_fraccion():
    n = buscar_numeros("con un 95% de confianza")[0]
    assert n.pct and n.fraccion == pytest.approx(0.95)


def test_lista_de_datos_y_filas_indice():
    listas = buscar_listas("ventas: 15,4 – 18,5 – 16,3 – 19,2. Persona 1 2 3 4 Zapato: 12 7 18 15")
    assert [l.valores for l in listas] == [[15.4, 18.5, 16.3, 19.2], [12.0, 7.0, 18.0, 15.0]]


def test_normalizar_conserva_longitud():
    s = "Estadística Aplicada ñandú"
    assert len(normalizar(s)) == len(s)


def test_fmt_coma_decimal():
    assert fmt(1234567.5) == "1.234.567,5"
    assert fmt(0.05) == "0,05"


def test_editor_ida_y_vuelta():
    assert de_texto(a_texto(0.05, "float"), "float") == pytest.approx(0.05)
    assert de_texto("5%", "float") == pytest.approx(0.05)
    assert de_texto("15,4 ; 18,5 ; 16,3", "lista") == [15.4, 18.5, 16.3]
    assert de_texto("1 2\n3 4", "tabla") == [[1, 2], [3, 4]]
    assert de_texto("", "float") is None


def test_separar_incisos():
    planteo, incs = separar_incisos("Texto del planteo. a) Estimar la media. b) ¿Cuántos más? c) Otra.")
    assert planteo == "Texto del planteo."
    assert [l for l, _ in incs] == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# Casos de la guía (de punta a punta)
# ---------------------------------------------------------------------------

I_1 = ("Una máquina llenadora de latas de café dosifica cantidades variables con distribución Normal de desvío "
       "estándar 15 gramos. A intervalos regulares se toman muestras de 10 envases con el fin de estimar la "
       "dosificación media. Una de estas muestras arrojó una media de 246 gramos.",
       ["Estimar la dosificación media con un 90% de confianza.",
        "¿Cuántos envases más habría que pesar para poder obtener una estimación cuyo error de muestreo sea de 5 gramos?"])


def test_guia_I_1_ic_y_delta_n():
    an = analizar(*I_1)
    assert an.tema == "media"
    assert an.datos["sigma_conocido"] is True
    assert (an.datos["n"], an.datos["xbar"], an.datos["desvio"]) == (10, 246, 15)
    assert [i.tipo for i in an.incisos] == ["ic", "n"]
    a, b = resolver(an)
    assert a.numeros[:2] == pytest.approx([238.19, 253.81], abs=0.01)
    assert b.numeros == [25, 15]          # n = 25 -> 15 envases más


def test_guia_I_3_tabla_de_frecuencias_e_idem():
    """Ejercicio resuelto en la guía: n correcto con σ; con S hacen falta 12 más."""
    an = analizar(
        "En una zona de Capital Federal se realizará un muestreo sobre una población compuesta por negocios "
        "minoristas, con el objeto de estimar el número medio de empleados por establecimiento. La experiencia en "
        "encuestas por muestreo indica que el desvío estándar es de 1,2 empleados por establecimiento. Se han "
        "obtenido los siguientes resultados muestrales: Cantidad de empleados Número de establecimientos "
        "0 2 1 4 2 5 3 6 4 4 5 2",
        ["¿El tamaño de muestra extraído es correcto si se pretende un error muestral de ± 0,5 empleados, y un "
         "nivel de confianza en la estimación del 95%?",
         "Estimar el número medio de empleados para todos los negocios minoristas.",
         "Ídem a) y b) considerando que el desvío histórico no se conoce."])
    assert len(an.datos["datos"]) == 23
    r = resolver(an)
    assert r[0].numeros[0] == 23
    assert r[1].numeros[:2] == pytest.approx([2.03, 3.02], abs=0.01)
    assert r[2].numeros == [35, 12]
    assert r[3].numeros[:2] == pytest.approx([1.89, 3.15], abs=0.01)


def test_guia_I_11_ensayo_beta_y_n_por_potencia():
    an = analizar(
        "Un cliente recibe habitualmente una partida de medidores eléctricos que, según las especificaciones del "
        "contrato, el promedio de las pérdidas debe ser menor o igual a 1 watt. Una muestra de 10 medidores, de una "
        "partida recién recibida, arroja una pérdida media de 1,06 watts. Se sabe, además, por experiencia anterior, "
        "que las pérdidas se distribuyen Normalmente con un desvío de 0,1 watts.",
        ["Asumiendo un 10% el riesgo de rechazar la partida indebidamente, ¿puede aceptarse la misma?",
         "¿Cuál es la probabilidad de aceptar una partida cuya pérdida media sea de 1,05 watts?",
         "¿Cuál debería ser el tamaño de muestra si se pretende que la probabilidad anterior valga 0,10?"])
    assert an.criterio == "optimista"
    assert an.incisos[0].params["tail"] == "derecha"
    a, b, c = resolver(an)
    assert "RECHAZA" in a.resumen and "NO" not in a.resumen
    assert b.numeros[0] == pytest.approx(0.3831, abs=0.002)   # β
    assert c.numeros[0] == 27


def test_guia_I_16_diseno_con_dos_probabilidades():
    an = analizar(
        "Se desea establecer un sistema de muestreo periódico para controlar la resistencia a la rotura de unas "
        "piezas de “Dural”, de modo tal que se cumplan las siguientes condiciones: i) Si la resistencia media es de "
        "38 kg/mm², detener el proceso productivo con probabilidad 0,1; ii) si dicho parámetro vale 37 kg/mm², "
        "detener el proceso con probabilidad 0,95. Se sabe que esta variable tiene un desvío estándar de 1,3 kg/mm².",
        ["Indicar la hipótesis nula apropiada, su condición de rechazo, el tamaño de la muestra a tomar y la regla "
         "de decisión.", "Calcular la probabilidad de detectar que la resistencia media vale 37,5 kg/mm 2."])
    assert (an.datos["alpha"], an.datos["beta"]) == pytest.approx((0.1, 0.05))
    assert (an.datos["mu0"], an.datos["mu1"]) == (38, 37)
    a, b = resolver(an)
    assert a.numeros[:2] == pytest.approx([15, 37.57], abs=0.01)
    assert b.numeros[0] == pytest.approx(0.5824, abs=0.001)   # potencia


def test_guia_I_34_poblacion_finita_y_total():
    an = analizar(
        "Por investigaciones anteriores se sabe que el peso promedio de los cerdos de 6 semanas es de 45 kg con un "
        "σ = 8 kg. Se ensaya un nuevo tipo de alimentación con una población total de 1.200 cerdos de un "
        "establecimiento, seleccionando una muestra al azar de 36 de ellos arrojando un peso medio de 47 Kg. Se "
        "considera que el desvío histórico se mantiene.",
        ["¿Se puede decir que se ha incrementado el peso promedio de los cerdos?",
         "Estimar con un 90% de confianza el peso promedio de la población de cerdos de dicho establecimiento.",
         "Estimar con un 90% de confianza el peso total de la población de cerdos de dicho establecimiento."])
    assert (an.datos["mu0"], an.datos["xbar"], an.datos["N"], an.datos["n"]) == (45, 47, 1200, 36)
    a, b, c = resolver(an)
    assert any(abs(x - 0.0639) < 0.0002 for x in a.numeros)   # valor a posteriori de la guía: 6,39%
    assert b.numeros[:2] == pytest.approx([44.84, 49.16], abs=0.01)
    assert c.numeros[0] == pytest.approx(53808, rel=1e-4)


def test_guia_II_4_ic_desvio_y_garcia():
    an = analizar("En una muestra de 15 tubos fluorescentes pertenecientes al último lote de producción, se obtuvo "
                  "que la desviación estándar de la duración ha sido de 120 horas.",
                  ["Estimar el desvío estándar de la duración de todos los tubos con un riesgo del 10%.",
                   "Calcular el tamaño de muestra necesario para reducir en un 30% la relación entre los límites "
                   "del desvío anterior."])
    assert an.tema == "varianza"
    a, b = resolver(an)
    assert a.numeros[2:4] == pytest.approx([92.25, 175.17], abs=0.01)
    assert b.numeros[0] == 69


def test_guia_II_12_valor_critico_y_n_por_potencia():
    an = analizar(
        "El control de la variabilidad de los pesos de suelas de goma se realiza tomando muestras de suelas "
        "periódicas de 10 unidades, deteniendo el proceso tecnológico en caso de que el desvío poblacional de los "
        "pesos tome un valor mayor que el desvío estipulado en la especificación. El valor considerado adecuado por "
        "especificación para el desvío de la población es de 5 gramos como máximo y, de ser así, la probabilidad de "
        "detener el proceso indebidamente se ha establecido en 0,05.",
        ["Calcular el valor crítico ( Sc) del desvío estándar muestral.",
         "¿Cuál es la probabilidad de no detectar que el desvío es de 8 gramos?",
         "¿Cuántas suelas más se deberán tomar si se quiere que la probabilidad anterior valga 0,05?"])
    a, b, c = resolver(an)
    assert a.numeros[0] == pytest.approx(6.86, abs=0.01)
    assert b.numeros[0] == pytest.approx(0.3222, abs=0.001)
    assert c.numeros[0] == 27 and c.numeros[-1] == 17


def test_guia_III_4_ic_proporcion_exacto():
    an = analizar("En un estudio de muestreo de trabajo se indica que, sobre una muestra de 600 observaciones, una "
                  "máquina se mantuvo inactiva el 10% del tiempo total. ¿Cuáles serán los límites de confianza para "
                  "la proporción de tiempo inactivo? (Tomar un Nivel de Confianza de 0,95).")
    assert an.tema == "proporcion"
    (r,) = resolver(an)
    assert r.numeros[:2] == pytest.approx([0.0771, 0.1269], abs=0.0002)


def test_cota_unilateral_proporcion():
    """'La fracción defectuosa máxima con una probabilidad de 0,95' es un límite unilateral superior."""
    an = analizar("El control consiste en tomar una muestra de 25 unidades. En una de estas muestras se encontraron "
                  "3 unidades defectuosas.",
                  ["La fracción defectuosa máxima que hay en la población con una probabilidad de 0,95."])
    assert an.incisos[0].tipo == "ic" and an.incisos[0].params["cota"] == "sup"
    (r,) = resolver(an)
    assert r.numeros[0] == pytest.approx(0.2819, abs=0.001)   # guía III-2 b): 28,18%


def test_datos_faltantes_se_informan_sin_romper():
    an = analizar("Estimar la media con un 95% de confianza.")
    (r,) = resolver(an)
    assert r.errores and "Falta" in r.errores[0]


# ---------------------------------------------------------------------------
# Buscador y glosario
# ---------------------------------------------------------------------------

def test_buscador_encuentra_el_mismo_ejercicio():
    sim, ej = buscar(I_1[0] + " " + " ".join(I_1[1]), k=1)[0]
    assert ej["id"] == "I-1"


def test_buscador_solo_parcial():
    for _, ej in buscar("tabla de contingencia independencia chi cuadrado", k=5, solo_parcial=True):
        assert ej["tema"] in ("I", "II", "III")


def test_glosario_detecta_frases():
    frases = [f for f, _ in buscar_frases("¿Cuántos envases más habría que pesar? el desvío histórico es 2")]
    assert any("más" in f for f in frases)
    assert any("histórico" in f for f in frases)


# ---------------------------------------------------------------------------
# Final anticipado 14/09/2026 (Tema 3): enunciados con trampas
# ---------------------------------------------------------------------------

EXAMEN_P1 = ("Se desea establecer un sistema de control para la resistencia a la tracción, la cual debe ser lo más alta "
      "posible, de un hilo de alambre para cuerda de tensión, de modo tal que se cumplan las siguientes condiciones: "
      "Si la resistencia promedio es de 2,0 Tn no detener el proceso con probabilidad de 0,05; pero si la resistencia "
      "promedio es de 3,2 Tn, detener el proceso con probabilidad de 0,10. Se sabe que esta variable tiene un desvío "
      "estándar de 0,65 Tn.")
EXAMEN_I1 = ["Indicar la hipótesis nula apropiada a esta situación, la condición de rechazo y la regla de decisión.",
      "¿Cuál es la probabilidad de no detener el proceso cuando la resistencia promedio es de 1,5 Tn?"]

EXAMEN_P2 = ("Una empresa desea adquirir una nueva máquina para la elaboración de cierto tipo de piezas. La decisión de compra "
      "se basará en el rendimiento promedio de la máquina medido en el tiempo expresado en minutos/pieza y su desvío "
      "estándar. De manera que si el tiempo promedio es inferior a 1,5 minutos/pieza y su desvío es inferior a 0,09 "
      "minutos/pieza, la máquina se comprará. Para la decisión de compra, la empresa le pide al fabricante de la máquina "
      "realizar una prueba piloto con una muestra de 20 piezas elegidas al azar obteniendo los siguientes resultados "
      "(medidos en minutos/pieza):\n"
      "1,01 - 1,08 - 1,01 - 0,99 - 1,01 - 1,10 - 0,98 - 1,05 - 1,09 - 1,10\n"
      "1,10 - 1,07 - 0,98 - 1,09 - 1,07 - 1,05 - 1,05 - 1,06 - 1,02 - 1,01")
EXAMEN_I2 = ["¿Considera que los datos son concluyentes como para recomendar la compra de la máquina? Tomar un riesgo del 1%",
      "¿Cuál es la probabilidad de detectar que el desvío estándar es de 0,05 minutos/pieza?",
      "¿Cuántas barras más se deberán probar para que la probabilidad anterior valga 0,99?",
      "Estimar, con un 95% de seguridad, la resistencia promedio y el desvío estándar de toda la partida."]



def test_examen_control_detener_en_orden_invertido():
    """Da primero el valor MALO con 'no detener' y α > β: igual H0 es μ = 3,2 (el proceso anda bien)."""
    an = analizar(EXAMEN_P1, EXAMEN_I1)
    assert an.criterio == "optimista"
    assert (an.datos["mu0"], an.datos["mu1"]) == (3.2, 2.0)
    assert an.datos["alpha"] == pytest.approx(0.10) and an.datos["beta"] == pytest.approx(0.05)
    a, b = resolver(an)
    assert a.numeros[:2] == [3, pytest.approx(2.7191, abs=1e-4)]
    assert "detiene" in " ".join(a.pasos)
    assert b.numeros[0] == pytest.approx(0.00058, abs=2e-5)  # P(no detener | μ = 1,5)


def test_examen_doble_condicion_media_y_desvio():
    an = analizar(EXAMEN_P2, EXAMEN_I2)
    assert an.datos["doble"] and an.datos["mu0"] == 1.5 and an.datos["sigma0"] == 0.09
    a, b, c, d = resolver(an)
    assert a.resumen.count("RECHAZA H0") == 2 and "se recomienda" in a.conclusion
    assert b.numeros[0] == pytest.approx(0.8304, abs=1e-4)
    assert c.numeros[0] == 34 and c.numeros[-1] == 14
    assert d.numeros[:2] == [pytest.approx(1.0265, abs=1e-4), pytest.approx(1.0655, abs=1e-4)]
    assert pytest.approx(0.0316, abs=1e-4) in d.numeros and pytest.approx(0.0608, abs=1e-4) in d.numeros


def test_beta_del_lado_de_h0_no_se_llama_beta():
    an = analizar(EXAMEN_P1, [EXAMEN_I1[0], "¿Cuál es la probabilidad de no detener el proceso cuando la "
                                            "resistencia promedio es de 3,5 Tn?"])
    b = resolver(an)[1]
    assert "β" not in b.conclusion and "no rechazar" in b.conclusion


def test_coma_decimal_en_textos_del_solver():
    from interprete.resolver import _coma
    assert _coma("x̄c = 37.5698") == "x̄c = 37,5698"


def test_cambiar_criterio_invierte_el_diseno_y_vuelve():
    from interprete.analizador import cambiar_criterio
    an = analizar(EXAMEN_P1, EXAMEN_I1)
    assert cambiar_criterio(an, "pesimista")
    assert (an.datos["mu0"], an.datos["alpha"], an.datos["beta"]) == (2.0, 0.05, 0.1)
    a, b = resolver(an)
    assert a.numeros[:2] == [3, pytest.approx(2.6173, abs=1e-4)] and "sigue" in a.conclusion
    assert b.numeros[0] == pytest.approx(0.0015, abs=1e-4)  # 'no detener' ahora es rechazar H0
    cambiar_criterio(an, "optimista")
    assert resolver(an)[0].numeros[:2] == [3, pytest.approx(2.7191, abs=1e-4)]


def test_cambiar_criterio_da_vuelta_las_colas():
    from interprete.analizador import cambiar_criterio
    an = analizar(EXAMEN_P2, EXAMEN_I2)
    cambiar_criterio(an, "optimista")
    assert an.incisos[0].params["tail"] == "derecha"
    assert "NO rechaza" in resolver(an)[0].resumen


def test_presentacion_justifica_h0_y_explica_distribuciones():
    """El examen pide en cada problema justificar H0 y explicar las distribuciones."""
    a, b = resolver(analizar(EXAMEN_P1, EXAMEN_I1))
    texto = " ".join(a.pasos)
    assert "Justificación de H0" in texto and "Criterio optimista" in texto and "se detiene el proceso | μ = 3,2" in texto
    assert "x̄ ~ N(μ; σ²/n)" in texto
    assert a.pasos.index(next(p for p in a.pasos if p.startswith("**Justificación"))) < \
        a.pasos.index(next(p for p in a.pasos if p.startswith("**Hipótesis**")))
    assert "H0: μ ≥ 3,2" in texto  # coma decimal
    d = resolver(analizar(EXAMEN_P2, EXAMEN_I2))[3]
    assert "t de Student" in " ".join(d.pasos) and "χ²" in " ".join(d.pasos)


def test_ensayo_sale_en_los_7_pasos_de_la_catedra():
    an = analizar("Una máquina llena bolsas con distribución normal. Se sabe que el desvío es 15 gramos. Se toma una "
                  "muestra de 25 bolsas y se obtiene una media de 506 gramos. Con un riesgo del 5%, ¿se puede afirmar "
                  "que el peso medio supera los 500 gramos?", [])
    a = resolver(an)[0]
    numerados = [p[2] for p in a.pasos if p.startswith("**") and p[2].isdigit() and p[3:6] == " · "]
    assert numerados == ["1", "2", "3", "4", "5", "6"]
    rd = next(p for p in a.pasos if p.startswith("**5 · Regla de decisión"))
    assert "n = 25" in rd and "504,9346" in rd and "En caso contrario" in rd
    assert a.conclusion.startswith("A un nivel de significación del 5%, existe evidencia estadística suficiente")
    assert "Por consiguiente" in a.conclusion and "acepta" not in a.conclusion


def test_conclusion_formal_usa_la_accion_del_sistema_de_control():
    an = analizar(EXAMEN_P2, EXAMEN_I2)
    a = resolver(an)[0]
    assert a.conclusion.count("A un nivel de significación") == 2
    assert sum(p.startswith("**5 · Regla de decisión") for p in a.pasos) == 2
