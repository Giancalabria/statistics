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


def test_numeros_al_pie_de_la_letra_y_con_su_signo():
    f = "P(55,128 ≤ μ ≤ 56,206) = 0,99; P(β1 ≤ -0,3747) = 0,95; 82,77% con 95% de confianza; Σy = 1.696"
    assert rp.numeros_literales("entre 55,128 y 56,206", f) == []
    assert rp.numeros_literales("entre 55,13 y 56,21", f) == ["55,13", "56,21"]       # otro redondeo (hacia adentro)
    assert rp.numeros_literales("una reducción de 0,3747", f) == ["0,3747 (signo)"]   # da vuelta el sentido
    assert rp.numeros_literales("un cambio de -0,3747", f) == []
    assert rp.numeros_literales("el 82,77%, con 95%; 1.696", f) == []


def test_la_unidad_de_la_ia_completa_la_que_detecto_el_solver(ia):
    ia(IAFalsa({"variable": "maleabilidad", "unidad": "Tn/mm2"}, rechaza=False))
    red = rp.redactar_por_partes(_examen("F3"), hilos=1)
    assert "X = maleabilidad, en Tn/mm2." in red.texto


def test_la_unidad_se_compara_sin_espacios():
    assert rp._sin_espacios("cm3/cm2/s") in rp._sin_espacios("permeabilidad al aire (cm3 /cm2 /s) de varios tipos")


def test_una_proporcion_dentro_de_otro_tema_lleva_su_propio_nombre(ia):
    ia(IAFalsa({"variable": "tiempo de respuesta", "unidad": "mili-segundos"},
               que_pide="disyuntores de la Marca B que no cumplen con la especificación", rechaza=True))
    red = rp.redactar_por_partes(_examen("P2"), hilos=1)
    assert "porcentaje poblacional de disyuntores de la Marca B que no cumplen" in red.texto
    assert "porcentaje poblacional de tiempo de respuesta" not in red.texto


def test_afirmar_en_una_comparacion_va_en_h1():
    an = _examen("P2")
    a = resolver(an)[0]
    just = next(p for p in a.pasos if p.startswith("**Justificación de H0"))
    assert "El enunciado dice qué se quiere probar" in just and "Criterio optimista" not in just


def test_los_grupos_sin_nombre_se_nombran_con_el_dato_de_cada_uno(ia, monkeypatch):
    nombres = {"1.050": "marca Y", "1.250": "marca X"}
    falsa = IAFalsa({"variable": "duración de una lámpara", "unidad": "horas"}, rechaza=False)

    def chat(mensajes, **kw):
        if mensajes[0]["content"] is rp._NOMBRE:
            valor = mensajes[-1]["content"].split("es ")[-1].rstrip(".")
            return json.dumps({"nombre": nombres.get(valor, "")})
        return falsa(mensajes, **kw)
    ia(chat)
    red = rp.redactar_por_partes(_examen_nuevo("N4"), hilos=1)
    assert "μ(marca X) ≤ 1,15·μ(marca Y)" in red.texto and "Muestra" not in red.texto


def test_un_nombre_cruzado_no_pasa(ia):
    def chat(mensajes, **kw):
        if mensajes[0]["content"] is rp._NOMBRE:          # contesta al revés: «marca X» para el promedio de 1.050
            return json.dumps({"nombre": "marca X" if "1.050" in mensajes[-1]["content"] else "marca Y"})
        return IAFalsa({"variable": "duración de una lámpara"}, rechaza=False)(mensajes, **kw)
    ia(chat)
    red = rp.redactar_por_partes(_examen_nuevo("N4"), hilos=1)
    assert any("misma oración" in d for d in red.descartados)


def _examen_nuevo(ident):
    ex = next(e for e in json.load(open("datos/ejercicios_nuevos.json", encoding="utf-8")) if e["id"] == ident)
    return analizar(ex["planteo"], [tuple(i) for i in ex["incisos"]], tablas=ex["tablas"])


def test_ejercicios_nuevos_lo_que_se_quiere_probar_nombres_y_r_de_un_porcentaje():
    n2 = resolver(_examen_nuevo("N2"))[0]
    just = next(p for p in n2.pasos if p.startswith("**Justificación"))
    assert "demuestra que su espesor es más regular" in just and "Criterio optimista" not in just
    n3 = resolver(_examen_nuevo("N3"))[0]
    assert "μ(Antes) - μ(Después)" in n3.resumen                  # sin el salto de línea del renglón «Antes: …»
    n10 = resolver(_examen_nuevo("N10"))[1]
    assert any("r = p̂·n = 0,0625·400 = 25" in p for p in n10.pasos)
    assert any("1/[1 + ((n − r + 1)/r)·F] = 1/[1 + (376/25)" in p for p in n10.pasos)
