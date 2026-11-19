# Todo para el examen (2° parcial)

Un solo archivo para tener abierto en el examen. Junta lo que sirve de `GUIA_CONTROL.md` (control de la app), `REGLAS_PROFESOR.md` y `ESTILO_CATEDRA.md` (cómo se escribe), `TEORIA.md` (letras) y `EJERCICIOS_EXPLICADOS.md` (Excel). Esos archivos siguen como estaban.

**Tarjeta rápida**: lo de esta caja se mira en cada problema. El detalle está en las secciones de abajo.

**Por cada problema**
1. Pegar el enunciado, ✂️ Separar incisos, 📋 tabla si hay, 🗳️ Interpretar (o ⚡ Solo reglas).
2. **Mientras espera, escribir mi planteo a ciegas**: tema, parámetro, p₀ o δ₀, α (y β), H0/H1 y cola.
3. Comparar con la app. **Si no coinciden, releer el enunciado justo en ese punto.**
4. Corregir en la app y 🧮 Recalcular. Escribir copiando los números **solo del panel «Resolución»** (nunca del chat).

**Alarmas de la app**: ⚠️ sin consenso · ⚠️ las 2 IA contra las reglas · ☝️ una sola lectura · «faltan datos» o un tema raro ⇒ no confiar en lo que eligió. **✅ consenso tampoco garantiza nada.**

**Los 5 controles**
1. **Tema** de **cada** inciso (un inciso puede ser de otro tema).
2. **Parámetro**: ¿de lo que pregunta o de su complemento? ¿Varianza o desvío? ¿A − B o B − A? ¿Diferencia fija o con %?
3. **H1 = lo que se quiere probar**, y la dirección cierra con la muestra. Nada bilateral en p, σ ni comparaciones.
4. **α**: ¿lo dice **ese** inciso? Si no, elegir 0,05 y justificarlo. «Máximo» o «mínimo» ⇒ un límite, α entero.
5. **Datos**: cada número de la app está en el enunciado o sale de una cuenta. Las columnas de la tabla suman n.

**Sentido común al final**: probabilidades entre 0 y 1 · Sa entre los dos S · r con el signo de b1 · r² ≥ 0,8 si es técnico · si no se rechaza, el IC contiene el valor de H0 · la conclusión responde la pregunta.

**Frases de cierre**
- Se rechaza: «De manera que la hipótesis se rechaza, por lo cual **se puede asegurar que** …».
- No se rechaza: «De manera que la hipótesis no se rechaza, por lo cual **no hay evidencia suficiente para asegurar que** …». **Nunca «acepto H0».**
- Intervalo: «P(A ≤ θ ≤ B) = 0,95: se estima con un 95% de confianza que [parámetro en palabras] está entre A y B [unidad]».

---

## 1. Control del planteo de la app

Las **cuentas** del solver son confiables. Lo que falla es cómo **lee** el enunciado: eso es lo que se controla.

### Los votos

| Marca | Qué significa | Qué hacer |
|---|---|---|
| ✅ consenso | Dos o más lecturas dan lo mismo | Controlarlo igual: hubo errores con las tres de acuerdo |
| ⚠️ las 2 IA contra las reglas | Las IA coinciden y las reglas dicen otra cosa | La app elige las IA, pero es una moneda al aire (son el mismo modelo). Comparar las lecturas con el control y elegir con «Usar la lectura de» |
| ⚠️ sin consenso | Las tres dicen cosas distintas | La diferencia entre ellas marca el punto dudoso. **No elegir a ojo**: la lectura con n que no cierran está mal |
| ☝️ una sola lectura | Solo una pudo resolverlo | Controlar con más cuidado |

Al elegir otra lectura, la resolución se recalcula sola.

### Control de cada inciso (en este orden)

1. **Tema**: ¿es el test que pide **este** inciso? Una palabra de un inciso («Modelo Gamma») puede arrastrar a todos.
2. **Parámetro**: μ o σ; p de los que cumplen o de los que **no** cumplen; la diferencia en qué sentido; fija (δ₀) o porcentual (μA − 1,10·μB).
3. **H0 y cola**: ¿quedó en H1 lo que se quiere probar? ¿Criterio bien elegido? ¿La igualdad en H0?
4. **α (y β)**: ¿de dónde salió? Si el inciso no lo dice, la app puede haberlo **heredado** de otro inciso (por ejemplo, el 90% de confianza de una estimación). Un solo límite ⇒ α entero.
5. **Datos**: n, x̄, S, r, la columna correcta, la tabla completa. Un número que no está en el enunciado ni sale de una cuenta está inventado.
6. **Variable, unidad y acción** (sección 3 de la app): la variable en palabras, la unidad y la **acción si se rechaza H0** en infinitivo («lanzar el aditivo»). Con eso la app escribe α, β, la RD y la conclusión en términos del problema.
7. **Conclusión**: ¿responde la pregunta, en términos del problema?

### Dónde se corrige

- Tema → «Tema detectado».
- Criterio optimista o pesimista → «Criterio para plantear H0». Invierte H0: cambiarlo **antes** de tocar datos.
- n, x̄, S, p₀… → sección 3 «Datos del planteo» («Agregar un dato que no detectó» si falta).
- Tipo de pregunta, cola, α, δ₀ de un inciso → sección 4 «Cada inciso».
- Valores negativos (β₁₀, δ₀): fijarse que la conclusión hable del signo correcto.

### Si algo falla

- **La IA no responde**: ⚡ Solo reglas, y controlar todavía más.
- **El intérprete no entiende el problema**: páginas «Resolver a mano, por tema». Se cargan los datos a mano y el solver calcula igual.
- **La justificación de H0** que escribe la app puede ser genérica: reescribirla siempre con el enunciado.

---

## 2. Cómo se escribe la resolución

El profesor corrige **la interpretación, no solo los números**: «si falta alguno de esos elementos, el problema está mal hecho, aunque los números estén bien».

### Pasos del ensayo (en este orden)

1. **Variable** en palabras, con unidad y entorno. «X: consumo de combustible de un vehículo en una corrida, en litros.» En proporción, lo que se cuenta: «r: cantidad de piezas defectuosas en una muestra de 50».
2. **H0 y H1**, primero en palabras y después en símbolos, con el criterio **justificado**.
3. **α** (y β en el valor alternativo, si corresponde). Las 4 probabilidades en términos del problema: α = P(lanzar el aditivo ∣ no reduce el consumo), 1 − α, β = P(no lanzar ∣ lo reduce a μ₁), 1 − β.
4. **n**, si no está dado.
5. **Valor crítico, CR y RD**, antes de ver la muestra.
   - CR: la desigualdad («r ≥ 55»).
   - RD: en lenguaje de planta, para el operario. «Si en 1637 encuestados hay 229 o más interesados, se inicia una nueva campaña; si no, no.»
6. **Estimador** de la muestra (x̄, S, r, j, d, d̄, b1).
7. **Comparar el estimador contra el crítico**, en unidades de la variable (r contra r_c, j contra j_c, d contra d_c). **Nunca** contra μ₀ o δ₀. Concluir en términos del problema.

Diseño (todavía no hay muestra): pasos 1 a 5.

### H0: dónde va cada cosa

- **Regla madre**: H0 se plantea para que el **error de tipo I sea el más grave**.
- **Orden para decidir**:
  1. Si el enunciado dice qué se quiere probar («¿se puede asegurar que…?», «confirman», «la denuncia dice que…»), eso va en **H1**.
  2. Si no, el criterio.
  3. Si no alcanza, comparar la gravedad de los errores.
- **Pesimista** (riesgo económico: inversión, máquina o proveedor nuevo, producto nuevo, modificación, campaña): H0 = «no funciona». Pesimista **aunque la campaña sea barata**.
- **Optimista** (control de proceso, recepción de un **proveedor habitual**, controles de rutina): H0 = «cumple, está bajo control». Rechazar = detener el proceso o rechazar el lote.
- **La igualdad va siempre en H0.**
- **Sin bilaterales** en σ², σ, p ni comparaciones: «jamás me planteen una hipótesis bilateral en comparación». La muestra orienta: si S₂ > S₁, solo se puede intentar probar σ₂ > σ₁.
- **α no dado**: se elige y se justifica (chico ≤ 0,01; estándar 0,05; grande ≥ 0,10). Ruleta: 0,05 «no porque sea estándar», sino porque el perito tiene que ser imparcial. **Una vez fijado, no se toca.** Nunca decidir con el p-valor.

### Justificar la distribución

- No es «uso Z porque conozco σ» ni «t porque no conozco σ».
- x̄ es normal; al estandarizar se divide por un **parámetro** (σ), y una normal dividida por una constante sigue siendo normal ⇒ **Z**.
- Si se divide por **S**, que es una variable aleatoria (raíz de una χ²), queda una **t de Student** con ν = n − 1, **sea cual sea n**. Nada de «n ≥ 30».
- Dos varianzas: poblaciones normales y muestras independientes ⇒ j²/ψ² ~ F(n₁ − 1; n₂ − 1).
- p: binomial **exacta** (cada elemento cumple o no, con la misma p, independientes).

### Números

- **Nada sale «de la galera»**: cada número es un **dato** del enunciado, un **valor de tabla** con su argumento («t(0,95; 7) = 1,8946») o una **fórmula con los valores reemplazados**. Un número de otro inciso se cita («del inciso a»).
- **Mínimo 4 decimales** en todo el desarrollo y en los fractiles. Los periódicos como fracción (1/37).
- **Probabilidades entre 0 y 1, nunca en %**: «el primero que me ponga 30% de probabilidad, olvidate de aprobar». Se admite «95% de confianza» y una proporción en % si piden un «porcentaje».
- **Redondeos lógicos**:
  - n y ν al entero superior;
  - ν de Welch se **trunca** (124,9 → 124);
  - en los IC, el límite inferior hacia abajo y el superior hacia arriba;
  - en discretas, el crítico que deja α real ≤ α.
- **Notación**: P puntual, F acumulada a izquierda, G acumulada a derecha, Φ la F de la normal estándar. Escribir P(X ≤ x) en lugar de F es un «error conceptual». Escribir «ν = número de grados de libertad».

### Intervalos

1. Variable y datos.
2. Confianza y fractil: 1 − α = 0,90 ⇒ α/2 = 0,05 ⇒ Z(0,95) = 1,6449. **Un solo límite («mínimo», «máximo») ⇒ α entero.**
3. Límites A y B con unidades.
4. **P(A ≤ θ ≤ B) = 1 − α**.
5. Conclusión en palabras.

### β y potencia

Decir qué evento es en palabras («no implementar la modificación cuando la proporción real es 0,10»), la región de no rechazo, la cuenta y la probabilidad (entre 0 y 1) con una frase que la interprete. β no es 1 − α.

### Errores que el profesor ya penalizó o anticipó

- Probabilidades en %.
- Hipótesis sin justificar en palabras.
- Mal fundamento de la distribución.
- Estimar p con la aproximación normal («aberración»).
- 2 decimales o periódicos truncados.
- Comparar el estimador contra μ₀, o el crítico del lado equivocado.
- Dividir α por 2 con un solo límite.
- Creer que n iguales ⇒ apareadas.
- En bondad de ajuste, la probabilidad puntual en la clase que completa el dominio.
- En n para desvíos, usar R' en lugar de R = R'².
- Confundir α con β en la fórmula de n.
- «Acepto H0».

### Checklist antes de pasar al siguiente problema

- [ ] Variable en palabras, con unidad.
- [ ] H0 justificada en palabras, con la igualdad.
- [ ] Distribución justificada por su estructura.
- [ ] α fijado antes de la muestra; CR y RD escritas.
- [ ] Estimador contra crítico, en unidades de la variable.
- [ ] 4 decimales; probabilidades entre 0 y 1.
- [ ] Cada número con su origen (dato, tabla o fórmula reemplazada).
- [ ] Intervalos con P(A ≤ θ ≤ B) = 1 − α.
- [ ] Conclusión en términos del problema, sin «acepto H0».

---

## 3. Tema III · Proporción

**Se reconoce por**: «porcentaje de», «proporción», «defectuosos», «x de las n unidades». Se cuenta cuántos cumplen algo (sí/no).

**Controlar de la app**
- ¿p de lo que pregunta o del **complemento**? («estimar el porcentaje de **no** falladas» ⇒ r = n − r.)
- Control de proceso o proveedor habitual ⇒ optimista (H0: cumple). Campaña, producto o proveedor nuevo ⇒ pesimista (H0: no funciona).
- «Aumento de 3 **puntos**» es 0,12 → 0,15, no 0,12·1,03.

**Ensayo** (siempre unilateral, se decide con r contra r_c):

| Caso | H0 | r_c | CR | β en p₁ |
|---|---|---|---|---|
| 1 (sospecho p mayor) | p ≤ p₀ | el menor con G_b(r_c ∣ n; p₀) ≤ α | r ≥ r_c | F_b(r_c − 1 ∣ n; p₁) |
| 2 (sospecho p menor) | p ≥ p₀ | el mayor con F_b(r_c ∣ n; p₀) ≤ α | r ≤ r_c | G_b(r_c + 1 ∣ n; p₁) |

- El aplicativo da dos r_c vecinos: se elige el que deja **α real ≤ α**, y se muestran los dos.
- El α* (p-valor) «no me gusta»: no decide.
- En la guía, G_b(55 ∣ 150; 0,30) se escribe Gb(55/150; 0,30).

**IC de p**: siempre **exacto** (Beta o F), nunca la normal.
- A = 1 / [1 + ((n − r + 1)/r)·F(1 − α/2; 2(n − r + 1); 2r)]
- B = 1 / [1 + (n − r)/((r + 1)·F(1 − α/2; 2(r + 1); 2(n − r)))]
- Con **r = 0**: el límite superior con **α entero**.

**n del plan con α y β**
- **Exacto**: el menor n con G ≤ α y F ≤ β (o al revés en el caso 2).
- **Normal**: n = [(Z(1 − α)·√(p₀q₀) + Z(1 − β)·√(p₁q₁)) / (p₁ − p₀)]².
- **Poisson**: con R = p₁/p₀. Si los n difieren, se toma el mayor.
- **Justificar la aproximación con el n resultante**: normal si n·p > 10 y n·(1 − p) > 10; Poisson si p ≤ 0,005. Si se cumplen los dos o ninguno, **Mermoz**: n₀ = 0,23·(1 − p)²/p³; si n > n₀, normal; si no, Poisson. «No me usen otro criterio» (nada de n ≥ 30 ni np ≥ 5).

**Recepción de lotes**: AQL = p₀ (α = riesgo del proveedor); RQL o LTPD = p₁ (β = riesgo del comprador).

---

## 4. Tema IV · Comparación de varianzas o desvíos

**Se reconoce por**: «variabilidad», «dispersión», «homogeneidad», «más regular», «desvío» de dos grupos. «¿Confirman los datos la conclusión de…?» ⇒ esa conclusión va en H1.

**Controlar de la app**
- ¿Pregunta por **varianza** o por **desvío**? El mismo parámetro de punta a punta: ψ² y j² si es varianza; φ y j si es desvío. La decisión es la misma, pero la conclusión habla de lo que pregunta.
- ¿Quién va arriba? El que se sospecha mayor (la muestra orienta). Usar letras de los grupos (A/B, Norte/Sur), no 1/2.
- Poblaciones normales e independientes: es un supuesto **necesario** (la F no es robusta).

**Ensayo**
- ψ² = σ₁²/σ₂², con estimador j² = S₁²/S₂² ~ F(ν₁ = n₁ − 1; ν₂ = n₂ − 1).
- Caso 1, H0: ψ² ≤ ψ₀²: j²_c = ψ₀²·F(1 − α; ν₁; ν₂), CR: j² > j²_c. β = F_F(ψ₀²/ψ₁²·F(1 − α)).
- Caso 2, H0: ψ² ≥ ψ₀²: j²_c = ψ₀²·F(α; ν₁; ν₂), CR: j² < j²_c. β = 1 − F_F(ψ₀²/ψ₁²·F(α)).
- Con desvíos, «el φ va al cuadrado»: j_c = √(φ₀²·F). Comparar j con j_c.
- «Reducir el desvío un 12%» ⇒ H0: φ ≥ 0,88.
- F(α; ν₁; ν₂) = 1 / F(1 − α; ν₂; ν₁): se **invierten** los grados de libertad.

**IC**: A = j²/F(1 − α/2; ν₁; ν₂) y B = j²/F(α/2; ν₁; ν₂). Para desvíos, A' = √A y B' = √B.
- La F es asimétrica: el IC no es «j² ± algo».
- **Interpretar en %**: «σA² como mínimo 79,65% menor y como máximo 11,37% mayor que σB²».
- Si no dicen la relación (A/B o B/A), se elige una, se dice cuál y se resuelve solo esa.

**n** con n₁ = n₂, iterando ν (n = ν + 1). R = B/A; para desvíos **R = R'²**. En ensayos, R = ψ₁²/ψ₀² (caso 1) o ψ₀²/ψ₁² (caso 2): tiene que dar > 1.

---

## 5. Tema V · Comparación de medias

**Se reconoce por**: «promedio», «rendimiento», «performance» de dos grupos; «supera en X», «más de un X% más».

**Controlar de la app**
- **¿Apareadas?** Solo si es el mismo individuo o la misma unidad experimental («los mismos operarios antes y después»). **No** por n iguales.
- ¿Quién va primero? ¿La diferencia es fija (δ₀) o porcentual (h)?
- **Nunca bilateral**: la muestra orienta.

**Elegir el método (y justificarlo)**
1. σ₁ y σ₂ conocidos ⇒ Z (teórico: «jamás vas a conocer ambos»).
2. Desconocidos ⇒ **test F auxiliar**: unilateral, con la S mayor sospechada mayor, **α propio de 0,10** (no el del problema).
   - No se rechaza ⇒ **amalgamado**: Sa² = [(n₁ − 1)S₁² + (n₂ − 1)S₂²]/(n₁ + n₂ − 2), ν = n₁ + n₂ − 2. Control: Sa queda entre S₁ y S₂.
   - Se rechaza ⇒ **Welch**: √(S₁²/n₁ + S₂²/n₂), con ν = (S₁²/n₁ + S₂²/n₂)² / [(S₁²/n₁)²/(n₁ − 1) + (S₂²/n₂)²/(n₂ − 1)], **truncado**.
3. Mismo individuo ⇒ **apareadas**: dᵢ = diferencia de cada par, d̄, S_d, t con ν = n − 1 (n = pares).

**Ensayo**
- Caso 1 (H0: δ ≤ δ₀): d_c = δ₀ + t(1 − α; ν)·Sa·√(1/n₁ + 1/n₂). Caso 2: con −.
- Apareadas: d_c = δ₀ + t(1 − α; n − 1)·S_d/√n.
- **Sin β ni n** en ensayos de medias con t (hace falta la t no central).

**Porcentuales**
- «μ₁ supera en más de un 10% a μ₂» ⇒ δ* = μ₁ − 1,10·μ₂, con estimador d* = x̄₁ − 1,10·x̄₂.
- Desvío: Sa·√(1/n₁ + h²/n₂). **h² va en el término de la población que lleva h** (la de referencia). En Welch, también dentro de ν.
- **Porcentaje mínimo**: plantear la CR justo en el límite como ecuación en h, elevar al cuadrado y resolver la cuadrática. **Verificar cada raíz** en la ecuación original: una suele ser falsa.

**Diferencia mínima o máxima**: un solo límite, con t(1 − α).

---

## 6. Tema VI · Contrastes χ²

**Cuál usar**
- «asociación», «¿depende…?» ⇒ **independencia**;
- «niveles, probabilidades o porcentajes» de varios grupos (o dos proporciones) ⇒ **consistencia**;
- «se ajusta a», «sigue la ley», «es razonable suponer un modelo» ⇒ **bondad de ajuste**.

**H0** (no hay criterio pesimista ni optimista)
- Consistencia: **por categoría**, p₁ª,M = p₁ª,T = p₁ª,N, y lo mismo para cada categoría. H1: alguna es distinta. No poner «p mañana = p tarde» sin decir de qué categoría.
- Independencia: **en palabras** («las fallas de pintura son independientes del color»).
- Bondad: «lo observado se ajusta al modelo X».

**Cálculo**
- Esperados: consistencia, p̂ global de la categoría × n del grupo; independencia, total de la fila · total de la columna / N; bondad, N·pᵢ.
- Los observados no se tocan. Los esperados **llevan decimales** y las sumas cierran.
- N ≥ 60 y todos los E ≥ 5 (los O pueden ser 0). Si un E < 5, **amalgamar** con la clase vecina (O y E juntos). N < 60: anotarlo como limitación.
- ν: tablas, (f − 1)(k − 1); bondad, **clases efectivas** − 1 − parámetros estimados con la muestra (Poisson con x̄ ⇒ 1; uniforme o patrón histórico ⇒ 0).
- **Completar el dominio**: una clase nueva al final (y/o al principio) con O = 0 y probabilidad **acumulada** (G en la última, F en la primera), nunca la puntual. Son clases nuevas: se amalgaman solo si su E < 5.
  - Normal y Gumbel: los dos extremos. Exponencial, Weibull y gamma (x ≥ 0) con datos desde 0: solo al final.
- CR siempre a la derecha: χ²calc > χ²(1 − α; ν). α en general 0,05.
- **Ajuste demasiado perfecto**: si χ²calc < χ²(α; ν), sospechar de los datos.

**Modelos continuos**: x̄ y S con las marcas de clase; probabilidades por intervalos.
- Gumbel: β = S·√6/π; θ = x̄ + 0,5772·β (mínimo) o θ = x̄ − 0,5772·β (máximo).
- Weibull: por Solver, Buscar objetivo o la tabla de ajuste por momentos (CV = S/x̄): **decir cuál se usó**.
- **Mejor ajuste** = el de menor χ² entre los que no se rechazan.

**Conclusión: ¿«sigue» o «es un buen candidato»?**

| Resultado | Modelo | ¿Proceso físico? | Se escribe |
|---|---|---|---|
| Se rechaza | cualquiera | — | «Se puede asegurar que **no sigue** el modelo X» |
| No se rechaza | **continuo** | no se pregunta | «El modelo X **es un buen candidato**» |
| No se rechaza | **discreto** | **sí, todas las condiciones** | «**Sigue** el modelo X con [parámetro y unidad]» |
| No se rechaza | discreto | no, o no se puede afirmar | «El modelo X **es un buen candidato**» |

- **Proceso de Poisson**: sucesos **puntuales**, en un **medio continuo** (tiempo, longitud, área), **independientes**, **al azar** (no programados) y con **tasa media constante**. No se cumple con llegadas en grupos, turnos o citas programadas, hora pico mezclada con valle, o contagios.
- **Binomial**: dos resultados, p constante, ensayos independientes, n fijo, población infinita o con reposición. Población finita sin reposición ⇒ hipergeométrica.
- Ejemplo: «Como la llegada de vehículos es un proceso de Poisson (sucesos puntuales, independientes y al azar en el tiempo, con tasa constante), se puede afirmar que la cantidad de vehículos por minuto sigue una Poisson con m = 10,52 veh/min».
- Al rechazar en consistencia: «algún nivel es distinto», no «todos». Al no rechazar independencia: «no hay evidencia suficiente para asegurar que exista asociación».

---

## 7. Tema VII · Regresión simple

**Se reconoce por**: «recta», «modelo lineal», «asociación lineal», «por cada unidad de X» (β₁), «influencia porcentual» (r²). Regresión **múltiple no entra** en el parcial.

**Controlar de la app**
- ¿Cuál es Y (explicada, aleatoria) y cuál X (explicativa)? Nunca decir «variable independiente». Revisar las unidades.
- ¿Validó el modelo, con el mínimo de r² del **uso del problema**?
- «Disminuye en más de 0,25» ⇒ **β₁₀ = −0,25** y cola izquierda: revisar el signo.
- ¿x₀ está dentro del entorno observado? Si no, es extrapolar y hay que decirlo.

**Procesar los datos** (como en el pizarrón)
- n, Σx, x̄, Σx², Σy, ȳ, Σy², Σxy.
- Sxy = Σxy − n·x̄·ȳ; Sxx = Σx² − n·x̄²; Syy = Σy² − n·ȳ².
- b1 = Sxy/Sxx (unidad de Y por unidad de X); b0 = ȳ − b1·x̄ (unidad de Y). Recta: ŷ = b0 + b1·x.
- r = Sxy/√(Sxx·Syy), con el signo de b1; r².
- S² = (Σy² − b0·Σy − b1·Σxy)/(n − 2); S_b1 = S/√Sxx.

**Validar siempre, aunque no lo pidan**
1. **Existencia**: H0: ρ = 0 (β₁ = 0). |t_obs| = |b1|/S_b1 contra **t(1 − α; n − 2)**. Si no dan α, se elige y se justifica.
2. **Fuerza** con r², según el uso (orientativo): ≥ 0,8 técnico o industrial; ≥ 0,6 económico; ≥ 0,4 sociología o psicología.

Si no se valida, «la pregunta no tiene sentido»: no se lo usa para estimar.

**Interpretar en términos del problema, con unidades**
- b1: «por cada m/min más de velocidad, el desgaste aumenta en promedio 0,002577 mm» (contribución marginal).
- r²: «la velocidad influye en un 99,30% sobre el desgaste; el resto, la perturbación del entorno u otras variables».
- b0: solo «en teoría», si x = 0 está en el entorno observado. **β₀ no se estima**: el modelo vale de x mín a x máx.

**Inferencias**
- IC de β₁: b1 ± t(1 − α/2; n − 2)·S_b1. Con negativos, A es el más negativo. P(A ≤ β₁ ≤ B) = 1 − α.
- Ensayo de β₁ (sin bilateral): b1c = β₁₀ + t(1 − α; n − 2)·S_b1 si H1: β₁ > β₁₀; con − si H1: β₁ < β₁₀. Comparar b1 contra b1c.
- **Promedio** («el desgaste medio», «toda la estructura») ⇒ IC de E(y ∣ x₀): ŷ₀ ± t(1 − α/2; n − 2)·S·√(1/n + (x₀ − x̄)²/Sxx).
- **Un caso** («una jornada», «un acero», «un sector») ⇒ **predicción**: lo mismo con **1 +** dentro de la raíz. P(A ≤ y(x₀) ≤ B) = 1 − α.
- ρ² por Fisher: Zρ ± Z(1 − α/2)·√(1/(n − 3)), y los límites al cuadrado.

---

## 8. Valores de tabla y Excel

Se sacan con *Probability Distributions* o con Excel (en castellano). La app ya los calcula: esto es para verificar.

| Valor | Excel |
|---|---|
| Z(1 − α) | `INV.NORM.ESTAND(1−α)` |
| Φ(z) | `DISTR.NORM.ESTAND.N(z; VERDADERO)` |
| Normal acumulada | `DISTR.NORM.N(x; μ; σ; VERDADERO)` |
| t(1 − α; ν) | `INV.T(1−α; ν)` |
| F(1 − α; ν₁; ν₂) | `INV.F(1−α; ν₁; ν₂)` |
| F_F(x), acumulada de la F | `DISTR.F.N(x; ν₁; ν₂; VERDADERO)` |
| χ²(1 − α; ν) | `INV.CHICUAD(1−α; ν)` |
| Binomial puntual P_b(r) | `DISTR.BINOM.N(r; n; p; FALSO)` |
| Binomial F_b(r) = P(R ≤ r) | `DISTR.BINOM.N(r; n; p; VERDADERO)` |
| Binomial G_b(r) = P(R ≥ r) | `1 − DISTR.BINOM.N(r − 1; n; p; VERDADERO)` |
| Poisson puntual P(r) | `POISSON.DIST(r; m; FALSO)` |
| Poisson G(r) = P(X ≥ r) | `1 − POISSON.DIST(r − 1; m; VERDADERO)` |
| IC exacto de p: A | `INV.BETA.N(α/2; r; n − r + 1)` |
| IC exacto de p: B | `INV.BETA.N(1 − α/2; r + 1; n − r)` |

Probabilidades: todas entre 0 y 1, con 4 decimales.

---

## 9. Qué es cada letra

**Cómo se lee la notación**

| Se escribe | Se lee |
|---|---|
| Letra griega: μ, σ, φ, ψ, δ, ρ, β₁ | Un número de la **población**. Existe, pero no se conoce. Excepción: p. |
| Letra latina: x̄, S, p̂, r, j, d, b1 | Una cuenta hecha con la **muestra**. |
| Subíndice 0: p₀, φ₀, δ₀, β₁₀ | El valor que **propone H0** (el límite). |
| Subíndice 1: p₁, φ₁ | Un valor de H1 que **interesa detectar** (para β y n). |
| Subíndice c: r_c, j_c, d_c, b1c | El valor **crítico**: desde ahí se rechaza H0. |
| Raya arriba: x̄, d̄, ȳ | Promedio de la muestra. |
| Gorro: p̂, ŷ | Valor estimado. |
| «∣» o «/» dentro de una probabilidad | «**dado**»: G_b(55 ∣ 150; 0,30) = Gb(55/150; 0,30) es la probabilidad de 55 o más, dado n = 150 y p = 0,30. |
| ~ | «se distribuye como»: r ~ Bi(150; 0,30). |
| P, F, G, Φ | Puntual (=), acumulada a izquierda (≤), acumulada a derecha (≥), acumulada de la normal estándar. El subíndice b es binomial. |
| Z(0,95); t(0,95; 7); F(0,95; 15; 20); χ²(0,95; 3) | Valor de tabla que deja 0,95 a la izquierda; después del «;», los grados de libertad. |

**Glosario**

| Letra | Qué es | Tema |
|---|---|---|
| α | Probabilidad de rechazar H0 siendo cierta (error de tipo I). Se elige. | todos |
| β | Probabilidad de no rechazar H0 siendo falsa (tipo II), en un valor de H1. | III, IV |
| 1 − β | Potencia: probabilidad de detectar H1 en ese valor. | III, IV |
| α real | El riesgo de tipo I que queda de verdad con el r_c elegido. | III |
| α* | p-valor. Solo informativo. | III |
| p, p₀, p₁, p̂ | Proporción real, la de H0, la que interesa detectar, la de la muestra. | III |
| q₀, q₁ | 1 − p₀ y 1 − p₁. | III |
| n, r, r_c | Tamaño de la muestra, cantidad de casos en la muestra, cantidad crítica. | III |
| R (en III) | p₁/p₀ (aproximación Poisson para n). | III |
| ψ² = σ₁²/σ₂², φ = σ₁/σ₂ | Cociente de varianzas y de desvíos reales. | IV |
| j², j | Sus estimadores, S₁²/S₂² y S₁/S₂ (`TEORIA.md` y la app: J², J). | IV |
| R (en IV) | Relación entre los límites de un IC (B/A). Para desvíos, R = R'². | IV |
| ν, ν₁, ν₂ | Grados de libertad (arriba y abajo en la F). | todos |
| δ = μ₁ − μ₂, d | Diferencia de medias real y de la muestra (`TEORIA.md`: Δ, D). | V |
| h, δ*, d* | Factor porcentual (1,15 = 15% más) y la diferencia con el h. | V |
| Sa | Desvío amalgamado (común a las dos muestras). | V |
| dᵢ, d̄, S_d | Diferencia de cada par, su promedio y su desvío (apareadas). | V |
| Fo, Fe (O, E) | Frecuencias observadas (se cuentan) y esperadas (se calculan bajo H0). | VI |
| N, m | Total de observaciones; media de la Poisson. | VI |
| f, k | Cantidad de filas y de columnas; en bondad, k = clases efectivas. | VI |
| X, Y | Explicativa y explicada. | VII |
| β₀, β₁ | Coeficientes **reales** de la recta. No confundir β₁ con el β del error. | VII |
| b0, b1, ŷ | Sus estimadores y el valor de la recta. | VII |
| Sxx, Syy, Sxy | Sumas de cuadrados y de productos respecto de los promedios. | VII |
| S, S_b1 | Desvío alrededor de la recta y desvío de b1. | VII |
| r (en VII), r², ρ | Correlación de la muestra, coeficiente de determinación, correlación real. | VII |
| x₀, ŷ₀, y(x₀) | Donde se pronostica, el valor de la recta ahí, el valor de **un** caso. | VII |

---

## 10. Diferencias a propósito con la guía

Si un problema del examen es de la guía y la app da otro número, puede ser a propósito: la app sigue al profesor.

| Ejercicio | Guía | App | Por qué |
|---|---|---|---|
| III-3b | 0,2589 | 0,2057 | IC con r = 0: α entero (lo dijo el profesor). |
| III-11c | 855 | 755 exacto / 715 normal | La guía aplicó el criterio con el n inicial. |
| III-16a | RD 228 | CR 233 exacto / 229 normal | El exacto es el menor n con G ≤ α y F ≤ β; el 228 de la guía es una errata. |
| III-15d | 26909 | 22255 | La guía usó Poisson por tanteo. |
