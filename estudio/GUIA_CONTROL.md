# Guía de control del planteo

Para usar en el examen al lado de la app. Las **cuentas** del solver son confiables; lo que hay que controlar es el **planteo**. Cada error real de la app que aparezca en una práctica se agrega en la sección 3.

---

## 0. Flujo en el examen

**Antes de empezar (una vez):**
1. En la terminal, desde la carpeta del repo: `./levantar.sh`. Levanta Ollama, carga qwen3:8b, abre la app y evita que la Mac se suspenda. **No cerrar la tapa.**
2. Apagar el wifi y fijarse que la barra lateral diga «✅ Lista (qwen3:8b)».
3. Tener abiertas (o impresas) esta guía y `REGLAS_PROFESOR.md`.

**Por cada problema (~30 min):**

1. **Cargar (1 min).** Página *Interpretar un enunciado* (es la que abre la app).
   - Pegar el enunciado completo en «Planteo» y apretar **✂️ Separar incisos**. Revisar que cada inciso haya quedado en su campo.
   - Si hay tabla: **📋 Tabla de datos** → pegarla (encabezados en el primer renglón, una fila por renglón, separada con `|`, `;` o tab), o **Buscar la tabla en el planteo** si vino dentro del texto.
   - Apretar **🗳️ Interpretar** (~1 min).
2. **Planteo a ciegas mientras espera (2-3 min).** Sin mirar la pantalla, escribir en el papel: tema, parámetro, p₀/p₁ (o δ₀), α y β, H0/H1 y cola.
3. **Leer los votos** (sección 2 «Qué te piden» de la app):

   | Marca | Qué significa | Qué hacer |
   |---|---|---|
   | ✅ consenso | Dos o más lecturas llegaron al mismo resultado | Controlarlo igual (paso 4) |
   | ⚠️ las 2 IA contra las reglas | Las IA coinciden entre sí y las reglas dicen otra cosa | Abrir el desplegable, comparar las dos lecturas y elegir con «Usar la lectura de» |
   | ⚠️ sin consenso | Las tres lecturas dicen cosas distintas | Igual que el anterior |
   | ☝️ una sola lectura | Solo una pudo resolverlo | Controlar con más cuidado |

   Al elegir otra lectura, la resolución se recalcula sola.
4. **Controlar (5 min).** Comparar el planteo a ciegas con el de la app con la sección 1 de abajo. Si no coinciden, alguno de los dos está mal: releer el enunciado.
5. **Corregir si hace falta** y apretar **🧮 Recalcular con lo que corregí**:
   - Tema → «Tema detectado».
   - Criterio optimista/pesimista → «Criterio para plantear H0». Invierte H0: cambiarlo **antes** de tocar datos.
   - n, x̄, S, p₀… → sección 3 «Datos del planteo» («Agregar un dato que no detectó» si falta).
   - Tipo de pregunta, cola, α, δ₀ de un inciso → sección 4 «Cada inciso» («Agregar parámetros a este inciso» si falta).
6. **Escribir (15-20 min).** Los números se copian **solo del panel «Resolución»**: nunca del chat ni de una explicación de la IA (ver 3.4 bis). La redacción, con `REGLAS_PROFESOR.md`:
   - variable con unidad;
   - H0 justificada en palabras;
   - por qué Z, t o F;
   - α, CR y RD antes de ver la muestra;
   - estimador contra valor crítico;
   - conclusión en términos del problema;
   - 4 decimales, probabilidades entre 0 y 1, nunca «acepto H0».

   «📝 Redactar como en el examen» puede dar un texto de partida; si se usa, mirar el checklist que trae abajo.

**Si algo falla:**
- **La IA no responde:** **⚡ Solo reglas** (instantáneo) y controlar con más cuidado todavía.
- **El intérprete no entiende el problema:** páginas de «Resolver a mano, por tema». Se cargan los datos a mano y el solver calcula igual.
- **Duda conceptual** («¿por qué t y no Z?»): página *Asistente IA*, que ya tiene el ejercicio cargado. Sirve para entender, no para sacar números.

**Para decidir antes del 19/11:** el profesor dijo que pone cero si ve una resolución hecha con IA. Si eso incluye una IA local, se sigue el mismo flujo con **⚡ Solo reglas** y sin «Redactar». En ese caso el control del paso 4 importa todavía más: en exámenes que no habían visto, las reglas fallaron más que en el banco.

---

## 1. Control rápido de cada inciso (en este orden)

1. **Tema**: ¿es el test que pide el inciso? Leer la línea «tema» de la app. Un problema puede mezclar temas (comparación de medias + bondad de ajuste con la misma tabla).
2. **Parámetro**: ¿qué se estima o se ensaya? μ o σ; p de los que cumplen o de los que **no** cumplen; la diferencia en qué sentido (A − B o B − A); fija (δ₀) o porcentual (μA − 1,01·μB).
3. **H0 y cola**: ¿quedó en H1 lo que se quiere probar? ¿Criterio pesimista u optimista bien elegido? ¿La igualdad está en H0? ¿Nada bilateral en σ², p ni comparaciones?
4. **α (y β)**: ¿de dónde salió? Si el inciso no lo dice, la app puede haberlo **heredado de otro inciso**: hay que elegirlo y justificarlo (0,05 estándar). ¿Pide un solo límite («máximo», «mínimo»)? Entonces α entero, no α/2.
5. **Datos**: ¿tomó los números correctos? n, x̄, S, r, la columna correcta de la tabla, la tabla completa.
6. **Variable, unidad y acción** (sección 3 de la app, siempre visibles): escribir la variable en palabras («consumo de combustible de un auto en el recorrido»; en proporción, lo que se cuenta en plural: «piezas defectuosas»), revisar la unidad y la **acción si se rechaza H0** en infinitivo («lanzar el aditivo», «detener el proceso»). Con eso la app escribe α y β en términos del problema, la RD en lenguaje de planta y la conclusión con la variable y su unidad. La acción la detecta sola cuando el enunciado la dice («probabilidad de … de modificar el sistema»): controlar que tenga sentido.
7. **Conclusión**: ¿responde la pregunta en términos del problema? «Se rechaza: puedo asegurar que…» / «No se rechaza: no hay evidencia suficiente para asegurar que…». Nunca «acepto H0».

Si la app muestra **⚠️ sin consenso**, mirar las lecturas: la diferencia entre ellas suele señalar justo el punto dudoso. Que diga **✅ consenso** no garantiza que esté bien (ver 3.1).

Si muestra **⚠️ las 2 IA contra las reglas**, la app eligió lo de las IA, pero es una moneda al aire: las dos IA son el mismo modelo y suelen equivocarse juntas (en los enunciados trampa, 4 de cada 10 veces), aunque en exámenes nuevos a veces aciertan donde las reglas no (Q1). Comparar las dos lecturas con el control de arriba y elegir.

---

## 2. Por tema: cómo se reconoce y qué tiene que decir

### Proporción (Tema III)
- **Frases**: «porcentaje de», «proporción», «defectuosos», «x de las n unidades».
- **H0**: siempre unilateral. Control de proceso / proveedor habitual → optimista (H0: p ≤ p₀, cumple). Campaña, producto o proveedor nuevo → pesimista (H0: no funciona).
- **Decide** con r ≥ rc (o r ≤ rc), con α real ≤ α. Nunca con la normal.
- **IC de p**: siempre **exacto** (Beta / F). ¿Es de lo que se pide o de su complemento?
- **n con α y β**: exacto, o normal / Poisson **justificada con el n resultante** (n·p > 10 y n·q > 10; Poisson si p ≤ 0,005; si no, Mermoz).
- «Aumento de 3 puntos» = 0,12 → 0,15.

### Comparación de varianzas o desvíos (Tema IV)
- **Frases**: «variabilidad», «dispersión», «homogeneidad», «desvío» de dos grupos.
- ψ² = σA²/σB²; la muestra orienta (si SB > SA, solo se puede intentar probar σB > σA).
- Con desvíos, φ va al cuadrado. «Reducir el desvío un 12%» → H0: φ ≥ 0,88. En n para desvíos, R = R'².
- IC interpretado en %.

### Comparación de medias (Tema V)
- **Frases**: «promedio», «rendimiento», «performance» de dos grupos; «supera en X», «diferencia de más del X%».
- **¿Apareadas?** Solo si es el mismo individuo o la misma unidad experimental (no por n iguales).
- **Test F previo** (unilateral, α = 0,10) → amalgamado (S ponderada) o Welch (ν truncado).
- **Nunca bilateral**: la muestra orienta.
- **Porcentual**: δ* = μ₁ − h·μ₂ con h = 1,01, 1,10… ¿Quién va primero?
- «Diferencia máxima / mínima esperada» = **un** límite del IC, con α entero.

### χ² (Tema VI)
- **Frases**: «asociación» → independencia; «niveles / porcentajes de varios grupos» → consistencia; «se ajusta a / sigue la ley» → bondad de ajuste.
- E ≥ 5 (amalgamar), esperados con decimales, ν = clases efectivas − 1 − parámetros estimados.
- Completar el dominio con clases **nuevas** con O = 0 y probabilidad acumulada.
- No rechazar en continuas → «es un buen candidato». Mejor ajuste = menor χ².

### Regresión (Tema VII)
- **Frases**: «recta», «modelo lineal», «asociación lineal», «por cada unidad de X» (β₁, contribución marginal), «influencia porcentual» (r², coeficiente de determinación).
- ¿Cuál es Y (explicada) y cuál X (explicativa)?
- Promedio → IC de la media de Y; valor puntual → pronóstico (intervalo de predicción).
- «Máximo / mínimo por cada unidad» → un límite del IC de β₁.
- **Solo regresión simple entra en el parcial** (múltiple, para el final).
- ¿Validó el modelo antes de usarlo (aunque no lo pidan)? ¿Se valida para el uso del problema (técnico ⇒ r² ≥ 0,8)? Si no es válido, la pregunta no tiene sentido.
- ¿Están bien Y, X y sus **unidades** (campos «Y/X en palabras» y «Unidad»)? Las conclusiones las usan.
- «Promedio» / «toda la estructura» ⇒ E(y | x₀); «un sector» / «un acero» ⇒ predicción.
- «Disminuye en más de 0,25» ⇒ **β₁₀ = −0,25** y cola izquierda. Revisar el signo en el campo β1₀.
- ¿x₀ está dentro del entorno observado? Si no, decir que es extrapolar.

---

## 3. Por qué falla la app (casos reales)

La app combina tres lecturas: **reglas** (un programa que reconoce frases), **IA con ejemplos** e **IA por tema** (hasta el 04/11 la tercera era la «IA razonada»). Las tres alimentan el **mismo** motor de cálculo, así que si coinciden en el planteo, coinciden en el número. Los errores salen de cómo se **lee** el enunciado.

### 3.1 Las tres lecturas coinciden en el mismo error (consenso equivocado)
Es el más peligroso, porque la app muestra ✅.
- **Complemento**: «9 unidades tienen fallas… estimar el porcentaje de unidades **no falladas**». Las tres estimaron p de falladas: [0,0442; 0,1723] en lugar de [0,8277; 0,9558]. *(2° parcial 10/11/25, 2b; corregido.)*
- **Relación de σ vs. error de la media**: «reducir un 15% la relación de la estimación del desvío». Las dos IA calcularon el n del error de la **media** (7 más) en lugar de la relación entre límites del IC de **σ** (10 más). *(1° parcial 29/04/25, 1c; corregido.)*

**Qué mirar:** el punto 2 del control (¿qué parámetro?).

### 3.2 Una palabra de un inciso arrastra todo el problema
- En el 2° parcial 10/11/25, el inciso c dice «Modelo Gamma» y las reglas trataron los incisos a y b (comparación de medias de A y B) también como bondad de ajuste: «faltan datos». *(Corregido.)*
- Mismo patrón en el 2° parcial 23/06/25 (Q2, práctica del 02/11): las reglas leyeron 2b («mínima diferencia porcentual») como χ² («faltan datos»; las IA dan bien h = 1,0037 → 0,37%). Al revés, las dos IA marcaron 2c («¿se ajusta a un modelo Normal?») como «no lo resuelve la app», y solo las reglas lo resolvieron (χ² = 2,2167 < 5,9915, no rechaza). La app lo muestra como **una sola lectura**, no como error. *(Corregido el 02/11: un inciso que pregunta «¿se ajusta a…?» es siempre bondad de ajuste, y en la diferencia porcentual mínima sin sujeto va primero el grupo de mayor media.)*

**Qué mirar:** el punto 1 (¿el tema de **cada** inciso es el suyo?).

### 3.3 Datos que el enunciado no da y la app completa
- **α no dicho**: en el 2° parcial 10/11/25, 1c («¿se ajusta a un Modelo Gamma?») no dice el riesgo. La app heredó el 90% de confianza del inciso b → α = 0,10 → χ² = 4,6678 > 4,6052, **rechaza**. Con α = 0,05 (crítico 5,9915) **no rechaza**. El profesor dice: si no lo dan, se elige y se justifica.
- **Enunciado contradictorio**: en el 2° parcial 23/06/25, Q1 dice «reducir al 20%» y después «se redujo al 30%». Las reglas tomaron 20%; las IA, 30% (lo correcto según la referencia).

**Qué mirar:** el punto 4 (¿de dónde salió α?) y releer el enunciado cuando la app toma un número dudoso.

### 3.3 bis Números negativos escritos en la pantalla
- Hasta el 05/11, un número negativo escrito a mano en un campo **perdía el signo**: VII-13 d) («disminuye en más de 0,25 MPa», β₁₀ = −0,25) pasaba a +0,25 y la app concluía «se rechaza» con «aumenta en menos de 0,25». *(Corregido; test en `tests/test_clase_051126.py`.)*

**Qué mirar:** si un campo lleva un valor negativo (β₁₀, δ₀, datos), que la conclusión hable del signo correcto.

### 3.4 Redacciones nuevas que la app no conoce
Cada examen nuevo trajo una o dos frases que la app no reconocía:
- «diferencia de más del 1% … de A respecto de B» (comparación porcentual);
- «estimar la diferencia máxima esperada» (cota superior del IC);
- «sigue la ley Poisson», «NC = 99%», «5% de riesgo», «por cada ppm … máxima».

Todas quedaron corregidas, pero en el parcial va a haber frases nuevas. Cuando la app dice «faltan datos» o elige un tema raro, casi siempre es esto.

### 3.4 bis El chat de explicación inventa números
- En Q2 (práctica del 02/11), la explicación de la IA escribió x̄A = 10,61, x̄B = 10,67, SB > SA, d = 0,06 y t = 0,371. El solver da x̄A = 10,6957, SA = 0,2903, x̄B = 10,7972, SB = 0,2758 (**SA > SB**, así que el F es σA/σB), d = 0,1015 y t = 1,3785. La conclusión coincidió de casualidad. Además repitió el «no lo resuelve» del inciso c aunque las reglas lo resolvieron.

**Qué mirar:** los números se copian **solo del panel del solver**. La explicación sirve para la redacción, no para los valores.

### 3.5 Diferencias a propósito con la guía (la app sigue al profesor)
| Ejercicio | Guía | App | Por qué |
|---|---|---|---|
| III-3b | 0,2589 | 0,2057 | IC con r = 0: α entero (lo dijo el profesor). |
| III-11c | 855 | 755 exacto / 715 normal | La guía aplicó el criterio con el n inicial. |
| III-16a | RD 228 | CR 233 exacto / 229 normal | El exacto del profesor es el menor n con G ≤ α y F ≤ β. |
| III-15d | 26909 | 22255 | La guía usó Poisson por tanteo; la app no lo reproduce. |

### Cómo rindió la app en exámenes que no había visto
| Examen (a ciegas) | Acertó | Consensos equivocados |
|---|---|---|
| Final 15/12/25 + 2° parcial 23/06/25 | 11/12 | 0 |
| Exámenes 2024 (Notion) | 8/12 | 2 |
| 1° parcial 29/04/25 | 4/5 | 1 |
| 2° parcial 10/11/25 | 2/5 | 1 |

Después de cada uno se corrigieron las reglas (hoy acierta todos los del banco), pero **cada examen nuevo trajo errores nuevos**: hay que contar con que en el parcial aparezcan uno o dos.
