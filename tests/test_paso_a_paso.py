"""Paso a paso: cada número de la resolución sale de una fórmula con los valores reemplazados (11/11/2026).

Lo escribe el solver, no la IA: los números son los mismos que usa para decidir. Valores del pizarrón en
estudio/informes/ (y datos/clase_resueltos.json).
"""

import json
from pathlib import Path

from tests.test_clases_profesor import resolver_guia

RAIZ = Path(__file__).resolve().parent.parent


def _pasos(res) -> str:
    return " ".join(res.pasos)


def test_varianza_cr_beta_y_n_con_tabla():
    _, (a, b, c, d) = resolver_guia("II-8")
    assert "S²c = σ₀²·χ²(0,95; ν)/ν = 0,09·19,6751/11 = 0,16098" in _pasos(b)
    assert "P(χ² ≤ 11·0,16098/0,11 = 16,0978) = 0,8625" in _pasos(c)
    it = _pasos(d)
    assert "R = σ₁²/σ₀² = 0,11/0,09 = 1,2222" in it
    assert "con n = 539" in it and "0,0501 > 0,05" in it and "0,0498 ≤ 0,05 ⇒ n = 540" in it


def test_dos_varianzas_iteracion_sobre_f():
    _, (a, b, c, d) = resolver_guia("IV-1")
    assert "ν = 43" in _pasos(b) and "2,7581 > 2,7352" in _pasos(b) and "ν = 44, n = ν + 1 = 45" in _pasos(b)
    _, (a4, b4, c4) = resolver_guia("IV-4")
    assert "j²c = φ₀²·F(0,1; 3; 15) = 0,7744·0,1923 = 0,1489" in _pasos(a4)
    assert "ν = 127, n = ν + 1 = 128" in _pasos(c4)


def test_dos_medias_sa_sigma_d_y_cr_reemplazados():
    _, (a, b, c, d) = resolver_guia("V-8")
    t = _pasos(a)
    assert "√[(20·1,2² + 60·1,25²)/80] = 1,237689" in t
    assert "σ(d) = Sa·√(1/n₁ + 1/n₂) = 1,237689·√(1/21 + 1/61) = 0,313144" in t
    assert "0,45 + 1,6641·0,313144 = 0,9711 kg" in t
    assert "A = d - e = 0,9 - 0,521111 = 0,378889" in _pasos(b)


def test_apareadas_diferencias_y_limites():
    _, (a, b) = resolver_guia("V-12")
    assert "6; 8; -2; 2; 7; 11; 1; 13" in _pasos(a)
    assert "2 + 1,8946·1,810189 = 5,4295" in _pasos(a)
    assert "1,8946·5,12/√8 = 3,4295" in _pasos(b) and "5,75 ∓ 3,429" in _pasos(b)


def test_media_diseno_y_p_normal_reemplazados():
    _, res = resolver_guia("I-10")
    assert "11,2 - 1,6449·1,3/√30 = 10,8096" in _pasos(res[2])
    _, res = resolver_guia("III-11")
    assert "[(1,6449·√(0,12·0,88) + 0·√(0,14·0,86))/0,02]² = 714,2635" in _pasos(res[2])


def test_chi_contingencia_ejemplo_de_esperado():
    _, (r,) = resolver_guia("VI-6")
    assert "E(Mañana; Primera calidad) = 500·1.450/1.700 = 426,4706" in _pasos(r)


def test_regresion_error_y_limites_del_pronostico():
    _, res = resolver_guia("VII-13")
    f, g = res[5], res[6]
    assert "2,1199·2,526991·√(1/18 + (10 - 36,611111)²/4.840,7778) = 2,4067" in _pasos(f)
    assert "23,8837 ∓ 5,8728 = 18,0109 ; 29,7565" in _pasos(g)


def test_banco_de_clase_coincide_con_la_guia():
    banco = json.loads((RAIZ / "datos" / "clase_resueltos.json").read_text(encoding="utf-8"))["ejercicios"]
    guia = {e["id"]: e for e in json.loads((RAIZ / "datos" / "guia_ejercicios.json").read_text(encoding="utf-8"))}
    for e in banco:
        n = len(guia[e["guia"]]["incisos"])
        assert len(e["esperado"]) == n and len(e["profesor"]) == n, e["guia"]


def test_parecidos_de_clase_por_tema():
    from asistente.clase import parecidos
    ids = [ej["id"] for _, ej in parecidos("la varianza no debe superar 4 mm2; riesgo 5%", 2, tema="varianza")]
    assert all(i.startswith("II-") for i in ids)
    assert "VI-13" not in [ej["id"] for _, ej in parecidos("patrón histórico", 3, excluir=["VI-13"], tema="chi_ajuste")]


def test_consenso_pasa_excluir_a_las_dos_ia(monkeypatch):
    from asistente import consenso as cons
    from interprete.analizador import analizar
    vistos = []

    def falsa(planteo, incisos, tablas, modelo, excluir=()):
        vistos.append(tuple(excluir))
        return analizar(planteo, incisos, tablas=tablas), []

    monkeypatch.setattr(cons, "pedir_ia", falsa)
    monkeypatch.setattr(cons, "pedir_ia_tema", falsa)
    ej = resolver_guia.__globals__["GUIA"]["V-12"]
    cons.consenso(ej["planteo"], [(i["letra"], i["texto"]) for i in ej["incisos"]], ej["tablas"], excluir=["V-12"])
    assert vistos == [("V-12",), ("V-12",)]


# ---------------------------------------------------------------------------
# De dónde sale cada número (13/11/2026): nada «de la galera», temas del 2° parcial
# ---------------------------------------------------------------------------

def test_plan_exacto_de_p_con_alfa_y_beta_reales_de_la_binomial():
    _, res = resolver_guia("III-11")
    t = _pasos(res[2])
    assert "α real = G_b(106 | n = 755; p₀ = 0,12) = 0,0499 ≤ 0,05" in t
    assert "β real = F_b(105 | n = 755; p₁ = 0,14) = 0,4967 ≤ 0,5" in t
    assert "Z(1-α) = Z(0,95) = 1,6449, Z(1-β) = Z(0,5) = 0" in t


def test_dos_varianzas_inversa_raiz_relacion_y_beta_real():
    _, res = resolver_guia("IV-1")
    t = _pasos(res[0])
    assert "[1/B ; 1/A]" in t and "B/A = " in t and "√0,898" in t
    assert "Δn = 45 - 25 = 20 y 45 - 13 = 32" in res[1].conclusion
    _, res = resolver_guia("IV-2")
    assert "P(F(482; 482) ≥ j²c/φ₁²) = P(F ≥ 0,5694/0,49 = 1,1621) = 0,0497" in _pasos(res[2])


def test_n_de_dos_medias_muestra_cada_iteracion():
    _, res = resolver_guia("V-1")
    t = _pasos(res[2])
    assert "con n = 30: ν = 2·30 - 2 = 58, t(0,95; 58) = 1,6716" in t and "Se repite ⇒ n = 45" in t
    assert "faltan 45 - 12 = 33" in res[2].conclusion


def test_bondad_de_ajuste_con_momentos_a_la_vista():
    _, res = resolver_guia("VI-15")
    t = _pasos(res[0])
    assert "x̄ = Σ mᵢ·Foᵢ / N = 6.532,5/143 = 45,6818" in t
    assert "β = S·√6/π = 24,3257·√6/π = 18,9667" in t


def test_regresion_sumas_de_cuadrados_y_r():
    _, res = resolver_guia("VII-13")
    t = _pasos(res[0])
    assert "Sxx = Σx² - n·x̄² = 28.967,5 - 18·36,611111² = 4.840,7778" in t
    assert "r² = (-0,896366)² = 0,803472" in t and "|b1|/Sb1 = 0,293751/0,03632 = 8,0879" in t


def test_numeros_con_punto_de_miles_no_se_rompen():
    """V-10: «d > 103,161 unidades,2303» (el _coma pasaba los puntos de miles a coma y la unidad caía en el medio)."""
    from interprete.resolver import _coma
    assert _coma("Si d > 103.161,2303, se rechaza. H0: δ ≤ 50.000. x = 37.5698") == \
        "Si d > 103.161,2303, se rechaza. H0: δ ≤ 50.000. x = 37,5698"
    _, res = resolver_guia("V-10")
    assert "Si d > 103.161,2303 unidades," in res[0].regla and "50,000" not in res[0].conclusion


def test_detector_de_numeros_sin_origen():
    from interprete.origen import sin_origen
    assert sin_origen("β = 0,4769.", "") == ["0,4769"]                          # resultado suelto
    assert sin_origen("β = P(Z ≥ 0,0579) = 0,4769.", "0,0579") == []            # con su cuenta
    assert sin_origen("t(0,95; 7) = 1,8946; d_c = δ₀ + t(0,95; 7)·σ(d) = 2 + 1,8946·1,81 = 5,4295.", "2 1,81") == []
    assert sin_origen("F(0,95; 4; 18) = 2,9277.", "") == []                     # los argumentos son ν
    assert sin_origen("= [0,898 ; 4,9126]. Inversa: [0,2036 ; 1,1135].", "") == ["0,2036", "1,1135"]
    assert sin_origen("A ; B = 5,75 ∓ 3,4295 = 2,3205 ; 9,1795", "5,75 3,4295") == []
    assert sin_origen("n = 45 (del inciso a).", "", previos=[45.0]) == []


def test_el_solver_casi_no_deja_numeros_sin_origen_en_el_parcial():
    """Auditoría sobre la guía, temas III a VII (herramientas/auditar_origen.py): al 13/11 quedan 31/192 incisos con
    algún número marcado, casi todos enteros de listas de datos o fracciones; antes eran 154."""
    from asistente.explicar import enunciado_texto
    from interprete.origen import resultados, sin_origen
    guia = resolver_guia.__globals__["GUIA"]
    con, total = 0, 0
    for eid in guia:
        if not eid.split("-")[0] in ("III", "IV", "V", "VI", "VII"):
            continue
        an, res = resolver_guia(eid)
        previos = []
        for r in res:
            if r.errores:
                continue
            total += 1
            texto = "\n".join(r.pasos) + "\n" + r.conclusion
            con += bool(sin_origen(texto, enunciado_texto(an), previos=previos))
            previos += resultados(texto)
    assert con <= 35, f"{con}/{total}"
