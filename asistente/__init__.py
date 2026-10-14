"""Asistente con un modelo de lenguaje LOCAL (Ollama), sin internet.

La IA no hace cuentas: todos los números los calcula `solver/`. El modelo sirve para lo que a las reglas
les cuesta:

- `interpretar`: cuando las reglas de `interprete/` no entienden un enunciado (tema no identificado, un
  inciso que no saben clasificar, datos que faltan), el modelo lee el texto y devuelve el planteo en el
  mismo formato que el analizador (JSON validado). Solo se aplica donde las reglas fallaron; el resto
  queda como sugerencia para revisar.
- `explicar`: redacta / explica una resolución YA calculada por el solver, con las convenciones de la
  cátedra, y marca cualquier número que no salga de los resultados.
- `contexto`: busca en los apuntes del repo (convenciones, esquema teórico, guía resuelta) lo que se le
  pasa al modelo para responder preguntas.

Configuración (variables de entorno): `OLLAMA_HOST` (por defecto http://localhost:11434) y
`ASISTENTE_MODELO` (por defecto qwen3:8b). Ver `ASISTENTE_IA.md`.
"""
