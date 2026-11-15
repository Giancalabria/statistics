"""Redacción por partes: el solver escribe los números y la IA solo palabras validadas (sin Ollama: IA simulada)."""

import json

import pytest

from asistente import cliente
from asistente import redaccion_partes as rp
from interprete.analizador import analizar
from interprete.resolver import resolver

RAIZ_EX = "datos/examenes_reales.json"


def _examen(ident):
    ex = next(e for e in json.load(open(RAIZ_EX, encoding="utf-8")) if e["id"] == ident)
    return analizar(ex["planteo"], [tuple(i) for i in ex["incisos"]], tablas=ex["tablas"])


class IAFalsa:
    """Responde según la consigna; `textos` = respuestas para los huecos de texto, en orden por tipo."""

    def __init__(self, palabras, que_pide="", opuestas=True, textos=None, rechaza=None):
        self.palabras, self.que_pide, self.opuestas = palabras, que_pide, opuestas
        self.textos = textos or {}
        self.rechaza = rechaza
        self.pedidos = []

    def __call__(self, mensajes, **kw):
        sistema, usuario = mensajes[0]["content"], mensajes[-1]["content"]
        self.pedidos.append(usuario)
        if sistema is rp._PALABRAS_SISTEMA:
            return json.dumps(self.palabras)
        if sistema is rp._CONTRARIO:
            return json.dumps({"que_pide": self.que_pide})
        if sistema is rp._OPUESTAS:
            return json.dumps({"opuestas": self.opuestas})
        if sistema is rp._CONSISTENCIA:
            return json.dumps({"rechaza": self.rechaza})
        for clave, texto in self.textos.items():
            if clave in usuario:
                return texto
        return "Texto de contexto del problema."


@pytest.fixture
def ia(monkeypatch):
    def poner(falsa):
        monkeypatch.setattr(cliente, "chat", falsa)
        return falsa
    return poner


def test_validaciones_de_frases():
    enun = "Se cuentan las unidades con fallas de un proceso productivo."
    assert rp._frase_ok("unidades con fallas", enun) is None
    assert rp._frase_ok("9 unidades", enun) == "tiene números"
    assert rp._frase_ok("clientes satisfechos", enun) == "sus palabras no salen del enunciado"


def test_para_el_examen_saca_las_notas_de_la_app_y_deja_las_cuentas():
    paso = ("**Variable** (paso 1): X = ⟨qué se mide⟩. _El profesor exige definirla; completala en «Variable»._")
    assert rp.para_el_examen(paso) == "**Variable**: X = ⟨qué se mide⟩."
    fe = ("**Frecuencias esperadas** Feᵢ = N·P(clase i) (se completa el dominio del modelo con clases de Fo = 0):"
          "\n\n| Clase | Fo |\n|---|---|\n| 0 a 15 | 0 |")
    assert rp.para_el_examen(fe) == fe                     # «se completa» no es una nota para el alumno
    alfa = ("α = 0,05 — riesgo máximo. **El enunciado no lo fija: se elige y se justifica antes de ver los datos** "
            "(p. ej. «α = 0,05: …»). Una vez fijado, α no se toca.")
    assert rp.para_el_examen(alfa) == "α = 0,05 — riesgo máximo. Una vez fijado, α no se toca."


def test_t2_los_numeros_son_los_del_solver_y_el_b_cuenta_las_no_falladas(ia):
    falsa = ia(IAFalsa({"variable": "unidades con fallas", "unidad": ""}, que_pide="unidades no falladas",
                       rechaza=False,
                       textos={"Respondé la pregunta del inciso «¿Considera": "No hay evidencia suficiente para "
                                                                             "asegurar que el proceso no cumple."}))
    red = rp.redactar_por_partes(_examen("T2"), hilos=1)
    assert "r = cantidad de unidades con fallas" in red.texto
    assert "(unidades no falladas) → r = n - 9 = 95 - 9 = 86" in red.texto
    assert "porcentaje poblacional de unidades no falladas estará entre 82,77% y 95,58%" in red.texto
    assert "G_b(11) = 0,0683 > α y G_b(12) = 0,0335 ≤ α" in red.texto
    assert "**Respuesta**: No hay evidencia suficiente" in red.texto
    assert "profesor" not in red.texto.lower() and "Aviso" not in red.texto
    assert any("Considera" in p for p in falsa.pedidos)


def test_lo_contrario_que_no_es_opuesto_no_se_usa(ia):
    ia(IAFalsa({"variable": "unidades con fallas"}, que_pide="unidades falladas", opuestas=False, rechaza=False))
    red = rp.redactar_por_partes(_examen("T2"), hilos=1)
    assert "unidades falladas" not in red.texto        # diría lo opuesto de lo que pide el b)
    assert "estimar → r = n - 9" in red.texto           # el b) queda con el texto del solver, sin nombre
    assert any("no es lo contrario" in d for d in red.descartados)


def test_un_texto_con_un_numero_inventado_o_que_contradice_la_decision_se_descarta(ia):
    ia(IAFalsa({"variable": "unidades con fallas"}, que_pide="unidades no falladas", rechaza=True,
               textos={"Respondé la pregunta del inciso «¿Considera": "Se rechaza: el proceso no cumple.",
                       "Explicá por qué las hipótesis": "El 33,3337 de las unidades falla."}))
    red = rp.redactar_por_partes(_examen("T2"), hilos=1)
    # el número inventado no llega: se pide de nuevo con el motivo y queda el texto corregido
    assert "33,3337" not in red.texto and "**En este problema**: Texto de contexto del problema." in red.texto
    # la consistencia la decide otra pregunta: acá dice que rechaza y el solver no rechazó
    assert any("contradice la decisión" in d for d in red.descartados)
    assert "Se rechaza: el proceso no cumple" not in red.texto


def test_t1_numeros_del_solver_y_cota_con_su_expresion_formal(ia):
    ia(IAFalsa({"variable": "tiempo de fabricación de una pieza", "unidad": "minutos por pieza"}, rechaza=False))
    red = rp.redactar_por_partes(_examen("T1"), hilos=1)
    t = red.texto
    assert "e = t(0,9; 229)·σ(d) = 1,2853·0,610721 = 0,7849" in t
    assert "P(μ(equipo “A”) - μ(equipo “B”) ≤ 1,2268) = 0,9" in t
    assert "d*_c = δ₀ + t(0,95; 229)·σ(d*)" in t and "Si d* > 1,0142" in t
    assert "x̄ = Σmᵢ·Foᵢ/n = 2.702,5/103 = 26,2379" in t      # de dónde sale x̄ de B
    assert "| 0 a 15 |" in t and "-∞ a 15" not in t              # la Gamma empieza en 0
    assert "| **Total** | **128** |" in t


def test_sin_ia_util_queda_la_resolucion_del_solver(ia):
    ia(IAFalsa({"variable": "123"}, rechaza=None))
    red = rp.redactar_por_partes(_examen("T2"), hilos=1)
    assert "⟨qué se cuenta" in red.texto and "⚠️ Quedaron huecos" in red.texto
    assert "r_c = 12" in red.texto
