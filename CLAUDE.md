# Solver de Estadística Aplicada (UADE)

App Streamlit que resuelve los ejercicios de la cátedra Dopazo: reglas (`interprete/`), cálculo (`solver/`) e IA local opcional (`asistente/`, Ollama + `qwen3:8b`).

- **Estudio para el 2° parcial (19/11/2026):** todo está en [estudio/](estudio/). Al empezar una sesión de estudio, leer `estudio/CLAUDE.md` y la sección «Estado actual» de `estudio/PLAN.md`.
- **En el examen la app resuelve y el usuario controla el planteo**: `estudio/GUIA_CONTROL.md` tiene el control y el catálogo de fallas reales de la app.
- Reglas del profesor: `estudio/REGLAS_PROFESOR.md`. Mandan sobre la guía y sobre el solver; si el solver las contradice, se corrige y se anota en `CONVENCIONES_CATEDRA.md`.

## Comandos

```sh
streamlit run app.py                              # la app (o ./levantar.sh)
python -m pytest -q                               # tests
python herramientas/evaluar_guia.py               # la guía completa (532/536 al 31/10)
python herramientas/evaluar_examenes.py [--ia]    # exámenes reales; --ia = consenso (Ollama abierto)
```

En Windows: `python -X utf8` (o `PYTHONUTF8=1`).
