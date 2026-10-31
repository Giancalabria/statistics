# Informe clases 1 a 6 (06/08 a 10/09/2026): Estadística Aplicada, Ing. Dopazo

**Fuentes.** Transcripciones automáticas de las 6 clases: 06/08, 13/08, 20/08, 27/08, 03/09 y 10/09. Las citas son textuales y conservan los errores de reconocimiento.

**Notas detalladas por clase.** Están en `notas_clase_MMDD.md`, en la carpeta scratchpad, por ejemplo `/private/tmp/claude-502/-Users-gianluca-calabria-Software-Personal/4913a8ed-bf17-49fe-a2b2-ff2d2681be6b/scratchpad/notas_clase_0910.md`.

**Marcas.** **[2P]** indica lo que aplica al 2° parcial: ensayos de hipótesis y reglas transversales. Lo que es solo de estimación (1° parcial, ya rendido) va resumido.

---

## 1. Resumen por clase

| Fecha | Temas (apunte) | Ejercicios de la guía |
|---|---|---|
| 06/08 | Presentación, logística, herramientas. Repaso de modelos (Est. I). Cap. 1, intro: población, individuo, muestra, parámetro vs estimador, idea de IC. | Ninguno |
| 13/08 | Cap. 1: estimación de μ con σ conocido (Z) y desconocido (t). Insesgado/"potente", TCL, crítica a "n ≥ 30". n por fórmula y método iterativo. | **I-1** resuelto. **I-6** de tarea. |
| 20/08 | Cierre de μ con t: n iterativo, población finita (factor de corrección, n corregido), total poblacional. **[2P] Inicio del Cap. 2:** filosofía del ensayo, H0/H1, errores I/II, cuadro decisional, criterio pesimista/optimista, pasos, valor crítico, CR/RD, prohibición del p-value. | **I-7** resuelto (más un b) agregado). **I-34** mencionado. Tarea: plantear en palabras las H0 de todos los problemas. |
| 27/08 | **[2P]** Cap. 2: ensayos de μ con σ conocido. Casos I (≤), II (≥) y III (=). β, potencia, curvas OC y de potencia, n por dos condiciones. | **I-10** resuelto a)-c). **I-8** planteado. Tarea: todos los de σ conocido. |
| 03/09 | **[2P]** μ con σ desconocido (t, sin β ni n). Población finita en ensayos. Cap. 1: IC de σ²/σ y ecuación de García (estimación). **[2P]** Cap. 2: ensayo de σ² casos 1 y 2, β y n por García. | **I-26**, **I-33** y **II-6** resueltos. |
| 10/09 | **[2P]** Cierre del Cap. 2: ensayos de σ²/σ ("doy por finalizado todo el tema dos"). Cap. 1: estimación de p (exacto, F, criterios de aproximación, Mermoz, n). Adelanta que en p "no existe caso bilateral". | **II-8** y **II-12** resueltos. Tarea: "del tema tres todos los ejercicios de estimación". |

---

## 2. Logística

### Horario y asistencia
- Clase de 18:45 a 22:15. Es puntual: "Yo empiezo 1845 en punto".
- Asistencia mínima del 75%, tomada por QR.
- Consultas antes de clase, de 18:00 a 18:45. El 10/09 dijo "tienen eh 45 minutos para hacer preguntas".
- **[2P]** Las dudas se preguntan antes del examen, no durante: "Pregunten antes que examen" (03/09).

### Fechas
- **Las fechas de parciales no se dicen en voz alta.** El 06/08 dijo "ahí tienen la fecha de los del primero y segundo parcial": estaban en una diapositiva y están en el cronograma del campus/Teams. **Hay que buscarlas en el campus.**
- Después del 2° parcial queda "una clase más".
- Final regular: "el 17, el 12", probablemente el **17/12**, a las 18:45. No está confirmado.
- **10/09:** al profesor lo operan el 18/09. La clase pasa al **sábado 19/09** con un reemplazo y será "repaso para el tercero" (transcripción confusa). Un alumno pregunta "¿Hasta el parcial TP2?" y la respuesta es "Dos clases". El sábado complementario 19/09 (8:30 a 12:30) ya estaba anunciado el 06/08 y en él se toma asistencia.

### Régimen
- "El final es obligatorio. La materia no es promocionable."
- "Se puede recuperar un solo parcial." El recuperatorio cae en la misma fecha que el final anticipado.
- El final anticipado es solo para quienes aprobaron los dos parciales, y "se rinde toda la materia".

### Qué entra en cada parcial **[2P]**
- "vemos lo que tomamos en función de hasta dónde llegamos, pero al final todo."
- Según las clases, el 2° parcial cubriría como mínimo:
  - el Cap. 2 completo de μ y σ²;
  - ensayos sobre p (Tema III), que adelantó y empezaría después del 10/09.
- Lo que entra realmente se confirma con las clases 7 en adelante y el cronograma.

### Formato **[2P]**
- **Problemas, no ejercicios mecánicos.** La guía está desordenada a propósito: "en un examen yo te puedo preguntar cualquier cosa... tenés que saber cuándo me pid[e] una estimación y si... sigma conocido o sigma desconocido" (13/08).
- **Toma problemas ya resueltos de la guía y del apunte**: "He tomado en los exámenes los problemas que están resueltos y me he encontrado que nadie los resuelve" (06/08).
- **Toma los tips que da en clase**: "tips que uno da en clase que suelo tomar en los exámenes" (06/08).
- **Califica la interpretación, no los números**: "Si falta alguno de esos elementos, considero que el problema está mal hecho, aunque los números estén bien" (13/08).
- **Muestra las iteraciones**: "no me pongan el resultado ... le voy a poner una llamada diciendo de dónde lo saco, de la galera" (20/08).
- **Copia**: si dos alumnos arrancan la iteración con el mismo n, lo toma como copia (20/08).

### Herramientas **[2P]**
- **Apuntes permitidos ("libro abierto")**: "tienen machete oficial, yo les permito usar los apuntes" (03/09). Lo que no está en el apunte es "cómo plantear la hipótesis".
- **No inventar ecuaciones**: usar las del apunte (03/09).
- **CONTRADICCIÓN sobre la computadora:**
  - 06/08: "Puede traer ... la notebook, ... su celular", con wifi apagado y celular en modo avión. También: "pueden usar notebook, tablet, lo que ustedes quieran".
  - 10/09: "**en los exámenes no se puede usar computador**". Lo presenta como regla de la institución, que él critica.
  - Vale lo más reciente: **asumir sin computadora** (solo calculadora, aplicativo del celular en modo avión y apuntes). Conviene confirmarlo.
- **Aplicativo "Probability Distributions" (Matthew Bognar)**, en el celular:
  - Es la herramienta oficial; no se usan tablas.
  - "aprendan a usar el aplicativo. No me vengan el día del examen a decir y dónde" (20/08).
  - Da la acumulada izquierda y la derecha. Se ingresa la probabilidad acumulada izquierda.
  - Tiene Z, t, χ² y F.
- **Calculadora con funciones estadísticas**, obligatoria para x̄ y S, también con datos agrupados (centro de clase y frecuencia). Calcular a mano es "Siglo XX".
- **Software DOS del profesor** (DIS, GRAPHDIS, INDIS, con DOSBox, subido a Teams): calcula la binomial y la invierte. Primero dijo "yo lo obligo a que lo usen" y después "yo no obligo". En el examen sería inviable si no hay computadora.
- Excel, R y Python sirven para estudiar. Excel solo da la acumulada izquierda y no procesa datos agrupados.
- **Prohibido usar IA: "Al primero que veo resolviendo los problemas con la IA le pongo cero"** (06/08). Avisa que la IA resuelve mal el cálculo de n (ver §3.6).
- **No acepta resoluciones de otros profesores**: "la posta te la doy yo porque soy yo el que te pone la nota" (06/08).

---

## 3. Reglas del profesor (todas **[2P]** salvo que se indique)

### 3.1 Planteo de H0/H1

- **Regla madre: H0 se plantea para que el error tipo I sea el más grave.** "la hipótesis nula se plantea de manera ... que el error del tipo uno sea más grave que el error de tipo [dos]" (20/08 y 27/08). El motivo es que α es el error que se cuantifica arbitrariamente.
- **Orden para decidir:** "Primero criterio, si no el criterio, errores. Y si no es errores, ¿qué es lo que quiero provocar?" (10/09, que remite al apunte).
  - **Pesimista**: cuando hay "riesgo económico inminente", es decir inversión, comprar una máquina, proveedor nuevo o barato, producto nuevo o modificación. H0 es "no funciona / no cumple" y se formula en extremo: "no reduce el consumo, sino que lo empeora" (27/08, I-10).
  - **Optimista**: control de recepción de un proveedor habitual, controles rutinarios y control de proceso. H0 es "cumple la especificación": "si soy pesimista lo estoy parando siempre" (20/08).
  - **Excepción**: "si no hay riesgo económico, más que sea una inversión, No voy a ser pesimista". Si la inversión busca abaratar costos, el criterio puede ser optimista (apunte).
  - "no se debe ser siempre optimista o ... siempre pesimista. Uno tiene que saber discernir."
- **Si el enunciado dice qué se quiere probar, eso va en H1 y no hace falta pensar el criterio.** "como me dicen qué es lo que quiero probar ... pruebo lo que usted me está pidiendo" (03/09). Ejemplos:
  - "¿hay razón para creer que μ > 10,25?" se plantea como H0: μ ≤ 10,25 (I-33).
  - "no es aceptable una varianza mayor de 0,09" se plantea como H0: σ² ≤ 0,09 (II-8).
- **No asociar el criterio con la forma matemática.** "No asocien estos casos a los criterios": I-10 es pesimista con H0: μ ≥ 11,2 e I-8 es optimista con H0: μ ≥ 250 (27/08).
- **Primero en palabras, después en matemática.** "Primero piensa el problema, escríbalo en palabras y después traduzca" (27/08); "no me planteen hipótesis numéricamente" (20/08).
- **La igualdad va siempre en H0.** Hay solo tres formas (≤, ≥, =): "No existe un cuarto caso".
- **H1 es el complemento.** "nunca se debe poner la hipótesis alternativa, pero mientras nosotros estamos aprendiendo, lo vamos a poner." Conviene escribirla.
- **Bilateral solo cuando el enunciado lo impone** ("diferente de", valor exacto, "tan grave que sea menor como mayor"). "Siempre los ensayos bilaterales no tienen criterio" (03/09).
  - Preferir siempre el unilateral: "Siempre que usted pueda plantear una hipótesis unilateral, plantéela".
  - Si en un bilateral el error tipo II es más grave, hay que agrandar α ("esto no lo dice ningún libro").
- **σ², σ y p solo tienen ensayos unilaterales.** "jamás van a encontrar un ensayo de hipótesis bilateral para la varianza" (03/09); "No existe caso bilateral en P" (10/09).
- **Especificación** es lo que se desea: "5 g máx" se plantea como H0: σ ≤ 5 (control, optimista).
- **Los supuestos y las hipótesis se hacen sobre parámetros, nunca sobre la muestra.** "Las muestras se [observan], no se supone" (03/09).
- **La decisión contundente sale de rechazar H0.** "las decisiones contundentes se obtienen cuando rechazo la hipótesis" (27/08). Con H0 "lote bueno" se sabe cómo actuar; con H0 "lote malo", si no se rechaza "no tenemos la menor idea" (20/08).

### 3.2 Pasos del ensayo (orden exigido, "están escritos en el apunte")

1. **Definir la variable** con su unidad y condiciones: "consumo de combustible", no "litros de cualquier cosa" (27/08). "Si no define la variable de estudio no sabe cómo sacar la muestra" (13/08).
2. **H0 (y H1)**, con el criterio justificado en palabras.
3. **α.** Se busca en el enunciado o en las preguntas. Si no está, lo fija el alumno: "no me preguntes en un examen. Falta alfa. No falta ... lo pones [vos]" (20/08). Escala: chico ≤ 1%, estándar 5%, grande ≥ 10%. **Una vez fijado, "alfa no se toca"**, salvo que el enunciado lo pida.
4. **n.** Si no lo dan, se calcula con μ1 y β (o 1−β).
5. **Valor crítico, CR y RD**, antes de ver la muestra.
6. **Experimento y conclusión.**

**Las 4 probabilidades.** Escribirlas siempre en términos del problema: "se manejan cuatro probabilidades... Y uno las tiene que escribir... en términos del problema" (27/08). Ejemplo I-10: α = P(lanzar el aditivo | μ ≥ 11,2); 1−α; β = P(no lanzar | μ < 11,2); 1−β.

**Prohibido decidir con p-value o fijar α después.** "Nunca el alfa se pone después del ensayo"; "es sospechoso de que sea tendencioso" (20/08). El apunte presenta el planteo pivotal y el a posteriori solo como informativos.

### 3.3 Lectura del enunciado ("cuando dice X, significa Y")

| Frase del enunciado | Significado |
|---|---|
| "nivel de confianza 95%" | 1−α = 0,95 |
| "riesgo de lanzar el producto **cuando no produce el efecto**" | α |
| "riesgo de lanzar / revisar **cuando cumple el objetivo** (μ = μ1)" | 1−β |
| "probabilidad máxima de rechazar una partida que cumple" | α |
| "detener el proceso **indebidamente**" / "revisar equivocadamente" | α |
| "probabilidad de **detectar** que θ = θ1" / "de revisar si μ = μ1" | 1−β (potencia) |
| "probabilidad de **no detectar** / no revisar si θ = θ1" | β |
| "con el producto se tiene una media de 10,5" | alternativa μ1 (sobre el parámetro) |
| desvío dado "de la variable" / histórico / de experimentos sucesivos | σ poblacional, se usa Z |
| varianza o desvío "que sale de la muestra" | S, se usa t |
| "nivel promedio" / "promedio" en la pregunta | μ poblacional |
| "Parece razonable asumir que el desvío no se modificará" | recién ahí σ es conocido; "lean todo el problema completo" |
| "¿cuántas X **más**?" | n_total − n_inicial |
| "diferente de" | bilateral |

- **α no se calcula.** "Nadie te va a pedir que vos calcules alfa": si piden una probabilidad, en general es β o 1−β (27/08).
- **Truco**: "Siga leyendo". Si la frase es ambigua entre α y 1−β, se decide por la condición sobre μ que la acompaña.

### 3.4 Distribuciones y modelos

**z vs t**
- σ conocido se usa con Z.
- σ desconocido se usa con **t, ν = n−1, siempre, sin importar n**. "jamás se debe usar [la normal], aunque sea infinito" (20/08). Usar Z con S lleva a "recursa".
- **La regla "n ≥ 30" está prohibida** ("libros muy viejos").
- Normalidad de x̄: un indicio práctico es CV(x̄) = (σ/√n)/μ ≤ 0,20 (13/08).

**Normal**
- Solo para variables medibles.

**σ desconocido en ensayos de μ**
- **No se calculan β ni n** porque requieren la t no central: "No van a calcular ustedes beta cuando desconocen [sigma]"; "Tampoco vamos a calcular tamaño de muestra" (03/09).

**Población finita**
- Si se conoce N, hay que usar las ecuaciones de población finita: "No cometan papelones".
- Factor √((N−n)/N), igual que el apunte: "Algunos autores ponen sobre N − 1. El uno mucho no hace" (20/08; corregido el 29/10 releyendo la transcripción).
- n = N·n∞/(N + n∞).
- El factor se aplica también en x̄c, β y n de los ensayos (03/09).
- El 20/08 lo presentó como "Esto se lo regalo ... no es parte del programa", pero hay unos 12 problemas de ese tipo en la guía.

**Varianza: χ² siempre con varianzas**
- Si dan desvíos, se elevan al cuadrado: "Desvío por cuadrado" (10/09).
- **Caso 1** (H0: σ² ≤ σ0²):
  - S²c = σ0²·χ²(1−α; ν)/ν.
  - CR: S² > S²c.
  - β = F_χ²(ν·S²c/σ1²; ν), la acumulada izquierda.
- **Caso 2** (H0: σ² ≥ σ0²):
  - S²c = σ0²·χ²(α; ν)/ν.
  - CR: S² < S²c.
  - β = G (acumulada derecha) = 1 − F(...).
- **Si H0 es sobre σ**: Sc = √(S²c), pero β y n se trabajan con varianzas.
- **n por ecuación de García (ensayo)**: ν = (2/9)·(a + √(a²+1))², redondeando ν hacia arriba, y n = ν + 1.
  - Caso 1: R = σ1²/σ0² y a = [Z(1−α) + Z(1−β)·∛R] / [2(∛R − 1)].
  - Caso 2: R = σ0²/σ1² (siempre > 1) y a = [Z(1−β) + Z(1−α)·∛R] / [2(∛R − 1)].
  - **∛R multiplica solo a un Z**: "no me hagan esta suma y lo multiplican por la raíz cubica" (03/09).
  - R es **de varianzas**: "siempre se olvidan y me ponen el R prima".
- **n se calcula con α fijo**, nunca mirando solo β: "Cuando ustedes cambian la muestra el crítico va a cambiar" (10/09).

**p (Bernoulli)** (estimación resumida; lo marcado vale para ensayos de p)
- Bernoulli es siempre población infinita o proceso; si la población es finita es hipergeométrica. Muestreo siempre a la binomial; Pascal no se da.
- **IC de p con la normal está prohibido**: lo llama "aberración estadística" ("No me usen para estimar la normal").
- El intervalo es exacto (binomial o F).
- **Con r = 0, B se calcula con α entero, sin dividir por 2**: "todo el riesgo lo juntás en el límite superior" (10/09).
- **Criterios de aproximación, "los únicos valederos"** (solo para calcular n). **[2P]**: probablemente también para ensayos y planes de p.
  - Normal si n·p > 10 **y** n·(1−p) > 10.
  - Poisson si p ≤ 0,005.
  - Si se cumplen los dos o ninguno: **criterio de Mermoz**. Con p ≤ 0,5, n0 = 0,23·(1−p)²/p³; con p ≥ 0,5, n0 = 0,23·p²/(1−p)³. Si n > n0 se usa la normal; si no, Poisson.
  - "No me usen otro criterio porque está mal." Descarta "n > 30" y "n y p grandes".

### 3.5 CR, RD y conclusión

- **Nunca comparar x̄ (ni S²) con μ0 (o σ0²); siempre con el valor crítico.** "Nunca compare una variable aleatoria contra un parámetro" (27/08, 03/09, 10/09). El ejemplo de error que da: "10,6 es menor que 11,2, por lo tanto se reduce el consumo".
- **Los críticos y los límites de control se calculan con la curva de H0.** μ1 se usa solo para n y β.
- **CR**: es la condición matemática.
  - "Si x̄ < x̄c rechazo H0."
  - En el bilateral: "x̄ < x̄c1 **o** x̄ > x̄c2".
  - El límite es estricto: "8,99 no es casi 9".
- **RD**: es el curso de acción en lenguaje del problema, dirigido "al operario". Plantilla de I-10: "Se realiza una prueba de 10 corridas de igual recorrido; se mide el consumo de cada corrida; se calcula el promedio; si ese promedio es menor a 10,52 L se lanzará el producto al mercado; caso contrario no."
- **Conclusión**
  - Si se rechaza H0: "Puedo asegurar que el tiempo medio de armado es superior a 10,25 min."
  - Si no se rechaza: "No tengo pruebas para asegurar que…", "con esta muestra no se puede probar que el consumo medio se haya reducido", "No puedo asegurar que la varianza sea mayor a 0,09 mm²".
  - **Prohibido "acepto H0"** y no hay que decir que el producto es malo ("no pude probar").
  - La conclusión se refiere al parámetro poblacional.
- **La decisión es distinta del resultado del ensayo** (absuelto ≠ inocente).
- **Sin muestra**: se deja la CR planteada y "no puedo hacer nada" más (10/09).
- **Dibujar la campana**: "dibújenla porque ahí se van a enterar de todo".

### 3.6 β, potencia y n (μ con σ conocido)

**Fórmulas por caso**
- **Caso I** (H0: μ ≤ μ0):
  - x̄c = μ0 + Z(1−α)·σ/√n.
  - β = Φ((x̄c − μ1)/(σ/√n)).
- **Caso II** (H0: μ ≥ μ0):
  - x̄c = μ0 − Z(1−α)·σ/√n.
  - β = 1 − Φ(...).
- **Caso III** (H0: μ = μ0):
  - x̄c1,2 = μ0 ∓ Z(1−α/2)·σ/√n.
  - β = Φ(z2) − Φ(z1).
  - "la colita del otro lado no es β", es parte de 1−β.

**Tamaño de muestra**
- n = [(Z(1−α) + Z(1−β))·σ/(μ1−μ0)]². En el caso III se usa Z(1−α/2).

**Cálculo de β**
- β se calcula con el crítico **con todos sus decimales**: "En realidad no es 11,55 exacto, eh, sino que tiene varios decimales" (03/09).

**Curva OC**
- β en función de μ1.
- Con μ1 = μ0, β = 1−α. Con μ1 = x̄c, β = 0,5.

**Error que el profesor llama "aberración"**
- Calcular un nuevo n reutilizando el x̄c del n anterior. "El que me hace esto, olvídese de aprobar estadística aplicada"; "el x̄ crítico depende de n". Avisa que la IA lo hace así.
- Hay que usar la fórmula de las dos condiciones.

**β no es 1 − α.**

### 3.7 Redondeos y decimales

- **Calcular con todos los decimales, como mínimo 4, siempre la misma cantidad; "jamás con dos ... eso déjelo a los contadores"** (20/08).
- Los fractiles van con 4 decimales: "Dame los cuatro decimales".
- **Expresar** los resultados según la variable (por ejemplo, 2 decimales en g, L o min): "como expresan los resultados eso dependerá de la variable".
- **Redondeo estadístico**:
  - En los IC, el límite inferior hacia abajo y el superior hacia arriba: "esto es estadísticas, no es matemática".
  - Agrega que la guía a veces redondea mal: "aunque lo diga la [guía] y está mal".
- **n y ν siempre al entero superior**: 24,0001 → 25; 110,01 → 111; ν de García 538,4 → 539.
- **Probabilidades**:
  - Siempre entre 0 y 1, nunca en %: "el primero que me ponga 30 por de probabilidad. Olvídate de aprobar".
  - Se admite "90% de confianza/seguridad", pero no "nivel de confianza 90%".
- **Unidades** en límites, críticos, n ("11 piezas") y varianzas (mm², g²).

### 3.8 Notación exigida

- **Parámetros con letras griegas** (μ, σ, σ², λ); p es la excepción. **Estimadores con latinas** (x̄, S, S², p̂, L).
- **P = probabilidad puntual. F = acumulada izquierda. G = acumulada derecha. Φ = F de la normal estándar.**
  - "Escribir P(X ≤ x) en lugar de F es un error conceptual estadístico" (10/09).
  - "No me pregunten más qué es Φ."
- **Grados de libertad**: escribir "ν = número de grados de libertad", no "n−1".
- **S²** se calcula con n−1.

### 3.9 Método iterativo para n con t (estimación; vale la forma de presentar)

- Empezar con un n **bastante mayor que el original**, nunca igual ni menor.
- Iterar hasta que el n de entrada = n de salida. "Si usted necesita más de tres iteraciones, dude."
- Mostrar todas las iteraciones.
- Para bajar el error se sube n; "nunca se toca el riesgo".

---

## 4. Ejercicios resueltos en clase (casos de prueba)

### [2P] I-10, aditivo, consumo de combustible (27/08)

**Datos.** μ0 = 11,2 L; σ = 1,3 L (no cambia); α = 0,05 ("riesgo de lanzar cuando no produce el efecto"); n = 10 corridas; x̄ = 10,6 L.

**Planteo.** Criterio pesimista: H0: μ ≥ 11,2 L (el aditivo no reduce el consumo, o lo empeora); H1: μ < 11,2.

**Resultados.**
- x̄c = 11,2 − 1,6449·1,3/√10 = 10,5238, informado como **10,52 L**.
- CR: x̄ < 10,52.
- **a)** 10,6 no es menor que 10,52, así que no se rechaza H0. **No es concluyente**: "con esta muestra no se puede probar que el consumo medio se haya reducido".
- **b)** Con μ1 = 10,5: z = 0,0579, **1−β = 0,5231** (β = 0,4769).
- **c)** Para 1−β = 0,90: n = [(1,6449 + 1,2816)·1,3/0,7]² = 29,54, o sea **n = 30** (20 más).

### [2P] I-8, ovillos, control de recepción (27/08)

**Datos.** μ0 = 250 g (mínimo); σ = 15 g (histórico); n = 10; α = 0,05 ("probabilidad máxima de rechazar una partida que cumple").

**Planteo.** Criterio optimista (proveedor habitual): H0: μ ≥ 250 g.

**Resultados.**
- x̄c = 250 − 1,6449·15/√10 = **242,19 g**.
- CR: x̄ < 242,19.
- RD: si el peso promedio de 10 ovillos es menor que 242,19 g, se rechaza la partida.

### [2P] I-26, dimensión crítica, bilateral (03/09)

**Datos.** μ0 = 11,5 cm; σ = 0,1 cm; α = 0,10 ("revisar equivocadamente"); β = 0,05 con μ1 = 11,4.

**Planteo.** H0: μ = 11,5.

**Resultados.**
- **a)** n = [(1,6449 + 1,6449)·0,1/0,1]² = 10,82, o sea **n = 11 piezas**.
- **b)** Límites de control **11,45 y 11,55 cm**. CR: x̄ < 11,45 o x̄ > 11,55. RD: parar el proceso y revisarlo.
- **c)** Con μ = 11,46: β = Φ(2,9716) − Φ(−0,3183) = 0,6234, así que **1−β = 0,3766**.

### [2P] I-33, tiempos de armado, datos agrupados (03/09)

**Datos.** Datos agrupados:

| Clase (min) | Frecuencia |
|---|---|
| 9,5–9,8 | 4 |
| 9,8–10,1 | 10 |
| 10,1–10,4 | 35 |
| 10,4–10,7 | 12 |
| 10,7–11,0 | 8 |
| 11,0–11,3 | 6 |

n = 75, x̄ = 10,362 min, S ≈ 0,37 min.

**Planteo.** H0: μ ≤ 10,25; α = 0,05.

**Resultados.**
- **a)** Con σ = 0,65: x̄c = **10,37**. No se rechaza H0: "No tengo pruebas para asegurar que…".
- **b)** Con S: x̄c = 10,25 + t(0,95; 74)·S/√75 = **10,32**. Se rechaza H0: "Puedo asegurar que…".
- Muestra que una misma muestra puede llevar a conclusiones distintas según la información disponible.

### [2P] II-8, láminas de plástico (10/09)

**Datos.** 12 espesores (mm): 12,6; 11,9; 12,3; 12,8; 11,8; 11,7; 12,4; 12,1; 12,3; 12,0; 12,5; 12,9. De ahí x̄ = 12,275 y S² = 0,14932 mm², con ν = 11.

**Resultados.**
- **a)** (estimación) P(0,0834 ≤ σ² ≤ 0,3591) = 0,90.
- **b)** H0: σ² ≤ 0,09 mm² (sale de la pregunta); α = 0,05.
  - S²c = 0,09·19,6751/11 = **0,16098 mm²**.
  - Como 0,1493 ≤ 0,161, no se rechaza H0: "No puedo asegurar que la varianza sea mayor a 0,09 mm²".
- **c)** Con σ1² = 0,11: β = F_χ²(16,0978; 11) = 0,8627, así que **1−β ≈ 0,1373/0,1375** (la guía da 0,1375).
- **d)** Para 1−β = 0,95: R = 1,2222, a ≈ 24,60, ν = 538,4 → 539, **n = 540, es decir 528 más**.

### [2P] II-12, suelas de goma (10/09)

**Datos y planteo.** H0: σ ≤ 5 g (control, optimista); α = 0,05 ("detener indebidamente"); n = 10, ν = 9.

**Resultados.**
- **a)** S²c = 25·16,919/9 = 47,0, así que **Sc = 6,86 g**. CR: S > 6,86 g. No hay muestra, así que no se decide.
- **b)** Con σ = 8: β = F_χ²(9·6,86²/64 = 6,618; 9) = **0,3222**.
- **c)** Para β = 0,05: R = 2,56, a = 5,2925, ν = 25,34 → 26, **n = 27, es decir 17 más**.

### Estimación (1° parcial; solo valores de control)

- **I-1**: e = 7,8024; P(238,19 ≤ μ ≤ 253,81) = 0,90; n = 24,35 → 25, **15 más**.
- **I-7**:
  - t(0,975; 24) = 2,0639; e = 8,8135; P(205,18 ≤ μ ≤ 222,82) = 0,95.
  - b) agregado por el profesor, con e = 4: iteración 501 → 111 → 112 → 112, **87 más**.
- **II-6**: P(11,40 g ≤ σ ≤ 21,91 g) = 0,95; con R' = 1,5 (R = 2,25), ν ≈ 48, **n = 49**.
- **Ejemplo de p con n = 30, r = 3, 95%**: exacto A = 0,0211, B = 0,2653. La normal da [−0,0092; 0,2092], un límite negativo.
- **Ejemplo de p con n = 400, r = 40**: exacto 7,24% a 13,367%; la normal da 7,06% a 12,94%.

---

## 5. Contraste con el repo

Documentos comparados: ESTILO_CATEDRA.md, CONVENCIONES_CATEDRA.md, esquema_teorico_examen_estadistica.md ("esquema"), Guía Definitiva…md ("GD"), con una mirada rápida al solver.

### Severidad ALTA

1. **IC de p por aproximación normal.**
   - El esquema §1.3 la presenta como método, con la condición n·p̂ ≥ 5, y el solver tiene `ic_proporcion_normal` con aviso en np ≥ 5.
   - El profesor dice: "aberración estadística ... No me usen para estimar la normal". Se usa siempre el exacto.
   - **Corrección**: no ofrecer la normal como resultado para el IC de p, o marcarla como "solo comparación, NO usar en el examen".
2. **Criterio de aproximación de la binomial.**
   - El repo (esquema y solver) usa np ≥ 5 y n(1−p) ≥ 5.
   - El profesor usa **np > 10 y n(1−p) > 10; Poisson si p ≤ 0,005; si no queda claro, Mermoz** (n0 = 0,23(1−p)²/p³). "No me usen otro criterio porque está mal."
   - Mermoz no aparece en ningún .md del repo; habría que verificar si el solver lo tiene.
   - Afecta n de p y probablemente los ensayos y planes de p del 2° parcial.
3. **IC de p con r = 0.**
   - El repo (CONVENCIONES y `ic_proporcion_exacto`) sigue a la guía y usa α/2 (III-3b: 0,2589).
   - El profesor (10/09): "No se divide el alfa por 2 … todo el riesgo lo juntás en el límite superior". Con α entero da 0,2057.
   - Contradice a la guía; manda el profesor. **Mostrar como resultado principal el de α entero** y dejar el de la guía como nota. Es del 1° parcial, pero puede volver en el final.
4. **β y n en ensayos de μ con σ desconocido.**
   - El solver tiene `disenar_ensayo_media_sigma_desconocido` y `n_media_sigma_desconocido_para_potencia` (iterando con t central). Su propio docstring admite que no está validado.
   - El profesor: "No van a calcular ustedes beta cuando desconocen [sigma] ... Tampoco ... tamaño de muestra" (requiere t no central).
   - **Corrección**: no ofrecerlo, o advertir que la cátedra no lo pide. Si el enunciado lo pide, revisar si σ es en realidad conocido.
5. **Decidir con p-value o α a posteriori.**
   - El solver calcula `p_value`: en `interprete/resolver.py:912` muestra el "valor a posteriori α*" en la línea de **Decisión** de p, y two_samples también lo usa.
   - El profesor prohíbe decidir así: "Nunca el alfa se pone después del ensayo". La decisión tiene que salir de la CR con el valor crítico.
   - El p-value puede quedar solo como dato informativo, nunca en la decisión ni en la redacción.
6. **Ecuación de García mal transcripta en GD §4.**
   - GD dice ν = 9 + (a² + a·√(a²+18)) con a = Z(1−α)(R+1)√2/(3(R−1)).
   - La versión del profesor es ν = (2/9)(a + √(a²+1))², con a sobre ∛R. Hay dos variantes: estimación con a = Z(1−α/2)(∛R+1)/(2(∛R−1)), y ensayo con ∛R multiplicando un solo Z.
   - Si la IA usa GD, el número sale mal. **Corregir o eliminar ese bloque de GD.**
7. **Falta la versión de García para ensayos de varianza.**
   - ESTILO y el esquema solo muestran García para estimación (relación de límites).
   - Para ensayos, el solver (`n_varianza_para_potencia`) busca el n exacto con χ², no con García. Coincide en II-8 (540) y II-12 (27), pero el profesor redondea el **ν de García hacia arriba**, y en otros casos los dos métodos pueden diferir en ±1.
   - El profesor también exige mostrar a y ν. **Agregar García (casos 1 y 2) como método principal y el exacto como control.**
8. **La regla de "n ≥ 30" (TCL) que aparece en GD §4.**
   - GD dice "x̄ aproximadamente normal solo si n ≥ 30". El profesor dice que lo usan los "libros muy viejos", lo llama "mentira" y lo penaliza.
   - Con S se usa siempre t, sea cual sea n. El indicio es CV(x̄) ≤ 0,20.
9. **Contradicción de los 7 pasos en GD §3.**
   - GD pone "Estadístico de prueba" como paso 3 y no incluye ni la definición de la variable ni n.
   - El profesor exige: variable → H0 → α → n → crítico/CR/RD → muestra y conclusión. ESTILO §2 sí coincide.
   - Ojo: el ejemplo de conclusión de GD ("se procede al rechazo del lote y a la recalibración…") mezcla decisión con conclusión. Con todo, no es grave.
10. **Probabilidades en %.**
    - Ni ESTILO ni GD lo prohíben.
    - El profesor: "el primero que me ponga 30 por de probabilidad. Olvídate de aprobar".
    - **Agregar a ESTILO**: β, 1−β y α como número entre 0 y 1. Se puede decir "riesgo del 5 %" o "95 % de confianza", pero no "nivel de confianza 95 %" ni "probabilidad del 30 %".
11. **Cálculo de n con el x̄c viejo ("aberración").**
    - El repo no lo menciona.
    - Agregarlo como error prohibido en ESTILO y verificar que el solver siempre use la fórmula de dos condiciones.

### Severidad MEDIA

12. **Población finita: la fórmula del factor.**
    - El profesor y el apunte usan √((N−n)/N) ("algunos autores ponen sobre N − 1. El uno mucho no hace"); el esquema usaba N−1 (corregido).
    - CONVENCIONES usa (N−n)/N, que además reproduce I-34.
    - GD dice que se aplica solo si n/N > 0,20; el profesor dice "siempre que se conoce N" (CONVENCIONES coincide con él). **Eliminar el umbral de GD.**
13. **β calculado con el crítico redondeado a 4 decimales** (CONVENCIONES, para reproducir la guía).
    - El profesor dice que se calcula con el crítico con todos sus decimales.
    - Sugerencia: mostrar el β con el crítico exacto como resultado principal y el de la guía como control.
14. **Redondeo de valores críticos "hacia afuera"** (CONVENCIONES).
    - El profesor solo explicó el redondeo hacia afuera para límites de IC.
    - Para x̄c usó la expresión con 2 decimales (10,52; 242,19; 11,45/11,55; 10,37) sin explicar el criterio. Con x̄c = 10,5238 en cola izquierda, "hacia afuera" daría 10,52, así que coincide.
    - Mantener, pero la decisión siempre con el valor exacto. CONVENCIONES ya lo hace.
15. **Regla del repo "hipótesis a la luz de los datos → unilateral hacia la muestra".**
    - No tiene respaldo en estas clases.
    - El profesor usa otra regla: lo que pide probar el enunciado va a H1, y bilateral solo con "diferente".
    - Revisar que no choque: por ejemplo, si el enunciado pide "≠", no forzar un unilateral.
16. **Criterio pesimista/optimista en ESTILO §1.2.**
    - Está bien, pero faltan:
      - la regla madre (el tipo I tiene que ser el más grave);
      - el orden criterio → errores → qué se quiere probar;
      - "si el enunciado dice qué probar, eso va en H1";
      - la excepción "inversión para abaratar costos ⇒ puede ser optimista";
      - "no asociar el criterio con ≤/≥".
    - GD tiene **mal** el criterio optimista: dice "se asume la mejora o cumplimiento en H0 ... se acepta el cambio a menos que…". Para el profesor, el optimista es para controles y recepción de un proveedor habitual, no para aceptar cambios.
17. **Las 4 probabilidades en palabras.** ESTILO no lo exige; el profesor sí. Agregarlo al formato del ensayo.
18. **El esquema dice "Optimista: H0: μ = μ0"** para control de recepción. Para el profesor, la recepción es unilateral (I-8: H0: μ ≥ 250). El bilateral se usa solo cuando el enunciado lo pide.
19. **Notación F/G/Φ.** El repo no la define. Las salidas del solver tienen que usar F, G y Φ, y no P(X ≤ x).
20. **Unilateralidad de σ² y p.** El esquema §2.4 solo muestra el caso 1 de varianza. Agregar el caso 2 y la regla "nunca bilateral" para σ² y p. En p, el solver acepta bilateral (líneas 610-612 de `hypothesis_one.py`).
21. **Herramientas.** El repo no registra que el examen sería **sin computadora**, ni que el aplicativo oficial es Probability Distributions. El solver es una herramienta para estudiar, no para el examen.

### Severidad BAJA

22. El esquema dice "UTN / FIUBA": es UADE.
23. ESTILO usa "χ²" y "j²" correctamente. Para σ² en ensayos, el profesor también expresa Sc = √S²c cuando H0 es sobre σ (II-12). Verificar que el solver lo muestre.
24. Decimales: CONVENCIONES (2 en medias, 4 en p, etc.) es compatible con el profesor ("dependerá de la variable"). Agregar "cálculo intermedio con todos los decimales, mínimo 4" en la redacción.
25. "Nivel de confianza 95%" aparece en el esquema y en GD. Preferir "1−α = 0,95" o "95 % de confianza".
26. GD habla de "tipo de muestreo" (estratificado, etc.). El profesor: "todas las muestras que yo les voy a dar ... se supone que son muestras al azar".
27. ESTILO tiene bien la regla de nunca escribir "Acepto H0"; agregar que tampoco se dice que el producto "es malo".

---

## 6. Dudas y ambigüedades

- **Fechas del 2° parcial y del recuperatorio**: no se dicen en estas clases; están en la diapositiva y el cronograma del campus. El final regular probablemente es el 17/12.
- **"repaso para el tercero" / "¿Hasta el parcial TP2?" → "Dos clases"** (10/09): no queda claro si el 2° parcial es dos clases después del 19/09 ni qué incluye.
- **Computadora**: el 06/08 la permite (sin wifi); el 10/09 dice que "en los exámenes no se puede usar computador". Asumir que no se puede y confirmar.
- **H1**: "nunca se debe poner ... pero mientras estamos aprendiendo lo vamos a poner". No está claro si en el parcial la quiere; conviene escribirla.
- **r = 0 con n = 100**: el profesor dijo B ≈ "0,017 / 1,47%", pero el cálculo exacto con α entero da 0,0295 (con α/2, 0,0362). Seguramente es un error de transcripción. La regla (α entero) sí está clara.
- **"no siempre doy la ecuación de beta, nunca doy la ecuación de 1−β"** (27/08): no se sabe si se refiere al apunte, a un formulario o al examen.
- **El S de I-33** se oyó como "0 37", así que es aproximado.
- **En II-8 c)** el profesor dio "0,13757" y la guía 0,1375; el recálculo da 0,1373.
- **Poblaciones finitas**: el 20/08 dijo "no es parte del programa ... se lo regalo", pero la guía tiene unos 12 problemas de ese tipo e I-34 (población finita) le gusta ("ejemplo real"). La respuesta de la guía para I-34 a) tiene forma de p-value ("Si se toma un 6,39% o más de riesgo…"), lo que choca con la prohibición del p-value. No quedó claro cómo lo quiere en el examen.
- **Umbral de Poisson**: se oyó "0,005" y una vez "0,05"; el apunte dice 0,005.
- **Criterios de aproximación para ensayos de p**: los dio para el n de la estimación. Falta confirmar en las clases 7 en adelante si son los mismos para ensayos y planes de muestreo.
