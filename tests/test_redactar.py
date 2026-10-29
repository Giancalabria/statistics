"""Redacción con el estilo de la cátedra, sin modelo: el checklist y la segunda vuelta."""

import json

from asistente import cliente, redactar as red
from asistente.explicar import enunciado_texto, resolucion_texto
from interprete.analizador import analizar
from interprete.resolver import resolver

PROP = ("Calcular los límites de confianza del 90% para la fracción defectuosa, si de un proceso productivo se tomó "
        "una muestra de 10 unidades en la cual se encontró 1 unidad defectuosa.")
DISENO = ("La resistencia a la rotura de cierto tipo de alambre es una variable aleatoria con una media de 280 kg y un "
          "desvío estándar de 20 kg. Se cree que un proceso de fabricación recién desarrollado puede aumentar la "
          "resistencia media sin modificar el desvío estándar, pero sólo se lo implementará si se tiene una razonable "
          "seguridad de que efectivamente es así. Se ha establecido en 0,05 la probabilidad de implementar el nuevo "
          "método cuando en realidad la resistencia no se modifica, y en 0,15 la probabilidad de no implementarlo si "
          "se incrementa en 10 kg.")


def _resuelto(planteo, incisos=None):
    an = analizar(planteo, incisos)
    res = resolver(an)
    return an, res, enunciado_texto(an) + "\n" + resolucion_texto(an, res)


def _fallas(texto, an, res, fuentes):
    return red.problemas(red.controlar(texto, an, fuentes, res))


def test_el_solver_muestra_los_fractiles_f_como_la_guia():
    _, res, _ = _resuelto(PROP)
    pasos = " ".join(res[0].pasos)
    assert "F(0,95; 20; 2) = 19,4458" in pasos and "F(0,95; 4; 18) = 2,9277" in pasos


def test_una_redaccion_correcta_pasa_el_checklist():
    an, res, fuentes = _resuelto(PROP)
    texto = ("### única) Intervalo\nX: atributo de cada pieza (1 = defectuosa, 0 = buena). n = 10, r = 1.\n"
             "F(0,95; 20; 2) = 19,4458 ⇒ A = 0,0051. F(0,95; 4; 18) = 2,9277 ⇒ B = 0,3942.\n"
             "P(0,0051 ≤ p ≤ 0,3942) = 0,90.")
    assert _fallas(texto, an, res, fuentes) == []


def test_el_checklist_marca_redondeo_numeros_inventados_y_falta_de_expresion_formal():
    an, res, fuentes = _resuelto(PROP)
    texto = ("### única) Intervalo\nX: atributo de cada pieza. F(0,95; 20; 2) = 19,5 ⇒ A = 0,0052 y B = 0,3941; el "
             "intervalo va de 0,0052 a 0,3941.")
    fallas = " | ".join(_fallas(texto, an, res, fuentes))
    assert "expresión formal" in fallas
    assert "faltan 0,0051, 0,3942" in fallas
    assert "19,5" in fallas


def test_el_checklist_marca_acepto_h0_y_falta_de_cr_y_rd():
    an, res, fuentes = _resuelto(DISENO, ["Establecer la hipótesis nula, la condición de rechazo y la regla de "
                                          "decisión."])
    texto = "### a) Diseño\nX: resistencia a la rotura, en kg. H0: μ ≤ 280 vs H1: μ > 280. n = 29. Acepto H0."
    fallas = " | ".join(_fallas(texto, an, res, fuentes))
    assert "Acepto H0" in fallas and "condición de rechazo y regla de decisión" in fallas


def test_la_segunda_vuelta_recibe_los_problemas(monkeypatch):
    recibidos = []

    def chat(mensajes, **kw):
        recibidos.append(mensajes)
        return iter(["ok"])
    monkeypatch.setattr(cliente, "chat", chat)
    an, res, _ = _resuelto(PROP)
    "".join(red.corregir(an, res, "texto viejo", ["falta la expresión formal"]))
    ultimo = recibidos[0]
    assert ultimo[-2] == {"role": "assistant", "content": "texto viejo"}
    assert "falta la expresión formal" in ultimo[-1]["content"]
    assert "FORMATO DE LA RESOLUCIÓN" in ultimo[0]["content"] and "Ejemplo 3" in ultimo[0]["content"]


def test_el_formato_trae_solo_lo_del_tema():
    an, res, _ = _resuelto(PROP)                                  # Tema III: intervalo de una proporción
    sistema = red.mensajes(an, res)[0]["content"]
    assert "Ejemplo 3" in sistema and "Ejemplo 1" not in sistema and "χ²" not in sistema
    assert "Este archivo es lo que lee la IA" not in sistema      # el encabezado del archivo no va
    assert "<!--" not in sistema
    an, res, _ = _resuelto("Se arrojó un dado 60 veces: 1 salió 14 veces, 2 salió 6, 3 salió 6, 4 salió 13, 5 salió "
                           "16 y 6 salió 5. ¿Se puede asegurar, con un riesgo del 5%, que el dado está cargado?")
    m = red.mensajes(an, res)
    assert an.tema == "chi_ajuste"
    assert "### Contrastes χ²" in m[0]["content"] and "Checklist" not in m[0]["content"] and "pesimista / defensivo" not in m[0]["content"]
    assert "no corresponde en este tema" in m[1]["content"] and "una sola consigna" in m[1]["content"].lower()
    assert "**4 · " not in m[1]["content"]                       # sin la numeración interna del solver


def test_el_checklist_marca_incisos_inventados_y_criterio_en_chi():
    an, res, fuentes = _resuelto("Se arrojó un dado 60 veces: 1 salió 14 veces, 2 salió 6, 3 salió 6, 4 salió 13, 5 "
                                 "salió 16 y 6 salió 5. ¿Se puede asegurar, con un riesgo del 5%, que el dado está "
                                 "cargado?")
    texto = ("### a) Variable\nX: cara del dado.\n### b) Ensayo\nCriterio optimista. H0: equilibrado vs H1: cargado. "
             "CR y RD. Se rechaza H0.")
    fallas = " | ".join(_fallas(texto, an, res, fuentes))
    assert "Agrega incisos" in fallas and "criterio optimista" in fallas.lower()


def test_el_checklist_marca_probabilidades_en_porcentaje():
    an, res, fuentes = _resuelto(PROP)
    base = ("### única) Intervalo\nX: atributo de cada pieza (1 = defectuosa, 0 = buena). n = 10, r = 1.\n"
            "F(0,95; 20; 2) = 19,4458 ⇒ A = 0,0051. F(0,95; 4; 18) = 2,9277 ⇒ B = 0,3942.\n"
            "P(0,0051 ≤ p ≤ 0,3942) = 0,90. ")
    for mal in ("Hay un 97,88 % de probabilidad de rechazar H0.", "La potencia es del 97,88 %.", "β = 2,12 %."):
        assert any("en %" in f for f in _fallas(base + mal, an, res, fuentes)), mal
    for bien in ("Con un 90 % de confianza el porcentaje de defectuosas no supera el 39,42 %.",
                 "Con α = 0,10, β = 0,0212."):
        assert not any("en %" in f for f in _fallas(base + bien, an, res, fuentes)), bien


def test_va_un_solo_ejemplo_el_del_tipo_de_inciso():
    an, res, _ = _resuelto(PROP)                                  # intervalo de p: el ejemplo de intervalo
    sistema = red.mensajes(an, res)[0]["content"]
    assert sistema.count("### Ejemplo") == 1 and "Ejemplo 3" in sistema
    assert red.estilo_para("proporcion").count("### Ejemplo") > 1  # sin tipos, todos los del tema
    assert "Ejemplo III-16" in red.estilo_para("proporcion", ["diseno", "beta", "diseno", "curva"])
    assert "Ejemplo III-19" in red.estilo_para("proporcion", ["ensayo", "beta"])


def test_expresion_formal_con_parentesis_y_cotas_de_un_limite():
    for bien in ("P(67,55 ≤ μ(R) − μ(S) ≤ 456,45) = 0,9", "P(0,4732 ≤ σ(P)/σ(A) ≤ 1,1392) = 0,9",
                 "P(δ ≥ 0,3788 kg) = 0,95", "P(0,0051 ≤ p ≤ 0,3942) = 0,90"):
        assert red._FORMAL.search(bien), bien
    for mal in ("P(h = 1,0490 ⇒ μ ≥ 1,0490·μ) = 0,95", "P(rechazar H0) = 0,21", "P(F < 0,6341) = 0,2103"):
        assert not red._FORMAL.search(mal), mal
