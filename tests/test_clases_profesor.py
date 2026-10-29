"""Ejercicios resueltos por el profesor (Ing. Dopazo) en clase, 27/08 a 22/10/2026.

Fuente: estadistica/informes/informe_clases_1_6.md e informe_clases_7_12.md (sección 4, números verificados con
scipy) y estadistica/REGLAS_PROFESOR.md. Lo que dice el profesor manda sobre la guía: donde difieren (III-3b,
III-11c) estos tests siguen al profesor. Se resuelven por el camino del intérprete (enunciado de la guía →
analizar → resolver), como lo usaría el alumno.
"""

import json
from pathlib import Path

import pytest

from interprete.analizador import analizar
from interprete.resolver import Resultado, prop_ensayo, resolver
from solver import chi_square as chi
from solver import hypothesis_one as hyp
from solver.aproximaciones import criterio_aproximacion

GUIA = {e["id"]: e for e in json.loads((Path(__file__).resolve().parent.parent / "datos" / "guia_ejercicios.json")
                                       .read_text(encoding="utf-8"))}


def resolver_guia(eid):
    ej = GUIA[eid]
    if ej["incisos"] and ej["incisos"][0]["letra"] == "única":
        an = analizar(ej["enunciado"], None, tablas=ej.get("tablas") or None)
    else:
        an = analizar(ej["planteo"], [(i["letra"], i["texto"]) for i in ej["incisos"]], tablas=ej.get("tablas") or None)
    return an, resolver(an)


def tiene(res, valor, tol=1e-4):
    return any(abs(float(v) - valor) <= tol for v in res.numeros if v is not None)


def texto(res):
    return "\n".join(res.pasos) + "\n" + res.conclusion


# ------------------------------------------------------------------------------------------- TEMA I y II

def test_I_10_aditivo():
    _, (a, b, c, *_) = resolver_guia("I-10")
    assert tiene(a, 10.5238) and "NO rechaza" in a.resumen          # 10,6 no es menor que 10,52
    assert "μ ≥ 11.2" in a.resumen or "μ ≥ 11,2" in a.resumen       # pesimista
    assert tiene(b, 0.5231) and tiene(b, 0.4769)                    # 1-β y β
    assert c.numeros[0] == 30 and tiene(c, 20)                      # n = 30, 20 corridas más
    # justificación de Z por estructura, no «porque conozco σ»
    assert "se divide por el parámetro σ" in texto(a)


def test_II_8_laminas():
    _, (a, b, c, d) = resolver_guia("II-8")
    assert tiene(a, 0.0835) and tiene(a, 0.3590)                    # P(0,0834 ≤ σ² ≤ 0,3591) = 0,90
    assert tiene(b, 0.16098) and "NO rechaza" in b.resumen          # S²c = 0,16098
    assert tiene(c, 0.1375, 3e-4)                                   # 1-β (profesor 0,1373 / guía 0,1375)
    assert d.numeros[0] == 540 and tiene(d, 528)                    # n = 540, 528 más


def test_II_12_suelas():
    _, (a, b, c) = resolver_guia("II-12")
    assert tiene(a, 6.8554) and tiene(a, 16.919)                    # Sc = 6,86 g
    assert tiene(b, 0.3222)
    assert c.numeros[0] == 27 and tiene(c, 17)


# ------------------------------------------------------------------------------------------- TEMA III

def test_III_3_ic_exacto_y_r_cero_con_alpha_entero():
    _, (a, b) = resolver_guia("III-3")
    assert tiene(a, 0.0051) and tiene(a, 0.3942)
    # b) r = 0: un solo límite, α ENTERO → 0,2057 (la guía dice 0,2589 y el profesor dijo que está mal)
    assert tiene(b, 0.2057) and not tiene(b, 0.2589)
    assert "α ENTERO" in texto(b) and any("0.2589" in w for w in b.avisos)
    # nunca la aproximación normal como estimación («aberración»)
    assert "Referencia, aproximación normal" not in texto(a)


def test_III_3_tamano_extra_del_profesor():
    # a') reducir 80 % el error 0,1945 → n = 162; se verifica con el n RESULTANTE: 16,2 y 145,8 > 10 → normal
    c = criterio_aproximacion(162, 0.10)
    assert c.elegida == "normal" and c.normal_ok and c.n0 is None


def test_III_11_control_de_proceso():
    _, (a, b, c) = resolver_guia("III-11")
    assert a.numeros == [11]                                         # G(10) = 0,0708 > 0,05; G(11) = 0,0325
    assert "G_b(10" in texto(a) and "α real" in texto(a)
    assert tiene(b, 0.9176)                                          # β = F_b(10 | 50; 0,14)
    assert c.numeros[:2] == [755, 106]                               # exacto
    assert 715 in c.numeros                                          # normal, justificada con n = 715
    # Poisson: 855 es INCORRECTO (el criterio con el n resultante habilita la normal)
    assert 855 not in c.numeros and "NO habilita Poisson" in texto(c)


def test_III_16_campania():
    _, res = resolver_guia("III-16")
    a, b = res[0], res[1]
    assert a.numeros[:2] == [1675, 233]
    assert 1637 in a.numeros and 229 in a.numeros                    # normal: n = 1637, rc = 229 (α real ≤ α)
    assert "196,44" in texto(a)                                      # 1637·0,12 > 10 → normal
    assert tiene(b, 0.5527) and tiene(b, 0.5159)                     # exacto y con el plan normal


def test_III_19_ruleta():
    _, (a, b) = resolver_guia("III-19")
    assert a.numeros[0] == 37 and "RECHAZA" in a.resumen and "NO" not in a.resumen
    assert "1/37" in a.resumen                                       # periódico como fracción
    decision = next(p for p in a.pasos if "Cálculos y decisión" in p)
    assert "r_c = 37" in decision and "α*" not in decision          # se decide con r ≥ rc, no con α*
    assert tiene(b, 0.9788)


def test_ejemplo_del_software_24_09():
    r = hyp.disenar_plan_proporcion(0.05, 0.06, 0.01, 0.05)
    assert (r.n, r.rc) == (8142, 454)
    assert hyp.plan_proporcion_normal(0.05, 0.06, 0.01, 0.05).n == 8058


def test_criterio_de_aproximacion_del_profesor():
    assert criterio_aproximacion(715, 0.12).elegida == "normal"
    assert criterio_aproximacion(855, 0.12).elegida == "normal"      # por eso el 855 por Poisson no vale
    assert criterio_aproximacion(50, 0.12).elegida == "poisson"      # con el n inicial sí (el error de la guía)
    m = criterio_aproximacion(325, 0.015)                            # III-22a: ninguna → Mermoz
    assert m.elegida == "poisson" and m.n0 == pytest.approx(0.23 * 0.985 ** 2 / 0.015 ** 3)
    assert criterio_aproximacion(5000, 0.004).poisson_ok


def test_no_hay_bilateral_en_p():
    res = Resultado()
    prop_ensayo({"n": 100, "p0": 0.1, "r": 15, "tail": "bilateral"}, 0.05, res, {})
    assert any("bilateral" in a for a in res.avisos)
    assert "p > 0.1" in res.resumen or "p ≤ 0.1" in res.resumen


# ------------------------------------------------------------------------------------------- TEMA IV

def test_IV_1_tornos():
    _, (a, b, c, d) = resolver_guia("IV-1")
    assert tiene(a, 0.2036) and tiene(a, 1.1135)                     # A/B, el profesor 0,2035 y 1,1137
    assert b.numeros[0] == 45                                        # ν = 44 → n = 45 por torno
    assert tiene(c, 0.4512) and tiene(c, 1.0552)
    assert d.numeros[0] == 444                                       # R = R'² → ν = 443


def test_IV_4_hiladoras():
    _, (a, b, c) = resolver_guia("IV-4")
    assert tiene(a, 0.3859) and tiene(a, 0.3729) and "RECHAZA" in a.resumen
    assert "J = 0,3729 vs Jc = 0,3859" in a.resumen                  # estimador J contra Jc (desvíos)
    assert tiene(b, 0.1779) and tiene(b, 0.8221)
    assert c.numeros[0] == 128                                       # ν = 127


# ------------------------------------------------------------------------------------------- TEMA V

def test_V_8_latex():
    _, (a, b, c, d) = resolver_guia("V-8")
    t = texto(a)
    # ensayo auxiliar F: unilateral, orientado por los datos, α propio 0,10
    assert "ensayo auxiliar" in t and "α = 0,1" in t and "1,2949" in t and "1,0417" in t
    assert tiene(a, 1.2377) and tiene(a, 0.9711) and "NO rechaza" in a.resumen
    assert tiene(b, 0.37889)                                          # mínimo: un límite, t(0,95)
    assert tiene(c, 0.5349) and tiene(c, 0.14) and "NO rechaza" in c.resumen
    assert tiene(d, 1.0490)
    td = texto(d)
    assert "1,0490" in td and "1,1906" in td and "NO sirve" in td    # se verifican las dos raíces


def test_V_12_trigo_apareadas():
    _, (a, b) = resolver_guia("V-12")
    assert tiene(a, 5.75) and tiene(a, 5.4295) and "RECHAZA" in a.resumen and "NO" not in a.resumen
    assert tiene(b, 2.3205) and tiene(b, 9.1795)


def test_sin_beta_con_t_en_comparaciones():
    an = analizar("Línea vieja: 30 piezas con media 12 y desvío 2. Línea nueva: 30 piezas con media 13 y desvío 2.",
                  ["¿Se puede asegurar con 5% de riesgo que la línea nueva produce piezas más largas?",
                   "¿Qué probabilidad hay de no detectar una diferencia real de 1,5?"])
    res = resolver(an)
    assert res[1].resumen == "fuera de la cátedra"


# ------------------------------------------------------------------------------------------- TEMA VI

def test_VI_6_turnos_consistencia():
    _, (r,) = resolver_guia("VI-6")
    assert tiene(r, 38.9843) and tiene(r, 13.2767) and "RECHAZA" in r.resumen
    assert "consistencia" in texto(r)


def test_VI_7_color_independencia():
    _, (r,) = resolver_guia("VI-7")
    assert tiene(r, 5.5739) and tiene(r, 7.8147) and "NO rechaza" in r.resumen
    assert "independiente" in r.conclusion and "No hay evidencia suficiente" in r.conclusion


def test_VI_10_dado():
    _, (r,) = resolver_guia("VI-10")
    assert tiene(r, 11.8) and tiene(r, 11.0705) and "RECHAZA" in r.resumen


def test_VI_13_televisores():
    _, (r,) = resolver_guia("VI-13")
    assert tiene(r, 5.625) and tiene(r, 5.9915) and "NO rechaza" in r.resumen


def test_VI_16_poisson_dominio_completado_con_acumulada():
    _, (r,) = resolver_guia("VI-16")
    assert tiene(r, 9.4346) and tiene(r, 15.5073) and tiene(r, 8.0)  # 10 clases efectivas → ν = 8
    assert any("≥ 11" in a and "acumulada" in a for a in r.avisos)


def test_ajuste_demasiado_perfecto():
    # 11/9/11/9/11/9 en 60 tiradas: χ² = 0,6 < χ²(0,05; 5) = 1,1455 → sospechar de los datos
    r = chi.bondad_de_ajuste([11, 9, 11, 9, 11, 9], [10] * 6, 0, 0.05)
    assert r.chi2_calc == pytest.approx(0.6)
    assert any("demasiado perfecto" in w for w in r.warnings)


# ------------------------------------------------------------------------------------------- transversal

def test_probabilidades_nunca_en_porcentaje_en_la_conclusion():
    _, (a, *_) = resolver_guia("I-10")
    assert "Con α = 0,05" in a.conclusion and "5%" not in a.conclusion
    assert "No hay evidencia suficiente para asegurar" in a.conclusion and "acepta" not in a.conclusion
