# Asistente con IA local (sin internet)

La app usa un modelo de lenguaje que corre **en la propia computadora** con [Ollama](https://ollama.com).
Es opcional: si Ollama no está abierto, la app funciona exactamente igual que antes (solo reglas + solver).

## Qué hace y qué no

La IA **no hace cuentas**. Todos los números los sigue calculando `solver/`, que está verificado contra la guía.
El modelo se usa para lo que a las reglas les cuesta:

| Dónde | Qué hace la IA |
|---|---|
| **Interpretar un enunciado** → **🗳️ Interpretar** (la página que abre la app; lo que se usa en el examen) | Tres lecturas del mismo enunciado: las **reglas**, la **IA con ejemplos** (`interpretar.pedir_ia`) y la **IA por tema** (`por_tema.pedir_ia_tema`: primero clasifica el tema, después un prompt corto con solo las claves de ese tema y ejemplos del mismo tema). Las cuentas sobre tablas y listas las pone siempre el programa (`interpretar.completar_con_reglas`). Por inciso se vota (`asistente/consenso.py`): ✅ consenso si al menos dos dan el mismo planteo y los mismos números; ⚠️ sin consenso → elegís la lectura con un botón. El resultado se calcula solo; si corregís algo, *🧮 Recalcular*. Si las dos IA coinciden contra las reglas se elige lo de las IA, pero se marca **⚠️ las 2 IA contra las reglas** (no ✅): son el mismo modelo y se equivocan juntas. Medido el 04-05/11 con qwen3:8b: exámenes del 2° parcial, 30/30 y ningún ✅ equivocado; banco completo con el código de la app, 35/35; enunciados trampa (82 incisos), 76/82 elegidos bien y 1 ✅ equivocado (sin la marca ⚠️ eran 5). ~1 min por problema con la Mac despierta. Un consenso puede estar equivocado: controlar el planteo con `estudio/GUIA_CONTROL.md`. |
| **Interpretar un enunciado** → **⚡ Solo reglas** | Solo las reglas, sin IA, al instante. Plan B si Ollama no anda. |
| **Interpretar un enunciado** → *💬 Explicar con IA* (después de Calcular) | Explica por qué se eligió cada camino y redacta la respuesta de examen con las convenciones de la cátedra, a partir de la resolución del solver. Marca con ⚠️ cualquier número que no salga del enunciado ni de la resolución. |
| **Asistente IA** (página 8) | **Un solo campo de chat, sin opciones.** Si lo que mandás parece un **enunciado** (varios datos y además incisos, una tabla o una consigna), se resuelve en modo **🗳️ consenso** (reglas + 2 lecturas de IA, se vota) y se muestra el estado de cada inciso (✅ consenso / ⚠️ sin consenso / ☝️ una sola lectura) y la resolución del solver; después la IA lo redacta sin agregar números. Si es una **pregunta** o un pedido («explicame…», «revisá mi respuesta…»), responde con los apuntes del repo y el último ejercicio resuelto (del chat o de *Interpretar un enunciado*). Con 📎 se adjunta material (txt, md, csv, json, pdf). Los números que no salen de la app ni del material se marcan con ⚠️. |

La IA **nunca hace las cuentas**: no hay un modo «solo IA» porque un modelo de 8B se equivoca en aritmética y el
solver está verificado dígito a dígito contra la guía. Para resolver charlando está la página *Asistente IA*.

**Modos que se sacaron de la pantalla (04/11).** *⚖️ Comparar*, *🛡️ Revisión*, *🧩 Híbrido* y *🤖 La IA sola* rendían menos que el consenso o mostraban lo mismo con más pasos. El código sigue (`comparar.py`, `revisar.py`, `interpretar.interpretar`, `simple.py`) porque lo usan `herramientas/evaluar_guia.py` y los tests. La IA razonada (`simple.plantear`) era la tercera lectura del consenso hasta el 04/11: en los exámenes del 2° parcial acertaba 22/30 y tardaba ~104 s por problema (la IA por tema: 23/30 sola, pero el consenso con ella da 30/30 contra 29/30, en la mitad del tiempo).

**Reglas del profesor en los prompts.** Las instrucciones de *Explicar con IA* (`asistente/explicar.py`) y la
redacción (`asistente/redactar.py`, que lee `ESTILO_CATEDRA.md`) siguen lo que dijo el profesor en clase, que manda
sobre la guía: probabilidades entre 0 y 1 (nunca en %), mínimo 4 decimales en el desarrollo, Z/t justificadas por
la estructura (dividir por el parámetro σ o por la variable aleatoria S), estimador contra valor crítico, nunca
«acepto H0», sin bilaterales en p, σ², σ ni comparaciones, sin decidir con α*, estimación de p siempre exacta y
sin β ni n con t. Ojo: el profesor dijo en clase que no acepta resoluciones hechas con IA en el examen; esto es
para estudiar.

## Instalación en la MacBook (una sola vez, con internet)

1. Instalar Ollama: descargar la app de <https://ollama.com/download> (o `brew install ollama`).
2. Descargar el modelo (unos 5 GB):

   ```bash
   ollama pull qwen3:8b
   ```

3. Las dependencias de Python son las mismas de siempre (`pip install -r requirements.txt`). El asistente usa
   solo la biblioteca estándar para hablar con Ollama.

Listo: a partir de acá funciona **sin internet**. Para verificarlo, desactivá el Wi-Fi y probá la página
*Asistente IA*.

### Qué modelo usar

| Modelo | Memoria | En una MacBook Air M4 de 16 GB |
|---|---|---|
| `qwen3:8b` (recomendado) | ~5 GB | Fluido (~20-30 palabras/s). Buen español y buena salida JSON. |
| `qwen3:14b` | ~9 GB | Entra, pero es más o menos la mitad de rápido. Mejor en enunciados enredados. |
| `qwen3:4b` | ~2,5 GB | Rápido, para máquinas con poca memoria. Se equivoca más. |

La app usa el modelo de `ASISTENTE_MODELO` (la barra lateral solo muestra si está listo). Para probar otro:
`export ASISTENTE_MODELO=qwen3:14b` antes de `streamlit run app.py`, y medilo antes con
`python herramientas/evaluar_examenes.py --ia --modelo qwen3:14b`.

Sin modo razonamiento: se sacó de la pantalla porque tardaba minutos por pedido y no mejoró los resultados
(medido en octubre con qwen3:8b y qwen3:14b).

### Variables de entorno (opcionales)

- `OLLAMA_HOST`: dónde corre Ollama (por defecto `http://localhost:11434`).
- `ASISTENTE_MODELO`: modelo por defecto (`qwen3:8b`).
- `ASISTENTE_NUM_CTX`: contexto en tokens que se le pide al modelo (16384; el prompt de interpretación usa ~4000 y el de redacción de los temas del 2° parcial, hasta ~10.000 más la respuesta).
- `ASISTENTE_FACTOR_CLASE`: cuánto se prefieren los ejercicios resueltos por el profesor en clase (`datos/clase_resueltos.json`) como ejemplos de la IA (1,25; 1 = como cualquier ejercicio de la guía). Medido el 11/11: con 1,25 el consenso queda igual en los exámenes reales (33/35) y Q1 a/b pasan de una lectura a consenso; con 1,6 la IA sola empeora en los exámenes (29 → 24/35).
- `OLLAMA_NUM_PARALLEL` (de Ollama, no de la app): cuántas consultas atiende a la vez. El consenso pide las dos lecturas de IA juntas, así que con 2 o más tarda la mitad. En la PC con Windows (RX 9070 XT, 16 GB) quedó en 3 como variable de usuario: 3 consultas tardan lo mismo que 1 (~98 tokens/s, 100 % GPU). Se aplica al reiniciar Ollama.

### Afinar los prompts sin sesgar (`herramientas/optimizar_prompts.py`)

Se afina SOLO con la guía (cada ejercicio excluido de sus ejemplos) y se valida al final con exámenes reales + enunciados raros, que no se miran para afinar. Solo cambios genéricos; la base se corre dos veces para medir el ruido. 11/11: se sacó la persona («Sos un asistente… cátedra Dopazo») de los dos prompts (igual o mejor en guía y validación). Sacar las claves por tema mejoraba la guía pero empeoraba la validación (−4): descartado por sobreajuste. 1 o 3 ejemplos: peor o mixto (quedan 2). Con el cambio: consenso 34/35 en exámenes, 54/56 en el banco de clase, 0 consensos equivocados.

### Ejercicios de clase (prueba a ciegas)

`python -X utf8 herramientas/evaluar_clase.py [--reglas] [--hilos 3] [--solo V-8 IV-4]` corre el consenso sobre los 24 ejercicios que resolvió el profesor (`datos/clase_resueltos.json`) sin darle a la IA ese mismo ejercicio como ejemplo, y compara número y decisión con el pizarrón; el informe (H0 de la app al lado del planteo del profesor) queda en `herramientas/tmp/evaluar_clase.md`. Las reglas se ajustaron con la guía, así que ahí no son ciegas: lo que mide algo nuevo es la IA. 11/11: app 52/56 sin priorizar los de clase y 54/56 con 1,25 (IA con ejemplos 44/56, IA por tema 37/56, ningún consenso equivocado). En la página 5, «👨‍🏫 Parecidos resueltos por el profesor en clase» muestra los dos más parecidos del mismo tema con su planteo.

## Antes del examen

0. **Medí el consenso con exámenes reales** (`datos/examenes_reales.json`, con la referencia de cada inciso):

   ```bash
   python herramientas/evaluar_examenes.py        # solo reglas, instantáneo
   python herramientas/evaluar_examenes.py --ia   # consenso (Ollama abierto)
   ```

   Un examen nuevo se agrega al banco y se mide **antes** de corregir nada (prueba a ciegas).
1. **Medí el modelo contra la guía** (con Ollama abierto):

   ```bash
   python herramientas/evaluar_guia.py --ia --limite 30           # la IA sola, sin reglas
   python herramientas/evaluar_guia.py --ia-hibrido I II III      # reglas + IA que completa
   python herramientas/evaluar_guia.py --revision                 # solver + revisión IA (falsas alarmas)
   python herramientas/evaluar_guia.py --ia --modelo qwen3:14b    # comparar modelos
   ```

   `--ia` mide cuánto entiende el modelo por sí mismo. En la guía, las reglas solas resuelven el 100 %, así
   que `--ia-hibrido` debería quedar igual. Lo que importa ahí son las «sugerencias»: diferencias con las
   reglas, que en la guía son falsas alarmas. El ejercicio evaluado se saca de los ejemplos que ve el modelo.
2. Con la batería cargada, probá unos cuantos ejercicios para ver cuánto tarda y cuánta batería gasta.
3. Unos minutos antes, abrí la página *Asistente IA* y hacé una pregunta cualquiera para que el modelo quede
   cargado en memoria (queda 30 minutos; si no, la primera respuesta tarda unos segundos más).

## Cómo está hecho

```
asistente/
  cliente.py      API local de Ollama (urllib): chat, streaming, salida JSON con esquema, modo razonamiento
  esquema.py      JSON Schema del planteo (mismas claves que interprete/modelo.py) y su validación
  interpretar.py  híbrido reglas + IA (con ejercicios parecidos de la guía como ejemplos)
  simple.py       IA que razona el planteo en palabras y después lo traduce a campos (ya no se usa en la app)
  por_tema.py     IA con un prompt corto por tema (clasifica el tema y después pide el JSON de ese tema)
  consenso.py     vota reglas + IA con ejemplos + IA por tema, por inciso
  revisar.py      solver + revisión: lectura a ciegas, arbitraje con cita, hipótesis en palabras
  numeros.py      números del enunciado que el planteo no usa (sin IA)
  contexto.py     búsqueda TF-IDF en los apuntes .md
  explicar.py     explicaciones / chat y control de números sin respaldo
  tareas.py       consultas en segundo plano (un hilo por consulta): siguen aunque cambies de página
  ui.py           barra lateral de Streamlit (estado de Ollama y modelo) y seguimiento de tareas
```

- **Seguir trabajando en otra página**: interpretar con IA, rehacer el planteo, redactar, explicar y el chat corren
  en un hilo aparte que deja lo que va generando en la sesión. Si te vas a otra página la consulta sigue; la barra
  lateral avisa cuándo termina y al volver ves lo que lleva o el resultado. Recargar el navegador (F5) sí empieza
  una sesión nueva y se pierde todo, como antes.

- **JSON libre, validado después**: se le pide a Ollama JSON (`format: "json"`), pero **no** el JSON Schema:
  con un esquema, Ollama obliga a escribir las claves en el orden del esquema, y el modelo, que las escribe en
  el orden del enunciado, salteaba `xbar` o `mu0` y usaba la siguiente clave parecida (`xbar1`, `sigma_pob1`).
  El prompt lista qué claves van con cada tema, y `esquema.desde_dict` descarta claves desconocidas, traduce o
  descarta las de otro tema, hereda α (y la cola, μ₁…) entre incisos como las reglas, convierte tipos, pasa
  porcentajes a fracción (α = 5 → 0,05) y rechaza valores imposibles.
- **Ejemplos reales**: a cada pedido se le agregan los 2 ejercicios de la guía más parecidos, con el JSON que
  arman las reglas (verificado contra la guía). Así el modelo aprende el formato y las convenciones.
- **Tema forzado**: si la IA identifica otro tema, se vuelven a correr las reglas con ese tema
  (`analizar(..., tema=...)`), y queda el análisis que resuelve más incisos.
- Los tests (`tests/test_asistente.py`) reemplazan el modelo por respuestas fijas: no hace falta Ollama.
