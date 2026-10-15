"""Asistente de IA sin modelo: el cliente de Ollama se reemplaza por respuestas fijas.

Se prueba lo que no depende del modelo: el esquema, la validación del JSON, la regla de "la IA solo aplica lo
que mejora la resolución", la búsqueda en los apuntes y el control de números inventados.
"""

import json

import pytest

from asistente import cliente, contexto, explicar
from asistente import interpretar as interp
from asistente.esquema import CLAVES_TEMA, a_dict, desde_dict, json_schema
from interprete.modelo import TEMAS
from interprete.analizador import analizar
from interprete.resolver import resolver

PLANTEO_MEDIA = ("Una máquina llenadora de latas de café dosifica cantidades variables con distribución Normal de "
                 "desvío estándar 15 gramos. A intervalos regulares se toman muestras de 10 envases con el fin de "
                 "estimar la dosificación media. Una de estas muestras arrojó una media de 246 gramos.")
INCISOS_MEDIA = ["Estimar la dosificación media con un 90% de confianza.",
                 "¿Cuántos envases más habría que pesar para poder obtener una estimación cuyo error de muestreo "
                 "sea de 5 gramos?"]


@pytest.fixture
def modelo_falso(monkeypatch):
    """Hace que cliente.chat devuelva lo que el test pida (y guarda los mensajes que recibió)."""
    llamadas = []

    def instalar(respuesta):
        def chat(mensajes, **kw):
            llamadas.append((mensajes, kw))
            if kw.get("stream"):
                return iter([respuesta[:10], respuesta[10:]])
            return respuesta if isinstance(respuesta, str) else json.dumps(respuesta)
        monkeypatch.setattr(cliente, "chat", chat)
        return llamadas
    return instalar


# ---------------------------------------------------------------- esquema

def test_esquema_cubre_el_catalogo():
    js = json_schema()
    assert "regresion" in js["properties"]["tema"]["enum"]
    assert "pronostico" in js["properties"]["incisos"]["items"]["properties"]["tipo"]["enum"]
    assert js["properties"]["datos"]["properties"]["alpha"] == {"type": "number"}


def test_las_claves_por_tema_estan_en_el_catalogo():
    assert set(CLAVES_TEMA) == set(TEMAS) - {"desconocido"}
    assert "xbar" in CLAVES_TEMA["media"][0] and "xbar1" not in CLAVES_TEMA["media"][0]


def test_las_reglas_de_la_guia_entran_en_el_esquema_de_su_tema():
    """Todo lo que arman las reglas en la guía (verificado) tiene que caber en la rama de su tema."""
    from herramientas.evaluar_guia import GUIA, entradas
    for ej in GUIA:
        planteo, incisos = entradas(ej)
        d = a_dict(analizar(planteo, incisos, tablas=ej.get("tablas") or None))
        datos, params = CLAVES_TEMA[d["tema"]]
        assert set(d["datos"]) <= set(datos), (ej["id"], set(d["datos"]) - set(datos))
        for inc in d["incisos"]:
            assert set(inc["params"]) <= set(params), (ej["id"], set(inc["params"]) - set(params))


def test_claves_de_otro_tema_se_traducen_o_descartan():
    an, avisos = desde_dict({
        "tema": "media",
        "datos": {"n": 20, "xbar1": 38, "sigma_pob1": 4.2, "nombre_x": "peso"},
        "incisos": [{"letra": "a", "tipo": "ic", "params": {"alpha": 0.05}},
                    {"letra": "b", "tipo": "n", "params": {"e": 1}}]})
    assert an.datos == {"n": 20, "xbar": 38, "desvio": 4.2, "sigma_conocido": True}
    assert any("nombre_x" in a for a in avisos)
    assert an.incisos[1].params == {"e": 1, "alpha": 0.05}      # α heredado del inciso a)
    assert [r.numeros for r in resolver(an)][1]                 # ahora b) se resuelve


def test_la_herencia_no_pisa_ni_arrastra_la_cola_a_un_ensayo():
    an, _ = desde_dict({
        "tema": "media", "datos": {"n": 36, "xbar": 10, "desvio": 2, "sigma_conocido": True, "mu0": 9},
        "incisos": [{"letra": "a", "tipo": "ensayo", "params": {"alpha": 0.01, "tail": "derecha"}},
                    {"letra": "b", "tipo": "ensayo", "params": {"alpha": 0.05}},
                    {"letra": "c", "tipo": "ic", "params": {"tema": "proporcion", "r": 3, "n": 40}}]})
    assert an.incisos[1].params == {"alpha": 0.05}
    assert an.incisos[2].params["alpha"] == 0.05 and "tail" not in an.incisos[2].params


def test_ida_y_vuelta_de_un_analisis():
    an = analizar(PLANTEO_MEDIA, INCISOS_MEDIA)
    d = json.loads(json.dumps(a_dict(an)))
    assert d["incisos"][0]["params"]["alpha"] == 0.1          # sin ruido de punto flotante
    vuelta, avisos = desde_dict(d, an.planteo)
    assert not avisos
    assert vuelta.tema == "media" and vuelta.datos["xbar"] == 246
    assert [r.numeros for r in resolver(vuelta)] == [r.numeros for r in resolver(an)]


def test_validacion_corrige_y_descarta():
    an, avisos = desde_dict({
        "tema": "media",
        "datos": {"n": "10", "desvio": -3, "alpha": 5, "inventada": 1, "xbar": "246,5"},
        "incisos": [{"letra": "a)", "tipo": "pronostico", "params": {"tail": "Derecha", "beta": 150}}],
    })
    assert an.datos["n"] == 10 and an.datos["xbar"] == 246.5
    assert an.datos["alpha"] == pytest.approx(0.05)            # 5 → 5%
    assert "desvio" not in an.datos and "inventada" not in an.datos
    inc = an.incisos[0]
    assert inc.letra == "a" and inc.tipo == "no_soportado"      # 'pronostico' no es de medias
    assert inc.params == {"tail": "derecha"}                    # β = 150 no es una probabilidad
    assert len(avisos) == 4


# ---------------------------------------------------------------- híbrido

def test_si_las_reglas_resuelven_no_se_consulta(modelo_falso):
    llamadas = modelo_falso({"tema": "varianza", "datos": {}, "incisos": []})
    r = interp.interpretar(PLANTEO_MEDIA, INCISOS_MEDIA)
    assert not llamadas and not r.usado_ia
    assert r.analisis.tema == "media"


def test_la_ia_no_pisa_lo_que_las_reglas_resuelven(modelo_falso):
    modelo_falso({"tema": "media", "datos": {"n": 10, "desvio": 15, "sigma_conocido": True, "xbar": 250},
                  "incisos": [{"letra": "a", "tipo": "ic", "params": {"alpha": 0.1}},
                              {"letra": "b", "tipo": "n", "params": {"e": 5, "alpha": 0.1}}]})
    r = interp.interpretar(PLANTEO_MEDIA, INCISOS_MEDIA, siempre=True)
    assert r.usado_ia and r.analisis.datos["xbar"] == 246       # se mantiene lo de las reglas
    assert any("246" in s and "250" in s for s in r.sugerencias)
    assert not r.informe


def test_la_ia_completa_un_inciso_que_las_reglas_no_entienden(modelo_falso, monkeypatch):
    real = interp.analizar

    def reglas_que_fallan(planteo, incisos=None, tablas=None, tema=None, **kw):
        an = real(planteo, incisos, tablas=tablas, tema=tema, **kw)
        if tema is None:                                        # simula un inciso que las reglas no clasifican
            an.incisos[1].tipo, an.incisos[1].params = "no_soportado", {}
        return an

    monkeypatch.setattr(interp, "analizar", reglas_que_fallan)
    llamadas = modelo_falso({"tema": "media", "datos": {}, "incisos": [
        {"letra": "a", "tipo": "ic", "params": {}},
        {"letra": "b", "tipo": "n", "params": {"e": 5, "alpha": 0.1}}]})
    r = interp.interpretar(PLANTEO_MEDIA, INCISOS_MEDIA)
    assert llamadas
    b = r.analisis.incisos[1]
    assert b.tipo == "n" and b.params["e"] == 5
    assert any(s.startswith("b) lo completó la IA") for s in r.informe)
    res = resolver(r.analisis)
    assert not res[1].errores


def test_tema_de_la_ia_se_acepta_si_las_reglas_no_lo_detectan(modelo_falso, monkeypatch):
    real = interp.analizar

    def sin_tema(planteo, incisos=None, tablas=None, tema=None, **kw):
        an = real(planteo, incisos, tablas=tablas, tema=tema, **kw)
        if tema is None:
            an.tema = "desconocido"
            for i in an.incisos:
                i.tipo = "no_soportado"
        return an

    monkeypatch.setattr(interp, "analizar", sin_tema)
    modelo_falso({"tema": "media", "datos": {}, "incisos": [{"letra": "a", "tipo": "ic", "params": {}},
                                                           {"letra": "b", "tipo": "n", "params": {}}]})
    r = interp.interpretar(PLANTEO_MEDIA, INCISOS_MEDIA)
    assert r.analisis.tema == "media"
    assert "Tema" in r.informe[0]
    assert all(not x.errores for x in resolver(r.analisis))    # las reglas con el tema forzado sacan los datos


def test_sin_ollama_quedan_las_reglas(monkeypatch):
    def caido(*a, **kw):
        raise cliente.ErrorIA("No se pudo conectar")
    monkeypatch.setattr(cliente, "chat", caido)
    r = interp.interpretar(PLANTEO_MEDIA, INCISOS_MEDIA, siempre=True)
    assert r.error and r.analisis is r.reglas


def test_los_ejemplos_excluyen_el_ejercicio_evaluado():
    texto = PLANTEO_MEDIA + " " + " ".join(INCISOS_MEDIA)
    ids = [e.id for e in interp.ejemplos(texto, k=2)]
    assert "I-1" in ids
    assert "I-1" not in [e.id for e in interp.ejemplos(texto, k=2, excluir=["I-1"])]


def test_json_con_texto_alrededor():
    assert interp._parsear('<think>hmm</think>\nAcá va: {"tema": "media"} listo') == {"tema": "media"}


# ---------------------------------------------------------------- tema forzado en las reglas

def test_analizar_con_tema_forzado():
    an = analizar(PLANTEO_MEDIA, INCISOS_MEDIA, tema="media")
    assert an.tema == "media" and an.razones_tema == ["Tema indicado de antemano: Media de 1 población (μ)."]
    assert analizar(PLANTEO_MEDIA, INCISOS_MEDIA, tema="desconocido").tema == "media"


# ---------------------------------------------------------------- apuntes y verificación

def test_busqueda_en_apuntes():
    frags = contexto.buscar("criterio pesimista optimista hipótesis nula", k=3, fuentes=explicar.APUNTES)
    assert frags and any("riterio" in f.titulo for f in frags)
    assert contexto.buscar("dosificación latas café", k=1, fuentes=("guia",))[0].titulo.startswith("I-1")


def test_numeros_sin_respaldo():
    fuentes = "x̄ = 246, Z = 1,6449, límites 238,19 y 253,81, con 90% de confianza"
    texto = ("Con 90% de confianza (α = 0,1) el intervalo es 238,19 a 253,81; Z vale 1,645 y en el paso 3 "
             "el error es 7,9.")
    assert explicar.numeros_sin_respaldo(texto, fuentes) == ["7,9"]


def test_explicar_arma_el_contexto_con_la_resolucion(modelo_falso):
    llamadas = modelo_falso("La media está entre 238,19 y 253,81.")
    an = analizar(PLANTEO_MEDIA, INCISOS_MEDIA)
    res = resolver(an)
    trozos, fuentes = explicar.explicar(an, res)
    texto = "".join(trozos)
    assert explicar.numeros_sin_respaldo(texto, fuentes) == []
    usuario = llamadas[0][0][1]["content"]
    assert "RESOLUCIÓN DEL SOLVER" in usuario and "253,81" in usuario and "CONVENCIONES" in usuario


def test_modelo_instalado():
    assert cliente.modelo_instalado("qwen3:8b", ["qwen3:8b", "llama3.2:latest"])
    assert cliente.modelo_instalado("llama3.2", ["llama3.2:latest"])
    assert not cliente.modelo_instalado("qwen3:14b", ["qwen3:8b"])


def test_chat_libre_con_material_propio_y_sin_apuntes():
    msgs, frags = explicar.mensajes_pregunta("¿Está bien?", [{"role": "user", "content": "hola"},
                                                            {"role": "assistant", "content": "hola!"}],
                                             ejercicio="RESOLUCIÓN: P(238,19 ≤ μ ≤ 253,81)",
                                             sistema=explicar.SISTEMA_LIBRE, apuntes=False,
                                             adjuntos="Mi conclusión: entre 238 y 254")
    assert frags == []
    sistema = msgs[0]["content"]
    assert sistema.startswith("Sos un asistente experto") and "APUNTES" not in sistema
    assert "Mi conclusión" in sistema and "253,81" in sistema
    assert [m["role"] for m in msgs[1:]] == ["user", "assistant", "user"]


def test_chat_resuelve_un_enunciado_pegado(modelo_falso):
    llamadas = modelo_falso({"tema": "varianza", "datos": {}, "incisos": []})
    r, resultados, texto = explicar.resolver_enunciado(
        PLANTEO_MEDIA + " a) " + INCISOS_MEDIA[0] + " b) " + INCISOS_MEDIA[1])
    assert not llamadas                                          # las reglas alcanzan: no se consulta a la IA
    assert len(resultados) == 2 and "253,81" in texto


def test_leer_adjunto_de_texto():
    assert explicar.leer_adjunto("notas.md", "α = 0,05 ✓".encode("utf-8")) == "α = 0,05 ✓"


def test_los_pasos_intermedios_y_los_fractiles_de_tabla_tienen_respaldo():
    fuentes = "S₁ = 0,06, S₂ = 0,084, α = 0,05, n = 7"
    texto = "S₁² = 0,0036 y S₂² = 0,007056; 1 − α/2 = 0,975; t(0,975; 6) = 2,4469; z = 2,5758; además 2,4471."
    assert explicar.numeros_sin_respaldo(texto, fuentes) == ["2,4471"]
