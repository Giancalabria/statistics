"""Lo que se agregó para que la IA llegue al resultado correcto (sin Ollama: lecturas y JSON armados a mano)."""

import pytest

from asistente.consenso import Consenso, Lectura, combinado, igual, votar
from asistente.esquema import desde_dict
from asistente.interpretar import completar_con_reglas, con_tablas
from interprete.analizador import analizar
from interprete.resolver import Resultado, resolver

TABLA = {"titulo": "", "columnas": ["Tiempo (ms)", "Marca A", "Marca B"],
         "filas": [["2-3", 35, 11], ["3-4", 20, 16], ["4-5", 19, 26], ["5-6", 15, 28], ["6-7", 8, 18], ["7-8", 5, 9]]}


def test_la_tabla_llega_al_prompt_de_la_ia():
    texto = con_tablas("Planteo", [TABLA])
    assert "Tabla de datos:" in texto and "2-3 | 35 | 11" in texto


def test_beta_mayor_a_medio_es_la_potencia():
    an, avisos = desde_dict({"tema": "proporcion", "datos": {"p0": 0.4, "alpha": 0.05},
                             "incisos": [{"letra": "a", "tipo": "diseno", "params": {"p1": 0.3, "beta": 0.99}}]})
    assert an.incisos[0].params["beta"] == pytest.approx(0.01) and any("potencia" in a for a in avisos)


def test_modelos_como_texto_en_datos_y_en_incisos():
    an, _ = desde_dict({"tema": "chi_ajuste", "datos": {"modelos": "['poisson']"},
                        "incisos": [{"letra": "a", "tipo": "ensayo", "params": {"modelos": "normal y weibull"}}]})
    assert an.datos["modelos"] == ["poisson"] and set(an.incisos[0].params["modelos"]) == {"normal", "weibull"}


def test_el_ensayo_despues_del_diseno_usa_la_cola_del_plan():
    an, _ = desde_dict({"tema": "media", "datos": {"mu0": 3.62, "desvio": 0.45, "alpha": 0.01, "beta": 0.05},
                        "incisos": [{"letra": "a", "tipo": "diseno", "params": {"mu1": 4.15, "tail": "derecha"}},
                                    {"letra": "b", "tipo": "ensayo", "params": {"tail": "izquierda"}}]})
    assert an.incisos[1].params["tail"] == "derecha"


def test_las_cuentas_sobre_la_tabla_las_pone_el_programa():
    planteo = "Se registraron los tiempos de respuesta de dos marcas de disyuntores."
    lista = [("a", "¿Se puede afirmar que el tiempo de una marca es superior al de la otra por más del 10%?")]
    an, _ = desde_dict({"tema": "dos_medias", "datos": {"xbar1": 9.99, "n1": 3},
                        "incisos": [{"letra": "a", "tipo": "ensayo", "params": {"tail": "derecha"}}]}, planteo)
    an.tablas = [TABLA]
    completar_con_reglas(an, planteo, lista, [TABLA])
    assert an.datos["n1"] == 102 and an.datos["xbar1"] == pytest.approx(4.0686, abs=1e-4)   # no los de la IA
    assert an.incisos[0].params["tail"] == "derecha"                                       # la cola sí es de la IA


def _res(resumen, error=""):
    return Resultado(resumen=resumen, errores=[error] if error else [])


def test_igual_exige_la_misma_hipotesis_ademas_de_la_decision():
    assert igual(_res("H0: δ ≤ 0,05; dc = 0,1117; NO rechaza H0"), _res("H0: δ ≤ 0,05; dc = 0,1117; NO rechaza H0"))
    assert not igual(_res("H0: δ ≤ 0; dc = 0,0617; RECHAZA H0"), _res("H0: δ ≤ 0,05; dc = 0,1117; RECHAZA H0"))
    assert not igual(_res("faltan datos", "Falta n"), _res("faltan datos", "Falta n"))


def test_votacion_y_planteo_combinado():
    planteo = "Se midió la rigidez de 12 piezas: 55,1 - 55,8 - 56,0 - 54,9 - 55,0 - 56,9 - 55,2 - 55,2 - 55,9 - 56,1 - 56,2 - 55,7"
    incisos = ["Estimar la rigidez promedio con un 95% de confianza.", "Estimar el desvío con un 95% de confianza."]
    buena = analizar(planteo, incisos)
    mala = analizar(planteo, incisos)
    mala.incisos[0].params["alpha"] = 0.01                      # otra lectura con otro α en el inciso a)
    lecturas = [Lectura(f, an, resolver(an)) for f, an in (("reglas", mala), ("ia", buena), ("ia_razonada", buena))]
    votos = votar(lecturas)
    assert [v.estado for v in votos] == ["consenso", "consenso"]
    assert {v.fuente for v in votos[0].grupos[0]} == {"ia", "ia_razonada"}
    an = combinado(Consenso(lecturas, votos))
    assert an.incisos[0].params.get("alpha") != 0.01
    assert resolver(an)[0].resumen == resolver(buena)[0].resumen
    # el alumno elige otra lectura para un inciso sin acuerdo
    an2 = combinado(Consenso(lecturas, votos), {"a": "reglas"})
    assert resolver(an2)[0].resumen == resolver(mala)[0].resumen


def test_la_relacion_entre_limites_es_del_desvio():
    # 1er parcial 29/04/25: las dos lecturas de IA dejaron el inciso en 'media' y calcularon el n del error
    texto = ("¿Cuántos cerdos más se deberán pesar para reducir en un 15% la relación de la estimación del desvío "
             "estándar de los pesos calculada anteriormente?")
    an, avisos = desde_dict({"tema": "media", "datos": {"alpha": 0.01},
                             "incisos": [{"letra": "c", "tipo": "n", "params": {"reduccion": 0.15}}]}, "", {"c": texto})
    assert an.incisos[0].params["tema"] == "varianza"
