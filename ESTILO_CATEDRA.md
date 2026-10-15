# Estilo de resolución de la cátedra (Dopazo – García)

Este archivo es lo que lee la IA para **redactar la resolución como la quiere el profesor** (botón
*📝 Redactar como en el examen* en *Interpretar un enunciado*). Se puede editar libremente: agregar ejemplos,
frases que el profesor exige o correcciones, y la próxima redacción ya las usa. Los **números** nunca salen de
acá: los pone siempre el solver.

Fuente: tutorial metodológico de la cátedra (temas I a IV). Los resultados de los ejemplos se verificaron contra
la Guía de Problemas y con scipy. La sección de los temas V a VIII es **provisoria** hasta tener ejemplos.

## 1. Criterios que no se negocian

- **Definir la variable antes de escribir un número**, en palabras, con su **unidad** y su entorno.
  Ej.: «X: resistencia a la tracción de un hilo de alambre para cuerda de tensión, expresada en toneladas (Tn).»
- Distinguir **parámetros** (población, fijos y desconocidos: μ, σ², σ, p, φ) de **estimadores** (muestra,
  variables aleatorias: x̄, S², S, p̂, j²).
- La **igualdad (=, ≤, ≥) va siempre en H0**.
- **Criterio pesimista / defensivo** (inversión, modificación de proceso, producto nuevo, cambiar de proveedor):
  en H0 va la posición defensiva («el cambio no funciona», «no cumple la especificación»); el error grave es
  implementar un cambio inútil (error de tipo I, α).
- **Criterio optimista** (control de rutina, inspección periódica, sistema de control): en H0 se asume que el
  proceso está calibrado / opera normalmente.
- **Nunca escribir «Acepto H0»**: la muestra no prueba H0. Se escribe «**Se rechaza H0**» o «**No se rechaza H0**»
  (no hay evidencia suficiente).
- **Condición de rechazo (CR)**: la desigualdad que define la zona crítica. Ej.: «CR: si x̄ > 5,1306 piezas/min ⇒
  se rechaza H0».
- **Regla de decisión (RD)**: instrucción operativa en lenguaje llano, para el operario o el responsable, que se
  entienda sin saber estadística. Ej.: «Se tomará una muestra de 40 minutos de producción. Si la productividad
  promedio es superior a 5,1306 piezas/min, se implementa la modificación; de lo contrario, se mantiene el
  sistema actual.»
- **Tamaños de muestra**: siempre al **entero superior**. Si ya había una muestra, informar además cuántas
  unidades **más** hay que tomar (Δn = n_total − n_preliminar).
- **Intervalos**: cerrar con la **expresión formal** P(A ≤ θ ≤ B) = 1 − α y una conclusión en palabras.

## 2. Los 7 pasos de un ensayo de hipótesis (en este orden)

1. **Definir la variable X y los parámetros** en palabras, con unidades.
2. **Formular H0 y H1**, fundamentando el criterio (pesimista u optimista) con el contexto del enunciado.
3. **Fijar el riesgo α** (error de tipo I) antes de mirar la muestra; si corresponde, también β en μ₁.
4. **Tamaño de muestra n y valor crítico** (x̄c, Sc, rc, j²c).
5. **Condición de rechazo (CR) y regla de decisión (RD)**, redactada antes de ver los datos.
6. **Estimador muestral** (x̄, S, p̂, j²obs) calculado con la muestra.
7. **Comparar con el valor crítico y conclusión formal**, que empieza por el nivel de significación: «Con un riesgo
   del 5 % se rechaza H0: se puede asegurar que…» / «… no se rechaza H0: no hay evidencia suficiente para
   asegurar que…».

## 3. Modelos y distribuciones

| Tema | Parámetro | Situación | Distribución | Notas |
|---|---|---|---|---|
| I | media μ | σ conocido | Normal estándar Z | n = (Z·σ/e)² |
| I | media μ | σ desconocido (se usa S) | t de Student, ν = n − 1 | n por método iterativo. Usar Z con S es un error de concepto |
| I | total τ | población finita | — | τ = N·μ; factor de corrección √((N − n)/N) |
| II | varianza σ², desvío σ | una población | Chi-cuadrado, ν = n − 1 | n por la ecuación de García (relación de límites R' = B'/A') |
| III | proporción p | Bernoulli / Binomial | **método exacto (F / Beta)** | |
| IV | φ = σ₁/σ₂ | dos poblaciones independientes | F de Fisher-Snedecor (ν₁, ν₂) | n₁ = n₂ por la ecuación de García |

## 4. Formato por tipo de inciso

**Intervalo de confianza**
1. Definición de la variable (y el modelo, p. ej. X ~ Normal(μ; σ² = 15²)).
2. Datos: parámetros conocidos y estimadores de la muestra.
3. Confianza y fractil: 1 − α = 0,90 ⇒ α/2 = 0,05 ⇒ Z(0,95) = 1,6449.
4. Error muestral y límites A y B, con unidades.
5. Expresión formal P(A ≤ θ ≤ B) = 1 − α.
6. Conclusión: «Se estima con un 90 % de confianza que [el parámetro en palabras] se encuentra entre A y B.»

**Tamaño de muestra**: fórmula con los valores, resultado sin redondear ⇒ entero superior, y Δn si ya había
muestra.

**Ensayo**: los 7 pasos de la sección 2.

**Diseño del ensayo** (todavía no hay muestra): pasos 1 a 5, hasta la condición de rechazo y la regla de decisión.
No hay estimador ni conclusión.

**Probabilidad de error (β) o potencia (1 − β)**: decir qué evento es en palabras («no implementar la
modificación cuando la media real es 4,98»), que es el error de tipo II evaluado en ese valor, la región de
no rechazo, la cuenta y la probabilidad, y una frase que la interprete.

## 5. Ejemplos resueltos

### Ejemplo 1 · Tema I · Intervalo y tamaño de muestra (Guía, Tema I, problema 1)

> «Una máquina llenadora de latas de café dosifica cantidades variables con distribución Normal de desvío
> estándar 15 gramos. A intervalos regulares se toman muestras de 10 envases con el fin de estimar la
> dosificación media. Una de estas muestras arrojó una media de 246 gramos. Estimar la dosificación media con un
> 90 % de confianza y calcular cuántos envases más habría que pesar para reducir el error de muestreo a
> 5 gramos.»

1. **Definición de la variable**: X: cantidad de café dosificada en una lata, expresada en gramos (g).
   X ~ Normal(μ; σ² = 15²).
2. **Datos**: desvío poblacional conocido σ = 15 g; muestra preliminar n = 10 latas; media muestral x̄ = 246 g.
3. **Intervalo de confianza del 90 %**: 1 − α = 0,90 ⇒ α/2 = 0,05 ⇒ Z(0,95) = 1,6449.
   - Error muestral: e = Z(0,95)·σ/√n = 1,6449 · 15/√10 = 7,81 g.
   - Límites: A = 246 − 7,81 = 238,19 g; B = 246 + 7,81 = 253,81 g.
   - **Expresión formal**: P(238,19 g ≤ μ ≤ 253,81 g) = 0,90.
   - **Conclusión**: «Se estima con un 90 % de confianza que la dosificación media real de todas las latas de
     café (μ) se encuentra entre 238,19 g y 253,81 g.»
4. **Tamaño de muestra para e = 5 g**: n = [Z(0,95)·σ/e]² = [1,6449 · 15/5]² = 24,35 ⇒ **25 latas** (entero
   superior). Δn = 25 − 10 = **15 latas más**.

### Ejemplo 2 · Tema I · Diseño del ensayo con α y β (examen: modificación del sistema productivo)

> «… se piensa que el nuevo sistema aumentaría la productividad a un valor promedio de 5,8 piezas por minuto. El
> sistema actual tiene una productividad promedio de 4,2 piezas por minuto con un desvío estándar de 2,53 … una
> probabilidad de 0,95 de modificar el sistema cuando con la modificación se obtiene 5,8 …; el gerente desea la
> certeza del 99 % de no realizar la modificación cuando no se consigue el efecto deseado. Se asume que el desvío
> no se modificará. a) Indicar el tamaño de la muestra y la hipótesis adecuada, la condición de rechazo y la regla
> de decisión.»

1. **Variable**: X: productividad del proceso, expresada en piezas por minuto. σ = 2,53 piezas/min conocido (no
   cambia con la modificación) ⇒ modelo Normal (Z).
2. **Hipótesis** (criterio pesimista: modificar el proceso tiene un costo; solo se hace con evidencia):
   H0: μ ≤ 4,2 (la modificación no aumenta la productividad) · H1: μ > 4,2 (la modificación la aumenta).
3. **Riesgos**: 99 % de certeza de no modificar si no hay efecto ⇒ 1 − α = 0,99 ⇒ α = 0,01. Probabilidad 0,95 de
   modificar si μ = 5,8 ⇒ 1 − β = 0,95 ⇒ β = 0,05 en μ₁ = 5,8.
4. **Tamaño de muestra y valor crítico**: n = [(Z(0,99) + Z(0,95))·σ/(μ₁ − μ₀)]² = 39,43 ⇒ **n = 40**.
   x̄c = 4,2 + 2,3263 · 2,53/√40 = **5,1306 piezas/min**.
5. **CR**: si x̄ > 5,1306 piezas/min ⇒ se rechaza H0.
   **RD**: «Se tomará una muestra de 40 minutos de producción con el sistema modificado. Si la productividad
   promedio supera 5,1306 piezas/min, se implementa la modificación; de lo contrario, se mantiene el sistema
   actual.»

### Ejemplo 3 · Tema III · Intervalo exacto de una proporción (Guía, Tema III, problema 3a)

> «Calcular los límites de confianza del 90 % para la fracción defectuosa, si de un proceso productivo se tomó
> una muestra de 10 unidades en la cual se encontró 1 unidad defectuosa.»

1. **Variable**: atributo de Bernoulli de cada pieza (1 = defectuosa, 0 = buena). Parámetro: p, proporción de
   piezas defectuosas del proceso.
2. **Datos**: n = 10, r = 1 defectuosa, 1 − α = 0,90 ⇒ α/2 = 0,05.
3. **Límite inferior (A)** por la distribución F: ν₁ = 2(10) − 2(1) + 2 = 20, ν₂ = 2(1) = 2; F(0,95; 20; 2) =
   19,4458; A = 1/[1 + (10/1)·19,4458] = **0,0051 (0,51 %)**.
4. **Límite superior (B)**: ν₁ = 2(1) + 2 = 4, ν₂ = 2(10) − 2(1) = 18; F(0,95; 4; 18) = 2,9277;
   B = 1/[1 + 9/(2·2,9277)] = **0,3942 (39,42 %)**.
5. **Expresión formal**: P(0,0051 ≤ p ≤ 0,3942) = 0,90.

### Ejemplo 4 · Tema IV · Ensayo sobre la relación de desvíos (Guía, Tema IV, problema 4)

> «Se quiere verificar si el reacondicionamiento de hiladoras reduce en al menos un 12 % el desvío estándar de la
> producción. Se probaron 4 máquinas reacondicionadas obteniendo S₁ = 132 m y 16 máquinas sin reacondicionar con
> S₂ = 354 m. Ensayar con un 10 % de error.»

1. **Variable**: X: producción de hilado por máquina, expresada en metros (m). Parámetro de comparación:
   φ = σ₁/σ₂ (reacondicionadas / sin reacondicionar).
2. **Hipótesis** (criterio pesimista): reducción del 12 % ⇒ φ₀ = 1 − 0,12 = 0,88 ⇒ φ₀² = 0,7744.
   H0: φ ≥ 0,88 (el reacondicionamiento no reduce la variabilidad en un 12 %) · H1: φ < 0,88 (la reduce en más de
   un 12 %).
3. **Riesgo**: α = 0,10.
4. **Valor crítico**: ν₁ = 4 − 1 = 3, ν₂ = 16 − 1 = 15; F(0,10; 3; 15) = 0,1923;
   j²c = φ₀² · F(0,10; 3; 15) = 0,7744 · 0,1923 = **0,1489**.
5. **CR**: si j²obs < 0,1489 ⇒ se rechaza H0.
6. **Estimador**: j²obs = S₁²/S₂² = 132²/354² = 17.424/125.316 = **0,1390**.
7. **Conclusión**: como 0,1390 < 0,1489 cae en la zona de rechazo. «Con un riesgo del 10 % se rechaza H0: se puede
   asegurar que las máquinas reacondicionadas reducen en más de un 12 % el desvío estándar respecto de las sin
   reacondicionar.»

### Ejemplo 5 · Tema II · Intervalo para el desvío (Guía, Tema II, problema 6)

> «… muestras de 20 ovillos. Una de dichas muestras arrojó un desvío de 15 gramos. Calcular los límites de
> confianza del 95 % para el desvío y determinar qué tamaño de muestra habría que tomar para que el límite superior
> sea un 50 % mayor que el inferior.»

1. **Variable**: X: peso de un ovillo de hilo, expresado en gramos (g).
2. **Datos**: n = 20 ⇒ ν = 19; desvío muestral S = 15 g.
3. **Intervalo del 95 % para σ**: χ²(0,975; 19) = 32,8523 y χ²(0,025; 19) = 8,9065;
   A' = √(19·15²/32,8523) = **11,40 g**; B' = √(19·15²/8,9065) = **21,91 g**.
   **Expresión formal**: P(11,40 g ≤ σ ≤ 21,91 g) = 0,95.
4. **Tamaño de muestra** (B' = 1,5·A', ecuación de García): **n = 49 ovillos** (ν = 48). Los pasos intermedios se
   copian de la resolución del solver.

## 6. Temas V a VIII (provisorio: completar con ejemplos del profesor)

Mientras no haya ejemplos, se aplica la misma estructura:

- **Dos medias (V)**: definir las dos variables (X₁, X₂, con unidades) y δ = μ₁ − μ₂ en palabras (qué población va
  primero). Si los desvíos son muestrales, primero el test F de igualdad de varianzas (con su conclusión) y después
  el ensayo de δ con 7 pasos. Si son apareadas, definir la diferencia D por individuo.
- **Chi-cuadrado (VI)**: H0 en palabras («la preferencia es independiente del sexo» / «los datos se ajustan a una
  distribución …»), tabla de frecuencias observadas y esperadas, grados de libertad, valor crítico, estadístico y
  conclusión formal.
- **Regresión (VII y VIII)**: definir x e y con unidades, la recta estimada ŷ = b₀ + b₁·x con la interpretación
  de b₁ («por cada unidad de x, y aumenta en promedio b₁»), la validación (r, r², ensayo de β₁ = 0) y los
  pronósticos con la expresión formal del intervalo.

## 7. Checklist final

- [ ] ¿Está definida la variable X en palabras y con su **unidad**?
- [ ] ¿La igualdad está en H0?
- [ ] ¿Está justificado el criterio (pesimista u optimista)?
- [ ] ¿Se fijó α antes de mirar la muestra?
- [ ] ¿Están la **CR** y la **RD** en lenguaje llano?
- [ ] ¿No aparece «Acepto H0»?
- [ ] ¿Cada intervalo cierra con P(A ≤ θ ≤ B) = 1 − α?
- [ ] ¿Los tamaños de muestra están al **entero superior** (y con Δn si había muestra)?
