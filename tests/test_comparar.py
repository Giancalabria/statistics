"""Comparación reglas vs IA (sin modelo: la IA se reemplaza por respuestas fijas)."""

import json

from asistente import cliente, comparar as comp
from interprete.analizador import analizar
from interprete.resolver import resolver

PAQUETES = ("Se sabe que el peso de los paquetes tiene distribución Normal con un desvío estándar de 6 kg. Se eligieron "
            "al azar 25 paquetes y se los pesó juntos: la balanza registró un peso conjunto de 1.237,5 kg.")
INCISOS = ["Estimar el peso medio de los paquetes con un 95% de confianza."]


def _ia(monkeypatch, datos, razonamiento="TEMA: media\nDATOS: x̄ = 1237,5 / 25 = 49,5 kg"):
    llamadas = []

    def chat(mensajes, **kw):
        llamadas.append(mensajes)
        if kw.get("formato"):
            return json.dumps({"tema": "media", "datos": datos,
                               "incisos": [{"letra": "a", "tipo": "ic", "params": {"alpha": 0.05}}]})
        return razonamiento
    monkeypatch.setattr(cliente, "chat", chat)
    return llamadas


def test_si_la_ia_lee_otra_cosa_no_coinciden_y_se_ven_los_dos(monkeypatch):
    _ia(monkeypatch, {"n": 25, "desvio": 6, "sigma_conocido": True, "xbar": 49.5})
    c = comp.comparar(PAQUETES, INCISOS)
    assert not c.error and c.ia is not None
    reglas_ok = not c.res_reglas[0].errores
    ia = c.res_ia[0]
    assert not ia.errores and "47,1" in ia.resumen and "51,8" in ia.resumen       # 49,5 ± 2,35
    assert c.incisos[0].coincide == (reglas_ok and comp.mismo_resultado(c.res_reglas[0], ia))
    assert "49,5" in c.ia.razonamiento


def test_si_llegan_a_lo_mismo_coinciden(monkeypatch):
    an = analizar(PAQUETES, INCISOS)
    an.datos.update({"xbar": 49.5, "n": 25})
    _ia(monkeypatch, {"n": 25, "desvio": 6, "sigma_conocido": True, "xbar": 49.5})
    c = comp.comparar(PAQUETES, INCISOS, analisis=an)
    assert c.coinciden


def test_la_correccion_del_usuario_le_llega_a_la_ia(monkeypatch):
    llamadas = _ia(monkeypatch, {"n": 25, "desvio": 6, "sigma_conocido": True, "xbar": 1237.5},
                   razonamiento="TEMA: media\nDATOS: x̄ = 1237,5")
    c = comp.comparar(PAQUETES, INCISOS)
    _ia_llamadas = _ia(monkeypatch, {"n": 25, "desvio": 6, "sigma_conocido": True, "xbar": 49.5})
    c2 = comp.corregir(c, "el 1.237,5 es el peso total", PAQUETES, INCISOS)
    paso1 = _ia_llamadas[0]
    assert any("el 1.237,5 es el peso total" in m["content"] for m in paso1)
    assert any(m["role"] == "assistant" and "1237,5" in m["content"] for m in paso1)   # recuerda lo que dijo
    assert "51,8" in c2.res_ia[0].resumen
    assert llamadas                                                                      # la primera vuelta sí se hizo


def test_mismo_resultado_tolera_redondeo_y_compara_decisiones():
    an = analizar(PAQUETES, INCISOS)
    an.datos.update({"xbar": 49.5, "n": 25})
    r = resolver(an)[0]
    assert comp.mismo_resultado(r, r)
    otro = analizar(PAQUETES, INCISOS)
    otro.datos.update({"xbar": 49.0, "n": 25})
    assert not comp.mismo_resultado(r, resolver(otro)[0])


def test_sin_ollama_quedan_las_reglas(monkeypatch):
    def caido(*a, **kw):
        raise cliente.ErrorIA("no conecta")
    monkeypatch.setattr(cliente, "chat", caido)
    c = comp.comparar(PAQUETES, INCISOS)
    assert c.error and c.reglas is not None and not c.coinciden


def test_estado_distingue_desacuerdo_de_no_poder(monkeypatch):
    _ia(monkeypatch, {"n": 25, "desvio": 6, "sigma_conocido": True, "xbar": 49.5})
    c = comp.comparar(PAQUETES, INCISOS)
    assert c.incisos[0].estado in ("solo_ia", "distinto")         # la IA lo resuelve; las reglas según lo que lean
    _ia(monkeypatch, {"desvio": 6})                                 # a la IA le faltan datos
    an = analizar(PAQUETES, INCISOS)
    an.datos.update({"xbar": 49.5, "n": 25})
    assert comp.comparar(PAQUETES, INCISOS, analisis=an).incisos[0].estado == "solo_reglas"
