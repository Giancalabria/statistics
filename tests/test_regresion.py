"""Solver de regresión (TEMA VII y VIII), validado contra la Guía de Problemas."""

import pytest

from solver import regresion as rg

X1 = [3.0402, 2.9819, 3.0934, 3.8050, 5.4230]
Y1 = [8.014, 7.891, 8.207, 8.310, 8.450]


def test_recta_y_pronostico_VII_1():
    r = rg.ajustar_simple(X1, Y1)
    assert r.predecir(5.401) == pytest.approx(8.488544, abs=1e-5)
    assert r.r == pytest.approx(0.8372, abs=1e-4)
    ic = rg.ic_prediccion(r, 5.401, 0.10)
    assert (ic.A, ic.B) == (pytest.approx(8.028998, abs=1e-5), pytest.approx(8.94809, abs=1e-5))


def test_limite_inferior_individual_VII_2():
    r = rg.ajustar_simple([0.80, 0.75, 0.60, 0.92, 0.86], [36.40, 32.10, 32.30, 40.30, 37.10])
    assert r.r == pytest.approx(0.8816, abs=1e-4)
    assert rg.ic_prediccion(r, 0.80, 0.10, "inferior").A == pytest.approx(32.594, abs=1e-3)


def test_existencia_usa_t_1_menos_alfa():
    r = rg.ajustar_simple(X1, Y1)
    e = rg.ensayo_beta1(r, 0.05, 0.0, "existencia")
    assert e.t_critico == pytest.approx(2.3534, abs=1e-4)  # t(0,95; 3), criterio de la cátedra
    assert e.rechaza


def test_sumatorias_VII_5():
    r = rg.desde_sumatorias(10, 97, 1169, 21.16, 48.68, 180.9326)
    assert rg.ic_prediccion(r, 5, 0.10, "inferior").A == pytest.approx(1.99813, abs=1e-4)
    e = rg.ensayo_beta1(r, 0.05, -0.07, "izquierda")
    assert not e.rechaza


def test_ic_rho_fisher():
    r = rg.ajustar_simple([3, 3, 6, 6, 9, 9, 12, 12], [0, 0, 0, 0, 0, 0, 0, 1])  # solo forma
    ic = rg.ic_rho(r, 0.05)
    assert -1 < ic.A < r.r < ic.B < 1


def test_doble_log_y_origen():
    x = [110, 568, 245, 324, 76]
    y = [0.7, 2.41, 1.19, 1.53, 0.53]
    r = rg.ajustar_simple(x, y, modelo="loglog")
    assert r.b0 == pytest.approx(-3.8635, abs=1e-3)
    assert r.b1 == pytest.approx(0.743, abs=1e-3)
    o = rg.ajustar_simple([3, 6, 9], [100, 210, 290], origen=True)
    assert o.b0 == 0 and o.b1 == pytest.approx((300 + 1260 + 2610) / (9 + 36 + 81))


def test_multiple_VIII_2():
    x1 = [24.81, 26.27, 23.93, 25.24, 24.15, 25.07, 23.98, 25.16, 23.97, 25.98]
    # datos de la guía en datos/guia_ejercicios.json; acá solo se prueba la mecánica con una relación exacta
    x2 = [46, 42, 48, 40, 44, 45, 41, 47, 43, 49]
    y = [2 + 3 * a - 0.5 * b for a, b in zip(x1, x2)]
    reg = rg.ajustar_multiple([x1, x2], y, ["x1", "x2"])
    assert reg.b == pytest.approx([2, 3, -0.5], abs=1e-6)
    assert reg.R2 == pytest.approx(1.0)


def test_seleccion_devuelve_todos_los_subconjuntos():
    import random
    random.seed(1)
    xs = [[random.random() for _ in range(12)] for _ in range(3)]
    y = [1 + 2 * a + random.random() * 0.1 for a in xs[0]]
    cands = rg.seleccion_modelos(xs, y, ["x1", "x2", "x3"])
    assert len(cands) == 7
    assert rg.mejor_candidato(cands).variables[0] == "x1"
