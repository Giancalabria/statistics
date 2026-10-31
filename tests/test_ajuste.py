"""Bondad de ajuste χ² con frecuencias esperadas calculadas por el modelo (TEMA VI)."""

import pytest

from solver import ajuste as aj


def _lim(txt):
    return [tuple(float(v) for v in par.split("-")) for par in txt.split()]


def test_poisson_VI_16_no_rechaza():
    r = aj.ajuste_discreto("poisson", range(11), [26, 62, 120, 145, 131, 101, 61, 27, 9, 1, 1], 0.05)
    assert r.estimados == ["m"]
    assert not r.rechaza
    assert all(c.fe >= 5 for c in r.tabla_final)


def test_normal_VI_14_rechaza():
    r = aj.ajuste_continuo("normal", _lim("20-30 30-40 40-50 50-60 60-70 70-80 80-90"),
                           [6, 90, 232, 192, 66, 12, 2], 0.05)
    assert r.rechaza
    assert r.chi2_calc == pytest.approx(9.5963, rel=0.01)  # la guía agrega clases extremas: misma decisión


def test_normal_con_parametros_dados_VI_20b():
    r = aj.ajuste_continuo("normal", _lim("10-12 12-14 14-16 16-18 18-20 20-22 22-24 24-26 26-28"),
                           [2, 6, 13, 18, 30, 22, 16, 5, 1], 0.05, {"mu": 20, "sigma": 2.5})
    assert r.estimados == [] and r.df == 5
    assert r.chi2_critico == pytest.approx(11.0705, abs=1e-4)
    assert r.rechaza


def test_gumbel_min_rechaza_y_max_weibull_no_VI_15():
    lim = _lim("0-15 15-30 30-45 45-60 60-75 75-90 90-105")
    fo = [8, 40, 30, 25, 18, 15, 7]
    # números de la clase del 29/10: las clases que completan el dominio van aparte con Fo = 0
    r = aj.ajuste_continuo("gumbel_min", lim, fo, 0.01)
    assert r.rechaza and r.df == 4
    assert r.tabla[0].etiqueta == "-∞ a 0" and r.tabla[0].fe == pytest.approx(7.04, abs=0.01)
    assert r.chi2_calc == pytest.approx(68.55, abs=0.02)
    assert r.chi2_critico == pytest.approx(13.2767, abs=1e-4)
    r = aj.ajuste_continuo("gumbel_max", lim, fo, 0.01)
    assert not r.rechaza and r.df == 4
    assert r.chi2_calc == pytest.approx(10.8398, abs=0.03)  # el profesor redondeó las Fe
    r = aj.ajuste_continuo("weibull", lim, fo, 0.01)
    assert not r.rechaza and r.df == 4
    assert r.parametros["w"] == pytest.approx(1.9592, abs=1e-4) and r.parametros["beta"] == pytest.approx(51.52, abs=0.01)
    assert r.chi2_calc == pytest.approx(8.3318, abs=0.02)


def test_weibull_forma_por_momentos_tabla_catedra():
    # tabla de la cátedra: w = 0,5 → δ = s/m = 2,23607
    assert aj._weibull_forma(2.23607) == pytest.approx(0.5, abs=1e-3)


def test_pareto_con_minimo_dado_VI_18():
    r = aj.ajuste_continuo("pareto", _lim("400-500 500-600 600-700 700-800 800-1000 1000-1200 1200-1500 1500-2000 "
                                          "2000-3000 3000-5000"), [59, 34, 26, 20, 21, 15, 11, 10, 12, 6], 0.05,
                           {"alpha": 400})
    assert r.estimados == ["b"]
    assert not r.rechaza


def test_amalgamado():
    t = [aj.Clase(str(i), 1, 0.1, fe) for i, fe in enumerate([2, 10, 10, 3, 1])]
    final = aj.amalgamar(t)
    assert all(c.fe >= 5 for c in final)
    assert sum(c.fe for c in final) == 26
