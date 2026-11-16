# Solver de Estadística Aplicada (UADE)

App Streamlit que resuelve los ejercicios de la cátedra Dopazo: reglas (`interprete/`), cálculo (`solver/`) e IA local opcional (`asistente/`, Ollama + `qwen3:8b`).

- **Estudio para el 2° parcial (19/11/2026):** todo está en [estudio/](estudio/). Al empezar una sesión de estudio, leer `estudio/CLAUDE.md` y la sección «Estado actual» de `estudio/PLAN.md`.
- **En el examen la app resuelve y el usuario controla el planteo**: `estudio/GUIA_CONTROL.md` tiene el control y el catálogo de fallas reales de la app.
- **Sección «Teoría» de la app** (`teoria.py`): muestra los .md útiles para resolver, con buscador. Para sumar uno, agregarlo a `DOCUMENTOS`.
- Reglas del profesor: `estudio/REGLAS_PROFESOR.md`. Mandan sobre la guía y sobre el solver; si el solver las contradice, se corrige y se anota en `CONVENCIONES_CATEDRA.md`.

## Comandos

```sh
streamlit run app.py                              # la app (o ./levantar.sh)
python -m pytest -q                               # tests
python herramientas/evaluar_guia.py               # la guía completa (532/536 al 31/10)
python herramientas/evaluar_examenes.py [--ia]    # exámenes reales; --ia = consenso (Ollama abierto)
python herramientas/generar_ejercicios_nuevos.py   # ejercicios nuevos tipo examen con otras redacciones (tanda 1: datos/ejercicios_nuevos.json; tandas 2 a 5: ejercicios_nuevos_2.json … _5.json)
python herramientas/evaluar_examenes.py --archivo ejercicios_nuevos.json [--ia]   # la app a ciegas sobre esos ejercicios (o ejercicios_nuevos_2 … _5.json)
python herramientas/evaluar_clase.py [--reglas]   # ejercicios resueltos en clase, a ciegas (datos/clase_resueltos.json)
python herramientas/optimizar_prompts.py <variante> guia|validacion   # variantes de prompt (afinar con guía, validar fuera)
python herramientas/auditar_origen.py [III IV V-12 ...] [--detalle]   # números de la resolución sin fórmula ni dato («de la galera»)
python herramientas/comparar_redaccion_examenes.py [--solo T1] [--solo-partes]   # redacción completa vs. por partes (Ollama)
python herramientas/comparar_redaccion_clase.py [--partes]   # redacción vs. el pizarrón del profesor (Ollama)
```

En Windows: `python -X utf8` (o `PYTHONUTF8=1`).
