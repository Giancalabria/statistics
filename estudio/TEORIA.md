# Teoría para entender (no para calcular): 2° parcial

Resumen conceptual de los temas nuevos: ensayos sobre p (III), comparación de varianzas (IV), comparación de medias (V), χ² (VI) y regresión simple (VII). La idea es entender **qué representa cada letra**, para poder controlar el planteo de la app y escribirlo como lo pide Dopazo. Las cuentas las hace la app; las reglas de redacción están en [REGLAS_PROFESOR.md](REGLAS_PROFESOR.md).

---

## 0. La idea que ordena todo: tres niveles

Casi toda la confusión se arregla si cada símbolo se ubica en uno de estos tres niveles:

| Nivel | Qué es | Cómo se escribe | ¿Cambia de muestra en muestra? |
|---|---|---|---|
| **Parámetro** | Un número de la **población**. Existe, pero no lo conocemos. Es lo que queremos saber. | Letra **griega** (μ, σ, ψ, φ, Δ, ρ, β₁). Excepción: p | **No.** Es fijo. |
| **Estimador** | Una **cuenta que se hace con la muestra** para aproximar el parámetro. Antes de sacar la muestra es una variable aleatoria. | Letra **latina** (x̄, S, p̂, r, J, D, b₁) | **Sí.** Otra muestra da otro valor. |
| **Distribución del estimador** | Cómo se reparten los valores del estimador si sacáramos muchas muestras. Es lo que permite decir «este valor es raro». | Z, t, F, χ², binomial | — |

Y hay un cuarto tipo de número que **no es ninguno de los tres**: los valores que **uno propone** en las hipótesis (p₀, p₁, ψ₀, Δ₀, β₁₀). No salen de la muestra ni son la verdad: son la «línea» que se elige para decidir.

> **Regla práctica:** si una letra es griega, preguntate «¿de qué población?». Si es latina, preguntate «¿de qué muestra?». Si tiene subíndice 0 o 1, preguntate «¿quién lo propuso y por qué?».

### Mapa de los temas

| Tema | Pregunta que contesta | Parámetro | Estimador | Distribución |
|---|---|---|---|---|
| III | ¿La proporción de una población supera (o no llega a) un valor? | p | r (cantidad de casos en la muestra), o p̂ = r/n | Binomial (n, p) |
| IV | ¿Una población es más dispersa que otra? | ψ² = σ₁²/σ₂² (o φ = σ₁/σ₂) | J² = S₁²/S₂² (o J) | F (ν₁, ν₂) |
| V | ¿Una población tiene media mayor que otra? | Δ = μ₁ − μ₂ | D = x̄₁ − x̄₂ (o d̄ en apareadas) | Z o t |
| VI | ¿Los datos son compatibles con un reparto supuesto? | Las probabilidades de cada categoría | Las frecuencias observadas O | χ² |
| VII | ¿Y depende de X? ¿Cuánto cambia Y por cada unidad de X? | β₀, β₁, ρ | b₀, b₁, r | t (y Fisher para ρ) |

---

## 1. La lógica del ensayo (vale para todos los temas)

### 1.1 Qué es un ensayo

Un ensayo es una **regla de decisión armada antes de mirar la muestra**. Se parece a un juicio:

- **H0** es lo que se sostiene mientras no haya pruebas en contra (el acusado es inocente).
- **H1** es lo que se quiere demostrar y requiere evidencia (culpable).
- La muestra es la evidencia. Si es muy difícil de explicar suponiendo H0, se rechaza H0.
- Si la evidencia no alcanza, el acusado no queda «probado inocente»: queda «no se pudo probar que sea culpable». Por eso **nunca se dice «se acepta H0»**, sino «no hay evidencia suficiente para asegurar que…».

### 1.2 Por qué H0 va donde va

El ensayo controla directamente **solo un error**: rechazar H0 cuando era cierta (error de tipo I, con probabilidad α). Entonces:

> **H0 se elige de modo que el error de tipo I sea el más grave.** Así el error peor es el que queda controlado con α chico.

- **Pesimista** (invertir, cambiar de proveedor, máquina nueva, campaña): H0 = «no funciona». El error grave es invertir en algo que no sirve, y queda como tipo I.
- **Optimista** (control de un proceso, proveedor habitual): H0 = «está bien». El error grave es parar la planta o rechazar el lote sin motivo.
- Si el enunciado dice «se quiere probar que…», eso va en **H1**.
- **La igualdad siempre va en H0.** Por eso nunca se puede «probar» la igualdad: está del lado que solo se puede no rechazar.

### 1.3 Las cuatro probabilidades

|  | H0 es cierta | H0 es falsa (vale H1) |
|---|---|---|
| **Se rechaza H0** | Error tipo I → **α** | Acierto → **1 − β** (potencia) |
| **No se rechaza H0** | Acierto → **1 − α** (confianza) | Error tipo II → **β** |

- **α**: probabilidad de rechazar H0 siendo cierta. **Se elige**, antes de ver la muestra, y no se toca más.
- **β**: probabilidad de no rechazar H0 siendo falsa. Pero «H0 falsa» abarca infinitos valores, así que **β siempre se calcula en un valor concreto de H1** (p₁, ψ₁…): «si la proporción real fuera 0,08, la probabilidad de no darme cuenta es β».
- **1 − β** (potencia): probabilidad de detectar que H0 es falsa cuando el valor real es ese p₁.
- Son probabilidades: **van entre 0 y 1, nunca en %**. Y en el examen hay que escribirlas en términos del problema.

### 1.4 Valor crítico, CR y RD

- **Valor crítico** (rc, J²c, Dc, χ²(1−α; ν)…): el valor del estimador que separa «compatible con H0» de «demasiado raro si H0 fuera cierta». Se calcula con α y con el valor de H0.
- **CR (región crítica)**: el conjunto de valores del estimador que llevan a rechazar (por ejemplo, r ≥ rc).
- **RD (regla de decisión)**: la CR dicha en lenguaje de planta: «si en 1637 encuestados hay 229 o más interesados, se inicia la campaña».
- Lo que se compara es **estimador contra crítico**, nunca el estimador contra p₀ o μ₀.

### 1.5 Por qué no hay bilaterales (en lo nuevo)

En p, en σ² y en todas las comparaciones, la pregunta real siempre tiene una dirección (¿es mayor?, ¿se redujo?). La muestra orienta: si S_B > S_A, lo único que tiene sentido intentar probar es σ_B > σ_A. Un solo límite ⇒ **α entero** en una sola cola (no α/2).

### 1.6 Qué hace n

Con n fijo, si se achica α crece β (y al revés). La única forma de achicar los dos a la vez es **juntar más datos**. Por eso, cuando dan α, β y un valor de H1, se puede calcular el n del plan: es el n más chico que cumple las dos exigencias.

### 1.7 Grados de libertad (ν)

ν = cantidad de datos «libres» que quedan después de estimar cosas con la misma muestra. Cada parámetro que se estima con la muestra consume uno:

- S con una muestra: ν = n − 1 (se usó x̄).
- Amalgamado: ν = n₁ + n₂ − 2 (se usaron dos medias).
- Regresión: ν = n − 2 (se usaron b₀ y b₁).
- χ² de bondad: clases − 1 − parámetros estimados.

---

## 2. Tema III: ensayos sobre una proporción p

### Qué representa cada cosa

| Símbolo | Qué es | Ejemplo |
|---|---|---|
| **p** | Proporción **real** de la población con la característica. Desconocida. | La fracción de piezas defectuosas de toda la producción. |
| **n** | Tamaño de la muestra. | 200 piezas revisadas. |
| **r** | Cantidad de casos con la característica **en la muestra**. Es el estimador con el que se decide. | 13 defectuosas. |
| **p̂ = r/n** | Proporción muestral. Equivalente a r. | 0,065. |
| **p₀** | Valor de p que define H0 (el límite). | «A lo sumo 5 % de defectuosos» ⇒ p₀ = 0,05. |
| **p₁** | Un valor de H1 que **importa detectar**. Sirve para β y para n. | «Si llega al 10 % quiero darme cuenta» ⇒ p₁ = 0,10. |
| **rc** | Cantidad crítica: a partir de cuántos casos se rechaza. | Rechazo si r ≥ 15. |
| **R** | Cantidad de casos con la característica en la muestra, **como variable aleatoria** (antes de sacarla). R ~ Binomial(n, p). | — |

### Por qué binomial

Cada elemento revisado «tiene o no tiene» la característica (Bernoulli), con la misma probabilidad p, independientes. Contar cuántos la tienen en n intentos es exactamente una binomial. Por eso **la estimación y el ensayo de p son exactos con la binomial**; las aproximaciones (normal, Poisson) se usan solo para calcular n.

### Los dos casos

- **Caso 1, H0: p ≤ p₀** (sospecho que p es mayor). Valores grandes de r son raros si H0 es cierta ⇒ rechazo si **r ≥ rc**. El rc es el primero que deja G_b(rc | n, p₀) ≤ α (la probabilidad de ver tantos o más, si p fuera p₀).
- **Caso 2, H0: p ≥ p₀** (sospecho que p es menor). Rechazo si **r ≤ rc**.
- β: suponiendo que el valor real es p₁, la probabilidad de caer **fuera** de la CR.

Como r es entero, no se puede lograr α exacto: se elige el rc que deja **α real ≤ α pedido**.

### Vocabulario de recepción de lotes

- **AQL** = p₀: la calidad aceptable. **α = riesgo del proveedor** (que le rechacen un lote bueno).
- **RQL / LTPD** = p₁: la calidad que no se tolera. **β = riesgo del comprador** (que le acepten un lote malo).

### Pregunta de control

<details><summary>Si en el caso 1 el valor de β te da 0,30, ¿qué significa en palabras?</summary>

Que si la proporción real de defectuosos fuera p₁, hay probabilidad 0,30 de que la muestra no muestre suficientes defectuosos y no rechacemos el lote (o no detectemos el aumento). No es «el 30 % de los lotes»: es una probabilidad y se escribe 0,30.
</details>

---

## 3. Tema IV: comparación de varianzas o desvíos

### Qué representa cada cosa

| Símbolo | Qué es |
|---|---|
| **σ₁², σ₂²** | Varianzas **reales** de cada población (dispersión, variabilidad, «precisión» de un proceso). |
| **ψ² = σ₁²/σ₂²** | El parámetro de comparación: **cuántas veces** es más grande una varianza que la otra. ψ² = 1 significa iguales; ψ² = 2, la del numerador es el doble. |
| **φ = σ₁/σ₂** | Lo mismo pero con desvíos (φ² = ψ²). |
| **S₁², S₂²** | Varianzas muestrales. |
| **J² = S₁²/S₂²** | El estimador de ψ². J = S₁/S₂ estima φ. |
| **ψ₀², φ₀** | El valor que se pone en H0. «Reducir el desvío un 12 %» ⇒ φ₀ = 0,88. |
| **ν₁ = n₁ − 1, ν₂ = n₂ − 1** | Grados de libertad del numerador y del denominador. |

### Por qué un cociente y no una resta

Las varianzas se comparan **en proporción**: «el doble de dispersión» tiene sentido; «4 unidades² más» casi no. Además, el cociente de dos varianzas muestrales (cada una ligada a una χ²) tiene una distribución conocida, la **F de Snedecor**. Si H0 dice ψ² = ψ₀², entonces J²/ψ₀² sigue una F(ν₁, ν₂). De ahí sale el crítico: J²c = ψ₀²·F(1−α).

### Lo que hay que pensar

- **Qué va en el numerador**: se recomienda poner arriba la población que se sospecha más dispersa y usar letras (A/B) en vez de 1/2.
- **Interpretar un IC en %**: si el IC de ψ² = σA²/σB² es (0,2035; 1,1137), significa que σA² está entre 79,65 % menor y 11,37 % mayor que σB². Si el intervalo contiene el 1, no se puede asegurar cuál es más dispersa.

---

## 4. Tema V: comparación de medias

### Qué representa cada cosa

| Símbolo | Qué es |
|---|---|
| **μ₁, μ₂** | Medias **reales** de cada población. |
| **Δ = μ₁ − μ₂** | El parámetro: cuánto más grande es una media que la otra (en las unidades de la variable). |
| **Δ₀** | El valor de H0. «Supera en más de 5 kg» ⇒ Δ₀ = 5. «Es mayor» ⇒ Δ₀ = 0. |
| **D = x̄₁ − x̄₂** | El estimador de Δ. |
| **Dc** | El crítico: Δ₀ más (o menos) un margen que depende de α y del error del estimador. |
| **Sa** (amalgamado) | Estimación del **desvío común** de las dos poblaciones, combinando las dos muestras. |
| **d, d̄, S_D** (apareadas) | La diferencia **dentro de cada individuo**, su media y su desvío. |
| **h** | Factor de una diferencia porcentual: «μ₁ supera en 10 % a μ₂» ⇒ h = 1,10 y Δ* = μ₁ − 1,10·μ₂. |

### Cómo se elige el método (lo que más se pregunta)

1. **¿Son los mismos individuos o la misma unidad experimental medidos dos veces?** (antes y después, el mismo auto con dos naftas) ⇒ **apareadas**. Tener n iguales **no** las hace apareadas.
2. Si son independientes y los σ son conocidos ⇒ Z (teórico, casi nunca pasa).
3. Si son independientes y los σ son desconocidos ⇒ **test F auxiliar** para ver si se puede suponer σ₁ = σ₂:
   - no se rechaza ⇒ **amalgamado** (se supone un σ común y se lo estima con las dos muestras juntas);
   - se rechaza ⇒ **Welch** (cada muestra con su propio S, y ν aproximado).

### Por qué cada cosa

- **Por qué t y no Z**: D se estandariza dividiendo por un error que contiene S. S es una variable aleatoria (cambia con la muestra), y dividir una normal por la raíz de una χ² da una **t de Student**. Si se dividiera por σ (un número fijo), seguiría siendo normal (Z).
- **Por qué el test F auxiliar usa α = 0,10**: acá el error peligroso es **no detectar** que las varianzas son distintas (y usar el amalgamado cuando no corresponde). Para que ese error (β) sea chico, se acepta un α más grande.
- **Por qué amalgamar**: si los dos σ son iguales, cada muestra es una estimación del mismo número; juntarlas (ponderando por sus ν) da una estimación mejor. Por eso Sa² siempre queda **entre** S₁² y S₂².
- **Por qué apareadas es mejor cuando corresponde**: al restar dentro de cada individuo, se cancela todo lo que es propio de ese individuo (un auto que gasta mucho gasta mucho con las dos naftas). Queda solo el efecto que interesa, con mucha menos variabilidad. Pasa a ser un problema de **una sola muestra** de diferencias, con ν = n − 1.
- **Por qué no hay β ni n en medias con t**: requieren la t no central, que no se da en la materia.

---

## 5. Tema VI: contrastes χ²

### Qué representa cada cosa

| Símbolo | Qué es |
|---|---|
| **O** (observadas) | Lo que **pasó** en la muestra: cuántos cayeron en cada celda o clase. No se tocan nunca. |
| **E** (esperadas) | Lo que **debería haber pasado en promedio si H0 fuera cierta**. Llevan decimales (son promedios, no conteos). |
| **(O − E)²/E** | Cuánto se aparta cada celda de lo esperado, en relación con lo esperado (desviarse 5 de un E = 10 es mucho; de un E = 1000, nada). |
| **χ²obs = Σ(O − E)²/E** | La distancia total entre lo observado y lo que dice H0. **0 = coincidencia perfecta**; cuanto más grande, peor. |
| **ν** | Cuántas celdas se pueden llenar «libremente» una vez fijados los totales y los parámetros estimados. |

### Por qué siempre cola derecha

El estadístico mide distancia: solo valores **grandes** contradicen H0. Se rechaza si χ²obs > χ²(1 − α; ν). (Un χ²obs sospechosamente chico, menor que χ²(α; ν), es un «ajuste demasiado perfecto»: se sospecha de los datos.)

### Los tres contrastes: misma cuenta, distinta pregunta

| | Consistencia (homogeneidad) | Independencia | Bondad de ajuste |
|---|---|---|---|
| **Diseño** | Varias **poblaciones** (turnos, sucursales), una variable categórica. Los totales de cada grupo los fija el diseño. | **Una** población, cada elemento se clasifica según **dos** variables. | **Una** muestra contra un **modelo teórico**. |
| **Palabra clave** | «niveles», «probabilidades», «porcentajes» de cada grupo | «asociación», «relación entre» | «se ajusta», «sigue un modelo» |
| **H0** | Por categoría: p_defectuoso,M = p_defectuoso,T = p_defectuoso,N (y una igualdad por cada categoría) | «La variable A es independiente de la B» (en palabras) | «Lo observado se ajusta al modelo X» |
| **Qué es E** | Si todos los grupos tuvieran las mismas proporciones | Si P(A y B) = P(A)·P(B) | n · P(clase) según el modelo |
| **ν** | (f − 1)(c − 1) | (f − 1)(c − 1) | clases efectivas − 1 − parámetros estimados |

- **De dónde sale E = (total fila · total columna)/N**: si no hay asociación, la proporción de la columna es la misma en todas las filas, así que a cada celda le toca su total de fila multiplicado por la proporción de su columna.
- **Por qué E ≥ 5**: la χ² es una aproximación y con esperadas chicas falla. Si alguna E < 5, se **amalgaman** clases (y se pierden grados de libertad).
- **Por qué se resta un ν por cada parámetro estimado**: al estimar (por ejemplo) la media del modelo con la misma muestra, el modelo «se acomoda» a los datos y el ajuste parece mejor de lo que es. Restar ν compensa eso.
- **Completar el dominio**: el modelo asigna probabilidad también a valores que no aparecieron (por ejemplo, la cola de una normal). Esas probabilidades van en clases **nuevas** con O = 0 y probabilidad **acumulada** (F o G), para que las probabilidades sumen 1.

### Qué se concluye

- Rechazar en consistencia: «**alguna** proporción es distinta», no «todas son distintas».
- No rechazar en bondad de ajuste con modelo continuo: «es un **buen candidato**», no «sigue el modelo» (otro podría ajustar mejor). Entre varios que no se rechazan, el mejor es el de **menor χ²obs**.
- No rechazar en independencia: «no hay evidencia de asociación», nunca «son independientes».

---

## 6. Tema VII: regresión simple

### Qué representa cada cosa

| Símbolo | Qué es | Unidad |
|---|---|---|
| **X** | **Variable explicativa** (no «independiente»): la que se fija o se elige. Conviene que no sea aleatoria. | la de X |
| **Y** | **Variable explicada**: la que se mide y es aleatoria. La dirección es única: Y en función de X. | la de Y |
| **β₀** | Valor promedio de Y cuando X no influye (X = 0). Poblacional. | de Y |
| **β₁** | **Coeficiente de regresión** o **contribución marginal**: cuánto cambia **en promedio** Y por cada unidad que aumenta X. | de Y por unidad de X |
| **ε** | **Perturbación del entorno**: todo lo que mueve a Y y no es X. Hace que los puntos no caigan sobre la recta. | de Y |
| **b₀, b₁** | Las estimaciones de β₀ y β₁ con la muestra (mínimos cuadrados: la recta que minimiza la suma de los desvíos verticales al cuadrado). | las mismas |
| **Ŷ = b₀ + b₁x** | Lo que la recta estimada pronostica para un x. | de Y |
| **S²** | Estimación de la varianza de ε: cuánto se dispersan los puntos alrededor de la recta. Usa ν = n − 2. | de Y² |
| **S_b₁** | Error estándar de b₁: cuánto variaría b₁ si se repitiera el estudio con otra muestra. | la de b₁ |
| **ρ** | Coeficiente de correlación poblacional: fuerza y sentido de la relación **lineal**, entre −1 y 1. | sin unidad |
| **r** | Su estimador. Tiene el **signo de b₁**. | sin unidad |
| **r²** | **Influencia porcentual**: qué parte de la variabilidad de Y se explica por X. El resto (1 − r²) es perturbación del entorno u otras variables. | sin unidad |

### Modelo promedio y modelo puntual

- **Modelo promedio**: E(Y | x) = β₀ + β₁x. Es el valor medio de Y para todos los casos con ese x.
- **Modelo puntual**: Y = β₀ + β₁x + ε. Es un caso individual, que además tiene su perturbación.

De ahí salen las dos estimaciones que se confunden:

| Te piden… | Es… | Se estima con… |
|---|---|---|
| «el promedio», «toda la estructura», «en general» | E(Y \| x₀) | **Intervalo de confianza** |
| «un sector», «un acero», «una empresa» | Un valor individual | **Intervalo de predicción** (pronóstico): lleva «1 +» en la raíz, porque suma la variabilidad de ε. Siempre es **más ancho**. |

### Validar antes de usar (siempre, aunque no lo pidan)

Si el modelo no es válido, cualquier pregunta sobre él «no tiene sentido».

1. **Existencia**: H0: ρ = 0 (equivale a β₁ = 0: X no influye en Y). Si no se rechaza, no hay evidencia de relación y se termina ahí.
2. **Fuerza**: r² suficientemente alto según el área (≥ 0,4 sociales; ≥ 0,6 económico; ≥ 0,8 técnico, orientativos).

Son condiciones necesarias, no suficientes: una relación fuerte no prueba causa-efecto.

### Lo que no hay que hacer

- **Extrapolar**: el modelo vale solo en el **entorno observado** (entre el x mínimo y el máximo). Por eso β₀ en general no se estima: X = 0 suele estar fuera del rango, y b₀ se interpreta «en teoría».
- **Interpretar sin unidades**: «por cada mm que aumenta la profundidad, la resistencia disminuye **en promedio** 0,29 MPa».
- **«Lineal» no significa recta en X**: significa lineal en los parámetros. Por eso se pueden usar modelos con logaritmos.

---

## 7. Glosario rápido de letras

| Letra | Qué es | Tema |
|---|---|---|
| α | Probabilidad de rechazar H0 siendo cierta. Se elige. | todos |
| β | Probabilidad de no rechazar H0 siendo falsa, calculada en un valor de H1. | todos (no en medias con t) |
| 1 − β | Potencia: probabilidad de detectar H1 en ese valor. | todos |
| β₀, β₁ | **Otra cosa**: coeficientes de la recta de regresión. No confundir con el β del error. | VII |
| p, p₀, p₁ | Proporción real, la de H0, la que interesa detectar. | III |
| r (en III) | Cantidad de casos en la muestra. | III |
| r (en VII) | Coeficiente de correlación muestral. | VII |
| R (en n de III) | Cociente p₁/p₀ (aproximación Poisson). | III |
| R (en IV) | Relación entre los límites de un IC (B/A). Para desvíos, R = R'². | IV |
| ψ², φ | Cociente de varianzas, cociente de desvíos. | IV |
| J², J | Sus estimadores. | IV |
| Δ, D | Diferencia de medias real y muestral. | V |
| Sa | Desvío amalgamado (común). | V |
| h | Factor porcentual (1,10 = 10 % más). | V |
| O, E | Frecuencias observadas y esperadas. | VI |
| ν | Grados de libertad. | todos |
| P, F, G, Φ | Probabilidad puntual, acumulada izquierda, acumulada derecha, acumulada de la normal estándar. | todos |

---

## 8. Autoevaluación: ¿entendí qué representa cada cosa?

<details><summary>1. ¿Por qué x̄ es una variable aleatoria y μ no?</summary>

μ es una característica fija de la población. x̄ depende de qué elementos cayeron en la muestra: con otra muestra da otro valor. Por eso x̄ tiene distribución y μ no.
</details>

<details><summary>2. Un compañero escribe «se acepta H0, las varianzas son iguales». ¿Qué está mal?</summary>

La igualdad está en H0, y H0 nunca se prueba. Lo correcto: «no hay evidencia suficiente para asegurar que la varianza de A sea mayor que la de B».
</details>

<details><summary>3. Ocho operarios arman una pieza con el método viejo y después con el nuevo. ¿Qué método de comparación de medias es y por qué?</summary>

Apareadas: son los mismos individuos. Se trabaja con la diferencia de cada operario (d), que cancela la habilidad propia de cada uno.
</details>

<details><summary>4. 50 piezas de la máquina A y 50 de la B. ¿Son apareadas?</summary>

No. Que los n sean iguales no importa: son piezas distintas. Son independientes ⇒ test F auxiliar ⇒ amalgamado o Welch.
</details>

<details><summary>5. En un χ², ¿qué representa una E de 12,4 en una celda?</summary>

La cantidad promedio de casos que caerían en esa celda si H0 fuera cierta (por ejemplo, si no hubiera asociación). Por eso puede tener decimales.
</details>

<details><summary>6. «Se encuestó a 300 clientes de cada una de tres sucursales y se registró si están satisfechos.» ¿Consistencia o independencia?</summary>

Consistencia: son tres poblaciones (sucursales) con tamaños fijados por el diseño, y se compara la proporción de satisfechos entre ellas. Sería independencia si se tomara una sola muestra de clientes y se clasificara a cada uno por sucursal y por satisfacción.
</details>

<details><summary>7. En regresión, b₁ = −0,29 MPa/mm y r² = 0,72. Interpretá los dos.</summary>

b₁: por cada mm que aumenta la profundidad, la resistencia disminuye en promedio 0,29 MPa. r²: el 72 % de la variabilidad de la resistencia se explica por la profundidad; el 28 % restante se debe a perturbaciones del entorno u otras variables. (Antes, el modelo tiene que estar validado.)
</details>

<details><summary>8. ¿Por qué el intervalo de predicción es más ancho que el de confianza de E(Y | x₀)?</summary>

Porque además de la incertidumbre de dónde está la recta (la misma que en el IC), un caso individual tiene su propia perturbación ε. El «1 +» de la raíz es esa variabilidad extra.
</details>

<details><summary>9. En el test F auxiliar, ¿por qué se usa α = 0,10 y no el α del problema?</summary>

Porque el error que importa ahí es no detectar que las varianzas son distintas (y amalgamar mal), que es un error de tipo II. Para achicar β, se acepta un α más grande.
</details>

<details><summary>10. En un ensayo de p caso 1, ¿qué representa rc y por qué se compara r con rc y no con p₀?</summary>

rc es la menor cantidad de casos en la muestra que sería demasiado rara si p fuera p₀ (probabilidad ≤ α). p₀ es un valor de la población; r es un conteo de la muestra: no se pueden comparar directamente. Se compara estimador (r) con crítico (rc).
</details>
