"""Convenciones de la cátedra verificadas dígito a dígito contra la guía (ver CONVENCIONES_CATEDRA.md)."""

import sys
from pathlib import Path

import pytest

from interprete import redondeo
from interprete.analizador import analizar
from interprete.resolver import resolver
from solver import distributions as dist
from solver import hypothesis_one as hyp
from solver import intervals as ic

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "herramientas"))
from evaluar_guia import coincide_exacto  # noqa: E402


# --- población finita: √((N-n)/N) -------------------------------------------------------------

def test_factor_de_finitud_es_N_no_N_menos_1():
    assert dist.fpc(1200, 36) == pytest.approx((1164 / 1200) ** 0.5)


def test_I_34_total_poblacional_coincide_con_la_guia():
    r = ic.ic_media_sigma_conocido(47, 8, 36, 0.10, N=1200)
    t = ic.ic_total_poblacional(r, 1200)
    assert (redondeo.abajo(t.a, 2), redondeo.arriba(t.b, 2)) == (53808.01, 58991.99)
    assert (redondeo.abajo(r.a, 2), redondeo.arriba(r.b, 2)) == (44.84, 49.16)


# --- β con el crítico redondeado hacia afuera a 4 decimales -------------------------------------

def test_critico_catedra_redondea_hacia_afuera():
    assert hyp.critico_catedra(37.56981, "izquierda") == 37.5698
    assert hyp.critico_catedra(4.58221, "derecha") == 4.5823
    assert hyp.critico_catedra((9.12345, 10.98761), "bilateral") == (9.1234, 10.9877)


@pytest.mark.parametrize("ej, beta_guia", [("I-9", 0.2775), ("I-11", 0.3831), ("I-27", 0.5259)])
def test_beta_de_la_guia_se_reproduce_con_el_critico_de_catedra(ej, beta_guia):
    import json
    raiz = Path(__file__).resolve().parent.parent
    guia = {e["id"]: e for e in json.loads((raiz / "datos" / "guia_ejercicios.json").read_text(encoding="utf-8"))}
    e = guia[ej]
    an = analizar(e["planteo"], [(i["letra"], i["texto"]) for i in e["incisos"]], tablas=e.get("tablas") or None)
    numeros = [x for r in resolver(an) for x in r.numeros]
    assert coincide_exacto(beta_guia, numeros)


# --- redondeo de presentación -------------------------------------------------------------------

def test_intervalo_hacia_afuera_con_ceros_fijos():
    assert redondeo.intervalo(270.4041, 289.5959, 2, por_error=True)[:2] == ("270,40", "289,60")
    assert redondeo.intervalo(3.0122, 3.5, 2)[:2] == ("3,01", "3,50")


def test_decimales_por_cifras_significativas():
    # II-1: σ² con base 4 se amplía a 5 decimales; I-36b: e = 0,1149 pide 3 decimales
    assert redondeo.intervalo(0.000412, 0.0015724, 4)[1] == "0,00158"
    assert redondeo.intervalo(0.98509, 1.21491, 2, por_error=True)[:2] == ("0,985", "1,215")


def test_critico_informado_alejandose_de_mu0():
    assert redondeo.critico(1.069616, "derecha") == "1,07"
    assert redondeo.critico(37.5698, "izquierda") == "37,56"
    assert redondeo.critico((11.4523, 11.5477), "bilateral") == "11,45 ; 11,55"


# --- ensayo planteado «a la luz de los datos» ---------------------------------------------------

def test_I_36_a_posteriori_es_unilateral_hacia_la_muestra():
    planteo = ("Un fabricante de azúcar envasa en bolsas de papel de 1 kg lo que es correcto cuando el proceso está bajo "
               "control. Sobre un lote de 1.400 bolsas terminadas, se tomó una muestra al azar de 9 unidades arrojando "
               "una media que resultó de 1,10 kg y un desvío de 0,15 kg.")
    an = analizar(planteo, [("a", "Plantear la hipótesis adecuada al problema y determinar si el proceso se encuentra "
                                  "fuera de control, a la luz de los datos obtenidos, para un riesgo del 10%.")])
    res = resolver(an)[0]
    assert "μ ≤ 1" in res.resumen and "RECHAZA" in res.resumen
    assert any("1,07" in p for p in res.pasos)


# --- proporciones -------------------------------------------------------------------------------

def test_ic_proporcion_r_cero_usa_alpha_medio():
    assert ic.ic_proporcion_exacto(0, 10, 0.10).b == pytest.approx(0.2589, abs=1e-4)


@pytest.mark.parametrize("p0, p1, alpha, beta, tail, n, rc", [
    (0.015, 0.04, 0.05, 0.10, "derecha", 325, 10),   # III-22a
    (0.02, 0.05, 0.15, 0.10, "derecha", 186, 7),     # III-22b
])
def test_plan_poisson_con_garcia(p0, p1, alpha, beta, tail, n, rc):
    r = hyp.plan_poisson_garcia(p0, p1, alpha, beta, tail)
    assert (r.n, r.rc) == (n, rc)


def test_plan_mas_proximo_a_las_premisas():
    assert hyp.plan_mas_proximo(0.02, 0.05, 0.15, 0.10)[:2] == (218, 7)    # III-22b
    assert hyp.plan_mas_proximo(0.015, 0.04, 0.05, 0.10)[:2] == (353, 10)  # III-22a (coincide con el n mínimo)


# --- evaluador estricto -------------------------------------------------------------------------

def test_coincide_exacto_acepta_redondeo_comun_o_hacia_afuera():
    assert coincide_exacto(44.84, [44.84001])
    assert coincide_exacto(4.59, [4.5822])          # hacia arriba
    assert not coincide_exacto(53808.01, [53806.93])
    assert coincide_exacto(25.89, [0.258866])       # como porcentaje
