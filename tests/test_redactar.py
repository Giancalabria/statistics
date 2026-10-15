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
    assert "ESTILO DE LA CÁTEDRA" in ultimo[0]["content"] and "Ejemplo 1" in ultimo[0]["content"]
