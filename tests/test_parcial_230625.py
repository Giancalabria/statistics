"""2° parcial del 23/06/2025 (tema 4), problema 2: dos máquinas con tabla de clases.

Practicado el 02/11/2026: las reglas leían 2b («mínima diferencia porcentual») como χ² y las dos IA dejaban 2c («¿se
ajusta a un modelo Normal?») como no soportado. Valores controlados con scipy."""

import json
from pathlib import Path

from asistente.interpretar import corregir_incisos_de_ajuste
from interprete.analizador import analizar
from interprete.modelo import Analisis, Inciso
from interprete.resolver import resolver

EX = {x["id"]: x for x in json.loads((Path(__file__).resolve().parent.parent / "datos" / "examenes_reales.json")
                                     .read_text(encoding="utf-8")) if x["id"] == "Q2"}


def test_minima_diferencia_porcentual_a_esperar_en_tabla_de_clases():
    ex = EX["Q2"]
    an = analizar(ex["planteo"], [tuple(i) for i in ex["incisos"]], tablas=ex["tablas"])
    res = [r.resumen for r in resolver(an)]
    assert "NO rechaza" in res[0]
    # el de mayor media (B) va primero: h = μB/μA = 1,0037 (0,37%), cota inferior con α entero
    assert an.incisos[1].params["tema"] == "dos_medias" and an.incisos[1].params["cota"] == "inf"
    assert "1,0037" in res[1]
    assert "2,2167" in res[2]


def test_inciso_que_pregunta_si_se_ajusta_es_bondad_de_ajuste_aunque_la_ia_diga_otra_cosa():
    an = Analisis(planteo="", tema="dos_medias")
    an.incisos = [Inciso(letra="a", texto="¿Existen diferencias en más de 0,05 ml?", tipo="ensayo"),
                  Inciso(letra="c", texto="Con un 5% de riesgo, ¿se puede afirmar que el llenado de la máquina "
                                          "\"A\" se ajusta a un modelo Normal?", tipo="no_soportado",
                         params={"alpha": 0.05, "cota": "inf", "tail": "derecha"})]
    assert corregir_incisos_de_ajuste(an) == ["c"]
    assert an.incisos[1].tipo == "ensayo"
    assert an.incisos[1].params == {"tema": "chi_ajuste", "alpha": 0.05}
    assert an.incisos[0].tipo == "ensayo" and "tema" not in an.incisos[0].params


def test_solo_es_bondad_de_ajuste_si_nombra_un_modelo_y_no_es_regresion():
    def inc(texto, tema="dos_medias"):
        an = Analisis(planteo="", tema=tema)
        an.incisos = [Inciso(letra="a", texto=texto, tipo="ensayo")]
        return corregir_incisos_de_ajuste(an)
    assert inc("Puede garantizar que el tiempo de respuesta del disyuntor \"Marca A\", se ajusta a la ley Exponencial.")
    assert inc("¿Los datos de la máquina B siguen una distribución de Poisson?")
    assert not inc("¿El proceso se ajusta a las especificaciones?", tema="proporcion")
    assert not inc("¿Los datos se ajustan a un modelo lineal?")
    assert not inc("¿Se ajusta a un modelo exponencial?", tema="regresion")


def test_el_chat_distingue_enunciado_de_pregunta():
    from asistente.explicar import parece_enunciado
    for e in json.loads((Path(__file__).resolve().parent.parent / "datos" / "examenes_reales.json").read_text("utf-8")):
        texto = e["planteo"] + "\n" + "\n".join(f"{l}) {t}" for l, t in (e["incisos"] or []))
        for tb in e["tablas"] or []:      # pegado como en el chat: la tabla va en el mismo texto
            texto += "\n" + " | ".join(tb["columnas"]) + "\n" + "\n".join(" | ".join(map(str, f)) for f in tb["filas"])
        assert parece_enunciado(texto), e["id"]
    assert parece_enunciado("Calcular los límites de confianza del 90% de la fracción defectuosa, si de un proceso "
                            "productivo se tomó una muestra de 10 unidades en la que hubo 2 defectuosas.")
    for pregunta in ("¿Por qué en el ensayo de p se usa la binomial y no la normal?",
                     "explicame el β del inciso b, me dio 0,3892 con n = 360 y p = 0,35",
                     "Revisá mi respuesta: H0: p ≥ 0,40, n = 360, rechazo si r ≤ 128, β = 0,3892. ¿Está bien "
                     "redactado así para el examen? Lo escribí como lo entregaría.",
                     "qué es el criterio de Mermoz"):
        assert not parece_enunciado(pregunta), pregunta


def test_enunciado_con_preguntas_para_la_ia_es_un_pedido():
    from asistente.explicar import parece_enunciado
    texto = ("Se ha lanzado una campaña publicitaria sobre un jabón en polvo cuya penetración en el mercado era del "
             "12%. Se establece una probabilidad de 0,01 de tomar una decisión errónea y, si hay un aumento de 3 "
             "puntos, de 0,10.\nb) Calcular la probabilidad de efectuar otra campaña con un aumento de 2 puntos.\n\n"
             "Escribí solo esto, sin hacer cuentas:\n1. p₀ = ?\n2. ¿Pesimista u optimista?\n5. p₁ = ?")
    assert not parece_enunciado(texto)
    assert parece_enunciado(texto.split("\n\nEscrib")[0])
