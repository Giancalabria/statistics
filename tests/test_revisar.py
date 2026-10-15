"""Revisión del planteo con IA, sin modelo: cliente.chat se reemplaza por respuestas fijas según quién pregunta
(la lectura a ciegas o el árbitro)."""

import json
import re

import pytest

from asistente import cliente
from asistente import revisar as rev
from asistente.numeros import sin_usar
from interprete.analizador import analizar
from interprete.resolver import resolver

# variante que las reglas todavía leen mal ('envasar 250 cc' no es un umbral; '1 vez en 50' no es una frecuencia
# reconocida): toman el '1' como μ₀ y no encuentran α. La redacción del caso trampa T-12 ('calibrada para 250 cc',
# '1 de cada 50 veces') ya la resuelven las reglas (tests/test_trampas_redaccion.py).
CONTROL = ("Una llenadora se usa para envasar 250 cc y su desvío, conocido, es de 3,5 cc. Periódicamente se toma una "
           "muestra de 30 envases para decidir si se detiene la máquina para recalibrarla. Se acepta detenerla sin "
           "necesidad a lo sumo 1 vez en 50. La última muestra dio un promedio de 251,4 cc.")
MAQUINAS = ("Se quiere comparar una máquina nueva con una vieja. Se registró la producción por hora de la máquina nueva "
            "durante 15 horas: promedio 48,5 unidades, desvío 3,1. La vieja se observó durante 12 horas: promedio "
            "44,9 unidades, desvío 2,8.")
PREGUNTA_MAQ = ["Con un riesgo del 5%, ¿puede afirmarse que la máquina vieja produce, en promedio, al menos 2 unidades "
                "por hora menos que la nueva?"]


@pytest.fixture
def modelo(monkeypatch):
    """modelo(ciega, arbitro): respuestas fijas para cada rol; devuelve las preguntas que recibió el árbitro."""
    preguntas = []

    def instalar(ciega, arbitro=None):
        def chat(mensajes, **kw):
            sistema = mensajes[0]["content"]
            if sistema == rev.ARBITRO:
                preguntas.append(mensajes[-1]["content"])
                r = arbitro(mensajes[-1]["content"]) if callable(arbitro) else arbitro
                return json.dumps(r or {"respuestas": []})
            if sistema == rev.AUDITOR:
                return json.dumps({"incisos": []})
            return json.dumps(ciega)
        monkeypatch.setattr(cliente, "chat", chat)
        return preguntas
    return instalar


def _id_de(preguntas: str, texto: str) -> str:
    return next(l.split(":")[0] for l in preguntas.splitlines() if texto in l)


def test_numeros_sin_usar_marcan_lo_que_las_reglas_no_leyeron():
    an = analizar(CONTROL, ["¿Debe detenerse la máquina?"])
    assert an.datos.get("mu0") == 1                      # las reglas toman el '1 vez en 50' como μ₀
    assert {n.crudo for n in sin_usar(an, ["¿Debe detenerse la máquina?"])} == {"250", "50"}


def _opcion(preguntas: str, texto: str, valor: str) -> tuple:
    """(id, letra) de la pregunta que contiene `texto`, eligiendo la opción que dice `valor`."""
    linea = next(l for l in preguntas.splitlines() if texto in l)
    return linea.split(":")[0], ("A" if re.search(r"A\) " + re.escape(valor) + r"\b", linea) else "B")


def test_corrige_un_dato_con_cita_del_enunciado(modelo):
    def arbitro(p):
        id_mu, op = _opcion(p, "μ₀", "250")
        return {"respuestas": [
            {"id": id_mu, "opcion": op, "cita": "Una llenadora se usa para envasar 250 cc"},
            {"id": _id_de(p, "«50»"), "opcion": "B", "clave": "alpha", "valor": 0.02,
             "cita": "a lo sumo 1 vez en 50"}]}
    modelo({"tema": "media", "datos": {"n": 30, "desvio": 3.5, "sigma_conocido": True, "xbar": 251.4, "mu0": 250},
            "incisos": [{"letra": "a", "tipo": "no_soportado", "params": {}}]}, arbitro)
    rv = rev.revisar(CONTROL, ["¿Debe detenerse la máquina?"])
    # las reglas ya resolvían: la IA no pisa nada, sugiere (con cita) y el usuario decide
    assert rv.analisis.datos["mu0"] == 1 and not rv.corregidos
    assert len(rv.sugeridos) == 2 and all(i.cita for i in rv.sugeridos)
    an = rev.aplicar_sugerencias(rv, rv.sugeridos)
    assert an.datos["mu0"] == 250 and an.datos["alpha"] == pytest.approx(0.02)
    assert rv.reglas.datos["mu0"] == 1                   # el análisis de las reglas no se toca


def test_completa_lo_que_falta_para_resolver(modelo):
    planteo = "Se midieron piezas elegidas al azar y se obtuvo un promedio de 10,2 mm con un desvío de 0,3 mm."
    modelo({"tema": "media", "datos": {"n": 25, "xbar": 10.2, "desvio": 0.3, "sigma_conocido": False},
            "incisos": [{"letra": "a", "tipo": "ic", "params": {"alpha": 0.05}}]},
           lambda p: {"respuestas": [{"id": _id_de(p, "«25»"), "opcion": "B", "clave": "n", "valor": 25,
                                      "cita": "en total fueron 25 piezas"}]})
    rv = rev.revisar(planteo + " En total fueron 25 piezas.", ["Estimar la media con 95% de confianza."])
    assert rv.analisis.datos.get("n") == 25 and len(rv.corregidos) == 1     # sin n no se resolvía: se aplica


def test_una_cita_inventada_no_se_aplica(modelo):
    def arbitro(p):
        id_mu, op = _opcion(p, "μ₀", "250")
        return {"respuestas": [{"id": id_mu, "opcion": op,
                                "cita": "la media del proceso es de 250 cc según el fabricante"}]}
    modelo({"tema": "media", "datos": {"mu0": 250}, "incisos": [{"letra": "a", "tipo": "no_soportado",
                                                                 "params": {}}]}, arbitro)
    rv = rev.revisar(CONTROL, ["¿Debe detenerse la máquina?"])
    assert rv.analisis.datos["mu0"] == 1 and not rv.corregidos


def test_un_numero_sin_usar_no_pisa_un_dato_que_ya_esta(modelo):
    planteo = ("El tiempo de armado de un mueble tiene, según los registros históricos de la fábrica, un desvío de "
               "2,5 minutos. Se cronometraron 40 armados y se obtuvo un tiempo medio de 61,3 minutos; el desvío de "
               "esa muestra fue de 3 minutos.")

    def arbitro(p):
        return {"respuestas": [{"id": _id_de(p, "«3»"), "opcion": "B", "clave": "desvio", "valor": 3,
                                "cita": "el desvío de esa muestra fue de 3 minutos"}]}
    modelo({"tema": "media", "datos": {}, "incisos": [{"letra": "a", "tipo": "ic", "params": {}}]}, arbitro)
    rv = rev.revisar(planteo, ["Estimar el tiempo medio con 95% de confianza."])
    assert rv.analisis.datos["desvio"] == 2.5
    assert any("dos valores" in i.detalle for i in rv.a_revisar)


def test_una_cuenta_de_la_ia_que_no_sale_del_enunciado_no_se_aplica(modelo):
    # ('8.160 g en total' ya lo leen las reglas como total: acá el total está dicho de una forma que no reconocen)
    planteo = "Se midieron 16 bolsas; la balanza, con todas ellas encima, marcó 8.160 g. Se sabe que el desvío es de 20 g."

    def arbitro(p):
        return {"respuestas": [{"id": _id_de(p, "«8.160»"), "opcion": "B", "clave": "xbar", "valor": 512,
                                "cita": "pesaron 8.160 g en total"}]}
    modelo({"tema": "media", "datos": {}, "incisos": [{"letra": "a", "tipo": "ic", "params": {}}]}, arbitro)
    rv = rev.revisar(planteo, ["Estimar el peso medio con 95% de confianza."])
    assert "xbar" not in rv.analisis.datos
    assert any("no sale del enunciado" in i.detalle for i in rv.a_revisar)


def test_un_total_dividido_por_n_si_se_aplica(modelo):
    planteo = "Se midieron 16 bolsas y pesaron 8.160 g en total. Se sabe que el desvío es de 20 g."

    def arbitro(p):
        return {"respuestas": [{"id": _id_de(p, "«8.160»"), "opcion": "B", "clave": "xbar", "valor": 510,
                                "cita": "pesaron 8.160 g en total"}]}
    modelo({"tema": "media", "datos": {}, "incisos": [{"letra": "a", "tipo": "ic", "params": {}}]}, arbitro)
    rv = rev.revisar(planteo, ["Estimar el peso medio con 95% de confianza."])
    assert rv.analisis.datos.get("xbar") == 510


def test_la_hipotesis_se_arbitra_entera_y_en_palabras(modelo):
    ciega = {"tema": "dos_medias", "datos": {"n1": 12, "n2": 15, "xbar1": 44.9, "xbar2": 48.5, "s1": 2.8, "s2": 3.1,
                                             "nombre1": "vieja", "nombre2": "nueva", "sujeto": 2},
             "incisos": [{"letra": "a", "tipo": "ensayo", "params": {"alpha": 0.05, "tail": "derecha",
                                                                      "delta0": 2}}]}

    def arbitro(p):
        linea = next(l for l in p.splitlines() if "DEMOSTRAR" in l)
        op = "A" if "A) H1: la media de «nueva» supera a la de «vieja» en MÁS de 2" in linea else "B"
        return {"respuestas": [{"id": linea.split(":")[0], "opcion": op,
                                "cita": "la máquina de siempre produce, en promedio, al menos 2 unidades por hora menos"}]}
    preguntas = modelo(ciega, arbitro)
    # variante que las reglas todavía leen al revés ('la máquina de siempre' no se reconoce como la vieja); la
    # redacción del caso trampa T-11 ya la resuelven las reglas (tests/test_trampas_redaccion.py)
    rv = rev.revisar(MAQUINAS, [PREGUNTA_MAQ[0].replace("la máquina vieja", "la máquina de siempre")])
    # las reglas plantean la diferencia al revés (H1: μ(nueva) - μ(vieja) < -2): se arbitra en palabras, sin δ
    assert "«vieja» supera a la de «nueva» en MÁS de 2" in preguntas[0] and "δ" not in next(l for l in preguntas[0].splitlines() if "DEMOSTRAR" in l)
    assert "«2»" not in preguntas[0] or "Diferencia" not in str(rv.corregidos)
    an = rev.aplicar_sugerencias(rv, rv.sugeridos)
    assert rev.hipotesis(an)["a"].endswith("> 2")
    res = resolver(an)[0]
    assert "NO rechaza" in res.resumen                                     # t = 1,39 < 1,708


def test_lo_que_la_ia_inventa_no_genera_dudas(modelo):
    planteo = "Se midieron 25 piezas elegidas al azar y se obtuvo un promedio de 10,2 mm con un desvío de 0,3 mm."
    modelo({"tema": "media", "datos": {"n": 25, "xbar": 10.25, "desvio": 0.3, "sigma_conocido": False},
            "incisos": [{"letra": "a", "tipo": "ic", "params": {"alpha": 0.05}}]})
    rv = rev.revisar(planteo, ["Estimar la media con 95% de confianza."])
    assert not rv.corregidos and not rv.a_revisar                          # 10,25 no está en el enunciado


def test_sin_ollama_devuelve_las_reglas_con_el_error(monkeypatch):
    def caido(*a, **kw):
        raise cliente.ErrorIA("no conecta")
    monkeypatch.setattr(cliente, "chat", caido)
    rv = rev.revisar(CONTROL, ["¿Debe detenerse la máquina?"])
    assert rv.error and rv.analisis is rv.reglas


@pytest.mark.parametrize("hip,palabras", [
    ("H0: δ = μ(a) - μ(b) ≥ 0  vs  H1: δ = μ(a) - μ(b) < 0", "la media de «a» es MENOR que la de «b»"),
    ("H0: x  vs  H1: δ = μ(a) - μ(b) < -2", "la media de «b» supera a la de «a» en MÁS de 2"),
    ("H0: x  vs  H1: μ(B) > 1,1·μ(A)", "la media de «B» supera a la de «A» en MÁS de un 10%"),
    ("H0: x  vs  H1: φ = σ₁/σ₂ < 0.85", "la relación de desvíos σ₁/σ₂ es MENOR que 0,85"),
])
def test_hipotesis_en_palabras(hip, palabras):
    assert rev.en_palabras(hip) == "H1: " + palabras


REGRESION = ("Una empresa registró durante 8 meses su inversión en publicidad (x, en miles de pesos) y sus ventas (y, en "
             "miles de pesos): x: 2 - 4 - 5 - 7 - 8 - 10 - 12 - 15; y: 21 - 30 - 33 - 41 - 42 - 50 - 57 - 70.")


def test_si_no_se_resolvia_las_sugerencias_que_van_juntas_se_aplican_juntas(modelo):
    x, y = [2, 4, 5, 7, 8, 10, 12, 15], [21, 30, 33, 41, 42, 50, 57, 70]

    def arbitro(p):                      # elige siempre la lectura de la IA (la opción que no dice "no figura")
        resp = []
        for l in p.splitlines():
            m = re.match(r"(P\d+):", l)
            if m:
                resp.append({"id": m.group(1), "opcion": "B" if "A) no figura" in l else "A",
                             "cita": "x: 2 - 4 - 5 - 7 - 8 - 10 - 12 - 15; y: 21 - 30 - 33 - 41 - 42 - 50 - 57 - 70"})
        return {"respuestas": resp}
    modelo({"tema": "regresion", "datos": {"x": x, "y": y},
            "incisos": [{"letra": "a", "tipo": "recta", "params": {}}]}, arbitro)
    incisos = ["Hallar la recta de regresión de las ventas en función de la publicidad."]
    assert rev.fallas(analizar(REGRESION, incisos), resolver(analizar(REGRESION, incisos)))   # las reglas no pueden
    rv = rev.revisar(REGRESION, incisos)
    assert rv.analisis.datos.get("x") == x and rv.analisis.datos.get("y") == y
    assert not rv.sugeridos and len(rv.corregidos) >= 2
    assert any(abs(v - 3.63) < 0.01 for v in resolver(rv.analisis)[0].numeros)              # b1 = 3,63
