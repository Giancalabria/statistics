"""La presentación de la app contra los ejercicios que el profesor resolvió en clase (paso a paso del pizarrón).

Los números ya se controlan en test_clases_profesor.py; acá se controla CÓMO se presenta: la variable, las 4
probabilidades en términos del problema, la regla de decisión en lenguaje de planta y la conclusión con unidades.
Cada test cita lo que escribió el profesor (informes de clase y ESTILO_CATEDRA.md).
"""

import json
from pathlib import Path

from interprete.analizador import analizar
from interprete.resolver import resolver

RAIZ = Path(__file__).parent.parent
GUIA = {e["id"]: e for e in json.loads((RAIZ / "datos" / "guia_ejercicios.json").read_text(encoding="utf8"))}


def _resolver(id_, **datos):
    ej = GUIA[id_]
    an = analizar(ej["planteo"], [(i["letra"], i["texto"]) for i in ej["incisos"]], tablas=ej.get("tablas") or None)
    an.datos.update(datos)
    return an, resolver(an)


def _todo(res) -> str:
    return " ".join(res.pasos) + " " + res.conclusion


# ------------------------------------------------------------------ Tema I

def test_I_10_aditivo():
    """Clase: H0: μ ≥ 11,2 (pesimista: lanzar el aditivo es la decisión costosa); x̄c = 10,52; x̄ = 10,6 no rechaza;
    1 - β = 0,5231 en μ = 10,5; n = 30. α = P(lanzar el producto | no reduce el consumo)."""
    an, (a, b, c, d) = _resolver("I-10")
    assert an.datos["unidad"] == "litros" and an.datos["accion"] == "lanzar el producto"
    assert a.pasos[0].startswith("**Variable** (paso 1)")
    assert "α = P(corresponde lanzar el producto | μ = 11,2) = 0,05" in _todo(a)
    assert "x̄c = 10,52" in _todo(a)
    assert "Si x̄ < 10,5238, se rechaza H0 → corresponde lanzar el producto" in _todo(a)
    assert "x̄ = 10,6 litros" in a.conclusion and "no corresponde lanzar el producto" in a.conclusion
    assert "1-β = 0,5231" in b.conclusion and "1 - β = P(corresponde lanzar el producto | μ = 10,5)" in b.conclusion
    assert "n = 30" in c.conclusion and "inferior a 10,8096 litros" in c.conclusion


def test_I_10_con_la_variable_escrita():
    _, (a, *_) = _resolver("I-10", variable="consumo de combustible de un automóvil en el recorrido")
    assert "(la media de consumo de combustible de un automóvil en el recorrido es menor que 11,2 litros)" in a.conclusion


def test_diseno_sistema_productivo():
    """Examen (ESTILO, ejemplo 2): n = 40, x̄c = 5,1306 piezas/min; las 4 probabilidades con «modificar»."""
    planteo = ("Se estudia la posibilidad de modificar el sistema productivo de una planta. Se estima que el nuevo "
               "sistema aumentaría la productividad a un valor promedio de 5,8 piezas por minuto. El sistema actual "
               "tiene una productividad promedio de 4,2 piezas por minuto con un desvío estándar de 2,53 piezas por "
               "minuto. El gerente desea tener una probabilidad de 0,95 de modificar el sistema cuando con la "
               "modificación se obtiene 5,8 piezas por minuto; además desea la certeza del 99% de no realizar la "
               "modificación cuando no se consigue el efecto deseado. Se asume que el desvío no se modificará.")
    an = analizar(planteo, ["Diseñar el ensayo: hallar el tamaño de muestra y la regla de decisión."])
    (a,) = resolver(an)
    t = _todo(a)
    assert "n = 40" in t and "5,1306 piezas por minuto" in t
    assert "1 - α = P(no corresponde modificar el sistema productivo de una planta | μ = 4,2) = 0,99" in t
    assert "1 - β = P(corresponde modificar el sistema productivo de una planta | μ = 5,8) = 0,95" in t


# ------------------------------------------------------------------ Tema II

def test_II_8_laminas():
    """Clase: S²c = 0,16098; n = 540 (528 más), con García. La unidad está dicha en palabras («en milímetros»)."""
    an, (a, b, c, d) = _resolver("II-8")
    assert an.datos["unidad"] == "milímetros"
    assert "S²c = σ₀²·χ²/ν = 0,09·χ²/11 = 0,16098" in _todo(b)
    assert "n = 540" in d.conclusion and "Δn = 540 - 12 = 528" in d.conclusion


def test_II_12_suelas():
    """Clase: Sc = 6,86 g; β = 0,3222 en σ = 8; n = 27 (17 más). Control de proceso: rechazar H0 = detener."""
    an, (a, b, c) = _resolver("II-12")
    assert "Sc = 6,86" in _todo(a)
    assert "Si S > 6,8554, se rechaza H0 → corresponde detener el proceso" in a.conclusion   # RD, no «ver arriba»
    assert "α = P(corresponde detener el proceso | σ = 5) = 0,05" in _todo(a)
    assert "β = 0,3222" in b.conclusion and "β = P(no corresponde detener el proceso | σ = 8)" in b.conclusion
    assert "n = 27" in c.conclusion and "Δn = 27 - 10 = 17" in c.conclusion
    assert "Si S > 6,1147" in _todo(c)


# ------------------------------------------------------------------ Tema III

def test_III_3_intervalo_exacto():
    """Clase: a) P(0,0051 ≤ p ≤ 0,3942) = 0,90; b) r = 0 ⇒ un solo límite con α entero: B = 0,2057."""
    _, (a, b) = _resolver("III-3", variable="piezas defectuosas")
    assert "P(0,0051 ≤ p ≤ 0,3942) = 0,9" in a.conclusion
    assert "El porcentaje poblacional de piezas defectuosas" in a.conclusion
    assert "0,2057" in b.conclusion and "α ENTERO" in _todo(b)


def test_III_11_control_de_proceso():
    """Clase: optimista; rc = 11; «Se revisan 50 piezas; si hay 11 o más defectuosas, se detiene el proceso y se
    revisa»; β = P(no detener | p = 0,14) = 0,9176; c) exacto n = 755, normal 715."""
    an, (a, b, c) = _resolver("III-11", variable="piezas defectuosas")
    assert an.criterio == "optimista" and an.datos["accion"] == "detenerlo y revisarlo"
    assert "Si en la muestra de 50 hay 11 o más piezas defectuosas, se rechaza H0: corresponde detenerlo y revisarlo"         in a.conclusion
    assert "β = 0,9176" in b.conclusion and "β = P(no corresponde detenerlo y revisarlo | p = 0,14)" in b.conclusion
    assert "n = 755" in c.conclusion and "n = 715" in c.conclusion


def test_III_16_campana():
    """Clase: pesimista; α = P(hacer otra campaña | p ≤ 0,12) = 0,01; exacto n = 1675 (rc = 233), normal 1637
    (rc = 229); «si en 1637 encuestados hay 229 o más interesados, se inicia una nueva campaña»; 1-β = 0,5159."""
    an, (a, b, *_) = _resolver("III-16", variable="encuestados interesados")
    assert an.criterio == "pesimista" and an.datos["accion"] == "efectuar otra campaña"
    t = _todo(a)
    assert "α = P(corresponde efectuar otra campaña | p = 0,12) = 0,01" in t
    assert "Si hay 233 o más encuestados interesados, se rechaza H0: corresponde efectuar otra campaña" in a.conclusion
    assert "n = 1637 y r_c = 229" in a.conclusion
    assert "1-β = 0,5159" in _todo(b) and "1 - β = P(corresponde efectuar otra campaña | p = 0,14)" in b.conclusion


def test_III_19_ruleta():
    """Clase: H0: p ≤ 1/37 (la denuncia va en H1, no es bilateral); α = 0,05; rc = 37; r = 42 ⇒ se rechaza:
    «puedo asegurar que el cero sale con una frecuencia mayor que 1/37»; 1-β = 0,9788."""
    _, (a, b) = _resolver("III-19", variable="ceros")
    assert "H0: p ≤ 1/37" in _todo(a) and "r_c = 37" in _todo(a)
    assert "Si hay 37 o más ceros, se rechaza H0" in _todo(a)
    assert "se rechaza la hipótesis nula" in a.conclusion
    assert "(la proporción de ceros es mayor que 1/37)" in a.conclusion
    assert "1-β = 0,9788" in b.conclusion


# ------------------------------------------------------------------ Tema IV

def test_IV_1_tornos():
    """Clase: P(0,2035 ≤ σA²/σB² ≤ 1,1136) = 0,90, «la varianza de A es como mínimo un 79,65 % menor y como máximo un
    11,36 % mayor que la de B»; n = 45; desvíos 0,4511 a 1,0553; n = 444."""
    _, (a, b, c, d) = _resolver("IV-1", nombre1="A", nombre2="B")
    t = a.conclusion
    assert "0,2035 ≤" in t and "≤ 1,1136" in t
    assert "como mínimo un 79,65% menor y como máximo un 11,36% mayor" in t
    assert "n = 45" in b.conclusion
    assert "0,4511 ≤" in c.conclusion and "≤ 1,0553" in c.conclusion
    assert "n = 444" in d.conclusion


def test_IV_4_hiladoras():
    """Clase: H0: φ ≥ 0,88 (pesimista); α = P(reacondicionar | no se reduce el 12 %); Jc = 0,3859; RD con J;
    J = 0,3729 ⇒ se rechaza: «se reduce el desvío en más de un 12 %»; 1-β = 0,1779; n = 128."""
    an, (a, b, c) = _resolver("IV-4")
    assert an.datos["accion"] == "reacondicionar a nuevo las hiladoras"
    t = _todo(a)
    assert "α = P(corresponde reacondicionar a nuevo las hiladoras |" in t
    assert "Si J < 0,3859" in t
    assert "J = 0,3729 cae en la zona de rechazo" in a.conclusion
    assert "se reduce en más de un 12%" in a.conclusion
    assert "1-β = 0,1779" in b.conclusion and "P(corresponde reacondicionar a nuevo las hiladoras | φ = 0,7)" in b.conclusion
    assert "n = 128" in c.conclusion
