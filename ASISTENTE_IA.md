# Asistente con IA local (sin internet)

La app usa un modelo de lenguaje que corre **en la propia computadora** con [Ollama](https://ollama.com).
Es opcional: si Ollama no está abierto, la app funciona exactamente igual que antes (solo reglas + solver).

## Qué hace y qué no

La IA **no hace cuentas**. Todos los números los sigue calculando `solver/`, que está verificado contra la guía.
El modelo se usa para lo que a las reglas les cuesta:

| Dónde | Qué hace la IA |
|---|---|
| **Interpretar un enunciado** → modo **⚖️ Reglas y IA por separado, y se comparan** (recomendado) | Dos lecturas independientes: las reglas resuelven al instante y la IA (`asistente/simple.py`) primero **razona el planteo en palabras**, sin formulario ni categorías, y después se traduce a los campos del solver con ejemplos de la guía. Se comparan los **resultados** de los dos por inciso: ✅ iguales, ❌ distintos, 🤖 solo la IA o 📐 solo las reglas. Si no coinciden ves los dos planteos y elegís con un botón, o le **escribís a la IA qué leyó mal** y rehace su planteo (`asistente/comparar.py`). En una prueba rápida, las reglas acertaron 17/17 en ejercicios normales y la IA 2/17; en trampas de redacción, la IA 8/16 y las reglas 3/16: se equivocan en lugares distintos. ~1-2 min. |
| **Interpretar un enunciado** → modo **🛡️ Solver + revisión IA** | Las reglas arman el planteo y el solver calcula; después la IA lo **audita**: (1) busca números del enunciado que el planteo no usa (sin IA), (2) lee el enunciado **a ciegas**, sin ver lo de las reglas, y compara campo por campo —la hipótesis se compara entera, en palabras—, y (3) donde no coinciden, un árbitro decide con las opciones en orden neutro y una **cita textual** del enunciado, que se verifica. Si el planteo de las reglas no se podía resolver, lo que la IA respalda con cita se aplica (🛠️); si ya se resolvía, **no lo pisa**: queda como sugerencia 💡 que aplicás con un clic (en la guía, aplicarlas solas rompía 35 de 536 valores). Lo dudoso queda ⚠️. ~30 s. |
| **Interpretar un enunciado** → modo **🧩 Solver, y la IA completa lo que no entiende** | Primero corren las reglas. Solo si fallan (tema no identificado, un inciso sin clasificar, datos que faltan) se consulta a la IA, y su propuesta se aplica **únicamente si hace que el solver resuelva más incisos sin romper ninguno**. No detecta un planteo equivocado que igual se pueda calcular: para eso está la revisión. |
| **Interpretar un enunciado** → modo **🤖 La IA arma el planteo** | La IA arma el planteo sola (sin las reglas) y el solver calcula. Sirve para comparar. |
| **Interpretar un enunciado** → modo **🔍 Solo solver** | Solo las reglas, sin IA. |
| **Interpretar un enunciado** → *💬 Explicar con IA* (después de Calcular) | Explica por qué se eligió cada camino y redacta la respuesta de examen con las convenciones de la cátedra, a partir de la resolución del solver. Marca con ⚠️ cualquier número que no salga del enunciado ni de la resolución. |
| **Asistente IA** (página 8) | **Chat libre**: dudas, revisar lo que escribiste, resolver ejercicios. Opciones: instrucciones editables (estilo *Libre*, *Responder con los apuntes* o *Personalizado*), buscar o no en los apuntes del repo, subir material propio (txt, md, csv, json, pdf) o pegar texto, e incluir el ejercicio de *Interpretar un enunciado*. Con **🧮 Resolver mi mensaje con la app**, el mensaje se toma como enunciado: lo interpretan las reglas (+ IA si hace falta), lo calcula el solver y la IA lo explica. Ese ejercicio queda en la conversación para seguir preguntando. Los números que no salen de la app ni del material se marcan con ⚠️. |

La IA **nunca hace las cuentas**: no hay un modo «solo IA» porque un modelo de 8B se equivoca en aritmética y el
solver está verificado dígito a dígito contra la guía. Para resolver charlando está la página *Asistente IA*.

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

El modelo se elige en la barra lateral (aparecen los que tengas descargados). Para cambiar el que viene
elegido por defecto: `export ASISTENTE_MODELO=qwen3:14b` antes de `streamlit run app.py`.

El interruptor **«Razonar antes de responder»** activa el modo razonamiento de Qwen3. Es más preciso, pero
puede tardar un minuto o más por pedido.

### Variables de entorno (opcionales)

- `OLLAMA_HOST`: dónde corre Ollama (por defecto `http://localhost:11434`).
- `ASISTENTE_MODELO`: modelo por defecto (`qwen3:8b`).
- `ASISTENTE_NUM_CTX`: contexto en tokens que se le pide al modelo (12288; el prompt de interpretación usa ~4000).

## Antes del examen

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
  revisar.py      solver + revisión: lectura a ciegas, arbitraje con cita, hipótesis en palabras
  numeros.py      números del enunciado que el planteo no usa (sin IA)
  contexto.py     búsqueda TF-IDF en los apuntes .md
  explicar.py     explicaciones / chat y control de números sin respaldo
  ui.py           barra lateral de Streamlit (estado de Ollama, modelo, razonamiento)
```

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
