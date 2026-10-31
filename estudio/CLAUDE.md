# Estadística Aplicada: estudio para el 2° parcial

Carpeta `estudio/` del repo del solver, para preparar el **2° parcial de Estadística Aplicada (UADE)**, que es el que hay que aprobar. Docente: Ing. Sergio Aníbal Dopazo (cátedra Dopazo–García). El plan y el estado de avance están en [PLAN.md](PLAN.md); las reglas del profesor, en [REGLAS_PROFESOR.md](REGLAS_PROFESOR.md); qué controlar del planteo de la app, en [GUIA_CONTROL.md](GUIA_CONTROL.md).

## Prioridad de las fuentes

1. **Lo que dice el profesor en clase** (grabaciones del cuaderno de NotebookLM). Manda sobre todo lo demás.
2. El apunte y la Guía de Problemas 2026. Si la guía contradice al profesor, se sigue al profesor y se anota la diferencia (por ejemplo, III-3b y III-11c).
3. Los `.md` de la raíz del repo (armados con IA). Si contradicen al profesor, están mal.

Si hay una contradicción que no está clara, preguntarle al usuario antes de decidir.

## Al empezar una sesión

1. Leer `PLAN.md`, en especial la sección **Estado actual**, para saber qué examen o tema toca.
2. **Conectarse a NotebookLM** y revisar si hay fuentes nuevas, sobre todo grabaciones de clases después del 22/10. Si hay, leerlas completas, sumar sus reglas a `REGLAS_PROFESOR.md` y sus ejercicios a `PLAN.md`. Los informes por clase están en `informes/`.
3. No responder ejercicios de memoria: leer el enunciado real de la guía (`datos/guia_ejercicios.json` o la fuente de NotebookLM).

## NotebookLM

- Cuaderno: **Estadistica**, ID `211f0336-5aad-4eba-829f-ac4427955c5c`.
- En la Mac: wrapper `~/Software/Personal/.tools/bin/notebooklm`. En la PC con Windows: el comando es `notebooklm` (notebooklm-py en `~/.local/share/notebooklm-py`, con login hecho). No leer `.notebooklm/`.
- Nunca usar `notebooklm ask --new`: borra el historial de chat del cuaderno.
- Comandos útiles:
  ```sh
  NB=~/Software/Personal/.tools/bin/notebooklm
  $NB use 211f0336                      # seleccionar el cuaderno
  $NB source list                       # listar fuentes (buscar nuevas)
  $NB source fulltext <id> -o out.txt   # texto completo (las grabaciones vienen transcriptas)
  $NB source search "amalgamado"        # buscar pasajes en todas las fuentes
  $NB ask "..."                         # preguntarle al cuaderno (respuesta con citas)
  ```
- Guardar los textos descargados en el scratchpad, no en esta carpeta.
- Las transcripciones son automáticas y tienen errores (números mal reconocidos). Verificar los números con scipy o con la guía.

## El solver (raíz del repo)

- App Streamlit que resuelve los ejercicios (la raíz de este repo, rama `main`). Funciona sin internet, con la IA local (Ollama + `qwen3:8b`) para interpretar enunciados. El profesor permite computadora y programas propios en el examen, con wifi apagado.
- **Desde el 31/10, en el examen el solver resuelve y el usuario controla el planteo** (ver `PLAN.md`, sección «Enfoque»). Las cuentas del solver están verificadas; lo que falla es la interpretación del enunciado. El catálogo de fallas está en `GUIA_CONTROL.md`.
- Si el solver contradice una regla del profesor, corregir el solver (y sus tests) y anotarlo en `CONVENCIONES_CATEDRA.md`.
- Banco de exámenes reales: `datos/examenes_reales.json`. Un examen nuevo se mide **a ciegas** (`python herramientas/evaluar_examenes.py --ia`) antes de corregir nada.

## Cómo trabajar conmigo

- **Practicamos con exámenes reales**, no resolviendo en papel. En cada sesión: darme el examen sin la resolución; yo lo cargo en la app, controlo el planteo con `GUIA_CONTROL.md` y escribo la respuesta como la entregaría.
- Corregir mi respuesta contra la referencia y `REGLAS_PROFESOR.md`: qué error de la app se me escapó, qué falta en la redacción (H0 justificada, distribución justificada, 4 decimales, conclusión en términos del problema, probabilidades nunca en %) y cuánto tardé.
- Explicar la teoría **solo en lo conceptual** (cuándo se usa cada test, cómo se plantea H0, qué significa el resultado), no las cuentas a mano.
- Cada error real de la app que aparezca: agregarlo a `GUIA_CONTROL.md` (sección 3) y, si es general, corregir el solver.
- Al terminar una sesión, **actualizar la sección «Estado actual» de `PLAN.md`**: marcar lo hecho, anotar errores detectados y la fecha.
