"""La sección Teoría: cada documento existe, se parte en secciones y el buscador filtra."""

import teoria


def test_los_documentos_existen_y_se_parten():
    for doc in teoria.DOCUMENTOS:
        texto = (teoria.RAIZ / doc.archivo).read_text(encoding="utf-8")
        _, partes = teoria.secciones(texto)
        assert len(partes) >= 2, doc.archivo


def test_buscar_sin_tildes_y_recortar_subsecciones():
    texto = (teoria.RAIZ / "estudio/GUIA_CONTROL.md").read_text(encoding="utf-8")
    _, partes = teoria.secciones(texto)
    por_tema = next(c for t, c in partes if t.startswith("2."))
    assert teoria.coincide(por_tema, "WELCH apareadas")
    recorte = teoria.recortar(por_tema, "welch")
    assert "Comparación de medias" in recorte and "Proporción (Tema III)" not in recorte


def test_los_links_locales_quedan_en_negrita():
    assert teoria._limpiar("ver [REGLAS.md](REGLAS.md) y [x](https://a.b)") == "ver **REGLAS.md** y [x](https://a.b)"
