"""Extrae los ejercicios de la Guía de Problemas (PDF) a `datos/guia_ejercicios.json`.

Se corre una sola vez (o cuando cambie la guía):

    python herramientas/extraer_guia.py [ruta_al_pdf]

Para cada ejercicio guarda: tema, número, página, planteo, incisos, respuesta
(`Resp:`) y la resolución si la guía la trae (`Solución:`). Las fórmulas de las
resoluciones salen desordenadas del PDF, pero el texto corrido (conclusiones,
explicaciones) se lee bien y es lo que usa la app.

Requiere `pypdf` (solo para esta herramienta, la app no lo necesita).
"""

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PDF_DEFAULT = RAIZ.parent / "OneDrive_2_23-8-2026" / "Guia Problemas Estadística Aplicada 2026.pdf"
SALIDA = RAIZ / "datos" / "guia_ejercicios.json"

# Encabezados de tema tal como aparecen en el cuerpo de la guía (no en el índice).
TEMAS = [
    ("I", "Inferencia para medias (IC y ensayos)"),
    ("II", "Inferencia sobre varianzas / desvíos"),
    ("III", "Procesos de Bernoulli (proporciones)"),
    ("IV", "Comparación de varianzas (2 poblaciones)"),
    ("V", "Comparación de dos medias"),
    ("VI", "Contrastes chi-cuadrado"),
    ("VII", "Regresión lineal simple"),
    ("VIII", "Modelo lineal general"),
]

# Numeraciones internas de algunas resoluciones que parecen inicio de ejercicio.
FALSOS_INICIOS = re.compile(r"^(Si se resuelve|Esta resoluci)")

RE_ENCABEZADO = re.compile(r"^Ing\. Roberto M\. Garc.a .*Gu.a de Problemas")
RE_PIE = re.compile(r"^\s*(\d+) de 62\s*$")
RE_TEMA = re.compile(r"^\s*TEMA (VIII|VII|VI|IV|V|III|II|I)\s*[-–]")
RE_INICIO = re.compile(r"^\s*(\d{1,2})\)\s+(\S.*)$")
RE_INCISO = re.compile(r"(?:(?<=\s)|^)([a-h])\)\s")


def leer_lineas(pdf: Path):
    """Devuelve [(pagina_impresa, linea)] sin encabezados ni pies de página."""
    import pypdf

    lector = pypdf.PdfReader(str(pdf))
    salida = []
    for idx, page in enumerate(lector.pages):
        pagina = idx - 1  # la hoja 2 del PDF es la "1 de 62"
        for linea in page.extract_text().splitlines():
            m = RE_PIE.match(linea)
            if m:
                pagina = int(m.group(1))
                continue
            if RE_ENCABEZADO.match(linea):
                continue
            salida.append((pagina, linea.rstrip()))
    return salida


def limpiar(texto: str) -> str:
    texto = texto.replace("\uf020", " ")
    texto = re.sub(r"[\uf000-\uf8ff]", "", texto)  # glifos de la fuente Symbol
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r" *\n *", "\n", texto)
    return texto.strip()


def unir_parrafo(texto: str) -> str:
    """Une las líneas cortadas por el ancho de página en un único párrafo."""
    return re.sub(r"\s*\n\s*", " ", texto).strip()


def separar_incisos(enunciado: str):
    """Parte el enunciado en planteo + incisos a), b), c)...

    Solo corta en letras consecutivas (a, b, c, ...) para no confundir con
    textos como 'i)' o 'ii)' que la guía usa para listar condiciones.
    """
    esperado = "a"
    cortes = []
    for m in RE_INCISO.finditer(enunciado):
        if m.group(1) == esperado:
            cortes.append((m.start(1), m.end(), esperado))
            esperado = chr(ord(esperado) + 1)
    if not cortes:
        return enunciado.strip(), []
    planteo = enunciado[: cortes[0][0]].strip()
    incisos = []
    for i, (ini, fin_marca, letra) in enumerate(cortes):
        fin = cortes[i + 1][0] if i + 1 < len(cortes) else len(enunciado)
        incisos.append({"letra": letra, "texto": enunciado[fin_marca:fin].strip()})
    return planteo, incisos


def conclusiones(solucion: str):
    """Oraciones legibles de la resolución (las que sacan conclusiones)."""
    oraciones = re.split(r"(?<=\.)\s+", unir_parrafo(solucion))
    claves = ("conclu", "se rechaza", "no se rechaza", "se puede", "no se puede", "comprendid", "se acepta", "se debe")
    salida = []
    for o in oraciones:
        if any(c in o.lower() for c in claves) and len(o) < 600:
            salida.append(o.strip())
    return salida


def extraer(pdf: Path):
    lineas = leer_lineas(pdf)

    # 1) Ubicar los temas (se saltea el índice: la primera aparición real es tras "1 de 62").
    tema_actual = None
    bloques = {}  # tema -> [(pagina, linea)]
    for pagina, linea in lineas:
        if pagina < 1:
            continue
        m = RE_TEMA.match(linea)
        if m:
            tema_actual = m.group(1)
            bloques.setdefault(tema_actual, [])
            continue
        if tema_actual:
            bloques[tema_actual].append((pagina, linea))

    ejercicios = []
    for tema, nombre in TEMAS:
        cuerpo = bloques.get(tema, [])
        # 2) Inicios de ejercicio: numeración consecutiva, precedida por línea en blanco.
        inicios = []
        esperado = 1
        previa_vacia = True
        en_resp = False  # a veces el ejercicio siguiente viene pegado al "Resp:" anterior
        for i, (pagina, linea) in enumerate(cuerpo):
            m = RE_INICIO.match(linea)
            if (m and (previa_vacia or en_resp) and int(m.group(1)) == esperado
                    and not FALSOS_INICIOS.match(m.group(2))):
                inicios.append(i)
                esperado += 1
                en_resp = False
            previa_vacia = not linea.strip()
            if linea.lstrip().startswith("Resp"):
                en_resp = True
            elif previa_vacia:
                en_resp = False
        for k, ini in enumerate(inicios):
            fin = inicios[k + 1] if k + 1 < len(inicios) else len(cuerpo)
            pagina = cuerpo[ini][0]
            texto = "\n".join(l for _, l in cuerpo[ini:fin])
            texto = re.sub(r"^\s*\d{1,2}\)\s+", "", texto, count=1)
            texto = limpiar(texto)

            solucion = ""
            partes = re.split(r"\n\s*Soluci[oó]n\s*:?\s*\n", texto, maxsplit=1)
            if len(partes) == 2:
                texto, solucion = partes
            resp = ""
            partes = re.split(r"\n\s*Resp\s*:", texto, maxsplit=1)
            if len(partes) == 2:
                texto, resp = partes
            elif solucion:
                partes = re.split(r"\n\s*Resp\s*:", solucion, maxsplit=1)
                if len(partes) == 2:
                    solucion, resp = partes

            enunciado = unir_parrafo(texto)
            planteo, incisos = separar_incisos(enunciado)
            ejercicios.append({
                "id": f"{tema}-{k + 1}",
                "tema": tema,
                "tema_nombre": nombre,
                "numero": k + 1,
                "pagina": pagina,
                "enunciado": enunciado,
                "planteo": planteo,
                "incisos": incisos,
                "respuesta": unir_parrafo(resp),
                "resuelto": bool(solucion.strip()),
                "conclusiones": conclusiones(solucion) if solucion else [],
            })
    return ejercicios


def main():
    pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else PDF_DEFAULT
    ejercicios = extraer(pdf)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(ejercicios, ensure_ascii=False, indent=1), encoding="utf-8")
    por_tema = {}
    for e in ejercicios:
        por_tema[e["tema"]] = por_tema.get(e["tema"], 0) + 1
    print(f"{len(ejercicios)} ejercicios -> {SALIDA}")
    print("Por tema:", por_tema)
    print("Resueltos:", sum(e["resuelto"] for e in ejercicios))


if __name__ == "__main__":
    main()
