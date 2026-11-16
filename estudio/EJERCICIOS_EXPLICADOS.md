# Ejercicios explicados paso a paso (uno por tema)

Un ejercicio de cada tema del 2° parcial, resuelto con los pasos de la cátedra: **qué se hace, por qué y de dónde sale cada número**. Los enunciados son de los ejercicios nuevos tipo examen (`datos/ejercicios_nuevos*.json`). Sus resultados están verificados dos veces: con scipy por separado y con la app.

**Cómo leer cada ejercicio**

- 🔎 **Cómo se reconoce el tema**: las pistas del enunciado.
- Los pasos son los de la cátedra: Variable → 1. Hipótesis → 2. α → 3. Estadístico → 4. Condición de rechazo (CR) → 5. Regla de decisión (RD) → 6. Cálculos y decisión → 7. Conclusión.
- 📍 **De dónde sale**: el origen de cada número. Es un dato del enunciado, una cuenta o un valor de tabla.
- ⚠️ **Trampa**: lo que suele salir mal, en la app o a mano.

**Valores de tabla.** Se sacan con *Probability Distributions* o con Excel. En Excel en castellano:

| Valor | Excel |
|---|---|
| t(1−α; ν) | `INV.T(1−α; ν)` |
| F(1−α; ν₁; ν₂) | `INV.F(1−α; ν₁; ν₂)` |
| χ²(1−α; ν) | `INV.CHICUAD(1−α; ν)` |
| Binomial acumulada F_b(r) | `DISTR.BINOM.N(r; n; p; VERDADERO)` |
| Binomial G_b(r) = P(R ≥ r) | `1 − DISTR.BINOM.N(r − 1; n; p; VERDADERO)` |
| Poisson puntual | `POISSON.DIST(r; m; FALSO)` |
| Normal acumulada | `DISTR.NORM.N(x; μ; σ; VERDADERO)` |

---

## III · Proporción: ensayo binomial y estimación exacta

> Una cadena de farmacias solo lanzará una línea propia de productos genéricos si más del 30% de sus clientes estaría dispuesto a comprarla. En una encuesta a 150 clientes elegidos al azar, 56 respondieron que la comprarían.
> a) Con un nivel de significación de 0,05, ¿alcanzan los resultados para lanzar la línea?
> b) Con una confianza del 90%, ¿entre qué valores se encuentra la proporción de clientes que NO comprarían la línea?

🔎 **Tema.** Se cuenta cuántos de los encuestados cumplen algo (sí/no): es una proporción. Cada cliente es una prueba de Bernoulli y la cantidad r en n clientes sigue una Binomial.

### a) Ensayo

**Variable.**
- r = cantidad de clientes, en la muestra, que comprarían la línea.
- p = proporción de clientes de la cadena que la comprarían.

**1 · Hipótesis.** H0: p ≤ 0,30 vs H1: p > 0,30.
- *Por qué.* Lanzar la línea es la decisión costosa. Solo se lanza si se **prueba** que p > 0,30, y lo que se quiere probar va en H1.
- Es el **criterio pesimista**: H0 supone lo desfavorable y la decisión se toma solo con evidencia.
- Así, el error grave (lanzar sin que convenga) queda acotado por α.
- El 0,30 es el valor de referencia del enunciado y va con la igualdad, en H0.

**2 · α = 0,05.** α = P(lanzar la línea | p = 0,30), el error de tipo I.

**3 · Estadístico.** r, con r ~ Binomial(n = 150; p₀ = 0,30).
- Se usa la Binomial **exacta**. La normal no se usa en el ensayo sobre p si se puede calcular la exacta.

**4 · CR.** Se rechaza si r ≥ r_c. r_c es el **menor** valor con G_b(r_c) = P(R ≥ r_c | n = 150; p = 0,30) ≤ α.
- G_b(54) = 0,0667 > 0,05: con r_c = 54 el riesgo real pasaría del 5%.
- G_b(55) = 0,0471 ≤ 0,05 ⇒ **r_c = 55**.
- 📍 G_b(55) = 1 − `DISTR.BINOM.N(54; 150; 0,3; VERDADERO)`. Se prueban valores alrededor de n·p₀ = 45, hacia arriba.
- 📍 α real = 0,0471: nunca puede pasar del α pedido.

**5 · RD.** Se encuesta a 150 clientes. Si 55 o más dicen que la comprarían, se rechaza H0 y se lanza la línea; si no, no se lanza.

**6 · Cálculo y decisión.** r = 56 (dato) ≥ 55 ⇒ se rechaza H0.

**7 · Conclusión.** Con α = 0,05 se puede asegurar que más del 30% de los clientes compraría la línea: corresponde lanzarla.

⚠️ **Trampas**

- La decisión se toma con **r contra r_c**, decidido antes de mirar la muestra. El p-valor (α* = 0,0325) es solo informativo: el profesor no decide con él.
- El ejercicio está justo en el límite (56 contra 55). Un r_c mal calculado cambia la respuesta.

### b) Estimación exacta del complemento

**Qué se estima.** Lo que se pide es la proporción de los que **NO** comprarían, así que r cambia: **r = 150 − 56 = 94**, y p̂ = 94/150 = 0,6267.

**Modelo.** Intervalo exacto, por la relación Binomial–F (o Beta). El profesor no acepta la normal para estimar p: la llama «aberración».

**Límite inferior.** A = 1 / [1 + ((n − r + 1)/r)·F(1 − α/2; 2(n − r + 1); 2r)]
- 📍 α = 0,10, porque la confianza es del 90%. Entonces 1 − α/2 = 0,95.
- 📍 Grados de libertad: 2(n − r + 1) = 2·57 = 114 y 2r = 188.
- F(0,95; 114; 188) = 1,3121.
- A = 1/[1 + (57/94)·1,3121] = **0,5569**.

**Límite superior.** B = 1 / [1 + (n − r)/((r + 1)·F(1 − α/2; 2(r + 1); 2(n − r)))]
- 📍 Grados de libertad: 2(r + 1) = 190 y 2(n − r) = 112.
- F(0,95; 190; 112) = 1,3283.
- B = 1/[1 + 56/(95·1,3283)] = **0,6926**.

**Conclusión.** P(0,5568 ≤ p ≤ 0,6927) = 0,90. Entre el 55,68% y el 69,27% de los clientes no compraría la línea.

📍 Los límites se redondean **hacia afuera**: A hacia abajo y B hacia arriba, para no achicar el intervalo.
📍 Control con Excel: A = `INV.BETA.N(0,05; 94; 57)` y B = `INV.BETA.N(0,95; 95; 56)`.

⚠️ **Trampa.** Usar r = 56 en b). El inciso pide el complemento.

---

## III · Diseño del plan de muestreo (n y r_c con α y β)

> Históricamente, el 20% de los clientes de una financiera paga la cuota con atraso. Se va a probar un sistema de recordatorios y se quiere verificar si logra bajar ese porcentaje. Se acepta un riesgo de 0,05 de dar por efectivo el sistema cuando en realidad el porcentaje sigue en el 20%, y se quiere una probabilidad de 0,90 de detectar la mejora si el porcentaje bajara al 10%.
> a) Plantear las hipótesis, determinar el tamaño de la muestra, la condición de rechazo y la regla de decisión.
> b) Si con el sistema el porcentaje bajara al 15%, ¿qué probabilidad hay de que el plan no lo detecte?

🔎 **Tema.** El enunciado da **dos probabilidades**, una para cada valor de p. Es un diseño: no hay muestra todavía y se pide n.

### a)

**Qué es cada número**

| Número | Qué es | Por qué |
|---|---|---|
| 20% | **p₀**, el valor de referencia | Es lo que pasa si el sistema no sirve. |
| 10% | **p₁**, el valor alternativo | Es el «si bajara al 10%». |
| 0,05 | **α** | Riesgo de decir que funciona cuando p sigue en 0,20: rechazar H0 siendo cierta. |
| 0,90 | Potencia 1 − β ⇒ **β = 0,10** | Es la probabilidad de *detectar* la mejora (acertar). β es la de *no* detectarla. |

⚠️ El «20%» aparece dos veces («sigue en el 20%»). Es p₀, no un riesgo.

**Hipótesis.** H0: p ≥ 0,20 vs H1: p < 0,20.
- *Por qué.* Se quiere probar que el sistema **baja** el porcentaje, y eso va en H1.
- Además p₁ = 0,10 < p₀, y la alternativa siempre está del lado de H1: el ensayo es a la izquierda. Se rechaza si salen **pocos** atrasados, r ≤ r_c.

**Condiciones del plan**
- P(R ≤ r_c | n; p = 0,20) ≤ α = 0,05.
- P(R > r_c | n; p = 0,10) ≤ β = 0,10.

**Cálculo.** Se itera n desde abajo. Para cada n:
1. r_c es el **mayor** valor con F_b(r_c | n; 0,20) ≤ 0,05.
2. Se controla β con p₁.

El primer n que cumple las dos condiciones es **n = 112, r_c = 15**:
- 📍 α real = F_b(15 | 112; 0,20) = 0,0467 ≤ 0,05.
- 📍 β real = P(R ≥ 16 | 112; 0,10) = 0,0922 ≤ 0,10.

**RD.** Se revisan 112 clientes con el sistema nuevo. Si 15 o menos pagan con atraso, se rechaza H0: el sistema baja el porcentaje.

📍 **Aproximación normal.**
- n = [(Z(1−α)·√(p₀q₀) + Z(1−β)·√(p₁q₁)) / (p₁ − p₀)]² = [(1,6449·0,4 + 1,2816·0,3)/0,1]² = 108,66 ⇒ n = 109.
- La app la muestra como alternativa. El exacto es el que manda.

### b) β en otro valor de p

β(0,15) = P(no rechazar | p = 0,15) = P(R ≥ 16 | n = 112; p = 0,15) = **0,624**.
- 📍 Se calcula con el plan del inciso a): n = 112, r_c = 15.
- Un plan diseñado para detectar 0,10 detecta mal una mejora más chica (0,15): falla el 62,4% de las veces.

⚠️ **Trampa.** «Que **no** lo detecte» es β; «que lo detecte» sería la potencia 1 − β = 0,376.

---

## IV · Comparación de dos varianzas (test F)

> Se midió el espesor (en micrones) de 16 rollos del proveedor Norte, con un desvío estándar de 2,8 micrones, y de 21 rollos del proveedor Sur, con un desvío estándar de 1,9 micrones. Compras solo pasará a trabajar con el proveedor Sur si se demuestra que su espesor es más regular que el del proveedor Norte.
> a) Con un riesgo del 5%, ¿qué decisión debería tomar Compras?
> b) Estimar, con un nivel de confianza del 95%, el cociente entre la varianza del espesor del proveedor Norte y la del proveedor Sur.

🔎 **Tema.** «Más regular» significa con **menos variabilidad**. Se comparan los desvíos de dos poblaciones independientes: test F.

### a)

**Variable.** X₁ = espesor de un rollo del proveedor Norte; X₂ = espesor de un rollo del Sur (en micrones). Se suponen Normales e independientes: es un supuesto **necesario**, porque la F no es robusta.

**1 · Hipótesis.** H0: φ = σ(Norte)/σ(Sur) ≤ 1 vs H1: φ > 1.
- *Por qué.* El enunciado dice qué hay que **demostrar**: que el Sur es más regular, o sea σ(Sur) < σ(Norte). Lo que se demuestra va en H1.
- Se pone arriba el que se sospecha **mayor** (Norte), así el ensayo queda a la derecha.

**2 · α = 0,05.**

**3 · Estadístico.** j² = S²(Norte)/S²(Sur). Bajo H0, j²/φ₀² ~ F(ν₁ = 16 − 1 = 15; ν₂ = 21 − 1 = 20).
- 📍 Numerador: los grados de libertad de la muestra de arriba.

**4 · CR.** j²_c = φ₀²·F(0,95; 15; 20) = 1·2,2033 = 2,2033, o en desvíos J_c = √2,2033 = 1,4843.

**5 · RD.** Si J = S(Norte)/S(Sur) > 1,4843, se rechaza H0 y Compras pasa al proveedor Sur.

**6 · Cálculo.** J = 2,8/1,9 = 1,4737 (J² = 2,1717). 1,4737 < 1,4843 ⇒ **no se rechaza H0**, por muy poco.

**7 · Conclusión.** Con α = 0,05 no hay evidencia suficiente de que el espesor del Sur sea más regular: Compras no debería cambiar de proveedor. No rechazar H0 no prueba que sean iguales.

### b) Intervalo del cociente de varianzas

**IC.** IC(σ²N/σ²S) = [ j²/F(1 − α/2; 15; 20) ; j²/F(α/2; 15; 20) ]
- 📍 F(0,975; 15; 20) = 2,5731.
- 📍 F(0,025; 15; 20) = 1/F(0,975; 20; 15) = 0,3629: se **invierten** los grados de libertad.
- Límites: 2,1717/2,5731 = **0,8440** y 2,1717/0,3629 = **5,9851**.

**Conclusión.** P(0,8440 ≤ σ²N/σ²S ≤ 5,9852) = 0,95.
- El intervalo contiene el 1, coherente con no haber rechazado.
- Si pidieran el cociente de **desvíos**, se saca la raíz de cada límite: [0,9187 ; 2,4464].

⚠️ **Trampas**

- La F es asimétrica: el intervalo **no** es «j² ± algo».
- «Más regular» es el desvío más chico. Confundirlo invierte H1.

---

## V · Comparación de dos medias independientes, con porcentaje

> Las lámparas LED de la marca Y, que la empresa usa hoy, duraron en promedio 1.050 horas, con un desvío de 95 horas, en un ensayo con 35 lámparas. En las mismas condiciones, 40 lámparas de la marca X duraron en promedio 1.250 horas con un desvío de 110 horas. El proveedor de la marca X asegura que sus lámparas duran más de un 15% más que las de la marca Y.
> a) Con un nivel de significación del 1%, ¿puede aceptarse lo que asegura el proveedor?
> b) Con un 99% de confianza, ¿en qué porcentaje mínimo supera la duración media de la marca X a la de la marca Y?

🔎 **Tema.**
- Dos marcas y dos muestras distintas: medias independientes.
- «Más de un 15% más» es una diferencia **porcentual**: se trabaja con h = 1,15.

### a)

**1 · Hipótesis.** H0: μX ≤ 1,15·μY vs H1: μX > 1,15·μY.
- Equivale a δ* = μX − 1,15·μY y H0: δ* ≤ 0.
- *Por qué.* Lo que asegura el proveedor es lo que hay que probar, y va en H1.
- El 1,15 multiplica a la marca de **referencia** (Y), porque el «15% más» es respecto de Y.

**2 · α = 0,01.**

**3 · Estadístico.** Primero hay que elegir el método, porque los σ son desconocidos.

**Test F auxiliar** (previo, no es parte de lo que se pregunta):
- S(X) = 110 > S(Y) = 95, así que lo único que se puede sospechar es σX > σY. Es unilateral: H0: σX ≤ σY.
- Usa un **α propio y grande, 0,10**, no el del problema. La idea es poder suponer los desvíos iguales solo si no hay ninguna evidencia en contra.
- J = 110/95 = 1,1579 contra J_c = √F(0,90; 39; 34) = √1,5442 = 1,2427. 📍 Grados de libertad: 40 − 1 = 39 arriba y 35 − 1 = 34 abajo.
- 1,1579 ≤ 1,2427 ⇒ no se rechaza ⇒ los desvíos se suponen **iguales** y se **amalgaman**.

**Desvío amalgamado.** Sa = √[((n₁−1)S₁² + (n₂−1)S₂²)/(n₁+n₂−2)] = √[(39·110² + 34·95²)/73] = 103,2851, con ν = 40 + 35 − 2 = 73.
- 📍 Control: Sa queda entre 95 y 110.

**Estimador.** d* = x̄X − 1,15·x̄Y = 1.250 − 1,15·1.050 = 42,5 horas.

**Su desvío.** σ(d*) = Sa·√(1/nX + h²/nY) = 103,2851·√(1/40 + 1,15²/35) = 25,8802.
- 📍 h² va **en el término de la marca que lleva el h** (Y).

**4 · CR.** d*_c = 0 + t(0,99; 73)·25,8802 = 2,3785·25,8802 = **61,5567 horas**.

**5 · RD.** Si d* > 61,5567, se rechaza H0 y se acepta lo que asegura el proveedor.

**6 · Cálculo.** d* = 42,5 < 61,5567 ⇒ **no se rechaza H0**.

**7 · Conclusión.** Con α = 0,01 no hay evidencia suficiente para aceptar que la marca X dure más de un 15% más que la Y.

### b) Porcentaje mínimo garantizado

Se busca el h que deja la condición de rechazo **justo en el límite**: x̄X − h·x̄Y = t(0,99; 73)·Sa·√(1/40 + h²/35).

**Cuadrática.** Se eleva al cuadrado y queda a·h² + b·h + c = 0, con q = 2,3785, c₁ = Sa²/40 = 266,6952 y c₂ = Sa²/35 = 304,7945:
- a = x̄Y² − q²·c₂ = 1.100.775,67
- b = −2·x̄X·x̄Y = −2.625.000
- c = x̄X² − q²·c₁ = 1.560.991,21

**Raíces y verificación.** Las raíces son h = 1,1324 y h = 1,2523. Hay que **verificar cada una** en la ecuación original, sin elevar al cuadrado:
- h = 1,1324: el lado izquierdo da +60,99, positivo como el derecho. **Sirve.**
- h = 1,2523: el lado izquierdo da −64,91, negativo. **No sirve**: es una raíz falsa que aparece al elevar al cuadrado.

**Conclusión.** Con un 99% de confianza, la duración media de X es como mínimo un **13,24%** mayor que la de Y (h = 1,1324). Es menos del 15% que asegura el proveedor, coherente con a).

⚠️ **Trampas**

- El test F auxiliar va con α = 0,10, no con el del problema.
- El h² va del lado de la marca de referencia.
- Siempre se verifican las dos raíces.
- No hay ensayos bilaterales en comparaciones (regla del profesor).

---

## V · Comparación de medias apareadas

> Para evaluar un curso de capacitación, se registró el tiempo (en minutos) que tardan los mismos ocho operarios en armar un tablero antes y después de hacer el curso:
> Antes: 12,4 - 10,8 - 13,1 - 11,6 - 12,9 - 14,2 - 11,1 - 12,7
> Después: 10,9 - 10,1 - 11,2 - 10,4 - 11,5 - 12,3 - 10,6 - 11,0
> a) ¿Hay evidencia, al 5%, de que el curso reduce el tiempo medio de armado en más de 1 minuto?
> b) ¿Cuál es la reducción mínima del tiempo medio que se puede garantizar con un 95% de confianza?

🔎 **Tema.** Son **los mismos** operarios antes y después: cada dato de «Antes» tiene su pareja en «Después». Es apareadas, no independientes.

*Por qué importa.* Cada operario tiene su propia velocidad. Restando dentro de cada par se elimina esa diferencia entre personas y queda solo el efecto del curso.

### a)

**Variable.** dᵢ = tiempo antes − tiempo después del operario i, en minutos: lo que bajó su tiempo.

**Procesar los datos**
- dᵢ = 1,5; 0,7; 1,9; 1,2; 1,4; 1,9; 0,5; 1,7.
- d̄ = Σdᵢ/n = 10,8/8 = **1,35 min**.
- S_d = √[Σ(dᵢ − d̄)²/(n − 1)] = **0,5237 min**.
- n = 8 pares ⇒ ν = 7.

**1 · Hipótesis.** H0: δ = μ(Antes) − μ(Después) ≤ 1 vs H1: δ > 1.
- *Por qué.* «Reduce en más de 1 minuto» es lo que hay que probar.
- Se escribe en positivo (antes − después > 1), no como «después − antes < −1»: es lo mismo, pero se lee mejor.

**2 · α = 0,05.**

**3 · Estadístico.** d̄, con (d̄ − δ₀)/(S_d/√n) ~ t(ν = 7), porque σ_d es desconocido.

**4 · CR.** d_c = δ₀ + t(0,95; 7)·S_d/√n = 1 + 1,8946·0,5237/√8 = 1 + 1,8946·0,1852 = **1,3508 min**.

**5 · RD.** Si d̄ > 1,3508, se rechaza H0: el curso reduce el tiempo en más de 1 minuto.

**6 · Cálculo.** d̄ = 1,35 < 1,3508 ⇒ **no se rechaza H0**, por una diezmilésima.

**7 · Conclusión.** Con α = 0,05 no hay evidencia suficiente para asegurar que el curso reduzca el tiempo medio en más de 1 minuto.

### b) Reducción mínima garantizada

Es un **solo límite**, el inferior, y se calcula con t(1 − α), no con t(1 − α/2):

A = d̄ − t(0,95; 7)·S_d/√n = 1,35 − 0,3508 = 0,99919 ⇒ **0,9991 min**, redondeado hacia abajo.

**Conclusión.** P(μ(Antes) − μ(Después) ≥ 0,9991) = 0,95: el curso reduce el tiempo medio por lo menos 0,9991 minutos.
- Es coherente con a): la reducción garantizada no llega a 1 minuto.

⚠️ **Trampa.** Tratarlo como dos muestras independientes, con Sa y ν = 14. Eso usa un desvío mucho mayor y responde otra pregunta.

---

## VI · χ² de bondad de ajuste (Poisson)

> En una central de emergencias se contó la cantidad de llamadas recibidas en 100 intervalos de un minuto elegidos al azar:
>
> | Llamadas por minuto | 0 | 1 | 2 | 3 | 4 | 5 o más |
> |---|---|---|---|---|---|---|
> | Cantidad de intervalos | 18 | 34 | 30 | 12 | 4 | 2 |
>
> ¿Es razonable suponer que la cantidad de llamadas por minuto se distribuye según la ley de Poisson? Tomar α = 0,05.

🔎 **Tema.** Pregunta si los datos **siguen un modelo** teórico: es bondad de ajuste.

**Variable.** X = cantidad de llamadas recibidas en un minuto.

**Estimar el parámetro con la muestra.** m = x̄ = Σxᵢ·Foᵢ/N = (0·18 + 1·34 + 2·30 + 3·12 + 4·4 + 5·2)/100 = 156/100 = **1,56 llamadas por minuto**.
- 📍 La clase «5 o más» entra con 5 para la media, el mínimo de la clase.
- Por cada parámetro estimado con la muestra se pierde un grado de libertad.

**1 · Hipótesis.** H0: la cantidad de llamadas por minuto se ajusta a un modelo Poisson vs H1: no lo sigue.

**2 · α = 0,05.**

**Frecuencias esperadas.** Feᵢ = N·P(X = xᵢ), con P(r) = e^(−m)·m^r/r!.
- Por ejemplo, P(0) = e^(−1,56) = 0,2101, así que Fe = 100·0,2101 = 21,01.
- La última clase está **abierta** («5 o más»). Se le asigna la probabilidad **acumulada** G(5) = P(X ≥ 5), no la puntual: el modelo tiene que cubrir todo su dominio.

**Amalgamado.** Las clases con Fe < 5 se juntan con la vecina:

| Clase | Fo | Fe | (Fo − Fe)²/Fe |
|---|---|---|---|
| 0 | 18 | 21,0136 | 0,4322 |
| 1 | 34 | 32,7812 | 0,0453 |
| 2 | 30 | 25,5694 | 0,7677 |
| 3 | 12 | 13,2961 | 0,1263 |
| 4 o más | 6 | 7,3397 | 0,2445 |
| **Total** | **100** | **100** | **χ² = 1,6161** |

- 📍 «5 o más» tiene Fe = 2,15 < 5: se suma a la clase 4, y queda Fe = 5,19 + 2,15 = 7,34.
- 📍 Los Fo no se tocan. Los Fe llevan decimales y tienen que sumar N.

**3 · Estadístico.** χ² = Σ(Fo − Fe)²/Fe = 1,6161. Grados de libertad: ν = clases efectivas − 1 − parámetros estimados = 5 − 1 − 1 = **3**.

**4 · CR.** χ²(0,95; 3) = 7,8147. Siempre es la cola derecha: se rechaza si χ² > 7,8147.

**Controles**
- N = 100 ≥ 60, y todos los Fe ≥ 5 después de amalgamar.
- **Ajuste demasiado perfecto**: χ² = 1,6161 > χ²(0,05; 3) = 0,3518, así que no hay sospecha de datos «cocinados».

**6 · Decisión.** 1,6161 < 7,8147 ⇒ no se rechaza H0.

**7 · Conclusión.** No se rechaza el modelo. Además, las llamadas son sucesos puntuales en el tiempo, independientes y con una tasa media constante: se cumple el **proceso físico de Poisson**. Por eso se puede decir que la cantidad de llamadas por minuto **sigue** un modelo Poisson con m = 1,56.
- En un modelo continuo, o si no se cumple el proceso físico, se dice «es un **buen candidato**», nunca «sigue».

⚠️ **Trampas**

- Dar la probabilidad puntual P(5) en la clase abierta.
- Olvidarse de restar el parámetro estimado en ν.
- Amalgamar los Fo con un criterio distinto al de los Fe: se amalgaman los dos juntos.

---

## VI · χ² de independencia (tabla de contingencia)

> Una empresa encuestó a 230 empleados sobre su conformidad con el nuevo sistema de turnos rotativos y registró el turno en el que trabaja cada uno:
>
> | Turno | Conforme | Indiferente | Disconforme |
> |---|---|---|---|
> | Mañana | 38 | 22 | 15 |
> | Tarde | 30 | 28 | 22 |
> | Noche | 17 | 25 | 33 |
>
> ¿Depende el grado de conformidad del turno en el que se trabaja? Usar un riesgo del 5%.

🔎 **Tema.** Cada empleado se clasifica de **dos formas** (turno y conformidad) y se pregunta si una **depende** de la otra: es independencia χ².
- Si cada turno fuera una muestra de tamaño fijado y se preguntara si los porcentajes son los mismos, sería **consistencia** (homogeneidad). La cuenta es la misma; cambia cómo se escribe H0.

**1 · Hipótesis.** H0: la conformidad es independiente del turno vs H1: hay asociación entre las dos.
- H0 equivale a que, para cada categoría de conformidad, la proporción es la misma en los tres turnos.

**2 · α = 0,05.**

**Esperados bajo H0.** Eᵢⱼ = (total de la fila i · total de la columna j)/N.
- Por ejemplo, E(Mañana; Conforme) = 75·85/230 = 27,7174.
- 📍 Totales: Mañana 75, Tarde 80, Noche 75; Conforme 85, Indiferente 75, Disconforme 70; N = 230.

| Esperados | Conforme | Indiferente | Disconforme |
|---|---|---|---|
| Mañana | 27,7174 | 24,4565 | 22,8261 |
| Tarde | 29,5652 | 26,0870 | 24,3478 |
| Noche | 27,7174 | 24,4565 | 22,8261 |

**3 · Estadístico.** χ² = Σ(O − E)²/E. Por ejemplo, la celda Mañana–Conforme aporta (38 − 27,7174)²/27,7174 = 3,8146. Sumando las 9 celdas, **χ² = 15,8085**.
- ν = (filas − 1)(columnas − 1) = 2·2 = **4**.
- Condiciones: N ≥ 60, y el menor esperado es 22,83 ≥ 5.

**4 · CR.** χ²(0,95; 4) = 9,4877. Se rechaza si χ² > 9,4877.

**6 · Decisión.** 15,8085 > 9,4877 ⇒ **se rechaza H0**.

**7 · Conclusión.** Con α = 0,05 se puede asegurar que el grado de conformidad depende del turno.
- Los aportes más grandes dicen dónde está la diferencia: Noche–Disconforme (4,53), Noche–Conforme (4,14) y Mañana–Conforme (3,81). En el turno noche hay más disconformes y menos conformes de lo esperado.

⚠️ **Trampa.** Escribir H0 como «p(mañana) = p(tarde) = p(noche)» sin decir de qué categoría. El profesor pide la igualdad **por categoría**, o la independencia en palabras.

---

## VII · Regresión lineal simple

> Un ingeniero de producción sospecha que la velocidad de corte (en m/min) influye en el desgaste del filo de la herramienta (en mm) al cabo de una jornada:
>
> | Velocidad (m/min) | 120 | 140 | 160 | 180 | 200 | 220 | 240 | 260 |
> |---|---|---|---|---|---|---|---|---|
> | Desgaste (mm) | 0,21 | 0,26 | 0,30 | 0,37 | 0,40 | 0,47 | 0,50 | 0,58 |
>
> a) Ajustar el modelo lineal, interpretar los coeficientes en términos del problema y decidir si el modelo es válido.
> b) Si mañana se trabaja una jornada a 210 m/min, ¿entre qué valores se espera el desgaste de esa herramienta? (95%)
> c) ¿Se puede afirmar, al 5%, que por cada m/min adicional el desgaste aumenta en más de 0,0015 mm?

🔎 **Tema.** Hay dos variables medidas sobre las mismas jornadas y se pregunta cómo **influye** una en la otra: regresión.

### a)

**Variables**
- Y = desgaste del filo, en mm: la variable explicada (aleatoria).
- X = velocidad de corte, en m/min: la explicativa.

**Procesar los datos**
- n = 8; Σx = 1.520 ⇒ x̄ = 190.
- Σy = 3,09 ⇒ ȳ = 0,38625.
- Σx² = 305.600; Σy² = 1,3059; Σxy = 630,4.

**Sumas de cuadrados**
- Sxy = Σxy − n·x̄·ȳ = 630,4 − 8·190·0,38625 = 43,3.
- Sxx = Σx² − n·x̄² = 305.600 − 8·190² = 16.800.
- Syy = Σy² − n·ȳ² = 0,1124.

**Estimadores**
- b1 = Sxy/Sxx = 43,3/16.800 = **0,002577 mm por m/min**.
- b0 = ȳ − b1·x̄ = 0,38625 − 0,002577·190 = **−0,1035 mm**.
- Recta: **ŷ = −0,1035 + 0,002577·x**.

**Interpretación en términos del problema**
- **b1**: por cada m/min más de velocidad, el desgaste aumenta en promedio 0,002577 mm. Es la contribución marginal.
- **b0**: sería el desgaste a velocidad 0. Pero x = 0 queda **fuera del rango observado** (120 a 260 m/min), así que no se interpreta ni se estima β0. El modelo solo vale en el entorno observado.

**Ajuste**
- S² = (Σy² − b0·Σy − b1·Σxy)/(n − 2) = 0,000131, así que S = 0,011452.
- Sb1 = S/√Sxx = 0,011452/√16.800 = 0,00008835.
- r = Sxy/√(Sxx·Syy) = 0,9965, y r² = **0,9930**.

**Validación del modelo, en dos partes**

1. **Existencia de la relación.** H0: β1 = 0 (no hay relación lineal) vs H1: β1 ≠ 0.
   - t_obs = b1/Sb1 = 0,002577/0,00008835 = 29,17.
   - Se compara con t(1 − α; n − 2) = t(0,95; 6) = 1,9432, que es como lo hace la cátedra.
   - |29,17| > 1,9432 ⇒ existe relación lineal.
2. **Fuerza de la relación.** r² = 0,993: la velocidad explica el 99,3% de la variabilidad del desgaste.
   - El mínimo orientativo depende del uso: 0,8 técnico o industrial; 0,6 económico; 0,4 sociología o psicología.
   - Este es un problema técnico y 0,993 ≥ 0,8 ⇒ **el modelo se valida**, solo para el entorno observado.

### b) Una jornada: intervalo de predicción, individual

Es **una** jornada, no el promedio de muchas, así que va el «1 +» dentro de la raíz:

ŷ₀ ± t(1 − α/2; n − 2)·S·√(1 + 1/n + (x₀ − x̄)²/Sxx)

- 📍 ŷ₀ = −0,1035 + 0,002577·210 = 0,4378 mm.
- 📍 t(0,975; 6) = 2,4469.
- 📍 Error = 2,4469·0,011452·√(1 + 1/8 + (210 − 190)²/16.800) = 0,0300.

**Conclusión.** P(0,4077 ≤ y(210) ≤ 0,4679) = 0,95, con los límites redondeados hacia afuera.
- Si preguntaran el desgaste **medio** de las jornadas a 210 m/min, se saca el «1 +» y el intervalo queda más angosto.

### c) Ensayo de la pendiente contra un valor

**1 · Hipótesis.** H0: β1 ≤ 0,0015 vs H1: β1 > 0,0015.
- *Por qué.* «Aumenta en más de 0,0015» es lo que hay que afirmar, y va en H1.

**4 · CR.** b1c = β1₀ + t(1 − α; n − 2)·Sb1 = 0,0015 + 1,9432·0,00008835 = **0,001672**. Es un solo lado, así que va t(0,95; 6).

**6 · Decisión.** b1 = 0,002577 > 0,001672 ⇒ **se rechaza H0**.

**7 · Conclusión.** Con α = 0,05 se puede afirmar que por cada m/min adicional el desgaste aumenta en más de 0,0015 mm.

⚠️ **Trampas**

- Interpretar b0 fuera del rango de x.
- Usar el intervalo de la media cuando se pregunta por **una** jornada, o al revés.
- Juzgar r² con el mínimo de otro tipo de problema (el examen R tenía r² = 0,76 en un problema técnico: no se valida).
- Redondear b1 a 0,0026: las cuentas dejan de cerrar. Una pendiente chica se escribe con 4 cifras significativas.
