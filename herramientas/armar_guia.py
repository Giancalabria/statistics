"""Une las transcripciones verificadas (`datos/verdad/tema_*.json`) en `datos/guia_ejercicios.json`.

    python herramientas/armar_guia.py

Las transcripciones se hicieron leyendo cada página del PDF (ver `datos/verdad/INSTRUCCIONES.md`).
Si falta el archivo de algún tema, se conservan los ejercicios de ese tema del JSON anterior.
"""

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VERDAD = RAIZ / "datos" / "verdad"
SALIDA = RAIZ / "datos" / "guia_ejercicios.json"

TEMAS = {
    "I": "Inferencia para medias (IC y ensayos)",
    "II": "Inferencia sobre varianzas / desvíos",
    "III": "Procesos de Bernoulli (proporciones)",
    "IV": "Comparación de varianzas (2 poblaciones)",
    "V": "Comparación de dos medias",
    "VI": "Contrastes chi-cuadrado",
    "VII": "Regresión y correlación simple",
    "VIII": "Modelo lineal general (regresión múltiple)",
}


def normalizar(ej: dict) -> dict:
    incisos = []
    for inc in ej.get("incisos", []):
        incisos.append({
            "letra": inc["letra"],
            "texto": inc.get("texto", ""),
            "respuesta": inc.get("respuesta", ""),
            "valores": inc.get("valores", []),
            **({"decision": inc["decision"]} if inc.get("decision") else {}),
        })
    planteo = ej.get("planteo", "").strip()
    if incisos and incisos[0]["letra"] == "única":
        enunciado = planteo if incisos[0]["texto"] in planteo else f"{planteo} {incisos[0]['texto']}"
    else:
        enunciado = planteo + " " + " ".join(f"{i['letra']}) {i['texto']}" for i in incisos)
    out = {
        "id": ej["id"], "tema": ej["tema"], "tema_nombre": TEMAS[ej["tema"]], "numero": ej["numero"],
        "pagina": ej.get("pagina"), "enunciado": enunciado.strip(), "planteo": planteo, "incisos": incisos,
        "tablas": ej.get("tablas", []), "respuesta": ej.get("respuesta", ""),
        "respuesta_fuente": ej.get("respuesta_fuente", "resp" if ej.get("respuesta") else "ninguna"),
        "resuelto": bool(ej.get("resuelto")), "conclusiones": ej.get("conclusiones", []),
        "observaciones": ej.get("observaciones", ""),
    }
    for extra in ("alpha", "que_pide", "sumatorias", "tablas_solucion"):
        if extra in ej:
            out[extra] = ej[extra]
    return out


def main():
    anterior = json.loads(SALIDA.read_text(encoding="utf-8")) if SALIDA.exists() else []
    salida = []
    for tema in TEMAS:
        archivo = VERDAD / f"tema_{tema}.json"
        if archivo.exists():
            ejs = [normalizar(e) for e in json.loads(archivo.read_text(encoding="utf-8"))]
            print(f"Tema {tema}: {len(ejs)} ejercicios (verificados)")
        else:
            ejs = [e for e in anterior if e["tema"] == tema]
            print(f"Tema {tema}: {len(ejs)} ejercicios (SIN verificar, del JSON anterior)")
        salida += sorted(ejs, key=lambda e: e["numero"])
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Total: {len(salida)} -> {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
