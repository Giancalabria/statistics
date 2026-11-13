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
