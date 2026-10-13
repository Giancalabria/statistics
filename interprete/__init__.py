"""Intérprete de enunciados: lee el texto de un problema y arma el planteo para el solver.

Funciona 100% offline y sin modelos de lenguaje: usa reglas (palabras clave y
patrones del estilo de redacción de la cátedra) y un buscador de ejercicios
parecidos de la Guía de Problemas (`datos/guia_ejercicios.json`).

Flujo:
    analizador.analizar(planteo, incisos) -> Analisis   (editable por el usuario)
    resolver.resolver(analisis)            -> resultados por inciso
"""

# Temas resueltos en módulos aparte: se registran al importarse.
from . import chi_modelos, regresion  # noqa: E402,F401
from . import dos_muestras  # noqa: E402,F401  (TEMA V: comparación de dos medias)
