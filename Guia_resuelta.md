# Guía de Problemas de Estadística Aplicada 2026 — resuelta

Generado con `python herramientas/generar_resueltos.py` a partir de `datos/guia_ejercicios.json` (transcripción verificada contra el PDF) y el intérprete + solver de la app. Cada inciso muestra los pasos en el orden de la cátedra, la conclusión, la respuesta de la guía y si coinciden.

**Resumen:** ✅ 303 incisos coinciden · ⚠️ 4 no coinciden · ℹ️ 18 sin valores para comparar.

Índice: [Tema I](#tema-i--inferencia-para-medias) · [Tema II](#tema-ii--inferencia-sobre-varianzas--desvíos) · [Tema III](#tema-iii--procesos-de-bernoulli-proporciones) · [Tema IV](#tema-iv--comparación-de-varianzas) · [Tema V](#tema-v--comparación-de-dos-medias) · [Tema VI](#tema-vi--contrastes-chi-cuadrado) · [Tema VII](#tema-vii--regresión-y-correlación-simple) · [Tema VIII](#tema-viii--modelo-lineal-general)

## TEMA I — Inferencia para medias

### I-1 · Problema 1 (pág. 1)

**Enunciado.** Una máquina llenadora de latas de café dosifica cantidades variables con distribución Normal de desvío estándar 15 gramos. A intervalos regulares se toman muestras de 10 envases con el fin de estimar la dosificación media. Una de estas muestras arrojó una media de 246 gramos.

- **a)** Estimar la dosificación media con un 90% de confianza.
- **b)** ¿Cuántos envases más habría que pesar para poder obtener una estimación cuyo error de muestreo sea de 5 gramos?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 90% de confianza mediante un intervalo de confianza. Como σ es conocido se usa Z.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α/2) = Z(0,95) = 1,6449.
- **Límites**: A;B = x̄ ∓ Z·σ/√n = 246 ∓ 1,6449·15/√10 = 246 ∓ 7,8022.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 238,19 y 253,81, afirmándolo con un 90% de confianza, o sea: P(238,19 ≤ μ ≤ 253,81) = 0,9 (límites redondeados hacia afuera; sin redondear: 238,197774 y 253,802226).

**Respuesta de la guía:** Entre 238,19 y 253,81 gramos.

#### b) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para un error máximo e = 5. Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n.
- **Fórmula** (σ conocido): n = (Z·σ/e)² = (1,6449·15/5)² = 24,3499 → se redondea hacia arriba.

**Conclusión:** El tamaño de muestra necesario es n = 25. Como ya se tomaron 10, hay que agregar Δn = 25 - 10 = 15 unidades más.

**Respuesta de la guía:** 15 envases más.

> 📝 *Notas de la transcripción:* a) Con Z=1,6449 el cálculo da 246 ± 7,80 → 238,20 y 253,80; la guía informa 238,19 y 253,81 (diferencia de redondeo).

---

### I-2 · Problema 2 (pág. 1)

**Enunciado.** Una empresa dedicada a la fabricación de envases de vidrio, cuenta con un plantel numeroso de operarios, y desea estimar el tiempo medio de tardanza de los mismos. El estudio se realizará sobre la base de las tarjetas horarias, estableciendo que: El máximo error muestral admitido debe ser de 2 minutos; el nivel de confianza debe ser del 99%, y, el desvío estándar poblacional es de 5 minutos (conocido por ensayos anteriores).

- **a)** Calcular el tamaño adecuado de muestra.
- **b)** Se ha tomado la muestra y se obtuvo que la tardanza media, de la muestra, fue de 15 minutos; estimar la tardanza media de todo el personal.

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra (completá el error e o la reducción pedida).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n.
- **Fórmula** (σ conocido): n = (Z·σ/e)² = (2,5758·5/2)² = 41,4681 → se redondea hacia arriba.

**Conclusión:** El tamaño de muestra necesario es n = 42. (Sin redondear, la fórmula da 41,4681.)

**Respuesta de la guía:** 42 tarjetas.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 99% de confianza mediante un intervalo de confianza. Como σ es conocido se usa Z.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α/2) = Z(0,995) = 2,5758.
- **Límites**: A;B = x̄ ∓ Z·σ/√n = 15 ∓ 2,5758·5/√42 = 15 ∓ 1,9873.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 13,01 y 16,99, afirmándolo con un 99% de confianza, o sea: P(13,01 ≤ μ ≤ 16,99) = 0,99 (límites redondeados hacia afuera; sin redondear: 13,012705 y 16,987295).

**Respuesta de la guía:** Entre 13,01 y 16,99 minutos.

---

### I-3 · Problema 3 (pág. 1)

**Enunciado.** En una zona de Capital Federal se realizará un muestreo sobre una población compuesta por negocios minoristas, con el objeto de estimar el número medio de empleados por establecimiento. La experiencia en encuestas por muestreo indica que el desvío estándar es de 1,2 empleados por establecimiento. Se han obtenido los siguientes resultados muestrales: Cantidad de empleados | Número de establecimientos: 0 | 2; 1 | 4; 2 | 5; 3 | 6; 4 | 4; 5 | 2.

- **a)** ¿El tamaño de muestra extraído es correcto si se pretende un error muestral de ± 0,5 empleados, y un nivel de confianza en la estimación del 95%?
- **b)** Estimar el número medio de empleados para todos los negocios minoristas.
- **c)** Ídem a) y b) considerando que el desvío histórico no se conoce.

| Cantidad de empleados | Número de establecimientos |
|---|---|
| 0 | 2 |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |
| 4 | 4 |
| 5 | 2 |

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para un error máximo e = 0,5.

- **Procesar la muestra**: n = 23, x̄ = Σxᵢ/n = 2,5217, S = √[Σ(xᵢ - x̄)²/(n-1)] = 1,4419.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n.
- **Fórmula** (σ conocido): n = (Z·σ/e)² = (1,96·1,2/0,5)² = 22,1268 → se redondea hacia arriba.

**Conclusión:** El tamaño de muestra necesario es n = 23. Como ya se tomaron 23, hay que agregar Δn = 23 - 23 = 0 unidades más. (El tamaño de muestra actual alcanza.) (Sin redondear, la fórmula da 22,1268.)

**Respuesta de la guía:** n = 22,13 → 23 establecimientos; la muestra obtenida fue de 23 establecimientos, el tamaño de muestra extraído es correcto.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 95% de confianza mediante un intervalo de confianza. Como σ es conocido se usa Z.

- **Procesar la muestra**: n = 23, x̄ = Σxᵢ/n = 2,5217, S = √[Σ(xᵢ - x̄)²/(n-1)] = 1,4419.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α/2) = Z(0,975) = 1,96.
- **Límites**: A;B = x̄ ∓ Z·σ/√n = 2,5217 ∓ 1,96·1,2/√23 = 2,5217 ∓ 0,4904.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 2,031 y 3,013, afirmándolo con un 95% de confianza, o sea: P(2,031 ≤ μ ≤ 3,013) = 0,95 (límites redondeados hacia afuera; sin redondear: 2,031322 y 3,012156).

**Respuesta de la guía:** Entre 2,03 y 3,02 empleados (x̄ = 2,5217 ± 0,4904), con un 95% de confianza.

#### c.a) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para un error máximo e = 0,5.

- **Procesar la muestra**: n = 23, x̄ = Σxᵢ/n = 2,5217, S = √[Σ(xᵢ - x̄)²/(n-1)] = 1,4419.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)  
• El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n (con t se itera porque ν depende de n).
- **Fórmula** (σ desconocido): n = (t(1-α/2; n-1)·S/e)². Como t depende de n se itera: [33, 35, 35].

**Conclusión:** El tamaño de muestra necesario es n = 35. Como ya se tomaron 23, hay que agregar Δn = 35 - 23 = 12 unidades más.

**Respuesta de la guía:** Con S = 1,4419: n = 35 establecimientos, el tamaño de muestra no es correcto, se necesitan 12 establecimientos más. Estimación: entre 1,89 y 3,15 empleados (x̄ = 2,5217 ± 0,6235), con un 95% de confianza.

#### c.b) Intervalo de confianza (estimar) ℹ️

*Qué pide:* Estimar la media poblacional μ con un 95% de confianza mediante un intervalo de confianza. Como σ es conocido se usa Z.

- **Procesar la muestra**: n = 23, x̄ = Σxᵢ/n = 2,5217, S = √[Σ(xᵢ - x̄)²/(n-1)] = 1,4419.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **Distribución**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student con ν = número de grados de libertad = n-1 = 22. t(0,975; 22) = 2,0739.
- **Límites**: A;B = x̄ ∓ t·S/√n = 2,5217 ∓ 2,0739·1,4419/√23 = 2,5217 ∓ 0,6235.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 1,898 y 3,146, afirmándolo con un 95% de confianza, o sea: P(1,898 ≤ μ ≤ 3,146) = 0,95 (límites redondeados hacia afuera; sin redondear: 1,898218 y 3,14526).

> 📝 *Notas de la transcripción:* Redondeo: 2,5217 + 0,4904 = 3,0121 (la guía dice 3,02) y 2,5217 − 0,6235 = 1,8982 (la guía dice 1,89).

<details><summary>Cómo lo concluye la guía</summary>

> Primero se procesan los resultados muestrales: n = 23 establecimientos, x̄ = 2,5217 empleados y S = 1,4419 empleados.
> La muestra obtenida en los resultados fue de 23 establecimientos, entonces se concluye que el tamaño de muestra extraído es correcto.
> Se concluye que el promedio de la población de establecimientos estará comprendido entre 2,03 empleados y 3,02 empleados, afirmándolo con un 95% de confianza, o sea: P(2,03 empleados ≤ μ ≤ 3,02 empleados) = 0,95.
> c) Si el desvío histórico (poblacional), σ = 1,2, se considera desconocido se debe tener en cuenta al desvío obtenido del procesamiento de los resultados muestrales, S = 1,4419.
> El resultado se obtiene con n = 35 establecimientos. De manera que se concluye que el tamaño de muestra no es correcto y se necesitarán incluir en la muestra obtenida, 12 establecimientos más.
> Se concluye que el promedio de la población de establecimientos estará comprendido entre 1,89 empleados y 3,15 empleados, afirmándolo con un 95% de confianza, o sea: P(1,89 empleados ≤ μ ≤ 3,15 empleados) = 0,95.

</details>

---

### I-4 · Problema 4 (pág. 2)

**Enunciado.** Las ventas de una revista semanal han sido las siguientes (en miles) en las últimas cuatro semanas: 15,4 – 18,5 – 16,3 – 19,2.

- **a)** Estimar la venta media semanal con un 95% de confianza.
- **b)** ¿Cuántas semanas más harían falta para poder dar un intervalo con un error de muestreo de ± 1 (± 1.000 ejemplares)?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 95% de confianza mediante un intervalo de confianza. Como σ no se conoce se usa S y t de Student (ν = n-1).

- **Procesar la muestra**: n = 4, x̄ = Σxᵢ/n = 17,35, S = √[Σ(xᵢ - x̄)²/(n-1)] = 1,7935.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **Distribución**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student con ν = número de grados de libertad = n-1 = 3. t(0,975; 3) = 3,1824.
- **Límites**: A;B = x̄ ∓ t·S/√n = 17,35 ∓ 3,1824·1,7935/√4 = 17,35 ∓ 2,8539.
- **En unidades** (los datos venían en miles, × 1.000): entre 14.496,13 y 20.203,87 (e = 2.853,87).

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 14,49 y 20,21, afirmándolo con un 95% de confianza, o sea: P(14,49 ≤ μ ≤ 20,21) = 0,95 (límites redondeados hacia afuera; sin redondear: 14,49613 y 20,20387). En unidades: entre 14.496,13 y 20.203,87.

**Respuesta de la guía:** Entre 14.496,13 y 20.203,88 unidades (x̄ = 17,35 ± 2,8539 miles), con un 95% de confianza.

> ≈ Coincide solo aproximadamente (20.203,88): Errata de la guía: el límite exacto 20.203,8696 se informa 20.203,88 (redondeado da 20.203,87).

#### b) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para un error máximo e = 1. Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Procesar la muestra**: n = 4, x̄ = Σxᵢ/n = 17,35, S = √[Σ(xᵢ - x̄)²/(n-1)] = 1,7935.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)  
• El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n (con t se itera porque ν depende de n).
- **Fórmula** (σ desconocido): n = (t(1-α/2; n-1)·S/e)². Como t depende de n se itera: [13, 16, 15, 15].

**Conclusión:** El tamaño de muestra necesario es n = 15. Como ya se tomaron 4, hay que agregar Δn = 15 - 4 = 11 unidades más.

**Respuesta de la guía:** n = 15 semanas de muestra, o sea 11 semanas más de las que se tenían al principio.

<details><summary>Cómo lo concluye la guía</summary>

> Primero se procesan los resultados muestrales: n = 4 semanas, x̄ = 17,35 miles de unidades y S = 1,793507 miles de unidades.
> Se concluye que el promedio de la población de las ventas semanales estará comprendido entre 14.496,13 unidades y 20.203,88 unidades, afirmándolo con un 95% de confianza, o sea: P(14.496,13 unidades ≤ μ ≤ 20.203,88 unidades) = 0,95.
> b) Se utiliza n = [t(0,975;ν=n−1)·S/e]² = [t(0,975;ν=n−1)·1,793507/1]², se debe utilizar el método iterativo para llegar a la solución, comenzando con un n arbitrario (n = 100 semanas).
> n = 15 ⇒ ν = 14 ⇒ t = 2,1448 ⇒ n = 15. Coincide el resultado, de manera que la solución son un total de 15 semanas de muestra, o sea 11 semanas más de las que se tenían al principio.

</details>

---

### I-5 · Problema 5 (pág. 2)

**Enunciado.** En una fábrica de materiales eléctricos se desea estimar el peso promedio del último lote de rollos de alambre de cobre salido de producción. Para ello se eligió al azar una muestra de 20 rollos que arrojó un promedio de 38 kg. Se conoce, además, de registros históricos, el desvío poblacional que vale 4,2 kg.

- **a)** Estimar el peso medio de los rollos con un 95% de confianza.
- **b)** ¿Cuántos rollos más habría que pesar para poder obtener una estimación cuyo error de muestreo sea de 1 kg?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 95% de confianza mediante un intervalo de confianza. Como σ es conocido se usa Z.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α/2) = Z(0,975) = 1,96.
- **Límites**: A;B = x̄ ∓ Z·σ/√n = 38 ∓ 1,96·4,2/√20 = 38 ∓ 1,8407.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 36,15 y 39,85, afirmándolo con un 95% de confianza, o sea: P(36,15 ≤ μ ≤ 39,85) = 0,95 (límites redondeados hacia afuera; sin redondear: 36,159303 y 39,840697).

**Respuesta de la guía:** Entre 36,15 y 39,85 kg.

#### b) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para un error máximo e = 1. Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n.
- **Fórmula** (σ conocido): n = (Z·σ/e)² = (1,96·4,2/1)² = 67,7633 → se redondea hacia arriba.

**Conclusión:** El tamaño de muestra necesario es n = 68. Como ya se tomaron 20, hay que agregar Δn = 68 - 20 = 48 unidades más.

**Respuesta de la guía:** 48 rollos más.

> 📝 *Notas de la transcripción:* a) 38 ± 1,96·4,2/√20 = 38 ± 1,84 → 36,16 y 39,84; la guía informa 36,15 y 39,85 (diferencia de redondeo).

---

### I-6 · Problema 6 (pág. 3)

**Enunciado.** En una fábrica de alfombras se desea estimar el peso promedio de los rollos que salen a despacho, que es muy variable pues su longitud está determinada por la aparición de fallas en el material. Una muestra de 60 rollos arrojó un peso medio de 48,5 kg con un desvío estándar de 42 kg.

*Estimar el peso medio de los rollos con un 10% de riesgo.*

*Tema detectado por la app: Media de 1 población (μ).*

#### Resolución (Intervalo de confianza (estimar)) ✅

*Qué pide:* Estimar la media poblacional μ con un 90% de confianza mediante un intervalo de confianza. Como σ no se conoce se usa S y t de Student (ν = n-1).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **Distribución**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student con ν = número de grados de libertad = n-1 = 59. t(0,95; 59) = 1,6711.
- **Límites**: A;B = x̄ ∓ t·S/√n = 48,5 ∓ 1,6711·42/√60 = 48,5 ∓ 9,061.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 39,43 y 57,57, afirmándolo con un 90% de confianza, o sea: P(39,43 ≤ μ ≤ 57,57) = 0,9 (límites redondeados hacia afuera; sin redondear: 39,439038 y 57,560962).

**Respuesta de la guía:** Entre 39,43 y 57,57 kg.

---

### I-7 · Problema 7 (pág. 3)

**Enunciado.** El nivel promedio de colesterol para una muestra aleatoria de 25 hombres de 30 años de edad fue de 214 unidades (miligramos de colesterol por cada 100 mililitros de sangre) y la varianza dio 456 unidades².

*¿Entre qué valores se encontrará el nivel promedio de colesterol con un Nivel de Confianza del 95%?*

*Tema detectado por la app: Media de 1 población (μ).*

#### Resolución (Intervalo de confianza (estimar)) ✅

*Qué pide:* Estimar la media poblacional μ con un 95% de confianza mediante un intervalo de confianza. Como σ no se conoce se usa S y t de Student (ν = n-1).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **Distribución**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student con ν = número de grados de libertad = n-1 = 24. t(0,975; 24) = 2,0639.
- **Límites**: A;B = x̄ ∓ t·S/√n = 214 ∓ 2,0639·21,3542/√25 = 214 ∓ 8,8146.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 205,18 y 222,82, afirmándolo con un 95% de confianza, o sea: P(205,18 ≤ μ ≤ 222,82) = 0,95 (límites redondeados hacia afuera; sin redondear: 205,185437 y 222,814563).

**Respuesta de la guía:** Entre 205,18 y 222,82 unidades.

---

### I-8 · Problema 8 (pág. 3)

**Enunciado.** El control de recepción de las partidas de un tipo de hilo de coser industrial, se realiza pesando una muestra de 10 ovillos de cada partida, rechazando la partida si el peso medio de la muestra resulta inferior a cierto valor crítico. El valor mínimo admisible del peso medio de los ovillos de toda la partida es de 250 gramos y la probabilidad máxima de rechazar una partida que cumple con dicha especificación es de 0,05. Se sabe, además, por disponer de registros históricos extensos, que el desvío estándar de esta variable es de 15 gramos.

*Indicar la hipótesis nula apropiada a esta situación, su condición de rechazo y la regla de decisión.*

*Tema detectado por la app: Media de 1 población (μ).*

#### Resolución (Diseñar el ensayo (H0, n, valor crítico, regla de decisión)) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≥ 250 supone que cumple; H1: μ < 250 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≥ 250  vs  H1: μ < 250  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,6449.
- **Condición de rechazo**: x̄c = μ₀ - 1,6449·σ/√n = 250 - 1,6449·15/√10 = 242,1978. Si x̄ < 242,1978 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 242,19; la decisión se toma con el valor exacto.
- **Regla de decisión**: Si en una muestra de 10 la media es menor que 242,1978 se rechaza H0.

**Conclusión:** Si en una muestra de 10 la media es menor que 242,1978 se rechaza H0.

**Respuesta de la guía:** H0) μ ≥ μ0 = 250 g; CR: Si x̄ < x̄c = 242,19 g ⇒ Rechazo H0; RD: Si de una muestra de 10 ovillos el peso promedio, de la misma, es inferior a 242,19 gramos, se rechaza la partida.

> 📝 *Notas de la transcripción:* 250 − 1,6449·15/√10 = 242,20; la guía informa 242,19 (redondeo).

---

### I-9 · Problema 9 (pág. 3)

**Enunciado.** Una carpintería de Capital Federal recibe periódicamente grandes partidas de madera de cedro procedentes de un aserradero de Salta. Una partida se considera aceptable si la longitud media de sus tablas es mayor o igual que 4 metros. Al examinar una muestra de 5 tablas de una partida recién recibida, se obtuvieron los siguientes resultados (en metros): 3,8 – 3,74 – 3,98 – 4,1 – 3,9. Se sabe además que la longitud de las tablas se distribuye Normalmente con un desvío estándar de 0,15 metros.

- **a)** ¿Se considera aceptable esta partida si se establece en 0,05 la probabilidad de rechazarla indebidamente? Justificar conceptualmente el planteo optimista de la hipótesis.
- **b)** ¿Cuál sería la probabilidad de aceptar una partida cuya longitud media sea de 3,85 metros?
- **c)** Dibujar las curvas Característica Operativa y de Potencia.
- **d)** ¿Cuántas tablas habría que medir de cada partida para que dicha probabilidad anterior valga 0,1?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '<'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **Procesar la muestra**: n = 5, x̄ = Σxᵢ/n = 3,904, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,1431.
- **1 · Planteo de hipótesis**: H0: μ ≥ 4  vs  H1: μ < 4.
- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≥ 4 supone que cumple; H1: μ < 4 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,6449.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ - 1,6449·σ/√n = 4 - 1,6449·0,15/√5 = 3,8897. Si x̄ < 3,8897 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 3,88; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 5 unidades y se calcula su media x̄. Si x̄ < 3,8897, se rechaza H0 → se puede asegurar que μ < 4. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ < 4.
- **6 · Cálculos y decisión**: x̄ = 3,904 → no cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0762. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,05, x̄ = 3,904 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ ≥ 4. No hay evidencia suficiente para asegurar que μ < 4 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No hay pruebas suficientes para asegurar que la longitud media sea inferior a los 4 metros, por lo cual se considera aceptable la partida.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Procesar la muestra**: n = 5, x̄ = Σxᵢ/n = 3,904, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,1431.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ ≥ 4,0, x̄c = 3,8897; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 3,8896), como la cátedra.
- **β** = P(x̄ ≥ x̄c | μ = 3,85) con Z = (x̄c - μ₁)/(σ/√n) = (3,8896 - 3,85)/0,0671 = 0,5903 → β = 0,2775.
- **Potencia** 1-β = 0,7225.

**Conclusión:** La probabilidad pedida es β = 0,2775 (potencia 1-β = 0,7225).

**Respuesta de la guía:** β = 0,2775.

#### c) Curva característica operativa / de potencia ℹ️

*Qué pide:* Tabular β y 1-β para varios valores del parámetro y graficar la curva OC (β) y la de potencia (1-β).

- **Procesar la muestra**: n = 5, x̄ = Σxᵢ/n = 3,904, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,1431.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- Se toman valores de μ del lado de H1 (cola izquierda), con n = 5 y α = 0,05; para cada uno se calcula β = P(no rechazar H0 | μ) y la potencia 1-β.
- En el eje X va el parámetro μ; en el eje Y la probabilidad (β para la curva OC, 1-β para la de potencia). Marcá al menos 3 puntos con sus valores.

**Conclusión:** Tabla de puntos para graficar las curvas (ver abajo).

**Respuesta de la guía:** Ver procedimiento de construcción de las curvas en los problemas 24 y 27.

#### d) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Procesar la muestra**: n = 5, x̄ = Σxᵢ/n = 3,904, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,1431.
- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≥ 4 supone que cumple; H1: μ < 4 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | μ = 3,85) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≥ 4  vs  H1: μ < 4.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 4) = α = 0,05 y P(no rechazar H0 | μ = 3,85) = β = 0,1.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + 1,2816)·0,15/0,15]² = 8,5638 → n = 9.
- **Condición de rechazo**: x̄c = 3,9178  (con n = 9).
- **Regla de decisión**: Tomar una muestra de n = 9. Si la media de esa muestra es inferior a 3,9178 (x̄ < x̄_c) se rechaza H0.
- Con n = 9: β real = 0,0877, potencia real = 0,9123.

**Conclusión:** Tomar una muestra de n = 9. Si la media de esa muestra es inferior a 3,9178 (x̄ < x̄_c) se rechaza H0. (Respecto de la muestra actual de 5: Δn = 4.)

**Respuesta de la guía:** 9 tablas.

---

### I-10 · Problema 10 (pág. 3)

**Enunciado.** El consumo de combustible de un automóvil para un determinado recorrido es una variable aleatoria de la cual se ha tomado una importante cantidad de datos que han arrojado una media de 11,2 litros con un desvío estándar de 1,3 litros, valores estos que pueden considerarse parámetros poblacionales. Se desea ensayar el efecto de un nuevo aditivo con el que se espera reducir el consumo medio y, de confirmarse esta suposición, se lanzará al mercado. Dados los costos implicados, se establece un riesgo del 5% de lanzar el producto cuando no produce el efecto deseado. Se realiza una prueba preliminar en la cual, sobre 10 corridas (de igual recorrido) se registra un consumo medio de 10,6 litros. Parece razonable asumir que el desvío estándar no se modificará.

- **a)** ¿Se considera que el resultado de la prueba es concluyente para lanzar el aditivo al mercado?
- **b)** ¿Cuál es la probabilidad de lanzar el producto cuando con él se tiene un consumo medio de 10,5 litros?
- **c)** ¿Cuántas corridas habría que efectuar para que la probabilidad anterior valga 0,90?
- **d)** Dibujar las curvas Característica Operativa y de Potencia para ambos tamaños de muestra.

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '<'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ ≥ 11,2  vs  H1: μ < 11,2.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≥ 11,2 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ < 11,2 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,6449.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ - 1,6449·σ/√n = 11,2 - 1,6449·1,3/√10 = 10,5238. Si x̄ < 10,5238 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 10,52; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 10 unidades y se calcula su media x̄. Si x̄ < 10,5238, se rechaza H0 → se puede asegurar que μ < 11,2. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ < 11,2.
- **6 · Cálculos y decisión**: x̄ = 10,6 → no cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0722. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,05, x̄ = 10,6 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ ≥ 11,2. No hay evidencia suficiente para asegurar que μ < 11,2 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No, no se puede asegurar que el consumo promedio ha disminuido.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ ≥ 11,2, x̄c = 10,5238; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 10,5238), como la cátedra.
- **β** = P(x̄ ≥ x̄c | μ = 10,5) con Z = (x̄c - μ₁)/(σ/√n) = (10,5238 - 10,5)/0,4111 = 0,0579 → β = 0,4769.
- **Potencia** 1-β = 0,5231.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,5231 (β = 0,4769).

**Respuesta de la guía:** 1–β = 0,5231.

#### c) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≥ 11,2 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ < 11,2 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | μ = 10,5) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≥ 11,2  vs  H1: μ < 11,2.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 11,2) = α = 0,05 y P(no rechazar H0 | μ = 10,5) = β = 0,1.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + 1,2816)·1,3/0,7]² = 29,5365 → n = 30.
- **Condición de rechazo**: x̄c = 10,8096  (con n = 30).
- **Regla de decisión**: Tomar una muestra de n = 30. Si la media de esa muestra es inferior a 10,8096 (x̄ < x̄_c) se rechaza H0.
- Con n = 30: β real = 0,096, potencia real = 0,904.

**Conclusión:** Tomar una muestra de n = 30. Si la media de esa muestra es inferior a 10,8096 (x̄ < x̄_c) se rechaza H0. (Respecto de la muestra actual de 10: Δn = 20.)

**Respuesta de la guía:** 30 corridas (de igual recorrido).

#### d) Curva característica operativa / de potencia ℹ️

*Qué pide:* Tabular β y 1-β para varios valores del parámetro y graficar la curva OC (β) y la de potencia (1-β).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- Se toman valores de μ del lado de H1 (cola izquierda), con n = 10 y α = 0,05; para cada uno se calcula β = P(no rechazar H0 | μ) y la potencia 1-β.
- En el eje X va el parámetro μ; en el eje Y la probabilidad (β para la curva OC, 1-β para la de potencia). Marcá al menos 3 puntos con sus valores.

**Conclusión:** Tabla de puntos para graficar las curvas (ver abajo).

**Respuesta de la guía:** Ver procedimiento de construcción de las curvas en los problemas 24 y 27.

---

### I-11 · Problema 11 (pág. 4)

**Enunciado.** Un cliente recibe habitualmente una partida de medidores eléctricos que, según las especificaciones del contrato, el promedio de las pérdidas debe ser menor o igual a 1 watt. Una muestra de 10 medidores, de una partida recién recibida, arroja una pérdida media de 1,06 watts. Se sabe, además, por experiencia anterior, que las pérdidas se distribuyen Normalmente con un desvío de 0,1 watts.

- **a)** Asumiendo un 10% el riesgo de rechazar la partida indebidamente, ¿puede aceptarse la misma?
- **b)** ¿Cuál es la probabilidad de aceptar una partida cuya pérdida media sea de 1,05 watts?
- **c)** ¿Cuál debería ser el tamaño de muestra si se pretende que la probabilidad anterior valga 0,10?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ ≤ 1  vs  H1: μ > 1.
- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≤ 1 supone que cumple; H1: μ > 1 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,2816.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 1,2816·σ/√n = 1 + 1,2816·0,1/√10 = 1,0405. Si x̄ > 1,0405 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 1,05; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 10 unidades y se calcula su media x̄. Si x̄ > 1,0405, se rechaza H0 → se puede asegurar que μ > 1. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 1.
- **6 · Cálculos y decisión**: x̄ = 1,06 → cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0289. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,1, x̄ = 1,06 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: μ ≤ 1. Se puede asegurar que μ > 1.

**Respuesta de la guía:** No, se puede asegurar que las pérdidas promedio son mayores que 1 watts.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ ≤ 1,0, x̄c = 1,0405; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 1,0406), como la cátedra.
- **β** = P(x̄ ≤ x̄c | μ = 1,05) con Z = (x̄c - μ₁)/(σ/√n) = (1,0406 - 1,05)/0,0316 = -0,2973 → β = 0,3831.
- **Potencia** 1-β = 0,6169.

**Conclusión:** La probabilidad pedida es β = 0,3831 (potencia 1-β = 0,6169).

**Respuesta de la guía:** β = 0,3831.

#### c) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≤ 1 supone que cumple; H1: μ > 1 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I); β = P(no rechazar H0 | μ = 1,05) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≤ 1  vs  H1: μ > 1.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 1) = α = 0,1 y P(no rechazar H0 | μ = 1,05) = β = 0,1.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,2816 + 1,2816)·0,1/0,05]² = 26,278 → n = 27.
- **Condición de rechazo**: x̄c = 1,0247  (con n = 27).
- **Regla de decisión**: Tomar una muestra de n = 27. Si la media de esa muestra es superior a 1,0247 (x̄ > x̄_c) se rechaza H0.
- Con n = 27: β real = 0,094, potencia real = 0,906.

**Conclusión:** Tomar una muestra de n = 27. Si la media de esa muestra es superior a 1,0247 (x̄ > x̄_c) se rechaza H0. (Respecto de la muestra actual de 10: Δn = 17.)

**Respuesta de la guía:** 27 medidores.

---

### I-12 · Problema 12 (pág. 4)

**Enunciado.** Una cadena de supermercados considera la posibilidad de cambiar sus máquinas registradoras por otras más modernas lanzadas al mercado recientemente. Se ha establecido la conveniencia de la inversión si se puede asegurar que el tiempo medio de atención por cliente ha de ser inferior a los 2 minutos y se desea que valga 0,05 la probabilidad de tomar una decisión errónea en tal sentido. Se sabe que, con las máquinas actuales, el desvío estándar respecto del tiempo de atención es de 1,5 minutos, teniéndose razones fundadas para asumir que con las máquinas nuevas no ha de modificarse. Se realizó un ensayo con las máquinas nuevas, en el cual se atendieron 40 personas en 68 minutos.

- **a)** ¿Cuál sería, con esta información, la decisión recomendada?
- **b)** ¿Cuál sería la probabilidad de comprar las nuevas máquinas, si con ellas el tiempo medio de atención fuera de 1,8 minutos?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '<'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ ≥ 2  vs  H1: μ < 2.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≥ 2 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ < 2 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,6449.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ - 1,6449·σ/√n = 2 - 1,6449·1,5/√40 = 1,6099. Si x̄ < 1,6099 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 1,60; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 40 unidades y se calcula su media x̄. Si x̄ < 1,6099, se rechaza H0 → se puede asegurar que μ < 2. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ < 2.
- **6 · Cálculos y decisión**: x̄ = 1,7 → no cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,103. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,05, x̄ = 1,7 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ ≥ 2. No hay evidencia suficiente para asegurar que μ < 2 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No comprar las nuevas máquinas.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ ≥ 2,0, x̄c = 1,6099; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 1,6098), como la cátedra.
- **β** = P(x̄ ≥ x̄c | μ = 1,8) con Z = (x̄c - μ₁)/(σ/√n) = (1,6098 - 1,8)/0,2372 = -0,802 → β = 0,7887.
- **Potencia** 1-β = 0,2113.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,2113 (β = 0,7887).

**Respuesta de la guía:** 1–β = 0,2113.

---

### I-13 · Problema 13 (pág. 4)

**Enunciado.** El consumo diario de combustible en una planta industrial es una variable cuya desviación estándar es de 23 litros. Se considera la posibilidad de introducir una modificación en el proceso tecnológico, que sólo se justificará si se logra obtener un consumo medio inferior a 200 litros. A efectos de tomar una decisión, se trabajó durante 5 días con el proceso modificado obteniéndose un consumo medio de 180 litros.

- **a)** ¿Se aconseja efectuar la modificación con probabilidad máxima de error de 0,05?
- **b)** Estimar con un 20% de riesgo el consumo medio de combustible con el proceso modificado.

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '<'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ ≥ 200  vs  H1: μ < 200.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≥ 200 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ < 200 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,6449.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ - 1,6449·σ/√n = 200 - 1,6449·23/√5 = 183,0812. Si x̄ < 183,0812 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 183,08; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 5 unidades y se calcula su media x̄. Si x̄ < 183,0812, se rechaza H0 → se puede asegurar que μ < 200. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ < 200.
- **6 · Cálculos y decisión**: x̄ = 180 → cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0259. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,05, x̄ = 180 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: μ ≥ 200. Se puede asegurar que μ < 200.

**Respuesta de la guía:** Sí, se puede asegurar que el consumo medio es inferior a 200 litros.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 80% de confianza mediante un intervalo de confianza. Como σ es conocido se usa Z.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α/2) = Z(0,9) = 1,2816.
- **Límites**: A;B = x̄ ∓ Z·σ/√n = 180 ∓ 1,2816·23/√5 = 180 ∓ 13,1819.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 166,81 y 193,19, afirmándolo con un 80% de confianza, o sea: P(166,81 ≤ μ ≤ 193,19) = 0,8 (límites redondeados hacia afuera; sin redondear: 166,818072 y 193,181928).

**Respuesta de la guía:** Entre 166,81 y 193,19 litros.

---

### I-14 · Problema 14 (pág. 4)

**Enunciado.** En una curtiembre, el consumo diario de uno de los productos químicos principales es variable con una media de 580 litros y un desvío estándar de 72 litros. El Jefe de Producción ha propuesto una modificación en una de las etapas del proceso, que implicará mayores costos, pero que se justificaría si se lograra una disminución del 10% en el consumo medio. Si así ocurriera, se desea que la probabilidad de implementar la modificación sea de 0,90, pero si no se obtuviera resultado alguno, el riesgo se establece en un 5%.

- **a)** Indicar la hipótesis nula apropiada a esta situación, calcular el tamaño de la muestra a tomar, indicar la condición de rechazo y la regla de decisión correspondiente.
- **b)** Calcular la probabilidad de implementar la modificación si con ella se obtiene una disminución del 5% en el consumo medio y dibujar la curva de potencia del ensayo, marcando claramente los valores numéricos de abscisa y ordenada de 3 puntos al menos.
- **c)** Si se decidiera hacer el ensayo de hipótesis dos veces, cada una con una muestra de n días, y el consumo hubiera disminuido en un 5%, ¿cuál sería la probabilidad de que ninguna de las muestras lo detecte?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≥ 580 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ < 580 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | μ = 522) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≥ 580  vs  H1: μ < 580.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 580) = α = 0,05 y P(no rechazar H0 | μ = 522) = β = 0,1.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + 1,2816)·72/58]² = 13,1971 → n = 14.
- **Condición de rechazo**: x̄c = 548,3484  (con n = 14).
- **Regla de decisión**: Tomar una muestra de n = 14. Si la media de esa muestra es inferior a 548,3484 (x̄ < x̄_c) se rechaza H0.
- Con n = 14: β real = 0,0855, potencia real = 0,9145.

**Conclusión:** Tomar una muestra de n = 14. Si la media de esa muestra es inferior a 548,3484 (x̄ < x̄_c) se rechaza H0.

**Respuesta de la guía:** (Criterio Pesimista) H0) μ ≥ μ0 = 580 litros; n = 14 días; CR: Si x̄ < x̄c = 548,34 litros ⇒ Rechazo H0; RD: Si de una muestra de n = 14 días de observación el consumo promedio es inferior a 548,34 litros, se implementará la modificación.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ ≥ 580,0, x̄c = 548,3484; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 548,3483), como la cátedra.
- **β** = P(x̄ ≥ x̄c | μ = 551) con Z = (x̄c - μ₁)/(σ/√n) = (548,3483 - 551)/19,2428 = -0,1378 → β = 0,5548.
- **Potencia** 1-β = 0,4452.
- Se toman valores de μ del lado de H1 (cola izquierda), con n = 14 y α = 0,05; para cada uno se calcula β = P(no rechazar H0 | μ) y la potencia 1-β.
- En el eje X va el parámetro μ; en el eje Y la probabilidad (β para la curva OC, 1-β para la de potencia). Marcá al menos 3 puntos con sus valores.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,4452 (β = 0,5548).

**Respuesta de la guía:** 1–β = 0,4452. Procedimiento de construcción de las curvas en problemas 24 y 27.

#### c) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ ≥ 580,0, x̄c = 548,3484; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 548,3483), como la cátedra.
- **β** = P(x̄ ≥ x̄c | μ = 551) con Z = (x̄c - μ₁)/(σ/√n) = (548,3483 - 551)/19,2428 = -0,1378 → β = 0,5548.
- **Potencia** 1-β = 0,4452.
- **Ensayos repetidos** (muestras independientes): P(ninguna de las 2 muestras lo detecte) = β^2 = 0,5548^2 = 0,3078.

**Conclusión:** La probabilidad pedida es P(ninguna de las 2 muestras lo detecte) = β^2 = 0,5548^2 = 0,3078.

**Respuesta de la guía:** β² = 0,3078.

---

### I-15 · Problema 15 (pág. 5)

**Enunciado.** Un fabricante estudia la posibilidad de compra de un equipo para elaborar herramientas para la construcción. La compra será viable si se puede asegurar que el equipo requiere en promedio menos de 12 minutos de tiempo de preparación por cada hora de operación. El jefe de compras visita una empresa en donde se está instalado el equipo y por la información que recibe comprueba que 25 horas de operación seleccionadas al azar, han requerido un total de 4 horas y 30 minutos de tiempo de preparación. Se sabe, además, que el desvío estándar del tiempo de preparación por hora de operación es de 2 minutos. Si se establece en un 5% el riesgo de comprar equivocadamente el equipo:

- **a)** ¿Se aconseja comprar el equipo?
- **b)** ¿Cuál es la probabilidad de no efectuar la compra si el tiempo medio de preparación es de 11 minutos?
- **c)** ¿Cuántas horas habría que operar el equipo si se pretende que la probabilidad anterior valga 0,10?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '<'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ ≥ 12  vs  H1: μ < 12.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≥ 12 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ < 12 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,6449.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ - 1,6449·σ/√n = 12 - 1,6449·2/√25 = 11,3421. Si x̄ < 11,3421 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 11,34; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 25 unidades y se calcula su media x̄. Si x̄ < 11,3421, se rechaza H0 → se puede asegurar que μ < 12. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ < 12.
- **6 · Cálculos y decisión**: x̄ = 10,8 → cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0013. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,05, x̄ = 10,8 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: μ ≥ 12. Se puede asegurar que μ < 12.

**Respuesta de la guía:** Sí, se puede asegurar que el equipo requiere en promedio menos de 12 minutos de preparación.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ ≥ 12,0, x̄c = 11,3421; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 11,342), como la cátedra.
- **β** = P(x̄ ≥ x̄c | μ = 11) con Z = (x̄c - μ₁)/(σ/√n) = (11,342 - 11)/0,4 = 0,855 → β = 0,1963.
- **Potencia** 1-β = 0,8037.

**Conclusión:** La probabilidad pedida es β = 0,1963 (potencia 1-β = 0,8037).

**Respuesta de la guía:** β = 0,1963.

#### c) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≥ 12 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ < 12 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | μ = 11) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≥ 12  vs  H1: μ < 12.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 12) = α = 0,05 y P(no rechazar H0 | μ = 11) = β = 0,1.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + 1,2816)·2/1]² = 34,2554 → n = 35.
- **Condición de rechazo**: x̄c = 11,4439  (con n = 35).
- **Regla de decisión**: Tomar una muestra de n = 35. Si la media de esa muestra es inferior a 11,4439 (x̄ < x̄_c) se rechaza H0.
- Con n = 35: β real = 0,0946, potencia real = 0,9054.

**Conclusión:** Tomar una muestra de n = 35. Si la media de esa muestra es inferior a 11,4439 (x̄ < x̄_c) se rechaza H0. (Respecto de la muestra actual de 25: Δn = 10.)

**Respuesta de la guía:** 35 horas.

---

### I-16 · Problema 16 (pág. 5)

**Enunciado.** Se desea establecer un sistema de muestreo periódico para controlar la resistencia a la rotura de unas piezas de “Dural”, de modo tal que se cumplan las siguientes condiciones: i) Si la resistencia media es de 38 kg/mm², detener el proceso productivo con probabilidad 0,1; ii) si dicho parámetro vale 37 kg/mm², detener el proceso con probabilidad 0,95. Se sabe que esta variable tiene un desvío estándar de 1,3 kg/mm².

- **a)** Indicar la hipótesis nula apropiada, su condición de rechazo, el tamaño de la muestra a tomar y la regla de decisión.
- **b)** Calcular la probabilidad de detectar que la resistencia media vale 37,5 kg/mm².
- **c)** Dibujar la curva de potencia del ensayo.

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• Es un **sistema de control**: la decisión es entre dos acciones. Rechazar H0 ⇒ se detiene el proceso; no rechazarla ⇒ el proceso sigue.  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≥ 38 supone que cumple; H1: μ < 38 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(error de tipo I) = P(se detiene el proceso | μ = 38) = 0,1; β = P(error de tipo II) = P(el proceso sigue | μ = 37) = 0,05.  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≥ 38  vs  H1: μ < 38.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 38) = α = 0,1 y P(no rechazar H0 | μ = 37) = β = 0,05.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,2816 + 1,6449)·1,3/1]² = 14,4729 → n = 15.
- **Condición de rechazo**: x̄c = 37,5698  (con n = 15).
- **Regla de decisión**: Tomar una muestra de n = 15. Si la media de esa muestra es inferior a 37,5698 (x̄ < x̄_c) se rechaza H0.
- **En palabras del problema**: rechazar H0 ⇒ se detiene el proceso. Si en una muestra de 15 la media da menor que 37,5698, se detiene el proceso; si no, el proceso sigue.
- Con n = 15: β real = 0,0448, potencia real = 0,9552.

**Conclusión:** Tomar una muestra de n = 15. Si la media de esa muestra es inferior a 37,5698 (x̄ < x̄_c) se rechaza H0. Rechazar H0 ⇒ se detiene el proceso.

**Respuesta de la guía:** (Criterio Optimista) H0) μ ≥ μ0 = 38 kg/mm²; CR: Si x̄ < x̄c = 37,56 kg/mm² ⇒ Rechazo H0; n = 15 piezas; RD: Si de una muestra de 15 piezas, la resistencia promedio de la misma es inferior a 37,56 kg/mm² se detiene el proceso.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ ≥ 38,0, x̄c = 37,5698; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 37,5698), como la cátedra.
- **β** = P(x̄ ≥ x̄c | μ = 37,5) con Z = (x̄c - μ₁)/(σ/√n) = (37,5698 - 37,5)/0,3357 = 0,2079 → β = 0,4176.
- **Potencia** 1-β = 0,5824.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,5824 (β = 0,4176).

**Respuesta de la guía:** 1–β = 0,5824.

#### c) Curva característica operativa / de potencia ℹ️

*Qué pide:* Tabular β y 1-β para varios valores del parámetro y graficar la curva OC (β) y la de potencia (1-β).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- Se toman valores de μ del lado de H1 (cola izquierda), con n = 15 y α = 0,1; para cada uno se calcula β = P(no rechazar H0 | μ) y la potencia 1-β.
- En el eje X va el parámetro μ; en el eje Y la probabilidad (β para la curva OC, 1-β para la de potencia). Marcá al menos 3 puntos con sus valores.

**Conclusión:** Tabla de puntos para graficar las curvas (ver abajo).

**Respuesta de la guía:** Ver procedimiento de construcción de las curvas en los problemas 24 y 27.

> 📝 *Notas de la transcripción:* 38 − 1,2816·1,3/√15 = 37,57; la guía informa 37,56 (redondeo).

---

### I-17 · Problema 17 (pág. 5)

**Enunciado.** Se desea diseñar un sistema de muestreo periódico para controlar el rendimiento de un proceso químico, cuyo valor estándar (rendimiento promedio) es del 80%; la probabilidad de detenerlo y revisarlo equivocadamente debe ser de 0,05, pero cuando baja al 75% se desea una probabilidad de 0,90 de detectarlo. Entre distintas pruebas, los valores de rendimiento son una variable aleatoria cuyo desvío es del 6%.

- **a)** Indicar la hipótesis nula apropiada, su condición de rechazo y la regla de decisión.
- **b)** Calcular la probabilidad de detener el proceso cuando su rendimiento es del 76%.
- **c)** Dibujar las curvas Característica Operativa y de Potencia.
- **d)** Si en un ensayo de prueba se obtuvo un rendimiento medio de 75%, ¿qué decisión tomaría?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≥ 80 supone que cumple; H1: μ < 80 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | μ = 75) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≥ 80  vs  H1: μ < 80.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 80) = α = 0,05 y P(no rechazar H0 | μ = 75) = β = 0,1.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + 1,2816)·6/5]² = 12,3319 → n = 13.
- **Condición de rechazo**: x̄c = 77,2628  (con n = 13).
- **Regla de decisión**: Tomar una muestra de n = 13. Si la media de esa muestra es inferior a 77,2628 (x̄ < x̄_c) se rechaza H0.
- Con n = 13: β real = 0,087, potencia real = 0,913.

**Conclusión:** Tomar una muestra de n = 13. Si la media de esa muestra es inferior a 77,2628 (x̄ < x̄_c) se rechaza H0.

**Respuesta de la guía:** (Criterio Optimista) H0) μ ≥ μ0 = 80%; CR: Si x̄ < x̄c = 77,26% ⇒ Rechazo H0; RD: Si de una muestra de 13 observaciones el rendimiento promedio es menor que 77,26% se detiene el proceso.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ ≥ 80,0, x̄c = 77,2628; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 77,2627), como la cátedra.
- **β** = P(x̄ ≥ x̄c | μ = 76) con Z = (x̄c - μ₁)/(σ/√n) = (77,2627 - 76)/1,6641 = 0,7588 → β = 0,224.
- **Potencia** 1-β = 0,776.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,776 (β = 0,224).

**Respuesta de la guía:** 1–β = 0,776.

#### c) Curva característica operativa / de potencia ℹ️

*Qué pide:* Tabular β y 1-β para varios valores del parámetro y graficar la curva OC (β) y la de potencia (1-β).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- Se toman valores de μ del lado de H1 (cola izquierda), con n = 13 y α = 0,05; para cada uno se calcula β = P(no rechazar H0 | μ) y la potencia 1-β.
- En el eje X va el parámetro μ; en el eje Y la probabilidad (β para la curva OC, 1-β para la de potencia). Marcá al menos 3 puntos con sus valores.

**Conclusión:** Tabla de puntos para graficar las curvas (ver abajo).

**Respuesta de la guía:** Ver procedimiento de construcción de las curvas en los problemas 24 y 27.

#### d) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ℹ️

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≥ 80 supone que cumple; H1: μ < 80 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | μ = 76) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≥ 80  vs  H1: μ < 80.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 80) = α = 0,05 y P(no rechazar H0 | μ = 76) = β = 0,1.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + 1,2816)·6/4]² = 19,2687 → n = 20.
- **Condición de rechazo**: x̄c = 77,7932  (con n = 20).
- **Regla de decisión**: Tomar una muestra de n = 20. Si la media de esa muestra es inferior a 77,7932 (x̄ < x̄_c) se rechaza H0.
- Con n = 20: β real = 0,0907, potencia real = 0,9093.

**Conclusión:** Tomar una muestra de n = 20. Si la media de esa muestra es inferior a 77,7932 (x̄ < x̄_c) se rechaza H0.

**Respuesta de la guía:** Detener el proceso y revisarlo.

---

### I-18 · Problema 18 (pág. 5)

**Enunciado.** La resistencia a la rotura de cierto tipo de alambre es una variable aleatoria con una media de 280 kg y un desvío estándar de 20 kg. Se cree que un proceso de fabricación recién desarrollado puede aumentar la resistencia media sin modificar el desvío estándar, pero sólo se lo implementará si se tiene una razonable seguridad de que efectivamente es así. Se ha establecido en 0,05 la probabilidad de implementar el nuevo método cuando en realidad la resistencia no se modifica, y en 0,15 la probabilidad de no implementarlo si se incrementa en 10 kg.

- **a)** Establecer la hipótesis nula, la condición de rechazo y la regla de decisión.
- **b)** ¿Cuál es la probabilidad de implementar el nuevo método si la resistencia media aumenta en 5 kg?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≤ 280 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ > 280 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | μ = 290) = 0,15 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≤ 280  vs  H1: μ > 280.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 280) = α = 0,05 y P(no rechazar H0 | μ = 290) = β = 0,15.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + 1,0364)·20/10]² = 28,7572 → n = 29.
- **Condición de rechazo**: x̄c = 286,1088  (con n = 29).
- **Regla de decisión**: Tomar una muestra de n = 29. Si la media de esa muestra es superior a 286,1088 (x̄ > x̄_c) se rechaza H0.
- Con n = 29: β real = 0,1474, potencia real = 0,8526.

**Conclusión:** Tomar una muestra de n = 29. Si la media de esa muestra es superior a 286,1088 (x̄ > x̄_c) se rechaza H0.

**Respuesta de la guía:** (Criterio Pesimista) H0) μ ≤ μ0 = 280 kg; CR: Si x̄ > x̄c = 286,11 kg ⇒ Rechazo H0; RD: Si de una muestra de 29 observaciones la resistencia promedio es mayor que 286,11 kg se implementa el nuevo método de fabricación.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ ≤ 280,0, x̄c = 286,1088; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 286,1089), como la cátedra.
- **β** = P(x̄ ≤ x̄c | μ = 285) con Z = (x̄c - μ₁)/(σ/√n) = (286,1089 - 285)/3,7139 = 0,2986 → β = 0,6174.
- **Potencia** 1-β = 0,3826.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,3826 (β = 0,6174).

**Respuesta de la guía:** 1–β = 0,3826.

---

### I-19 · Problema 19 (pág. 6)

**Enunciado.** Una compañía desea diseñar un sistema de muestreo periódico para controlar la recepción de grandes partidas de un producto. El proveedor desea tener la seguridad de que le rechacen a lo sumo el 5% de las partidas buenas, que son aquellas que cumplen con la especificación de que la resistencia media mínima es de 1.250 kg. A su vez, el cliente desea rechazar al menos el 90% de las partidas malas, que son aquellas cuya resistencia media es inferior a 1.100 kg. Ambos firman un contrato en el cual constan las condiciones anteriores y se establece que la decisión de rechazar o aceptar una partida se tomará en función del resultado de una muestra de n unidades elegidas al azar de la misma. Existen registros históricos por los cuales se sabe que el desvío de la resistencia a la rotura es de 180 kg.

- **a)** Indicar la hipótesis nula apropiada, su condición de rechazo y la regla de decisión.
- **b)** Calcular la probabilidad de detectar que una partida dada resiste en promedio 1.200 kg.

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≥ 1.250 supone que cumple; H1: μ < 1.250 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | μ = 1.100) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≥ 1250  vs  H1: μ < 1250.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 1.250) = α = 0,05 y P(no rechazar H0 | μ = 1.100) = β = 0,1.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + 1,2816)·180/150]² = 12,3319 → n = 13.
- **Condición de rechazo**: x̄c = 1.167,8839  (con n = 13).
- **Regla de decisión**: Tomar una muestra de n = 13. Si la media de esa muestra es inferior a 1167,8839 (x̄ < x̄_c) se rechaza H0.
- Con n = 13: β real = 0,087, potencia real = 0,913.

**Conclusión:** Tomar una muestra de n = 13. Si la media de esa muestra es inferior a 1167,8839 (x̄ < x̄_c) se rechaza H0.

**Respuesta de la guía:** (Criterio Optimista) H0) μ ≥ μ0 = 1.250 kg; CR: Si x̄ < x̄c = 1.167,88 kg ⇒ Rechazo H0; RD: Si de una muestra de 13 unidades la resistencia promedio es menor que 1.167,88 kg se rechaza la partida.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ ≥ 1250,0, x̄c = 1,167,8839; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 1,167,8839), como la cátedra.
- **β** = P(x̄ ≥ x̄c | μ = 1.200) con Z = (x̄c - μ₁)/(σ/√n) = (1.167,8839 - 1.200)/49,923 = -0,6433 → β = 0,74.
- **Potencia** 1-β = 0,26.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,26 (β = 0,74).

**Respuesta de la guía:** 1–β = 0,26.

---

### I-20 · Problema 20 (pág. 6)

**Enunciado.** La resistencia a la rotura de un tipo de látex es una variable con una media de 4,5 kg y un desvío estándar de 0,3 kg. Se cree que un aditivo recientemente desarrollado por los técnicos puede incrementar la resistencia media. Si así no ocurriera, se desea un 0,05 de probabilidad de tomar la decisión incorrecta. Si la resistencia se incrementa en 0,2 kg, se desea una probabilidad de 0,99 de adoptar el aditivo.

- **a)** Indicar la hipótesis nula apropiada a esta situación, el tamaño de la muestra a tomar, la condición de rechazo y la regla de decisión.
- **b)** Realizar tablas de valores para las curvas operativa y de potencia y graficarlas.

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≤ 4,5 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ > 4,5 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | μ = 4,7) = 0,01 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≤ 4,5  vs  H1: μ > 4,5.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 4,5) = α = 0,05 y P(no rechazar H0 | μ = 4,7) = β = 0,01.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + 2,3263)·0,3/0,2]² = 35,4835 → n = 36.
- **Condición de rechazo**: x̄c = 4,5822  (con n = 36).
- **Regla de decisión**: Tomar una muestra de n = 36. Si la media de esa muestra es superior a 4,5822 (x̄ > x̄_c) se rechaza H0.
- Con n = 36: β real = 0,0093, potencia real = 0,9907.

**Conclusión:** Tomar una muestra de n = 36. Si la media de esa muestra es superior a 4,5822 (x̄ > x̄_c) se rechaza H0.

**Respuesta de la guía:** (Criterio Pesimista) H0) μ ≤ μ0 = 4,5 kg; n = 36 muestras; CR: Si x̄ > x̄c = 4,59 kg ⇒ Rechazo H0; RD: Si de una muestra de 36 observaciones la resistencia promedio es mayor que 4,59 kg se adopta el aditivo.

#### b) Curva característica operativa / de potencia ℹ️

*Qué pide:* Tabular β y 1-β para varios valores del parámetro y graficar la curva OC (β) y la de potencia (1-β).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- Se toman valores de μ del lado de H1 (cola derecha), con n = 36 y α = 0,05; para cada uno se calcula β = P(no rechazar H0 | μ) y la potencia 1-β.
- En el eje X va el parámetro μ; en el eje Y la probabilidad (β para la curva OC, 1-β para la de potencia). Marcá al menos 3 puntos con sus valores.

**Conclusión:** Tabla de puntos para graficar las curvas (ver abajo).

**Respuesta de la guía:** Ver procedimiento de construcción de las curvas en los problemas 24 y 27.

> 📝 *Notas de la transcripción:* Posible inconsistencia: con n = 36, x̄c = 4,5 + 1,6449·0,3/√36 = 4,5822 ≈ 4,58 kg, no 4,59 kg como informa la guía.

---

### I-21 · Problema 21 (pág. 6)

**Enunciado.** El tipo de aceite usado en las unidades de una empresa trasportista es una variable que incide sensiblemente en el costo de mantenimiento. En la actualidad se tiene un costo promedio por unidad de 250 U$s por mes y se desea realizar un experimento con otro tipo de aceite más costoso que el actual a los efectos de comprobar una posible disminución del costo promedio total de mantenimiento. Se ha establecido un presupuesto experimental de 6 meses y una probabilidad de 0,01 de tomar una decisión equivocada en caso de que el costo mensual no disminuya. Se sabe que el costo mensual tiene un desvío estándar de 30 U$s, valor este que se ha mantenido muy estable con el tiempo y seguramente no se modificará con el nuevo aceite. Se realizó la prueba durante los 6 meses y se obtuvo un costo promedio por unidad de 232 U$s por mes.

- **a)** Establecer la hipótesis nula apropiada, realizar el ensayo e indicar la decisión recomendada.
- **b)** Calcular la probabilidad de tomar una decisión equivocada para el caso en que el costo baje en un 10% y dibujar la curva operativa del ensayo indicando claramente las variables que se llevan en los ejes y los valores numéricos de abscisa y ordenada de tres puntos al menos.

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '<'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ ≥ 250  vs  H1: μ < 250.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≥ 250 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ < 250 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,01 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,01 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 2,3263.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ - 2,3263·σ/√n = 250 - 2,3263·30/√6 = 221,5082. Si x̄ < 221,5082 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 221,50; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 6 unidades y se calcula su media x̄. Si x̄ < 221,5082, se rechaza H0 → se puede asegurar que μ < 250. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ < 250.
- **6 · Cálculos y decisión**: x̄ = 232 → no cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0708. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,01, x̄ = 232 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ ≥ 250. No hay evidencia suficiente para asegurar que μ < 250 (no rechazar H0 no la prueba).

**Respuesta de la guía:** (Criterio Pesimista) H0) μ ≥ μ0 = 250 U$s; No se rechaza la hipótesis nula, por lo tanto, se concluye que no se cambia por el nuevo tipo de aceite.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ ≥ 250,0, x̄c = 221,5082; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 221,5081), como la cátedra.
- **β** = P(x̄ ≥ x̄c | μ = 225) con Z = (x̄c - μ₁)/(σ/√n) = (221,5081 - 225)/12,2474 = -0,2851 → β = 0,6122.
- **Potencia** 1-β = 0,3878.
- Se toman valores de μ del lado de H1 (cola izquierda), con n = 6 y α = 0,01; para cada uno se calcula β = P(no rechazar H0 | μ) y la potencia 1-β.
- En el eje X va el parámetro μ; en el eje Y la probabilidad (β para la curva OC, 1-β para la de potencia). Marcá al menos 3 puntos con sus valores.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,3878 (β = 0,6122).

**Respuesta de la guía:** β = 0,6122. Procedimiento de construcción de curvas en problemas 24 y 27.

---

### I-22 · Problema 22 (pág. 6)

**Enunciado.** Un fabricante de pilas para linternas afirma que la vida media de ellas excede las 30 horas y las ofrece en condiciones muy ventajosas. Una empresa desea comprar una cantidad muy grande de pilas si la afirmación es cierta y a efectos de evaluarla se plantean en la gerencia 2 alternativas. Alternativa 1: algunos sostienen que, en principio, no hay motivos para dudar del fabricante deseando considerar la oferta, estableciendo en 0,10 la probabilidad de no concretar la operación cuando la vida media exceda las 30 hs, y en 0,05 la probabilidad de concretarla si la vida media es de 27 hs. Alternativa 2: otros en cambio consideran, por las condiciones tan ventajosas, que la afirmación del fabricante debe tomarse con cautela, siendo conveniente establecer una probabilidad de 0,05 de concretar la operación si la vida media no supera las 30 hs, y en 0,90 la probabilidad de concretarla si la vida media es de 32 hs. Se sabe que la duración de las pilas es una variable aleatoria con una desviación estándar de 5,5 hs.

*Indicar, para cada una de las alternativas, la hipótesis nula apropiada, la condición de rechazo y la regla de decisión.*

*Tema detectado por la app: Media de 1 población (μ).*

#### Resolución (Diseñar el ensayo (H0, n, valor crítico, regla de decisión)) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **— Alternativa 1 —**
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≤ 30 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ > 30 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I); β = P(no rechazar H0 | μ = 27) = 0,05 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≥ 30  vs  H1: μ < 30.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 30) = α = 0,1 y P(no rechazar H0 | μ = 27) = β = 0,05.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,2816 + 1,6449)·5,5/3]² = 28,784 → n = 29.
- **Condición de rechazo**: x̄c = 28,6911  (con n = 29).
- **Regla de decisión**: Tomar una muestra de n = 29. Si la media de esa muestra es inferior a 28,6911 (x̄ < x̄_c) se rechaza H0.
- Con n = 29: β real = 0,0489, potencia real = 0,9511.
- **— Alternativa 2 —**
- **Hipótesis**: H0: μ ≤ 30  vs  H1: μ > 30.
- **Condiciones**: P(rechazar H0 | μ = 30) = α = 0,05 y P(no rechazar H0 | μ = 32) = β = 0,1.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + 1,2816)·5,5/2]² = 64,7641 → n = 65.
- **Condición de rechazo**: x̄c = 31,1221  (con n = 65).
- **Regla de decisión**: Tomar una muestra de n = 65. Si la media de esa muestra es superior a 31,1221 (x̄ > x̄_c) se rechaza H0.
- Con n = 65: β real = 0,0991, potencia real = 0,9009.

**Conclusión:** Alternativa 1: Tomar una muestra de n = 29. Si la media de esa muestra es inferior a 28,6911 (x̄ < x̄_c) se rechaza H0. Alternativa 2: Tomar una muestra de n = 65. Si la media de esa muestra es superior a 31,1221 (x̄ > x̄_c) se rechaza H0.

**Respuesta de la guía:** Alternativa 1: (Criterio Optimista) H0) μ ≥ μ0 = 30 hs; CR: Si x̄ < x̄c = 28,69 hs ⇒ Rechazo H0; RD: Si de una muestra de 29 pilas la duración promedio es menor que 28,69 hs no concretar la operación. Alternativa 2: (Criterio Pesimista) H0) μ ≤ μ0 = 30 hs; CR: Si x̄ > x̄c = 31,13 hs ⇒ Rechazo H0; RD: Si de una muestra de 65 pilas la duración promedio es mayor que 31,13 hs concretar la operación.

> 📝 *Notas de la transcripción:* La Resp está en la página 7. Alternativa 2: con n = 65, 30 + 1,6449·5,5/√65 = 31,12; la guía informa 31,13 (redondeo).

---

### I-23 · Problema 23 (pág. 7)

**Enunciado.** El control de recepción de las partidas de hilado que llegan a una tejeduría se efectúa a través de una muestra de 10 ovillos midiéndose en cada uno la resistencia del hilado, cuyo valor medio para toda la partida debe ser de 25 kg por lo menos. El proveedor acepta un riesgo máximo del 5% de recibir de vuelta una partida buena y el comprador, a su vez, desea rechazar el 99% por lo menos de las partidas consideradas malas. Se sabe que la resistencia a la rotura de este hilado es una variable aleatoria con un desvío de 2,2 kg.

- **a)** ¿Cuál es la resistencia media muestral mínima para aceptar una partida?
- **b)** ¿Cuál es la resistencia media poblacional de las partidas consideradas malas por el comprador?
- **c)** Dibujar la curva que describe las probabilidades de detectar partidas malas.

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≥ 25 supone que cumple; H1: μ < 25 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≥ 25  vs  H1: μ < 25  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,6449.
- **Condición de rechazo**: x̄c = μ₀ - 1,6449·σ/√n = 25 - 1,6449·2,2/√10 = 23,8557. Si x̄ < 23,8557 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 23,85; la decisión se toma con el valor exacto.
- **Regla de decisión**: Si en una muestra de 10 la media es menor que 23,8557 se rechaza H0.
- **Media alternativa** (la que se detecta con 1-β = 0,99): μ₁ = x̄c - Z(1-β)·σ/√n = 23,8557 - 2,3263·2,2/√10 = 22,2372.

**Conclusión:** Si en una muestra de 10 la media es menor que 23,8557 se rechaza H0. La media alternativa definida por β = 0,01 es μ₁ = 22,2372.

**Respuesta de la guía:** x̄c = 23,86 kg.

#### b) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≥ 25 supone que cumple; H1: μ < 25 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≥ 25  vs  H1: μ < 25  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,6449.
- **Condición de rechazo**: x̄c = μ₀ - 1,6449·σ/√n = 25 - 1,6449·2,2/√10 = 23,8557. Si x̄ < 23,8557 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 23,85; la decisión se toma con el valor exacto.
- **Regla de decisión**: Si en una muestra de 10 la media es menor que 23,8557 se rechaza H0.
- **Media alternativa** (la que se detecta con 1-β = 0,99): μ₁ = x̄c - Z(1-β)·σ/√n = 23,8557 - 2,3263·2,2/√10 = 22,2372.

**Conclusión:** Si en una muestra de 10 la media es menor que 23,8557 se rechaza H0. La media alternativa definida por β = 0,01 es μ₁ = 22,2372.

**Respuesta de la guía:** μ1 = 22,23 kg.

#### c) Curva característica operativa / de potencia ℹ️

*Qué pide:* Tabular β y 1-β para varios valores del parámetro y graficar la curva OC (β) y la de potencia (1-β).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- Se toman valores de μ del lado de H1 (cola izquierda), con n = 10 y α = 0,05; para cada uno se calcula β = P(no rechazar H0 | μ) y la potencia 1-β.
- En el eje X va el parámetro μ; en el eje Y la probabilidad (β para la curva OC, 1-β para la de potencia). Marcá al menos 3 puntos con sus valores.

**Conclusión:** Tabla de puntos para graficar las curvas (ver abajo).

**Respuesta de la guía:** Ver procedimiento de construcción de las curvas en los problemas 24 y 27.

---

### I-24 · Problema 24 (pág. 7)

**Enunciado.** El departamento de Ingeniería de una empresa ha desarrollado una modificación de su contactor modelo “AX–2”. Luego de algunas pruebas experimentales, se piensa que el nuevo modelo tendrá una vida útil promedio de por lo menos un 10% superior al actual. De acuerdo con registros históricos, la vida del “AX–2” tiene una media de 10.000.000 contactos con un desvío de 2.300.000. Después de algunas discusiones, la Gerencia General decide fabricar una serie de prototipos y someterlos a pruebas exhaustivas. Como el contactor actual está muy bien posicionado en el mercado y si bien el nuevo modelo tendría el mismo costo, el Gerente Comercial opina que le parece razonable aceptar un riesgo del 15% de poner en el mercado el nuevo modelo en caso de que su vida media sea exactamente un 10% superior a la actual. Dado el costo de los prototipos, se recomienda además al Jefe de Ingeniería, que limite la cantidad a ensayar de modo que la probabilidad de recomendar el cambio si la vida media no aumentó sea a lo sumo de 0,05. Se asumirá además que el desvío estándar no se modificará.

- **a)** Indicar la hipótesis nula, la condición de rechazo y la regla de decisión.
- **b)** Dibujar la curva de potencia del ensayo.

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≤ 10.000.000 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ > 10.000.000 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | μ = 11.000.000) = 0,85 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≤ 10000000  vs  H1: μ > 10000000.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 10.000.000) = α = 0,05 y P(no rechazar H0 | μ = 11.000.000) = β = 0,85.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + -1,0364)·2.300.000/1.000.000]² = 1,9582 → n = 2.
- **Condición de rechazo**: x̄c = 12.675.100,4535  (con n = 2).
- **Regla de decisión**: Tomar una muestra de n = 2. Si la media de esa muestra es superior a 12675100,4535 (x̄ > x̄_c) se rechaza H0.
- Con n = 2: β real = 0,8485, potencia real = 0,1515.

**Conclusión:** Tomar una muestra de n = 2. Si la media de esa muestra es superior a 12675100,4535 (x̄ > x̄_c) se rechaza H0.

**Respuesta de la guía:** (Criterio Pesimista) H0) μ ≤ μ0 = 10 millones de contactos; α = 0,05; n = 2; CR: Si x̄ > x̄c = 12,67510045 millones de contactos ⇒ Rechazo H0; RD: se realizará una prueba con 2 prototipos del nuevo modelo de contactor y se calculará el promedio de sus duraciones, si este promedio supera los 12.675.100,45 contactos, se adoptará el nuevo modelo.

#### b) Curva característica operativa / de potencia ℹ️

*Qué pide:* Tabular β y 1-β para varios valores del parámetro y graficar la curva OC (β) y la de potencia (1-β).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- Se toman valores de μ del lado de H1 (cola derecha), con n = 2 y α = 0,05; para cada uno se calcula β = P(no rechazar H0 | μ) y la potencia 1-β.
- En el eje X va el parámetro μ; en el eje Y la probabilidad (β para la curva OC, 1-β para la de potencia). Marcá al menos 3 puntos con sus valores.

**Conclusión:** Tabla de puntos para graficar las curvas (ver abajo).

**Respuesta de la guía:** Tabla de la curva de potencia (1–β = 1 − φ((12,6751 − μ1)/(2,3/√2))): μ1 = 10 → 0,05; 11 → 0,15; 12,67 → 0,50; 15,36 → 0,95 (μ1 en millones de contactos).

<details><summary>Cómo lo concluye la guía</summary>

> a) Por tratarse de una inversión con riesgo económico, se recomienda ensayar una hipótesis con criterio pesimista, adoptando como μ0 el peor valor, es decir 10 (millones de contactos), o sea: H0) μ ≤ μ0 = 10 millones de contactos.
> De acuerdo con el enunciado, el valor de α es 0,05.
> Para calcular el valor de n se utiliza el dato de 0,15, que es la probabilidad de poner en el mercado el nuevo modelo en caso de que su vida media alcance los 11 millones de contactos (1–β = 0,15), de manera que Z(1−β) = Z(0,15) = −1,0364.
> n = [(1,6449 − 1,0364)·2,3/(11 − 10)]² = 2. Ahora se puede calcular el crítico: x̄c = 10 + 1,6449·2,3/√2 = 12,67510045 millones de contactos.
> La regla de decisión es: se realizará una prueba con 2 prototipos del nuevo modelo de contactor y se calculará el promedio de sus duraciones, si este promedio supera los 12.675.100,45 contactos, se adoptará el nuevo modelo.

</details>

---

### I-25 · Problema 25 (pág. 8)

**Enunciado.** La recaudación mensual de un club en concepto de cuotas de socios es variable con una media de 128.000 U$s y un desvío de 12.500 U$s. A efectos de aumentar la recaudación, se contratan los servicios de una compañía de cobranzas que obtiene, en los primeros 4 meses una media de 140.000 U$s; esta compañía cobra 5.000 U$s por sus servicios.

- **a)** Si se asume que el desvío estándar no se modifica y se toma un riesgo del 10%, ¿se continuaría contratando a esta compañía?
- **b)** ¿Cuál sería la probabilidad de no detectar que la recaudación media (sin descontar lo que cobra) aumenta a 145.000 U$s (bruto)?
- **c)** ¿Cuál sería la respuesta a la pregunta a) si la compañía cobrara por sus servicios una comisión del 2% sobre el monto recaudado?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **Valor neto**: lo que se compara con μ₀ es la media NETA: x̄ neto = x̄ - 5.000 = 140.000 - 5.000 = 135.000.
- **1 · Planteo de hipótesis**: H0: μ ≤ 128000  vs  H1: μ > 128000.
- **Justificación de H0**:  
• H1: μ > 128.000 recoge lo que el enunciado quiere probar; H0: μ ≤ 128.000 es el complemento y lleva la igualdad (el valor de referencia 128.000).  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,2816.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 1,2816·σ/√n = 128.000 + 1,2816·12.500/√4 = 136.009,6973. Si x̄ > 136.009,6973 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 136.009,70; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 4 unidades y se calcula su media x̄. Si x̄ > 136,009,6973, se rechaza H0 → se puede asegurar que μ > 128000. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 128000.
- **6 · Cálculos y decisión**: x̄ = 135.000 → no cae en la zona de rechazo.
- **Equivalente en valores brutos**: la media bruta debería superar x̄c bruto = 141.009,7 (se obtuvo 140.000).
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,1314. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,1, x̄ = 135,000 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ ≤ 128000. No hay evidencia suficiente para asegurar que μ > 128000 (no rechazar H0 no la prueba).

**Respuesta de la guía:** H0) μ ≤ μ0 = 128.000 U$s (pesimista); x̄c = 136.009,70 U$s. La recaudación media neta es 135.000 U$s, la hipótesis no se rechaza y no se recomienda continuar con esta compañía (equivalente: con valores brutos, crítico de 141.010 U$s).

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Valor alternativo neto** (el enunciado lo da sin descontar): μ₁ - 5.000 = 145.000 - 5.000 = 140.000
- **Región crítica** (del ensayo): H0: μ ≤ 128000,0, x̄c = 136,009,6973; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 136,009,6973), como la cátedra.
- **β** = P(x̄ ≤ x̄c | μ = 140.000) con Z = (x̄c - μ₁)/(σ/√n) = (136.009,6973 - 140.000)/6.250 = -0,6384 → β = 0,2616.
- **Potencia** 1-β = 0,7384.

**Conclusión:** La probabilidad pedida es β = 0,2616 (potencia 1-β = 0,7384).

**Respuesta de la guía:** β = φ(−0,6384) = 0,2616.

#### c) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **Valor neto**: lo que se compara con μ₀ es la media NETA: x̄ neto = x̄·(1 - 0,02) = 140.000·0,98 = 137.200.
- **1 · Planteo de hipótesis**: H0: μ ≤ 128000  vs  H1: μ > 128000.
- **Justificación de H0**:  
• H1: μ > 128.000 recoge lo que el enunciado quiere probar; H0: μ ≤ 128.000 es el complemento y lleva la igualdad (el valor de referencia 128.000).  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,2816.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 1,2816·σ/√n = 128.000 + 1,2816·12.500/√4 = 136.009,6973. Si x̄ > 136.009,6973 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 136.009,70; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 4 unidades y se calcula su media x̄. Si x̄ > 136,009,6973, se rechaza H0 → se puede asegurar que μ > 128000. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 128000.
- **6 · Cálculos y decisión**: x̄ = 137.200 → cae en la zona de rechazo.
- **Con μ₁ = 145.000**: β = 0,0752, potencia 1-β = 0,9248.
- **Equivalente en valores brutos**: la media bruta debería superar x̄c bruto = 138.785,41 (se obtuvo 140.000).
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0705. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,1, x̄ = 137,200 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: μ ≤ 128000. Se puede asegurar que μ > 128000.

**Respuesta de la guía:** La recaudación bruta deberá superar los 138.785,41 U$s; la hipótesis nula se rechazaría y convendría continuar con la compañía.

> 📝 *Notas de la transcripción:* En la Solución el fractil se escribe Z(0,90) = 1,2826 (el valor tabulado es 1,2816); con 1,2816 el crítico daría 136.009,70 igualmente, por lo que parece un error tipográfico. Valores b) usan 136.010 neto y 140.000 neto (= 145.000 bruto − 5.000).

<details><summary>Cómo lo concluye la guía</summary>

> a) Se ensaya la siguiente hipótesis pesimista porque hay riesgo económico: H0) μ ≤ μ0 = 128.000 U$s.
> Siendo el crítico: x̄c = 128.000 + Z(0,90)·12.500/√4 = 128.000 + 1,2826·12.500/√4 = 136.009,70 U$s.
> Esta hipótesis se rechazará si la compañía de cobranzas obtiene una recaudación media neta mayor o igual a 136.010 U$s (siendo este valor el crítico). Como se obtuvo una recaudación media bruta de 140.000 U$s, que equivale a un valor neto de 135.000 U$s, la hipótesis no se rechaza y no se recomienda continuar con esta compañía.
> Se obtiene el mismo resultado con valores brutos tomando μ0 = 133.000 U$s, con lo cual el valor crítico es de 141.010 U$s.
> b) β = P(x̄ < x̄c / μ = μ1) = φ((136.010 − 140.000)/(12.500/√4)) = φ(−0,6384) = 0,2616.
> c) En este caso la hipótesis que se ensaya también es pesimista: H0) μ ≤ μ0 = 128.000 U$s. Como se cobra el 2% de comisión, el bruto se calcula dividiendo el neto por 0,98, por lo tanto, la recaudación bruta deberá superar los 138.785,41 U$s. En este caso la hipótesis nula se rechazaría y convendría continuar con la compañía.

</details>

---

### I-26 · Problema 26 (pág. 8)

**Enunciado.** En una pieza fabricada que ha de acoplarse a otras piezas, hay una dimensión crítica cuyo valor medio debe ser aproximadamente de 11,5 cm. La variabilidad del proceso de fabricación está dada por el desvío estándar que vale 0,1 cm. El proceso se considera bajo control si con una muestra de n piezas, no hay motivos para pensar que la dimensión media es diferente de 11,5 cm.

- **a)** ¿Cuál deberá ser el tamaño de la muestra si se establece en 0,10 la probabilidad de revisar el proceso equivocadamente y en 0,05 la probabilidad de no revisarlo cuando la dimensión media es de 11,4 cm?
- **b)** ¿Cuáles serán los límites de control?
- **c)** ¿Cuál es la probabilidad de revisar el proceso cuando la dimensión media es de 11,46 cm?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ = 11,5 supone que cumple; H1: μ ≠ 11,5 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I); β = P(no rechazar H0 | μ = 11,4) = 0,05 (error de tipo II).  
• El ensayo es bilateral (sin dirección): la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ = 11,5  vs  H1: μ ≠ 11,5.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 11,5) = α = 0,1 y P(no rechazar H0 | μ = 11,4) = β = 0,05.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + 1,6449)·0,1/0,1]² = 10,8222 → n = 11.
- **Condición de rechazo**: x̄c = 11,4504 ; 11,5496  (con n = 11).
- **Regla de decisión**: Tomar una muestra de n = 11. Si la media muestral cae fuera del intervalo [11,4504, 11,5496] se rechaza H0.
- Con n = 11: β real = 0,0473, potencia real = 0,9527.

**Conclusión:** Tomar una muestra de n = 11. Si la media muestral cae fuera del intervalo [11,4504, 11,5496] se rechaza H0.

**Respuesta de la guía:** n = 11 piezas.

#### b) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ = 11,5 supone que cumple; H1: μ ≠ 11,5 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es bilateral (sin dirección): la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ = 11,5  vs  H1: μ ≠ 11,5  (α = 0,1).
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α/2) = 1,6449.
- **Condición de rechazo**: x̄c₁;x̄c₂ = μ₀ ∓ 1,6449·σ/√n = 11,5 ∓ 1,6449·0,1/√11 = 11,4504 ; 11,5496. Si x̄ < 11,4504 o x̄ > 11,5496 ⇒ se rechaza H0. Informados como la cátedra (hacia afuera): 11,45 ; 11,55.
- **Con μ₁ = 11,4**: β = 0,0473, potencia 1-β = 0,9527.
- **Regla de decisión**: Si en una muestra de 11 la media cae fuera de [11,4504 ; 11,5496] se rechaza H0.

**Conclusión:** Si en una muestra de 11 la media cae fuera de [11,4504 ; 11,5496] se rechaza H0.

**Respuesta de la guía:** LIC = x̄c1 = 11,45 cm y LSC = x̄c2 = 11,55 cm.

#### c) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ = 11,5, x̄c = 11,4504 ; 11,5496; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 11,4504 ; 11,5496), como la cátedra.
- **β** = P(x̄c₁ ≤ x̄ ≤ x̄c₂ | μ = 11,46) = Φ((11,5496 - 11,46)/0,0302) - Φ((11,4504 - 11,46)/0,0302) = 0,6234.
- **Potencia** 1-β = 0,3766.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,3766 (β = 0,6234).

**Respuesta de la guía:** 1–β = 0,3766.

> 📝 *Notas de la transcripción:* La Resp está en la página 9.

---

### I-27 · Problema 27 (pág. 9)

**Enunciado.** Un torno automático produce una pieza cuya longitud tiene distribución Normal con un desvío estándar de 0,1 cm. Si el torno está bien ajustado, el valor medio es de 2 cm, pero cuando la herramienta de corte adopta una posición incorrecta, dicho promedio se altera, aumentando o disminuyendo, sin llegar a modificarse el desvío estándar; en ese caso debe corregirse la posición de la herramienta. Una muestra de 10 piezas arrojó una longitud media de 2,04 cm.

- **a)** Si se establece en un 0,10 la probabilidad de concluir erróneamente que el torno está desajustado, ¿cuál sería la conclusión?
- **b)** Si el torno estuviera desajustado y la longitud media fuera de 1,95 cm, ¿cuál sería la probabilidad de no efectuar el ajuste?
- **c)** ¿Cuál debería ser el tamaño de la muestra si se desea reducir dicha probabilidad a 0,20?
- **d)** Dibujar las curvas Característica Operativa y de Potencia para ambos tamaños de muestra.

*Curvas OC y de potencia (Solución d)*

| n | μ1 | β | 1–β |
|---|---|---|---|
| 10 | 1,896 | 0,05 | 0,95 |
| 10 | 1,948 | 0,5 | 0,5 |
| 10 | 2 | 0,9 | 0,1 |
| 10 | 2,052 | 0,5 | 0,5 |
| 10 | 2,104 | 0,05 | 0,95 |
| 25 | 1,921 | 0,01 | 0,99 |
| 25 | 1,967 | 0,5 | 0,5 |
| 25 | 2 | 0,9 | 0,1 |
| 25 | 2,033 | 0,5 | 0,5 |
| 25 | 2,079 | 0,01 | 0,99 |

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '≠'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ = 2  vs  H1: μ ≠ 2.
- **Justificación de H0**:  
• H1: μ ≠ 2 recoge lo que el enunciado quiere probar; H0: μ = 2 es el complemento y lleva la igualdad (el valor de referencia 2).  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es bilateral (sin dirección): la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α/2) = 1,6449.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c₁;x̄c₂ = μ₀ ∓ 1,6449·σ/√n = 2 ∓ 1,6449·0,1/√10 = 1,948 ; 2,052. Si x̄ < 1,948 o x̄ > 2,052 ⇒ se rechaza H0. Informados como la cátedra (hacia afuera): 1,94 ; 2,06.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 10 unidades y se calcula su media x̄. Si x̄ < 1,948 o x̄ > 2,052, se rechaza H0 → se puede asegurar que μ ≠ 2. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ ≠ 2.
- **6 · Cálculos y decisión**: x̄ = 2,04 → no cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,2059. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,1, x̄ = 2,04 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ = 2. No hay evidencia suficiente para asegurar que μ ≠ 2 (no rechazar H0 no la prueba).

**Respuesta de la guía:** H0) μ = μ0 = 2 cm (bilateral); LIC = x̄c1 = 1,9479 cm y LSC = x̄c2 = 2,0521 cm; CR: Si x̄ < 1,9479 cm o x̄ > 2,0521 cm ⇒ Rechazo H0. Como x̄ = 2,04 cm, no se rechaza H0: el torno no necesita ajuste.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ = 2,0, x̄c = 1,948 ; 2,052; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 1,9479 ; 2,0521), como la cátedra.
- **β** = P(x̄c₁ ≤ x̄ ≤ x̄c₂ | μ = 1,95) = Φ((2,0521 - 1,95)/0,0316) - Φ((1,9479 - 1,95)/0,0316) = 0,5259.
- **Potencia** 1-β = 0,4741.

**Conclusión:** La probabilidad pedida es β = 0,5259 (potencia 1-β = 0,4741).

**Respuesta de la guía:** β = 0,5259.

#### c) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• H1: μ ≠ 2 recoge lo que el enunciado quiere probar; H0: μ = 2 es el complemento y lleva la igualdad (el valor de referencia 2).  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I); β = P(no rechazar H0 | μ = 1,95) = 0,2 (error de tipo II).  
• El ensayo es bilateral (sin dirección): la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ = 2  vs  H1: μ ≠ 2.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Condiciones**: P(rechazar H0 | μ = 2) = α = 0,1 y P(no rechazar H0 | μ = 1,95) = β = 0,2.
- **Tamaño de muestra**: n = [(Z_α + Z_β)·σ/(μ₀ - μ₁)]² = [(1,6449 + 0,8416)·0,1/0,05]² = 24,7302 → n = 25.
- **Condición de rechazo**: x̄c = 1,9671 ; 2,0329  (con n = 25).
- **Regla de decisión**: Tomar una muestra de n = 25. Si la media muestral cae fuera del intervalo [1,9671, 2,0329] se rechaza H0.
- Con n = 25: β real = 0,1962, potencia real = 0,8038.

**Conclusión:** Tomar una muestra de n = 25. Si la media muestral cae fuera del intervalo [1,9671, 2,0329] se rechaza H0. (Respecto de la muestra actual de 10: Δn = 15.)

**Respuesta de la guía:** n = 25 piezas.

#### d) Curva característica operativa / de potencia ℹ️

*Qué pide:* Tabular β y 1-β para varios valores del parámetro y graficar la curva OC (β) y la de potencia (1-β).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- Se toman valores de μ del lado de H1 (cola bilateral), con n = 10 y α = 0,1; para cada uno se calcula β = P(no rechazar H0 | μ) y la potencia 1-β.
- En el eje X va el parámetro μ; en el eje Y la probabilidad (β para la curva OC, 1-β para la de potencia). Marcá al menos 3 puntos con sus valores.

**Conclusión:** Tabla de puntos para graficar las curvas (ver abajo).

**Respuesta de la guía:** Tabla: n = 10: μ1 = 1,896 / 1,948 / 2,000 / 2,052 / 2,104 → β = 0,05 / 0,50 / 0,90 / 0,50 / 0,05 (1–β = 0,95 / 0,50 / 0,10 / 0,50 / 0,95). n = 25: μ1 = 1,921 / 1,967 / 2,000 / 2,033 / 2,079 → β = 0,01 / 0,50 / 0,90 / 0,50 / 0,01 (1–β = 0,99 / 0,50 / 0,10 / 0,50 / 0,99).

> 📝 *Notas de la transcripción:* En la Solución la RD dice 'por debajo de 1,94 cm o por encima de 2,06 cm' y en b) la fórmula muestra 2,05 y 1,94, mientras que los críticos calculados son 1,9479 y 2,0521 cm (el resultado β = 0,5259 corresponde a los críticos 1,9479/2,0521). Para n = 25 la tabla da β = 0,90 en μ1 = 2,000.

<details><summary>Cómo lo concluye la guía</summary>

> a) Hay que ensayar una hipótesis bilateral, la cual no tiene criterio, adoptando como μ0 el valor deseado para el ajuste óptimo del torno: H0) μ = μ0 = 2 cm. α = 0,10; n = 10 piezas.
> x̄c1 = LIC = 2 − 1,6449·0,1/√10 = 1,9479 cm y x̄c2 = LSC = 2 + 1,6449·0,1/√10 = 2,0521 cm.
> La regla de decisión es: RD: Si de una muestra de 10 piezas la longitud promedio está por debajo de 1,94 cm o está por encima de 2,06 cm, detengo el torno y efectúo el ajuste de la pieza.
> Como la muestra de 10 piezas arrojó una longitud media de 2,04 cm, no puedo rechazar la H0. Por lo tanto, se considera que el torno no necesita ajuste.
> b) β = P(x̄c1 ≤ x̄ ≤ x̄c2 / μ = μ1) = φ((2,05 − 1,95)/(0,1/√10)) − φ((1,94 − 1,95)/(0,1/√10)) = 0,5259.
> c) Z(0,80) = 0,8416; n = [(1,6449 + 0,8416)·0,1/(2 − 1,95)]² = 25. Quiere decir que el tamaño de la muestra debe ser de 25 piezas.

</details>

---

### I-28 · Problema 28 (pág. 10)

**Enunciado.** Las ventas mensuales de un producto son variables con un valor medio de 700.000 unidades. Durante 5 meses se ha desarrollado una campaña publicitaria registrándose los siguientes volúmenes de venta en miles de unidades: 607; 725; 784; 790 y 810.

- **a)** ¿Se puede considerar que los datos arrojan una concluyente evidencia para poder afirmar con un riesgo máximo del 1% que la campaña ha sido efectiva?
- **b)** Estimar el volumen medio de ventas con un 95% de confianza.
- **c)** ¿Durante cuántos meses más habría que continuar con la campaña si se pretende disminuir en un 50% el error muestral de la estimación anterior?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **Procesar la muestra**: n = 5, x̄ = Σxᵢ/n = 743.200, S = √[Σ(xᵢ - x̄)²/(n-1)] = 82.460,2935.
- **1 · Planteo de hipótesis**: H0: μ ≤ 700000  vs  H1: μ > 700000.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≤ 700.000 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ > 700.000 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,01 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,01 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student, ν = número de grados de libertad = 4. t(1-α) = 3,7469.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 3,7469·S/√n = 700.000 + 3,7469·82.460,2935/√5 = 838.177,544. Si x̄ > 838.177,544 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 838.177,55; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 5 unidades y se calcula su media x̄. Si x̄ > 838,177,544, se rechaza H0 → se puede asegurar que μ > 700000. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 700000.
- **6 · Cálculos y decisión**: x̄ = 743.200 → no cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,1532. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,01, x̄ = 743,200 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ ≤ 700000. No hay evidencia suficiente para asegurar que μ > 700000 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No, no se puede afirmar que la campaña fue efectiva.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 95% de confianza mediante un intervalo de confianza. Como σ no se conoce se usa S y t de Student (ν = n-1).

- **Procesar la muestra**: n = 5, x̄ = Σxᵢ/n = 743.200, S = √[Σ(xᵢ - x̄)²/(n-1)] = 82.460,2935.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **Distribución**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student con ν = número de grados de libertad = n-1 = 4. t(0,975; 4) = 2,7764.
- **Límites**: A;B = x̄ ∓ t·S/√n = 743.200 ∓ 2,7764·82.460,2935/√5 = 743.200 ∓ 102.387,9777.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 640.812,02 y 845.587,98, afirmándolo con un 95% de confianza, o sea: P(640.812,02 ≤ μ ≤ 845.587,98) = 0,95 (límites redondeados hacia afuera; sin redondear: 640.812,022311 y 845.587,977689).

**Respuesta de la guía:** Entre 640.812,02 y 845.587,98 unidades.

#### c) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para reducir un 50% el error (o la relación entre límites). Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Procesar la muestra**: n = 5, x̄ = Σxᵢ/n = 743.200, S = √[Σ(xᵢ - x̄)²/(n-1)] = 82.460,2935.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)  
• El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n (con t se itera porque ν depende de n).
- **Error buscado**: e = e_actual·(1 - 0,5) = 102.387,9777·0,5 = 51.193,9888.
- **Fórmula** (σ desconocido): n = (t(1-α/2; n-1)·S/e)². Como t depende de n se itera: [11, 13, 13].

**Conclusión:** El tamaño de muestra necesario es n = 13. Como ya se tomaron 5, hay que agregar Δn = 13 - 5 = 8 unidades más.

**Respuesta de la guía:** 8 meses más.

---

### I-29 · Problema 29 (pág. 10)

**Enunciado.** El departamento de producción de una empresa ha resuelto instalar un nuevo dispositivo en el proceso productivo si existe una razonable seguridad de que la producción media por hora aumenta en un 10% como mínimo. Actualmente la producción media es de 100 unidades por hora. Se establece en un 5% el riesgo máximo de instalar equivocadamente el nuevo dispositivo y, a efectos de tomar una decisión, se realiza una prueba durante 50 horas obteniéndose un promedio de 120 unidades con un desvío estándar de 10 unidades.

*Establecer la hipótesis adecuada e indicar ¿qué decisión se tomaría?*

*Tema detectado por la app: Media de 1 población (μ).*

#### Resolución (Diseñar el ensayo (H0, n, valor crítico, regla de decisión)) ℹ️

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≤ 100 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ > 100 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ ≤ 100  vs  H1: μ > 100  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,6449.
- **Condición de rechazo**: x̄c = μ₀ + 1,6449·σ/√n = 100 + 1,6449·10/√50 = 102,3262. Si x̄ > 102,3262 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 102,33; la decisión se toma con el valor exacto.
- **Regla de decisión**: Si en una muestra de 50 la media es mayor que 102,3262 se rechaza H0.
- **Media alternativa** (la que se detecta con 1-β = 0,9): μ₁ = x̄c + Z(1-β)·σ/√n = 102,3262 + 1,2816·10/√50 = 104,1386.

**Conclusión:** Si en una muestra de 50 la media es mayor que 102,3262 se rechaza H0. La media alternativa definida por β = 0,1 es μ₁ = 104,1386.

**Respuesta de la guía:** H0) μ ≤ μ0 = 110 unidades. Se toma la decisión de instalar el nuevo dispositivo, se puede asegurar que la producción por hora promedio aumenta.

---

### I-30 · Problema 30 (pág. 10)

**Enunciado.** Una pequeña fábrica de pinturas ha desarrollado un producto que puede competir en calidad y precio con el de la empresa líder del ramo. Se ha establecido la conveniencia de su lanzamiento si se puede asegurar una venta media mayor que 100 litros por cliente y por año. A tal efecto, se enviaron muestras gratis a 16 posibles clientes, interrogándoselos luego sobre el volumen anual de pintura que estarían dispuestos a comprar. Se obtuvo así una media muestral de 114 litros con un desvío estándar de 18 litros.

- **a)** Asumiendo un riesgo del 10%, ¿cuál sería la decisión recomendada?
- **b)** Calcular los límites de confianza del 90% para el volumen medio de pintura.
- **c)** ¿A cuántos clientes más habría que enviar muestras para poder dar un intervalo cuya amplitud sea la mitad del anterior?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ℹ️

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ ≤ 100  vs  H1: μ > 100.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≤ 100 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ > 100 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student, ν = número de grados de libertad = 15. t(1-α) = 1,3406.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 1,3406·S/√n = 100 + 1,3406·18/√16 = 106,0327. Si x̄ > 106,0327 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 106,04; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 16 unidades y se calcula su media x̄. Si x̄ > 106,0327, se rechaza H0 → se puede asegurar que μ > 100. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 100.
- **6 · Cálculos y decisión**: x̄ = 114 → cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0036. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,1, x̄ = 114 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: μ ≤ 100. Se puede asegurar que μ > 100.

**Respuesta de la guía:** Se toma la decisión de lanzar el nuevo producto, se puede asegura que el volumen de venta anual promedio tiene un valor mayor que 100 litros.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 90% de confianza mediante un intervalo de confianza. Como σ no se conoce se usa S y t de Student (ν = n-1).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **Distribución**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student con ν = número de grados de libertad = n-1 = 15. t(0,95; 15) = 1,7531.
- **Límites**: A;B = x̄ ∓ t·S/√n = 114 ∓ 1,7531·18/√16 = 114 ∓ 7,8887.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 106,11 y 121,89, afirmándolo con un 90% de confianza, o sea: P(106,11 ≤ μ ≤ 121,89) = 0,9 (límites redondeados hacia afuera; sin redondear: 106,111273 y 121,888727).

**Respuesta de la guía:** Entre 106,11 y 121,89 litros.

#### c) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para reducir un 50% el error (o la relación entre límites). Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)  
• El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n (con t se itera porque ν depende de n).
- **Error buscado**: e = e_actual·(1 - 0,5) = 7,8887·0,5 = 3,9444.
- **Fórmula** (σ desconocido): n = (t(1-α/2; n-1)·S/e)². Como t depende de n se itera: [58, 59, 59].

**Conclusión:** El tamaño de muestra necesario es n = 59. Como ya se tomaron 16, hay que agregar Δn = 59 - 16 = 43 unidades más.

**Respuesta de la guía:** 43 clientes más.

---

### I-31 · Problema 31 (pág. 10)

**Enunciado.** Una empresa radicada en el interior del país comenzará una campaña de ventas si el ingreso medio de las familias de la zona supera los 1.000 U$s por mes. A efectos de tomar una decisión se toma una muestra de 100 familias registrándose un ingreso medio en el último mes de 1.100 U$s y un desvío estándar de 923 U$s. Asumiendo una probabilidad de 0,01 de comenzar la campaña equivocadamente:

- **a)** ¿Se aconseja comenzar la campaña de ventas?
- **b)** Calcular los límites de confianza del 90% para el ingreso medio de esta zona.
- **c)** Recalcular tamaño de muestra para reducir a la mitad el error muestral del intervalo hallado anteriormente.

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ ≤ 1000  vs  H1: μ > 1000.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≤ 1.000 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ > 1.000 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,01 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,01 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student, ν = número de grados de libertad = 99. t(1-α) = 2,3646.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 2,3646·S/√n = 1.000 + 2,3646·923/√100 = 1.218,2531. Si x̄ > 1.218,2531 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 1.218,26; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 100 unidades y se calcula su media x̄. Si x̄ > 1,218,2531, se rechaza H0 → se puede asegurar que μ > 1000. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 1000.
- **6 · Cálculos y decisión**: x̄ = 1.100 → no cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,1406. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,01, x̄ = 1,100 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ ≤ 1000. No hay evidencia suficiente para asegurar que μ > 1000 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No se aconseja comenzar la campaña, no se puede asegurar que los ingresos promedio por familia de la región superen los 1.000 U$s.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 90% de confianza mediante un intervalo de confianza. Como σ no se conoce se usa S y t de Student (ν = n-1).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **Distribución**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student con ν = número de grados de libertad = n-1 = 99. t(0,95; 99) = 1,6604.
- **Límites**: A;B = x̄ ∓ t·S/√n = 1.100 ∓ 1,6604·923/√100 = 1.100 ∓ 153,2541.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 946,74 y 1.253,26, afirmándolo con un 90% de confianza, o sea: P(946,74 ≤ μ ≤ 1.253,26) = 0,9 (límites redondeados hacia afuera; sin redondear: 946,745896 y 1.253,254104).

**Respuesta de la guía:** Entre 946,74 y 1.253,26 U$s.

#### c) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para reducir un 50% el error (o la relación entre límites). Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)  
• El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n (con t se itera porque ν depende de n).
- **Error buscado**: e = e_actual·(1 - 0,5) = 153,2541·0,5 = 76,6271.
- **Fórmula** (σ desconocido): n = (t(1-α/2; n-1)·S/e)². Como t depende de n se itera: [400, 395, 395].

**Conclusión:** El tamaño de muestra necesario es n = 395. Como ya se tomaron 100, hay que agregar Δn = 395 - 100 = 295 unidades más.

**Respuesta de la guía:** n = 395 familias.

> 📝 *Notas de la transcripción:* La Resp está en la página 11.

---

### I-32 · Problema 32 (pág. 11)

**Enunciado.** Una empresa que produce galletitas desea controlar el funcionamiento de una máquina empaquetadora que, en condiciones normales, el peso medio de los paquetes debe ser 250 gramos. Se tomó una muestra de 20 paquetes obteniéndose un peso medio de 280 gramos y una desviación estándar de 15 gramos, y se establece en un 1% el riesgo máximo de detener y revisar la máquina si funciona correctamente. Luego de evaluar los resultados de la muestra se decide detener la máquina y revisarla.

- **a)** ¿Se considera que la decisión tomada es correcta?
- **b)** ¿Estimar con un 1% de riesgo el peso promedio de los paquetes?
- **c)** ¿Cómo se disminuye el error de la estimación anterior en un 30%?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ ≤ 250  vs  H1: μ > 250.
- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≤ 250 supone que cumple; H1: μ > 250 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,01 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,01 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student, ν = número de grados de libertad = 19. t(1-α) = 2,5395.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 2,5395·S/√n = 250 + 2,5395·15/√20 = 258,5177. Si x̄ > 258,5177 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 258,52; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 20 unidades y se calcula su media x̄. Si x̄ > 258,5177, se rechaza H0 → se puede asegurar que μ > 250. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 250.
- **6 · Cálculos y decisión**: x̄ = 280 → cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,01, x̄ = 280 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: μ ≤ 250. Se puede asegurar que μ > 250.

**Respuesta de la guía:** Sí, se pudo asegurar que la máquina estaba fuera de control.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 99% de confianza mediante un intervalo de confianza. Como σ no se conoce se usa S y t de Student (ν = n-1).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **Distribución**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student con ν = número de grados de libertad = n-1 = 19. t(0,995; 19) = 2,8609.
- **Límites**: A;B = x̄ ∓ t·S/√n = 280 ∓ 2,8609·15/√20 = 280 ∓ 9,5959.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 270,40 y 289,60, afirmándolo con un 99% de confianza, o sea: P(270,40 ≤ μ ≤ 289,60) = 0,99 (límites redondeados hacia afuera; sin redondear: 270,404134 y 289,595866).

**Respuesta de la guía:** Entre 270,40 y 289,60 gramos.

#### c) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para reducir un 30% el error (o la relación entre límites). Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)  
• El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n (con t se itera porque ν depende de n).
- **Error buscado**: e = e_actual·(1 - 0,3) = 9,5959·0,7 = 6,7171.
- **Fórmula** (σ desconocido): n = (t(1-α/2; n-1)·S/e)². Como t depende de n se itera: [35, 38, 37, 37].

**Conclusión:** El tamaño de muestra necesario es n = 37. Como ya se tomaron 20, hay que agregar Δn = 37 - 20 = 17 unidades más.

**Respuesta de la guía:** Aumentando el tamaño de la muestra a 37 paquetes.

---

### I-33 · Problema 33 (pág. 11)

**Enunciado.** Los siguientes datos representan los tiempos de armado de circuitos electrónicos elegidos al azar: Tpo. (en minutos) | Cantidad: 9,5 – 9,8 | 4; 9,8 – 10,1 | 10; 10,1 – 10,4 | 35; 10,4 – 10,7 | 12; 10,7 – 11,0 | 8; 11,0 – 11,3 | 6. Se supone que el tiempo necesario para armar una unidad es una variable aleatoria con un desvío estándar de σ = 0,65 minutos.

- **a)** Basándose en esta muestra, ¿existe alguna razón para creer, con un nivel de confianza del 95%, que el tiempo medio de armado es mayor de 10,25 minutos?
- **b)** Si no se conociera el desvío estándar de la variable, ¿se arribaría a la misma conclusión que el punto anterior?

| Tpo. (en minutos) desde | Tpo. (en minutos) hasta | Cantidad |
|---|---|---|
| 9,5 | 9,8 | 4 |
| 9,8 | 10,1 | 10 |
| 10,1 | 10,4 | 35 |
| 10,4 | 10,7 | 12 |
| 10,7 | 11 | 8 |
| 11 | 11,3 | 6 |

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **Procesar la muestra**: n = 75, x̄ = Σxᵢ/n = 10,362, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,3716.
- **1 · Planteo de hipótesis**: H0: μ ≤ 10,25  vs  H1: μ > 10,25.
- **Justificación de H0**:  
• H1: μ > 10,25 recoge lo que el enunciado quiere probar; H0: μ ≤ 10,25 es el complemento y lleva la igualdad (el valor de referencia 10,25).  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,6449.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 1,6449·σ/√n = 10,25 + 1,6449·0,65/√75 = 10,3735. Si x̄ > 10,3735 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 10,38; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 75 unidades y se calcula su media x̄. Si x̄ > 10,3735, se rechaza H0 → se puede asegurar que μ > 10,25. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 10,25.
- **6 · Cálculos y decisión**: x̄ = 10,362 → no cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0678. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,05, x̄ = 10,362 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ ≤ 10,25. No hay evidencia suficiente para asegurar que μ > 10,25 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No, no hay razón para creer que el tiempo medio es mayor que 10,25 minutos.

#### b) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **Procesar la muestra**: n = 75, x̄ = Σxᵢ/n = 10,362, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,3716.
- **1 · Planteo de hipótesis**: H0: μ ≤ 10,25  vs  H1: μ > 10,25.
- **Justificación de H0**:  
• H1: μ > 10,25 recoge lo que el enunciado quiere probar; H0: μ ≤ 10,25 es el complemento y lleva la igualdad (el valor de referencia 10,25).  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student, ν = número de grados de libertad = 74. t(1-α) = 1,6657.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 1,6657·S/√n = 10,25 + 1,6657·0,3716/√75 = 10,3215. Si x̄ > 10,3215 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 10,33; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 75 unidades y se calcula su media x̄. Si x̄ > 10,3215, se rechaza H0 → se puede asegurar que μ > 10,25. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 10,25.
- **6 · Cálculos y decisión**: x̄ = 10,362 → cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0055. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,05, x̄ = 10,362 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: μ ≤ 10,25. Se puede asegurar que μ > 10,25.

**Respuesta de la guía:** No se arriba a la misma conclusión, en este caso se tiene seguridad para afirmar que el tiempo medio de armado es mayor a 10,25 minutos.

---

### I-34 · Problema 34 (pág. 11)

**Enunciado.** Por investigaciones anteriores se sabe que el peso promedio de los cerdos de 6 semanas es de 45 kg con un σ = 8 kg. Se ensaya un nuevo tipo de alimentación con una población total de 1.200 cerdos de un establecimiento, seleccionando una muestra al azar de 36 de ellos arrojando un peso medio de 47 Kg. Se considera que el desvío histórico se mantiene.

- **a)** ¿Se puede decir que se ha incrementado el peso promedio de los cerdos?
- **b)** Estimar con un 90% de confianza el peso promedio de la población de cerdos de dicho establecimiento.
- **c)** Estimar con un 90% de confianza el peso total de la población de cerdos de dicho establecimiento.
- **d)** ¿Cuántos cerdos más habría que seleccionar de la población para reducir en un 70% el error de estimación?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

> ⚠️ El enunciado no fija el riesgo α: se eligió α = 0,05. En el examen hay que elegirlo y JUSTIFICARLO antes de ver la muestra (p. ej. «0,05, no porque sea estándar, sino porque el perito tiene que ser imparcial»); una vez fijado, α no se toca. El valor a posteriori α* se muestra solo como dato: no se decide con él.

- **1 · Planteo de hipótesis**: H0: μ ≤ 45  vs  H1: μ > 45.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≤ 45 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ > 45 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Población finita** (N = 1.200): factor √((N-n)/N) = 0,9849 → σ·factor = 7,8791. (El apunte y el profesor usan √((N-n)/(N-1)) = 0,9853 y aceptan N: «el uno mucho no hace»; la app usa N porque así reproduce la guía.)
- **3 · Estadístico de prueba**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α) = 1,6449.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n). Como la población es finita (N = 1.200) y se muestrea sin reposición, el error estándar lleva el factor de corrección √((N-n)/(N-1)) (la app usa √((N-n)/N), que reproduce la guía; el profesor acepta los dos: «el uno mucho no hace»).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 1,6449·σ/√n = 45 + 1,6449·7,8791/√36 = 47,16. Si x̄ > 47,16 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 47,16; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 36 unidades y se calcula su media x̄. Si x̄ > 47,16, se rechaza H0 → se puede asegurar que μ > 45. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 45.
- **6 · Cálculos y decisión**: x̄ = 47 → no cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0639. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,05, x̄ = 47 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ ≤ 45. No hay evidencia suficiente para asegurar que μ > 45 (no rechazar H0 no la prueba).

**Respuesta de la guía:** Si se toma un 6,39% o más de riesgo, la respuesta es “si”; caso contrario, la respuesta es: “no puede asegurarse que el peso medio de los cerdos se haya incrementado”.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 90% de confianza mediante un intervalo de confianza. Como σ es conocido se usa Z.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n). Como la población es finita (N = 1.200) y se muestrea sin reposición, el error estándar lleva el factor de corrección √((N-n)/(N-1)) (la app usa √((N-n)/N), que reproduce la guía; el profesor acepta los dos: «el uno mucho no hace»).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α/2) = Z(0,95) = 1,6449.
- **Límites**: A;B = x̄ ∓ Z·σ/√n · √((N-n)/N) = 47 ∓ 1,6449·8/√36 · √((N-n)/N) = 47 ∓ 2,16.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 44,84 y 49,16, afirmándolo con un 90% de confianza, o sea: P(44,84 ≤ μ ≤ 49,16) = 0,9 (límites redondeados hacia afuera; sin redondear: 44,840009 y 49,159991).

**Respuesta de la guía:** Entre 44,84 y 49,16 kg.

#### c) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 90% de confianza mediante un intervalo de confianza. Como σ es conocido se usa Z. Se pide el TOTAL: multiplicá los límites por N.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n). Como la población es finita (N = 1.200) y se muestrea sin reposición, el error estándar lleva el factor de corrección √((N-n)/(N-1)) (la app usa √((N-n)/N), que reproduce la guía; el profesor acepta los dos: «el uno mucho no hace»).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α/2) = Z(0,95) = 1,6449.
- **Límites**: A;B = x̄ ∓ Z·σ/√n · √((N-n)/N) = 47 ∓ 1,6449·8/√36 · √((N-n)/N) = 47 ∓ 2,16.
- **Total poblacional** T = N·μ: se multiplican los límites por N = 1.200.

**Conclusión:** El total poblacional estará entre 53.808,01 y 58.991,99 (límites redondeados hacia afuera; sin redondear: 53.808,011284 y 58.991,988716): P(53.808,01 ≤ T ≤ 58.991,99) = 0,9

**Respuesta de la guía:** Entre 53.808,01 y 58.991,99 kg.

#### d) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para reducir un 70% el error (o la relación entre límites). Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n). Como la población es finita (N = 1.200) y se muestrea sin reposición, el error estándar lleva el factor de corrección √((N-n)/(N-1)) (la app usa √((N-n)/N), que reproduce la guía; el profesor acepta los dos: «el uno mucho no hace»).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n.
- **Error buscado**: e = e_actual·(1 - 0,7) = 2,16·0,3 = 0,648.
- **Fórmula** (σ conocido): n = (Z·σ/e)² = (1,6449·8/0,648)² = 412,3711 → se redondea hacia arriba.
- **Población finita**: n∞ = 413; n = N·n∞/(N + n∞) = 1.200·413/(1.200 + 413) → n = 308.

**Conclusión:** El tamaño de muestra necesario es n = 308. Como ya se tomaron 36, hay que agregar Δn = 308 - 36 = 272 unidades más.

**Respuesta de la guía:** 272 cerdos más, seleccionados de la población de 1.200.

---

### I-35 · Problema 35 (pág. 11)

**Enunciado.** El tiempo estándar (tiempo promedio) para el montaje de un conjunto es de 360 segundos con un desvío estándar de 50 segundos:

- **a)** ¿Dentro de qué límites variará el tiempo medio durante una jornada de 8 horas, para que se pueda decir que el operario trabaja en forma estándar? (Se acepta un error de tipo I de 0,05).
- **b)** ¿Cuál será el error de tipo II si el operario realmente está utilizando un tiempo medio 8% superior al estándar y si las muestras que se utilizan para este control son de 20 conjuntos durante el período controlado?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ = 360 supone que cumple; H1: μ ≠ 360 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es bilateral (sin dirección): la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ = 360  vs  H1: μ ≠ 360  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α/2) = 1,96.
- **Condición de rechazo**: x̄c₁;x̄c₂ = μ₀ ∓ 1,96·σ/√n = 360 ∓ 1,96·50/√80 = 349,0435 ; 370,9565. Si x̄ < 349,0435 o x̄ > 370,9565 ⇒ se rechaza H0. Informados como la cátedra (hacia afuera): 349,04 ; 370,96.
- **Regla de decisión**: Si en una muestra de 80 la media cae fuera de [349,0435 ; 370,9565] se rechaza H0.

**Conclusión:** Si en una muestra de 80 la media cae fuera de [349,0435 ; 370,9565] se rechaza H0.

**Respuesta de la guía:** De una muestra de 80 conjuntos, los límites de control son: P(349,04" ≤ x̄ ≤ 370,96") = 0,95.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ = 360,0, x̄c = 338,0869 ; 381,9131; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 338,0869 ; 381,9131), como la cátedra.
- **β** = P(x̄c₁ ≤ x̄ ≤ x̄c₂ | μ = 388,8) = Φ((381,9131 - 388,8)/11,1803) - Φ((338,0869 - 388,8)/11,1803) = 0,2689.
- **Potencia** 1-β = 0,7311.

**Conclusión:** La probabilidad pedida es β = 0,2689 (potencia 1-β = 0,7311).

**Respuesta de la guía:** β = 0,2690.

---

### I-36 · Problema 36 (pág. 12)

**Enunciado.** Un fabricante de azúcar envasa en bolsas de papel de 1 kg lo que es correcto cuando el proceso está bajo control. Periódicamente se toma una muestra de 9 unidades, de un lote de producción, para controlar el proceso de embolsado. Sobre un lote de 1.400 bolsas terminadas, se tomó una muestra al azar arrojando una media que resultó de 1,10 kg y un desvío de 0,15 kg.

- **a)** Plantear la hipótesis adecuada al problema y determinar si el proceso se encuentra fuera de control, a la luz de los datos obtenidos, para un riesgo del 10%.
- **b)** Estimar para un 95% de confianza el peso promedio del lote producido.
- **c)** ¿Cuántas bolsas más habría que añadir a la muestra para reducir el error a 0,01 kg?

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ ≤ 1  vs  H1: μ > 1.
- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ ≤ 1 supone que cumple; H1: μ > 1 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Población finita** (N = 1.400): factor √((N-n)/N) = 0,9968 → σ·factor = 0,1495. (El apunte y el profesor usan √((N-n)/(N-1)) = 0,9971 y aceptan N: «el uno mucho no hace»; la app usa N porque así reproduce la guía.)
- **3 · Estadístico de prueba**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student, ν = número de grados de libertad = 8. t(1-α) = 1,3968.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».) Como la población es finita (N = 1.400) y se muestrea sin reposición, el error estándar lleva el factor de corrección √((N-n)/(N-1)) (la app usa √((N-n)/N), que reproduce la guía; el profesor acepta los dos: «el uno mucho no hace»).
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 1,3968·S/√n = 1 + 1,3968·0,1495/√9 = 1,0696. Si x̄ > 1,0696 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 1,07; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 9 unidades y se calcula su media x̄. Si x̄ > 1,0696, se rechaza H0 → se puede asegurar que μ > 1. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 1.
- **6 · Cálculos y decisión**: x̄ = 1,1 → cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0399. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,1, x̄ = 1,1 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: μ ≤ 1. Se puede asegurar que μ > 1.

**Respuesta de la guía:** H0) μ ≤ μ0 = 1 kg; x̄c = 1,07 kg; CR: Si x̄ > 1,07 kg ⇒ Rechazo H0. Como x̄ = 1,10 kg se rechaza H0: hay razones suficientes para afirmar que el proceso se encuentra fuera de control.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la media poblacional μ con un 95% de confianza mediante un intervalo de confianza. Como σ no se conoce se usa S y t de Student (ν = n-1).

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».) Como la población es finita (N = 1.400) y se muestrea sin reposición, el error estándar lleva el factor de corrección √((N-n)/(N-1)) (la app usa √((N-n)/N), que reproduce la guía; el profesor acepta los dos: «el uno mucho no hace»).
- **Distribución**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student con ν = número de grados de libertad = n-1 = 8. t(0,975; 8) = 2,306.
- **Límites**: A;B = x̄ ∓ t·S/√n · √((N-n)/N) = 1,1 ∓ 2,306·0,15/√9 · √((N-n)/N) = 1,1 ∓ 0,1149.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 0,985 y 1,215, afirmándolo con un 95% de confianza, o sea: P(0,985 ≤ μ ≤ 1,215) = 0,95 (límites redondeados hacia afuera; sin redondear: 0,985071 y 1,214929).

**Respuesta de la guía:** Entre 0,985 kg y 1,215 kg (1,1 ± 0,1149), con un 95% de confianza.

#### c) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para un error máximo e = 0,01. Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».) Como la población es finita (N = 1.400) y se muestrea sin reposición, el error estándar lleva el factor de corrección √((N-n)/(N-1)) (la app usa √((N-n)/N), que reproduce la guía; el profesor acepta los dos: «el uno mucho no hace»).  
• El tamaño de muestra sale de despejar n del error e = (fractil)·σ/√n (con t se itera porque ν depende de n).
- **Fórmula** (σ desconocido): n = (t(1-α/2; n-1)·S/e)². Como t depende de n se itera: [886, 867, 867].
- **Población finita**: n∞ = 867; n = N·n∞/(N + n∞) = 1.400·867/(1.400 + 867) → n = 536.

**Conclusión:** El tamaño de muestra necesario es n = 536. Como ya se tomaron 9, hay que agregar Δn = 536 - 9 = 527 unidades más.

**Respuesta de la guía:** n∞ = 867; n = 1.400·867/(1.400 + 867) = 536 bolsas en total, o sea 527 bolsas más.

> 📝 *Notas de la transcripción:* b) 2,306·0,05·√(1.391/1.400) = 0,1149 según la guía; el cálculo directo da ≈ 0,1151 (redondeo). El planteo usa hipótesis unilateral aunque el enunciado sugiere bilateral (la propia Solución lo aclara).

<details><summary>Cómo lo concluye la guía</summary>

> a) De acuerdo a lo planteado por el problema se debería ensayar una hipótesis bilateral, pero como la pregunta estipula que se analice a la luz de los datos obtenidos, ensayamos la siguiente hipótesis: H0) μ ≤ μ0 = 1 kg, porque se sospecha que el verdadero valor de μ es mayor que 1 kg.
> x̄c = μ0 + t(0,90;8)·(s/√n)·√((N−n)/N) = 1 + 1,3968·(0,15/√9)·√((1.400−9)/1.400) = 1,07 kg.
> La regla de decisión es: RD: Si de una muestra de 9 bolsas el peso promedio es mayor que 1,07 kg, detengo el proceso para revisarlo. Como la muestra de 9 bolsas arrojó un peso promedio de 1,10 kg, puedo rechazar la H0. Por lo tanto, hay razones suficientes para afirmar que el proceso se encuentra fuera de control.
> Se concluye que el peso promedio del lote producido de 1.400 bolsas estará comprendido entre 0,985 kg y 1,215 kg, afirmándolo con un 95% de confianza, o sea: P(0,985 kg ≤ μ ≤ 1,215 kg) = 0,95. Para un error muestral de e = 0,1149 kg.
> c) El resultado se obtiene con n∞ = 867. De manera que se debe corregir el resultado con la expresión: n = N·n∞/(N + n∞) = 1.400·867/(1.400 + 867) = 536. Se necesitan un total de 536 bolsas, o sea que se necesitarán incluir en la muestra obtenida 527 bolsas más.

</details>

---

### I-37 · Problema 37 (pág. 12)

**Enunciado.** El consejo estatal formado para controlar la calidad de agua selecciona cada semana 5 muestras de una fuente de abastecimiento y determina la concentración promedio de una sustancia tóxica. Los siguientes datos son las cantidades promedio en partes por millón, de la sustancia tóxica, durante 12 semanas: Semana: 1 - 2 - 3 - 4 - 5 - 6 - 7 - 8 - 9 - 10 - 11 - 12; Media: 5,2 - 4,9 - 5,5 - 5,4 - 4,8 - 4,6 - 5,5 - 4,7 - 5,1 - 4,5 - 5,8 - 5,6.

- **a)** Si se toma como valor nominal un promedio de 5 ppm con un σ = 0,5 ppm, obtener, para un riesgo del 5%, los límites de control para la concentración promedio. ¿Existe alguna razón para alarmarse para este período?
- **b)** ¿Cuál es la probabilidad de tener una concentración media, en la semana, de 6,6 ppm?
- **c)** ¿Cuál es la probabilidad de detectar un desplazamiento en el valor de la concentración media de 5 ppm a 5,25 ppm?

| Semana | Media (ppm) |
|---|---|
| 1 | 5,2 |
| 2 | 4,9 |
| 3 | 5,5 |
| 4 | 5,4 |
| 5 | 4,8 |
| 6 | 4,6 |
| 7 | 5,5 |
| 8 | 4,7 |
| 9 | 5,1 |
| 10 | 4,5 |
| 11 | 5,8 |
| 12 | 5,6 |

*Tema detectado por la app: Media de 1 población (μ).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Procesar la muestra**: n = 12, x̄ = Σxᵢ/n = 5,1333, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,4313.
- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: μ = 5 supone que cumple; H1: μ ≠ 5 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es bilateral (sin dirección): la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: μ = 5  vs  H1: μ ≠ 5  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Distribución**: x̄ es normal y al estandarizar se divide por el parámetro σ (una constante): sigue siendo normal → Z. Z(1-α/2) = 1,96.
- **Condición de rechazo**: x̄c₁;x̄c₂ = μ₀ ∓ 1,96·σ/√n = 5 ∓ 1,96·0,5/√5 = 4,5617 ; 5,4383. Si x̄ < 4,5617 o x̄ > 5,4383 ⇒ se rechaza H0. Informados como la cátedra (hacia afuera): 4,56 ; 5,44.
- **Regla de decisión**: Si en una muestra de 5 la media cae fuera de [4,5617 ; 5,4383] se rechaza H0.
- **Control de cada período** (cada valor es la media de una muestra de 5): 1: 5,2, 2: 4,9, 3: 5,5 ✗, 4: 5,4, 5: 4,8, 6: 4,6, 7: 5,5 ✗, 8: 4,7, 9: 5,1, 10: 4,5 ✗, 11: 5,8 ✗, 12: 5,6 ✗.

**Conclusión:** Si en una muestra de 5 la media cae fuera de [4,5617 ; 5,4383] se rechaza H0. Hay 5 período(s) fuera de los límites (n.º 3: 5,5, n.º 7: 5,5, n.º 10: 4,5, n.º 11: 5,8, n.º 12: 5,6): hay razones para alarmarse, el proceso estuvo fuera de control.

**Respuesta de la guía:** Entre 4,56 y 5,44 ppm, si hay razones para alarmarse porque se encuentran valores fuera de los límites.

#### b) Probabilidad de error / potencia (β, 1-β) ℹ️

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Procesar la muestra**: n = 12, x̄ = Σxᵢ/n = 5,1333, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,4313.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Distribución de la media** con el proceso en su valor nominal: x̄ ~ N(μ₀ = 5; σ/√n = 0,5/√5 = 0,2236).
- **Probabilidad**: P(x̄ ≥ 6,6) = P(Z ≥ 7,1554) = 0.

**Conclusión:** P(x̄ ≥ 6,6) = 0: es prácticamente imposible obtener esa media si el proceso está en su valor nominal; si apareciera, el proceso está fuera de control.

**Respuesta de la guía:** Es prácticamente imposible.

#### c) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Procesar la muestra**: n = 12, x̄ = Σxᵢ/n = 5,1333, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,4313.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²) (no vale la regla «n ≥ 30»: el profesor la descarta).  
• Por la reproductividad de la Normal, la media muestral también es Normal: x̄ ~ N(μ; σ²/n).  
• Al estandarizar, Z = (x̄ - μ)/(σ/√n), se divide por un PARÁMETRO (σ es una constante): una normal dividida por una constante sigue siendo normal → Z ~ N(0; 1). (No es «uso Z porque conozco σ».)  
• Para β y la potencia se usa la misma distribución de x̄ pero centrada en el valor alternativo μ₁: β = P(x̄ en la zona de no rechazo | μ = μ₁).
- **Región crítica** (del ensayo): H0: μ = 5,0, x̄c = 4,5617 ; 5,4383; para β se usa redondeado hacia afuera a 4 decimales (x̄c = 4,5617 ; 5,4383), como la cátedra.
- **β** = P(x̄c₁ ≤ x̄ ≤ x̄c₂ | μ = 5,25) = Φ((5,4383 - 5,25)/0,2236) - Φ((4,5617 - 5,25)/0,2236) = 0,7991.
- **Potencia** 1-β = 0,2009.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,2009 (β = 0,7991).

**Respuesta de la guía:** 1–β = 0,2009.

---

## TEMA II — Inferencia sobre varianzas / desvíos

### II-1 · Problema 1 (pág. 13)

**Enunciado.** Un proceso produce cierta clase de cojinetes de bolas (rulemanes) cuyo diámetro interior debe ser de 3 cm. Se seleccionaron en forma aleatoria 12 de estos cojinetes y se miden sus diámetros internos, que resultaron ser (valores en cm): 3,01 – 3,05 – 2,99 – 2,99 – 3,00 – 3,02 – 2,98 – 2,99 – 2,97 – 3,02 – 3,01 – 2,97.

*Determinar un intervalo de confianza del 95% para la varianza (σ²).*

*Diámetros internos (cm)*

|  |
|
| 3,01 | 3,05 | 2,99 | 2,99 | 3 | 3,02 |
| 2,98 | 2,99 | 2,97 | 3,02 | 3,01 | 2,97 |

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### Resolución (Intervalo de confianza (estimar)) ✅

*Qué pide:* Estimar la varianza σ² / el desvío σ con un 95% de confianza mediante un intervalo de confianza. Se usa χ² con ν = n-1 (el intervalo NO es simétrico).

- **Procesar la muestra**: n = 12, x̄ = Σxᵢ/n = 3, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,0234.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **Distribución**: χ² con ν = n-1 = 11. χ²(0,025; 11) = 3,8157 y χ²(0,975; 11) = 21,92.
- **Varianza**: A = (n-1)·S²/χ²(1-α/2) = 11·0,0005/21,92 = 0,00027 ; B = (n-1)·S²/χ²(α/2) = 11·0,0005/3,8157 = 0,00157.
- **Desvío**: A' = √A = 0,0165 ; B' = √B = 0,0397. Relación entre límites R' = B'/A' = 2,3968.

**Conclusión:** Con un 95% de confianza: P(0,00027 ≤ σ² ≤ 0,00158) = 0,95 y P(0,0165 ≤ σ ≤ 0,0397) = 0,95 (límites redondeados hacia afuera; sin redondear: σ² entre 0,000274 y 0,001572, σ entre 0,016545 y 0,039654).

**Respuesta de la guía:** Entre 0,00027 y 0,00158 cm².

> 📝 *Notas de la transcripción:* Con χ² exactos el límite superior da 0,001572 (redondearía a 0,00157); la guía dice 0,00158. Se transcribe tal cual.

---

### II-2 · Problema 2 (pág. 13)

**Enunciado.** Un torno automático produce cierta pieza de bronce que tiene una dimensión crítica cuya variabilidad se trata de controlar a tal efecto se midieron 5 piezas con los siguientes resultados en mm: 25,4 – 25,1 – 24,9 – 25,2 – 25,0.

*¿Entre qué límites se encontrará la varianza de esta dimensión con un 90% de Confianza?*

*Dimensión crítica (mm)*

|  |
|
| 25,4 | 25,1 | 24,9 | 25,2 | 25 |

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### Resolución (Intervalo de confianza (estimar)) ✅

*Qué pide:* Estimar la varianza σ² / el desvío σ con un 90% de confianza mediante un intervalo de confianza. Se usa χ² con ν = n-1 (el intervalo NO es simétrico).

- **Procesar la muestra**: n = 5, x̄ = Σxᵢ/n = 25,12, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,1924.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **Distribución**: χ² con ν = n-1 = 4. χ²(0,05; 4) = 0,7107 y χ²(0,95; 4) = 9,4877.
- **Varianza**: A = (n-1)·S²/χ²(1-α/2) = 4·0,037/9,4877 = 0,0156 ; B = (n-1)·S²/χ²(α/2) = 4·0,037/0,7107 = 0,20824.
- **Desvío**: A' = √A = 0,1249 ; B' = √B = 0,4563. Relación entre límites R' = B'/A' = 3,6537.

**Conclusión:** Con un 90% de confianza: P(0,0155 ≤ σ² ≤ 0,2083) = 0,9 y P(0,124 ≤ σ ≤ 0,457) = 0,9 (límites redondeados hacia afuera; sin redondear: σ² entre 0,015599 y 0,208239, σ entre 0,124896 y 0,456332).

**Respuesta de la guía:** Entre 0,0155 y 0,2083 mm².

---

### II-3 · Problema 3 (pág. 13)

**Enunciado.** La desviación estándar de la resistencia a la rotura de una partida de 30 piezas producidas por una compañía fue de 200 kg.

*Estimar con un nivel de confianza del 95% el desvío estándar de la resistencia a la rotura de todas las piezas.*

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### Resolución (Intervalo de confianza (estimar)) ✅

*Qué pide:* Estimar la varianza σ² / el desvío σ con un 95% de confianza mediante un intervalo de confianza. Se usa χ² con ν = n-1 (el intervalo NO es simétrico).

- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **Distribución**: χ² con ν = n-1 = 29. χ²(0,025; 29) = 16,0471 y χ²(0,975; 29) = 45,7223.
- **Varianza**: A = (n-1)·S²/χ²(1-α/2) = 29·40.000/45,7223 = 25.370,5601 ; B = (n-1)·S²/χ²(α/2) = 29·40.000/16,0471 = 72.287,33205.
- **Desvío**: A' = √A = 159,2814 ; B' = √B = 268,863. Relación entre límites R' = B'/A' = 1,688.

**Conclusión:** Con un 95% de confianza: P(25.370,5601 ≤ σ² ≤ 72.287,3321) = 0,95 y P(159,28 ≤ σ ≤ 268,87) = 0,95 (límites redondeados hacia afuera; sin redondear: σ² entre 25.370,560102 y 72.287,332045, σ entre 159,281387 y 268,863036).

**Respuesta de la guía:** Entre 159,28 y 268,87 kg.

---

### II-4 · Problema 4 (pág. 13)

**Enunciado.** En una muestra de 15 tubos fluorescentes pertenecientes al último lote de producción, se obtuvo que la desviación estándar de la duración ha sido de 120 horas.

- **a)** Estimar el desvío estándar de la duración de todos los tubos con un riesgo del 10%.
- **b)** Calcular el tamaño de muestra necesario para reducir en un 30% la relación entre los límites del desvío anterior.

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la varianza σ² / el desvío σ con un 90% de confianza mediante un intervalo de confianza. Se usa χ² con ν = n-1 (el intervalo NO es simétrico).

- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **Distribución**: χ² con ν = n-1 = 14. χ²(0,05; 14) = 6,5706 y χ²(0,95; 14) = 23,6848.
- **Varianza**: A = (n-1)·S²/χ²(1-α/2) = 14·14.400/23,6848 = 8.511,79128 ; B = (n-1)·S²/χ²(α/2) = 14·14.400/6,5706 = 30.681,98294.
- **Desvío**: A' = √A = 92,2594 ; B' = √B = 175,1627. Relación entre límites R' = B'/A' = 1,8986.

**Conclusión:** Con un 90% de confianza: P(8.511,7912 ≤ σ² ≤ 30.681,9830) = 0,9 y P(92,25 ≤ σ ≤ 175,17) = 0,9 (límites redondeados hacia afuera; sin redondear: σ² entre 8.511,791276 y 30.681,982937, σ entre 92,25937 y 175,162733).

**Respuesta de la guía:** Entre 92,25 y 175,17 horas.

#### b) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para reducir un 30% el error (o la relación entre límites). Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.  
• El n sale de la relación entre límites R' = B'/A' (Ecuación de García para aproximar ν).
- **Relación buscada** R' = B'/A' = 1,329 → R = (R')² = 1,7663.
- **Ecuación de García**: a = Z(1-α/2)·(R^(1/3)+1)/(2·(R^(1/3)-1)) = 8,7002; ν = (2/9)·(a + √(a²+1))² = 67,7275 → ν al entero superior; n = ν + 1 → 69.
- Control por búsqueda exacta en χ²: n = 69 (R' logrado = 1,3283).

**Conclusión:** Para reducir un 30% la relación entre límites (de R' = 1,8986 a R' = 1,3290), el tamaño de muestra necesario es n = 69. (Ecuación de García: a = 8,7002, ν = 67,7275.) Como ya se relevaron n_preliminar = 15 unidades, hay que tomar Δn = 69 - 15 = 54 unidades adicionales.

**Respuesta de la guía:** n = 69 tubos.

---

### II-5 · Problema 5 (pág. 13)

**Enunciado.** Se han tomado datos de tensión de rotura, en Kg/mm², de una aleación de aluminio, obteniéndose los siguientes resultados: 37,6 – 38,4 – 38,8 – 37,9.

- **a)** Calcular los límites de confianza del 90% para el desvío estándar.
- **b)** ¿Cuántos datos más habría que tomar para que el límite superior, del intervalo para el desvío estándar, sea el doble que el límite inferior?

*Tensión de rotura (Kg/mm²)*

|  |
|
| 37,6 | 38,4 | 38,8 | 37,9 |

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la varianza σ² / el desvío σ con un 90% de confianza mediante un intervalo de confianza. Se usa χ² con ν = n-1 (el intervalo NO es simétrico).

- **Procesar la muestra**: n = 4, x̄ = Σxᵢ/n = 38,175, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,5315.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **Distribución**: χ² con ν = n-1 = 3. χ²(0,05; 3) = 0,3518 y χ²(0,95; 3) = 7,8147.
- **Varianza**: A = (n-1)·S²/χ²(1-α/2) = 3·0,2825/7,8147 = 0,10845 ; B = (n-1)·S²/χ²(α/2) = 3·0,2825/0,3518 = 2,40872.
- **Desvío**: A' = √A = 0,3293 ; B' = √B = 1,552. Relación entre límites R' = B'/A' = 4,7128.

**Conclusión:** Con un 90% de confianza: P(0,1084 ≤ σ² ≤ 2,4088) = 0,9 y P(0,32 ≤ σ ≤ 1,56) = 0,9 (límites redondeados hacia afuera; sin redondear: σ² entre 0,108449 y 2,408722, σ entre 0,329316 y 1,552006).

**Respuesta de la guía:** Entre 0,32 Kg/mm² y 1,56 Kg/mm² (S = 0,5315; R' = B'/A' = 4,7128).

#### b) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para que la relación entre límites sea R' = 2. Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Procesar la muestra**: n = 4, x̄ = Σxᵢ/n = 38,175, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,5315.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.  
• El n sale de la relación entre límites R' = B'/A' (Ecuación de García para aproximar ν).
- **Relación buscada** R' = B'/A' = 2 → R = (R')² = 4.
- **Ecuación de García**: a = Z(1-α/2)·(R^(1/3)+1)/(2·(R^(1/3)-1)) = 3,6226; ν = (2/9)·(a + √(a²+1))² = 12,1058 → ν al entero superior; n = ν + 1 → 14.
- Control por búsqueda exacta en χ²: n = 14 (R' logrado = 1,9482).

**Conclusión:** Para lograr una relación entre límites R' = 2,0000, el tamaño de muestra necesario es n = 14. (Ecuación de García: a = 3,6226, ν = 12,1058.) Como ya se relevaron n_preliminar = 4 unidades, hay que tomar Δn = 14 - 4 = 10 unidades adicionales.

**Respuesta de la guía:** n = 14 datos en total, o sea 10 datos más de los 4 iniciales (a = 3,6227; ν = 12,11).

<details><summary>Cómo lo concluye la guía</summary>

> Se concluye que el desvío estándar de la población estará comprendido entre 0,32 Kg/mm² y 1,56 Kg/mm², afirmándolo con un 90% de confianza, o sea: P(0,32 Kg/mm² ≤ σ ≤ 1,56 Kg/mm²) = 0,90.
> Se necesitaría una muestra de 14 datos en total, o sea se deberían tomar 10 datos más de los 4 seleccionados en la muestra inicial.

</details>

---

### II-6 · Problema 6 (pág. 14)

**Enunciado.** El peso de los ovillos de hilo que salen de una ovilladora tiene distribución Normal con un desvío estándar que se controla periódicamente con muestras de 20 ovillos. Una de dichas muestras arrojó un desvío de 15 gramos.

- **a)** Calcular los límites de confianza del 95% para el desvío.
- **b)** ¿Qué tamaño de muestra habría que tomar para tener un intervalo de confianza cuyo límite superior sea un 50% mayor que el inferior?

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la varianza σ² / el desvío σ con un 95% de confianza mediante un intervalo de confianza. Se usa χ² con ν = n-1 (el intervalo NO es simétrico).

- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **Distribución**: χ² con ν = n-1 = 19. χ²(0,025; 19) = 8,9065 y χ²(0,975; 19) = 32,8523.
- **Varianza**: A = (n-1)·S²/χ²(1-α/2) = 19·225/32,8523 = 130,12777 ; B = (n-1)·S²/χ²(α/2) = 19·225/8,9065 = 479,98564.
- **Desvío**: A' = √A = 11,4074 ; B' = √B = 21,9086. Relación entre límites R' = B'/A' = 1,9206.

**Conclusión:** Con un 95% de confianza: P(130,1277 ≤ σ² ≤ 479,9857) = 0,95 y P(11,40 ≤ σ ≤ 21,91) = 0,95 (límites redondeados hacia afuera; sin redondear: σ² entre 130,127769 y 479,985638, σ entre 11,407356 y 21,908575).

**Respuesta de la guía:** Entre 11,40 y 21,91 gramos.

#### b) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para que la relación entre límites sea R' = 1,5. Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.  
• El n sale de la relación entre límites R' = B'/A' (Ecuación de García para aproximar ν).
- **Relación buscada** R' = B'/A' = 1,5 → R = (R')² = 2,25.
- **Ecuación de García**: a = Z(1-α/2)·(R^(1/3)+1)/(2·(R^(1/3)-1)) = 7,2949; ν = (2/9)·(a + √(a²+1))² = 47,7461 → ν al entero superior; n = ν + 1 → 49.
- Control por búsqueda exacta en χ²: n = 49 (R' logrado = 1,4981).

**Conclusión:** Para lograr una relación entre límites R' = 1,5000, el tamaño de muestra necesario es n = 49. (Ecuación de García: a = 7,2949, ν = 47,7461.) Como ya se relevaron n_preliminar = 20 unidades, hay que tomar Δn = 49 - 20 = 29 unidades adicionales.

**Respuesta de la guía:** n = 49 ovillos en total.

---

### II-7 · Problema 7 (pág. 14)

**Enunciado.** El promedio de ventas semanales en dólares por distribuidor de un determinado producto en una muestra de 20 supermercados, ha sido durante el año pasado de 3.500 U$s con un desvío estándar de 210 U$s.

- **a)** Estimar con un riesgo del 5% el desvío estándar de las ventas semanales por distribuidor, en todos los supermercados, durante el año pasado.
- **b)** ¿Cuántos supermercados más habría que analizar si se pretende disminuir en un 30% la relación entre ambos límites anterior?

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la varianza σ² / el desvío σ con un 95% de confianza mediante un intervalo de confianza. Se usa χ² con ν = n-1 (el intervalo NO es simétrico).

- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **Distribución**: χ² con ν = n-1 = 19. χ²(0,025; 19) = 8,9065 y χ²(0,975; 19) = 32,8523.
- **Varianza**: A = (n-1)·S²/χ²(1-α/2) = 19·44.100/32,8523 = 25.505,04272 ; B = (n-1)·S²/χ²(α/2) = 19·44.100/8,9065 = 94.077,18514.
- **Desvío**: A' = √A = 159,703 ; B' = √B = 306,72. Relación entre límites R' = B'/A' = 1,9206.

**Conclusión:** Con un 95% de confianza: P(25.505,0427 ≤ σ² ≤ 94.077,1852) = 0,95 y P(159,70 ≤ σ ≤ 306,73) = 0,95 (límites redondeados hacia afuera; sin redondear: σ² entre 25.505,042718 y 94.077,185137, σ entre 159,702983 y 306,720044).

**Respuesta de la guía:** Entre 159,70 y 306,73 U$s.

#### b) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para reducir un 30% el error (o la relación entre límites). Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.  
• El n sale de la relación entre límites R' = B'/A' (Ecuación de García para aproximar ν).
- **Relación buscada** R' = B'/A' = 1,3444 → R = (R')² = 1,8074.
- **Ecuación de García**: a = Z(1-α/2)·(R^(1/3)+1)/(2·(R^(1/3)-1)) = 9,9663; ν = (2/9)·(a + √(a²+1))² = 88,7348 → ν al entero superior; n = ν + 1 → 90.
- Control por búsqueda exacta en χ²: n = 90 (R' logrado = 1,3437).

**Conclusión:** Para reducir un 30% la relación entre límites (de R' = 1,9206 a R' = 1,3444), el tamaño de muestra necesario es n = 90. (Ecuación de García: a = 9,9663, ν = 88,7348.) Como ya se relevaron n_preliminar = 20 unidades, hay que tomar Δn = 90 - 20 = 70 unidades adicionales.

**Respuesta de la guía:** n = 90 supermercados en total, o sea, 70 supermercados más.

---

### II-8 · Problema 8 (pág. 14)

**Enunciado.** Se espera tener una cierta variación aleatoria nominal en el espesor de las láminas de plástico que una máquina produce. Para determinar cuándo la variación en el espesor se encuentra dentro de ciertos límites, cada día se seleccionan en forma aleatoria 12 láminas de plástico y se mide su espesor en milímetros. Los datos que se obtuvieron son los siguientes: 12,6 – 11,9 – 12,3 – 12,8 – 11,8 – 11,7 – 12,4 – 12,1 – 12,3 – 12,0 – 12,5 – 12,9.

- **a)** Obtener el intervalo de confianza del 90% para la varianza poblacional desconocida del espesor.
- **b)** Si no es aceptable una varianza mayor de 0,09 mm², para un riesgo del 5%, ¿existe alguna razón para preocuparse con base en esta evidencia?
- **c)** ¿Cuál es la probabilidad de detectar que la varianza es de 0,11 mm²?
- **d)** ¿Cuántas láminas más se deberán medir si se quiere que la probabilidad anterior valga 0,95?

*Espesor (mm)*

|  |
|
| 12,6 | 11,9 | 12,3 | 12,8 | 11,8 | 11,7 |
| 12,4 | 12,1 | 12,3 | 12 | 12,5 | 12,9 |

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la varianza σ² / el desvío σ con un 90% de confianza mediante un intervalo de confianza. Se usa χ² con ν = n-1 (el intervalo NO es simétrico).

- **Procesar la muestra**: n = 12, x̄ = Σxᵢ/n = 12,275, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,3864.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **Distribución**: χ² con ν = n-1 = 11. χ²(0,05; 11) = 4,5748 y χ²(0,95; 11) = 19,6751.
- **Varianza**: A = (n-1)·S²/χ²(1-α/2) = 11·0,1493/19,6751 = 0,08348 ; B = (n-1)·S²/χ²(α/2) = 11·0,1493/4,5748 = 0,35903.
- **Desvío**: A' = √A = 0,2889 ; B' = √B = 0,5992. Relación entre límites R' = B'/A' = 2,0738.

**Conclusión:** Con un 90% de confianza: P(0,0834 ≤ σ² ≤ 0,3591) = 0,9 y P(0,288 ≤ σ ≤ 0,600) = 0,9 (límites redondeados hacia afuera; sin redondear: σ² entre 0,083481 y 0,359031, σ entre 0,288931 y 0,599192).

**Respuesta de la guía:** Entre 0,0834 y 0,3591 mm².

#### b) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la varianza σ² / el desvío σ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **Procesar la muestra**: n = 12, x̄ = Σxᵢ/n = 12,275, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,3864.
- **1 · Planteo de hipótesis**: H0: σ² ≤ 0,09  vs  H1: σ² > 0,09.
- **Justificación de H0**:  
• H1: σ > 0,3 recoge lo que el enunciado quiere probar; H0: σ ≤ 0,3 es el complemento y lleva la igualdad (el valor de referencia 0,3).  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² con ν = 11.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **4 · Condición de rechazo (CR)**: S²c = σ₀²·χ²/ν = 0,09·χ²/11 = 0,16098 (Sc = 0,4012). Si S² > S²c ⇒ se rechaza H0. Informado (hacia afuera): Sc = 0,402.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 12 unidades y se calcula su desvío S. Si S > 0,4012, se rechaza H0 → se puede asegurar que σ² > 0,09. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que σ² > 0,09.
- **6 · Cálculos y decisión**: S² = 0,14932 (S = 0,3864) → no cae en la zona de rechazo.
- Dato informativo (la guía a veces lo informa; el profesor decide con S contra Sc): forma equivalente estandarizada ν·S²/σ₀² = 18,25 y χ² de tabla = 19,6751.

**Conclusión:** Con α = 0,05, S = 0,3864 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: σ² ≤ 0,09. No hay evidencia suficiente para asegurar que σ² > 0,09 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No, no se puede asegurar que la varianza sea mayor que 0,09 mm².

#### c) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Procesar la muestra**: n = 12, x̄ = Σxᵢ/n = 12,275, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,3864.
- **Hipótesis**: H0: σ² ≤ 0,09  vs  H1: σ² > 0,09  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.  
• Para β / potencia se usa que (n-1)·S²/σ₁² ~ χ²(n-1) cuando el desvío verdadero es σ₁.
- **Distribución**: χ² con ν = 11.
- **Condición de rechazo**: S²c = σ₀²·χ²/ν = 0,09·χ²/11 = 0,16098 (Sc = 0,4012). Si S² > S²c ⇒ se rechaza H0. Informado (hacia afuera): Sc = 0,402.
- **β** = P(no rechazar H0 | σ = 0,3317) = 0,8625.
- **Potencia** 1-β = 0,1375.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,1375 (β = 0,8625).

**Respuesta de la guía:** 1-β = 0,1375.

#### d) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Procesar la muestra**: n = 12, x̄ = Σxᵢ/n = 12,275, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,3864.
- **Justificación de H0**:  
• H1: σ > 0,3 recoge lo que el enunciado quiere probar; H0: σ ≤ 0,3 es el complemento y lleva la igualdad (el valor de referencia 0,3).  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | σ = 0,3317) = 0,05 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: σ² ≤ 0,09  vs  H1: σ² > 0,09.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.  
• Para β / potencia se usa que (n-1)·S²/σ₁² ~ χ²(n-1) cuando el desvío verdadero es σ₁.
- Se busca el menor n tal que con α = 0,05 se tenga β ≤ 0,05 cuando σ = 0,3317: n = 540 (S²c = 0,0992, Sc = 0,315, β real = 0,0498).

**Conclusión:** El tamaño de muestra necesario es n = 540. Como la muestra actual es de 12, hay que tomar Δn = 540 - 12 = 528 más.

**Respuesta de la guía:** n = 540 láminas en total, o sea, 528 láminas más.

---

### II-9 · Problema 9 (pág. 14)

**Enunciado.** Una máquina envasadora de botellas de gaseosas dosifica volúmenes variables cuyo desvío estándar no debe superar los 15 cm³. Se controla periódicamente tomando muestras de 10 envases y midiendo los volúmenes dosificados. Una de las muestras arrojó un desvío de 18,2 cm³.

- **a)** ¿Se recomienda detener la máquina y revisarla con un riesgo máximo del 5%?
- **b)** ¿Cuál es la probabilidad de no detectar que la máquina envasadora dosifica con un desvío estándar de 16 cm³?
- **c)** ¿Cuántos envases más se deberían controlar para que la probabilidad anterior valga 0,10?
- **d)** Estimar con la muestra obtenida, en el enunciado, y un riesgo del 5% la desviación estándar de los volúmenes dosificados.

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la varianza σ² / el desvío σ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: σ² ≤ 225  vs  H1: σ² > 225.
- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: σ ≤ 15 supone que cumple; H1: σ > 15 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² con ν = 9.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **4 · Condición de rechazo (CR)**: S²c = σ₀²·χ²/ν = 225·χ²/9 = 422,97444 (Sc = 20,5663). Si S² > S²c ⇒ se rechaza H0. Informado (hacia afuera): Sc = 20,57.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 10 unidades y se calcula su desvío S. Si S > 20,5663, se rechaza H0 → se puede asegurar que σ² > 225. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que σ² > 225.
- **6 · Cálculos y decisión**: S² = 331,24 (S = 18,2) → no cae en la zona de rechazo.
- Dato informativo (la guía a veces lo informa; el profesor decide con S contra Sc): forma equivalente estandarizada ν·S²/σ₀² = 13,2496 y χ² de tabla = 16,919.

**Conclusión:** Con α = 0,05, S = 18,2 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: σ² ≤ 225. No hay evidencia suficiente para asegurar que σ² > 225 (no rechazar H0 no la prueba).

**Respuesta de la guía:** H0) σ ≤ σ0 = 15 cm³; Sc = 20,5664 cm³. Como S = 18,2 cm³ no supera el crítico, no se recomienda detener la máquina: no se puede asegurar que el desvío supere los 15 cm³ (χ²c = 13,2496 < 16,9190).

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: σ² ≤ 225  vs  H1: σ² > 225  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.  
• Para β / potencia se usa que (n-1)·S²/σ₁² ~ χ²(n-1) cuando el desvío verdadero es σ₁.
- **Distribución**: χ² con ν = 9.
- **Condición de rechazo**: S²c = σ₀²·χ²/ν = 225·χ²/9 = 422,97444 (Sc = 20,5663). Si S² > S²c ⇒ se rechaza H0. Informado (hacia afuera): Sc = 20,57.
- **β** = P(no rechazar H0 | σ = 16) = 0,9054.
- **Potencia** 1-β = 0,0946.

**Conclusión:** La probabilidad pedida es β = 0,9054 (potencia 1-β = 0,0946).

**Respuesta de la guía:** β = 0,9054.

#### c) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: σ ≤ 15 supone que cumple; H1: σ > 15 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | σ = 16) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: σ² ≤ 225  vs  H1: σ² > 225.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.  
• Para β / potencia se usa que (n-1)·S²/σ₁² ~ χ²(n-1) cuando el desvío verdadero es σ₁.
- Se busca el menor n tal que con α = 0,05 se tenga β ≤ 0,1 cuando σ = 16: n = 1025 (S²c = 241,60191, Sc = 15,5435, β real = 0,0998).

**Conclusión:** El tamaño de muestra necesario es n = 1025. Como la muestra actual es de 10, hay que tomar Δn = 1025 - 10 = 1015 más.

**Respuesta de la guía:** n = 1.025 envases en total, o sea 1.015 envases más (R = 1,137; a = 33,9220; ν = 1.023,29).

#### d) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la varianza σ² / el desvío σ con un 95% de confianza mediante un intervalo de confianza. Se usa χ² con ν = n-1 (el intervalo NO es simétrico).

- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **Distribución**: χ² con ν = n-1 = 9. χ²(0,025; 9) = 2,7004 y χ²(0,975; 9) = 19,0228.
- **Varianza**: A = (n-1)·S²/χ²(1-α/2) = 9·331,24/19,0228 = 156,71537 ; B = (n-1)·S²/χ²(α/2) = 9·331,24/2,7004 = 1.103,97407.
- **Desvío**: A' = √A = 12,5186 ; B' = √B = 33,2261. Relación entre límites R' = B'/A' = 2,6541.

**Conclusión:** Con un 95% de confianza: P(156,7153 ≤ σ² ≤ 1.103,9741) = 0,95 y P(12,51 ≤ σ ≤ 33,23) = 0,95 (límites redondeados hacia afuera; sin redondear: σ² entre 156,715365 y 1.103,974075, σ entre 12,518601 y 33,226105).

**Respuesta de la guía:** Entre 12,51 cm³ y 33,23 cm³.

> 📝 *Notas de la transcripción:* El crítico se calcula como Sc = 20,5664 cm³ pero en el texto de la conclusión figura 20,5663 cm³.

<details><summary>Cómo lo concluye la guía</summary>

> Esta hipótesis se rechaza si en una muestra de 10 envases el desvío es mayor que 20,5663 cm³.
> Como la muestra obtenida arrojó un desvío de 18,2 cm³, no se recomienda detener la máquina y revisarla porque no se puede asegurar que el desvío estándar de dosificación de la máquina supere los 15 cm³.
> Como no se rechaza la hipótesis, se arriba a la misma conclusión.
> Se necesitaría una muestra de 1.025 envases en total, o sea se deberían controlar 1.015 envases más de los 10 seleccionados en la muestra inicial.
> Se concluye que el desvío estándar de la población estará comprendido entre 12,51 cm³ y 33,23 cm³, afirmándolo con un 95% de confianza, o sea: P(12,51 cm³ ≤ σ ≤ 33,23 cm³) = 0,95.

</details>

---

### II-10 · Problema 10 (pág. 15)

**Enunciado.** Una compañía embotelladora considera la posibilidad de comprar una nueva máquina dosificadora si se puede asegurar que el desvío estándar de los volúmenes dosificados es menor que 15 cm³, y a efectos de tomar una decisión se realiza una prueba con 20 envases arrojando, esta, un desvío estándar de 12,5 cm³.

- **a)** ¿Se recomendaría comprar la máquina con un riesgo máximo del 5%?
- **b)** Estimar con un riesgo del 5% la desviación estándar máxima de los volúmenes dosificados.

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la varianza σ² / el desvío σ: H1 con signo '<'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: σ² ≥ 225  vs  H1: σ² < 225.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: σ ≥ 15 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: σ < 15 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² con ν = 19.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **4 · Condición de rechazo (CR)**: S²c = σ₀²·χ²/ν = 225·χ²/19 = 119,80673 (Sc = 10,9456). Si S² < S²c ⇒ se rechaza H0. Informado (hacia afuera): Sc = 10,94.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 20 unidades y se calcula su desvío S. Si S < 10,9456, se rechaza H0 → se puede asegurar que σ² < 225. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que σ² < 225.
- **6 · Cálculos y decisión**: S² = 156,25 (S = 12,5) → no cae en la zona de rechazo.
- Dato informativo (la guía a veces lo informa; el profesor decide con S contra Sc): forma equivalente estandarizada ν·S²/σ₀² = 13,1944 y χ² de tabla = 10,117.

**Conclusión:** Con α = 0,05, S = 12,5 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: σ² ≥ 225. No hay evidencia suficiente para asegurar que σ² < 225 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No, porque no se puede asegurar que el desvío sea menor que 15 cm³.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la varianza σ² / el desvío σ con un 95% de confianza mediante un intervalo de confianza. Se usa χ² con ν = n-1 (el intervalo NO es simétrico).

- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **Límite unilateral** (máximo): todo α = 0,05 va a una sola cola → se calcula como el extremo del IC con riesgo 2α = 0,1.
- **Distribución**: χ² con ν = n-1 = 19. χ²(0,05; 19) = 10,117 y χ²(0,95; 19) = 30,1435.
- **Varianza**: A = (n-1)·S²/χ²(1-α/2) = 19·156,25/30,1435 = 98,48715 ; B = (n-1)·S²/χ²(α/2) = 19·156,25/10,117 = 293,44135.
- **Desvío**: A' = √A = 9,9241 ; B' = √B = 17,1301. Relación entre límites R' = B'/A' = 1,7261.

**Conclusión:** Con un 95% de confianza, σ ≤ 17,14: P(σ ≤ 17,14) = 0,95 (cota máxima redondeada hacia arriba; sin redondear 17,13013).

**Respuesta de la guía:** B' = 17,14 cm³.

> 📝 *Notas de la transcripción:* Con χ²(0,05;19) = 10,1170 exacto, B' da 17,13 cm³; la guía da 17,14 (diferencia de redondeo).

---

### II-11 · Problema 11 (pág. 15)

**Enunciado.** La volatilidad de una acción está dada por el desvío estándar de su cotización diaria. A mayor volatilidad mayor riesgo, pero también mayor posibilidad de obtener mayores ganancias en el corto plazo. Durante los últimos 20 días se obtuvo, para una acción dada, un desvío estándar de 25 U$s.

- **a)** ¿Se puede asegurar, con 10% de riesgo, que el desvío verdadero es superior a 20 U$s?
- **b)** Establecer un intervalo de confianza del 80% para el desvío verdadero.

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la varianza σ² / el desvío σ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: σ² ≤ 400  vs  H1: σ² > 400.
- **Justificación de H0**:  
• H1: σ > 20 recoge lo que el enunciado quiere probar; H0: σ ≤ 20 es el complemento y lleva la igualdad (el valor de referencia 20).  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² con ν = 19.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **4 · Condición de rechazo (CR)**: S²c = σ₀²·χ²/ν = 400·χ²/19 = 572,70676 (Sc = 23,9313). Si S² > S²c ⇒ se rechaza H0. Informado (hacia afuera): Sc = 23,94.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 20 unidades y se calcula su desvío S. Si S > 23,9313, se rechaza H0 → se puede asegurar que σ² > 400. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que σ² > 400.
- **6 · Cálculos y decisión**: S² = 625 (S = 25) → cae en la zona de rechazo.
- Dato informativo (la guía a veces lo informa; el profesor decide con S contra Sc): forma equivalente estandarizada ν·S²/σ₀² = 29,6875 y χ² de tabla = 27,2036.

**Conclusión:** Con α = 0,1, S = 25 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: σ² ≤ 400. Se puede asegurar que σ² > 400.

**Respuesta de la guía:** Si, se puede asegurar que el desvío es superior a 20 U$s.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la varianza σ² / el desvío σ con un 80% de confianza mediante un intervalo de confianza. Se usa χ² con ν = n-1 (el intervalo NO es simétrico).

- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **Distribución**: χ² con ν = n-1 = 19. χ²(0,1; 19) = 11,6509 y χ²(0,9; 19) = 27,2036.
- **Varianza**: A = (n-1)·S²/χ²(1-α/2) = 19·625/27,2036 = 436,52357 ; B = (n-1)·S²/χ²(α/2) = 19·625/11,6509 = 1.019,23369.
- **Desvío**: A' = √A = 20,8931 ; B' = √B = 31,9254. Relación entre límites R' = B'/A' = 1,528.

**Conclusión:** Con un 80% de confianza: P(436,5235 ≤ σ² ≤ 1.019,2337) = 0,8 y P(20,89 ≤ σ ≤ 31,93) = 0,8 (límites redondeados hacia afuera; sin redondear: σ² entre 436,523572 y 1.019,233688, σ entre 20,893147 y 31,92544).

**Respuesta de la guía:** Entre 20,89 y 31,93 U$s.

---

### II-12 · Problema 12 (pág. 16)

**Enunciado.** El control de la variabilidad de los pesos de suelas de goma se realiza tomando muestras de suelas periódicas de 10 unidades, deteniendo el proceso tecnológico en caso de que el desvío poblacional "σ" de los pesos tome un valor mayor que el desvío estipulado en la especificación. El valor considerado adecuado por especificación para el desvío de la población es de 5 gramos como máximo y, de ser así, la probabilidad de detener el proceso indebidamente se ha establecido en 0,05.

- **a)** Calcular el valor crítico (Sc) del desvío estándar muestral.
- **b)** ¿Cuál es la probabilidad de no detectar que el desvío es de 8 gramos?
- **c)** ¿Cuántas suelas más se deberán tomar si se quiere que la probabilidad anterior valga 0,05?

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: σ ≤ 5 supone que cumple; H1: σ > 5 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: σ² ≤ 25  vs  H1: σ² > 25  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.  
• Para β / potencia se usa que (n-1)·S²/σ₁² ~ χ²(n-1) cuando el desvío verdadero es σ₁.
- **Distribución**: χ² con ν = 9.
- **Condición de rechazo**: S²c = σ₀²·χ²/ν = 25·χ²/9 = 46,99716 (Sc = 6,8554). Si S² > S²c ⇒ se rechaza H0. Informado (hacia afuera): Sc = 6,86.
- Dato informativo (la guía a veces lo informa; el profesor decide con S contra Sc): forma equivalente estandarizada ν·S²/σ₀² = 9 y χ² de tabla = 16,919.

**Conclusión:** Valor crítico y condición de rechazo arriba.

**Respuesta de la guía:** Para rechazar la hipótesis y detener el proceso tecnológico, S debe ser mayor que Sc = 6,86 gramos.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: σ² ≤ 25  vs  H1: σ² > 25  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.  
• Para β / potencia se usa que (n-1)·S²/σ₁² ~ χ²(n-1) cuando el desvío verdadero es σ₁.
- **Distribución**: χ² con ν = 9.
- **Condición de rechazo**: S²c = σ₀²·χ²/ν = 25·χ²/9 = 46,99716 (Sc = 6,8554). Si S² > S²c ⇒ se rechaza H0. Informado (hacia afuera): Sc = 6,86.
- **β** = P(no rechazar H0 | σ = 8) = 0,3222.
- **Potencia** 1-β = 0,6778.

**Conclusión:** La probabilidad pedida es β = 0,3222 (potencia 1-β = 0,6778).

**Respuesta de la guía:** β = 0.3222.

#### c) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: σ ≤ 5 supone que cumple; H1: σ > 5 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | σ = 8) = 0,05 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: σ² ≤ 25  vs  H1: σ² > 25.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.  
• Para β / potencia se usa que (n-1)·S²/σ₁² ~ χ²(n-1) cuando el desvío verdadero es σ₁.
- Se busca el menor n tal que con α = 0,05 se tenga β ≤ 0,05 cuando σ = 8: n = 27 (S²c = 37,38956, Sc = 6,1147, β real = 0,0462).

**Conclusión:** El tamaño de muestra necesario es n = 27. Como la muestra actual es de 10, hay que tomar Δn = 27 - 10 = 17 más.

**Respuesta de la guía:** n = 27 suelas en total, o sea 17 suelas más.

> 📝 *Notas de la transcripción:* En b) la guía escribe 0.3222 con punto decimal.

---

### II-13 · Problema 13 (pág. 16)

**Enunciado.** Una hilandería adquiere una nueva máquina cuyo fabricante asegura gran regularidad en espesores y tensionado del hilado. Para un determinado tipo, el peso promedio por metro máximo deberá ser de 1,5 gramos con un desvío estándar máximo de 0,015 gramos/metro, lo que entra cómodamente en las especificaciones de la máquina. No obstante, dada la importancia del peso medio (por su incidencia directa en los costos) y de la variabilidad que afecta a la calidad del producto, se realiza una prueba piloto de la que se extraen 9 muestras de 1 metro con los siguientes resultados: Muestra N°: 1 - 2 - 3 - 4 - 5 - 6 - 7 - 8 - 9; Peso (g/m): 1,55 - 1,50 - 1,54 - 1,57 - 1,51 - 1,52 - 1,53 - 1,52 - 1,56.

- **a)** Asumiendo un 5% de riesgo máximo, ¿qué se puede decir a la luz de los resultados obtenidos en la prueba piloto?
- **b)** Estimar el peso medio por metro y el desvío standard de la producción total de la máquina con un Nivel de Confianza del 95%.
- **c)** ¿Cuántas muestras más se deberán extraer y adicionar a la prueba piloto para disminuir en un 60% la relación entre límites de la estimación del desvío standard calculado en b)?

| Muestra N° | Peso (g/m) |
|---|---|
| 1 | 1,55 |
| 2 | 1,5 |
| 3 | 1,54 |
| 4 | 1,57 |
| 5 | 1,51 |
| 6 | 1,52 |
| 7 | 1,53 |
| 8 | 1,52 |
| 9 | 1,56 |

*Tema detectado por la app: Varianza / desvío de 1 población (σ², σ).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Doble condición: hacer DOS ensayos, uno sobre la media μ (t de Student) y otro sobre el desvío σ (χ²), ambos con H1 '>'. Solo se recomienda si se rechazan las DOS hipótesis nulas.

- **Procesar la muestra**: n = 9, x̄ = Σxᵢ/n = 1,5333, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,0235.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≤ 1,5 y σ ≤ 0,015 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ > 1,5 y σ > 0,015 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Modelos y distribuciones empleados**:  
• **Para la media**: La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n). Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)  
• **Para el desvío**: La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal). Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **— Sobre la media μ —**
- **1 · Planteo de hipótesis**: H0: μ ≤ 1,5  vs  H1: μ > 1,5.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student, ν = número de grados de libertad = 8. t(1-α) = 1,8595.
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 1,8595·S/√n = 1,5 + 1,8595·0,0235/√9 = 1,5145. Si x̄ > 1,5145 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 1,52; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 9 unidades y se calcula su media x̄. Si x̄ > 1,5145, se rechaza H0 → se puede asegurar que μ > 1,5. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 1,5.
- **6 · Cálculos y decisión**: x̄ = 1,5333 → cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,0014. La decisión se toma comparando x̄ con x̄c.
- **— Sobre el desvío σ —**
- **1 · Planteo de hipótesis**: H0: σ² ≤ 0,000225  vs  H1: σ² > 0,000225.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² con ν = 8.
- **4 · Condición de rechazo (CR)**: S²c = σ₀²·χ²/ν = 0,00022·χ²/8 = 0,00044 (Sc = 0,0209). Si S² > S²c ⇒ se rechaza H0. Informado (hacia afuera): Sc = 0,0209.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 9 unidades y se calcula su desvío S. Si S > 0,0209, se rechaza H0 → se puede asegurar que σ² > 0,000225. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que σ² > 0,000225.
- **6 · Cálculos y decisión**: S² = 0,00055 (S = 0,0235) → cae en la zona de rechazo.
- Dato informativo (la guía a veces lo informa; el profesor decide con S contra Sc): forma equivalente estandarizada ν·S²/σ₀² = 19,5556 y χ² de tabla = 15,5073.

**Conclusión:** Media: Con α = 0,05, x̄ = 1,5333 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: μ ≤ 1,5. Se puede asegurar que μ > 1,5. Desvío: Con α = 0,05, S = 0,0235 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: σ² ≤ 0,000225. Se puede asegurar que σ² > 0,000225. Se rechazan las DOS hipótesis nulas: se cumplen ambas condiciones → se recomienda.

**Respuesta de la guía:** H0) σ ≤ 0,015 g/m: Sc = 0,0209 g/m < S = 0,0235 g/m, se rechaza; el desvío no cumple la especificación. H0) μ ≤ 1,5 g/m: x̄c = 1,52 g/m < x̄ = 1,5333 g/m, se rechaza; el promedio no cumple la especificación. No se cumplen las especificaciones del fabricante (ni μ ni σ).

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar LOS DOS parámetros con un 95% de confianza: la media μ (σ desconocido → t de Student, ν = n-1) y el desvío σ (χ² con ν = n-1, intervalo no simétrico).

- **Procesar la muestra**: n = 9, x̄ = Σxᵢ/n = 1,5333, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,0235.
- **Modelos y distribuciones empleados**:  
• **Para la media**: La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n). Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)  
• **Para el desvío**: La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal). Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.
- **— Sobre la media μ —**
- **Distribución**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student con ν = número de grados de libertad = n-1 = 8. t(0,975; 8) = 2,306.
- **Límites**: A;B = x̄ ∓ t·S/√n = 1,5333 ∓ 2,306·0,0235/√9 = 1,5333 ∓ 0,018.
- **— Sobre el desvío σ —**
- **Distribución**: χ² con ν = n-1 = 8. χ²(0,025; 8) = 2,1797 y χ²(0,975; 8) = 17,5345.
- **Varianza**: A = (n-1)·S²/χ²(1-α/2) = 8·0,0006/17,5345 = 0,00025 ; B = (n-1)·S²/χ²(α/2) = 8·0,0006/2,1797 = 0,00202.
- **Desvío**: A' = √A = 0,0158 ; B' = √B = 0,0449. Relación entre límites R' = B'/A' = 2,8363.

**Conclusión:** Se concluye que la media poblacional estará comprendida entre 1,5153 y 1,5514, afirmándolo con un 95% de confianza, o sea: P(1,5153 ≤ μ ≤ 1,5514) = 0,95 (límites redondeados hacia afuera; sin redondear: 1,515306 y 1,55136). Con un 95% de confianza: P(0,00025 ≤ σ² ≤ 0,00202) = 0,95 y P(0,0158 ≤ σ ≤ 0,0450) = 0,95 (límites redondeados hacia afuera; sin redondear: σ² entre 0,000251 y 0,002019, σ entre 0,015841 y 0,044929).

**Respuesta de la guía:** Media: entre 1,51 g/m y 1,56 g/m (1,533 ± 0,0180). Desvío: entre 0,0158 g/m y 0,0450 g/m (R' = 2,8363).

#### c) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para reducir un 60% el error (o la relación entre límites). Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Procesar la muestra**: n = 9, x̄ = Σxᵢ/n = 1,5333, S = √[Σ(xᵢ - x̄)²/(n-1)] = 0,0235.
- **Modelos y distribuciones empleados**:  
• La variable X debe ser Normal: X ~ N(μ; σ²). Es un supuesto necesario (el modelo χ² no es robusto si X no es Normal).  
• Entonces (n-1)·S²/σ² ~ χ² con ν = n - 1 grados de libertad. La χ² es asimétrica, por eso el intervalo no es simétrico y en un ensayo bilateral hay dos valores críticos distintos.  
• El n sale de la relación entre límites R' = B'/A' (Ecuación de García para aproximar ν).
- **Relación buscada** R' = B'/A' = 1,1345 → R = (R')² = 1,2871.
- **Ecuación de García**: a = Z(1-α/2)·(R^(1/3)+1)/(2·(R^(1/3)-1)) = 23,3106; ν = (2/9)·(a + √(a²+1))² = 483,4513 → ν al entero superior; n = ν + 1 → 485.
- Control por búsqueda exacta en χ²: n = 485 (R' logrado = 1,1344).

**Conclusión:** Para reducir un 60% la relación entre límites (de R' = 2,8363 a R' = 1,1345), el tamaño de muestra necesario es n = 485. (Ecuación de García: a = 23,3106, ν = 483,4513.) Como ya se relevaron n_preliminar = 9 unidades, hay que tomar Δn = 485 - 9 = 476 unidades adicionales.

**Respuesta de la guía:** n = 485 muestras en total, o sea 476 muestras más (R' = 1,1345; R = 1,2871; a = 23,3106; ν = 483,45).

> 📝 *Notas de la transcripción:* En b) la expresión probabilística dice P(0,0158 g/m ≤ σ ≤ 0,04450 g/m) = 0,95 (errata, el límite calculado es 0,0450). En c) 'disminuir en un 60%' se resuelve como R' = 2,8363·0,4 = 1,1345.

<details><summary>Cómo lo concluye la guía</summary>

> Esta hipótesis se rechaza si en las 9 muestras el desvío es mayor que 0,0209 g/m. Como las 9 muestras obtenidas arrojaron un desvío de 0,0235 g/m, se rechaza la hipótesis y se puede asegurar que el desvío estándar no cumple con la especificación del fabricante que debe ser de 0,015 g/m como máximo.
> Esta hipótesis se rechaza si en las 9 muestras el promedio es mayor que 1,52 g/m. Como las 9 muestras obtenidas arrojaron un promedio de 1,5333 g/m, se rechaza la hipótesis y se puede asegurar que el promedio no cumple con la especificación del fabricante que debe ser de 1,5 g/m.
> Por lo tanto, se concluye que no se cumplen con las especificaciones establecidas por el fabricante (tanto μ como σ).
> Se concluye que el peso por metro promedio de todos los hilos estará comprendido entre 1,51 g/m y 1,56 g/m, afirmándolo con un 95% de confianza, o sea: P(1,51 g/m ≤ μ ≤ 1,56 g/m) = 0,95.
> Se concluye que el desvío estándar de la población estará comprendido entre 0,0158 g/m y 0,0450 g/m, afirmándolo con un 95% de confianza.
> Se necesitaría 485 muestras en total, o sea se deberían tomar 476 muestras más de las 9 seleccionadas inicialmente.

</details>

---

## TEMA III — Procesos de Bernoulli (proporciones)

### III-1 · Problema 1 (pág. 18)

**Enunciado.** El rating de un programa de televisión se mide como el porcentaje de hogares que está viendo el programa en un momento dado. Las compañías medidoras de rating cuentan con un panel de hogares colaboradores, los cuales tienen asociado un people meter (que es un dispositivo que registra a cada minuto si el televisor está encendido y en qué canal, y guarda la información del día en una base de datos). Se toma una compañía medidora la cual tiene un panel de 600 hogares colaboradores y ha registrado el rating de un determinado programa en 25 puntos. Es decir que el 25% de los hogares del panel vio todo el programa ese día.

- **a)** Calcular un intervalo de confianza del 90% para el rating de ese determinado programa.
- **b)** Sabiendo que cada people meter cuesta 320 U$s, calcular la inversión adicional en dispositivos necesaria para medir el rating con un error de muestreo de ± 1%.

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la proporción poblacional p con un 90% de confianza mediante un intervalo de confianza. La cátedra usa el modelo exacto (Beta / F).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El intervalo exacto usa la relación entre la Binomial y la distribución Beta (o F de Snedecor).
- **Datos**: n = 600, r = 150, p̂ = r/n = 0,25.
- **Modelo exacto** (Beta / F, el que usa la cátedra): A = 0,221 ; B = 0,2808.
- **Límite inferior (A)**: ν₁ = 2(n − r + 1) = 902, ν₂ = 2r = 300; F(0,95; 902; 300) = 1,172; A = 1/[1 + (451/150)·1,172] = 0,22105.
- **Límite superior (B)**: ν₁ = 2(r + 1) = 302, ν₂ = 2(n − r) = 900; F(0,95; 302; 900) = 1,1635; B = 1/[1 + 450/(151·1,1635)] = 0,280792.
- La estimación de p es siempre exacta (Beta / F). La aproximación normal NO se usa para estimar p: el profesor la llama «aberración»; las aproximaciones solo sirven para calcular n.

**Conclusión:** El porcentaje poblacional estará entre 22,1% y 28,08%, con un 90% de confianza: P(0,2210 ≤ p ≤ 0,2808) = 0,9 (límites redondeados hacia afuera; sin redondear: 0,22105 y 0,280792).

**Respuesta de la guía:** Entre 22,10% y 28,08% (A = 0,2210; B = 0,2808; e = 0,0299).

#### b) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para un error máximo e = 0,01. Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• Para el n se usa la aproximación Normal: p̂ ~ N(p; p(1-p)/n). La aproximación se justifica con el n RESULTANTE: normal si n·p > 10 y n·(1-p) > 10; Poisson si p ≤ 0,005; si se cumplen las dos o ninguna, criterio de Mermoz (n₀ = 0,23·(1-p)²/p³).
- **Fórmula** (aprox. normal): n = Z²·p̂(1-p̂)/e² + 1 = 1,6449²·0,25·0,75/0,01² + 1 → n = 5074.
- **Justificación de la aproximación**: Criterio de aproximación con el n resultante: n·p = 5074·0,25 = 1268,5 y n·(1 − p) = 3805,5 (los dos > 10); p = 0,25 > 0,005 → aproximación normal.
- **Costo** adicional (Δn·c): 4474·320 = 1.431.680.

**Conclusión:** El tamaño de muestra necesario es n = 5074. Respecto de la muestra de 600: Δn = 4474. Inversión adicional (Δn·c): 1.431.680.

**Respuesta de la guía:** n = 5.074 hogares en total (aproximación normal); 4.474 people meter más; inversión adicional de 1.431.680 U$s.

<details><summary>Cómo lo concluye la guía</summary>

> Se concluye que el porcentaje de hogares de la población de establecimientos estará comprendido entre 22,10% y 28,08%, afirmándolo con un 90% de confianza, o sea: P(22,10% ≤ p ≤ 28,08%) = 0,90.
> Para calcular el valor de n, de manera que se reduzca el error a 0,01, no se puede calcular con el modelo binomial y hay que usar aproximaciones, en este caso se utiliza la distribución normal como aproximación.
> Se necesitan un total de 5.074 hogares colaboradores. Significa que se necesitarán 4.474 people meter más, y, como cada people meter tiene un costo de 320 U$s, se necesitará una inversión adicional de 1.431.680 U$s.

</details>

---

### III-2 · Problema 2 (pág. 18)

**Enunciado.** En un taller metalúrgico se controla diariamente la fracción defectuosa de un tipo de biela (se considera defectuosa la biela a la cual se le detecta poros de fundición). El control consiste en tomar una muestra de 25 unidades y sometiéndolas a un ensayo de ultrasonido para detectar dichos poros. En una de estas muestras se encontraron 3 unidades defectuosas. Se pide calcular:

- **a)** Los límites de confianza del 95% para la fracción defectuosa.
- **b)** La fracción defectuosa máxima que hay en la población con una probabilidad de 0,95.

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la proporción poblacional p con un 95% de confianza mediante un intervalo de confianza. La cátedra usa el modelo exacto (Beta / F).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El intervalo exacto usa la relación entre la Binomial y la distribución Beta (o F de Snedecor).
- **Datos**: n = 25, r = 3, p̂ = r/n = 0,12.
- **Modelo exacto** (Beta / F, el que usa la cátedra): A = 0,0254 ; B = 0,3122.
- **Límite inferior (A)**: ν₁ = 2(n − r + 1) = 46, ν₂ = 2r = 6; F(0,975; 46; 6) = 4,9916; A = 1/[1 + (23/3)·4,9916] = 0,025465.
- **Límite superior (B)**: ν₁ = 2(r + 1) = 8, ν₂ = 2(n − r) = 44; F(0,975; 8; 44) = 2,4964; B = 1/[1 + 22/(4·2,4964)] = 0,31219.
- La estimación de p es siempre exacta (Beta / F). La aproximación normal NO se usa para estimar p: el profesor la llama «aberración»; las aproximaciones solo sirven para calcular n.

**Conclusión:** El porcentaje poblacional estará entre 2,54% y 31,22%, con un 95% de confianza: P(0,0254 ≤ p ≤ 0,3122) = 0,95 (límites redondeados hacia afuera; sin redondear: 0,025465 y 0,31219).

**Respuesta de la guía:** Entre 0,0254 (2,54%) y 0,3122 (31,22%).

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la proporción poblacional p con un 95% de confianza mediante un intervalo de confianza. La cátedra usa el modelo exacto (Beta / F).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El intervalo exacto usa la relación entre la Binomial y la distribución Beta (o F de Snedecor).
- **Límite unilateral** (máximo): todo α = 0,05 va a una sola cola → se calcula como el extremo del IC con riesgo 2α = 0,1.
- **Datos**: n = 25, r = 3, p̂ = r/n = 0,12.
- **Modelo exacto** (Beta / F, el que usa la cátedra): A = 0,0335 ; B = 0,2818.
- **Límite inferior (A)**: ν₁ = 2(n − r + 1) = 46, ν₂ = 2r = 6; F(0,95; 46; 6) = 3,7609; A = 1/[1 + (23/3)·3,7609] = 0,03352.
- **Límite superior (B)**: ν₁ = 2(r + 1) = 8, ν₂ = 2(n − r) = 44; F(0,95; 8; 44) = 2,1572; B = 1/[1 + 22/(4·2,1572)] = 0,281723.
- La estimación de p es siempre exacta (Beta / F). La aproximación normal NO se usa para estimar p: el profesor la llama «aberración»; las aproximaciones solo sirven para calcular n.

**Conclusión:** Con un 95% de confianza, p ≤ 0,2818: P(p ≤ 0,2818) = 0,95 (cota máxima redondeada hacia arriba; sin redondear 0,281723).

**Respuesta de la guía:** B = 0,2818 (28,18%).

> 📝 *Notas de la transcripción:* La solución anuncia las expresiones exactas con el modelo F pero no las muestra (la página pasa directo al inciso b).

<details><summary>Cómo lo concluye la guía</summary>

> Entre el 2,54% y 31,22%, con un 95% de confianza.

</details>

---

### III-3 · Problema 3 (pág. 19)

**Enunciado.** Calcular los límites de confianza del 90% de la fracción de defectuosa, si de un proceso productivo se tomó una muestra de 10 unidades en la cual se encontró:

- **a)** 1 unidad defectuosa.
- **b)** 0 unidades defectuosas.

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la proporción poblacional p con un 90% de confianza mediante un intervalo de confianza. La cátedra usa el modelo exacto (Beta / F).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El intervalo exacto usa la relación entre la Binomial y la distribución Beta (o F de Snedecor).
- **Datos**: n = 10, r = 1, p̂ = r/n = 0,1.
- **Modelo exacto** (Beta / F, el que usa la cátedra): A = 0,0051 ; B = 0,3942.
- **Límite inferior (A)**: ν₁ = 2(n − r + 1) = 20, ν₂ = 2r = 2; F(0,95; 20; 2) = 19,4458; A = 1/[1 + (10/1)·19,4458] = 0,005116.
- **Límite superior (B)**: ν₁ = 2(r + 1) = 4, ν₂ = 2(n − r) = 18; F(0,95; 4; 18) = 2,9277; B = 1/[1 + 9/(2·2,9277)] = 0,394163.
- La estimación de p es siempre exacta (Beta / F). La aproximación normal NO se usa para estimar p: el profesor la llama «aberración»; las aproximaciones solo sirven para calcular n.

**Conclusión:** El porcentaje poblacional estará entre 0,51% y 39,42%, con un 90% de confianza: P(0,0051 ≤ p ≤ 0,3942) = 0,9 (límites redondeados hacia afuera; sin redondear: 0,005116 y 0,394163).

**Respuesta de la guía:** Entre 0,0051 (0,51%) y 0,3942 (39,42%).

#### b) Intervalo de confianza (estimar) ⚠️

*Qué pide:* Estimar la proporción poblacional p con un 90% de confianza mediante un intervalo de confianza. La cátedra usa el modelo exacto (Beta / F).

> ⚠️ Con r = 0 el límite inferior es 0 y hay un solo límite: el superior se calcula con α entero (criterio del profesor en clase). La guía usa α/2 en III-3b y daría 0.2589: el profesor dijo que eso está mal.

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El intervalo exacto usa la relación entre la Binomial y la distribución Beta (o F de Snedecor).
- **Datos**: n = 10, r = 0, p̂ = r/n = 0.
- **Modelo exacto** (Beta / F, el que usa la cátedra): A = 0 ; B = 0,2057.
- **Un solo límite**: con r = 0 el límite inferior es 0 y queda un único límite, que se calcula con α ENTERO = 0,1 (no α/2): «todo el riesgo lo juntás en un límite» (profesor en clase; la guía usa α/2 en III-3b y está mal).
- **Límite superior (B)**: ν₁ = 2(r + 1) = 2, ν₂ = 2(n − r) = 20; F(0,9; 2; 20) = 2,5893; B = 1/[1 + 10/(1·2,5893)] = 0,205672.
- La estimación de p es siempre exacta (Beta / F). La aproximación normal NO se usa para estimar p: el profesor la llama «aberración»; las aproximaciones solo sirven para calcular n.

**Conclusión:** El porcentaje poblacional estará entre 0% y 20,57%, con un 90% de confianza: P(0,0000 ≤ p ≤ 0,2057) = 0,9 (límites redondeados hacia afuera; sin redondear: 0 y 0,205672).

**Respuesta de la guía:** Entre 0 (0%) y 0,2589 (25,89%).

> ⚠️ **No coincide con la guía** (no aparecen: 0,2589). Ver la lista de discrepancias.

> 📝 *Notas de la transcripción:* En b) (r = 0) la guía usa α/2 = 0,05 para el límite superior (0,2589); con r = 0 el límite unilateral con α = 0,10 daría 0,2057. Se transcribe igual.

---

### III-4 · Problema 4 (pág. 19)

**Enunciado.** En un estudio de muestreo de trabajo se indica que, sobre una muestra de 600 observaciones, una máquina se mantuvo inactiva el 10% del tiempo total.

*¿Cuáles serán los límites de confianza para la proporción de tiempo inactivo? (Tomar un Nivel de Confianza de 0,95).*

*Tema detectado por la app: Proporción de 1 población (p).*

#### Resolución (Intervalo de confianza (estimar)) ✅

*Qué pide:* Estimar la proporción poblacional p con un 95% de confianza mediante un intervalo de confianza. La cátedra usa el modelo exacto (Beta / F).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El intervalo exacto usa la relación entre la Binomial y la distribución Beta (o F de Snedecor).
- **Datos**: n = 600, r = 60, p̂ = r/n = 0,1.
- **Modelo exacto** (Beta / F, el que usa la cátedra): A = 0,0771 ; B = 0,1269.
- **Límite inferior (A)**: ν₁ = 2(n − r + 1) = 1082, ν₂ = 2r = 120; F(0,975; 1082; 120) = 1,3261; A = 1/[1 + (541/60)·1,3261] = 0,07718.
- **Límite superior (B)**: ν₁ = 2(r + 1) = 122, ν₂ = 2(n − r) = 1080; F(0,975; 122; 1080) = 1,286; B = 1/[1 + 540/(61·1,286)] = 0,126843.
- La estimación de p es siempre exacta (Beta / F). La aproximación normal NO se usa para estimar p: el profesor la llama «aberración»; las aproximaciones solo sirven para calcular n.

**Conclusión:** El porcentaje poblacional estará entre 7,71% y 12,69%, con un 95% de confianza: P(0,0771 ≤ p ≤ 0,1269) = 0,95 (límites redondeados hacia afuera; sin redondear: 0,07718 y 0,126843).

**Respuesta de la guía:** Entre 0,0771 (7,71%) y 0,1269 (12,69%).

---

### III-5 · Problema 5 (pág. 19)

**Enunciado.** La producción de llantas del país se clasifica en tres categorías: llantas de primera, llantas con acabado imperfecto y llantas defectuosas. Las últimas dos categorías implican pérdidas para la compañía, ya que se venden en un precio menor o se desechan. En una fábrica de importancia se obtuvieron 198 llantas, en una muestra aleatoria de 1.000 llantas, que no cumplieron los requisitos para ser de primera.

*Estimar, con un intervalo de confianza del 95%, el porcentaje de llantas que no son de primera en toda la producción del país.*

*Tema detectado por la app: Proporción de 1 población (p).*

#### Resolución (Intervalo de confianza (estimar)) ✅

*Qué pide:* Estimar la proporción poblacional p con un 95% de confianza mediante un intervalo de confianza. La cátedra usa el modelo exacto (Beta / F).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El intervalo exacto usa la relación entre la Binomial y la distribución Beta (o F de Snedecor).
- **Datos**: n = 1000, r = 198, p̂ = r/n = 0,198.
- **Modelo exacto** (Beta / F, el que usa la cátedra): A = 0,1737 ; B = 0,2241.
- **Límite inferior (A)**: ν₁ = 2(n − r + 1) = 1606, ν₂ = 2r = 396; F(0,975; 1606; 396) = 1,1728; A = 1/[1 + (803/198)·1,1728] = 0,17372.
- **Límite superior (B)**: ν₁ = 2(r + 1) = 398, ν₂ = 2(n − r) = 1604; F(0,975; 398; 1604) = 1,1638; B = 1/[1 + 802/(199·1,1638)] = 0,224072.
- La estimación de p es siempre exacta (Beta / F). La aproximación normal NO se usa para estimar p: el profesor la llama «aberración»; las aproximaciones solo sirven para calcular n.

**Conclusión:** El porcentaje poblacional estará entre 17,37% y 22,41%, con un 95% de confianza: P(0,1737 ≤ p ≤ 0,2241) = 0,95 (límites redondeados hacia afuera; sin redondear: 0,17372 y 0,224072).

**Respuesta de la guía:** Entre 17,37 y 22,41%.

---

### III-6 · Problema 6 (pág. 19)

**Enunciado.** Un inspector de control de calidad ha encontrado, en una muestra de 30 tornillos, que el 30% de los mismos tienen algún tipo de defecto.

*Se desea conocer el intervalo de confianza del 95% para el porcentaje de tornillos defectuosos de toda la producción.*

*Tema detectado por la app: Proporción de 1 población (p).*

#### Resolución (Intervalo de confianza (estimar)) ✅

*Qué pide:* Estimar la proporción poblacional p con un 95% de confianza mediante un intervalo de confianza. La cátedra usa el modelo exacto (Beta / F).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El intervalo exacto usa la relación entre la Binomial y la distribución Beta (o F de Snedecor).
- **Datos**: n = 30, r = 9, p̂ = r/n = 0,3.
- **Modelo exacto** (Beta / F, el que usa la cátedra): A = 0,1473 ; B = 0,494.
- **Límite inferior (A)**: ν₁ = 2(n − r + 1) = 44, ν₂ = 2r = 18; F(0,975; 44; 18) = 2,3673; A = 1/[1 + (22/9)·2,3673] = 0,147345.
- **Límite superior (B)**: ν₁ = 2(r + 1) = 20, ν₂ = 2(n − r) = 42; F(0,975; 20; 42) = 2,0499; B = 1/[1 + 21/(10·2,0499)] = 0,493959.
- La estimación de p es siempre exacta (Beta / F). La aproximación normal NO se usa para estimar p: el profesor la llama «aberración»; las aproximaciones solo sirven para calcular n.

**Conclusión:** El porcentaje poblacional estará entre 14,73% y 49,4%, con un 95% de confianza: P(0,1473 ≤ p ≤ 0,4940) = 0,95 (límites redondeados hacia afuera; sin redondear: 0,147345 y 0,493959).

**Respuesta de la guía:** Entre 14,73 y 49,40%.

---

### III-7 · Problema 7 (pág. 19)

**Enunciado.** En los presupuestos de mano de obra se ha establecido el nivel de ausentismo en un valor igual al 7% respecto de los "días – hombre" disponibles. En un análisis efectuado sobre 1.000 "días – hombre" se ha registrado un 8,5% de ausentismo.

*Para un riesgo del 10%, ¿se puede decir que se han modificado las condiciones previstas en los presupuestos?*

*Tema detectado por la app: Proporción de 1 población (p).*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la proporción poblacional p: H1 con signo '≠'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

> ⚠️ No existen ensayos bilaterales sobre p (el profesor: «no existe caso bilateral»). Se planteó el unilateral hacia arriba, que es lo que la muestra/enunciado sugiere probar: revisá qué dice el enunciado que se quiere probar (eso va en H1).

- **1 · Planteo de hipótesis**: H0: p ≤ 0,07  vs  H1: p > 0,07.
- **Justificación de H0**:  
• H1: p > 0,07 recoge lo que el enunciado quiere probar; H0: p ≤ 0,07 es el complemento y lleva la igualdad (el valor de referencia 0,07).  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: binomial exacto con n = 1000 y p₀ = 0,07.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **4 · Condición de rechazo (CR)**: r_c es el menor valor con G_b(r_c | n = 1000; p₀ = 0,07) ≤ α: G_b(80) = 0,1207 > α y G_b(81) = 0,0985 ≤ α → r_c = 81 (α real = 0,0985 ≤ α = 0,1; el α real nunca puede superar al estipulado). Si r ≥ 81 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 1000 unidades y se cuenta la cantidad r de casos. Si r ≥ 81, se rechaza H0 → se puede asegurar que p > 0,07. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que p > 0,07.
- **6 · Cálculos y decisión**: r = 85 (p̂ = 0,085) ≥ r_c = 81 → se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,0391. El profesor decide con r contra r_c (a priori); el α* «no me gusta».

**Conclusión:** Con α = 0,1, r = 85 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: p ≤ 0,07. Se puede asegurar que p > 0,07.

**Respuesta de la guía:** Si, se puede asegurar que el nivel de ausentismo ha aumentado.

---

### III-8 · Problema 8 (pág. 19)

**Enunciado.** Una empresa comercializadora de cosméticos ha diseñado un nuevo catálogo para promocionar un producto, con el cual espera aumentar el porcentaje de clientes compradores en 2 puntos al menos. Con el catálogo actual, se sabe que cada vez que el mismo se envía a potenciales clientes, el porcentaje de compradores es del 8%. Para probar la efectividad del nuevo catálogo se envían una cantidad de 100 catálogos a posibles clientes y al tiempo se reciben 14 pedidos.

- **a)** Calcular el intervalo de confianza del 90% para el porcentaje de compradores.
- **b)** Calcular el nuevo tamaño de muestra para un error muestral de 0,02.
- **c)** ¿Se considera que la prueba ha sido concluyente para cambiar de catálogo asumiendo un 5% de riesgo?, es decir, ¿se considera que la prueba permite asegurar que con el nuevo catálogo el porcentaje de clientes compradores es superior al 10%?
- **d)** ¿Cuál es la probabilidad de cambiar de catálogo si con el nuevo se logra una efectividad de respuesta del 12%?

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la proporción poblacional p con un 90% de confianza mediante un intervalo de confianza. La cátedra usa el modelo exacto (Beta / F).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El intervalo exacto usa la relación entre la Binomial y la distribución Beta (o F de Snedecor).
- **Datos**: n = 100, r = 14, p̂ = r/n = 0,14.
- **Modelo exacto** (Beta / F, el que usa la cátedra): A = 0,0866 ; B = 0,2102.
- **Límite inferior (A)**: ν₁ = 2(n − r + 1) = 174, ν₂ = 2r = 28; F(0,95; 174; 28) = 1,6958; A = 1/[1 + (87/14)·1,6958] = 0,086668.
- **Límite superior (B)**: ν₁ = 2(r + 1) = 30, ν₂ = 2(n − r) = 172; F(0,95; 30; 172) = 1,5256; B = 1/[1 + 86/(15·1,5256)] = 0,210174.
- La estimación de p es siempre exacta (Beta / F). La aproximación normal NO se usa para estimar p: el profesor la llama «aberración»; las aproximaciones solo sirven para calcular n.

**Conclusión:** El porcentaje poblacional estará entre 8,66% y 21,02%, con un 90% de confianza: P(0,0866 ≤ p ≤ 0,2102) = 0,9 (límites redondeados hacia afuera; sin redondear: 0,086668 y 0,210174).

**Respuesta de la guía:** Entre 8,66 y 21,02%.

#### b) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para un error máximo e = 0,02. Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• Para el n se usa la aproximación Normal: p̂ ~ N(p; p(1-p)/n). La aproximación se justifica con el n RESULTANTE: normal si n·p > 10 y n·(1-p) > 10; Poisson si p ≤ 0,005; si se cumplen las dos o ninguna, criterio de Mermoz (n₀ = 0,23·(1-p)²/p³).
- **Fórmula** (aprox. normal): n = Z²·p̂(1-p̂)/e² + 1 = 1,6449²·0,14·0,86/0,02² + 1 → n = 816.
- **Justificación de la aproximación**: Criterio de aproximación con el n resultante: n·p = 816·0,14 = 114,24 y n·(1 − p) = 701,76 (los dos > 10); p = 0,14 > 0,005 → aproximación normal.

**Conclusión:** El tamaño de muestra necesario es n = 816. Respecto de la muestra de 100: Δn = 716.

**Respuesta de la guía:** n = 816 catálogos (por aproximación normal).

#### c) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la proporción poblacional p: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: p ≤ 0,1  vs  H1: p > 0,1.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: p ≤ 0,1 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: p > 0,1 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: binomial exacto con n = 100 y p₀ = 0,1.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **4 · Condición de rechazo (CR)**: r_c es el menor valor con G_b(r_c | n = 100; p₀ = 0,1) ≤ α: G_b(15) = 0,0726 > α y G_b(16) = 0,0399 ≤ α → r_c = 16 (α real = 0,0399 ≤ α = 0,05; el α real nunca puede superar al estipulado). Si r ≥ 16 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 100 unidades y se cuenta la cantidad r de casos. Si r ≥ 16, se rechaza H0 → se puede asegurar que p > 0,1. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que p > 0,1.
- **6 · Cálculos y decisión**: r = 14 (p̂ = 0,14) no es ≥ r_c = 16 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,1239. El profesor decide con r contra r_c (a priori); el α* «no me gusta».

**Conclusión:** Con α = 0,05, r = 14 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: p ≤ 0,1. No hay evidencia suficiente para asegurar que p > 0,1 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No, no se puede asegurar que con el nuevo catálogo el porcentaje de compradores sea superior al 10%.

#### d) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: p ≤ 0,1  vs  H1: p > 0,1  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Modelo**: binomial exacto con n = 100 y p₀ = 0,1.
- **Condición de rechazo**: r_c es el menor valor con G_b(r_c | n = 100; p₀ = 0,1) ≤ α: G_b(15) = 0,0726 > α y G_b(16) = 0,0399 ≤ α → r_c = 16 (α real = 0,0399 ≤ α = 0,05; el α real nunca puede superar al estipulado). Si r ≥ 16 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **β** = P(no rechazar H0 | p = 0,12) = F_b(15 | n = 100; p₁ = 0,12) = 0,8586.
- **Potencia** 1-β = 0,1414.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,1414 (β = 0,8586).

**Respuesta de la guía:** 1–β = 0,1415.

---

### III-9 · Problema 9 (pág. 19)

**Enunciado.** Una empresa productora de bebidas gaseosas iniciará una campaña publicitaria televisiva si el porcentaje de televidentes que ven programas deportivos en forma continuada es superior al 60%. A efectos de tomar una decisión se analiza una muestra de 500 televidentes comprobando que 325 de ellos ven programas deportivos en forma continuada, y se establece en un 10% el riesgo máximo de iniciar la campaña cuando el porcentaje no supera el 60%.

- **a)** A la luz de los datos obtenidos, ¿Se aconseja iniciar la campaña?
- **b)** ¿Cuál es la probabilidad de no iniciar la campaña cuando el porcentaje de televidentes es del 66%?
- **c)** ¿Cuál es la probabilidad de iniciar la campaña cuando dicho porcentaje es del 68%?
- **d)** Dibujar las curvas Característica Operativa y de Potencia.

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la proporción poblacional p: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: p ≤ 0,6  vs  H1: p > 0,6.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: p ≤ 0,6 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: p > 0,6 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: binomial exacto con n = 500 y p₀ = 0,6.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **4 · Condición de rechazo (CR)**: r_c es el menor valor con G_b(r_c | n = 500; p₀ = 0,6) ≤ α: G_b(314) = 0,1086 > α y G_b(315) = 0,0924 ≤ α → r_c = 315 (α real = 0,0924 ≤ α = 0,1; el α real nunca puede superar al estipulado). Si r ≥ 315 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 500 unidades y se cuenta la cantidad r de casos. Si r ≥ 315, se rechaza H0 → se puede asegurar que p > 0,6. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que p > 0,6.
- **6 · Cálculos y decisión**: r = 325 (p̂ = 0,65) ≥ r_c = 315 → se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,0122. El profesor decide con r contra r_c (a priori); el α* «no me gusta».

**Conclusión:** Con α = 0,1, r = 325 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: p ≤ 0,6. Se puede asegurar que p > 0,6.

**Respuesta de la guía:** Sí, se puede afirmar que el porcentaje de televidentes es superior al 60% y se aconseja iniciar la campaña.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: p ≤ 0,6  vs  H1: p > 0,6  (α = 0,1).
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Modelo**: binomial exacto con n = 500 y p₀ = 0,6.
- **Condición de rechazo**: r_c es el menor valor con G_b(r_c | n = 500; p₀ = 0,6) ≤ α: G_b(314) = 0,1086 > α y G_b(315) = 0,0924 ≤ α → r_c = 315 (α real = 0,0924 ≤ α = 0,1; el α real nunca puede superar al estipulado). Si r ≥ 315 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **β** = P(no rechazar H0 | p = 0,66) = F_b(314 | n = 500; p₁ = 0,66) = 0,0724.
- **Potencia** 1-β = 0,9276.

**Conclusión:** La probabilidad pedida es β = 0,0724 (potencia 1-β = 0,9276).

**Respuesta de la guía:** β = 0,0724.

#### c) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: p ≤ 0,6  vs  H1: p > 0,6  (α = 0,1).
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Modelo**: binomial exacto con n = 500 y p₀ = 0,6.
- **Condición de rechazo**: r_c es el menor valor con G_b(r_c | n = 500; p₀ = 0,6) ≤ α: G_b(314) = 0,1086 > α y G_b(315) = 0,0924 ≤ α → r_c = 315 (α real = 0,0924 ≤ α = 0,1; el α real nunca puede superar al estipulado). Si r ≥ 315 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **β** = P(no rechazar H0 | p = 0,68) = F_b(314 | n = 500; p₁ = 0,68) = 0,0078.
- **Potencia** 1-β = 0,9922.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,9922 (β = 0,0078).

**Respuesta de la guía:** 1–β = 0,9922.

#### d) Curva característica operativa / de potencia ℹ️

*Qué pide:* Tabular β y 1-β para varios valores del parámetro y graficar la curva OC (β) y la de potencia (1-β).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- Para cada p se calcula β = P(no rechazar H0 | p) con el binomial (n = 500).

**Conclusión:** Tabla de puntos para graficar las curvas (ver abajo).

**Respuesta de la guía:** Ver procedimiento de construcción de las curvas en el problema 12.

---

### III-10 · Problema 10 (pág. 20)

**Enunciado.** El director de un instituto superior de enseñanza no está conforme con la inscripción obtenida en los cursos a distancia, que actualmente es sólo del 5% sobre las cartas enviadas. Decide entonces encomendar la tarea de reorganizar dichos cursos a uno de sus profesores, quien ha de proponer los temas y programas. Se van a enviar n cartas a posibles interesados, tal que valga 0,20 la probabilidad de concluir erróneamente que la proporción aumentó y 0,90 la probabilidad de detectar que aumentó 2 puntos porcentuales.

- **a)** Indicar la condición de rechazo y la regla de decisión.
- **b)** Hallar la probabilidad de detectar que la proporción aumentó 1 punto porcentual.
- **c)** Suponer que se envían las n cartas y responden favorablemente el 5,2%, ¿se puede concluir que la proporción aumentó?
- **d)** Hallar la probabilidad de no detectar que la proporción aumentó en 2 puntos porcentuales.

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• H1: p > 0,05 recoge lo que el enunciado quiere probar; H0: p ≤ 0,05 es el complemento y lleva la igualdad (el valor de referencia 0,05).  
• α = P(rechazar H0 | H0 cierta) = 0,2 (error de tipo I); β = P(no rechazar H0 | p = 0,07) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≤ 0,05  vs  H1: p > 0,05.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condiciones**: P(rechazar | p₀ = 0,05) ≤ α = 0,2 y P(no rechazar | p₁ = 0,07) ≤ β = 0,1.
- **Plan (binomial exacto, se itera n)**: n = 638, r_c = 37. α real = 0,1993, β real = 0,1.
- **Regla de decisión**: Tomar una muestra de n = 638. Si se encuentran r ≥ 37 casos, se rechaza H0.
- **Por aproximación normal**: n = [(Z(1-α)·√(p₀q₀) + Z(1-β)·√(p₁q₁))/(p₁ - p₀)]² → n = 652; con ese n el binomial da r_c = 38 (α real = 0,1875, β real = 0,1032). Criterio de aproximación con el n resultante: n·p = 652·0,05 = 32,6 y n·(1 − p) = 619,4 (los dos > 10); p = 0,05 > 0,005 → aproximación normal.
- **Otros planes válidos**: para cada r_c, todos los n del rango cumplen α y β (uno de los riesgos baja y el otro sube con n). La app informa el menor n; la guía a veces da el mayor del rango o usa el r_c siguiente.

| r_c | n mínimo | n máximo |
|---|---|---|
| 37 | 638 | 638 |
| 38 | 654 | 656 |
| 39 | 670 | 675 |

- **Por aproximación de Poisson** (Ecuación de García): R = p₁/p₀ = 1,4; a = [Z(1-β) + Z(1-α)·∛R]/[2(∛R - 1)] = 9,3651; ν = 2/9·(a + √(a² + 1))² = 78,4036; c = ⌊ν/2⌋ = 39 → g.l. = 2c = 78; n = máx[χ²(α; 78)/(2p₀) ; χ²(1-β; 78)/(2p₁)] = máx[673,4146 ; 674,0965] → n = 675; r_c = c + 1 = 40. Criterio de aproximación con el n resultante: n·p = 675·0,05 = 33,75 y n·(1 − p) = 641,25 (los dos > 10); p = 0,05 > 0,005 → aproximación normal. ⚠️ Con el n resultante el criterio NO habilita Poisson: este n no es una respuesta válida (el profesor, sobre III-11c: el 855 por Poisson es incorrecto porque el criterio se aplicó con el n inicial).

**Conclusión:** Tomar una muestra de n = 638. Si se encuentran r ≥ 37 casos, se rechaza H0. (Por aproximación normal, justificada con el n resultante: n = 652 y r_c = 38.)

**Respuesta de la guía:** CR: Si r ≥ rc = 37 ⇒ rechazo la H0, si en una muestra de 638 cartas hay 37 o más inscriptos, se concluye que el porcentaje de inscriptos aumentó; o n = 652 cartas y rc = 38 (por aproximación normal).

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: p ≤ 0,05  vs  H1: p > 0,05  (α = 0,2).
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Modelo**: binomial exacto con n = 638 y p₀ = 0,05.
- **Condición de rechazo**: r_c es el menor valor con G_b(r_c | n = 638; p₀ = 0,05) ≤ α: G_b(36) = 0,2516 > α y G_b(37) = 0,1993 ≤ α → r_c = 37 (α real = 0,1993 ≤ α = 0,2; el α real nunca puede superar al estipulado). Si r ≥ 37 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **β** = P(no rechazar H0 | p = 0,06) = F_b(36 | n = 638; p₁ = 0,06) = 0,392.
- **Potencia** 1-β = 0,608.
- **Con el plan por aproximación normal** (n = 652, r_c = 38): 1-β = 0,5966, β = 0,4034.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,608 (β = 0,392).

**Respuesta de la guía:** 1–β = 0,6080 o 1–β = 0,5966 (por Normal).

#### c) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la proporción poblacional p: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: p ≤ 0,05  vs  H1: p > 0,05.
- **Justificación de H0**:  
• H1: p > 0,05 recoge lo que el enunciado quiere probar; H0: p ≤ 0,05 es el complemento y lleva la igualdad (el valor de referencia 0,05).  
• α = P(rechazar H0 | H0 cierta) = 0,2 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,2 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: binomial exacto con n = 638 y p₀ = 0,05.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **4 · Condición de rechazo (CR)**: r_c es el menor valor con G_b(r_c | n = 638; p₀ = 0,05) ≤ α: G_b(36) = 0,2516 > α y G_b(37) = 0,1993 ≤ α → r_c = 37 (α real = 0,1993 ≤ α = 0,2; el α real nunca puede superar al estipulado). Si r ≥ 37 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 638 unidades y se cuenta la cantidad r de casos. Si r ≥ 37, se rechaza H0 → se puede asegurar que p > 0,05. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que p > 0,05.
- **6 · Cálculos y decisión**: r = 33 (p̂ = 0,0517) no es ≥ r_c = 37 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,4459. El profesor decide con r contra r_c (a priori); el α* «no me gusta».

**Conclusión:** Con α = 0,2, r = 33 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: p ≤ 0,05. No hay evidencia suficiente para asegurar que p > 0,05 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No, no se puede asegurar que la proporción de inscriptos haya aumentado.

#### d) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: p ≤ 0,05  vs  H1: p > 0,05  (α = 0,2).
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Modelo**: binomial exacto con n = 638 y p₀ = 0,05.
- **Condición de rechazo**: r_c es el menor valor con G_b(r_c | n = 638; p₀ = 0,05) ≤ α: G_b(36) = 0,2516 > α y G_b(37) = 0,1993 ≤ α → r_c = 37 (α real = 0,1993 ≤ α = 0,2; el α real nunca puede superar al estipulado). Si r ≥ 37 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **β** = P(no rechazar H0 | p = 0,07) = F_b(36 | n = 638; p₁ = 0,07) = 0,1.
- **Potencia** 1-β = 0,9.
- **Con el plan por aproximación normal** (n = 652, r_c = 38): 1-β = 0,8968, β = 0,1032.

**Conclusión:** La probabilidad pedida es β = 0,1 (potencia 1-β = 0,9).

**Respuesta de la guía:** β = 0,10 (es dato).

---

### III-11 · Problema 11 (pág. 20)

**Enunciado.** El proceso productivo de una pieza trabaja en condiciones normales con un 12% de unidades defectuosas. Este porcentaje se controla periódicamente tomando muestras de 50 unidades y contando cuántas defectuosas hay. Si el proceso está bajo control, la probabilidad de detenerlo y revisarlo debe valer 0,05.

- **a)** ¿Cuántas defectuosas se deberán encontrar en la muestra de 50 para detener el proceso y revisarlo?
- **b)** ¿Cuál es la probabilidad de no detener el proceso cuando el porcentaje de defectuosas es del 14%? Dibuje la curva característica de operación.
- **c)** ¿Cuántas unidades se deberán controlar si se pretende disminuir a 0,50 la probabilidad anterior?

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: p ≤ 0,12 supone que cumple; H1: p > 0,12 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≤ 0,12  vs  H1: p > 0,12.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condición de rechazo**: r_c es el menor valor con G_b(r_c | n = 50; p₀ = 0,12) ≤ α: G_b(10) = 0,0708 > α y G_b(11) = 0,0325 ≤ α → r_c = 11 (α real = 0,0325 ≤ α = 0,05; el α real nunca puede superar al estipulado). Si r ≥ 11 ⇒ se rechaza H0.

**Conclusión:** Si en la muestra de 50 se encuentran r ≥ 11, se rechaza H0.

**Respuesta de la guía:** Por lo menos 11 defectuosas.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: p ≤ 0,12  vs  H1: p > 0,12  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Modelo**: binomial exacto con n = 50 y p₀ = 0,12.
- **Condición de rechazo**: r_c es el menor valor con G_b(r_c | n = 50; p₀ = 0,12) ≤ α: G_b(10) = 0,0708 > α y G_b(11) = 0,0325 ≤ α → r_c = 11 (α real = 0,0325 ≤ α = 0,05; el α real nunca puede superar al estipulado). Si r ≥ 11 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **β** = P(no rechazar H0 | p = 0,14) = F_b(10 | n = 50; p₁ = 0,14) = 0,9176.
- **Potencia** 1-β = 0,0824.

**Conclusión:** La probabilidad pedida es β = 0,9176 (potencia 1-β = 0,0824).

**Respuesta de la guía:** β = 0,9176. Ver procedimiento de construcción de la curva en el problema 12.

#### c) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ⚠️

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: p ≤ 0,12 supone que cumple; H1: p > 0,12 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | p = 0,14) = 0,5 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≤ 0,12  vs  H1: p > 0,12.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condiciones**: P(rechazar | p₀ = 0,12) ≤ α = 0,05 y P(no rechazar | p₁ = 0,14) ≤ β = 0,5.
- **Plan (binomial exacto, se itera n)**: n = 755, r_c = 106. α real = 0,0499, β real = 0,4967.
- **Regla de decisión**: Tomar una muestra de n = 755. Si se encuentran r ≥ 106 casos, se rechaza H0.
- **Por aproximación normal**: n = [(Z(1-α)·√(p₀q₀) + Z(1-β)·√(p₁q₁))/(p₁ - p₀)]² → n = 715; con ese n el binomial da r_c = 101 (α real = 0,0478, β real = 0,5223). Criterio de aproximación con el n resultante: n·p = 715·0,12 = 85,8 y n·(1 − p) = 629,2 (los dos > 10); p = 0,12 > 0,005 → aproximación normal.
- **Otros planes válidos**: para cada r_c, todos los n del rango cumplen α y β (uno de los riesgos baja y el otro sube con n). La app informa el menor n; la guía a veces da el mayor del rango o usa el r_c siguiente.

| r_c | n mínimo | n máximo |
|---|---|---|
| 106 | 755 | 755 |
| 107 | 762 | 762 |
| 108 | 769 | 770 |

- **Por aproximación de Poisson** (Ecuación de García): R = p₁/p₀ = 1,1667; a = [Z(1-β) + Z(1-α)·∛R]/[2(∛R - 1)] = 16,4204; ν = 2/9·(a + √(a² + 1))² = 240,1142; c = ⌊ν/2⌋ = 120 → g.l. = 2c = 240; n = máx[χ²(α; 240)/(2p₀) ; χ²(1-β; 240)/(2p₁)] = máx[854,7308 ; 854,7631] → n = 855; r_c = c + 1 = 121. Criterio de aproximación con el n resultante: n·p = 855·0,12 = 102,6 y n·(1 − p) = 752,4 (los dos > 10); p = 0,12 > 0,005 → aproximación normal. ⚠️ Con el n resultante el criterio NO habilita Poisson: este n no es una respuesta válida (el profesor, sobre III-11c: el 855 por Poisson es incorrecto porque el criterio se aplicó con el n inicial).

**Conclusión:** Tomar una muestra de n = 755. Si se encuentran r ≥ 106 casos, se rechaza H0. (Por aproximación normal, justificada con el n resultante: n = 715 y r_c = 101.)

**Respuesta de la guía:** n = 755 piezas, o n = 715 piezas (por aproximación normal), o n= 855 piezas (por aproximación de Poisson). En este caso la aproximación de Poisson no es correcta, la cual sería adecuada si n = 50.

> ⚠️ **No coincide con la guía** (no aparecen: 855). Ver la lista de discrepancias.

---

### III-12 · Problema 12 (pág. 20)

**Enunciado.** Problema fundamental del Control de Recepción: En una empresa industrial se desea diseñar un sistema periódico de muestreo para el control de recepción de una pieza que es suministrada en grandes cantidades. El proveedor admite que, como máximo, le rechacen el 5% de las partidas buenas, que son aquellas que tienen un 11% de unidades defectuosas. A su vez, el comprador desea rechazar el 99% de las partidas malas, que son aquellas cuyo porcentaje defectuoso es del 16%.

- **a)** Determinar el Plan de Muestreo, o sea, ¿Cuántas unidades deberán revisarse de cada partida y cuántas defectuosas deberán encontrarse en la muestra de control para rechazar la partida?
- **b)** ¿Cuál es la probabilidad de rechazar una partida que tiene un 14% de unidades defectuosas?
- **c)** Trazar las Curvas Característica Operativa y de Potencia, marcando claramente las variables en los ejes y los valores numéricos de abscisa y ordenada de tres puntos al menos.

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: p ≤ 0,11 supone que cumple; H1: p > 0,11 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | p = 0,16) = 0,01 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≤ 0,11  vs  H1: p > 0,11.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condiciones**: P(rechazar | p₀ = 0,11) ≤ α = 0,05 y P(no rechazar | p₁ = 0,16) ≤ β = 0,01.
- **Plan (binomial exacto, se itera n)**: n = 739, r_c = 96. α real = 0,0499, β real = 0,0098.
- **Regla de decisión**: Tomar una muestra de n = 739. Si se encuentran r ≥ 96 casos, se rechaza H0.
- **Por aproximación normal**: n = [(Z(1-α)·√(p₀q₀) + Z(1-β)·√(p₁q₁))/(p₁ - p₀)]² → n = 749; con ese n el binomial da r_c = 98 (α real = 0,0413, β real = 0,0114). Criterio de aproximación con el n resultante: n·p = 749·0,11 = 82,39 y n·(1 − p) = 666,61 (los dos > 10); p = 0,11 > 0,005 → aproximación normal.
- **Otros planes válidos**: para cada r_c, todos los n del rango cumplen α y β (uno de los riesgos baja y el otro sube con n). La app informa el menor n; la guía a veces da el mayor del rango o usa el r_c siguiente.

| r_c | n mínimo | n máximo |
|---|---|---|
| 96 | 739 | 739 |
| 97 | 746 | 747 |
| 98 | 753 | 755 |

- **Por aproximación de Poisson** (Ecuación de García): R = p₁/p₀ = 1,4545; a = [Z(1-β) + Z(1-α)·∛R]/[2(∛R - 1)] = 15,7481; ν = 2/9·(a + √(a² + 1))² = 220,8907; c = ⌊ν/2⌋ = 110 → g.l. = 2c = 220; n = máx[χ²(α; 220)/(2p₀) ; χ²(1-β; 220)/(2p₁)] = máx[848,5051 ; 849,1164] → n = 850; r_c = c + 1 = 111. Criterio de aproximación con el n resultante: n·p = 850·0,11 = 93,5 y n·(1 − p) = 756,5 (los dos > 10); p = 0,11 > 0,005 → aproximación normal. ⚠️ Con el n resultante el criterio NO habilita Poisson: este n no es una respuesta válida (el profesor, sobre III-11c: el 855 por Poisson es incorrecto porque el criterio se aplicó con el n inicial).

**Conclusión:** Tomar una muestra de n = 739. Si se encuentran r ≥ 96 casos, se rechaza H0. (Por aproximación normal, justificada con el n resultante: n = 749 y r_c = 98.)

**Respuesta de la guía:** H0) p ≤ p0 = 0,11. n = 739 piezas y rc = 96 defectuosas (α = 0,0499; β = 0,0098); o n = 749 piezas y rc = 98 defectuosas (por aproximación normal).

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: p ≤ 0,11  vs  H1: p > 0,11  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Modelo**: binomial exacto con n = 739 y p₀ = 0,11.
- **Condición de rechazo**: r_c es el menor valor con G_b(r_c | n = 739; p₀ = 0,11) ≤ α: G_b(95) = 0,0626 > α y G_b(96) = 0,0499 ≤ α → r_c = 96 (α real = 0,0499 ≤ α = 0,05; el α real nunca puede superar al estipulado). Si r ≥ 96 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **β** = P(no rechazar H0 | p = 0,14) = F_b(95 | n = 739; p₁ = 0,14) = 0,2004.
- **Potencia** 1-β = 0,7996.
- **Con el plan por aproximación normal** (n = 749, r_c = 98): 1-β = 0,7794, β = 0,2206.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,7996 (β = 0,2004).

**Respuesta de la guía:** 1–β = 0,7996 (β = 0,2004); con los datos de la aproximación normal: 1–β = 0,7793 (β = 0,2207).

#### c) Curva característica operativa / de potencia ℹ️

*Qué pide:* Tabular β y 1-β para varios valores del parámetro y graficar la curva OC (β) y la de potencia (1-β).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- Para cada p se calcula β = P(no rechazar H0 | p) con el binomial (n = 739).

**Conclusión:** Tabla de puntos para graficar las curvas (ver abajo).

**Respuesta de la guía:** Tabla de β y 1–β en función de p1 con n = 739 y rc = 96 (β = Fb(95/739; p1)) y gráfico de las curvas.

> 📝 *Notas de la transcripción:* En c) la tabla de la guía da p1 = 0,11 – 1,948 – 2,000 – 2,052 – 2,104 con β = 0,05 – 0,50 – 0,90 – 0,50 – 0,05 y 1–β = 0,95 – 0,50 – 0,10 – 0,50 – 0,95: valores incoherentes (p1 > 1, β no monótona), aparentemente copiados de otro problema; el gráfico muestra abscisas 0,11 a 0,16.

<details><summary>Cómo lo concluye la guía</summary>

> Luego de iterar, con computadora, distintos valores de rc y n se llega a la siguiente solución óptima: n = 739 piezas y rc = 96 defectuosas.
> La hipótesis se rechaza si en las 739 piezas elegidas al azar del lote recepcionado se encuentran por lo menos 96 defectuosas, de esa forma rechazamos la partida.
> Si no se cuenta con un programa que realice la búsqueda se debe utilizar una aproximación. En este caso, según los criterios de aproximaciones, se puede utilizar la aproximación por Normal (n = 749).
> La hipótesis se rechaza si en las 749 piezas elegidas al azar del lote recepcionado se encuentran por lo menos 98 defectuosas, y de esa forma rechazamos la partida.

</details>

---

### III-13 · Problema 13 (pág. 21)

**Enunciado.** El control de recepción de una pieza seriada se realiza revisando 100 unidades, rechazando el lote si se encuentran 9 o más defectuosas. De este modo, el comprador afirma que es pequeño el riesgo del proveedor (probabilidad de que le rechacen un lote que contiene el 5% defectuoso admitido por contrato) y, el comprador, tiene en cambio un riesgo del 15% de aceptar un lote "malo".

- **a)** Indicar la hipótesis nula que se está ensayando y calcular el riesgo del proveedor.
- **b)** Calcular el porcentaje defectuoso poblacional del lote definido como malo.

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: p ≤ 0,05 supone que cumple; H1: p > 0,05 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Plan dado**: n = 100; se rechaza H0 si r ≥ 9 (H0: p ≤ 0,05, criterio optimista).
- **Riesgo del proveedor** α = P(r ≥ 9 | n = 100; p₀ = 0,05) = 0,0631 (binomial exacto).
- **LTPD / lote malo**: p₁ tal que P(aceptar | p₁) = β = 0,15 → p₁ = 0,118306.

**Conclusión:** α = 0,0631; p₁ = 0,118306.

**Respuesta de la guía:** H0) p ≤ p0 = 0,05 (hipótesis optimista); α = Gb(9/100; 0,05) = 0,0631.

#### b) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: p ≤ 0,05 supone que cumple; H1: p > 0,05 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Plan dado**: n = 100; se rechaza H0 si r ≥ 9 (H0: p ≤ 0,05, criterio optimista).
- **Riesgo del proveedor** α = P(r ≥ 9 | n = 100; p₀ = 0,05) = 0,0631 (binomial exacto).
- **LTPD / lote malo**: p₁ tal que P(aceptar | p₁) = β = 0,15 → p₁ = 0,118306.

**Conclusión:** α = 0,0631; p₁ = 0,118306.

**Respuesta de la guía:** p1 = 0,1183 (11,83%).

<details><summary>Cómo lo concluye la guía</summary>

> El riesgo del proveedor, que se debe calcular, es precisamente el valor de α, es decir, el nivel de significación del ensayo (el Error de Tipo I): α = Gb(9/100; 0,05) = 0,0631.
> Averiguando el valor de p1 que satisface la ecuación β = 0,15 = Fb(8/100; p1), se tiene que p1 = 0,1183 (o sea 11,83%).

</details>

---

### III-14 · Problema 14 (pág. 22)

**Enunciado.** Para una pieza que se produce en grandes cantidades, se estudia la posibilidad de cambiar la materia prima por otra más costosa, si es posible asegurar una disminución importante en el porcentaje de defectuosas, que actualmente llega al 14%. Si se logra disminuir dicho porcentaje al 10%, se desea una probabilidad de 0,95 de cambiar la materia prima, pero si no hubiera disminución alguna, se establece en un 0,01 dicha probabilidad.

- **a)** Indicar la hipótesis nula apropiada a esta situación, el tamaño de la muestra, la condición de rechazo y la regla de decisión.
- **b)** Calcular la probabilidad de no efectuar el cambio, cuando con él se obtiene un porcentaje defectuoso del 12% y dibujar una curva que dé probabilidades de no efectuar el cambio en función del parámetro de ensayo, marcando los valores numéricos de abscisa y ordenada de 3 puntos al menos.

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: p ≥ 0,14 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: p < 0,14 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,01 (error de tipo I); β = P(no rechazar H0 | p = 0,1) = 0,05 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≥ 0,14  vs  H1: p < 0,14.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condiciones**: P(rechazar | p₀ = 0,14) ≤ α = 0,01 y P(no rechazar | p₁ = 0,1) ≤ β = 0,05.
- **Plan (binomial exacto, se itera n)**: n = 1043, r_c = 120. α real = 0,01, β real = 0,0495.
- **Regla de decisión**: Tomar una muestra de n = 1043. Si se encuentran r ≤ 120 casos, se rechaza H0.
- **Por aproximación normal**: n = [(Z(1-α)·√(p₀q₀) + Z(1-β)·√(p₁q₁))/(p₁ - p₀)]² → n = 1058; con ese n el binomial da r_c = 121 (α real = 0,0079, β real = 0,056). Criterio de aproximación con el n resultante: n·p = 1058·0,14 = 148,12 y n·(1 − p) = 909,88 (los dos > 10); p = 0,14 > 0,005 → aproximación normal.
- **Otros planes válidos**: para cada r_c, todos los n del rango cumplen α y β (uno de los riesgos baja y el otro sube con n). La app informa el menor n; la guía a veces da el mayor del rango o usa el r_c siguiente.

| r_c | n mínimo | n máximo |
|---|---|---|
| 120 | 1043 | 1043 |
| 121 | 1051 | 1052 |
| 122 | 1059 | 1062 |

- **Por aproximación de Poisson** (Ecuación de García): R = p₀/p₁ = 1,4; a = [Z(1-α) + Z(1-β)·∛R]/[2(∛R - 1)] = 17,5519; ν = 2/9·(a + √(a² + 1))² = 274,2828; r_c = ⌈(ν-2)/2⌉ = 137 → g.l. = 2r_c + 2 = 276; n = máx[χ²(1-α; 276)/(2p₀) ; χ²(β; 276)/(2p₁)] = máx[1.191,3525 ; 1.192,6233] → n = 1193. Criterio de aproximación con el n resultante: n·p = 1193·0,14 = 167,02 y n·(1 − p) = 1025,98 (los dos > 10); p = 0,14 > 0,005 → aproximación normal. ⚠️ Con el n resultante el criterio NO habilita Poisson: este n no es una respuesta válida (el profesor, sobre III-11c: el 855 por Poisson es incorrecto porque el criterio se aplicó con el n inicial).

**Conclusión:** Tomar una muestra de n = 1043. Si se encuentran r ≤ 120 casos, se rechaza H0. (Por aproximación normal, justificada con el n resultante: n = 1058 y r_c = 121.)

**Respuesta de la guía:** (Criterio pesimista) H0) p ≥ p0 = 0,14, n = 1.043 piezas o n = 1.058 piezas (por aproximación normal); CR: Si r ≤ rc = 120 defectuosas rechazo la H0 o Si r ≤ rc = 121 defectuosas rechazo la H0 (por aproximación normal); RD: Si de una muestra de 1.043 piezas hay 120 defectuosas o menos se cambia la materia prima o Si de una muestra de 1.058 piezas hay 121 defectuosas o menos se cambia la materia prima (por aproximación normal).

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: p ≥ 0,14  vs  H1: p < 0,14  (α = 0,01).
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Modelo**: binomial exacto con n = 1043 y p₀ = 0,14.
- **Condición de rechazo**: r_c es el mayor valor con F_b(r_c | n = 1043; p₀ = 0,14) ≤ α: F_b(121) = 0,0128 > α y F_b(120) = 0,01 ≤ α → r_c = 120 (α real = 0,01 ≤ α = 0,01; el α real nunca puede superar al estipulado). Si r ≤ 120 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **β** = P(no rechazar H0 | p = 0,12) = G_b(121 | n = 1043; p₁ = 0,12) = 0,668.
- **Potencia** 1-β = 0,332.
- **Con el plan por aproximación normal** (n = 1058, r_c = 121): 1-β = 0,3058, β = 0,6942.

**Conclusión:** La probabilidad pedida es β = 0,668 (potencia 1-β = 0,332).

**Respuesta de la guía:** β = 0,6680, o β = 0,6942 (por aproximación normal). Ver procedimiento de construcción de la curva en el problema 12.

---

### III-15 · Problema 15 (pág. 22)

**Enunciado.** Una empresa forestal ha resuelto explotar un monte de eucaliptus si se puede asegurar que el porcentaje de árboles mayores a 5 metros supera el 70%. Se eligieron 30 árboles al azar y se hallaron 25 mayores de 5 metros. Se ha fijado en un 5% el riesgo de explotarlo erróneamente.

- **a)** ¿Se aconseja la explotación del monte?
- **b)** Si se eligieran 100 árboles al azar, ¿cuántos deberían superar los 5 metros para aconsejar la explotación?
- **c)** Estimar, con la muestra obtenida y con un 5% de riesgo, el porcentaje de árboles mayores a 5 metros.
- **d)** ¿Cuántos árboles deberían seleccionarse si se pretende disminuir en un 30% la relación de estimación anterior?
- **e)** ¿Cuántos árboles deberían seleccionarse si se pretende disminuir en un 50% el error de la estimación anterior?

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la proporción poblacional p: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: p ≤ 0,7  vs  H1: p > 0,7.
- **Justificación de H0**:  
• H1: p > 0,7 recoge lo que el enunciado quiere probar; H0: p ≤ 0,7 es el complemento y lleva la igualdad (el valor de referencia 0,7).  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: binomial exacto con n = 30 y p₀ = 0,7.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **4 · Condición de rechazo (CR)**: r_c es el menor valor con G_b(r_c | n = 30; p₀ = 0,7) ≤ α: G_b(25) = 0,0766 > α y G_b(26) = 0,0302 ≤ α → r_c = 26 (α real = 0,0302 ≤ α = 0,05; el α real nunca puede superar al estipulado). Si r ≥ 26 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 30 unidades y se cuenta la cantidad r de casos. Si r ≥ 26, se rechaza H0 → se puede asegurar que p > 0,7. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que p > 0,7.
- **6 · Cálculos y decisión**: r = 25 (p̂ = 0,8333) no es ≥ r_c = 26 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,0766. El profesor decide con r contra r_c (a priori); el α* «no me gusta».

**Conclusión:** Con α = 0,05, r = 25 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: p ≤ 0,7. No hay evidencia suficiente para asegurar que p > 0,7 (no rechazar H0 no la prueba).

**Respuesta de la guía:** H0) p ≤ p0 = 0,70; rc = 26 éxitos. Como se encontraron 25, no se rechaza H0: no se aconseja explotar el monte (α* = Gb(25/30; 0,70) = 0,0766 > α).

#### b) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• H1: p > 0,7 recoge lo que el enunciado quiere probar; H0: p ≤ 0,7 es el complemento y lleva la igualdad (el valor de referencia 0,7).  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≤ 0,7  vs  H1: p > 0,7.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condición de rechazo**: r_c es el menor valor con G_b(r_c | n = 100; p₀ = 0,7) ≤ α: G_b(77) = 0,0755 > α y G_b(78) = 0,0479 ≤ α → r_c = 78 (α real = 0,0479 ≤ α = 0,05; el α real nunca puede superar al estipulado). Si r ≥ 78 ⇒ se rechaza H0.

**Conclusión:** Si en la muestra de 100 se encuentran r ≥ 78, se rechaza H0.

**Respuesta de la guía:** rc = 78 árboles como mínimo.

#### c) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la proporción poblacional p con un 95% de confianza mediante un intervalo de confianza. La cátedra usa el modelo exacto (Beta / F).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El intervalo exacto usa la relación entre la Binomial y la distribución Beta (o F de Snedecor).
- **Datos**: n = 30, r = 25, p̂ = r/n = 0,8333.
- **Modelo exacto** (Beta / F, el que usa la cátedra): A = 0,6527 ; B = 0,9436.
- **Límite inferior (A)**: ν₁ = 2(n − r + 1) = 12, ν₂ = 2r = 50; F(0,975; 12; 50) = 2,2162; A = 1/[1 + (6/25)·2,2162] = 0,652788.
- **Límite superior (B)**: ν₁ = 2(r + 1) = 52, ν₂ = 2(n − r) = 10; F(0,975; 52; 10) = 3,2161; B = 1/[1 + 5/(26·3,2161)] = 0,943578.
- La estimación de p es siempre exacta (Beta / F). La aproximación normal NO se usa para estimar p: el profesor la llama «aberración»; las aproximaciones solo sirven para calcular n.

**Conclusión:** El porcentaje poblacional estará entre 65,27% y 94,36%, con un 95% de confianza: P(0,6527 ≤ p ≤ 0,9436) = 0,95 (límites redondeados hacia afuera; sin redondear: 0,652788 y 0,943578).

**Respuesta de la guía:** Entre 65,27% y 94,36% (A = 0,6527; B = 0,9436).

#### d) Tamaño de muestra ⚠️

*Qué pide:* Calcular el tamaño de muestra para reducir un 30% el error (o la relación entre límites). Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• Para el n se usa la aproximación Normal: p̂ ~ N(p; p(1-p)/n). La aproximación se justifica con el n RESULTANTE: normal si n·p > 10 y n·(1-p) > 10; Poisson si p ≤ 0,005; si se cumplen las dos o ninguna, criterio de Mermoz (n₀ = 0,23·(1-p)²/p³).
- **Relación entre límites**: R = B/A = 1,44546 → R' = R·(1 - 0,3) = 1,01182. Con la aproximación normal (p̂ + e)/(p̂ - e) = R' → e = p̂·(R' - 1)/(R' + 1) = 0,004896.
- **Fórmula** (aprox. normal): n = Z²·p̂(1-p̂)/e² + 1 = 1,96²·0,8333·0,1667/0,0049² + 1 → n = 22255.
- **Justificación de la aproximación**: Criterio de aproximación con el n resultante: n·p = 22255·0,8333 = 18545,8333 y n·(1 − p) = 3709,1667 (los dos > 10); p = 0,8333 > 0,005 → aproximación normal.

**Conclusión:** El tamaño de muestra necesario es n = 22255. Respecto de la muestra de 30: Δn = 22225.

**Respuesta de la guía:** R = 1,44546 → R = 1,01182; n ≈ 22.255 árboles (aproximación normal); n ≈ 26.909 árboles (aproximación de Poisson).

> ⚠️ **No coincide con la guía** (no aparecen: 26.909). Ver la lista de discrepancias.

#### e) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para reducir un 50% el error (o la relación entre límites). Si ya hay una muestra, la respuesta es cuántas unidades MÁS: Δn = n_nuevo - n_actual.

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• Para el n se usa la aproximación Normal: p̂ ~ N(p; p(1-p)/n). La aproximación se justifica con el n RESULTANTE: normal si n·p > 10 y n·(1-p) > 10; Poisson si p ≤ 0,005; si se cumplen las dos o ninguna, criterio de Mermoz (n₀ = 0,23·(1-p)²/p³).
- **Error buscado**: e = 0,145395·(1 - 0,5) = 0,072698.
- **Fórmula** (aprox. normal): n = Z²·p̂(1-p̂)/e² + 1 = 1,96²·0,8333·0,1667/0,0727² + 1 → n = 102.
- **Justificación de la aproximación**: Criterio de aproximación con el n resultante: n·p = 102·0,8333 = 85 y n·(1 − p) = 17 (los dos > 10); p = 0,8333 > 0,005 → aproximación normal.

**Conclusión:** El tamaño de muestra necesario es n = 102. Respecto de la muestra de 30: Δn = 72.

**Respuesta de la guía:** e = 0,145395 → 0,072698; n ≈ 102 árboles (aproximación normal).

> 📝 *Notas de la transcripción:* d) La guía da dos resultados según la aproximación (normal 22.255; Poisson 26.909), sin indicar cuál adopta.

<details><summary>Cómo lo concluye la guía</summary>

> Si de una muestra de 30 árboles elegidos al azar se encuentran 26 o más árboles mayores que 5 metros, se rechaza la hipótesis nula y se recomienda explotar el monte.
> Como la cantidad de árboles mayores a 5 metros que se encontraron en la muestra, fueron 25 árboles, no se puede rechazar la hipótesis nula. Por lo cual no se aconseja explotar el monte porque no se puede asegurar que el porcentaje de árboles mayores a 5 metros sea superior al 70%.
> También se puede utilizar el procedimiento "A posteriori": α* = Gb(25/30; 0,70) = 0,0766, y como el α* es mayor que el α estipulado no se puede rechazar la hipótesis nula, arribando a la misma conclusión.
> El valor crítico que satisface la ecuación es: rc = 78 éxitos, se deberían encontrar en la muestra de 100 por lo menos 78 árboles superiores a 5 metros.
> Se concluye que el porcentaje de árboles con longitud superior a 5 metros del monte estará comprendido entre 65,27% y 94,36%, afirmándolo con un 95% de confianza, o sea: P(65,27% ≤ p ≤ 94,36%) = 0,95.
> Si se quiere reducir la relación entre límites, se debe aumentar el tamaño de la muestra; se deben usar aproximaciones ya que no hay un procedimiento de cálculo para el uso de la distribución binomial.
> Para reducir el error muestral en un 50% no queda otra alternativa que usar la aproximación normal ya que la aproximación de Poisson trabaja solamente con la relación entre límites y no con el error muestral.

</details>

---

### III-16 · Problema 16 (pág. 23)

**Enunciado.** En una empresa productora de artículos de consumo masivo se ha lanzado una campaña publicitaria sobre un jabón en polvo cuya penetración en el mercado era del 12%. Se desea ahora realizar una encuesta para comprobar si la campaña ha sido efectiva, en cuyo caso se realizará una campaña similar sobre otro de los productos. A tal efecto, si no se ha conseguido el resultado deseado, se establece una probabilidad de 0,01 de tomar una decisión errónea, y en cambio, si hay un aumento en la penetración de 3 puntos se considera un resultado razonablemente bueno, en cuyo caso la probabilidad de tomar una decisión equivocada se establece en 0,10.

- **a)** Indicar la hipótesis nula apropiada a esta situación, la condición de rechazo y la regla de decisión.
- **b)** Calcular la probabilidad de efectuar otra campaña cuando con ésta se ha obtenido un aumento de 2 puntos.
- **c)** ¿Qué tamaño de muestra se debería tomar si se pretende que la probabilidad anterior valga 0,90? y ¿cuál sería en este caso la regla de decisión?
- **d)** Dibujar la curva que representa dichas probabilidades en función de la penetración obtenida en el mercado, teniendo en cuenta ambos tamaños de muestra.

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ⚠️

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: p ≤ 0,12 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: p > 0,12 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,01 (error de tipo I); β = P(no rechazar H0 | p = 0,15) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≤ 0,12  vs  H1: p > 0,12.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condiciones**: P(rechazar | p₀ = 0,12) ≤ α = 0,01 y P(no rechazar | p₁ = 0,15) ≤ β = 0,1.
- **Plan (binomial exacto, se itera n)**: n = 1675, r_c = 233. α real = 0,01, β real = 0,0988.
- **Regla de decisión**: Tomar una muestra de n = 1675. Si se encuentran r ≥ 233 casos, se rechaza H0.
- **Por aproximación normal**: n = [(Z(1-α)·√(p₀q₀) + Z(1-β)·√(p₁q₁))/(p₁ - p₀)]² → n = 1637; con ese n el binomial da r_c = 229 (α real = 0,0083, β real = 0,1183). Criterio de aproximación con el n resultante: n·p = 1637·0,12 = 196,44 y n·(1 − p) = 1440,56 (los dos > 10); p = 0,12 > 0,005 → aproximación normal.
- **Otros planes válidos**: para cada r_c, todos los n del rango cumplen α y β (uno de los riesgos baja y el otro sube con n). La app informa el menor n; la guía a veces da el mayor del rango o usa el r_c siguiente.

| r_c | n mínimo | n máximo |
|---|---|---|
| 233 | 1675 | 1675 |
| 234 | 1682 | 1682 |
| 235 | 1689 | 1690 |

- **Por aproximación de Poisson** (Ecuación de García): R = p₁/p₀ = 1,25; a = [Z(1-β) + Z(1-α)·∛R]/[2(∛R - 1)] = 24,5251; ν = 2/9·(a + √(a² + 1))² = 535,0959; c = ⌊ν/2⌋ = 267 → g.l. = 2c = 534; n = máx[χ²(α; 534)/(2p₀) ; χ²(1-β; 534)/(2p₁)] = máx[1.920,5296 ; 1.920,9544] → n = 1921; r_c = c + 1 = 268. Criterio de aproximación con el n resultante: n·p = 1921·0,12 = 230,52 y n·(1 − p) = 1690,48 (los dos > 10); p = 0,12 > 0,005 → aproximación normal. ⚠️ Con el n resultante el criterio NO habilita Poisson: este n no es una respuesta válida (el profesor, sobre III-11c: el 855 por Poisson es incorrecto porque el criterio se aplicó con el n inicial).

**Conclusión:** Tomar una muestra de n = 1675. Si se encuentran r ≥ 233 casos, se rechaza H0. (Por aproximación normal, justificada con el n resultante: n = 1637 y r_c = 229.)

**Respuesta de la guía:** (Criterio pesimista) H0) p ≤ p0 = 0,12; CR: Si r ≥ rc = 233 éxitos se rechaza la H0 o r ≥ rc = 229 éxitos (por aproximación normal); RD: Si de una muestra de 1.675 encuestados por lo menos 233 se encuentran interesados, se concluye que la campaña ha sido efectiva o Si de una muestra de 1.637 encuestados por lo menos 228 se encuentran interesados se concluye que la campaña ha sido efectiva (por aproximación normal).

> ⚠️ **No coincide con la guía** (no aparecen: 228). Ver la lista de discrepancias.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: p ≤ 0,12  vs  H1: p > 0,12  (α = 0,01).
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Modelo**: binomial exacto con n = 1675 y p₀ = 0,12.
- **Condición de rechazo**: r_c es el menor valor con G_b(r_c | n = 1675; p₀ = 0,12) ≤ α: G_b(232) = 0,0121 > α y G_b(233) = 0,01 ≤ α → r_c = 233 (α real = 0,01 ≤ α = 0,01; el α real nunca puede superar al estipulado). Si r ≥ 233 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **β** = P(no rechazar H0 | p = 0,14) = F_b(232 | n = 1675; p₁ = 0,14) = 0,4473.
- **Potencia** 1-β = 0,5527.
- **Con el plan por aproximación normal** (n = 1637, r_c = 229): 1-β = 0,5159, β = 0,4841.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,5527 (β = 0,4473).

**Respuesta de la guía:** 1–β = 0,5527, o 1–β = 0,5443 (por aproximación normal).

> ≈ Coincide solo aproximadamente (0,5443): La guía calcula la potencia con el r_c = 228 de su RD (0,5443); con el r_c conservador 229 la aproximación normal da 0,5159 y el plan exacto 0,5527.

#### c) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: p ≤ 0,12 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: p > 0,12 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,01 (error de tipo I); β = P(no rechazar H0 | p = 0,14) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≤ 0,12  vs  H1: p > 0,12.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condiciones**: P(rechazar | p₀ = 0,12) ≤ α = 0,01 y P(no rechazar | p₁ = 0,14) ≤ β = 0,1.
- **Plan (binomial exacto, se itera n)**: n = 3660, r_c = 486. α real = 0,01, β real = 0,0994.
- **Regla de decisión**: Tomar una muestra de n = 3660. Si se encuentran r ≥ 486 casos, se rechaza H0.
- **Plan «más próximo a las premisas»** (el que suele informar la guía): entre los planes que cumplen α y β con r_c = 486 o 487, el de menor |α_real - α| + |β_real - β| es n = 3667, r_c = 487 (α real = 0,00983, β real = 0,09974). Los dos planes son válidos: el de n mínimo es el más barato.
- **Por aproximación normal**: n = [(Z(1-α)·√(p₀q₀) + Z(1-β)·√(p₁q₁))/(p₁ - p₀)]² → n = 3604; con ese n el binomial da r_c = 479 (α real = 0,0099, β real = 0,1048). Criterio de aproximación con el n resultante: n·p = 3604·0,12 = 432,48 y n·(1 − p) = 3171,52 (los dos > 10); p = 0,12 > 0,005 → aproximación normal.
- **Otros planes válidos**: para cada r_c, todos los n del rango cumplen α y β (uno de los riesgos baja y el otro sube con n). La app informa el menor n; la guía a veces da el mayor del rango o usa el r_c siguiente.

| r_c | n mínimo | n máximo |
|---|---|---|
| 486 | 3660 | 3660 |
| 487 | 3667 | 3668 |
| 488 | 3675 | 3675 |

- **Por aproximación de Poisson** (Ecuación de García): R = p₁/p₀ = 1,1667; a = [Z(1-β) + Z(1-α)·∛R]/[2(∛R - 1)] = 35,3765; ν = 2/9·(a + √(a² + 1))² = 1.112,8828; c = ⌊ν/2⌋ = 556 → g.l. = 2c = 1112; n = máx[χ²(α; 1112)/(2p₀) ; χ²(1-β; 1112)/(2p₁)] = máx[4.188,5022 ; 4.188,7469] → n = 4189; r_c = c + 1 = 557. Criterio de aproximación con el n resultante: n·p = 4189·0,12 = 502,68 y n·(1 − p) = 3686,32 (los dos > 10); p = 0,12 > 0,005 → aproximación normal. ⚠️ Con el n resultante el criterio NO habilita Poisson: este n no es una respuesta válida (el profesor, sobre III-11c: el 855 por Poisson es incorrecto porque el criterio se aplicó con el n inicial).

**Conclusión:** Tomar una muestra de n = 3660. Si se encuentran r ≥ 486 casos, se rechaza H0. (Plan más próximo a las premisas: n = 3667 y r_c = 487.) (Por aproximación normal, justificada con el n resultante: n = 3604 y r_c = 479.)

**Respuesta de la guía:** n = 3.667, RD: Si de una muestra de 3.667 encuestados por lo menos 487 se encuentran interesados, se concluye que la campaña ha sido efectiva o Si de una muestra de 3.604 encuestados por lo menos 479 se encuentran interesados se concluye que la campaña ha sido efectiva (por aproximación normal).

#### d) Curva característica operativa / de potencia ℹ️

*Qué pide:* Tabular β y 1-β para varios valores del parámetro y graficar la curva OC (β) y la de potencia (1-β).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- Para cada p se calcula β = P(no rechazar H0 | p) con el binomial (n = 3660).

**Conclusión:** Tabla de puntos para graficar las curvas (ver abajo).

**Respuesta de la guía:** Ver procedimiento de construcción de la curva en el problema 12.

> 📝 *Notas de la transcripción:* a) Inconsistencia interna: la CR por aproximación normal da rc = 229 pero la RD correspondiente dice 'por lo menos 228'.

---

### III-17 · Problema 17 (pág. 24)

**Enunciado.** En un proceso de mecanizado de precisión de ejes de bronce, el diámetro es variable con distribución normal de media 10 mm y desvío estándar 0,046 mm. La tolerancia de esta pieza es 10±0,08 mm por lo que se tiene un 4,1% de unidades en bajo-medida (defectuosas) pues la P(x ≤ 9,92) = φ(−1,74) = 0,041. Las unidades en sobremedida no se consideran defectuosas pues se vuelven a tornear. Se estima que, utilizando una nueva aleación, más costosa, se puede disminuir dicho porcentaje siendo el equilibrio económico para un 2,5%. Se desea no más de 0,10 la probabilidad de cambiar de aleación si el porcentaje no se modifica.

*Establecer la hipótesis nula apropiada, el tamaño de la muestra y la regla de decisión.*

*Tema detectado por la app: Proporción de 1 población (p).*

#### Resolución (Diseñar el ensayo (H0, n, valor crítico, regla de decisión)) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: p ≥ 0,041 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: p < 0,041 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I); β = P(no rechazar H0 | p = 0,025) = 0,5 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≥ 0,041  vs  H1: p < 0,041.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condiciones**: P(rechazar | p₀ = 0,041) ≤ α = 0,1 y P(no rechazar | p₁ = 0,025) ≤ β = 0,5.
- **Plan (binomial exacto, se itera n)**: n = 225, r_c = 5. α real = 0,0979, β real = 0,4937.
- **Regla de decisión**: Tomar una muestra de n = 225. Si se encuentran r ≤ 5 casos, se rechaza H0.
- **Plan «más próximo a las premisas»** (el que suele informar la guía): entre los planes que cumplen α y β con r_c = 5 o 6, el de menor |α_real - α| + |β_real - β| es n = 226, r_c = 5 (α real = 0,09572, β real = 0,49799). Los dos planes son válidos: el de n mínimo es el más barato.
- **Por aproximación normal**: n = [(Z(1-α)·√(p₀q₀) + Z(1-β)·√(p₁q₁))/(p₁ - p₀)]² → n = 253; con ese n el binomial da r_c = 5 (α real = 0,0508, β real = 0,6076). Criterio de aproximación con el n resultante: n·p = 253·0,041 = 10,373 y n·(1 − p) = 242,627 (los dos > 10); p = 0,041 > 0,005 → aproximación normal.
- **Otros planes válidos**: para cada r_c, todos los n del rango cumplen α y β (uno de los riesgos baja y el otro sube con n). La app informa el menor n; la guía a veces da el mayor del rango o usa el r_c siguiente.

| r_c | n mínimo | n máximo |
|---|---|---|
| 5 | 225 | 226 |
| 6 | 255 | 266 |
| 7 | 285 | 306 |

- **Por aproximación de Poisson** (Ecuación de García): R = p₀/p₁ = 1,64; a = [Z(1-α) + Z(1-β)·∛R]/[2(∛R - 1)] = 3,5743; ν = 2/9·(a + √(a² + 1))² = 11,7963; r_c = ⌈(ν-2)/2⌉ = 5 → g.l. = 2r_c + 2 = 12; n = máx[χ²(1-α; 12)/(2p₀) ; χ²(β; 12)/(2p₁)] = máx[226,2116 ; 226,8064] → n = 227. Criterio de aproximación con el n resultante: n·p = 227·0,041 = 9,307 y n·(1 − p) = 217,693 (no son los dos > 10); p = 0,041 > 0,005 → no se cumple ninguna, así que decide el criterio de Mermoz: n₀ = 0,23·(1 − p)²/p³ = 3069,12; n = 227 ≤ n₀ → aproximación de Poisson.

**Conclusión:** Tomar una muestra de n = 225. Si se encuentran r ≤ 5 casos, se rechaza H0. (Plan más próximo a las premisas: n = 226 y r_c = 5.) (Por aproximación normal, justificada con el n resultante: n = 253 y r_c = 5.) (Por aproximación de Poisson, justificada con el n resultante: n = 227 y r_c = 5.)

**Respuesta de la guía:** (Criterio pesimista) H0) p ≥ p0 = 0,041; n = 226 piezas o n = 253 piezas (por aproximación Normal), debería ser más apropiada la aproximación de Poisson que da n = 227; RD: Si en una muestra de 226 piezas se encuentran 5 o menos defectuosas, se rechaza la hipótesis y se adopta la nueva aleación o RD: Si en una muestra de 253 piezas se encuentran 5 o menos defectuosas, se rechaza la hipótesis y se adopta la nueva aleación (por aproximación Normal) o RD: Si en una muestra de 227 piezas se encuentran 5 o menos defectuosas, se rechaza la hipótesis y se adopta la nueva aleación (por aproximación de Poisson).

> 📝 *Notas de la transcripción:* El enunciado no fija explícitamente β para p1 = 2,5% (con n = 226, rc = 5 resulta 1–β ≈ 0,50, o sea el 'equilibrio económico' se interpreta como β = 0,50).

---

### III-18 · Problema 18 (pág. 24)

**Enunciado.** La fórmula del látex utilizada en diversas aplicaciones es un secreto industrial de cada fabricante. En una empresa se fabrica con el látex un determinado artículo. En el proceso de fabricación se tiene un porcentaje de defectuosos del 6%, pero se está considerando cambiar la formulación actual por otra más costosa, con la esperanza de disminuir el porcentaje de defectuosos. Si este porcentaje bajara al 4%, se desearía una probabilidad de 0,90 de cambiar, pero si no bajara, la probabilidad de cambio debe valer 0,01.

- **a)** Indicar la hipótesis nula apropiada, el tamaño de la muestra a tomar y el valor crítico.
- **b)** Calcular la probabilidad de adoptar la nueva fórmula si con ella se obtiene un 5% de unidades defectuosas y dibujar una curva que dé probabilidades de adoptar la nueva fórmula en función del parámetro de ensayo, marcando claramente los valores numéricos de abscisa y ordenada de 3 puntos al menos.

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: p ≥ 0,06 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: p < 0,06 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,01 (error de tipo I); β = P(no rechazar H0 | p = 0,04) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≥ 0,06  vs  H1: p < 0,06.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condiciones**: P(rechazar | p₀ = 0,06) ≤ α = 0,01 y P(no rechazar | p₁ = 0,04) ≤ β = 0,1.
- **Plan (binomial exacto, se itera n)**: n = 1561, r_c = 72. α real = 0,01, β real = 0,099.
- **Regla de decisión**: Tomar una muestra de n = 1561. Si se encuentran r ≤ 72 casos, se rechaza H0.
- **Plan «más próximo a las premisas»** (el que suele informar la guía): entre los planes que cumplen α y β con r_c = 72 o 73, el de menor |α_real - α| + |β_real - β| es n = 1562, r_c = 72 (α real = 0,00982, β real = 0,09992). Los dos planes son válidos: el de n mínimo es el más barato.
- **Por aproximación normal**: n = [(Z(1-α)·√(p₀q₀) + Z(1-β)·√(p₁q₁))/(p₁ - p₀)]² → n = 1615; con ese n el binomial da r_c = 74 (α real = 0,0077, β real = 0,1062). Criterio de aproximación con el n resultante: n·p = 1615·0,06 = 96,9 y n·(1 − p) = 1518,1 (los dos > 10); p = 0,06 > 0,005 → aproximación normal.
- **Otros planes válidos**: para cada r_c, todos los n del rango cumplen α y β (uno de los riesgos baja y el otro sube con n). La app informa el menor n; la guía a veces da el mayor del rango o usa el r_c siguiente.

| r_c | n mínimo | n máximo |
|---|---|---|
| 72 | 1561 | 1562 |
| 73 | 1580 | 1585 |
| 74 | 1599 | 1608 |

- **Por aproximación de Poisson** (Ecuación de García): R = p₀/p₁ = 1,5; a = [Z(1-α) + Z(1-β)·∛R]/[2(∛R - 1)] = 13,1064; ν = 2/9·(a + √(a² + 1))² = 153,1348; r_c = ⌈(ν-2)/2⌉ = 76 → g.l. = 2r_c + 2 = 154; n = máx[χ²(1-α; 154)/(2p₀) ; χ²(β; 154)/(2p₁)] = máx[1.647,8483 ; 1.649,7558] → n = 1650. Criterio de aproximación con el n resultante: n·p = 1650·0,06 = 99 y n·(1 − p) = 1551 (los dos > 10); p = 0,06 > 0,005 → aproximación normal. ⚠️ Con el n resultante el criterio NO habilita Poisson: este n no es una respuesta válida (el profesor, sobre III-11c: el 855 por Poisson es incorrecto porque el criterio se aplicó con el n inicial).

**Conclusión:** Tomar una muestra de n = 1561. Si se encuentran r ≤ 72 casos, se rechaza H0. (Plan más próximo a las premisas: n = 1562 y r_c = 72.) (Por aproximación normal, justificada con el n resultante: n = 1615 y r_c = 74.)

**Respuesta de la guía:** (Criterio pesimista) H0) p ≥ p0 = 0,06; n = 1.585 unidades o n = 1.615 unidades (por aproximación normal); rc = 73 o menos defectuosos o 74 o menos defectuosos (por aproximación normal).

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: p ≥ 0,06  vs  H1: p < 0,06  (α = 0,01).
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Modelo**: binomial exacto con n = 1561 y p₀ = 0,06.
- **Condición de rechazo**: r_c es el mayor valor con F_b(r_c | n = 1561; p₀ = 0,06) ≤ α: F_b(73) = 0,0135 > α y F_b(72) = 0,01 ≤ α → r_c = 72 (α real = 0,01 ≤ α = 0,01; el α real nunca puede superar al estipulado). Si r ≤ 72 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **β** = P(no rechazar H0 | p = 0,05) = G_b(73 | n = 1561; p₁ = 0,05) = 0,7371.
- **Potencia** 1-β = 0,2629.
- **Con el plan por aproximación normal** (n = 1615, r_c = 74): 1-β = 0,2403, β = 0,7597.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,2629 (β = 0,7371).

**Respuesta de la guía:** 1–β = 0,2569 o 1–β = 0,2403 (por aproximación Normal). Ver procedimiento de construcción de la curva en el problema 12.

> ≈ Coincide solo aproximadamente (0,2569): La guía usa su plan 1.585 / 73, que cumple α y β pero no es el de n mínimo (1.561 / 72) ni el más próximo a las premisas (1.562 / 72): ninguna regla lo reproduce.

---

### III-19 · Problema 19 (pág. 24)

**Enunciado.** Una persona denunció que en un casino privado había una ruleta adulterada pues había observado que el cero se producía con frecuencia excesiva. El juez solicitó entonces la asesoría de un consultor estadístico para que elevara el informe correspondiente. El consultor registró datos de 1.000 bolas en las cuales el cero se presentó 42 veces.

- **a)** ¿Se considera que la denuncia tiene fundamento estadístico?
- **b)** Si el cero tuviera una probabilidad de 0,05, ¿cuál sería con ese tamaño de muestra la probabilidad de detectar la anomalía? (Nota: En una ruleta equilibrada y convencional, la probabilidad de cero es 1/37).

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la proporción poblacional p: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: p ≤ 1/37  vs  H1: p > 1/37.
- **Justificación de H0**:  
• H1: p > 1/37 recoge lo que el enunciado quiere probar; H0: p ≤ 1/37 es el complemento y lleva la igualdad (el valor de referencia 1/37).  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: binomial exacto con n = 1000 y p₀ = 1/37.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **4 · Condición de rechazo (CR)**: r_c es el menor valor con G_b(r_c | n = 1000; p₀ = 1/37) ≤ α: G_b(36) = 0,054 > α y G_b(37) = 0,0372 ≤ α → r_c = 37 (α real = 0,0372 ≤ α = 0,05; el α real nunca puede superar al estipulado). Si r ≥ 37 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 1000 unidades y se cuenta la cantidad r de casos. Si r ≥ 37, se rechaza H0 → se puede asegurar que p > 1/37. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que p > 1/37.
- **6 · Cálculos y decisión**: r = 42 (p̂ = 0,042) ≥ r_c = 37 → se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,004. El profesor decide con r contra r_c (a priori); el α* «no me gusta».

**Conclusión:** Con α = 0,05, r = 42 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: p ≤ 1/37. Se puede asegurar que p > 1/37.

**Respuesta de la guía:** Si, se puede afirmar que el cero se produce con frecuencia excesiva, o sea que la denuncia tiene fundamento estadístico.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: p ≤ 1/37  vs  H1: p > 1/37  (α = 0,05).
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Modelo**: binomial exacto con n = 1000 y p₀ = 1/37.
- **Condición de rechazo**: r_c es el menor valor con G_b(r_c | n = 1000; p₀ = 1/37) ≤ α: G_b(36) = 0,054 > α y G_b(37) = 0,0372 ≤ α → r_c = 37 (α real = 0,0372 ≤ α = 0,05; el α real nunca puede superar al estipulado). Si r ≥ 37 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **β** = P(no rechazar H0 | p = 0,05) = F_b(36 | n = 1000; p₁ = 0,05) = 0,0212.
- **Potencia** 1-β = 0,9788.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,9788 (β = 0,0212).

**Respuesta de la guía:** 1–β = 0,9789.

> 📝 *Notas de la transcripción:* El enunciado no indica el riesgo α; la respuesta es consistente con α = 0,05 (rc = 37).

---

### III-20 · Problema 20 (pág. 24)

**Enunciado.** Para el plan de muestreo: n = 10 y rc = 1.

*Calcular el AQL y LTPD para riesgos de proveedor (α) y consumidor (β) 5% y 10% respectivamente.*

*Tema detectado por la app: Proporción de 1 población (p).*

#### Resolución (Diseñar el ensayo (H0, n, valor crítico, regla de decisión)) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: p ≤ p₀ supone que cumple; H1: p > p₀ es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Plan dado**: n = 10; se rechaza H0 si r ≥ 1.
- **AQL**: p₀ tal que P(rechazar | p₀) = α = 0,05 → AQL = p₀ = 0,005116.
- **LTPD / lote malo**: p₁ tal que P(aceptar | p₁) = β = 0,1 → p₁ = 0,205672.

**Conclusión:** AQL = 0,005116; p₁ = 0,205672.

**Respuesta de la guía:** AQL = p0 = 0,005116 y LTPD = p1 = 0,2057.

---

### III-21 · Problema 21 (pág. 24)

**Enunciado.** De un proceso productivo de horneada de piezas para tratamiento térmico se extrae una muestra de n unidades. La horneada se rechaza si en la muestra se encuentra como mínimo dos piezas defectuosas:

- **a)** ¿Qué valor debe tener n para que la probabilidad de aceptación (de una horneada dónde el 1% de defectuosas es aceptable) sea mayor a 0,95?
- **b)** ¿Cuál es la probabilidad de aceptar (con ese plan de muestreo) un lote que contenga el 11% de defectuosas?

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra (completá el error e o la reducción pedida).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• Para el n se usa la aproximación Normal: p̂ ~ N(p; p(1-p)/n). La aproximación se justifica con el n RESULTANTE: normal si n·p > 10 y n·(1-p) > 10; Poisson si p ≤ 0,005; si se cumplen las dos o ninguna, criterio de Mermoz (n₀ = 0,23·(1-p)²/p³).
- **Plan**: se rechaza si r ≥ 2. P(aceptar | p₀ = 0,01) = P(r ≤ 1) decrece con n: el mayor n con P ≥ 0,95 es n = 35 (P = 0,9521).
- **Por aproximación de Poisson** (como la guía, con la tabla de Poisson: m al 0,1): el mayor m con P(r ≤ 1 | m) ≥ 0,95 en la tabla es m = 0,3 → n = m/p₀ = 30. Criterio de aproximación con el n resultante: n·p = 30·0,01 = 0,3 y n·(1 − p) = 29,7 (no son los dos > 10); p = 0,01 > 0,005 → no se cumple ninguna, así que decide el criterio de Mermoz: n₀ = 0,23·(1 − p)²/p³ = 225423; n = 30 ≤ n₀ → aproximación de Poisson.

**Conclusión:** n = 35: con n mayor la probabilidad de aceptar un lote con p = 0,01 baja de 0,95. (Por aproximación de Poisson con la tabla: n = 30.)

**Respuesta de la guía:** n = 35 piezas o n = 30 piezas (por aproximación de Poisson).

#### b) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: p ≤ 0,01 supone que cumple; H1: p > 0,01 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Plan dado**: n = 35; se rechaza H0 si r ≥ 2 (H0: p ≤ 0,01, criterio optimista).
- **Riesgo del proveedor** α = P(r ≥ 2 | n = 35; p₀ = 0,01) = 0,0479 (binomial exacto).
- **Con p₁ = 0,11**: β = P(no rechazar) = 0,0902; potencia = 0,9098.
- **Por aproximación de Poisson** (n = 30): m = n·p₁ = 3,3; β = P(r ≤ 1 | m) = 0,1586.

**Conclusión:** α = 0,0479; β = 0,0902; Poisson: β = 0,1586.

**Respuesta de la guía:** β = 0,0902 o β = 0,1586 (por aproximación de Poisson).

---

### III-22 · Problema 22 (pág. 25)

**Enunciado.** Describir el plan de muestreo, de un proceso productivo, que mejor satisfaga las siguientes condiciones:

- **a)** AQL = p0 = 1,5% y LTPD = p1 = 4% para un riesgo del consumidor (β) y proveedor (α) del 10% y 5% respectivamente.
- **b)** AQL = p0 = 2% y LTPD = p1 = 5% para un riesgo del consumidor (β) y proveedor (α) del 10% y 15% respectivamente.

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: p ≤ 0,015 supone que cumple; H1: p > 0,015 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | p = 0,04) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≤ 0,015  vs  H1: p > 0,015.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condiciones**: P(rechazar | p₀ = 0,015) ≤ α = 0,05 y P(no rechazar | p₁ = 0,04) ≤ β = 0,1.
- **Plan (binomial exacto, se itera n)**: n = 353, r_c = 10. α real = 0,0426, β real = 0,0992.
- **Regla de decisión**: Tomar una muestra de n = 353. Si se encuentran r ≥ 10 casos, se rechaza H0.
- **Por aproximación normal**: n = [(Z(1-α)·√(p₀q₀) + Z(1-β)·√(p₁q₁))/(p₁ - p₀)]² → n = 326; con ese n el binomial da r_c = 10 (α real = 0,027, β real = 0,1578). Criterio de aproximación con el n resultante: n·p = 326·0,015 = 4,89 y n·(1 − p) = 321,11 (no son los dos > 10); p = 0,015 > 0,005 → no se cumple ninguna, así que decide el criterio de Mermoz: n₀ = 0,23·(1 − p)²/p³ = 66119,04; n = 326 ≤ n₀ → aproximación de Poisson. ⚠️ Con el n resultante el criterio NO habilita la normal: no usar este n como respuesta.
- **Otros planes válidos**: para cada r_c, todos los n del rango cumplen α y β (uno de los riesgos baja y el otro sube con n). La app informa el menor n; la guía a veces da el mayor del rango o usa el r_c siguiente.

| r_c | n mínimo | n máximo |
|---|---|---|
| 10 | 353 | 363 |
| 11 | 383 | 413 |
| 12 | 413 | 463 |

- **Por aproximación de Poisson** (Ecuación de García): R = p₁/p₀ = 2,6667; a = [Z(1-β) + Z(1-α)·∛R]/[2(∛R - 1)] = 4,606; ν = 2/9·(a + √(a² + 1))² = 19,3001; c = ⌊ν/2⌋ = 9 → g.l. = 2c = 18; n = máx[χ²(α; 18)/(2p₀) ; χ²(1-β; 18)/(2p₁)] = máx[313,0152 ; 324,8678] → n = 325; r_c = c + 1 = 10. Criterio de aproximación con el n resultante: n·p = 325·0,015 = 4,875 y n·(1 − p) = 320,125 (no son los dos > 10); p = 0,015 > 0,005 → no se cumple ninguna, así que decide el criterio de Mermoz: n₀ = 0,23·(1 − p)²/p³ = 66119,04; n = 325 ≤ n₀ → aproximación de Poisson.

**Conclusión:** Tomar una muestra de n = 353. Si se encuentran r ≥ 10 casos, se rechaza H0. (Por aproximación de Poisson, justificada con el n resultante: n = 325 y r_c = 10.)

**Respuesta de la guía:** n = 353 y rc = 10 o n = 325 y rc = 10 (por aproximación Poisson).

#### b) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: p ≤ 0,02 supone que cumple; H1: p > 0,02 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,15 (error de tipo I); β = P(no rechazar H0 | p = 0,05) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≤ 0,02  vs  H1: p > 0,02.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condiciones**: P(rechazar | p₀ = 0,02) ≤ α = 0,15 y P(no rechazar | p₁ = 0,05) ≤ β = 0,1.
- **Plan (binomial exacto, se itera n)**: n = 209, r_c = 7. α real = 0,1282, β real = 0,0983.
- **Regla de decisión**: Tomar una muestra de n = 209. Si se encuentran r ≥ 7 casos, se rechaza H0.
- **Plan «más próximo a las premisas»** (el que suele informar la guía): entre los planes que cumplen α y β con r_c = 7 o 8, el de menor |α_real - α| + |β_real - β| es n = 218, r_c = 7 (α real = 0,14941, β real = 0,07751). Los dos planes son válidos: el de n mínimo es el más barato.
- **Por aproximación normal**: n = [(Z(1-α)·√(p₀q₀) + Z(1-β)·√(p₁q₁))/(p₁ - p₀)]² → n = 201; con ese n el binomial da r_c = 7 (α real = 0,1107, β real = 0,1207). Criterio de aproximación con el n resultante: n·p = 201·0,02 = 4,02 y n·(1 − p) = 196,98 (no son los dos > 10); p = 0,02 > 0,005 → no se cumple ninguna, así que decide el criterio de Mermoz: n₀ = 0,23·(1 − p)²/p³ = 27611,5; n = 201 ≤ n₀ → aproximación de Poisson. ⚠️ Con el n resultante el criterio NO habilita la normal: no usar este n como respuesta.
- **Otros planes válidos**: para cada r_c, todos los n del rango cumplen α y β (uno de los riesgos baja y el otro sube con n). La app informa el menor n; la guía a veces da el mayor del rango o usa el r_c siguiente.

| r_c | n mínimo | n máximo |
|---|---|---|
| 7 | 209 | 218 |
| 8 | 234 | 258 |
| 9 | 258 | 299 |

- **Por aproximación de Poisson** (Ecuación de García): R = p₁/p₀ = 2,5; a = [Z(1-β) + Z(1-α)·∛R]/[2(∛R - 1)] = 3,7628; ν = 2/9·(a + √(a² + 1))² = 13,0261; c = ⌊ν/2⌋ = 6 → g.l. = 2c = 12; n = máx[χ²(α; 12)/(2p₀) ; χ²(1-β; 12)/(2p₁)] = máx[177,8459 ; 185,4935] → n = 186; r_c = c + 1 = 7. Criterio de aproximación con el n resultante: n·p = 186·0,02 = 3,72 y n·(1 − p) = 182,28 (no son los dos > 10); p = 0,02 > 0,005 → no se cumple ninguna, así que decide el criterio de Mermoz: n₀ = 0,23·(1 − p)²/p³ = 27611,5; n = 186 ≤ n₀ → aproximación de Poisson.

**Conclusión:** Tomar una muestra de n = 209. Si se encuentran r ≥ 7 casos, se rechaza H0. (Plan más próximo a las premisas: n = 218 y r_c = 7.) (Por aproximación de Poisson, justificada con el n resultante: n = 186 y r_c = 7.)

**Respuesta de la guía:** n = 218 y rc = 7 o n = 186 y rc = 7 (por aproximación Poisson).

---

### III-23 · Problema 23 (pág. 25)

**Enunciado.** Se supone que el porcentaje de defectuosos de un proceso de manufactura es del 4%. El proceso se vigila diariamente mediante la toma de muestras de n = 80 unidades. Éste se detiene cada vez que se encuentran cinco o más unidades defectuosas en la muestra.

*Si el verdadero porcentaje de unidades defectuosas es de 5,5%, ¿cuál es la probabilidad de detener el proceso?*

*Tema detectado por la app: Proporción de 1 población (p).*

#### Resolución (Probabilidad de error / potencia (β, 1-β)) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Plan dado**: n = 80; se rechaza si r ≥ 5.
- **Binomial** con p = 0,055: P(rechazar) = P(r ≥ 5) = 0,451; P(no rechazar / aceptar) = 0,549.
- **Potencia** 1-β = 0,451.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,451 (β = 0,549).

**Respuesta de la guía:** 1–β = 0,4510.

---

### III-24 · Problema 24 (pág. 25)

**Enunciado.** Se supone que la calidad de un lote muy grande es del 5% de unidades defectuosas como máximo. Un plan de muestreo requiere una muestra de 40 unidades y un número de aceptación de menor o igual a 2 unidades defectuosas.

- **a)** ¿Cuál es la probabilidad de que el lote sea aceptado?
- **b)** Si la calidad del lote fuera del 6,25% de unidades defectuosas, ¿cuál es la probabilidad de que el lote sea aceptado?

*Tema detectado por la app: Proporción de 1 población (p).*

#### a) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Plan dado**: n = 40; se rechaza si r ≥ 3.
- **Binomial** con p = 0,05: P(rechazar) = P(r ≥ 3) = 0,3233; P(no rechazar / aceptar) = 0,6767.
- **Potencia** 1-β = 0,3233.

**Conclusión:** La probabilidad pedida es β = 0,6767 (potencia 1-β = 0,3233).

**Respuesta de la guía:** 1–α = 0,6767.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **Plan dado**: n = 40; se rechaza si r ≥ 3.
- **Binomial** con p = 0,0625: P(rechazar) = P(r ≥ 3) = 0,4603; P(no rechazar / aceptar) = 0,5397.
- **Potencia** 1-β = 0,4603.

**Conclusión:** La probabilidad pedida es β = 0,5397 (potencia 1-β = 0,4603).

**Respuesta de la guía:** β = 0,5397.

---

### III-25 · Problema 25 (pág. 25)

**Enunciado.** En la década del '70 se descubrió que la sustancia cancerígena (NDMA) se formaba durante el secado de la malta verde usada en la fabricación de cerveza; se sabe que la presencia de esta sustancia era del 5% en las observaciones. En la década del '80 se desarrolla un nuevo proceso de secado inoculando un inhibidor biogenético para minimizar la formación de NDMA. Se obtuvo una muestra de 160 observaciones y se detecta una presencia del 1,25% de NDMA.

*¿Se puede asegurar que el porcentaje de presencia de NDMA ha disminuido? (Asumir un riesgo del 5%).*

*Tema detectado por la app: Proporción de 1 población (p).*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la proporción poblacional p: H1 con signo '<'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: p ≥ 0,05  vs  H1: p < 0,05.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: p ≥ 0,05 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: p < 0,05 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: binomial exacto con n = 160 y p₀ = 0,05.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El ensayo se resuelve con la Binomial exacta (el valor crítico r_c es un entero, con α real ≤ α). No hay ensayos bilaterales sobre p.
- **4 · Condición de rechazo (CR)**: r_c es el mayor valor con F_b(r_c | n = 160; p₀ = 0,05) ≤ α: F_b(4) = 0,0939 > α y F_b(3) = 0,0388 ≤ α → r_c = 3 (α real = 0,0388 ≤ α = 0,05; el α real nunca puede superar al estipulado). Si r ≤ 3 ⇒ se rechaza H0 (la decisión se toma con r contra r_c, a priori).
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 160 unidades y se cuenta la cantidad r de casos. Si r ≤ 3, se rechaza H0 → se puede asegurar que p < 0,05. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que p < 0,05.
- **6 · Cálculos y decisión**: r = 2 (p̂ = 0,0125) ≤ r_c = 3 → se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,0122. El profesor decide con r contra r_c (a priori); el α* «no me gusta».

**Conclusión:** Con α = 0,05, r = 2 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: p ≥ 0,05. Se puede asegurar que p < 0,05.

**Respuesta de la guía:** Sí, se puede asegurar que el porcentaje de presencia de formación de NDMA se ha reducido.

---

### III-26 · Problema 26 (pág. 25)

**Enunciado.** Un proceso productivo debe trabajar con máximo del 1% de defectuosos en condiciones normales de funcionamiento. A fin de controlarlo periódicamente se establece un sistema de muestreo de manera que se cumplan las siguientes condiciones: 1°- detener el proceso productivo con un riesgo máximo del 1%, si trabaja en condiciones normales de funcionamiento; 2°- detener el proceso productivo con una seguridad del 95%, si el porcentaje de defectuosos se incrementa al 2%.

*Se desea establecer el plan de muestreo adecuado.*

*Tema detectado por la app: Proporción de 1 población (p).*

#### Resolución (Diseñar el ensayo (H0, n, valor crítico, regla de decisión)) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: p ≤ 0,01 supone que cumple; H1: p > 0,01 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,01 (error de tipo I); β = P(no rechazar H0 | p = 0,02) = 0,05 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: p ≤ 0,01  vs  H1: p > 0,01.
- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El plan exacto sale de la Binomial (el menor n con G ≤ α y F ≤ β). Las aproximaciones normal o de Poisson solo sirven para calcular n y se justifican con el n RESULTANTE (normal si n·p₀ > 10 y n·(1-p₀) > 10; Poisson si p₀ ≤ 0,005; si no, criterio de Mermoz).
- **Condiciones**: P(rechazar | p₀ = 0,01) ≤ α = 0,01 y P(no rechazar | p₁ = 0,02) ≤ β = 0,05.
- **Plan (binomial exacto, se itera n)**: n = 2258, r_c = 35. α real = 0,0089, β real = 0,0499.
- **Regla de decisión**: Tomar una muestra de n = 2258. Si se encuentran r ≥ 35 casos, se rechaza H0.
- **Por aproximación normal**: n = [(Z(1-α)·√(p₀q₀) + Z(1-β)·√(p₁q₁))/(p₁ - p₀)]² → n = 2133; con ese n el binomial da r_c = 34 (α real = 0,0066, β real = 0,0741). Criterio de aproximación con el n resultante: n·p = 2133·0,01 = 21,33 y n·(1 − p) = 2111,67 (los dos > 10); p = 0,01 > 0,005 → aproximación normal.
- **Otros planes válidos**: para cada r_c, todos los n del rango cumplen α y β (uno de los riesgos baja y el otro sube con n). La app informa el menor n; la guía a veces da el mayor del rango o usa el r_c siguiente.

| r_c | n mínimo | n máximo |
|---|---|---|
| 35 | 2258 | 2277 |
| 36 | 2315 | 2358 |
| 37 | 2372 | 2439 |

- **Por aproximación de Poisson** (Ecuación de García): R = p₁/p₀ = 2; a = [Z(1-β) + Z(1-α)·∛R]/[2(∛R - 1)] = 8,8024; ν = 2/9·(a + √(a² + 1))² = 69,3171; c = ⌊ν/2⌋ = 34 → g.l. = 2c = 68; n = máx[χ²(α; 68)/(2p₀) ; χ²(1-β; 68)/(2p₁)] = máx[2.191,9017 ; 2.206,2541] → n = 2207; r_c = c + 1 = 35. Criterio de aproximación con el n resultante: n·p = 2207·0,01 = 22,07 y n·(1 − p) = 2184,93 (los dos > 10); p = 0,01 > 0,005 → aproximación normal. ⚠️ Con el n resultante el criterio NO habilita Poisson: este n no es una respuesta válida (el profesor, sobre III-11c: el 855 por Poisson es incorrecto porque el criterio se aplicó con el n inicial).

**Conclusión:** Tomar una muestra de n = 2258. Si se encuentran r ≥ 35 casos, se rechaza H0. (Por aproximación normal, justificada con el n resultante: n = 2133 y r_c = 34.)

**Respuesta de la guía:** n = 2.258 y rc = 35, si en una muestra de 2.258 piezas hay 35 o más defectuosas, se concluye que el porcentaje de defectuosas aumentó y el proceso productivo no trabaja en condiciones normales de funcionamiento; o n = 2.133 piezas y rc = 34 defectuosas (por aproximación normal).

---

## TEMA IV — Comparación de varianzas

### IV-1 · Problema 1 (pág. 26)

**Enunciado.** En un taller metalúrgico se han incorporado dos nuevos tornos automáticos de distinta marca. Con ambos tornos se hace la misma pieza. Con el fin de compararlos se toma como base las medidas (en décimas de mm) de los diámetros de dos conjuntos de piezas hechos en cada uno de ellos. Se obtuvieron los siguientes resultados: S1 = 3,6 de una muestra n1 = 13 piezas y S2 = 5,4 de una muestra n2 = 25 piezas.

- **a)** Calcular los límites de confianza del 90% para la relación entre las varianzas poblacionales.
- **b)** Si se decidiera trabajar con muestras iguales en cada torno, ¿cuál sería el tamaño de muestra en cada uno para reducir la relación entre límites anterior a la mitad?
- **c)** Calcular los límites de confianza del 90% para la relación entre los desvíos poblacionales.
- **d)** Si se decidiera trabajar con muestras iguales en cada torno, ¿cuál sería el tamaño de muestra en cada uno para reducir la relación entre los límites de estimación anterior a la mitad?

*Tema detectado por la app: Comparación de 2 varianzas (test F).*

#### a) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la relación de varianzas σ₁²/σ₂² con un 90% de confianza mediante un intervalo de confianza.

- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).
- **Modelo**: (S²₁/σ²₁)/(S²₂/σ²₂) ~ F(ν₁ = 24; ν₂ = 12); F(0,05) = 0,458, F(0,95) = 2,5055.
- **IC para φ² = σ²(Muestra 2)/σ²(Muestra 1)**: j²/F(1-α/2) ; j²/F(α/2) = 2,25/2,5055 ; 2,25/0,458 = [0,898 ; 4,9126]. Inversa σ²(Muestra 1)/σ²(Muestra 2): [0,2036 ; 1,1135].
- **IC para φ = σ(Muestra 2)/σ(Muestra 1)** (raíz de los límites): [0,9476 ; 2,2164]. Inversa σ(Muestra 1)/σ(Muestra 2): [0,4512 ; 1,0552].
- **Relación entre límites** B/A: 5,4704 para las varianzas y 2,3389 para los desvíos.

**Conclusión:** Con un 90% de confianza: P(0,8980 ≤ σ²(Muestra 2)/σ²(Muestra 1) ≤ 4,9127) = 0,9 (límites redondeados hacia afuera; sin redondear: 0,898031 y 4,912605).

**Respuesta de la guía:** Entre 0,2035 y 1,1136 décimas de mm², para la relación (σ1/σ2)², o Entre 0,8980 y 4,9127 décimas de mm², para la relación (σ2/σ1)².

#### b) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para reducir un 50% el error (o la relación entre límites).

- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• Con n₁ = n₂ = n la relación entre límites B/A = F(1-α/2; ν; ν)/F(α/2; ν; ν) depende solo de n: se itera sobre F hasta cumplirla.
- **Relación buscada** B/A = 5,4704·(1 - 0,5) = 2,7352 (varianzas).
- Con n₁ = n₂ = n la relación entre límites ya no depende de los desvíos: B/A = F(1-α/2; ν; ν)/F(α/2; ν; ν). Iterando sobre F: n = 45 (ν = 44) da B/A = 2,7256 ≤ 2,7352.

**Conclusión:** Se necesitan n = 45 unidades en cada muestra (ν = 44). (Hoy hay 25 y 13: Δn = 20 y 32.)

**Respuesta de la guía:** n = 45 piezas, para ambos tornos.

#### c) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la relación de varianzas σ₁²/σ₂² con un 90% de confianza mediante un intervalo de confianza.

- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).
- **Modelo**: (S²₁/σ²₁)/(S²₂/σ²₂) ~ F(ν₁ = 24; ν₂ = 12); F(0,05) = 0,458, F(0,95) = 2,5055.
- **IC para φ² = σ²(Muestra 2)/σ²(Muestra 1)**: j²/F(1-α/2) ; j²/F(α/2) = 2,25/2,5055 ; 2,25/0,458 = [0,898 ; 4,9126]. Inversa σ²(Muestra 1)/σ²(Muestra 2): [0,2036 ; 1,1135].
- **IC para φ = σ(Muestra 2)/σ(Muestra 1)** (raíz de los límites): [0,9476 ; 2,2164]. Inversa σ(Muestra 1)/σ(Muestra 2): [0,4512 ; 1,0552].
- **Relación entre límites** B/A: 5,4704 para las varianzas y 2,3389 para los desvíos.

**Conclusión:** Con un 90% de confianza: P(0,9476 ≤ σ(Muestra 2)/σ(Muestra 1) ≤ 2,2165) = 0,9 (límites redondeados hacia afuera; sin redondear: 0,947645 y 2,21644).

**Respuesta de la guía:** Entre 0,4511 y 1,0553 décimas de mm (para la relación σ1/σ2); o Entre 0,9476 y 2,2165 décimas de mm (para la relación σ2/σ1).

#### d) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para reducir un 50% el error (o la relación entre límites).

- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• Con n₁ = n₂ = n la relación entre límites B/A = F(1-α/2; ν; ν)/F(α/2; ν; ν) depende solo de n: se itera sobre F hasta cumplirla.
- **Relación buscada** B/A = 2,3389·(1 - 0,5) = 1,1694 (desvíos).
- Con n₁ = n₂ = n la relación entre límites ya no depende de los desvíos: B/A = √[F(1-α/2; ν; ν)/F(α/2; ν; ν)]. Iterando sobre F: n = 444 (ν = 443) da B/A = 1,1694 ≤ 1,1694.

**Conclusión:** Se necesitan n = 444 unidades en cada muestra (ν = 443). (Hoy hay 25 y 13: Δn = 419 y 431.)

**Respuesta de la guía:** n = 444 piezas, para ambos tornos.

> 📝 *Notas de la transcripción:* La Resp expresa los límites de la relación de varianzas en 'décimas de mm²' y los de la relación de desvíos en 'décimas de mm', aunque las relaciones son adimensionales; se transcribe tal cual.

---

### IV-2 · Problema 2 (pág. 26)

**Enunciado.** En un taller de manufactura de una pieza de una aleación especial “Dural”, se considera la posibilidad de cambiar la composición química por otra más costosa a efectos de disminuir el desvío estándar de la dimensión crítica en más de un 20%, estableciéndose en 0,1 la probabilidad de cambio si el desvío disminuyera sólo en un 20%. Se hizo una prueba con 21 piezas del material actual (A), obteniéndose un desvío de 0,084 mm y luego otra prueba con 13 piezas de la aleación propuesta (P), que arrojó un desvío de 0,06 mm.

- **a)** ¿Cuál es la decisión recomendada?
- **b)** ¿Cuál es la probabilidad de no cambiar la composición química cuando el desvío disminuye en un 30%?
- **c)** ¿Cuál sería el tamaño de muestra, en cada una de las aleaciones, si se pretende que la probabilidad anterior valga 0,05? (considerar trabajar con el mismo tamaño de muestra en ambas aleaciones).
- **d)** Con los datos obtenidos en el enunciado, calcular un intervalo de confianza del 90% para la relación entre los desvíos.
- **e)** ¿Cuál sería el tamaño de muestra, en cada una de las aleaciones, si se pretende disminuir a la mitad la relación de la estimación anterior? (considerar trabajar con el mismo tamaño de muestra en ambas aleaciones).

*Tema detectado por la app: Comparación de 2 varianzas (test F).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la relación de varianzas σ₁²/σ₂²: H1 con signo '<'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: φ = σ(P)/σ(A) ≥ 0,8  vs  H1: φ = σ(P)/σ(A) < 0,8.  En varianzas: φ₀² = 0,64.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: φ = σ(P)/σ(A) ≥ 0,8 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: φ = σ(P)/σ(A) < 0,8 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: j² = S²(P)/S²(A); bajo H0, j²/φ₀² ~ F(ν₁ = n(P) - 1 = 12; ν₂ = n(A) - 1 = 20).
- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².
- **4 · Condición de rechazo (CR)**: j²c = φ₀²·F(0,1; 12; 20) = 0,64·0,4855 = 0,3107 (jc = 0,5574). Si j² < 0,3107 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la relación j² = S²(P)/S²(A) con las muestras de 13 y 21. Si j² < 0,3107, se rechaza H0 → se puede asegurar que φ = σ(P)/σ(A) < 0,8. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(P)/σ(A) < 0,8.
- **6 · Cálculos y decisión** (el estimador contra el valor crítico): J = S(P)/S(A) = 0,06/0,084 = 0,7143 (J² = 0,5102) contra Jc = √0,3107 = 0,5574 → no cae en la zona de rechazo.

**Conclusión:** Con α = 0,1, J = 0,7143 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: φ = σ(P)/σ(A) ≥ 0,8. No hay evidencia suficiente para asegurar que φ = σ(P)/σ(A) < 0,8 (no rechazar H0 no la prueba).

**Respuesta de la guía:** H0: σP ≥ 0,8·σA; para φ = σP/σA, H0: φ ≥ φ0 = 0,8. jc = 0,5574 (j²c = 0,3107); j = SP/SA = 0,7143 (j² = 0,5102). No se rechaza la H0: no se aconseja el cambio de composición química, porque no se puede probar que la aleación propuesta disminuya el desvío en más de un 20% respecto de la aleación actual.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: φ = σ(P)/σ(A) ≥ 0,8  vs  H1: φ = σ(P)/σ(A) < 0,8  (α = 0,1).  En varianzas: φ₀² = 0,64.
- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².  
• Para β / potencia se usa que j²/φ₁² ~ F(ν₁; ν₂) cuando la relación verdadera es φ₁.
- **Estadístico**: j² = S²(P)/S²(A); bajo H0, j²/φ₀² ~ F(ν₁ = n(P) - 1 = 12; ν₂ = n(A) - 1 = 20).
- **Condición de rechazo**: j²c = φ₀²·F(0,1; 12; 20) = 0,64·0,4855 = 0,3107 (jc = 0,5574). Si j² < 0,3107 ⇒ se rechaza H0.
- **Si φ = φ₁ = 0,7** (φ₁² = 0,49), j²/φ₁² ~ F(12; 20). P(rechazar H0) = P(F(12; 20) < j²c/φ₁²) = P(F < 0,3107/0,49 = 0,6341) = 0,2103.
- **Potencia** 1-β = 0,2103.

**Conclusión:** La probabilidad pedida es β = 0,7897 (potencia 1-β = 0,2103).

**Respuesta de la guía:** β = 0,7897 (para φ1 = 0,70).

#### c) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: φ = σ(P)/σ(A) ≥ 0,8 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: φ = σ(P)/σ(A) < 0,8 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I); β = P(no rechazar H0 | φ = σ(P)/σ(A) = 0,7) = 0,05 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: φ = σ(P)/σ(A) ≥ 0,8  vs  H1: φ = σ(P)/σ(A) < 0,8.
- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².  
• Para β / potencia se usa que j²/φ₁² ~ F(ν₁; ν₂) cuando la relación verdadera es φ₁.
- **Condiciones**: P(rechazar H0 | φ = 0,8) = α = 0,1 y P(no rechazar H0 | φ = 0,7) = β = 0,05.
- **Tamaño de muestra** (n₁ = n₂ = n, ν₁ = ν₂ = n - 1): hay que cumplir R = φ₀²/φ₁² = 0,64/0,49 = 1,3061 ≥ F(1-α; ν; ν)·F(1-β; ν; ν). Iterando sobre F: n = 483 (ν = 482).
- **Condición de rechazo**: j²c = φ₀²·F(0,1; 482; 482) = 0,5694 (jc = 0,7546). Si j² < 0,5694 ⇒ se rechaza H0.
- **Regla de decisión**: Si en 483 muestras de cada grupo la relación j = S(P)/S(A) es menor que 0,7546, se rechaza H0 → se puede asegurar que φ = σ(P)/σ(A) < 0,8. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(P)/σ(A) < 0,8.
- Con n = 483: β real = 0,0497, potencia real = 0,9503.

**Conclusión:** ν = 482: n = 483 en cada muestra (P y A). Si en 483 muestras de cada grupo la relación j = S(P)/S(A) es menor que 0,7546, se rechaza H0 → se puede asegurar que φ = σ(P)/σ(A) < 0,8. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(P)/σ(A) < 0,8. (Hoy hay 13 de P y 21 de A: Δn = 470 y 462.)

**Respuesta de la guía:** ν = 482 ⇒ n = nP = nA = 483 piezas de cada aleación.

#### d) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la relación de varianzas σ₁²/σ₂² con un 90% de confianza mediante un intervalo de confianza.

- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).
- **Modelo**: (S²₁/σ²₁)/(S²₂/σ²₂) ~ F(ν₁ = 12; ν₂ = 20); F(0,05) = 0,3931, F(0,95) = 2,2776.
- **IC para φ² = σ²(P)/σ²(A)**: j²/F(1-α/2) ; j²/F(α/2) = 0,5102/2,2776 ; 0,5102/0,3931 = [0,224 ; 1,2977]. Inversa σ²(A)/σ²(P): [0,7706 ; 4,4641].
- **IC para φ = σ(P)/σ(A)** (raíz de los límites): [0,4733 ; 1,1392]. Inversa σ(A)/σ(P): [0,8778 ; 2,1128].
- **Relación entre límites** B/A: 5,7932 para las varianzas y 2,4069 para los desvíos.

**Conclusión:** Con un 90% de confianza: P(0,4732 ≤ σ(P)/σ(A) ≤ 1,1392) = 0,9 (límites redondeados hacia afuera; sin redondear: 0,473298 y 1,139188).

**Respuesta de la guía:** Entre 0,4732 y 1,1392 (para la relación φ = σP/σA).

#### e) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para reducir un 50% el error (o la relación entre límites).

- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• Con n₁ = n₂ = n la relación entre límites B/A = F(1-α/2; ν; ν)/F(α/2; ν; ν) depende solo de n: se itera sobre F hasta cumplirla.
- **Relación buscada** B/A = 2,4069·(1 - 0,5) = 1,2035 (desvíos).
- Con n₁ = n₂ = n la relación entre límites ya no depende de los desvíos: B/A = √[F(1-α/2; ν; ν)/F(α/2; ν; ν)]. Iterando sobre F: n = 318 (ν = 317) da B/A = 1,2033 ≤ 1,2035.

**Conclusión:** Se necesitan n = 318 unidades en cada muestra (ν = 317). (Hoy hay 13 y 21: Δn = 305 y 297.)

**Respuesta de la guía:** ν = 317 ⇒ n = nA = nP = 318 piezas de cada aleación.

> 📝 *Notas de la transcripción:* Sin 'Resp:'; respuesta armada desde la Solución. En d) la Solución usa R' = B'/A' = 2,4069, en e) R' = 1,2035 y R = 1,4483 para iterar ν. Las frases de porcentajes en d) (47,32%, 87,78%, 13,92%) se transcriben tal cual; el paréntesis queda sin cerrar en la guía.

<details><summary>Cómo lo concluye la guía</summary>

> De manera que la hipótesis no se rechaza por lo cual no se aconseja el cambio de composición química, porque no se puede probar que la aleación propuesta disminuya el desvío en más de un 20% respecto de la aleación actual.
> β = 1 − F_F-S(0,6341) = 0,7897.
> O sea que se deben elegir 483 piezas de cada aleación.
> Los límites de la relación se encontrarán entre 0,4732 y 1,1392. Quiere decir que el desvío estándar de la aleación propuesta puede ser mayor que la actual en un 47,32% o el desvío estándar de la aleación actual puede ser mayor que la propuesta en un 87,78% (o sea que la aleación propuesta puede incrementar su desvío estándar como máximo en un 13,92% respecto de la actual.
> Como n = ν + 1: n = nA = nP = 318 piezas de cada aleación.

</details>

---

### IV-3 · Problema 3 (pág. 27)

**Enunciado.** Una empresa agropecuaria posee dos establecimientos de invernada para engorde de novillos Angus, denominados “La Providencia” y “Casablanca”. Los lotes que salen a venta en ambos presentan pesos promedio razonablemente controlados, pero hay dudas en la variabilidad pues parece, por lo que se aprecia visualmente, que no son todos iguales de parejos lo cual se debe, probablemente, a distintos criterios de selección por parte de los capataces. A efectos de la comparación, se registraron los pesos de 50 animales terminados de cada establecimiento, con los siguientes resultados: Establecimiento: “La Providencia” | “Casablanca”; Muestra: n = 50 | 50; Media: x̄ = 428 kg | 432 kg; Desvío: S = 12 kg | 18 kg.

- **a)** ¿Se puede asegurar, con 5% de error, que los desvíos difieren (o sea que el de Casablanca es mayor al de La Providencia)?
- **b)** Calcular la probabilidad de no detectar que el desvío de Casablanca es un 20% mayor que el desvío de La Providencia.
- **c)** ¿Cuál debería ser el tamaño de muestra en cada establecimiento para que la probabilidad anterior valga 0,10?
- **d)** Con los datos del problema, establecer los límites de confianza del 90% para la relación de dichos desvíos.
- **e)** Recalcular el tamaño de muestra para un intervalo de estimación cuyo límite superior sea un 50% mayor que el inferior.

| Establecimiento | “La Providencia” | “Casablanca” |
|---|---|---|
| Muestra: n = | 50 | 50 |
| Media: x̄ = | 428 kg | 432 kg |
| Desvío: S = | 12 kg | 18 kg |

*Tema detectado por la app: Comparación de 2 varianzas (test F).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la relación de varianzas σ₁²/σ₂²: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: φ = σ(Casablanca)/σ(La Providencia) ≤ 1  vs  H1: φ = σ(Casablanca)/σ(La Providencia) > 1.  En varianzas: φ₀² = 1.
- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: φ = σ(Casablanca)/σ(La Providencia) ≤ 1 supone que cumple; H1: φ = σ(Casablanca)/σ(La Providencia) > 1 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: j² = S²(Casablanca)/S²(La Providencia); bajo H0, j²/φ₀² ~ F(ν₁ = n(Casablanca) - 1 = 49; ν₂ = n(La Providencia) - 1 = 49).
- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².
- **4 · Condición de rechazo (CR)**: j²c = φ₀²·F(0,95; 49; 49) = 1·1,6073 = 1,6073 (jc = 1,2678). Si j² > 1,6073 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la relación j² = S²(Casablanca)/S²(La Providencia) con las muestras de 50 y 50. Si j² > 1,6073, se rechaza H0 → se puede asegurar que φ = σ(Casablanca)/σ(La Providencia) > 1. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(Casablanca)/σ(La Providencia) > 1.
- **6 · Cálculos y decisión** (el estimador contra el valor crítico): J = S(Casablanca)/S(La Providencia) = 18/12 = 1,5 (J² = 2,25) contra Jc = √1,6073 = 1,2678 → cae en la zona de rechazo.

**Conclusión:** Con α = 0,05, J = 1,5 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: φ = σ(Casablanca)/σ(La Providencia) ≤ 1. Se puede asegurar que φ = σ(Casablanca)/σ(La Providencia) > 1.

**Respuesta de la guía:** Si, se puede asegurar que los desvíos difieren (en Casablanca el desvío es mayor que en La Providencia).

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular β = P(no rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: φ = σ(Casablanca)/σ(La Providencia) ≤ 1  vs  H1: φ = σ(Casablanca)/σ(La Providencia) > 1  (α = 0,05).  En varianzas: φ₀² = 1.
- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².  
• Para β / potencia se usa que j²/φ₁² ~ F(ν₁; ν₂) cuando la relación verdadera es φ₁.
- **Estadístico**: j² = S²(Casablanca)/S²(La Providencia); bajo H0, j²/φ₀² ~ F(ν₁ = n(Casablanca) - 1 = 49; ν₂ = n(La Providencia) - 1 = 49).
- **Condición de rechazo**: j²c = φ₀²·F(0,95; 49; 49) = 1·1,6073 = 1,6073 (jc = 1,2678). Si j² > 1,6073 ⇒ se rechaza H0.
- **Si φ = φ₁ = 1,2** (φ₁² = 1,44), j²/φ₁² ~ F(49; 49). P(rechazar H0) = P(F(49; 49) > j²c/φ₁²) = P(F > 1,6073/1,44 = 1,1162) = 0,351.
- **Potencia** 1-β = 0,351.

**Conclusión:** La probabilidad pedida es β = 0,649 (potencia 1-β = 0,351).

**Respuesta de la guía:** β = 0,649.

#### c) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio optimista**: se controla algo que en principio cumple (proceso, lote, especificación). H0: φ = σ(Casablanca)/σ(La Providencia) ≤ 1 supone que cumple; H1: φ = σ(Casablanca)/σ(La Providencia) > 1 es el incumplimiento que se quiere detectar. Se lo da por bueno salvo evidencia en contra.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | φ = σ(Casablanca)/σ(La Providencia) = 1,2) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: φ = σ(Casablanca)/σ(La Providencia) ≤ 1  vs  H1: φ = σ(Casablanca)/σ(La Providencia) > 1.
- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².  
• Para β / potencia se usa que j²/φ₁² ~ F(ν₁; ν₂) cuando la relación verdadera es φ₁.
- **Condiciones**: P(rechazar H0 | φ = 1) = α = 0,05 y P(no rechazar H0 | φ = 1,2) = β = 0,1.
- **Tamaño de muestra** (n₁ = n₂ = n, ν₁ = ν₂ = n - 1): hay que cumplir R = φ₀²/φ₁² = 1/1,44 = 1,44 ≥ F(1-α; ν; ν)·F(1-β; ν; ν). Iterando sobre F: n = 260 (ν = 259).
- **Condición de rechazo**: j²c = φ₀²·F(0,95; 259; 259) = 1,2273 (jc = 1,1078). Si j² > 1,2273 ⇒ se rechaza H0.
- **Regla de decisión**: Si en 260 muestras de cada grupo la relación j = S(Casablanca)/S(La Providencia) es mayor que 1,1078, se rechaza H0 → se puede asegurar que φ = σ(Casablanca)/σ(La Providencia) > 1. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(Casablanca)/σ(La Providencia) > 1.
- Con n = 260: β real = 0,0995, potencia real = 0,9005.

**Conclusión:** ν = 259: n = 260 en cada muestra (Casablanca y La Providencia). Si en 260 muestras de cada grupo la relación j = S(Casablanca)/S(La Providencia) es mayor que 1,1078, se rechaza H0 → se puede asegurar que φ = σ(Casablanca)/σ(La Providencia) > 1. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(Casablanca)/σ(La Providencia) > 1. Respecto de las 50 anteriores: Δn = 210 más en cada una.

**Respuesta de la guía:** n = 260 animales terminados en cada establecimiento.

#### d) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la relación de varianzas σ₁²/σ₂² con un 90% de confianza mediante un intervalo de confianza.

- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).
- **Modelo**: (S²₁/σ²₁)/(S²₂/σ²₂) ~ F(ν₁ = 49; ν₂ = 49); F(0,05) = 0,6222, F(0,95) = 1,6073.
- **IC para φ² = σ²(Casablanca)/σ²(La Providencia)**: j²/F(1-α/2) ; j²/F(α/2) = 2,25/1,6073 ; 2,25/0,6222 = [1,3999 ; 3,6164]. Inversa σ²(La Providencia)/σ²(Casablanca): [0,2765 ; 0,7144].
- **IC para φ = σ(Casablanca)/σ(La Providencia)** (raíz de los límites): [1,1832 ; 1,9017]. Inversa σ(La Providencia)/σ(Casablanca): [0,5258 ; 0,8452].
- **Relación entre límites** B/A: 2,5834 para las varianzas y 1,6073 para los desvíos.

**Conclusión:** Con un 90% de confianza: P(1,1831 ≤ σ(Casablanca)/σ(La Providencia) ≤ 1,9017) = 0,9 (límites redondeados hacia afuera; sin redondear: 1,183162 y 1,901684). El desvío de Casablanca es mayor que el de La Providencia entre un 18,32% y un 90,17%.

**Respuesta de la guía:** Entre 1,1831 y 1,9017 (para la relación σCa/σLP); quiere decir que el desvío de Casablanca puede ser mayor que el de La Providencia entre un 18,31% y un 90,17%.

#### e) Tamaño de muestra ✅

*Qué pide:* Calcular el tamaño de muestra para que la relación entre límites sea R' = 1,5.

- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• Con n₁ = n₂ = n la relación entre límites B/A = F(1-α/2; ν; ν)/F(α/2; ν; ν) depende solo de n: se itera sobre F hasta cumplirla.
- **Relación buscada** B/A = 1,5 (desvíos).
- Con n₁ = n₂ = n la relación entre límites ya no depende de los desvíos: B/A = √[F(1-α/2; ν; ν)/F(α/2; ν; ν)]. Iterando sobre F: n = 68 (ν = 67) da B/A = 1,499 ≤ 1,5.

**Conclusión:** Se necesitan n = 68 unidades en cada muestra (ν = 67). (Hoy hay 50 y 50: Δn = 18 y 18.)

**Respuesta de la guía:** En cada establecimiento 68 animales terminados.

> 📝 *Notas de la transcripción:* En la Resp la última parte está rotulada 'c)' pero corresponde al inciso e) (68 animales); se transcribe tal cual en 'respuesta' y se asigna al inciso e).

---

### IV-4 · Problema 4 (pág. 27)

**Enunciado.** En una hilandería se considera la posibilidad de reacondicionar a nuevo las hiladoras, si es posible asegurar con el reacondicionamiento, una reducción del 12% en el desvío estándar de la producción por máquina. Se eligieron entonces 4 máquinas al azar y se las reacondicionó, registrándose luego la producción de cada una para un período dado; se obtuvo así una media de 1.470 metros de hilado con un desvío estándar de 132 metros. Como se desconocía la producción de las máquinas sin reacondicionar, se registró la producción de 16 de ellas en el mismo período, obteniéndose una media de 1.208 metros con un desvío de 354 metros.

- **a)** ¿Se puede asegurar, con 10% de error, que hay una reducción del 12% en el desvío de las máquinas reacondicionadas respecto de las sin reacondicionar?
- **b)** ¿Cuál es la probabilidad de detectar una reducción del 30%?
- **c)** Calcular el tamaño de muestra necesario para que la probabilidad anterior valga 0,90.

*Tema detectado por la app: Comparación de 2 varianzas (test F).*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la relación de varianzas σ₁²/σ₂²: H1 con signo '<'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: φ = σ(reacondicionadas)/σ(sin reacondicionar) ≥ 0,88  vs  H1: φ = σ(reacondicionadas)/σ(sin reacondicionar) < 0,88.  En varianzas: φ₀² = 0,7744.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: φ = σ(reacondicionadas)/σ(sin reacondicionar) ≥ 0,88 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: φ = σ(reacondicionadas)/σ(sin reacondicionar) < 0,88 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: j² = S²(reacondicionadas)/S²(sin reacondicionar); bajo H0, j²/φ₀² ~ F(ν₁ = n(reacondicionadas) - 1 = 3; ν₂ = n(sin reacondicionar) - 1 = 15).
- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².
- **4 · Condición de rechazo (CR)**: j²c = φ₀²·F(0,1; 3; 15) = 0,7744·0,1923 = 0,1489 (jc = 0,3859). Si j² < 0,1489 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la relación j² = S²(reacondicionadas)/S²(sin reacondicionar) con las muestras de 4 y 16. Si j² < 0,1489, se rechaza H0 → se puede asegurar que φ = σ(reacondicionadas)/σ(sin reacondicionar) < 0,88. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(reacondicionadas)/σ(sin reacondicionar) < 0,88.
- **6 · Cálculos y decisión** (el estimador contra el valor crítico): J = S(reacondicionadas)/S(sin reacondicionar) = 132/354 = 0,3729 (J² = 0,139) contra Jc = √0,1489 = 0,3859 → cae en la zona de rechazo.

**Conclusión:** Con α = 0,1, J = 0,3729 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: φ = σ(reacondicionadas)/σ(sin reacondicionar) ≥ 0,88. Se puede asegurar que φ = σ(reacondicionadas)/σ(sin reacondicionar) < 0,88.

**Respuesta de la guía:** Si, se puede asegurar que hay una reducción de más del 12% (las máquinas reacondicionadas tienen un desvío estándar un 12% menor que el desvío de las máquinas sin reacondicionar).

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: φ = σ(reacondicionadas)/σ(sin reacondicionar) ≥ 0,88  vs  H1: φ = σ(reacondicionadas)/σ(sin reacondicionar) < 0,88  (α = 0,1).  En varianzas: φ₀² = 0,7744.
- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².  
• Para β / potencia se usa que j²/φ₁² ~ F(ν₁; ν₂) cuando la relación verdadera es φ₁.
- **Estadístico**: j² = S²(reacondicionadas)/S²(sin reacondicionar); bajo H0, j²/φ₀² ~ F(ν₁ = n(reacondicionadas) - 1 = 3; ν₂ = n(sin reacondicionar) - 1 = 15).
- **Condición de rechazo**: j²c = φ₀²·F(0,1; 3; 15) = 0,7744·0,1923 = 0,1489 (jc = 0,3859). Si j² < 0,1489 ⇒ se rechaza H0.
- **Si φ = φ₁ = 0,7** (φ₁² = 0,49), j²/φ₁² ~ F(3; 15). P(rechazar H0) = P(F(3; 15) < j²c/φ₁²) = P(F < 0,1489/0,49 = 0,3039) = 0,1779.
- **Potencia** 1-β = 0,1779.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,1779 (β = 0,8221).

**Respuesta de la guía:** 1−β = 0,1779.

#### c) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: φ = σ(reacondicionadas)/σ(sin reacondicionar) ≥ 0,88 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: φ = σ(reacondicionadas)/σ(sin reacondicionar) < 0,88 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I); β = P(no rechazar H0 | φ = σ(reacondicionadas)/σ(sin reacondicionar) = 0,7) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: φ = σ(reacondicionadas)/σ(sin reacondicionar) ≥ 0,88  vs  H1: φ = σ(reacondicionadas)/σ(sin reacondicionar) < 0,88.
- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².  
• Para β / potencia se usa que j²/φ₁² ~ F(ν₁; ν₂) cuando la relación verdadera es φ₁.
- **Condiciones**: P(rechazar H0 | φ = 0,88) = α = 0,1 y P(no rechazar H0 | φ = 0,7) = β = 0,1.
- **Tamaño de muestra** (n₁ = n₂ = n, ν₁ = ν₂ = n - 1): hay que cumplir R = φ₀²/φ₁² = 0,7744/0,49 = 1,5804 ≥ F(1-α; ν; ν)·F(1-β; ν; ν). Iterando sobre F: n = 128 (ν = 127).
- **Condición de rechazo**: j²c = φ₀²·F(0,1; 127; 127) = 0,6164 (jc = 0,7851). Si j² < 0,6164 ⇒ se rechaza H0.
- **Regla de decisión**: Si en 128 muestras de cada grupo la relación j = S(reacondicionadas)/S(sin reacondicionar) es menor que 0,7851, se rechaza H0 → se puede asegurar que φ = σ(reacondicionadas)/σ(sin reacondicionar) < 0,88. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(reacondicionadas)/σ(sin reacondicionar) < 0,88.
- Con n = 128: β real = 0,0986, potencia real = 0,9014.

**Conclusión:** ν = 127: n = 128 en cada muestra (reacondicionadas y sin reacondicionar). Si en 128 muestras de cada grupo la relación j = S(reacondicionadas)/S(sin reacondicionar) es menor que 0,7851, se rechaza H0 → se puede asegurar que φ = σ(reacondicionadas)/σ(sin reacondicionar) < 0,88. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(reacondicionadas)/σ(sin reacondicionar) < 0,88. (Hoy hay 4 de reacondicionadas y 16 de sin reacondicionar: Δn = 124 y 112.)

**Respuesta de la guía:** n = 128 máquinas reacondicionadas y 128 máquinas sin reacondicionamiento.

---

### IV-5 · Problema 5 (pág. 28)

**Enunciado.** Se quiere realizar un experimento para probar la eficacia de un aditivo en la fórmula de un tipo de látex, con el que se espera una reducción significativa de la desviación estándar. A tal fin se estipulan las siguientes condiciones: se establece un riesgo máximo del 5% de adoptar el aditivo si no hay reducción del desvío estándar y una probabilidad de 0,99 de adoptar el aditivo si la reducción de la desviación es de un 30% respecto a la fórmula sin el aditivo.

- **a)** Indicar la hipótesis nula apropiada, el tamaño de la muestra a tomar, establecer la condición de rechazo y la regla de decisión.
- **b)** Calcular la probabilidad de adoptar el aditivo si con él se obtiene una reducción del 20% respecto de la fórmula sin el aditivo.
- **c)** ¿Cuántas muestras más habría que observar de cada fórmula del látex para que la probabilidad anterior valga 0,9?

*Tema detectado por la app: Comparación de 2 varianzas (test F).*

#### a) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: φ = σ(con aditivo)/σ(sin aditivo) ≥ 1 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: φ = σ(con aditivo)/σ(sin aditivo) < 1 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | φ = σ(con aditivo)/σ(sin aditivo) = 0,7) = 0,01 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: φ = σ(con aditivo)/σ(sin aditivo) ≥ 1  vs  H1: φ = σ(con aditivo)/σ(sin aditivo) < 1.
- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².  
• Para β / potencia se usa que j²/φ₁² ~ F(ν₁; ν₂) cuando la relación verdadera es φ₁.
- **Condiciones**: P(rechazar H0 | φ = 1) = α = 0,05 y P(no rechazar H0 | φ = 0,7) = β = 0,01.
- **Tamaño de muestra** (n₁ = n₂ = n, ν₁ = ν₂ = n - 1): hay que cumplir R = φ₀²/φ₁² = 1/0,49 = 2,0408 ≥ F(1-α; ν; ν)·F(1-β; ν; ν). Iterando sobre F: n = 127 (ν = 126).
- **Condición de rechazo**: j²c = φ₀²·F(0,05; 126; 126) = 0,7451 (jc = 0,8632). Si j² < 0,7451 ⇒ se rechaza H0.
- **Regla de decisión**: Si en 127 muestras de cada grupo la relación j = S(con aditivo)/S(sin aditivo) es menor que 0,8632, se rechaza H0 → se puede asegurar que φ = σ(con aditivo)/σ(sin aditivo) < 1. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(con aditivo)/σ(sin aditivo) < 1.
- Con n = 127: β real = 0,0097, potencia real = 0,9903.

**Conclusión:** ν = 126: n = 127 en cada muestra (con aditivo y sin aditivo). Si en 127 muestras de cada grupo la relación j = S(con aditivo)/S(sin aditivo) es menor que 0,8632, se rechaza H0 → se puede asegurar que φ = σ(con aditivo)/σ(sin aditivo) < 1. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(con aditivo)/σ(sin aditivo) < 1.

**Respuesta de la guía:** H0: σCA ≥ σSA, para la relación φ = σCA/σSA, H0: φ ≥ φ0 = 1, nCA = 127 muestras de látex con aditivo y nCA = 127 muestras de látex sin aditivo. CR: Si j < jc = 0,8632 ⇒ Rechazo la H0. RD: Si en 127 muestras de cada fórmula de látex, la relación j = σCA/σSA es menor que 0,8632, se rechaza la H0 y se adopta el aditivo en la fórmula del látex.

#### b) Probabilidad de error / potencia (β, 1-β) ✅

*Qué pide:* Calcular la potencia 1-β = P(rechazar H0 | H0 falsa) para el valor alternativo del parámetro, con la región crítica del ensayo.

- **Hipótesis**: H0: φ = σ(con aditivo)/σ(sin aditivo) ≥ 1  vs  H1: φ = σ(con aditivo)/σ(sin aditivo) < 1  (α = 0,05).  En varianzas: φ₀² = 1.
- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².  
• Para β / potencia se usa que j²/φ₁² ~ F(ν₁; ν₂) cuando la relación verdadera es φ₁.
- **Estadístico**: j² = S²(con aditivo)/S²(sin aditivo); bajo H0, j²/φ₀² ~ F(ν₁ = n(con aditivo) - 1 = 126; ν₂ = n(sin aditivo) - 1 = 126).
- **Condición de rechazo**: j²c = φ₀²·F(0,05; 126; 126) = 1·0,7451 = 0,7451 (jc = 0,8632). Si j² < 0,7451 ⇒ se rechaza H0.
- **Si φ = φ₁ = 0,8** (φ₁² = 0,64), j²/φ₁² ~ F(126; 126). P(rechazar H0) = P(F(126; 126) < j²c/φ₁²) = P(F < 0,7451/0,64 = 1,1643) = 0,8028.
- **Potencia** 1-β = 0,8028.

**Conclusión:** La probabilidad pedida es la potencia 1-β = 0,8028 (β = 0,1972).

**Respuesta de la guía:** 1−β = 0,1972.

#### c) Diseñar el ensayo (H0, n, valor crítico, regla de decisión) ✅

*Qué pide:* Diseñar el ensayo: plantear H0 (según el criterio), hallar n y el valor crítico que cumplen las dos condiciones (α y β) y escribir la regla de decisión.

- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: φ = σ(con aditivo)/σ(sin aditivo) ≥ 1 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: φ = σ(con aditivo)/σ(sin aditivo) < 1 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I); β = P(no rechazar H0 | φ = σ(con aditivo)/σ(sin aditivo) = 0,8) = 0,1 (error de tipo II).  
• El ensayo es unilateral a la izquierda: la zona de rechazo está donde apunta H1.
- **Hipótesis**: H0: φ = σ(con aditivo)/σ(sin aditivo) ≥ 1  vs  H1: φ = σ(con aditivo)/σ(sin aditivo) < 1.
- **Modelos y distribuciones empleados**:  
• Las dos variables se suponen Normales y las muestras independientes (supuesto necesario: la F no es robusta si X no es Normal).  
• Entonces (S₁²/σ₁²)/(S₂²/σ₂²) ~ F de Snedecor con ν₁ = n₁-1 (numerador) y ν₂ = n₂-1 (denominador). Con φ = σ₁/σ₂ y j² = S₁²/S₂²: j²/φ² ~ F(ν₁; ν₂). La F es asimétrica: el IC no es simétrico y F(α; ν₁; ν₂) = 1/F(1-α; ν₂; ν₁).  
• En el ensayo, bajo H0 (φ = φ₀) el valor crítico de j² es φ₀²·F; si φ₀ ≠ 1 (p. ej. 'reducir el desvío un 12%' → φ₀ = 0,88) el fractil se multiplica por φ₀².  
• Para β / potencia se usa que j²/φ₁² ~ F(ν₁; ν₂) cuando la relación verdadera es φ₁.
- **Condiciones**: P(rechazar H0 | φ = 1) = α = 0,05 y P(no rechazar H0 | φ = 0,8) = β = 0,1.
- **Tamaño de muestra** (n₁ = n₂ = n, ν₁ = ν₂ = n - 1): hay que cumplir R = φ₀²/φ₁² = 1/0,64 = 1,5625 ≥ F(1-α; ν; ν)·F(1-β; ν; ν). Iterando sobre F: n = 174 (ν = 173).
- **Condición de rechazo**: j²c = φ₀²·F(0,05; 173; 173) = 0,7782 (jc = 0,8821). Si j² < 0,7782 ⇒ se rechaza H0.
- **Regla de decisión**: Si en 174 muestras de cada grupo la relación j = S(con aditivo)/S(sin aditivo) es menor que 0,8821, se rechaza H0 → se puede asegurar que φ = σ(con aditivo)/σ(sin aditivo) < 1. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(con aditivo)/σ(sin aditivo) < 1.
- Con n = 174: β real = 0,0998, potencia real = 0,9002.

**Conclusión:** ν = 173: n = 174 en cada muestra (con aditivo y sin aditivo). Si en 174 muestras de cada grupo la relación j = S(con aditivo)/S(sin aditivo) es menor que 0,8821, se rechaza H0 → se puede asegurar que φ = σ(con aditivo)/σ(sin aditivo) < 1. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que φ = σ(con aditivo)/σ(sin aditivo) < 1. Respecto de las 127 anteriores: Δn = 47 más en cada una.

**Respuesta de la guía:** nCA = nSA = 174 muestras, o sea 47 muestras más de cada fórmula del látex.

> 📝 *Notas de la transcripción:* En la Resp a) dice 'nCA = 127 muestras de látex sin aditivo' (debería ser nSA); y la RD define j = σCA/σSA (cociente de desvíos poblacionales, cuando j es el muestral SCA/SSA). Se transcribe tal cual.

---

## TEMA V — Comparación de dos medias

### V-1 · Problema 1 (pág. 29)

**Enunciado.** En la década del '70 se descubrió que la sustancia cancerígena (NDMA) se formaba durante el secado de la malta verde usada en la fabricación de cerveza. En la década del '80 se desarrolla un nuevo proceso de secado inoculando un inhibidor biogenético para minimizar la formación promedio de NDMA. Se obtuvieron muestras de ambos procesos con los siguientes resultados expresados en partes por billón de NDMA: Proceso Viejo: 6 – 4 – 5 – 5 – 6 – 5 – 5 – 6 – 4 – 6 – 7 – 4; Proceso Nuevo: 2 – 1 – 2 – 2 – 1 – 0 – 3 – 2 – 1 – 0 – 1 – 3.

- **a)** ¿Qué se puede decir, del nuevo proceso de secado, a la luz de los resultados obtenidos? (Asumir un riesgo del 1%).
- **b)** Calcular los límites de confianza del 90% para la diferencia entre las formaciones promedio de NDMA de ambos procesos.
- **c)** ¿Cuántas muestras más habría que tener de ambos procesos para reducir el error anterior a la mitad? (considerar trabajar con el mismo tamaño de muestra en ambos procesos de secado).

| Proceso | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Proceso Viejo | 6 | 4 | 5 | 5 | 6 | 5 | 5 | 6 | 4 | 6 | 7 | 4 |
| Proceso Nuevo | 2 | 1 | 2 | 2 | 1 | 0 | 3 | 2 | 1 | 0 | 1 | 3 |

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(Proceso Nuevo) - μ(Proceso Viejo) ≥ 0  vs  H1: δ = μ(Proceso Nuevo) - μ(Proceso Viejo) < 0.
- **2 · Nivel de significación**: α = 0,01 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Proceso Nuevo) > S(Proceso Viejo), lo único que se puede sospechar es σ(Proceso Nuevo) > σ(Proceso Viejo) → unilateral, H0: φ = σ(Proceso Nuevo)/σ(Proceso Viejo) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 11; ν₂ = 11) = √2,2269 = 1,4923; J = S(Proceso Nuevo)/S(Proceso Viejo) = 1,0359 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,982807; ν = n₁ + n₂ - 2 = 22.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(Proceso Nuevo) - x̄(Proceso Viejo) = -3,75; σ(d) = 0,401229, ν = 22.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ - t·σ(d) = -1,0064. Si d < -1,0064 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d < -1,0064, se rechaza H0 → se puede asegurar que δ = μ(Proceso Nuevo) - μ(Proceso Viejo) < 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Proceso Nuevo) - μ(Proceso Viejo) < 0.
- **6 · Cálculos y decisión**: d = -3,75 → se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,01, d = -3,75 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: δ = μ(Proceso Nuevo) - μ(Proceso Viejo) ≥ 0. Se puede asegurar que δ = μ(Proceso Nuevo) - μ(Proceso Viejo) < 0.

**Respuesta de la guía:** Desvíos: H0: σN ≤ σV (φ = σN/σV, H0: φ ≤ φ0 = 1), jc = 1,4923 (j²c = 2,2269), j = 1,0359 (j² = 1,0732): no se rechaza, se suponen desvíos iguales; Sa = 0,9828 p.p.b., ν = 22. Medias: H0: μN ≥ μV (δ = μN − μV, H0: δ ≥ δ0 = 0), dc = −1,0064 p.p.b., d = 1,5 − 5,25 = −3,75 p.p.b. Se rechaza la hipótesis: se puede asegurar que el proceso nuevo ha minimizado la formación de NDMA.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Pide estimar el parámetro: intervalo de confianza P(A ≤ θ ≤ B) = 1-α.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Modelo**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Proceso Nuevo) > S(Proceso Viejo), lo único que se puede sospechar es σ(Proceso Nuevo) > σ(Proceso Viejo) → unilateral, H0: φ = σ(Proceso Nuevo)/σ(Proceso Viejo) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 11; ν₂ = 11) = √2,2269 = 1,4923; J = S(Proceso Nuevo)/S(Proceso Viejo) = 1,0359 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,982807; ν = n₁ + n₂ - 2 = 22.
- **IC para δ = μ(Proceso Nuevo) - μ(Proceso Viejo)** (t con Sa (desvíos iguales)): d = -3,75; e = t(0,95; 22)·σ(d) = 1,7171·0,401229 = 0,689.

**Conclusión:** P(-4,44 ≤ μ(Proceso Nuevo) - μ(Proceso Viejo) ≤ -3,06) = 0,9 (e = 0,689). Para μ(Proceso Viejo) - μ(Proceso Nuevo): entre 3,06 y 4,44. Límites redondeados hacia afuera; sin redondear: -4,438968 y -3,061032.

**Respuesta de la guía:** Entre 3,06 y 4,44 partes por billón (δ = μV − μN; 3,75 ± 0,6890), con un error de muestreo e = 0,6890 p.p.b.

#### c) Tamaño de muestra ✅

*Qué pide:* Pregunta cuántas unidades hacen falta: tamaño de muestra (y Δn si ya hay una muestra).

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Error buscado**: e = 0,689·(1 - 0,5) = 0,3445.
- Con n₁ = n₂ = n: e = fractil·√((S₁² + S₂²)/n) (ν = 2n - 2); iterando: n = 45 [46, 45, 45].

**Conclusión:** Se necesitan n = 45 en cada muestra (e = 0,3445). Hoy hay 12 de Proceso Viejo y 12 de Proceso Nuevo: faltan 33 y 33 más.

**Respuesta de la guía:** n = 45 en cada proceso, o sea 33 muestras más.

> 📝 *Notas de la transcripción:* Sin 'Resp:'; respuesta armada desde la Solución. La prueba de desvíos se hace con riesgo 10% (F(0,90;11;11)). En c) la Solución dice 'en ambas aleaciones' (arrastre de otro problema).

<details><summary>Cómo lo concluye la guía</summary>

> Proceso Viejo: nV = 12, x̄V = 5,25 p.p.b., SV = 0,9653 p.p.b.; Proceso Nuevo: nN = 12, x̄N = 1,5 p.p.b., SN = 1,0 p.p.b.
> De manera que la hipótesis no se rechaza por lo cual no se puede probar que los desvíos poblacionales sean distintos, de manera que se supone que los desvíos poblacionales son iguales.
> De manera que la hipótesis se rechaza, por lo cual se puede asegurar que el proceso nuevo ha minimizado la formación de NDMA.
> Se concluye que la diferencia entre las medias poblacionales estará comprendida entre 3,06 partes por billón y 4,44 partes por billón, afirmándolo con un 90% de confianza.
> El resultado se obtiene con n = 45. Se necesitan un total de 45 muestras, o sea que se necesitarán incluir en la experimentación realizada 33 muestras más.

</details>

---

### V-2 · Problema 2 (pág. 30)

**Enunciado.** Se desea comparar dos raciones “A” y “B” para la crianza de potrillos sangre pura de carrera a efectos de lo cual se seleccionó un conjunto de 12 potrillos machos, todos hijos de un mismo semental, para el experimento. Se eligieron 6 al azar y se les asignó la ración “A”, en tanto que a los restantes se les asignó la ración “B”. Se les suministraron las raciones durante un el mismo lapso y se registraron los siguientes aumentos de alzada en cm: Ración “A”: 1,5 – 2,5 – 3,5 – 2,0 – 3,0 – 3,5; Ración “B”: 2,5 – 2,0 – 4,5 – 4,0 – 3,5 – 4,0.

- **a)** ¿Se considera que este experimento es concluyente para poder afirmar, con probabilidad máxima de error de 0,05, que las dos raciones difieren en cuanto a la influencia en el crecimiento promedio de los potrillos?
- **b)** ¿Cómo se plantearía, a priori de los datos, la hipótesis nula apropiada si se advierte que la ración “B” es más cara que la “A” y que sólo se la adoptará si se puede asegurar, con un riesgo del 10%, que con ella la alzada media supera a la que se obtendría con “A” en 0,5 cm al menos?

*Aumentos de alzada (cm)*

| Ración | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Ración “A” | 1,5 | 2,5 | 3,5 | 2 | 3 | 3,5 |
| Ración “B” | 2,5 | 2 | 4,5 | 4 | 3,5 | 4 |

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(Ración “B”) - μ(Ración “A”) ≤ 0  vs  H1: δ = μ(Ración “B”) - μ(Ración “A”) > 0.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Ración “B”) > S(Ración “A”), lo único que se puede sospechar es σ(Ración “B”) > σ(Ración “A”) → unilateral, H0: φ = σ(Ración “B”)/σ(Ración “A”) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 5; ν₂ = 5) = √3,453 = 1,8582; J = S(Ración “B”)/S(Ración “A”) = 1,1885 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,896753; ν = n₁ + n₂ - 2 = 10.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(Ración “B”) - x̄(Ración “A”) = 0,75; σ(d) = 0,517741, ν = 10.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 0,9384. Si d > 0,9384 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 0,9384, se rechaza H0 → se puede asegurar que δ = μ(Ración “B”) - μ(Ración “A”) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Ración “B”) - μ(Ración “A”) > 0.
- **6 · Cálculos y decisión**: d = 0,75 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,089. La decisión se toma comparando el estimador con el valor crítico.
- **Orientación**: el enunciado no da dirección («¿difieren?»), pero en comparaciones no existen ensayos bilaterales: la muestra orienta el ensayo y lo único que se puede intentar probar es que μ(Ración “B”), el de mayor media muestral, supera a μ(Ración “A”).

**Conclusión:** Con α = 0,05, d = 0,75 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(Ración “B”) - μ(Ración “A”) ≤ 0. No hay evidencia suficiente para asegurar que δ = μ(Ración “B”) - μ(Ración “A”) > 0 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No, no se puede asegurar que la ración “B” aumente el crecimiento promedio de los potrillos respecto de la ración “A”.

#### b) Ensayo de hipótesis (decidir) ℹ️

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(Ración “B”) - μ(Ración “A”) ≤ 0,5  vs  H1: δ = μ(Ración “B”) - μ(Ración “A”) > 0,5.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Ración “B”) > S(Ración “A”), lo único que se puede sospechar es σ(Ración “B”) > σ(Ración “A”) → unilateral, H0: φ = σ(Ración “B”)/σ(Ración “A”) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 5; ν₂ = 5) = √3,453 = 1,8582; J = S(Ración “B”)/S(Ración “A”) = 1,1885 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,896753; ν = n₁ + n₂ - 2 = 10.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(Ración “B”) - x̄(Ración “A”) = 0,75; σ(d) = 0,517741, ν = 10.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 1,2104. Si d > 1,2104 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 1,2104, se rechaza H0 → se puede asegurar que δ = μ(Ración “B”) - μ(Ración “A”) > 0,5. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Ración “B”) - μ(Ración “A”) > 0,5.
- **6 · Cálculos y decisión**: d = 0,75 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,3198. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,1, d = 0,75 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(Ración “B”) - μ(Ración “A”) ≤ 0,5. No hay evidencia suficiente para asegurar que δ = μ(Ración “B”) - μ(Ración “A”) > 0,5 (no rechazar H0 no la prueba).

**Respuesta de la guía:** H0: μB ≤ μA + 0,5 cm; o H0: δ ≤ 0,5 cm, para δ = μB − μA y α = 0,10.

> 📝 *Notas de la transcripción:* El inciso a) pregunta si las raciones 'difieren' (bilateral) pero la Resp habla de que 'B' aumente el crecimiento respecto de 'A' (unilateral).

---

### V-3 · Problema 3 (pág. 30)

**Enunciado.** En una hilandería se considera la posibilidad de reacondicionar a nuevo las hiladoras, si es posible asegurar con el reacondicionamiento, con un riesgo máximo del 5%, un aumento estadísticamente discernible en la producción media por máquina. Se eligieron entonces 4 máquinas al azar y se las reacondicionó, registrándose luego la producción de cada una para un período dado; se obtuvo así una media de 1.470 metros de hilado con un desvío estándar de 132 metros. Como se desconocía la producción de las máquinas sin reacondicionar, se registró la producción de 16 de ellas en el mismo período, obteniéndose una media de 1.208 metros con un desvío de 354 metros. Tener en cuenta las conclusiones obtenidas en el problema 4 del tema anterior de la presente guía (página 28).

- **a)** ¿Se puede aconsejar, con un riesgo máximo del 5%, el reacondicionamiento de todas las máquinas?
- **b)** Calcular los límites de confianza del 90% para la diferencia entre las producciones medias.
- **c)** Si se considera tomar una muestra igual de máquinas reacondicionadas y de máquinas sin reacondicionamiento, ¿Cuántas máquinas se deberían observar en el período dado para reducir a la mitad el error de estimación anterior?
- **d)** Con los datos iniciales, ¿qué diferencia mínima porcentual se puede garantizar, para las máquinas reacondicionadas, con un 5% de riesgo?

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(reacondicionadas) - μ(sin reacondicionar) ≤ 0  vs  H1: δ = μ(reacondicionadas) - μ(sin reacondicionar) > 0.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(sin reacondicionar) > S(reacondicionadas), lo único que se puede sospechar es σ(sin reacondicionar) > σ(reacondicionadas) → unilateral, H0: φ = σ(sin reacondicionar)/σ(reacondicionadas) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 15; ν₂ = 3) = √5,2003 = 2,2804; J = S(sin reacondicionar)/S(reacondicionadas) = 2,6818 → J > Jc: se rechaza H0 → los desvíos son DISTINTOS → Welch.
- ν de Aspin-Welch = (S₁²/n₁ + S₂²/n₂)²/[(S₁²/n₁)²/(n₁-1) + (S₂²/n₂)²/(n₂-1)] = 14,2641 → ν = 14.
- Diferencia observada (t de Welch (desvíos distintos)): d = x̄(reacondicionadas) - x̄(sin reacondicionar) = 262; σ(d) = 110,400408, ν = 14.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 194,4494. Si d > 194,4494 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 194,4494, se rechaza H0 → se puede asegurar que δ = μ(reacondicionadas) - μ(sin reacondicionar) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(reacondicionadas) - μ(sin reacondicionar) > 0.
- **6 · Cálculos y decisión**: d = 262 → se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,0162. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,05, d = 262 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: δ = μ(reacondicionadas) - μ(sin reacondicionar) ≤ 0. Se puede asegurar que δ = μ(reacondicionadas) - μ(sin reacondicionar) > 0.

**Respuesta de la guía:** Desvíos: H0: σSR ≤ σCR (φ = σSR/σCR, H0: φ ≤ φ0 = 1), jc = 2,2804 (j²c = 5,2003), j = 2,6818 (j² = 7,1922): se rechaza, los desvíos son distintos (Welch, νaw = 14,2641 → 14). Medias: H0: μCR ≤ μSR (δ = μCR − μSR, H0: δ ≤ δ0 = 0), dc = 194,4494 m, d = 1.470 − 1.208 = 262 m. Se rechaza la hipótesis: las máquinas reacondicionadas tienen una producción promedio mayor; se aconseja el reacondicionamiento de todas las máquinas.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Pide estimar el parámetro: intervalo de confianza P(A ≤ θ ≤ B) = 1-α.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Modelo**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(sin reacondicionar) > S(reacondicionadas), lo único que se puede sospechar es σ(sin reacondicionar) > σ(reacondicionadas) → unilateral, H0: φ = σ(sin reacondicionar)/σ(reacondicionadas) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 15; ν₂ = 3) = √5,2003 = 2,2804; J = S(sin reacondicionar)/S(reacondicionadas) = 2,6818 → J > Jc: se rechaza H0 → los desvíos son DISTINTOS → Welch.
- ν de Aspin-Welch = (S₁²/n₁ + S₂²/n₂)²/[(S₁²/n₁)²/(n₁-1) + (S₂²/n₂)²/(n₂-1)] = 14,2641 → ν = 14.
- **IC para δ = μ(reacondicionadas) - μ(sin reacondicionar)** (t de Welch (desvíos distintos)): d = 262; e = t(0,95; 14)·σ(d) = 1,7613·110,400408 = 194,4494.

**Conclusión:** P(67,55 ≤ μ(reacondicionadas) - μ(sin reacondicionar) ≤ 456,45) = 0,9 (e = 194,4494). Para μ(sin reacondicionar) - μ(reacondicionadas): entre -456,45 y -67,55. Límites redondeados hacia afuera; sin redondear: 67,550643 y 456,449357.

**Respuesta de la guía:** Entre 67,55 metros y 456,45 metros (δ = μCR − μSR; 262 ± 194,4482), con un error de muestreo e = 194,4482.

> ≈ Coincide solo aproximadamente (194,4482): Errata de la guía: imprime e = 194,4494 en a) y 194,4482 en b); los límites (67,55 y 456,45) coinciden.

#### c) Tamaño de muestra ✅

*Qué pide:* Pregunta cuántas unidades hacen falta: tamaño de muestra (y Δn si ya hay una muestra).

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Error buscado**: e = 194,4494·(1 - 0,5) = 97,2247.
- Con n₁ = n₂ = n: e = fractil·√((S₁² + S₂²)/n) (ν de Welch con n₁ = n₂ = n); iterando: n = 43 [44, 43, 43].

**Conclusión:** Se necesitan n = 43 en cada muestra (e = 97,2247). Hoy hay 4 de reacondicionadas y 16 de sin reacondicionar: faltan 39 y 27 más.

**Respuesta de la guía:** n = 43 máquinas de cada tipo (e = 97,2247 m), o sea 39 máquinas reacondicionadas más y 27 máquinas sin reacondicionar más.

#### d) Intervalo de confianza (estimar) ✅

*Qué pide:* Pide un valor máximo / mínimo del parámetro con cierta confianza: límite de confianza UNILATERAL.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Modelo**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(sin reacondicionar) > S(reacondicionadas), lo único que se puede sospechar es σ(sin reacondicionar) > σ(reacondicionadas) → unilateral, H0: φ = σ(sin reacondicionar)/σ(reacondicionadas) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 15; ν₂ = 3) = √5,2003 = 2,2804; J = S(sin reacondicionar)/S(reacondicionadas) = 2,6818 → J > Jc: se rechaza H0 → los desvíos son DISTINTOS → Welch.
- ν de Aspin-Welch = (S₁²/n₁ + S₂²/n₂)²/[(S₁²/n₁)²/(n₁-1) + (S₂²/n₂)²/(n₂-1)] = 14,2641 → ν = 14.
- **Relación mínima garantizada** h = μ(reacondicionadas)/μ(sin reacondicionar) (h es una constante, no un parámetro: no se estima): es el h que deja en el límite la condición de rechazo de H0: μ(reacondicionadas) ≤ h·μ(sin reacondicionar) con α = 0,05 (un solo límite: α entero).
- Con Welch ν depende de h (h² entra también en ν), así que se resuelve iterando: x̄(reacondicionadas) - h·x̄(sin reacondicionar) = t(1-α; ν(h))·σ(d*(h)) → h = 1,0506.

**Conclusión:** Con un 95% de confianza, μ(reacondicionadas) es como mínimo un 5,06% mayor que μ(sin reacondicionar) (h = 1,0506).

**Respuesta de la guía:** h = 1,0506: el incremento porcentual mínimo garantizado es del 5,06%.

> 📝 *Notas de la transcripción:* Sin 'Resp:'; respuesta armada desde la Solución. El valor crítico de a) es 194,4494 m mientras que el error de b) es 194,4482 (misma expresión 1,7613·√(132²/4+354²/16)); diferencia de redondeo en la guía. El enunciado remite al problema 4 del Tema IV 'página 28' (empieza en la 27).

<details><summary>Cómo lo concluye la guía</summary>

> De manera que la hipótesis se rechaza por lo cual se puede probar que los desvíos poblacionales son distintos.
> De manera que la hipótesis se rechaza, por lo cual se puede asegurar que las máquinas reacondicionadas tienen una producción promedio mayor que las máquinas sin reacondicionar. Por lo cual se aconseja el reacondicionamiento de todas las máquinas.
> Se concluye que la diferencia entre las medias poblacionales estará comprendida entre 67,55 metros y 456,45 metros, afirmándolo con un 90% de confianza.
> El resultado se obtiene con n = 43. Se necesitan un total de 43 máquinas de cada tipo, o sea que se necesitarán incluir en la observación realizada 39 máquinas reacondicionadas más y 27 máquinas sin reacondicionar más.
> Se puede estipular que el incremento porcentual mínimo garantizado de las máquinas con reacondicionamiento respecto de las máquinas sin reacondicionamiento es del 5,06%.

</details>

---

### V-4 · Problema 4 (pág. 32)

**Enunciado.** Se desea estudiar la efectividad de un nuevo aditivo para combustible, a efectos de lo cual se realizó una prueba sobre 10 corridas en distintos automóviles que arrojaron un consumo medio de 4,2 litros con un desvío estándar de 0,58 litros. Además, se efectuó una prueba similar, también sobre 10 corridas, con otros automóviles de la misma marca y modelo y el mismo trayecto, pero sin el aditivo, obteniéndose un consumo medio de 5,25 litros con un desvío de 0,63 litros.

- **a)** ¿Se puede asegurar que el aditivo reduce el consumo medio en 0,5 litros al menos para el recorrido dado?
- **b)** ¿Se puede asegurar que el aditivo reduce el consumo medio en un 10% al menos para el recorrido dado?

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(con aditivo) - μ(sin aditivo) ≥ -0,5  vs  H1: δ = μ(con aditivo) - μ(sin aditivo) < -0,5.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(sin aditivo) > S(con aditivo), lo único que se puede sospechar es σ(sin aditivo) > σ(con aditivo) → unilateral, H0: φ = σ(sin aditivo)/σ(con aditivo) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 9; ν₂ = 9) = √2,4403 = 1,5622; J = S(sin aditivo)/S(con aditivo) = 1,0862 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,605516; ν = n₁ + n₂ - 2 = 18.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(con aditivo) - x̄(sin aditivo) = -1,05; σ(d) = 0,270795, ν = 18.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ - t·σ(d) = -0,9696. Si d < -0,9696 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d < -0,9696, se rechaza H0 → se puede asegurar que δ = μ(con aditivo) - μ(sin aditivo) < -0,5. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(con aditivo) - μ(sin aditivo) < -0,5.
- **6 · Cálculos y decisión**: d = -1,05 → se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,0286. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,05, d = -1,05 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: δ = μ(con aditivo) - μ(sin aditivo) ≥ -0,5. Se puede asegurar que δ = μ(con aditivo) - μ(sin aditivo) < -0,5.

**Respuesta de la guía:** Se puede asegurar que el aditivo reduce el consumo de combustible en más de 0,5 litros.

#### b) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: μ(con aditivo) ≥ 0,9·μ(sin aditivo) (δ* = μ(con aditivo) - 0,9·μ(sin aditivo) ≥ 0)  vs  H1: μ(con aditivo) < 0,9·μ(sin aditivo).
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(sin aditivo) > S(con aditivo), lo único que se puede sospechar es σ(sin aditivo) > σ(con aditivo) → unilateral, H0: φ = σ(sin aditivo)/σ(con aditivo) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 9; ν₂ = 9) = √2,4403 = 1,5622; J = S(sin aditivo)/S(con aditivo) = 1,0862 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,605516; ν = n₁ + n₂ - 2 = 18.
- Diferencia observada (t con Sa (desvíos iguales)): d* = x̄(con aditivo) - 0,9·x̄(sin aditivo) = -0,525; σ(d*) = 0,257611, ν = 18.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ - t·σ(d) = -0,4467. Si d < -0,4467 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d < -0,4467, se rechaza H0 → se puede asegurar que μ(con aditivo) < 0,9·μ(sin aditivo). En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ(con aditivo) < 0,9·μ(sin aditivo).
- **6 · Cálculos y decisión**: d = -0,525 → se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,0283. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,05, d = -0,525 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: μ(con aditivo) ≥ 0,9·μ(sin aditivo) (δ* = μ(con aditivo) - 0,9·μ(sin aditivo) ≥ 0). Se puede asegurar que μ(con aditivo) < 0,9·μ(sin aditivo).

**Respuesta de la guía:** Se puede asegurar que el aditivo reduce el consumo de combustible en más del 10%.

> 📝 *Notas de la transcripción:* El enunciado no indica el riesgo α a utilizar.

---

### V-5 · Problema 5 (pág. 32)

**Enunciado.** Se desea comparar la efectividad para el engorde de novillos de dos variedades de cebada forrajera como pastoreo, a efectos de lo cual se seleccionó un lote lo más parejo posible, dividiéndolo en dos grupos de 15 animales cada uno, que se pastorearon durante el mismo lapso de tiempo en potreros sembrados con dichas variedades, registrándose los aumentos de peso en kg de todos los novillos, datos que, luego de procesados, arrojaron los siguientes resultados: Variedad “A”: Promedio (x̄) = 25 kg, Desvío std. (S) = 3,4 kg; Variedad “B”: Promedio (x̄) = 26,2 kg, Desvío std. (S) = 2,8 kg.

- **a)** ¿Considera que estos datos son concluyentes al 5% de riesgo?
- **b)** ¿Cuál es la diferencia de aumento de peso mínima que puede garantizarse para la variedad “B” con 5% de riesgo?

|  | Promedio (x̄) | Desvío std. (S) |
|---|---|---|
| Variedad “A” | 25 kg | 3,4 kg |
| Variedad “B” | 26,2 kg | 2,8 kg |

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(Variedad “B”) - μ(Variedad “A”) ≤ 0  vs  H1: δ = μ(Variedad “B”) - μ(Variedad “A”) > 0.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Variedad “A”) > S(Variedad “B”), lo único que se puede sospechar es σ(Variedad “A”) > σ(Variedad “B”) → unilateral, H0: φ = σ(Variedad “A”)/σ(Variedad “B”) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 14; ν₂ = 14) = √2,0224 = 1,4221; J = S(Variedad “A”)/S(Variedad “B”) = 1,2143 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 3,114482; ν = n₁ + n₂ - 2 = 28.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(Variedad “B”) - x̄(Variedad “A”) = 1,2; σ(d) = 1,137248, ν = 28.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 1,9346. Si d > 1,9346 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 1,9346, se rechaza H0 → se puede asegurar que δ = μ(Variedad “B”) - μ(Variedad “A”) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Variedad “B”) - μ(Variedad “A”) > 0.
- **6 · Cálculos y decisión**: d = 1,2 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,1502. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,05, d = 1,2 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(Variedad “B”) - μ(Variedad “A”) ≤ 0. No hay evidencia suficiente para asegurar que δ = μ(Variedad “B”) - μ(Variedad “A”) > 0 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No se puede asegurar que la variedad “B” sea más efectiva para el engorde promedio de los novillos que la variedad “A”.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Pide un valor máximo / mínimo del parámetro con cierta confianza: límite de confianza UNILATERAL.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Modelo**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Variedad “A”) > S(Variedad “B”), lo único que se puede sospechar es σ(Variedad “A”) > σ(Variedad “B”) → unilateral, H0: φ = σ(Variedad “A”)/σ(Variedad “B”) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 14; ν₂ = 14) = √2,0224 = 1,4221; J = S(Variedad “A”)/S(Variedad “B”) = 1,2143 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 3,114482; ν = n₁ + n₂ - 2 = 28.
- **Límite para δ = μ(Variedad “B”) - μ(Variedad “A”)** (t con Sa (desvíos iguales)): d = 1,2; e = t(0,95; 28)·σ(d) = 1,7011·1,137248 = 1,9346.

**Conclusión:** Con un 95% de confianza, μ(Variedad “B”) - μ(Variedad “A”) ≥ -0,735: la diferencia mínima garantizada para Variedad “B” es -0,735 (redondeada hacia abajo; sin redondear -0,734608).

**Respuesta de la guía:** (− 0,73) kg, se estima que la variedad “A” puede engordar más que la “B” en 0,73 kg.

---

### V-6 · Problema 6 (pág. 32)

**Enunciado.** Se tienen dos enconadoras de hilo de coser cuyas producciones se desean comparar. Para realizar dicha comparación, se realizó un experimento en el que se midió la cantidad de metros de hilo enconados, en ambas máquinas, durante el mismo lapso de tiempo (n = 90 días), obteniéndose los resultados de la siguiente tabla (en miles de km). Se tiene la presunción, no la certeza, de que los desvíos de ambas enconadoras son iguales. Hilo (en miles de km) : Cant. días observados de Máquina “A” | Hilo (en miles de km) : Cant. días observados de Máquina “B”: 1,2 – 1,3: 8 | 1,6 – 1,7: 8; 1,3 – 1,4: 12 | 1,7 – 1,8: 13; 1,4 – 1,5: 14 | 1,8 – 1,9: 14; 1,5 – 1,6: 26 | 1,9 – 2,0: 30; 1,6 – 1,7: 19 | 2,0 – 2,1: 10; 1,7 – 1,8: 8 | 2,1 – 2,2: 9; 1,8 – 1,9: 3 | 2,2 – 2,3: 6.

- **a)** ¿Se puede asegurar que con la máquina “B” se obtiene como mínimo una producción superior en 100 km respecto de la máquina “A”?
- **b)** ¿Se puede asegurar que con la máquina “B” se obtiene como mínimo una producción superior en un 24% que con la máquina “A”?
- **c)** ¿Cuál es la diferencia de producción mínima, en miles de km, que se puede garantizar para la máquina “B” con un 5% de riesgo?
- **d)** ¿Qué diferencia porcentual mínima se puede garantizar para la máquina “B” con un 5% de riesgo?

*Producción de hilo (en miles de km)*

| Hilo (en miles de km) | Cant. días observados de Máquina “A” | Hilo (en miles de km) | Cant. días observados de Máquina “B” |
|---|---|---|---|
| 1,2 – 1,3 | 8 | 1,6 – 1,7 | 8 |
| 1,3 – 1,4 | 12 | 1,7 – 1,8 | 13 |
| 1,4 – 1,5 | 14 | 1,8 – 1,9 | 14 |
| 1,5 – 1,6 | 26 | 1,9 – 2,0 | 30 |
| 1,6 – 1,7 | 19 | 2,0 – 2,1 | 10 |
| 1,7 – 1,8 | 8 | 2,1 – 2,2 | 9 |
| 1,8 – 1,9 | 3 | 2,2 – 2,3 | 6 |

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

> ⚠️ El enunciado no fija el riesgo α: se eligió α = 0,05. En el examen hay que elegirlo y JUSTIFICARLO antes de ver la muestra (p. ej. «0,05, no porque sea estándar, sino porque el perito tiene que ser imparcial»); una vez fijado, α no se toca. El valor a posteriori α* se muestra solo como dato: no se decide con él.

- **1 · Planteo de hipótesis**: H0: δ = μ(Máquina “B”) - μ(Máquina “A”) ≤ 0,1  vs  H1: δ = μ(Máquina “B”) - μ(Máquina “A”) > 0,1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Máquina “B”) > S(Máquina “A”), lo único que se puede sospechar es σ(Máquina “B”) > σ(Máquina “A”) → unilateral, H0: φ = σ(Máquina “B”)/σ(Máquina “A”) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 89; ν₂ = 89) = √1,3137 = 1,1462; J = S(Máquina “B”)/S(Máquina “A”) = 1,0605 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,157723; ν = n₁ + n₂ - 2 = 178.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(Máquina “B”) - x̄(Máquina “A”) = 0,4; σ(d) = 0,023512, ν = 178.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 0,1389. Si d > 0,1389 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 0,1389, se rechaza H0 → se puede asegurar que δ = μ(Máquina “B”) - μ(Máquina “A”) > 0,1. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Máquina “B”) - μ(Máquina “A”) > 0,1.
- **6 · Cálculos y decisión**: d = 0,4 → se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,05, d = 0,4 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: δ = μ(Máquina “B”) - μ(Máquina “A”) ≤ 0,1. Se puede asegurar que δ = μ(Máquina “B”) - μ(Máquina “A”) > 0,1.

**Respuesta de la guía:** Desvíos: H0: σB ≤ σA (φ = σB/σA), jc = 1,1462 (j²c = 1,3137), j = 1,0605 (j² = 1,1248): no se rechaza, se amalgama Sa = 0,157723 miles de km, ν = 178. H0: μB ≤ μA + 0,100 (δ0 = 0,100), dc = 0,1389 miles de km, d = 1,93 − 1,53 = 0,40 miles de km. Se rechaza la hipótesis: se puede asegurar que la máquina “B” produce en promedio 100 km más que la máquina “A”.

#### b) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

> ⚠️ El enunciado no fija el riesgo α: se eligió α = 0,05. En el examen hay que elegirlo y JUSTIFICARLO antes de ver la muestra (p. ej. «0,05, no porque sea estándar, sino porque el perito tiene que ser imparcial»); una vez fijado, α no se toca. El valor a posteriori α* se muestra solo como dato: no se decide con él.

- **1 · Planteo de hipótesis**: H0: μ(Máquina “B”) ≤ 1,24·μ(Máquina “A”) (δ* = μ(Máquina “B”) - 1,24·μ(Máquina “A”) ≤ 0)  vs  H1: μ(Máquina “B”) > 1,24·μ(Máquina “A”).
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Máquina “B”) > S(Máquina “A”), lo único que se puede sospechar es σ(Máquina “B”) > σ(Máquina “A”) → unilateral, H0: φ = σ(Máquina “B”)/σ(Máquina “A”) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 89; ν₂ = 89) = √1,3137 = 1,1462; J = S(Máquina “B”)/S(Máquina “A”) = 1,0605 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,157723; ν = n₁ + n₂ - 2 = 178.
- Diferencia observada (t con Sa (desvíos iguales)): d* = x̄(Máquina “B”) - 1,24·x̄(Máquina “A”) = 0,0328; σ(d*) = 0,026484, ν = 178.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 0,0438. Si d > 0,0438 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 0,0438, se rechaza H0 → se puede asegurar que μ(Máquina “B”) > 1,24·μ(Máquina “A”). En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ(Máquina “B”) > 1,24·μ(Máquina “A”).
- **6 · Cálculos y decisión**: d = 0,0328 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,1086. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,05, d = 0,0328 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ(Máquina “B”) ≤ 1,24·μ(Máquina “A”) (δ* = μ(Máquina “B”) - 1,24·μ(Máquina “A”) ≤ 0). No hay evidencia suficiente para asegurar que μ(Máquina “B”) > 1,24·μ(Máquina “A”) (no rechazar H0 no la prueba).

**Respuesta de la guía:** H0: μB ≤ 1,24·μA (δ* = μB − 1,24·μA ≤ 0), d*c = 0,0438 miles de km, d* = 1,93 − 1,24·1,53 = 0,0328 miles de km. No se rechaza: no se puede asegurar que la máquina “B” produzca en promedio un 24% más que la máquina “A”.

#### c) Intervalo de confianza (estimar) ✅

*Qué pide:* Pide un valor máximo / mínimo del parámetro con cierta confianza: límite de confianza UNILATERAL.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Modelo**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Máquina “B”) > S(Máquina “A”), lo único que se puede sospechar es σ(Máquina “B”) > σ(Máquina “A”) → unilateral, H0: φ = σ(Máquina “B”)/σ(Máquina “A”) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 89; ν₂ = 89) = √1,3137 = 1,1462; J = S(Máquina “B”)/S(Máquina “A”) = 1,0605 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,157723; ν = n₁ + n₂ - 2 = 178.
- **Límite para δ = μ(Máquina “B”) - μ(Máquina “A”)** (t con Sa (desvíos iguales)): d = 0,4; e = t(0,95; 178)·σ(d) = 1,6535·0,023512 = 0,0389.

**Conclusión:** Con un 95% de confianza, μ(Máquina “B”) - μ(Máquina “A”) ≥ 0,361: la diferencia mínima garantizada para Máquina “B” es 0,361 (redondeada hacia abajo; sin redondear 0,361124).

**Respuesta de la guía:** A = 0,361124 miles de km: la diferencia mínima es 0,361124 miles de km (361,12 km) con 95% de confianza.

#### d) Intervalo de confianza (estimar) ✅

*Qué pide:* Pide un valor máximo / mínimo del parámetro con cierta confianza: límite de confianza UNILATERAL.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Modelo**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Máquina “B”) > S(Máquina “A”), lo único que se puede sospechar es σ(Máquina “B”) > σ(Máquina “A”) → unilateral, H0: φ = σ(Máquina “B”)/σ(Máquina “A”) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 89; ν₂ = 89) = √1,3137 = 1,1462; J = S(Máquina “B”)/S(Máquina “A”) = 1,0605 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,157723; ν = n₁ + n₂ - 2 = 178.
- **Relación mínima garantizada** h = μ(Máquina “B”)/μ(Máquina “A”) (h es una constante, no un parámetro: no se estima): es el h que deja en el límite la condición de rechazo de H0: μ(Máquina “B”) ≤ h·μ(Máquina “A”) con α = 0,05 (un solo límite: α entero).
- **Inecuación en h**: x̄₁ - h·x̄₂ > t(1-α; 178)·Sa·√(1/n₁ + h²/n₂) (h² va en el término de la población que lleva h). Con 1,93 - 1,53·h y fractil 1,6535, al elevar al cuadrado: 2,3401·h² - 5,9058·h + 3,7241 = 0 → raíces h = 1,2329 y h = 1,2908. Verificación en la inecuación original: h = 1,2329: x̄₁ - h·x̄₂ = 0,0436; sirve (es raíz de la igualdad original). h = 1,2908: x̄₁ - h·x̄₂ = -0,0449; NO sirve (el lado izquierdo es negativo y no puede igualar a +0,0449).

**Conclusión:** Con un 95% de confianza, μ(Máquina “B”) es como mínimo un 23,29% mayor que μ(Máquina “A”) (h = 1,2329).

**Respuesta de la guía:** h = 1,2329: el incremento porcentual mínimo garantizado de la máquina “B” respecto de la “A” es del 23,29%.

> 📝 *Notas de la transcripción:* Sin 'Resp:'; respuesta armada desde la Solución. El enunciado no fija α para a) y b); la Solución usa 5% (y 10% para la prueba de desvíos).

<details><summary>Cómo lo concluye la guía</summary>

> Máquina “A”: nA = 90; x̄A = 1,53 miles de km; SA = 0,153022 miles de km. Máquina “B”: nB = 90; x̄B = 1,93 miles de km; SB = 0,162287 miles de km.
> De manera que la hipótesis no se rechaza por lo cual no se puede probar que los desvíos poblacionales son distintos.
> De manera que la hipótesis se rechaza, por lo cual se puede asegurar que la máquina “B” produce en promedio 100 km más que la máquina “A”.
> De manera que la hipótesis no se rechaza, por lo cual no se puede asegurar que la máquina “B” produzca en promedio un 24% más que la máquina “A”.
> Se concluye que la diferencia mínima entre las medias poblacionales será 0,361124 miles de km, afirmándolo con un 95% de confianza. Quiere decir que con la máquina “B” se puede esperar una producción promedio mínima de 361,12 km respecto de la máquina “A”.
> Se puede estipular que el incremento porcentual mínimo garantizado de la máquina “B” respecto de la máquina “A” es del 23,29%.

</details>

---

### V-7 · Problema 7 (pág. 34)

**Enunciado.** Se ha desarrollado una nueva variedad de maíz híbrido que tendrá un costo de producción mayor que la variedad actual. Para efectuar la comparación se sembraron 10 parcelas al azar con cada variedad, obteniéndose los siguientes rendimientos en quintales por parcela: Variedad Actual (A): Promedio (x̄) = 15,2, Desvío std. (S) = 1,63; Variedad Nueva (N): Promedio (x̄) = 17,1, Desvío std. (S) = 1,43. Para lanzar el nuevo producto al mercado, se desea tener un 95% de seguridad de que el rendimiento medio de la variedad nueva supera en un 10%, al menos, al de la variedad actual.

*Establecer la hipótesis nula apropiada, efectuar el ensayo e indicar la decisión a tomar.*

|  | Promedio (x̄) | Desvío std. (S) |
|---|---|---|
| Variedad Actual (A) | 15,2 | 1,63 |
| Variedad Nueva (N) | 17,1 | 1,43 |

*Tema detectado por la app: Comparación de 2 medias.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: μ(Variedad Nueva (N)) ≤ 1,1·μ(Variedad Actual (A)) (δ* = μ(Variedad Nueva (N)) - 1,1·μ(Variedad Actual (A)) ≤ 0)  vs  H1: μ(Variedad Nueva (N)) > 1,1·μ(Variedad Actual (A)).
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Variedad Actual (A)) > S(Variedad Nueva (N)), lo único que se puede sospechar es σ(Variedad Actual (A)) > σ(Variedad Nueva (N)) → unilateral, H0: φ = σ(Variedad Actual (A))/σ(Variedad Nueva (N)) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 9; ν₂ = 9) = √2,4403 = 1,5622; J = S(Variedad Actual (A))/S(Variedad Nueva (N)) = 1,1399 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 1,533264; ν = n₁ + n₂ - 2 = 18.
- Diferencia observada (t con Sa (desvíos iguales)): d* = x̄(Variedad Nueva (N)) - 1,1·x̄(Variedad Actual (A)) = 0,38; σ(d*) = 0,720797, ν = 18.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 1,2499. Si d > 1,2499 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 1,2499, se rechaza H0 → se puede asegurar que μ(Variedad Nueva (N)) > 1,1·μ(Variedad Actual (A)). En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ(Variedad Nueva (N)) > 1,1·μ(Variedad Actual (A)).
- **6 · Cálculos y decisión**: d = 0,38 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,3022. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,05, d = 0,38 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ(Variedad Nueva (N)) ≤ 1,1·μ(Variedad Actual (A)) (δ* = μ(Variedad Nueva (N)) - 1,1·μ(Variedad Actual (A)) ≤ 0). No hay evidencia suficiente para asegurar que μ(Variedad Nueva (N)) > 1,1·μ(Variedad Actual (A)) (no rechazar H0 no la prueba).

**Respuesta de la guía:** H0: μN ≤ 1,10·μA; o H0: δ* ≤ 0, no se recomienda el uso de la nueva variedad de maíz, no se puede asegurar que la variedad nueva supere a la actual en más de un 10%.

---

### V-8 · Problema 8 (pág. 34)

**Enunciado.** Se realizó un experimento para probar la eficacia de un aditivo en la fórmula de un tipo de látex, que se espera aumente la resistencia media a la tracción del producto. Se realizaron 21 ensayos con el aditivo, que arrojaron una resistencia media de 8,5 kg con un desvío estándar de 1,2 kg. Con respecto al comportamiento del producto sin el aditivo, jamás se había realizado un experimento para analizarlo, razón por la cual se aprovechó la oportunidad y se realizaron 61 ensayos que arrojaron una resistencia media de 7,6 kg, con un desvío estándar de 1,25 kg.

- **a)** ¿Aseguraría, con 5% de riesgo de equivocarse, que el aditivo aumenta la resistencia media en 0,45 kg al menos?
- **b)** ¿Cuál es la diferencia mínima en la resistencia media que se obtiene con el aditivo, con 95% de confianza?
- **c)** ¿Aseguraría, con 5% de riesgo de equivocarse, que el aditivo aumenta la resistencia media en un 10% al menos?
- **d)** ¿Cuál es el porcentaje mínimo de aumento en la resistencia media que se obtiene con el aditivo con 95% de confianza?

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pregunta si hay un efecto (aumenta / reduce / influye): ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(con aditivo) - μ(sin aditivo) ≤ 0,45  vs  H1: δ = μ(con aditivo) - μ(sin aditivo) > 0,45.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(sin aditivo) > S(con aditivo), lo único que se puede sospechar es σ(sin aditivo) > σ(con aditivo) → unilateral, H0: φ = σ(sin aditivo)/σ(con aditivo) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 60; ν₂ = 20) = √1,6768 = 1,2949; J = S(sin aditivo)/S(con aditivo) = 1,0417 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 1,237689; ν = n₁ + n₂ - 2 = 80.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(con aditivo) - x̄(sin aditivo) = 0,9; σ(d) = 0,313144, ν = 80.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 0,9711. Si d > 0,9711 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 0,9711, se rechaza H0 → se puede asegurar que δ = μ(con aditivo) - μ(sin aditivo) > 0,45. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(con aditivo) - μ(sin aditivo) > 0,45.
- **6 · Cálculos y decisión**: d = 0,9 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,0773. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,05, d = 0,9 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(con aditivo) - μ(sin aditivo) ≤ 0,45. No hay evidencia suficiente para asegurar que δ = μ(con aditivo) - μ(sin aditivo) > 0,45 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No se puede asegurar que el aditivo aumente la resistencia en 0,45 kg como mínimo.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Pide un valor máximo / mínimo del parámetro con cierta confianza: límite de confianza UNILATERAL.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Modelo**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(sin aditivo) > S(con aditivo), lo único que se puede sospechar es σ(sin aditivo) > σ(con aditivo) → unilateral, H0: φ = σ(sin aditivo)/σ(con aditivo) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 60; ν₂ = 20) = √1,6768 = 1,2949; J = S(sin aditivo)/S(con aditivo) = 1,0417 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 1,237689; ν = n₁ + n₂ - 2 = 80.
- **Límite para δ = μ(con aditivo) - μ(sin aditivo)** (t con Sa (desvíos iguales)): d = 0,9; e = t(0,95; 80)·σ(d) = 1,6641·0,313144 = 0,5211.

**Conclusión:** Con un 95% de confianza, μ(con aditivo) - μ(sin aditivo) ≥ 0,378: la diferencia mínima garantizada para con aditivo es 0,378 (redondeada hacia abajo; sin redondear 0,378889).

**Respuesta de la guía:** 0,3788 kg, el aditivo puede aumentar la resistencia del látex en 0,3788 kg.

#### c) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pregunta si hay un efecto (aumenta / reduce / influye): ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: μ(con aditivo) ≤ 1,1·μ(sin aditivo) (δ* = μ(con aditivo) - 1,1·μ(sin aditivo) ≤ 0)  vs  H1: μ(con aditivo) > 1,1·μ(sin aditivo).
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(sin aditivo) > S(con aditivo), lo único que se puede sospechar es σ(sin aditivo) > σ(con aditivo) → unilateral, H0: φ = σ(sin aditivo)/σ(con aditivo) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 60; ν₂ = 20) = √1,6768 = 1,2949; J = S(sin aditivo)/S(con aditivo) = 1,0417 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 1,237689; ν = n₁ + n₂ - 2 = 80.
- Diferencia observada (t con Sa (desvíos iguales)): d* = x̄(con aditivo) - 1,1·x̄(sin aditivo) = 0,14; σ(d*) = 0,321454, ν = 80.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 0,5349. Si d > 0,5349 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 0,5349, se rechaza H0 → se puede asegurar que μ(con aditivo) > 1,1·μ(sin aditivo). En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ(con aditivo) > 1,1·μ(sin aditivo).
- **6 · Cálculos y decisión**: d = 0,14 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,3322. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,05, d = 0,14 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ(con aditivo) ≤ 1,1·μ(sin aditivo) (δ* = μ(con aditivo) - 1,1·μ(sin aditivo) ≤ 0). No hay evidencia suficiente para asegurar que μ(con aditivo) > 1,1·μ(sin aditivo) (no rechazar H0 no la prueba).

**Respuesta de la guía:** No se puede asegurar que el aditivo aumente la resistencia en un 10% como mínimo.

#### d) Intervalo de confianza (estimar) ✅

*Qué pide:* Pide un valor máximo / mínimo del parámetro con cierta confianza: límite de confianza UNILATERAL.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Modelo**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(sin aditivo) > S(con aditivo), lo único que se puede sospechar es σ(sin aditivo) > σ(con aditivo) → unilateral, H0: φ = σ(sin aditivo)/σ(con aditivo) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 60; ν₂ = 20) = √1,6768 = 1,2949; J = S(sin aditivo)/S(con aditivo) = 1,0417 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 1,237689; ν = n₁ + n₂ - 2 = 80.
- **Relación mínima garantizada** h = μ(con aditivo)/μ(sin aditivo) (h es una constante, no un parámetro: no se estima): es el h que deja en el límite la condición de rechazo de H0: μ(con aditivo) ≤ h·μ(sin aditivo) con α = 0,05 (un solo límite: α entero).
- **Inecuación en h**: x̄₁ - h·x̄₂ > t(1-α; 80)·Sa·√(1/n₁ + h²/n₂) (h² va en el término de la población que lleva h). Con 8,5 - 7,6·h y fractil 1,6641, al elevar al cuadrado: 57,6905·h² - 129,2·h + 72,048 = 0 → raíces h = 1,0490 y h = 1,1906. Verificación en la inecuación original: h = 1,0490: x̄₁ - h·x̄₂ = 0,5278; sirve (es raíz de la igualdad original). h = 1,1906: x̄₁ - h·x̄₂ = -0,5483; NO sirve (el lado izquierdo es negativo y no puede igualar a +0,5483).

**Conclusión:** Con un 95% de confianza, μ(con aditivo) es como mínimo un 4,90% mayor que μ(sin aditivo) (h = 1,0490).

**Respuesta de la guía:** El incremento porcentual mínimo es del 4,90%.

---

### V-9 · Problema 9 (pág. 34)

**Enunciado.** Se realizó un experimento para comparar dos marcas de máquinas cosechadoras, John Deere y Vasalli, se han tomado 5 máquinas elegidas al azar de cada marca y se registraron los volúmenes cosechados en toneladas durante un día, con los siguientes resultados: John Deere (JD): 3,2 – 2,8 – 2,4 – 3,6 – 2,7; Vasalli (V): 2,5 – 2,2 – 3,7 – 2,1 – 2,9. Aceptando que la variabilidad en los resultados se debe a las siguientes causas: Primero la diferencia entre las parcelas cosechadas, segundo las contingencias de la tarea (roturas, paradas, etc.), y tercero la diferencia entre las máquinas. Entonces, las causas primera y segunda influyen igual para ambas marcas, pero no tenemos información sobre la causa tercera, es decir que las diferencias entre máquinas podrían ser distintas para John Deere y Vasalli.

- **a)** ¿Es posible asegurar con 10% de riesgo que los volúmenes medios cosechados son diferentes?
- **b)** Calcule un intervalo de confianza del 80% para la diferencia entre los volúmenes medios cosechados.

*Volúmenes cosechados (t/día)*

| Marca | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| John Deere (JD) | 3,2 | 2,8 | 2,4 | 3,6 | 2,7 |
| Vasalli (V) | 2,5 | 2,2 | 3,7 | 2,1 | 2,9 |

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(John Deere (JD)) - μ(Vasalli (V)) ≤ 0  vs  H1: δ = μ(John Deere (JD)) - μ(Vasalli (V)) > 0.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Vasalli (V)) > S(John Deere (JD)), lo único que se puede sospechar es σ(Vasalli (V)) > σ(John Deere (JD)) → unilateral, H0: φ = σ(Vasalli (V))/σ(John Deere (JD)) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 4; ν₂ = 4) = √4,1072 = 2,0266; J = S(Vasalli (V))/S(John Deere (JD)) = 1,3913 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,565685; ν = n₁ + n₂ - 2 = 8.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(John Deere (JD)) - x̄(Vasalli (V)) = 0,26; σ(d) = 0,357771, ν = 8.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 0,4997. Si d > 0,4997 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 0,4997, se rechaza H0 → se puede asegurar que δ = μ(John Deere (JD)) - μ(Vasalli (V)) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(John Deere (JD)) - μ(Vasalli (V)) > 0.
- **6 · Cálculos y decisión**: d = 0,26 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,2441. La decisión se toma comparando el estimador con el valor crítico.
- **Orientación**: el enunciado no da dirección («¿difieren?»), pero en comparaciones no existen ensayos bilaterales: la muestra orienta el ensayo y lo único que se puede intentar probar es que μ(John Deere (JD)), el de mayor media muestral, supera a μ(Vasalli (V)).

**Conclusión:** Con α = 0,1, d = 0,26 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(John Deere (JD)) - μ(Vasalli (V)) ≤ 0. No hay evidencia suficiente para asegurar que δ = μ(John Deere (JD)) - μ(Vasalli (V)) > 0 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No se puede asegurar que los volúmenes promedio cosechados sean diferentes, por lo cual se consideran iguales.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Pide estimar el parámetro: intervalo de confianza P(A ≤ θ ≤ B) = 1-α.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Modelo**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Vasalli (V)) > S(John Deere (JD)), lo único que se puede sospechar es σ(Vasalli (V)) > σ(John Deere (JD)) → unilateral, H0: φ = σ(Vasalli (V))/σ(John Deere (JD)) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 4; ν₂ = 4) = √4,1072 = 2,0266; J = S(Vasalli (V))/S(John Deere (JD)) = 1,3913 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,565685; ν = n₁ + n₂ - 2 = 8.
- **IC para δ = μ(John Deere (JD)) - μ(Vasalli (V))** (t con Sa (desvíos iguales)): d = 0,26; e = t(0,9; 8)·σ(d) = 1,3968·0,357771 = 0,4997.

**Conclusión:** P(-0,240 ≤ μ(John Deere (JD)) - μ(Vasalli (V)) ≤ 0,760) = 0,8 (e = 0,4997). Para μ(Vasalli (V)) - μ(John Deere (JD)): entre -0,760 y 0,240. Límites redondeados hacia afuera; sin redondear: -0,23974 y 0,75974.

**Respuesta de la guía:** Entre (−0,2397) y 0,7598 Tn/día (para δ = μJD − μV), se puede esperar como mínimo que John Deere coseche en promedio 0,2397 Tn/día menos que Vasalli o como máximo coseche en promedio 0,7598 Tn/día más.

---

### V-10 · Problema 10 (pág. 35)

**Enunciado.** En una empresa productora de artículos de consumo masivo se ha lanzado una campaña publicitaria sobre un jabón en polvo a efectos de incrementar las ventas mensuales. Se desea ahora comprobar si la campaña ha sido efectiva, en cuyo caso se realizará una campaña similar sobre otro de los productos. A tal efecto, si no se ha conseguido el resultado deseado, se establece una probabilidad de 0,05 de tomar una decisión equivocada. Se registraron las ventas durante los cuatro meses que duró la campaña obteniéndose un promedio de 642.000 unidades con un desvío estándar de 73.000 unidades. Con respecto a las ventas anteriores a la campaña, no se disponía de registros históricos extensos que permitieran conocer su valor exacto, pero pudo obtenerse los datos correspondientes a los últimos 12 meses que arrojaron un valor medio de 570.000 unidades con un desvío estándar de 45.000 unidades.

- **a)** ¿Cuál sería la decisión si se deseara tener la casi seguridad de que con la campaña las ventas promedio se incrementan en 50.000 unidades por lo menos?
- **b)** Ídem a), si se deseara asegurar un incremento del 10% por lo menos.
- **c)** Alguien ensayó la hipótesis de que las ventas medias con la campaña eran inferiores a 580.000 unidades y la rechazó; calcule la probabilidad de que se haya equivocado.

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide la conclusión / decisión: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(con la campaña) - μ(sin la campaña) ≤ 50,000  vs  H1: δ = μ(con la campaña) - μ(sin la campaña) > 50,000.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(con la campaña) > S(sin la campaña), lo único que se puede sospechar es σ(con la campaña) > σ(sin la campaña) → unilateral, H0: φ = σ(con la campaña)/σ(sin la campaña) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 3; ν₂ = 11) = √2,6602 = 1,631; J = S(con la campaña)/S(sin la campaña) = 1,6222 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 52.278,10249; ν = n₁ + n₂ - 2 = 14.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(con la campaña) - x̄(sin la campaña) = 72.000; σ(d) = 30.182,776546, ν = 14.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 103.161,2303. Si d > 103.161,2303 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 103,161,2303, se rechaza H0 → se puede asegurar que δ = μ(con la campaña) - μ(sin la campaña) > 50,000. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(con la campaña) - μ(sin la campaña) > 50,000.
- **6 · Cálculos y decisión**: d = 72.000 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,239. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,05, d = 72,000 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(con la campaña) - μ(sin la campaña) ≤ 50,000. No hay evidencia suficiente para asegurar que δ = μ(con la campaña) - μ(sin la campaña) > 50,000 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No se puede asegurar que la campaña haya incrementado las ventas en 50.000 unidades por lo menos.

#### b.a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide la conclusión / decisión: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: μ(con la campaña) ≤ 1,1·μ(sin la campaña) (δ* = μ(con la campaña) - 1,1·μ(sin la campaña) ≤ 0)  vs  H1: μ(con la campaña) > 1,1·μ(sin la campaña).
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(con la campaña) > S(sin la campaña), lo único que se puede sospechar es σ(con la campaña) > σ(sin la campaña) → unilateral, H0: φ = σ(con la campaña)/σ(sin la campaña) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 3; ν₂ = 11) = √2,6602 = 1,631; J = S(con la campaña)/S(sin la campaña) = 1,6222 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 52.278,10249; ν = n₁ + n₂ - 2 = 14.
- Diferencia observada (t con Sa (desvíos iguales)): d* = x̄(con la campaña) - 1,1·x̄(sin la campaña) = 15.000; σ(d*) = 30.964,939851, ν = 14.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 54.538,8624. Si d > 54.538,8624 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 54,538,8624, se rechaza H0 → se puede asegurar que μ(con la campaña) > 1,1·μ(sin la campaña). En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ(con la campaña) > 1,1·μ(sin la campaña).
- **6 · Cálculos y decisión**: d = 15.000 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,3178. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,05, d = 15,000 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ(con la campaña) ≤ 1,1·μ(sin la campaña) (δ* = μ(con la campaña) - 1,1·μ(sin la campaña) ≤ 0). No hay evidencia suficiente para asegurar que μ(con la campaña) > 1,1·μ(sin la campaña) (no rechazar H0 no la prueba).

**Respuesta de la guía:** No puedo asegurar que la campaña haya incrementado las ventas en un 10% por lo menos.

#### c) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ ≤ 580000  vs  H1: μ > 580000.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≤ 580.000 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ > 580.000 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,05 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student, ν = número de grados de libertad = 3. t(1-α) = 2,3534.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 2,3534·S/√n = 580.000 + 2,3534·73.000/√4 = 665.897,7654. Si x̄ > 665.897,7654 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 665.897,77; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 4 unidades y se calcula su media x̄. Si x̄ > 665,897,7654, se rechaza H0 → se puede asegurar que μ > 580000. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 580000.
- **6 · Cálculos y decisión**: x̄ = 642.000 → no cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,094. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,05, x̄ = 642,000 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ ≤ 580000. No hay evidencia suficiente para asegurar que μ > 580000 (no rechazar H0 no la prueba).

**Respuesta de la guía:** α = 0,094 o más.

---

### V-11 · Problema 11 (pág. 35)

**Enunciado.** Se desea estudiar la efectividad de un nuevo plaguicida contra el pulgón en cultivos de avena amarilla, que es muy sensible a dicho insecto. Para efectuar la prueba se fumigaron 5 parcelas infectadas y se obtuvo en la cosecha un rendimiento medio de 20 quintales por parcela, con un desvío de 2,5 quintales por parcela. Con el producto tradicional se hizo una prueba similar, en otras 5 parcelas infectadas, con un rendimiento medio de 19,5 quintales por parcela, con un desvío de 3 quintales por parcela.

- **a)** ¿Aseguraría, con un 10% de riesgo, que con el nuevo producto se obtiene una diferencia mínima de 0,2 quintales por parcela?
- **b)** ¿Cuál sería la conclusión si se tuviera el dato de que, con el producto tradicional, el rendimiento medio en cultivos infectados es de 19,5 quintales por parcela?

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide decidir si se puede asegurar una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(nuevo producto) - μ(producto tradicional) ≤ 0,2  vs  H1: δ = μ(nuevo producto) - μ(producto tradicional) > 0,2.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(producto tradicional) > S(nuevo producto), lo único que se puede sospechar es σ(producto tradicional) > σ(nuevo producto) → unilateral, H0: φ = σ(producto tradicional)/σ(nuevo producto) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 4; ν₂ = 4) = √4,1072 = 2,0266; J = S(producto tradicional)/S(nuevo producto) = 1,2 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 2,76134; ν = n₁ + n₂ - 2 = 8.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(nuevo producto) - x̄(producto tradicional) = 0,5; σ(d) = 1,746425, ν = 8.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 2,6394. Si d > 2,6394 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 2,6394, se rechaza H0 → se puede asegurar que δ = μ(nuevo producto) - μ(producto tradicional) > 0,2. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(nuevo producto) - μ(producto tradicional) > 0,2.
- **6 · Cálculos y decisión**: d = 0,5 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,4339. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,1, d = 0,5 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(nuevo producto) - μ(producto tradicional) ≤ 0,2. No hay evidencia suficiente para asegurar que δ = μ(nuevo producto) - μ(producto tradicional) > 0,2 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No se puede asegurar que el nuevo plaguicida mejore el rendimiento en 0,2 quintales como mínimo.

#### b) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Decidir con un ensayo de hipótesis sobre la media poblacional μ: H1 con signo '>'. Se compara el valor muestral con el valor crítico y se redacta 'se rechaza / no se rechaza H0'.

- **1 · Planteo de hipótesis**: H0: μ ≤ 19,5  vs  H1: μ > 19,5.
- **Justificación de H0**:  
• **Criterio pesimista**: hay una decisión costosa en juego (compra, inversión, cambio). H0: μ ≤ 19,5 supone lo desfavorable y solo se la rechaza con evidencia fuerte; H1: μ > 19,5 es la situación favorable que habilita la decisión. Así el error grave (decidir sin que se justifique) queda acotado por α.  
• α = P(rechazar H0 | H0 cierta) = 0,1 (error de tipo I).  
• El ensayo es unilateral a la derecha: la zona de rechazo está donde apunta H1.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: al estandarizar x̄ se divide por S, que es una variable aleatoria (raíz de una χ²/ν): queda una t de Student, ν = número de grados de libertad = 4. t(1-α) = 1,5332.
- **Modelos y distribuciones empleados**:  
• La variable X se supone Normal: X ~ N(μ; σ²), así que x̄ ~ N(μ; σ²/n).  
• Al estandarizar con el desvío muestral, t = (x̄ - μ)/(S/√n), se divide por S, que es una VARIABLE ALEATORIA (la raíz de una χ² dividida por ν): una normal dividida por la raíz de una χ²/ν es una t de Student con ν = n - 1 grados de libertad, sea cual sea n. (No es «uso t porque no conozco σ».)
- **4 · Condición de rechazo (CR)**: x̄c = μ₀ + 1,5332·S/√n = 19,5 + 1,5332·2,5/√5 = 21,2142. Si x̄ > 21,2142 ⇒ se rechaza H0. Informado como la cátedra (hacia afuera de μ₀): x̄c = 21,22; la decisión se toma con el valor exacto.
- **5 · Regla de decisión (RD)**: Se toma una muestra de n = 5 unidades y se calcula su media x̄. Si x̄ > 21,2142, se rechaza H0 → se puede asegurar que μ > 19,5. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que μ > 19,5.
- **6 · Cálculos y decisión**: x̄ = 20 → no cae en la zona de rechazo.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = P(obtener un x̄ tan extremo | H0) = 0,3389. La decisión se toma comparando x̄ con x̄c.

**Conclusión:** Con α = 0,1, x̄ = 20 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: μ ≤ 19,5. No hay evidencia suficiente para asegurar que μ > 19,5 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No se puede asegurar que el nuevo plaguicida mejore el rendimiento.

---

### V-12 · Problema 12 (pág. 35)

**Enunciado.** Para ensayar dos nuevas variedades de trigo bajo condiciones agrícolas normales, una sociedad de cereales eligió al azar 8 fincas plantando ambas variedades en parcelas experimentales de cada finca. La producción de las 8 fincas fue la siguiente (valores en quintales por parcela): Finca: I II III IV V VI VII VIII; Variedad “A”: 86 87 56 93 84 93 75 79; Variedad “B”: 80 79 58 91 77 82 74 66.

- **a)** Se puede asegurar, con un riesgo del 5%, que la producción obtenida con la Variedad “A” es mayor que la producción de la Variedad “B” en más de 2 quintales por parcela.
- **b)** Estimar la diferencia entre las producciones medias con un intervalo de confianza del 90%.

| Finca | I | II | III | IV | V | VI | VII | VIII |
|---|---|---|---|---|---|---|---|---|
| Variedad “A” | 86 | 87 | 56 | 93 | 84 | 93 | 75 | 79 |
| Variedad “B” | 80 | 79 | 58 | 91 | 77 | 82 | 74 | 66 |

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(Variedad “A”) - μ(Variedad “B”) ≤ 2  vs  H1: δ = μ(Variedad “A”) - μ(Variedad “B”) > 2.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: muestras apareadas, dᵢ = x(Variedad “A”) - x(Variedad “B”) → d̄ = 5,75, S_d = 5,12, n = 8 pares (ν = 7); σ(d̄) = S_d/√n = 1,8102.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 5,4295. Si d > 5,4295 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre los pares. Si d > 5,4295, se rechaza H0 → se puede asegurar que δ = μ(Variedad “A”) - μ(Variedad “B”) > 2. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Variedad “A”) - μ(Variedad “B”) > 2.
- **6 · Cálculos y decisión**: d = 5,75 → se rechaza H0.

**Conclusión:** Con α = 0,05, d = 5,75 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: δ = μ(Variedad “A”) - μ(Variedad “B”) ≤ 2. Se puede asegurar que δ = μ(Variedad “A”) - μ(Variedad “B”) > 2.

**Respuesta de la guía:** Se puede asegurar que la producción de la Variedad “A” es mayor que la de la Variedad “B” en más de 2 quintales por parcela.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Pide estimar el parámetro: intervalo de confianza P(A ≤ θ ≤ B) = 1-α.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Muestras apareadas**: dᵢ = x(Variedad “A”) - x(Variedad “B”) → d̄ = 5,75, S_d = 5,12, n = 8 pares (ν = 7); e = t(0,95; 7)·S_d/√n = 3,4295.

**Conclusión:** P(2,32 ≤ μ(Variedad “A”) - μ(Variedad “B”) ≤ 9,18) = 0,9 (e = 3,4295). Para μ(Variedad “B”) - μ(Variedad “A”): entre -9,18 y -2,32. Límites redondeados hacia afuera; sin redondear: 2,320454 y 9,179546.

**Respuesta de la guía:** Entre 2,32 y 9,18 quintales por parcela (para δ = μA − μB), con la variedad “A” se obtiene una producción mínima de 2,32 quintales por parcela mayor que la variedad “B” y de 9,18 quintales por parcela como máximo.

---

### V-13 · Problema 13 (pág. 35)

**Enunciado.** A efectos de determinar el poder calorífico de un combustible se propone un método simplificado que se supone dará buenos resultados, sin diferencias significativas respecto del método clásico. Se efectúa una serie de mediciones de distintas muestras, usando el método propuesto y el clásico (calorímetro de combustión), obteniéndose los siguientes resultados (Muestra Nº: Método Propuesto / Método Clásico): 1: 164,65 / 165,20; 2: 178,60 / 179,20; 3: 188,20 / 189,20; 4: 200,60 / 201,30; 5: 188,50 / 189,20; 6: 145,60 / 145,20; 7: 130,25 / 131,15; 8: 199,95 / 199,20; 9: 160,90 / 161,20; 10: 155,10 / 155,20; 11: 131,15 / 133,15; 12: 174,15 / 174,20; 13: 129,75 / 130,10; 14: 156,40 / 158,30.

*Teniendo en cuenta que se utilizaría el método propuesto si no hay diferencias significativas en las mediciones promedio, ¿Recomendaría el método propuesto, asumiendo un riesgo del 1%?*

| Muestra Nº | Método Propuesto | Método Clásico | Muestra Nº | Método Propuesto | Método Clásico |
|---|---|---|---|---|---|
| 1 | 164,65 | 165,2 | 8 | 199,95 | 199,2 |
| 2 | 178,6 | 179,2 | 9 | 160,9 | 161,2 |
| 3 | 188,2 | 189,2 | 10 | 155,1 | 155,2 |
| 4 | 200,6 | 201,3 | 11 | 131,15 | 133,15 |
| 5 | 188,5 | 189,2 | 12 | 174,15 | 174,2 |
| 6 | 145,6 | 145,2 | 13 | 129,75 | 130,1 |
| 7 | 130,25 | 131,15 | 14 | 156,4 | 158,3 |

*Tema detectado por la app: Comparación de 2 medias.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(Método Clásico) - μ(Método Propuesto) ≤ 0  vs  H1: δ = μ(Método Clásico) - μ(Método Propuesto) > 0.
- **2 · Nivel de significación**: α = 0,01 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: muestras apareadas, dᵢ = x(Método Clásico) - x(Método Propuesto) → d̄ = 0,5714, S_d = 0,7564, n = 14 pares (ν = 13); σ(d̄) = S_d/√n = 0,2022.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 0,5358. Si d > 0,5358 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre los pares. Si d > 0,5358, se rechaza H0 → se puede asegurar que δ = μ(Método Clásico) - μ(Método Propuesto) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Método Clásico) - μ(Método Propuesto) > 0.
- **6 · Cálculos y decisión**: d = 0,5714 → se rechaza H0.
- **Orientación**: el enunciado no da dirección («¿difieren?»), pero en comparaciones no existen ensayos bilaterales: la muestra orienta el ensayo y lo único que se puede intentar probar es que μ(Método Clásico), el de mayor media muestral, supera a μ(Método Propuesto).

**Conclusión:** Con α = 0,01, d = 0,5714 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: δ = μ(Método Clásico) - μ(Método Propuesto) ≤ 0. Se puede asegurar que δ = μ(Método Clásico) - μ(Método Propuesto) > 0.

**Respuesta de la guía:** No, porque se puede asegurar que el método propuesto presenta diferencias significativas en las mediciones respecto del método clásico.

> 📝 *Notas de la transcripción:* El planteo empieza en la página 35 y la tabla está en la 36.

---

### V-14 · Problema 14 (pág. 36)

**Enunciado.** Se supone que una tinta especial para calzado puede producir un aumento en la duración media, a efectos de lo cual se diseñó un experimento suministrando a 8 personas un par de zapatos, uno de los cuales fue tratado y el otro no. De este modo se espera eliminar la fuerte variabilidad existente entre las personas. Se obtuvieron así los siguientes resultados de duración en semanas, llamando duración al lapso comprendido entre el comienzo de uso y el momento en que aparecen las primeras grietas del cuero: Persona: 1 2 3 4 5 6 7 8; Zapato sin tratar: 12 7 18 15 20 8 13 13; Zapato tratado: 14 7 21 14 23 9 14 12.

*¿Se considera que el resultado ha sido concluyente, asumiendo un riesgo del 5%?*

| Persona | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Zapato sin tratar | 12 | 7 | 18 | 15 | 20 | 8 | 13 | 13 |
| Zapato tratado | 14 | 7 | 21 | 14 | 23 | 9 | 14 | 12 |

*Tema detectado por la app: Comparación de 2 medias.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(Zapato tratado) - μ(Zapato sin tratar) ≤ 0  vs  H1: δ = μ(Zapato tratado) - μ(Zapato sin tratar) > 0.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: muestras apareadas, dᵢ = x(Zapato tratado) - x(Zapato sin tratar) → d̄ = 1, S_d = 1,6036, n = 8 pares (ν = 7); σ(d̄) = S_d/√n = 0,5669.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 1,0741. Si d > 1,0741 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre los pares. Si d > 1,0741, se rechaza H0 → se puede asegurar que δ = μ(Zapato tratado) - μ(Zapato sin tratar) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Zapato tratado) - μ(Zapato sin tratar) > 0.
- **6 · Cálculos y decisión**: d = 1 → no se rechaza H0.

**Conclusión:** Con α = 0,05, d = 1 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(Zapato tratado) - μ(Zapato sin tratar) ≤ 0. No hay evidencia suficiente para asegurar que δ = μ(Zapato tratado) - μ(Zapato sin tratar) > 0 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No, no se puede asegurar que la tinta especial aumente la duración del cuero en el calzado.

---

### V-15 · Problema 15 (pág. 36)

**Enunciado.** Para conocer la influencia del ruido sobre el tiempo para la realización de una tarea, se realiza una prueba en un tiempo de operación estipulado de 8 horas con una muestra de operarios de la misma calificación con los siguientes resultados: Una muestra de 10 operarios sometidos, a un nivel bajo de ruido, hicieron un promedio de 6,3 piezas por hora durante el tiempo de operación estipulado con un desvío de 3,5 piezas por hora para ese tiempo. Una muestra de 12 operarios sometidos, a un alto nivel sonoro, rindieron, para el mismo tiempo estipulado, un promedio de 5,2 piezas por hora y un desvío de 3,1 piezas por hora.

*Asumiendo un riesgo del 1%, ¿se puede decir que el alto nivel sonoro influye sobre los tiempos de producción?*

*Tema detectado por la app: Comparación de 2 medias.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(Muestra 1) - μ(Muestra 2) ≤ 0  vs  H1: δ = μ(Muestra 1) - μ(Muestra 2) > 0.
- **2 · Nivel de significación**: α = 0,01 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Muestra 1) > S(Muestra 2), lo único que se puede sospechar es σ(Muestra 1) > σ(Muestra 2) → unilateral, H0: φ = σ(Muestra 1)/σ(Muestra 2) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 9; ν₂ = 11) = √2,2735 = 1,5078; J = S(Muestra 1)/S(Muestra 2) = 1,129 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 3,286031; ν = n₁ + n₂ - 2 = 20.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(Muestra 1) - x̄(Muestra 2) = 1,1; σ(d) = 1,406994, ν = 20.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 3,5568. Si d > 3,5568 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 3,5568, se rechaza H0 → se puede asegurar que δ = μ(Muestra 1) - μ(Muestra 2) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Muestra 1) - μ(Muestra 2) > 0.
- **6 · Cálculos y decisión**: d = 1,1 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,2217. La decisión se toma comparando el estimador con el valor crítico.
- **Orientación**: el enunciado no da dirección («¿difieren?»), pero en comparaciones no existen ensayos bilaterales: la muestra orienta el ensayo y lo único que se puede intentar probar es que μ(Muestra 1), el de mayor media muestral, supera a μ(Muestra 2).

**Conclusión:** Con α = 0,01, d = 1,1 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(Muestra 1) - μ(Muestra 2) ≤ 0. No hay evidencia suficiente para asegurar que δ = μ(Muestra 1) - μ(Muestra 2) > 0 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No se puede asegurar que el alto nivel sonoro influya sobre los tiempos de producción.

---

### V-16 · Problema 16 (pág. 36)

**Enunciado.** Se quiere comprobar si la introducción de un determinado acelerante en el material plástico usado para obtener piezas por inyección, aumenta la dureza promedio del mismo. Para ello se toma la dureza en piezas fabricadas con plástico sin acelerante y con acelerante, con los siguientes resultados de dureza (medida en grados Shore): Sin acelerante: 69,3 75,4 71,3 69,5 72,8 73,7 72,3 70,4 71,9 69,7; Con acelerante: 75,3 76,7 70,8 72,7 69,1.

*Dureza (grados Shore)*

| Grupo | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sin acelerante | 69,3 | 75,4 | 71,3 | 69,5 | 72,8 | 73,7 | 72,3 | 70,4 | 71,9 | 69,7 |
| Con acelerante | 75,3 | 76,7 | 70,8 | 72,7 | 69,1 |

*Tema detectado por la app: Comparación de 2 medias.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(Con acelerante) - μ(Sin acelerante) ≤ 0  vs  H1: δ = μ(Con acelerante) - μ(Sin acelerante) > 0.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Con acelerante) > S(Sin acelerante), lo único que se puede sospechar es σ(Con acelerante) > σ(Sin acelerante) → unilateral, H0: φ = σ(Con acelerante)/σ(Sin acelerante) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 4; ν₂ = 9) = √2,6927 = 1,6409; J = S(Con acelerante)/S(Sin acelerante) = 1,5695 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 2,398541; ν = n₁ + n₂ - 2 = 13.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(Con acelerante) - x̄(Sin acelerante) = 1,29; σ(d) = 1,313735, ν = 13.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 2,3265. Si d > 2,3265 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 2,3265, se rechaza H0 → se puede asegurar que δ = μ(Con acelerante) - μ(Sin acelerante) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Con acelerante) - μ(Sin acelerante) > 0.
- **6 · Cálculos y decisión**: d = 1,29 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,172. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,05, d = 1,29 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(Con acelerante) - μ(Sin acelerante) ≤ 0. No hay evidencia suficiente para asegurar que δ = μ(Con acelerante) - μ(Sin acelerante) > 0 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No se puede asegurar que el acelerante aumente la dureza promedio del material plástico.

> 📝 *Notas de la transcripción:* La guía no trae una consigna explícita después de la tabla ni indica el riesgo α; como texto del inciso se usa la frase del planteo ('Se quiere comprobar si ... aumenta la dureza promedio'). La fila 'Con acelerante' tiene 5 datos y 'Sin acelerante' 10.

---

### V-17 · Problema 17 (pág. 37)

**Enunciado.** Un fabricante desea comparar el proceso de armado actual para uno de sus productos con un método propuesto que supuestamente reduce el tiempo de armado. Se seleccionaron 8 trabajadores de la planta de armado y se les pidió que armaran las unidades con ambos procesos. Los siguientes resultados son los tiempos en minutos observados: Trabajador: 1 2 3 4 5 6 7 8; Proceso Actual (A): 38 32 41 35 42 32 45 37; Proceso Propuesto (P): 30 32 34 37 35 26 38 32.

- **a)** Para un riesgo del 5%, ¿existe alguna razón para creer que el tiempo de armado para el proceso actual es mayor que el del método propuesto por más de 2 minutos?
- **b)** Obtener un intervalo de confianza del 90% para la diferencia entre las medias de los tiempos de armado.
- **c)** ¿Cuántos trabajadores más se deberán incluir en el estudio para reducir a la tercera parte el error de estimación anterior?

| Trabajador | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Proceso Actual (A) | 38 | 32 | 41 | 35 | 42 | 32 | 45 | 37 |
| Proceso Propuesto (P) | 30 | 32 | 34 | 37 | 35 | 26 | 38 | 32 |

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(Proceso Actual (A)) - μ(Proceso Propuesto (P)) ≤ 2  vs  H1: δ = μ(Proceso Actual (A)) - μ(Proceso Propuesto (P)) > 2.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: muestras apareadas, dᵢ = x(Proceso Actual (A)) - x(Proceso Propuesto (P)) → d̄ = 4,75, S_d = 3,6936, n = 8 pares (ν = 7); σ(d̄) = S_d/√n = 1,3059.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 4,4741. Si d > 4,4741 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre los pares. Si d > 4,4741, se rechaza H0 → se puede asegurar que δ = μ(Proceso Actual (A)) - μ(Proceso Propuesto (P)) > 2. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Proceso Actual (A)) - μ(Proceso Propuesto (P)) > 2.
- **6 · Cálculos y decisión**: d = 4,75 → se rechaza H0.

**Conclusión:** Con α = 0,05, d = 4,75 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: δ = μ(Proceso Actual (A)) - μ(Proceso Propuesto (P)) ≤ 2. Se puede asegurar que δ = μ(Proceso Actual (A)) - μ(Proceso Propuesto (P)) > 2.

**Respuesta de la guía:** H0: μA ≤ μP + 2 (δ = μA − μP, H0: δ ≤ δ0 = 2); muestras apareadas, d̄ = 4,75', Sd = 3,6936', ν = 7, dc = 4,4741'. Se rechaza la hipótesis: se puede asegurar que el tiempo promedio del proceso de armado actual es mayor al tiempo promedio del proceso propuesto en más de 2 minutos.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Pide estimar el parámetro: intervalo de confianza P(A ≤ θ ≤ B) = 1-α.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Muestras apareadas**: dᵢ = x(Proceso Actual (A)) - x(Proceso Propuesto (P)) → d̄ = 4,75, S_d = 3,6936, n = 8 pares (ν = 7); e = t(0,95; 7)·S_d/√n = 2,4741.

**Conclusión:** P(2,27 ≤ μ(Proceso Actual (A)) - μ(Proceso Propuesto (P)) ≤ 7,23) = 0,9 (e = 2,4741). Para μ(Proceso Propuesto (P)) - μ(Proceso Actual (A)): entre -7,23 y -2,27. Límites redondeados hacia afuera; sin redondear: 2,275883 y 7,224117.

**Respuesta de la guía:** Entre 2,27' y 7,23' (δ = μA − μP; 4,75 ± 2,4741), con un error de muestreo e = 2,4741 minutos.

#### c) Tamaño de muestra ✅

*Qué pide:* Pregunta cuántas unidades hacen falta: tamaño de muestra (y Δn si ya hay una muestra).

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Error buscado**: e = 2,4741·(1 - 0,6667) = 0,8247.
- Apareadas: n = [t(1-α/2; n-1)·S_d/e]², iterando: n = 57 pares [56, 57, 57].

**Conclusión:** Se necesitan n = 57 en cada muestra (e = 0,8247). Hoy hay 8 pares: faltan 49 más.

**Respuesta de la guía:** e = 0,8247 minutos; n = 57 trabajadores en total, o sea 49 trabajadores más.

> 📝 *Notas de la transcripción:* Sin 'Resp:'; respuesta armada desde la Solución.

<details><summary>Cómo lo concluye la guía</summary>

> Como la comparación de ambos procesos se realiza en la misma unidad experimental (trabajador), hay que trabajar con muestras apareadas.
> Diferencias por trabajador (en minutos): 8, 0, 7, −2, 7, 6, 7, 5.
> De manera que la hipótesis se rechaza, por lo cual se puede asegurar que el tiempo promedio del proceso de armado actual es mayor al tiempo promedio del proceso propuesto en más de 2 minutos.
> Se concluye que la diferencia entre las medias poblacionales estará comprendida entre 2,27' y 7,23', afirmándolo con un 90% de confianza.
> El resultado se obtiene con n = 57. Se necesitan un total de 57 trabajadores, o sea que se necesitarán incluir en el estudio realizado 49 trabajadores más.

</details>

---

### V-18 · Problema 18 (pág. 37)

**Enunciado.** El interferón alfa es conocido por su efecto antiviral y anti proliferativo, se ha podido obtener por la vía del ADN recombinante (IFN alfa 2b hu-r). Con el objetivo de determinar el tiempo y la temperatura de almacenamiento de esta proteína se realizó un estudio de estabilidad bajo condiciones aceleradas. La función estabilizante de la albúmina humana sobre biomoléculas se ha destacado por diferentes autores empleándose para la estabilización de proteínas en la fase de investigación y muchas veces en los productos farmacéuticos (un exceso de albúmina en la formulación de interleucina 2 recombinante logró estabilizar la preparación liofilizada). Los siguientes datos muestran los resultados de un estudio de estabilidad del IFN alfa 2b hu-r bajo condiciones aceleradas y bajo condiciones reales de almacenamiento, tanto en presencia como en ausencia de albúmina. El material se dividió en dos partes (en envases de condiciones estériles), a una parte se le adicionó albúmina humana (en solución al 20% en volumen) como preservante. Los valores están medidos en constantes de la velocidad de degradación expresada en días^(-1). (Muestra Nº: Con albúmina humana / Sin albúmina humana): 1: −0,01653 / −0,01542; 2: −0,15279 / −0,08274; 3: −1,12040 / −0,77950; 4: −0,89723 / −0,59815; 5: −0,25473 / −0,18869; 6: −0,07298 / −0,06635.

*Determinar si existen diferencias significativas en la velocidad de degradación de la proteína con presencia y sin presencia de la albúmina (aceptando un riesgo del 1%).*

| Muestra Nº | Con albúmina humana | Sin albúmina humana |
|---|---|---|
| 1 | -0,01653 | -0,01542 |
| 2 | -0,15279 | -0,08274 |
| 3 | -1,1204 | -0,7795 |
| 4 | -0,89723 | -0,59815 |
| 5 | -0,25473 | -0,18869 |
| 6 | -0,07298 | -0,06635 |

*Tema detectado por la app: Comparación de 2 medias.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(Sin albúmina humana) - μ(Con albúmina humana) ≤ 0  vs  H1: δ = μ(Sin albúmina humana) - μ(Con albúmina humana) > 0.
- **2 · Nivel de significación**: α = 0,01 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: muestras apareadas, dᵢ = x(Sin albúmina humana) - x(Con albúmina humana) → d̄ = 0,1306, S_d = 0,1501, n = 6 pares (ν = 5); σ(d̄) = S_d/√n = 0,0613.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 0,2061. Si d > 0,2061 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre los pares. Si d > 0,2061, se rechaza H0 → se puede asegurar que δ = μ(Sin albúmina humana) - μ(Con albúmina humana) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Sin albúmina humana) - μ(Con albúmina humana) > 0.
- **6 · Cálculos y decisión**: d = 0,1306 → no se rechaza H0.
- **Orientación**: el enunciado no da dirección («¿difieren?»), pero en comparaciones no existen ensayos bilaterales: la muestra orienta el ensayo y lo único que se puede intentar probar es que μ(Sin albúmina humana), el de mayor media muestral, supera a μ(Con albúmina humana).

**Conclusión:** Con α = 0,01, d = 0,1306 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(Sin albúmina humana) - μ(Con albúmina humana) ≤ 0. No hay evidencia suficiente para asegurar que δ = μ(Sin albúmina humana) - μ(Con albúmina humana) > 0 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No se puede asegurar que existan diferencias significativas en la velocidad de degradación de la proteína.

---

### V-19 · Problema 19 (pág. 38)

**Enunciado.** A la proteína "IFN alfa 2b hu-r", se le realizó un estudio de actividad biológica determinada por ensayo de titulación (función antiviral del IFN alfa) expresado en UI/mL (tomando un valor de actividad biológica inicial de 10,8 x 106 UI/mL) a diferentes temperaturas. Las pruebas se hicieron dividiendo al material en dos partes (en envases de condiciones estériles), a una parte se le adicionó albúmina humana (en solución al 20% en volumen) como preservante. (Muestra Nº: 4 ºC Sin albúmina, 4 ºC Con albúmina, −20 ºC Sin albúmina, −20 ºC Con albúmina, −70 ºC Sin albúmina, −70 ºC Con albúmina): 1: 2,41 3,16 6,39 8,27 5,04 4,91; 2: 3,28 3,95 2,76 2,56 3,57 5,69; 3: 12,24 11,22 12,60 9,00 12,90 16,50; 4: 3,20 4,52 2,26 2,26 3,26 3,26; 5: 9,40 6,40 7,40 9,90 7,30 8,00; 6: 5,48 5,91 4,05 5,74 6,32 5,21; 7: 6,77 7,36 6,38 7,13 7,18 5,70.

*Determinar si existen diferencias significativas en la Actividad biológica con presencia y sin presencia de albúmina (sugerencia: para el alcance visto en la materia se propone hacer tres comparaciones, uno para cada temperatura de almacenamiento). Asumir un riesgo del 5%.*

*Actividad biológica (UI/mL)*

| Muestra Nº | 4 ºC Sin albúmina | 4 ºC Con albúmina | −20 ºC Sin albúmina | −20 ºC Con albúmina | −70 ºC Sin albúmina | −70 ºC Con albúmina |
|---|---|---|---|---|---|---|
| 1 | 2,41 | 3,16 | 6,39 | 8,27 | 5,04 | 4,91 |
| 2 | 3,28 | 3,95 | 2,76 | 2,56 | 3,57 | 5,69 |
| 3 | 12,24 | 11,22 | 12,6 | 9 | 12,9 | 16,5 |
| 4 | 3,2 | 4,52 | 2,26 | 2,26 | 3,26 | 3,26 |
| 5 | 9,4 | 6,4 | 7,4 | 9,9 | 7,3 | 8 |
| 6 | 5,48 | 5,91 | 4,05 | 5,74 | 6,32 | 5,21 |
| 7 | 6,77 | 7,36 | 6,38 | 7,13 | 7,18 | 5,7 |

*Tema detectado por la app: Comparación de 2 medias.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **— Comparación 1: 4 ºC Sin albúmina vs 4 ºC Con albúmina —**
- **1 · Planteo de hipótesis**: H0: δ = μ(4 ºC Sin albúmina) - μ(4 ºC Con albúmina) ≤ 0  vs  H1: δ = μ(4 ºC Sin albúmina) - μ(4 ºC Con albúmina) > 0.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: muestras apareadas, dᵢ = x(4 ºC Sin albúmina) - x(4 ºC Con albúmina) → d̄ = 0,0371, S_d = 1,4898, n = 7 pares (ν = 6); σ(d̄) = S_d/√n = 0,5631.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 1,0942. Si d > 1,0942 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre los pares. Si d > 1,0942, se rechaza H0 → se puede asegurar que δ = μ(4 ºC Sin albúmina) - μ(4 ºC Con albúmina) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(4 ºC Sin albúmina) - μ(4 ºC Con albúmina) > 0.
- **6 · Cálculos y decisión**: d = 0,0371 → no se rechaza H0.
- **Orientación**: el enunciado no da dirección («¿difieren?»), pero en comparaciones no existen ensayos bilaterales: la muestra orienta el ensayo y lo único que se puede intentar probar es que μ(4 ºC Sin albúmina), el de mayor media muestral, supera a μ(4 ºC Con albúmina).
- **— Comparación 2: −20 ºC Sin albúmina vs −20 ºC Con albúmina —**
- **1 · Planteo de hipótesis**: H0: δ = μ(−20 ºC Con albúmina) - μ(−20 ºC Sin albúmina) ≤ 0  vs  H1: δ = μ(−20 ºC Con albúmina) - μ(−20 ºC Sin albúmina) > 0.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: muestras apareadas, dᵢ = x(−20 ºC Con albúmina) - x(−20 ºC Sin albúmina) → d̄ = 0,4314, S_d = 2,0372, n = 7 pares (ν = 6); σ(d̄) = S_d/√n = 0,77.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 1,4962. Si d > 1,4962 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre los pares. Si d > 1,4962, se rechaza H0 → se puede asegurar que δ = μ(−20 ºC Con albúmina) - μ(−20 ºC Sin albúmina) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(−20 ºC Con albúmina) - μ(−20 ºC Sin albúmina) > 0.
- **6 · Cálculos y decisión**: d = 0,4314 → no se rechaza H0.
- **Orientación**: el enunciado no da dirección («¿difieren?»), pero en comparaciones no existen ensayos bilaterales: la muestra orienta el ensayo y lo único que se puede intentar probar es que μ(−20 ºC Con albúmina), el de mayor media muestral, supera a μ(−20 ºC Sin albúmina).
- **— Comparación 3: −70 ºC Sin albúmina vs −70 ºC Con albúmina —**
- **1 · Planteo de hipótesis**: H0: δ = μ(−70 ºC Con albúmina) - μ(−70 ºC Sin albúmina) ≤ 0  vs  H1: δ = μ(−70 ºC Con albúmina) - μ(−70 ºC Sin albúmina) > 0.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: muestras apareadas, dᵢ = x(−70 ºC Con albúmina) - x(−70 ºC Sin albúmina) → d̄ = 0,5286, S_d = 1,7994, n = 7 pares (ν = 6); σ(d̄) = S_d/√n = 0,6801.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 1,3216. Si d > 1,3216 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre los pares. Si d > 1,3216, se rechaza H0 → se puede asegurar que δ = μ(−70 ºC Con albúmina) - μ(−70 ºC Sin albúmina) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(−70 ºC Con albúmina) - μ(−70 ºC Sin albúmina) > 0.
- **6 · Cálculos y decisión**: d = 0,5286 → no se rechaza H0.
- **Orientación**: el enunciado no da dirección («¿difieren?»), pero en comparaciones no existen ensayos bilaterales: la muestra orienta el ensayo y lo único que se puede intentar probar es que μ(−70 ºC Con albúmina), el de mayor media muestral, supera a μ(−70 ºC Sin albúmina).

**Conclusión:** 1) 4 ºC Sin albúmina vs 4 ºC Con albúmina: Con α = 0,05, d = 0,0371 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(4 ºC Sin albúmina) - μ(4 ºC Con albúmina) ≤ 0. No hay evidencia suficiente para asegurar que δ = μ(4 ºC Sin albúmina) - μ(4 ºC Con albúmina) > 0 (no rechazar H0 no la prueba). 2) −20 ºC Sin albúmina vs −20 ºC Con albúmina: Con α = 0,05, d = 0,4314 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(−20 ºC Con albúmina) - μ(−20 ºC Sin albúmina) ≤ 0. No hay evidencia suficiente para asegurar que δ = μ(−20 ºC Con albúmina) - μ(−20 ºC Sin albúmina) > 0 (no rechazar H0 no la prueba). 3) −70 ºC Sin albúmina vs −70 ºC Con albúmina: Con α = 0,05, d = 0,5286 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(−70 ºC Con albúmina) - μ(−70 ºC Sin albúmina) ≤ 0. No hay evidencia suficiente para asegurar que δ = μ(−70 ºC Con albúmina) - μ(−70 ºC Sin albúmina) > 0 (no rechazar H0 no la prueba).

**Respuesta de la guía:** No se puede asegurar que existan diferencias en la actividad biológica con presencia y sin presencia de albúmina en las pruebas realizadas a distintas temperaturas: a 4 ºC, a -20 ºC y a -70 ºC,

> 📝 *Notas de la transcripción:* '10,8 x 106 UI/mL' probablemente sea 10,8 × 10^6 (exponente perdido en la guía); se transcribe tal cual. La Resp termina en coma.

---

### V-20 · Problema 20 (pág. 38)

**Enunciado.** En un Ingenio azucarero, que tiene plantación propia de caña de azúcar, se le aplica al cultivo un compuesto biogenético en forma de gramicida con el objeto de aumentar la madurez y el rinde de la caña en la obtención de jugo para la producción de azúcar. A tal efecto se eligieron parcelas al azar, a las cuales se le aplicó el tratamiento y a las otras no, obteniéndose los siguientes resultados (medidos en rendimiento por unidad de volumen seleccionado). De 655 observaciones provenientes de parcelas a las cuales se les aplicó el tratamiento, se obtuvo un rinde promedio de 9,97 con un desvío de 0,366; mientras que de 599 observaciones provenientes de parcelas a las cuales no se les aplicó el tratamiento, se obtuvo un rinde promedio de 9,83 con un desvío de 0,3342.

- **a)** Se puede afirmar con un riesgo del 10 % que la aplicación del tratamiento aumenta el rinde de la caña.
- **b)** ¿Cuál es el incremento porcentual mínimo que puede asegurarse en el rinde de la caña si se le aplica el tratamiento para un 95% de confianza?

*Tema detectado por la app: Comparación de 2 medias.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(tratadas) - μ(sin tratar) ≤ 0  vs  H1: δ = μ(tratadas) - μ(sin tratar) > 0.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(tratadas) > S(sin tratar), lo único que se puede sospechar es σ(tratadas) > σ(sin tratar) → unilateral, H0: φ = σ(tratadas)/σ(sin tratar) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 654; ν₂ = 598) = √1,1083 = 1,0527; J = S(tratadas)/S(sin tratar) = 1,0952 → J > Jc: se rechaza H0 → los desvíos son DISTINTOS → Welch.
- ν de Aspin-Welch = (S₁²/n₁ + S₂²/n₂)²/[(S₁²/n₁)²/(n₁-1) + (S₂²/n₂)²/(n₂-1)] = 1.251,9974 → ν = 1251.
- Diferencia observada (t de Welch (desvíos distintos)): d = x̄(tratadas) - x̄(sin tratar) = 0,14; σ(d) = 0,019773, ν = 1251.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 0,0254. Si d > 0,0254 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 0,0254, se rechaza H0 → se puede asegurar que δ = μ(tratadas) - μ(sin tratar) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(tratadas) - μ(sin tratar) > 0.
- **6 · Cálculos y decisión**: d = 0,14 → se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0. La decisión se toma comparando el estimador con el valor crítico.

**Conclusión:** Con α = 0,1, d = 0,14 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: δ = μ(tratadas) - μ(sin tratar) ≤ 0. Se puede asegurar que δ = μ(tratadas) - μ(sin tratar) > 0.

**Respuesta de la guía:** Si, se puede asegurar que la aplicación del tratamiento en la plantación aumenta el rinde de la caña de azúcar.

#### b) Intervalo de confianza (estimar) ✅

*Qué pide:* Pide un valor máximo / mínimo del parámetro con cierta confianza: límite de confianza UNILATERAL.

- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **Modelo**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(tratadas) > S(sin tratar), lo único que se puede sospechar es σ(tratadas) > σ(sin tratar) → unilateral, H0: φ = σ(tratadas)/σ(sin tratar) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 654; ν₂ = 598) = √1,1083 = 1,0527; J = S(tratadas)/S(sin tratar) = 1,0952 → J > Jc: se rechaza H0 → los desvíos son DISTINTOS → Welch.
- ν de Aspin-Welch = (S₁²/n₁ + S₂²/n₂)²/[(S₁²/n₁)²/(n₁-1) + (S₂²/n₂)²/(n₂-1)] = 1.251,9974 → ν = 1251.
- **Relación mínima garantizada** h = μ(tratadas)/μ(sin tratar) (h es una constante, no un parámetro: no se estima): es el h que deja en el límite la condición de rechazo de H0: μ(tratadas) ≤ h·μ(sin tratar) con α = 0,05 (un solo límite: α entero).
- Con Welch ν depende de h (h² entra también en ν), así que se resuelve iterando: x̄(tratadas) - h·x̄(sin tratar) = t(1-α; ν(h))·σ(d*(h)) → h = 1,0109.

**Conclusión:** Con un 95% de confianza, μ(tratadas) es como mínimo un 1,09% mayor que μ(sin tratar) (h = 1,0109).

**Respuesta de la guía:** Se puede esperar un incremento porcentual mínimo del 1,09%.

> 📝 *Notas de la transcripción:* El enunciado empieza en la página 38 y los incisos/Resp están en la 39.

---

### V-21 · Problema 21 (pág. 39)

**Enunciado.** Se emplean dos máquinas para llenar botellas de plástico con un volumen neto medido en cm³. El departamento de control de calidad considera que ambas máquinas llenan las botellas con el mismo volumen neto promedio y además considera que los procesos de llenado son normales, con desviaciones estándares de σA = 0,015 cm³ y σB = 0,018 cm³. Se toma una muestra aleatoria de 10 botellas de la producción de cada máquina, obteniendo los siguientes resultados, visualizados en la siguiente tabla (medidos en cm³): Máquina “A”: 16,03 – 16,04 – 16,05 – 16,05 – 16,02 – 16,01 – 15,96 – 15,98 – 16,02 – 15,99; Máquina “B”: 16,02 – 15,97 – 15,96 – 16,01 – 15,99 – 16,03 – 16,04 – 16,02 – 16,01 – 16,00.

*¿Es posible creer que el departamento de control de calidad esté en lo correcto? (Asumir un riesgo del 5%)*

*Volumen neto (cm³), dos columnas por máquina como en la guía*

| Máquina “A” | Máquina “A” | Máquina “B” | Máquina “B” |
|---|---|---|---|
| 16,03 | 16,01 | 16,02 | 16,03 |
| 16,04 | 15,96 | 15,97 | 16,04 |
| 16,05 | 15,98 | 15,96 | 16,02 |
| 16,05 | 16,02 | 16,01 | 16,01 |
| 16,02 | 15,99 | 15,99 | 16 |

*Tema detectado por la app: Comparación de 2 medias.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Pide tomar una decisión sobre una afirmación: ensayo de hipótesis.

- **1 · Planteo de hipótesis**: H0: δ = μ(Máquina “A”) - μ(Máquina “B”) ≤ 0  vs  H1: δ = μ(Máquina “A”) - μ(Máquina “B”) > 0.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: ¿valen los desvíos afirmados? H0: σ ≤ σ₀ (χ², α = 0,05). Máquina “A”: Sc = σ₀·√(χ²(0,95; 9)/9) = 0,0206 vs S = 0,0303 → se rechaza: σ no es 0,015. Máquina “B”: Sc = 0,0247 vs S = 0,0255 → se rechaza: σ no es 0,018.
- Los desvíos poblacionales no son los afirmados: se los considera desconocidos y se trabaja con S.
- **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Máquina “A”) > S(Máquina “B”), lo único que se puede sospechar es σ(Máquina “A”) > σ(Máquina “B”) → unilateral, H0: φ = σ(Máquina “A”)/σ(Máquina “B”) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 9; ν₂ = 9) = √2,4403 = 1,5622; J = S(Máquina “A”)/S(Máquina “B”) = 1,1875 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 0,027988; ν = n₁ + n₂ - 2 = 18.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(Máquina “A”) - x̄(Máquina “B”) = 0,01; σ(d) = 0,012517, ν = 18.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 0,0217. Si d > 0,0217 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 0,0217, se rechaza H0 → se puede asegurar que δ = μ(Máquina “A”) - μ(Máquina “B”) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Máquina “A”) - μ(Máquina “B”) > 0.
- **6 · Cálculos y decisión**: d = 0,01 → no se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,2174. La decisión se toma comparando el estimador con el valor crítico.
- **Orientación**: el enunciado no da dirección («¿difieren?»), pero en comparaciones no existen ensayos bilaterales: la muestra orienta el ensayo y lo único que se puede intentar probar es que μ(Máquina “A”), el de mayor media muestral, supera a μ(Máquina “B”).

**Conclusión:** Con α = 0,05, d = 0,01 no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula H0: δ = μ(Máquina “A”) - μ(Máquina “B”) ≤ 0. No hay evidencia suficiente para asegurar que δ = μ(Máquina “A”) - μ(Máquina “B”) > 0 (no rechazar H0 no la prueba).

**Respuesta de la guía:** Desvíos conocidos: H0: σA ≤ σA0 = 0,015 cm³, Sc = 0,0206 cm³, SA = 0,0303: se rechaza (el desvío estipulado no es correcto para “A”); H0: σB ≤ σB0 = 0,018 cm³, Sc = 0,0247 cm³, SB = 0,0255: se rechaza (no es correcto para “B”). Igualdad de desvíos: H0: σA ≤ σB (φ = σA/σB), jc = 1,5622 (j²c = 2,4403), j = 1,1875 (j² = 1,4103): no se rechaza, Sa = 0,028 cm³, ν = 18. Medias: H0: μA ≤ μB (δ = μA − μB, δ0 = 0), dc = 0,0217 cm³, d = 16,015 − 16,005 = 0,01 cm³: no se rechaza, se considera que ambas máquinas llenan las botellas con el mismo volumen neto. El departamento de control de calidad está en lo cierto respecto del llenado del volumen neto de ambas máquinas y no está en lo cierto respecto de los desvíos estándares de ambas máquinas.

> 📝 *Notas de la transcripción:* Sin 'Resp:'; respuesta armada desde la Solución. La pregunta es sobre igualdad de medias (bilateral) pero la Solución plantea H0: μA ≤ μB unilateral con t(0,95;18) = 1,7341. Las pruebas de desvío usan χ²(0,95;9) = 16,9190 (unilaterales). La tabla tiene dos columnas por máquina; el orden de los datos aplanados en el planteo es por columna.

<details><summary>Cómo lo concluye la guía</summary>

> Máquina “A”: nA = 10; x̄A = 16,015 cm³; SA = 0,0303 cm³. Máquina “B”: nB = 10; x̄B = 16,005 cm³; SB = 0,0255 cm³.
> Se rechaza la hipótesis nula, se puede asegurar que el desvío poblacional estipulado no es correcto para la máquina “A”.
> Se rechaza la hipótesis nula, se puede asegurar que el desvío poblacional estipulado no es correcto para la máquina “B”.
> Se concluye que ambos desvíos poblacionales son desconocidos, por lo que hay que averiguar si se los puede suponer iguales o se los puede probar distintos.
> De manera que la hipótesis no se rechaza por lo cual no se puede probar que los desvíos poblacionales sean distintos, de manera que se supone que los desvíos poblacionales son iguales.
> De manera que la hipótesis no se rechaza, por lo cual no se puede asegurar que las máquinas llenan las botellas en forma diferente (con distinto volumen neto), se considera que ambas máquinas llenan las botellas con el mismo volumen neto. Por lo cual, se considera que el departamento de control de calidad está en lo cierto respecto al llenado del volumen neto de ambas máquinas y no está en lo cierto respecto de los desvíos estándares de ambas máquinas.

</details>

---

## TEMA VI — Contrastes chi-cuadrado

### VI-1 · Problema 1 (pág. 41)

**Enunciado.** Un economista al servicio de una agencia estatal desea determinar si la proporción de ocupación (ocupados, desocupados y sub-ocupados) en dos grandes áreas urbanas de la provincia son diferentes. Con base en muestras aleatorias de cada área, cada una de 500 y 800 personas respectivamente en cada área, el economista encuentra 35 y 37 personas desocupadas respectivamente en cada área, a su vez, encuentra 165 y 263 personas sub–ocupadas respectivamente en cada área. Bajo las suposiciones adecuadas y con un riesgo del 5%, ¿existe alguna razón para creer que la proporción de ocupación de las dos áreas son diferentes? Tabla: Observados por área (Solución): Atributo | Área 1 | Área 2 | Totales de Atributos; Desocupados (r1) | 35 | 37 | 72; Sub-ocupados (r2) | 165 | 263 | 428; Ocupados (fracasos) | 300 | 500 | 800; Totales de Muestra | 500 | 800 | 1300.

*Con un riesgo del 5%, ¿existe alguna razón para creer que la proporción de ocupación de las dos áreas son diferentes?*

*Observados por área (Solución)*

| Atributo | Área 1 | Área 2 | Totales de Atributos |
|---|---|---|---|
| Desocupados (r1) | 35 | 37 | 72 |
| Sub-ocupados (r2) | 165 | 263 | 428 |
| Ocupados (fracasos) | 300 | 500 | 800 |
| Totales de Muestra | 500 | 800 | 1300 |

*Tema detectado por la app: Chi² — tabla de contingencia (independencia / homogeneidad).*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Es un contraste χ²: se compara χ² calculado contra el crítico.

- **1 · Planteo de hipótesis** (prueba de consistencia —homogeneidad—, se comparan niveles o porcentajes de varios grupos): H0: p₁ = p₂ para cada categoría (Desocupados, Sub-ocupados y Ocupados), siendo pᵢ su proporción en cada grupo (1 = Área 1, 2 = Área 2)  vs  H1: en al menos una categoría las pᵢ son distintas. Al rechazar: alguno es distinto (no «todos son distintos»).
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² = Σ (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ, con ν = (f-1)(c-1) = (3-1)(2-1) = 2 grados de libertad; χ²crítico(1-α; 2) = 5,9915.
- **Modelos y distribuciones empleados**:  
• Con las frecuencias esperadas Fe = (total fila · total columna)/total (con decimales: no se redondean), el estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = (filas - 1)(columnas - 1).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada celda (si no, se amalgaman categorías).
- **4 · Condición de rechazo (CR)**: si χ² > 5,9915 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² = Σ(Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ con la tabla observada. Si χ² > 5,9915, se rechaza H0 → se puede asegurar que la distribución de Desocupados, Sub-ocupados y Ocupados difiere en al menos uno de los grupos: Área 1 y Área 2. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la distribución de Desocupados, Sub-ocupados y Ocupados difiere en al menos uno de los grupos: Área 1 y Área 2.
- **6 · Cálculos y decisión**: frecuencias observadas Oᵢⱼ, esperadas bajo H0 Eᵢⱼ y aporte de cada celda al χ².

*Frecuencias observadas Oᵢⱼ*

| Atributo | Área 1 | Área 2 | **Total** |
|---|---|---|---|
| Desocupados | 35 | 37 | **72** |
| Sub-ocupados | 165 | 263 | **428** |
| Ocupados | 300 | 500 | **800** |
| **Total** | **500** | **800** | **1.300** |

*Frecuencias esperadas Eᵢⱼ = (total fila i · total columna j) / 1.300*

| Atributo | Área 1 | Área 2 | **Total** |
|---|---|---|---|
| Desocupados | 27,6923 | 44,3077 | **72** |
| Sub-ocupados | 164,6154 | 263,3846 | **428** |
| Ocupados | 307,6923 | 492,3077 | **800** |
| **Total** | **500** | **800** | **1.300** |

*Aportes (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ*

| Atributo | Área 1 | Área 2 | **Total** |
|---|---|---|---|
| Desocupados | 1,9284 | 1,2053 | **3,1337** |
| Sub-ocupados | 0,0009 | 0,0006 | **0,0015** |
| Ocupados | 0,1923 | 0,1202 | **0,3125** |
| **Total** | **2,1216** | **1,326** | **χ² = 3,4476** |

χ² = 3,4476 ≤ χ²c = 5,9915 ⇒ no se rechaza H0.


**Conclusión:** Con α = 0,05, χ² = 3,4476 [χ²c = 5,9915; ν = 2] no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula de que la distribución de Desocupados, Sub-ocupados y Ocupados es la misma en Área 1 y Área 2. No hay evidencia suficiente para asegurar que la distribución de Desocupados, Sub-ocupados y Ocupados difiere en al menos uno de los grupos: Área 1 y Área 2 (no rechazar H0 no la prueba).

**Respuesta de la guía:** Pruebas de Consistencia: H0) p1 = p2, α = 0,05. Esperados: 27,6923; 44,3077; 164,6154; 263,3846; 307,6923; 492,3077. χ²calc = 3,4476; ν = (f−1)·(k−1) = 2; χ²(0,95;2) = 5,9915. No se rechaza la hipótesis planteada, de manera que se concluye que no se puede asegurar que la proporción de ocupación en las dos áreas sean diferentes. (Ilustrativo, por atributo: desocupados p̂1,1 = 0,07, p̂2,1 = 0,0463, α* = 0,046 → se rechaza; sub-ocupados p̂1,2 = 0,33, p̂2,2 = 0,3288, α* = 0,505 → no se rechaza; ocupados p̂1,3 = 0,6, p̂2,3 = 0,625, α* = 0,1996 → no se rechaza. Aproximación normal: desocupados gc = 0,0215, g = 0,0237 → se rechaza; sub-ocupados gc = 0,0441, g = 0,0012 → no se rechaza; ocupados gc = 0,0457, g = 0,025 → no se rechaza.)

> 📝 *Notas de la transcripción:* Ejercicio resuelto (sin 'Resp:'); respuesta armada desde la Solución (p. 41-42). La tabla no está en el enunciado: es la de la Solución (observados). Los valores [χ²calc, ν, χ²crít] corresponden al contraste global; la Solución además da resultados por atributo (Fh/Gh y aproximación normal) que rechazan para desocupados.

<details><summary>Cómo lo concluye la guía</summary>

> No se rechaza la hipótesis planteada, de manera que se concluye que no se puede asegurar que la proporción de ocupación en las dos áreas sean diferentes.
> Se rechaza la hipótesis nula, de manera que se concluye que se puede asegurar que el porcentaje de desocupados en las dos áreas es diferente.
> No se rechaza la hipótesis planteada, de manera que se concluye que no se puede asegurar que el porcentaje de sub–ocupados en las dos áreas sea diferente. Por lo cual se llega a la misma conclusión que utilizando las “Pruebas de Consistencia”.
> No se rechaza la hipótesis planteada, de manera que se concluye que no se puede asegurar que el porcentaje de ocupados en las dos áreas sea diferente. Por lo cual se llega a la misma conclusión que utilizando las “Pruebas de Consistencia”.
> Conclusión: la diferencia en las conclusiones obtenidas por Contraste o por el procedimiento adecuado y la aproximación Normal, se debe a que en el Contraste se está evaluando las diferencias de manera global, en cambio en el procedimiento adecuado, se está evaluando la diferencia por cada atributo.

</details>

---

### VI-2 · Problema 2 (pág. 43)

**Enunciado.** Para el tendido de cables en campaña, la empresa de telégrafos utiliza postes de madera de palmito, los que deben ser tratados para evitar la putrefacción en su parte enterrada. Para comparar dos tratamientos distintos, ha colocado alternativamente postes con uno y otro tratamiento, en total 32 postes de cada uno, en una zona baja. Después de 6 años se inspeccionaron a todos los postes y se tienen que reponer 10 que fueron tratados con el método “A” y 20 que fueron tratados con el método “B”. ¿Se puede afirmar que la diferencia es significativa en el porcentaje de fallas, para un riesgo del 2%? Tabla: Método | Postes | Repuestos (fallas); A | 32 | 10; B | 32 | 20.

| Método | Postes | Repuestos (fallas) |
|---|---|---|
| A | 32 | 10 |
| B | 32 | 20 |

*Tema detectado por la app: Chi² — tabla de contingencia (independencia / homogeneidad).*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Es un contraste χ²: se compara χ² calculado contra el crítico.

- **1 · Planteo de hipótesis** (prueba de consistencia —homogeneidad—, se comparan niveles o porcentajes de varios grupos): H0: p₁ = p₂, siendo pᵢ la proporción de «Repuestos (fallas)» en cada método (1 = A, 2 = B)  vs  H1: p₁ ≠ p₂. Al rechazar: alguno es distinto (no «todos son distintos»).
- **2 · Nivel de significación**: α = 0,02 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² = Σ (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ, con ν = (f-1)(c-1) = (2-1)(2-1) = 1 grado de libertad; χ²crítico(1-α; 1) = 5,4119.
- **Modelos y distribuciones empleados**:  
• Con las frecuencias esperadas Fe = (total fila · total columna)/total (con decimales: no se redondean), el estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = (filas - 1)(columnas - 1).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada celda (si no, se amalgaman categorías).
- **4 · Condición de rechazo (CR)**: si χ² > 5,4119 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² = Σ(Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ con la tabla observada. Si χ² > 5,4119, se rechaza H0 → se puede asegurar que la proporción de «Repuestos (fallas)» difiere en al menos uno de los grupos: A y B. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la proporción de «Repuestos (fallas)» difiere en al menos uno de los grupos: A y B.
- **6 · Cálculos y decisión**: frecuencias observadas Oᵢⱼ, esperadas bajo H0 Eᵢⱼ y aporte de cada celda al χ².

*Frecuencias observadas Oᵢⱼ*

| Método | Repuestos (fallas) | No repuestos (fallas) | **Total** |
|---|---|---|---|
| A | 10 | 22 | **32** |
| B | 20 | 12 | **32** |
| **Total** | **30** | **34** | **64** |

*Frecuencias esperadas Eᵢⱼ = (total fila i · total columna j) / 64*

| Método | Repuestos (fallas) | No repuestos (fallas) | **Total** |
|---|---|---|---|
| A | 15 | 17 | **32** |
| B | 15 | 17 | **32** |
| **Total** | **30** | **34** | **64** |

*Aportes (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ*

| Método | Repuestos (fallas) | No repuestos (fallas) | **Total** |
|---|---|---|---|
| A | 1,6667 | 1,4706 | **3,1373** |
| B | 1,6667 | 1,4706 | **3,1373** |
| **Total** | **3,3333** | **2,9412** | **χ² = 6,2745** |

χ² = 6,2745 > χ²c = 5,4119 ⇒ se rechaza H0.


**Conclusión:** Con α = 0,02, χ² = 6,2745 [χ²c = 5,4119; ν = 1] cae en la zona de rechazo ⇒ se rechaza la hipótesis nula de que la proporción de «Repuestos (fallas)» es la misma en A y B. Se puede asegurar que la proporción de «Repuestos (fallas)» difiere en al menos uno de los grupos: A y B.

**Respuesta de la guía:** Resp: Se puede asegurar que la diferencia es significativa, el método “A” es mejor que el “B”.

> 📝 *Notas de la transcripción:* Tabla armada a partir del texto (no hay tabla en la guía).

---

### VI-3 · Problema 3 (pág. 43)

**Enunciado.** Un proveedor suministra grandes lotes de conos de hilo vacíos con un porcentaje alto de defectuosos. Se considera la posibilidad de cambiar por otro proveedor cuyo producto es más caro pero que se espera tenga un porcentaje de defectuosos considerablemente menor. Se le hizo un pedido y se tomó una muestra de 250 conos, que arrojó un resultado de 20 defectuosos. Con el proveedor habitual, se tomó una muestra de 500 conos que arrojó un resultado de 75 defectuosos. Se considera que el resultado de las pruebas es concluyente para cambiar de proveedor, para un riesgo del 1%. Tabla: Proveedor | Muestra | Defectuosos; Nuevo | 250 | 20; Habitual | 500 | 75.

*¿El resultado de las pruebas es concluyente para cambiar de proveedor, para un riesgo del 1%?*

| Proveedor | Muestra | Defectuosos |
|---|---|---|
| Nuevo | 250 | 20 |
| Habitual | 500 | 75 |

*Tema detectado por la app: Chi² — tabla de contingencia (independencia / homogeneidad).*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Es un contraste χ²: se compara χ² calculado contra el crítico.

- **1 · Planteo de hipótesis** (prueba de consistencia —homogeneidad—, se comparan niveles o porcentajes de varios grupos): H0: p₁ = p₂, siendo pᵢ la proporción de «Defectuosos» en cada proveedor (1 = Nuevo, 2 = Habitual)  vs  H1: p₁ ≠ p₂. Al rechazar: alguno es distinto (no «todos son distintos»).
- **2 · Nivel de significación**: α = 0,01 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² = Σ (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ, con ν = (f-1)(c-1) = (2-1)(2-1) = 1 grado de libertad; χ²crítico(1-α; 1) = 6,6349.
- **Modelos y distribuciones empleados**:  
• Con las frecuencias esperadas Fe = (total fila · total columna)/total (con decimales: no se redondean), el estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = (filas - 1)(columnas - 1).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada celda (si no, se amalgaman categorías).
- **4 · Condición de rechazo (CR)**: si χ² > 6,6349 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² = Σ(Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ con la tabla observada. Si χ² > 6,6349, se rechaza H0 → se puede asegurar que la proporción de «Defectuosos» difiere en al menos uno de los grupos: Nuevo y Habitual. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la proporción de «Defectuosos» difiere en al menos uno de los grupos: Nuevo y Habitual.
- **6 · Cálculos y decisión**: frecuencias observadas Oᵢⱼ, esperadas bajo H0 Eᵢⱼ y aporte de cada celda al χ².

*Frecuencias observadas Oᵢⱼ*

| Proveedor | Defectuosos | No defectuosos | **Total** |
|---|---|---|---|
| Nuevo | 20 | 230 | **250** |
| Habitual | 75 | 425 | **500** |
| **Total** | **95** | **655** | **750** |

*Frecuencias esperadas Eᵢⱼ = (total fila i · total columna j) / 750*

| Proveedor | Defectuosos | No defectuosos | **Total** |
|---|---|---|---|
| Nuevo | 31,6667 | 218,3333 | **250** |
| Habitual | 63,3333 | 436,6667 | **500** |
| **Total** | **95** | **655** | **750** |

*Aportes (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ*

| Proveedor | Defectuosos | No defectuosos | **Total** |
|---|---|---|---|
| Nuevo | 4,2982 | 0,6234 | **4,9217** |
| Habitual | 2,1491 | 0,3117 | **2,4608** |
| **Total** | **6,4474** | **0,9351** | **χ² = 7,3825** |

χ² = 7,3825 > χ²c = 6,6349 ⇒ se rechaza H0.


**Conclusión:** Con α = 0,01, χ² = 7,3825 [χ²c = 6,6349; ν = 1] cae en la zona de rechazo ⇒ se rechaza la hipótesis nula de que la proporción de «Defectuosos» es la misma en Nuevo y Habitual. Se puede asegurar que la proporción de «Defectuosos» difiere en al menos uno de los grupos: Nuevo y Habitual.

**Respuesta de la guía:** Resp: Se puede asegurar que los porcentajes de defectuosos son diferentes, se aconseja cambiar de proveedor.

> 📝 *Notas de la transcripción:* Tabla armada a partir del texto. La consigna está redactada como afirmación ("Se considera que...") y no como pregunta.

---

### VI-4 · Problema 4 (pág. 43)

**Enunciado.** Una hilandería tiene 4 plantas similares que producen el mismo tipo de hilo. Con respecto a su elongación de rotura, el hilo se clasifica como de elongación baja (que se considera defectuoso), de elongación media (de 1ª calidad) y elongación alta (de 2ª calidad). Se tomaron muestras de 200 unidades en las 4 plantas, con los siguientes resultados: En la planta 1 se encontró 10 unidades de elongación baja, 176 unidades de elongación media y 14 unidades de elongación alta; en la planta 2 se encontró 16 unidades de elongación baja, 178 unidades de elongación media y 6 unidades de elongación alta; en la planta 3 se encontró 17 unidades de elongación baja, 174 unidades de elongación media y 9 unidades de elongación alta; en la planta 4 se encontró 8 unidades de elongación baja, 173 unidades de elongación media y 19 unidades de elongación alta. ¿Se puede asegurar que las proporciones en las 4 plantas es diferente? Tabla: Unidades por elongación (muestras de 200 por planta): Planta | Elongación baja | Elongación media | Elongación alta; 1 | 10 | 176 | 14; 2 | 16 | 178 | 6; 3 | 17 | 174 | 9; 4 | 8 | 173 | 19.

*Unidades por elongación (muestras de 200 por planta)*

| Planta | Elongación baja | Elongación media | Elongación alta |
|---|---|---|---|
| 1 | 10 | 176 | 14 |
| 2 | 16 | 178 | 6 |
| 3 | 17 | 174 | 9 |
| 4 | 8 | 173 | 19 |

*Tema detectado por la app: Chi² — tabla de contingencia (independencia / homogeneidad).*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Es un contraste χ²: se compara χ² calculado contra el crítico.

- **1 · Planteo de hipótesis** (prueba de consistencia —homogeneidad—, se comparan niveles o porcentajes de varios grupos): H0: p₁ = p₂ = p₃ = p₄ para cada categoría (Elongación baja, Elongación media y Elongación alta), siendo pᵢ su proporción en cada planta (1 = Planta 1, 2 = Planta 2, 3 = Planta 3, 4 = Planta 4)  vs  H1: en al menos una categoría las pᵢ son distintas. Al rechazar: alguno es distinto (no «todos son distintos»).
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² = Σ (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ, con ν = (f-1)(c-1) = (4-1)(3-1) = 6 grados de libertad; χ²crítico(1-α; 6) = 12,5916.
- **Modelos y distribuciones empleados**:  
• Con las frecuencias esperadas Fe = (total fila · total columna)/total (con decimales: no se redondean), el estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = (filas - 1)(columnas - 1).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada celda (si no, se amalgaman categorías).
- **4 · Condición de rechazo (CR)**: si χ² > 12,5916 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² = Σ(Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ con la tabla observada. Si χ² > 12,5916, se rechaza H0 → se puede asegurar que la distribución de Elongación baja, Elongación media y Elongación alta difiere en al menos uno de los grupos: Planta 1, Planta 2, Planta 3 y Planta 4. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la distribución de Elongación baja, Elongación media y Elongación alta difiere en al menos uno de los grupos: Planta 1, Planta 2, Planta 3 y Planta 4.
- **6 · Cálculos y decisión**: frecuencias observadas Oᵢⱼ, esperadas bajo H0 Eᵢⱼ y aporte de cada celda al χ².

*Frecuencias observadas Oᵢⱼ*

| Planta | Elongación baja | Elongación media | Elongación alta | **Total** |
|---|---|---|---|---|
| Planta 1 | 10 | 176 | 14 | **200** |
| Planta 2 | 16 | 178 | 6 | **200** |
| Planta 3 | 17 | 174 | 9 | **200** |
| Planta 4 | 8 | 173 | 19 | **200** |
| **Total** | **51** | **701** | **48** | **800** |

*Frecuencias esperadas Eᵢⱼ = (total fila i · total columna j) / 800*

| Planta | Elongación baja | Elongación media | Elongación alta | **Total** |
|---|---|---|---|---|
| Planta 1 | 12,75 | 175,25 | 12 | **200** |
| Planta 2 | 12,75 | 175,25 | 12 | **200** |
| Planta 3 | 12,75 | 175,25 | 12 | **200** |
| Planta 4 | 12,75 | 175,25 | 12 | **200** |
| **Total** | **51** | **701** | **48** | **800** |

*Aportes (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ*

| Planta | Elongación baja | Elongación media | Elongación alta | **Total** |
|---|---|---|---|---|
| Planta 1 | 0,5931 | 0,0032 | 0,3333 | **0,9297** |
| Planta 2 | 0,8284 | 0,0432 | 3 | **3,8716** |
| Planta 3 | 1,4167 | 0,0089 | 0,75 | **2,1756** |
| Planta 4 | 1,7696 | 0,0289 | 4,0833 | **5,8818** |
| **Total** | **4,6078** | **0,0842** | **8,1667** | **χ² = 12,8587** |

χ² = 12,8587 > χ²c = 12,5916 ⇒ se rechaza H0.


**Conclusión:** Con α = 0,05, χ² = 12,8587 [χ²c = 12,5916; ν = 6] cae en la zona de rechazo ⇒ se rechaza la hipótesis nula de que la distribución de Elongación baja, Elongación media y Elongación alta es la misma en Planta 1, Planta 2, Planta 3 y Planta 4. Se puede asegurar que la distribución de Elongación baja, Elongación media y Elongación alta difiere en al menos uno de los grupos: Planta 1, Planta 2, Planta 3 y Planta 4.

**Respuesta de la guía:** Resp: Se puede asegurar que las proporciones de elongación en las 4 plantas son diferentes.

> 📝 *Notas de la transcripción:* Tabla armada a partir del texto. La consigna no indica riesgo. La planta 4 suma 8+173+19 = 200 y las demás también suman 200.

---

### VI-5 · Problema 5 (pág. 43)

**Enunciado.** En un taller metalúrgico se produce un tipo de biela para abastecer a una fábrica automotriz. Se toman nuestras semanales de 300 piezas y se efectúa un recuento de la cantidad de defectuosas. El control mensual consiste en verificar si no hubo variación semanal en el porcentaje de defectuosas. El último mes se obtuvo el siguiente resultado: la primera semana se observó 21 defectuosas; la segunda semana se observó 12 defectuosas; la tercera semana se observó 14 defectuosas, y, la cuarta semana se observó 11 defectuosas. ¿Se considera que los datos son concluyentes para afirmar que ha variado el porcentaje de defectuosas? Tabla: Muestras semanales de 300 piezas: Semana | Defectuosas | Muestra; 1 | 21 | 300; 2 | 12 | 300; 3 | 14 | 300; 4 | 11 | 300.

*Muestras semanales de 300 piezas*

| Semana | Defectuosas | Muestra |
|---|---|---|
| 1 | 21 | 300 |
| 2 | 12 | 300 |
| 3 | 14 | 300 |
| 4 | 11 | 300 |

*Tema detectado por la app: Chi² — tabla de contingencia (independencia / homogeneidad).*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Es un contraste χ²: se compara χ² calculado contra el crítico.

- **1 · Planteo de hipótesis** (prueba de consistencia —homogeneidad—, se comparan niveles o porcentajes de varios grupos): H0: p₁ = p₂ = p₃ = p₄, siendo pᵢ la proporción de «Defectuosas» en cada semana (1 = Semana 1, 2 = Semana 2, 3 = Semana 3, 4 = Semana 4)  vs  H1: al menos una pᵢ es distinta. Al rechazar: alguno es distinto (no «todos son distintos»).
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² = Σ (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ, con ν = (f-1)(c-1) = (4-1)(2-1) = 3 grados de libertad; χ²crítico(1-α; 3) = 7,8147.
- **Modelos y distribuciones empleados**:  
• Con las frecuencias esperadas Fe = (total fila · total columna)/total (con decimales: no se redondean), el estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = (filas - 1)(columnas - 1).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada celda (si no, se amalgaman categorías).
- **4 · Condición de rechazo (CR)**: si χ² > 7,8147 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² = Σ(Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ con la tabla observada. Si χ² > 7,8147, se rechaza H0 → se puede asegurar que la proporción de «Defectuosas» difiere en al menos uno de los grupos: Semana 1, Semana 2, Semana 3 y Semana 4. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la proporción de «Defectuosas» difiere en al menos uno de los grupos: Semana 1, Semana 2, Semana 3 y Semana 4.
- **6 · Cálculos y decisión**: frecuencias observadas Oᵢⱼ, esperadas bajo H0 Eᵢⱼ y aporte de cada celda al χ².

*Frecuencias observadas Oᵢⱼ*

| Semana | Defectuosas | No defectuosas | **Total** |
|---|---|---|---|
| Semana 1 | 21 | 279 | **300** |
| Semana 2 | 12 | 288 | **300** |
| Semana 3 | 14 | 286 | **300** |
| Semana 4 | 11 | 289 | **300** |
| **Total** | **58** | **1.142** | **1.200** |

*Frecuencias esperadas Eᵢⱼ = (total fila i · total columna j) / 1.200*

| Semana | Defectuosas | No defectuosas | **Total** |
|---|---|---|---|
| Semana 1 | 14,5 | 285,5 | **300** |
| Semana 2 | 14,5 | 285,5 | **300** |
| Semana 3 | 14,5 | 285,5 | **300** |
| Semana 4 | 14,5 | 285,5 | **300** |
| **Total** | **58** | **1.142** | **1.200** |

*Aportes (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ*

| Semana | Defectuosas | No defectuosas | **Total** |
|---|---|---|---|
| Semana 1 | 2,9138 | 0,148 | **3,0618** |
| Semana 2 | 0,431 | 0,0219 | **0,4529** |
| Semana 3 | 0,0172 | 0,0009 | **0,0181** |
| Semana 4 | 0,8448 | 0,0429 | **0,8877** |
| **Total** | **4,2069** | **0,2137** | **χ² = 4,4206** |

χ² = 4,4206 ≤ χ²c = 7,8147 ⇒ no se rechaza H0.


**Conclusión:** Con α = 0,05, χ² = 4,4206 [χ²c = 7,8147; ν = 3] no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula de que la proporción de «Defectuosas» es la misma en Semana 1, Semana 2, Semana 3 y Semana 4. No hay evidencia suficiente para asegurar que la proporción de «Defectuosas» difiere en al menos uno de los grupos: Semana 1, Semana 2, Semana 3 y Semana 4 (no rechazar H0 no la prueba).

**Respuesta de la guía:** Resp: No se puede asegurar que los porcentajes de defectuosas haya variado.

> 📝 *Notas de la transcripción:* Tabla armada a partir del texto. La consigna no indica riesgo. "nuestras" es errata de la guía por "muestras" (se transcribe tal cual).

---

### VI-6 · Problema 6 (pág. 43)

**Enunciado.** En una empresa que se trabaja 3 turnos se tienen la clasificación de los niveles de calidad fabricados en cada turno: En el turno mañana, sobre una muestra de 500 piezas se observan 450 piezas de primera calidad, 45 piezas de segunda calidad y 5 piezas defectuosas; en el turno tarde sobre 800 piezas se observaron 680 piezas de primera calidad, 80 piezas de segunda calidad y 40 piezas defectuosas, y, en el turno noche sobre 400 piezas se observaron 320 piezas de primera calidad, 40 piezas de segunda y 40 piezas defectuosas. Para un riesgo del 1%, ¿se puede asegurar que los niveles de calidad en los tres turnos difieren? Tabla: Turno | Primera calidad | Segunda calidad | Defectuosas | Muestra; Mañana | 450 | 45 | 5 | 500; Tarde | 680 | 80 | 40 | 800; Noche | 320 | 40 | 40 | 400.

| Turno | Primera calidad | Segunda calidad | Defectuosas | Muestra |
|---|---|---|---|---|
| Mañana | 450 | 45 | 5 | 500 |
| Tarde | 680 | 80 | 40 | 800 |
| Noche | 320 | 40 | 40 | 400 |

*Tema detectado por la app: Chi² — tabla de contingencia (independencia / homogeneidad).*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Es un contraste χ²: se compara χ² calculado contra el crítico.

- **1 · Planteo de hipótesis** (prueba de consistencia —homogeneidad—, se comparan niveles o porcentajes de varios grupos): H0: p₁ = p₂ = p₃ para cada categoría (Primera calidad, Segunda calidad y Defectuosas), siendo pᵢ su proporción en cada turno (1 = Mañana, 2 = Tarde, 3 = Noche)  vs  H1: en al menos una categoría las pᵢ son distintas. Al rechazar: alguno es distinto (no «todos son distintos»).
- **2 · Nivel de significación**: α = 0,01 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² = Σ (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ, con ν = (f-1)(c-1) = (3-1)(3-1) = 4 grados de libertad; χ²crítico(1-α; 4) = 13,2767.
- **Modelos y distribuciones empleados**:  
• Con las frecuencias esperadas Fe = (total fila · total columna)/total (con decimales: no se redondean), el estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = (filas - 1)(columnas - 1).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada celda (si no, se amalgaman categorías).
- **4 · Condición de rechazo (CR)**: si χ² > 13,2767 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² = Σ(Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ con la tabla observada. Si χ² > 13,2767, se rechaza H0 → se puede asegurar que la distribución de Primera calidad, Segunda calidad y Defectuosas difiere en al menos uno de los grupos: Mañana, Tarde y Noche. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la distribución de Primera calidad, Segunda calidad y Defectuosas difiere en al menos uno de los grupos: Mañana, Tarde y Noche.
- **6 · Cálculos y decisión**: frecuencias observadas Oᵢⱼ, esperadas bajo H0 Eᵢⱼ y aporte de cada celda al χ².

*Frecuencias observadas Oᵢⱼ*

| Turno | Primera calidad | Segunda calidad | Defectuosas | **Total** |
|---|---|---|---|---|
| Mañana | 450 | 45 | 5 | **500** |
| Tarde | 680 | 80 | 40 | **800** |
| Noche | 320 | 40 | 40 | **400** |
| **Total** | **1.450** | **165** | **85** | **1.700** |

*Frecuencias esperadas Eᵢⱼ = (total fila i · total columna j) / 1.700*

| Turno | Primera calidad | Segunda calidad | Defectuosas | **Total** |
|---|---|---|---|---|
| Mañana | 426,4706 | 48,5294 | 25 | **500** |
| Tarde | 682,3529 | 77,6471 | 40 | **800** |
| Noche | 341,1765 | 38,8235 | 20 | **400** |
| **Total** | **1.450** | **165** | **85** | **1.700** |

*Aportes (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ*

| Turno | Primera calidad | Segunda calidad | Defectuosas | **Total** |
|---|---|---|---|---|
| Mañana | 1,2982 | 0,2567 | 16 | **17,5549** |
| Tarde | 0,0081 | 0,0713 | 0 | **0,0794** |
| Noche | 1,3144 | 0,0357 | 20 | **21,3501** |
| **Total** | **2,6207** | **0,3636** | **36** | **χ² = 38,9843** |

χ² = 38,9843 > χ²c = 13,2767 ⇒ se rechaza H0.


**Conclusión:** Con α = 0,01, χ² = 38,9843 [χ²c = 13,2767; ν = 4] cae en la zona de rechazo ⇒ se rechaza la hipótesis nula de que la distribución de Primera calidad, Segunda calidad y Defectuosas es la misma en Mañana, Tarde y Noche. Se puede asegurar que la distribución de Primera calidad, Segunda calidad y Defectuosas difiere en al menos uno de los grupos: Mañana, Tarde y Noche.

**Respuesta de la guía:** Resp: Se puede asegurar que los niveles de calidad en los tres turnos son diferentes.

> 📝 *Notas de la transcripción:* Tabla armada a partir del texto.

---

### VI-7 · Problema 7 (pág. 43)

**Enunciado.** En una fábrica de automotores se han recibido reclamos por fallas de pintura en los automóviles. Se supone que todo cliente que detecta una falla efectúa el reclamo en fábrica. La producción del último año fue de: 550 autos blancos, 450 azules, 480 rojos y 320 verdes. Se han presentado un total de 300 reclamos de los cuales el 30% es propietario de autos blancos, otro 30% de azules, el 25% de rojos y el 15% de verdes. Para un riesgo del 5%, ¿se puede considerar que los resultados son una prueba concluyente para afirmar que existe asociación entre el color de los autos y el porcentaje de fallas por pintura? Tabla: Color | Producción (autos) | % de los 300 reclamos; Blanco | 550 | 30; Azul | 450 | 30; Rojo | 480 | 25; Verde | 320 | 15.

| Color | Producción (autos) | % de los 300 reclamos |
|---|---|---|
| Blanco | 550 | 30 |
| Azul | 450 | 30 |
| Rojo | 480 | 25 |
| Verde | 320 | 15 |

*Tema detectado por la app: Chi² — tabla de contingencia (independencia / homogeneidad).*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Es un contraste χ²: se compara χ² calculado contra el crítico.

- **1 · Planteo de hipótesis** (prueba de independencia: se pregunta por una asociación): H0: color es independiente de la clasificación en Con reclamo y Sin reclamo; equivale a p₁ = p₂ = p₃ = p₄, siendo pᵢ la proporción con reclamo en cada color (1 = Blanco, 2 = Azul, 3 = Rojo, 4 = Verde)  vs  H1: hay asociación entre las dos clasificaciones. No rechazar H0 no prueba la independencia.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² = Σ (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ, con ν = (f-1)(c-1) = (4-1)(2-1) = 3 grados de libertad; χ²crítico(1-α; 3) = 7,8147.
- **Modelos y distribuciones empleados**:  
• Con las frecuencias esperadas Fe = (total fila · total columna)/total (con decimales: no se redondean), el estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = (filas - 1)(columnas - 1).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada celda (si no, se amalgaman categorías).
- **4 · Condición de rechazo (CR)**: si χ² > 7,8147 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² = Σ(Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ con la tabla observada. Si χ² > 7,8147, se rechaza H0 → se puede asegurar que existe asociación entre color y la clasificación en Con reclamo y Sin reclamo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que existe asociación entre color y la clasificación en Con reclamo y Sin reclamo.
- **6 · Cálculos y decisión**: frecuencias observadas Oᵢⱼ, esperadas bajo H0 Eᵢⱼ y aporte de cada celda al χ².

*Frecuencias observadas Oᵢⱼ*

| Color | Con reclamo | Sin reclamo | **Total** |
|---|---|---|---|
| Blanco | 90 | 460 | **550** |
| Azul | 90 | 360 | **450** |
| Rojo | 75 | 405 | **480** |
| Verde | 45 | 275 | **320** |
| **Total** | **300** | **1.500** | **1.800** |

*Frecuencias esperadas Eᵢⱼ = (total fila i · total columna j) / 1.800*

| Color | Con reclamo | Sin reclamo | **Total** |
|---|---|---|---|
| Blanco | 91,6667 | 458,3333 | **550** |
| Azul | 75 | 375 | **450** |
| Rojo | 80 | 400 | **480** |
| Verde | 53,3333 | 266,6667 | **320** |
| **Total** | **300** | **1.500** | **1.800** |

*Aportes (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ*

| Color | Con reclamo | Sin reclamo | **Total** |
|---|---|---|---|
| Blanco | 0,0303 | 0,0061 | **0,0364** |
| Azul | 3 | 0,6 | **3,6** |
| Rojo | 0,3125 | 0,0625 | **0,375** |
| Verde | 1,3021 | 0,2604 | **1,5625** |
| **Total** | **4,6449** | **0,929** | **χ² = 5,5739** |

χ² = 5,5739 ≤ χ²c = 7,8147 ⇒ no se rechaza H0.


**Conclusión:** Con α = 0,05, χ² = 5,5739 [χ²c = 7,8147; ν = 3] no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula de que color es independiente de la clasificación en Con reclamo y Sin reclamo. No hay evidencia suficiente para asegurar que existe asociación entre color y la clasificación en Con reclamo y Sin reclamo (no rechazar H0 no la prueba).

**Respuesta de la guía:** Resp: No se puede asegurar que exista relación entre el color de los autos y el porcentaje de fallas por pintura.

> 📝 *Notas de la transcripción:* Enunciado entre p. 43 y 44 (se toma pagina 43). Tabla armada a partir del texto; reclamos en cantidad: 90, 90, 75, 45.

---

### VI-8 · Problema 8 (pág. 44)

**Enunciado.** Con el objeto de orientar su publicidad para neutralizar el efecto de la competencia, una empresa productora de artículos de consumo masivo ha realizado un ensayo sobre la preferencia del público en las distintas zonas del país, obteniendo estos resultados: Tabla: Preferencia | A | B | C | D | E; Empresa | 36 | 20 | 28 | 33 | 16; Competencia | 44 | 30 | 12 | 17 | 24.

*¿Se considera que existe evidencia para afirmar que ambas variables están asociadas?*

| Preferencia | A | B | C | D | E |
|---|---|---|---|---|---|
| Empresa | 36 | 20 | 28 | 33 | 16 |
| Competencia | 44 | 30 | 12 | 17 | 24 |

*Tema detectado por la app: Chi² — tabla de contingencia (independencia / homogeneidad).*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Es un contraste χ²: se compara χ² calculado contra el crítico.

- **1 · Planteo de hipótesis** (prueba de independencia: se pregunta por una asociación): H0: preferencia es independiente de la clasificación en A, B, C, D y E; equivale a p₁ = p₂ = … = p₅, siendo pᵢ la proporción de «Empresa» en cada grupo (1 = A, 2 = B, 3 = C, 4 = D, 5 = E)  vs  H1: hay asociación entre las dos clasificaciones. No rechazar H0 no prueba la independencia.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² = Σ (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ, con ν = (f-1)(c-1) = (2-1)(5-1) = 4 grados de libertad; χ²crítico(1-α; 4) = 9,4877.
- **Modelos y distribuciones empleados**:  
• Con las frecuencias esperadas Fe = (total fila · total columna)/total (con decimales: no se redondean), el estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = (filas - 1)(columnas - 1).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada celda (si no, se amalgaman categorías).
- **4 · Condición de rechazo (CR)**: si χ² > 9,4877 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² = Σ(Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ con la tabla observada. Si χ² > 9,4877, se rechaza H0 → se puede asegurar que existe asociación entre preferencia y la clasificación en A, B, C, D y E. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que existe asociación entre preferencia y la clasificación en A, B, C, D y E.
- **6 · Cálculos y decisión**: frecuencias observadas Oᵢⱼ, esperadas bajo H0 Eᵢⱼ y aporte de cada celda al χ².

*Frecuencias observadas Oᵢⱼ*

| Preferencia | A | B | C | D | E | **Total** |
|---|---|---|---|---|---|---|
| Empresa | 36 | 20 | 28 | 33 | 16 | **133** |
| Competencia | 44 | 30 | 12 | 17 | 24 | **127** |
| **Total** | **80** | **50** | **40** | **50** | **40** | **260** |

*Frecuencias esperadas Eᵢⱼ = (total fila i · total columna j) / 260*

| Preferencia | A | B | C | D | E | **Total** |
|---|---|---|---|---|---|---|
| Empresa | 40,9231 | 25,5769 | 20,4615 | 25,5769 | 20,4615 | **133** |
| Competencia | 39,0769 | 24,4231 | 19,5385 | 24,4231 | 19,5385 | **127** |
| **Total** | **80** | **50** | **40** | **50** | **40** | **260** |

*Aportes (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ*

| Preferencia | A | B | C | D | E | **Total** |
|---|---|---|---|---|---|---|
| Empresa | 0,5922 | 1,216 | 2,7773 | 2,1544 | 0,9728 | **7,7128** |
| Competencia | 0,6202 | 1,2735 | 2,9085 | 2,2561 | 1,0188 | **8,0772** |
| **Total** | **1,2125** | **2,4895** | **5,6859** | **4,4105** | **1,9916** | **χ² = 15,7899** |

χ² = 15,7899 > χ²c = 9,4877 ⇒ se rechaza H0.


**Conclusión:** Con α = 0,05, χ² = 15,7899 [χ²c = 9,4877; ν = 4] cae en la zona de rechazo ⇒ se rechaza la hipótesis nula de que preferencia es independiente de la clasificación en A, B, C, D y E. Se puede asegurar que existe asociación entre preferencia y la clasificación en A, B, C, D y E.

**Respuesta de la guía:** Resp: Sí, la preferencia del público, a una marca, depende de la zona en donde se comercializa.

> 📝 *Notas de la transcripción:* La consigna no indica riesgo. Columnas A-E son las Zonas.

---

### VI-9 · Problema 9 (pág. 44)

**Enunciado.** Una cadena de perfumerías tiene en exclusividad los productos de una determinada marca. Uno de ellos, es un desodorante para dama, el cual se ofrece en 4 fragancias: “Neutro”, “Lavanda”, “Deportivo” y “Fresh”. Se registraron las preferencias de las clientas en 3 locales, con los siguientes resultados: Tabla: Local | Neutro | Lavanda | Deportivo | Fresh; Local 1 | 32 | 45 | 23 | 28; Local 2 | 14 | 51 | 15 | 14; Local 3 | 14 | 14 | 12 | 8.

*¿Se puede asegurar, con un 10% de riesgo, que las preferencias a las distintas fragancias difieren entre los locales en donde se comercializan? Indique claramente la hipótesis nula que ensaya.*

| Local | Neutro | Lavanda | Deportivo | Fresh |
|---|---|---|---|---|
| Local 1 | 32 | 45 | 23 | 28 |
| Local 2 | 14 | 51 | 15 | 14 |
| Local 3 | 14 | 14 | 12 | 8 |

*Tema detectado por la app: Chi² — tabla de contingencia (independencia / homogeneidad).*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Es un contraste χ²: se compara χ² calculado contra el crítico.

- **1 · Planteo de hipótesis** (prueba de independencia: se pregunta por una asociación): H0: local es independiente de la clasificación en Neutro, Lavanda, Deportivo y Fresh; equivale a p₁ = p₂ = p₃ para cada categoría (Neutro, Lavanda, Deportivo y Fresh), siendo pᵢ su proporción en cada local (1 = Local 1, 2 = Local 2, 3 = Local 3)  vs  H1: hay asociación entre las dos clasificaciones. No rechazar H0 no prueba la independencia.
- **2 · Nivel de significación**: α = 0,1 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: χ² = Σ (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ, con ν = (f-1)(c-1) = (3-1)(4-1) = 6 grados de libertad; χ²crítico(1-α; 6) = 10,6446.
- **Modelos y distribuciones empleados**:  
• Con las frecuencias esperadas Fe = (total fila · total columna)/total (con decimales: no se redondean), el estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = (filas - 1)(columnas - 1).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada celda (si no, se amalgaman categorías).
- **4 · Condición de rechazo (CR)**: si χ² > 10,6446 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² = Σ(Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ con la tabla observada. Si χ² > 10,6446, se rechaza H0 → se puede asegurar que existe asociación entre local y la clasificación en Neutro, Lavanda, Deportivo y Fresh. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que existe asociación entre local y la clasificación en Neutro, Lavanda, Deportivo y Fresh.
- **6 · Cálculos y decisión**: frecuencias observadas Oᵢⱼ, esperadas bajo H0 Eᵢⱼ y aporte de cada celda al χ².

*Frecuencias observadas Oᵢⱼ*

| Local | Neutro | Lavanda | Deportivo | Fresh | **Total** |
|---|---|---|---|---|---|
| Local 1 | 32 | 45 | 23 | 28 | **128** |
| Local 2 | 14 | 51 | 15 | 14 | **94** |
| Local 3 | 14 | 14 | 12 | 8 | **48** |
| **Total** | **60** | **110** | **50** | **50** | **270** |

*Frecuencias esperadas Eᵢⱼ = (total fila i · total columna j) / 270*

| Local | Neutro | Lavanda | Deportivo | Fresh | **Total** |
|---|---|---|---|---|---|
| Local 1 | 28,4444 | 52,1481 | 23,7037 | 23,7037 | **128** |
| Local 2 | 20,8889 | 38,2963 | 17,4074 | 17,4074 | **94** |
| Local 3 | 10,6667 | 19,5556 | 8,8889 | 8,8889 | **48** |
| **Total** | **60** | **110** | **50** | **50** | **270** |

*Aportes (Oᵢⱼ - Eᵢⱼ)²/Eᵢⱼ*

| Local | Neutro | Lavanda | Deportivo | Fresh | **Total** |
|---|---|---|---|---|---|
| Local 1 | 0,4444 | 0,9798 | 0,0209 | 0,7787 | **2,2239** |
| Local 2 | 2,2719 | 4,2141 | 0,3329 | 0,667 | **7,4859** |
| Local 3 | 1,0417 | 1,5783 | 1,0889 | 0,0889 | **3,7977** |
| **Total** | **3,758** | **6,7722** | **1,4427** | **1,5346** | **χ² = 13,5075** |

χ² = 13,5075 > χ²c = 10,6446 ⇒ se rechaza H0.


**Conclusión:** Con α = 0,1, χ² = 13,5075 [χ²c = 10,6446; ν = 6] cae en la zona de rechazo ⇒ se rechaza la hipótesis nula de que local es independiente de la clasificación en Neutro, Lavanda, Deportivo y Fresh. Se puede asegurar que existe asociación entre local y la clasificación en Neutro, Lavanda, Deportivo y Fresh.

**Respuesta de la guía:** H0) “La preferencia a una determinada fragancia es independiente del local donde se comercializa el desodorante”, α = 0,10. Esperados: Loc 1: 28,4444; 52,1481; 23,7037; 23,7037; Loc 2: 20,8889; 38,2963; 17,4074; 17,4074; Loc 3: 10,6667; 19,5556; 8,8889; 8,8889. χ²calc = 13,5075; ν = (f−1)·(k−1) = 6; χ²(0,90;6) = 10,6446. Se rechaza la hipótesis planteada, de manera que se concluye que la preferencia de cada fragancia depende del local donde se comercializa o sea que las preferencias difieren entre los locales.

> 📝 *Notas de la transcripción:* Ejercicio resuelto (sin 'Resp:'); respuesta armada desde la Solución (p. 44-45). Totales: filas 128, 94, 48; columnas 60, 110, 50, 50; total 270.

<details><summary>Cómo lo concluye la guía</summary>

> Se rechaza la hipótesis planteada, de manera que se concluye que la preferencia de cada fragancia depende del local donde se comercializa o sea que las preferencias difieren entre los locales.

</details>

---

### VI-10 · Problema 10 (pág. 45)

**Enunciado.** Se desea verificar si un dado está cargado. A tal efecto se lo arrojó 60 veces, obteniendo los siguientes resultados: Tabla: Número obtenido | Cantidad de ocurrencias; 1 | 14; 2 | 6; 3 | 6; 4 | 13; 5 | 16; 6 | 5.

*¿Se puede asegurar, con probabilidad de error de 0,05, que este dado esté cargado?*

| Número obtenido | Cantidad de ocurrencias |
|---|---|
| 1 | 14 |
| 2 | 6 |
| 3 | 6 |
| 4 | 13 |
| 5 | 16 |
| 6 | 5 |

*Tema detectado por la app: Chi² — bondad de ajuste.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Bondad de ajuste χ² al modelo Uniforme discreto: se compara χ² calculado contra el crítico.

- **— Modelo Uniforme discreto —**
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Uniforme discreto  vs  H1: no lo sigue.  α = 0,05.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| 1 | 14 | 0,1667 | 10 | 1,6 |
| 2 | 6 | 0,1667 | 10 | 1,6 |
| 3 | 6 | 0,1667 | 10 | 1,6 |
| 4 | 13 | 0,1667 | 10 | 0,9 |
| 5 | 16 | 0,1667 | 10 | 3,6 |
| 6 | 5 | 0,1667 | 10 | 2,5 |
| **Total** | **60** | **1** | **60** | **χ² = 11,8** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 11,8; ν = clases efectivas - 1 - p = 6 - 1 - 0 = 5; χ²(1-α; ν) = 11,0705.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **4 · Condición de rechazo (CR)**: si χ² > 11,0705 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² con las frecuencias observadas y las esperadas del modelo. Si χ² > 11,0705, se rechaza H0 → se puede asegurar que la variable no sigue el modelo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la variable no sigue el modelo.
- **6 · Cálculos y decisión**: χ² = 11,8 > 11,0705 ⇒ se rechaza H0: la variable NO sigue el modelo Uniforme discreto.

**Conclusión:** Con α = 0,05 se rechaza H0: se puede asegurar que la variable no sigue el modelo Uniforme discreto.

**Respuesta de la guía:** Resp: Sí, se puede asegurar que el dado está cargado debido a que no cumple con el modelo uniforme (el cual es el modelo de comportamiento teórico de un dado equilibrado).

> 📝 *Notas de la transcripción:* Modelo uniforme discreto, parámetros dados (p = 1/6).

---

### VI-11 · Problema 11 (pág. 45)

**Enunciado.** Una persona denunció que en un casino privado había una ruleta adulterada. Su presunción estaría basada en el hecho de haber observado que el 0 se producía con una frecuencia excesiva y que los colores colorado y negro no se presentaban por igual. El juez solicitó entonces la asesoría de un consultor estadístico para que elevara el informe correspondiente. El consultor registró los datos de 1.000 bolas, con los siguientes resultados: Tabla: Resultado obtenido | Cantidad de ocurrencias; 0 (cero) | 42; Negro | 520; Colorado | 438.

*Indique las conclusiones del consultor.*

| Resultado obtenido | Cantidad de ocurrencias |
|---|---|
| 0 (cero) | 42 |
| Negro | 520 |
| Colorado | 438 |

*Tema detectado por la app: Chi² — bondad de ajuste.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Bondad de ajuste χ² al modelo Uniforme discreto: se compara χ² calculado contra el crítico.

- **— Modelo Uniforme discreto —**
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Uniforme discreto  vs  H1: no lo sigue.  α = 0,05.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| 0 (cero) | 42 | 0,25 | 250 | 173,056 |
| Negro | 520 | 0,25 | 250 | 291,6 |
| Colorado | 438 | 0,25 | 250 | 141,376 |
| **Total** | **1.000** | **0,75** | **750** | **χ² = 606,032** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 606,032; ν = clases efectivas - 1 - p = 3 - 1 - 0 = 2; χ²(1-α; ν) = 5,9915.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **4 · Condición de rechazo (CR)**: si χ² > 5,9915 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² con las frecuencias observadas y las esperadas del modelo. Si χ² > 5,9915, se rechaza H0 → se puede asegurar que la variable no sigue el modelo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la variable no sigue el modelo.
- **6 · Cálculos y decisión**: χ² = 606,032 > 5,9915 ⇒ se rechaza H0: la variable NO sigue el modelo Uniforme discreto.

**Conclusión:** Con α = 0,05 se rechaza H0: se puede asegurar que la variable no sigue el modelo Uniforme discreto.

**Respuesta de la guía:** Resp: Se puede asegurar que la ruleta está adulterada porque no se ajusta al modelo uniforme (el cual es el modelo de comportamiento teórico de una ruleta equilibrada).

> 📝 *Notas de la transcripción:* La consigna no indica riesgo. Modelo "uniforme" sobre los 37 números de la ruleta (p(0) = 1/37, p(negro) = p(colorado) = 18/37), parámetros dados; la guía no lo explicita.

---

### VI-12 · Problema 12 (pág. 45)

**Enunciado.** Un distribuidor de acondicionadores de aire tiene dividida su región en 4 localidades. El mismo afirma que las instalaciones del equipo están igualmente distribuidas entre las 4 localidades. Un posible representante ensaya una muestra de 80 instalaciones realizadas el año anterior, y comprueba lo siguiente: Tabla: Zonas | Cantidad de instalaciones; A | 16; B | 22; C | 24; D | 18.

*¿Se rechaza la afirmación del distribuidor?*

| Zonas | Cantidad de instalaciones |
|---|---|
| A | 16 |
| B | 22 |
| C | 24 |
| D | 18 |

*Tema detectado por la app: Chi² — bondad de ajuste.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Bondad de ajuste χ² al modelo Uniforme discreto: se compara χ² calculado contra el crítico.

- **— Modelo Uniforme discreto —**
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Uniforme discreto  vs  H1: no lo sigue.  α = 0,05.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| A | 16 | 0,25 | 20 | 0,8 |
| B | 22 | 0,25 | 20 | 0,2 |
| C | 24 | 0,25 | 20 | 0,8 |
| D | 18 | 0,25 | 20 | 0,2 |
| **Total** | **80** | **1** | **80** | **χ² = 2** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 2; ν = clases efectivas - 1 - p = 4 - 1 - 0 = 3; χ²(1-α; ν) = 7,8147.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **4 · Condición de rechazo (CR)**: si χ² > 7,8147 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² con las frecuencias observadas y las esperadas del modelo. Si χ² > 7,8147, se rechaza H0 → se puede asegurar que la variable no sigue el modelo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la variable no sigue el modelo.
- **6 · Cálculos y decisión**: χ² = 2 ≤ 7,8147 ⇒ no se rechaza H0: el modelo Uniforme discreto es un buen candidato.

**Conclusión:** Con α = 0,05 no se rechaza H0: no hay evidencia suficiente para asegurar que la variable no siga el modelo Uniforme discreto; el modelo Uniforme discreto es un buen candidato.

**Respuesta de la guía:** Resp: No hay motivo para rechazar la afirmación del distribuidor, se puede considerar que las instalaciones están igualmente distribuidas entre las cuatro localidades.

> 📝 *Notas de la transcripción:* La consigna no indica riesgo. Modelo uniforme, parámetros dados.

---

### VI-13 · Problema 13 (pág. 45)

**Enunciado.** Históricamente, un fabricante de televisores ha vendido sus productos en la siguiente forma: el 40% de 24", el 40% de 36" y el 20% de 40". Con el objeto de programar su producción para los próximos períodos, toma una muestra de 200 ventas recientes y encuentra los siguientes resultados: 85 TV de 24", 65 TV de 36" y 50 TV de 40". Verificar si realmente hubo cambios respecto del patrón histórico de ventas, asumiendo un riesgo del 5%. Tabla: Tamaño | Proporción histórica (%) | Ventas observadas; 24" | 40 | 85; 36" | 40 | 65; 40" | 20 | 50.

| Tamaño | Proporción histórica (%) | Ventas observadas |
|---|---|---|
| 24" | 40 | 85 |
| 36" | 40 | 65 |
| 40" | 20 | 50 |

*Tema detectado por la app: Chi² — bondad de ajuste.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Bondad de ajuste χ² al modelo propuesto: se compara χ² calculado contra el crítico.

- **1 · Planteo de hipótesis**: H0: las proporciones de cada categoría son las del modelo propuesto (24": 0,4; 36": 0,4; 40": 0,2)  vs  H1: al menos una difiere.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas**: bajo H0, Feᵢ = N·pᵢ con N = 200.
- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ, con ν = k - 1 - p = 3 - 1 - 0 = 2 grados de libertad; χ²crítico = 5,9915.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **4 · Condición de rechazo (CR)**: si χ² > 5,9915 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² = Σ(Foᵢ - Feᵢ)²/Feᵢ con las frecuencias observadas. Si χ² > 5,9915, se rechaza H0 → se puede asegurar que las proporciones no son las del modelo propuesto. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que las proporciones no son las del modelo propuesto.
- **6 · Cálculos y decisión**: frecuencias observadas, esperadas y aporte de cada categoría al χ².

| Categoría | Foᵢ | pᵢ | Feᵢ | (Foᵢ - Feᵢ)²/Feᵢ |
|---|---|---|---|---|
| 24" | 85 | 0,4 | 80 | 0,3125 |
| 36" | 65 | 0,4 | 80 | 2,8125 |
| 40" | 50 | 0,2 | 40 | 2,5 |
| **Total** | **200** | **1** | **200** | **χ² = 5,625** |

χ² = 5,625 ≤ χ²c = 5,9915 ⇒ no se rechaza H0.


**Conclusión:** Con α = 0,05, χ² = 5,625 [χ²c = 5,9915; ν = 2] no cae en la zona de rechazo ⇒ no se rechaza la hipótesis nula de que las proporciones son las del modelo propuesto. No hay evidencia suficiente para asegurar que las proporciones no son las del modelo propuesto (no rechazar H0 no la prueba).

**Respuesta de la guía:** Resp: No se puede asegurar que el patrón histórico de ventas haya cambiado.

> 📝 *Notas de la transcripción:* Tabla armada a partir del texto. La Resp está en la p. 46. Modelo multinomial con proporciones dadas (40%, 40%, 20%).

---

### VI-14 · Problema 14 (pág. 46)

**Enunciado.** Los datos de la tabla siguiente son consumos diarios de agua en una curtiembre: Tabla: Consumo diario (en miles de litros) | Cantidad de días observados; 20-30 | 6; 30-40 | 90; 40-50 | 232; 50-60 | 192; 60-70 | 66; 70-80 | 12; 80-90 | 2. n = 600 días.

*Se desea ensayar la hipótesis de que los consumos diarios de agua en una curtiembre se comportan de acuerdo a un modelo normal.*

| Consumo diario (en miles de litros) | Cantidad de días observados |
|---|---|
| 20-30 | 6 |
| 30-40 | 90 |
| 40-50 | 232 |
| 50-60 | 192 |
| 60-70 | 66 |
| 70-80 | 12 |
| 80-90 | 2 |

*Tema detectado por la app: Chi² — bondad de ajuste.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Bondad de ajuste χ² al modelo Normal: se compara χ² calculado contra el crítico.

> ⚠️ Se amalgamaron clases con Fe < 5: de 7 a 6 clases efectivas.

- **— Modelo Normal —**
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Normal  vs  H1: no lo sigue.  α = 0,05.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe |
|---|---|---|---|
| 20 a 30 | 6 | 0,0253 | 15,187 |
| 30 a 40 | 90 | 0,146 | 87,625 |
| 40 a 50 | 232 | 0,3514 | 210,824 |
| 50 a 60 | 192 | 0,3333 | 200,006 |
| 60 a 70 | 66 | 0,1246 | 74,784 |
| 70 a 80 | 12 | 0,0182 | 10,941 |
| 80 a 90 | 2 | 0,0011 | 0,633 |

- **Amalgamado** (Fe < 5 se une con la clase vecina):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| 20 a 30 | 6 | 0,0253 | 15,187 | 5,5572 |
| 30 a 40 | 90 | 0,146 | 87,625 | 0,0644 |
| 40 a 50 | 232 | 0,3514 | 210,824 | 2,1269 |
| 50 a 60 | 192 | 0,3333 | 200,006 | 0,3205 |
| 60 a 70 | 66 | 0,1246 | 74,784 | 1,0318 |
| 70 a 90 | 14 | 0,0193 | 11,573 | 0,5088 |
| **Total** | **600** | **1** | **600** | **χ² = 9,6097** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 9,6097; ν = clases efectivas - 1 - p = 6 - 1 - 2 = 3; χ²(1-α; ν) = 7,8147.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **Estimación** (marcas de clase): x̄ = 49,4333, S = 9,942.
- **Parámetros del modelo**: μ = 49,4333 (estimado), σ = 9,942 (estimado).
- **4 · Condición de rechazo (CR)**: si χ² > 7,8147 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² con las frecuencias observadas y las esperadas del modelo. Si χ² > 7,8147, se rechaza H0 → se puede asegurar que la variable no sigue el modelo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la variable no sigue el modelo.
- **6 · Cálculos y decisión**: χ² = 9,6097 > 7,8147 ⇒ se rechaza H0: la variable NO sigue el modelo Normal.

**Conclusión:** Con α = 0,05 se rechaza H0: se puede asegurar que la variable no sigue el modelo Normal.

**Respuesta de la guía:** Resp: Se puede asegurar, que los consumos diarios de agua en la curtiembre, no se comportan normalmente. Ver la resolución del problema en el apunte teórico (capítulo de Contrastes Chi – Cuadrado).

> 📝 *Notas de la transcripción:* La consigna no indica riesgo. Modelo normal sin parámetros dados (hay que estimar μ y σ). La resolución remite al apunte teórico.

---

### VI-15 · Problema 15 (pág. 46)

**Enunciado.** Se cree que la variable aleatoria “duración de herramientas de corte” tiene distribución Gumbel del mínimo con aplicaciones en la Teoría de Confiabilidad. Los parámetros de esta distribución son: “θ” que es el modo de la variable y “β” que es un parámetro de escala. Para verificar este supuesto, se registraron las duraciones de herramientas de corte provenientes de un torno automático y se obtuvieron los siguientes resultados, agrupados en una tabla de frecuencias: Tabla: Duración (en horas) | Observaciones; 0-15 | 8; 15-30 | 40; 30-45 | 30; 45-60 | 25; 60-75 | 18; 75-90 | 15; 90-105 | 7.

- **a)** ¿Para un riesgo del 1%, se puede rechazar la afirmación de que esta variable tiene un comportamiento según el modelo Gumbel del mínimo?
- **b)** Si se rechaza el comportamiento Gumbel del mínimo, verificar el ajuste a un comportamiento Gumbel del Máximo y de Weibull; ¿cuál es el mejor de los ajustes?

| Duración (en horas) | Observaciones |
|---|---|
| 0-15 | 8 |
| 15-30 | 40 |
| 30-45 | 30 |
| 45-60 | 25 |
| 60-75 | 18 |
| 75-90 | 15 |
| 90-105 | 7 |

*Tema detectado por la app: Chi² — bondad de ajuste.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Bondad de ajuste χ² al modelo Gumbel del mínimo: se compara χ² calculado contra el crítico.

> ⚠️ Se amalgamaron clases con Fe < 5: de 7 a 6 clases efectivas.

- **— Modelo Gumbel del mínimo —**
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Gumbel del mínimo  vs  H1: no lo sigue.  α = 0,01.
- **2 · Nivel de significación**: α = 0,01 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe |
|---|---|---|---|
| 0 a 15 | 8 | 0,1054 | 15,071 |
| 15 a 30 | 40 | 0,1124 | 16,07 |
| 30 a 45 | 30 | 0,2004 | 28,662 |
| 45 a 60 | 25 | 0,2789 | 39,887 |
| 60 a 75 | 18 | 0,2311 | 33,045 |
| 75 a 90 | 15 | 0,0688 | 9,836 |
| 90 a 105 | 7 | 0,003 | 0,429 |

- **Amalgamado** (Fe < 5 se une con la clase vecina):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| 0 a 15 | 8 | 0,1054 | 15,071 | 3,3178 |
| 15 a 30 | 40 | 0,1124 | 16,07 | 35,6352 |
| 30 a 45 | 30 | 0,2004 | 28,662 | 0,0625 |
| 45 a 60 | 25 | 0,2789 | 39,887 | 5,5562 |
| 60 a 75 | 18 | 0,2311 | 33,045 | 6,85 |
| 75 a 105 | 22 | 0,0718 | 10,265 | 13,4167 |
| **Total** | **143** | **1** | **143** | **χ² = 64,8385** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 64,8385; ν = clases efectivas - 1 - p = 6 - 1 - 2 = 3; χ²(1-α; ν) = 11,3449.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **Estimación** (marcas de clase): x̄ = 45,6818, S = 24,3257.
- **Parámetros del modelo**: β = 18,9667 (estimado), θ (modo) = 56,6297 (estimado).
- **4 · Condición de rechazo (CR)**: si χ² > 11,3449 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² con las frecuencias observadas y las esperadas del modelo. Si χ² > 11,3449, se rechaza H0 → se puede asegurar que la variable no sigue el modelo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la variable no sigue el modelo.
- **6 · Cálculos y decisión**: χ² = 64,8385 > 11,3449 ⇒ se rechaza H0: la variable NO sigue el modelo Gumbel del mínimo.

**Conclusión:** Con α = 0,01 se rechaza H0: se puede asegurar que la variable no sigue el modelo Gumbel del mínimo.

**Respuesta de la guía:** a) Sí, esta variable no se comporta según el modelo Gumbel del mínimo.

#### b) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Bondad de ajuste χ² al modelo Gumbel del máximo, Weibull: se compara χ² calculado contra el crítico.

- **— Modelo Gumbel del máximo —**
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Gumbel del máximo  vs  H1: no lo sigue.  α = 0,01.
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Weibull  vs  H1: no lo sigue.  α = 0,01.
- **Estimación** (marcas de clase): x̄ = 45,6818, S = 24,3257.
- **Parámetros del modelo**: w (forma) = 1,9592 (estimado), β = 51,5243 (estimado).
- **2 · Nivel de significación**: α = 0,01 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| 0 a 15 | 8 | 0,059 | 8,435 | 0,0224 |
| 15 a 30 | 40 | 0,2181 | 31,186 | 2,4913 |
| 30 a 45 | 30 | 0,2817 | 40,284 | 2,6255 |
| 45 a 60 | 25 | 0,2093 | 29,925 | 0,8105 |
| 60 a 75 | 18 | 0,1192 | 17,041 | 0,0539 |
| 75 a 90 | 15 | 0,06 | 8,576 | 4,8127 |
| 90 a 105 | 7 | 0,0528 | 7,553 | 0,0405 |
| **Total** | **143** | **1** | **143** | **χ² = 10,8569** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 10,8569; ν = clases efectivas - 1 - p = 7 - 1 - 2 = 4; χ²(1-α; ν) = 13,2767.
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| 0 a 15 | 8 | 0,0853 | 12,193 | 1,4422 |
| 15 a 30 | 40 | 0,2076 | 29,69 | 3,5802 |
| 30 a 45 | 30 | 0,2427 | 34,707 | 0,6384 |
| 45 a 60 | 25 | 0,2046 | 29,252 | 0,618 |
| 60 a 75 | 18 | 0,1357 | 19,412 | 0,1027 |
| 75 a 90 | 15 | 0,0734 | 10,501 | 1,9271 |
| 90 a 105 | 7 | 0,0507 | 7,245 | 0,0083 |
| **Total** | **143** | **1** | **143** | **χ² = 8,3167** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 8,3167; ν = clases efectivas - 1 - p = 7 - 1 - 2 = 4; χ²(1-α; ν) = 13,2767.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **Estimación** (marcas de clase): x̄ = 45,6818, S = 24,3257.
- **Parámetros del modelo**: β = 18,9667 (estimado), θ (modo) = 34,7339 (estimado).
- **4 · Condición de rechazo (CR)**: si χ² > 13,2767 ⇒ se rechaza H0.
- **4 · Condición de rechazo (CR)**: si χ² > 13,2767 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² con las frecuencias observadas y las esperadas del modelo. Si χ² > 13,2767, se rechaza H0 → se puede asegurar que la variable no sigue el modelo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la variable no sigue el modelo.
- **6 · Cálculos y decisión**: χ² = 10,8569 ≤ 13,2767 ⇒ no se rechaza H0: el modelo Gumbel del máximo es un buen candidato.
- **— Modelo Weibull —**
- **6 · Cálculos y decisión**: χ² = 8,3167 ≤ 13,2767 ⇒ no se rechaza H0: el modelo Weibull es un buen candidato.

**Conclusión:** Con α = 0,01 no se rechaza H0: no hay evidencia suficiente para asegurar que la variable no siga el modelo Gumbel del máximo; el modelo Gumbel del máximo es un buen candidato. Con α = 0,01 no se rechaza H0: no hay evidencia suficiente para asegurar que la variable no siga el modelo Weibull; el modelo Weibull es un buen candidato. El que mejor ajusta es el modelo Weibull (menor χ² relativo al crítico: 0,626).

**Respuesta de la guía:** b) El Modelo Gumbel del Máximo es un buen candidato, se puede suponer que sigue este comportamiento. El Modelo de Weibull es un buen candidato, se puede suponer que sigue este comportamiento. El Modelo que mejor se ajusta de los 2 candidatos es el de Weibull.

> 📝 *Notas de la transcripción:* Modelos Gumbel del mínimo, Gumbel del máximo y Weibull, sin parámetros dados (hay que estimarlos). n = 143. En b) no se rechaza ninguno de los dos candidatos; el mejor ajuste es Weibull.

---

### VI-16 · Problema 16 (pág. 46)

**Enunciado.** La siguiente tabla muestra la cantidad de reclamos por día de un determinado modelo de levanta cristales. Por estudios anteriores, se supone que la cantidad diaria de levanta cristales de un modelo de automóvil que llegan reclamados a fábrica por defectos responde a un proceso de Poisson, o sea que la cantidad de reclamos que llegan en un día a la fábrica se modelan según una distribución Poissoniana. Se tienen los registros correspondientes a una muestra de un total de 684 días observados con los siguientes datos de reclamos: Tabla: Cantidad de reclamos (r) | Ocurrencias (cantidad de días observados); 0 | 26; 1 | 62; 2 | 120; 3 | 145; 4 | 131; 5 | 101; 6 | 61; 7 | 27; 8 | 9; 9 | 1; 10 | 1.

*¿Se puede asegurar las premisas estipuladas?*

| Cantidad de reclamos (r) | Ocurrencias (cantidad de días observados) |
|---|---|
| 0 | 26 |
| 1 | 62 |
| 2 | 120 |
| 3 | 145 |
| 4 | 131 |
| 5 | 101 |
| 6 | 61 |
| 7 | 27 |
| 8 | 9 |
| 9 | 1 |
| 10 | 1 |

*Tema detectado por la app: Chi² — bondad de ajuste.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Bondad de ajuste χ² al modelo Poisson: se compara χ² calculado contra el crítico.

> ⚠️ Se completó el dominio al final con la clase «≥ 11» (O = 0, probabilidad acumulada G(11) = 0.0011), no la puntual.
> ⚠️ Se amalgamaron clases con Fe < 5: de 12 a 10 clases efectivas.

- **— Modelo Poisson —**
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Poisson  vs  H1: no lo sigue.  α = 0,05.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe |
|---|---|---|---|
| 0 | 26 | 0,0294 | 20,119 |
| 1 | 62 | 0,1037 | 70,944 |
| 2 | 120 | 0,1829 | 125,086 |
| 3 | 145 | 0,215 | 147,031 |
| 4 | 131 | 0,1895 | 129,619 |
| 5 | 101 | 0,1336 | 91,416 |
| 6 | 61 | 0,0785 | 53,727 |
| 7 | 27 | 0,0396 | 27,065 |
| 8 | 9 | 0,0174 | 11,93 |
| 9 | 1 | 0,0068 | 4,674 |
| 10 | 1 | 0,0024 | 1,648 |
| ≥ 11 | 0 | 0,0011 | 0,74 |

- **Amalgamado** (Fe < 5 se une con la clase vecina):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| 0 | 26 | 0,0294 | 20,119 | 1,7194 |
| 1 | 62 | 0,1037 | 70,944 | 1,1277 |
| 2 | 120 | 0,1829 | 125,086 | 0,2068 |
| 3 | 145 | 0,215 | 147,031 | 0,0281 |
| 4 | 131 | 0,1895 | 129,619 | 0,0147 |
| 5 | 101 | 0,1336 | 91,416 | 1,0048 |
| 6 | 61 | 0,0785 | 53,727 | 0,9846 |
| 7 | 27 | 0,0396 | 27,065 | 0,0002 |
| 8 | 9 | 0,0174 | 11,93 | 0,7197 |
| 9 a ≥ 11 | 2 | 0,0103 | 7,062 | 3,6287 |
| **Total** | **684** | **1** | **684** | **χ² = 9,4346** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 9,4346; ν = clases efectivas - 1 - p = 10 - 1 - 1 = 8; χ²(1-α; ν) = 15,5073.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **Estimación** (marcas de clase): x̄ = 3,5263.
- **Parámetros del modelo**: m = 3,5263 (estimado).
- **4 · Condición de rechazo (CR)**: si χ² > 15,5073 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² con las frecuencias observadas y las esperadas del modelo. Si χ² > 15,5073, se rechaza H0 → se puede asegurar que la variable no sigue el modelo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la variable no sigue el modelo.
- **6 · Cálculos y decisión**: χ² = 9,4346 ≤ 15,5073 ⇒ no se rechaza H0: el modelo Poisson es un buen candidato.

**Conclusión:** Con α = 0,05 no se rechaza H0. Si además se cumple el proceso físico del modelo Poisson (p. ej. Poisson: sucesos puntuales e independientes en un medio continuo), se puede afirmar que la variable sigue el modelo Poisson; si no se cumple, el modelo Poisson es un buen candidato.

**Respuesta de la guía:** Resp: No se puede decir que no sigue el modelo de Poisson, por lo tanto, se considera que el modelo de Poisson se ajusta adecuadamente a la variable “cantidad de reclamos por día”.

> 📝 *Notas de la transcripción:* La consigna no indica riesgo. Modelo Poisson sin parámetro dado (estimar λ con la media). Las ocurrencias suman 684, coincide con el enunciado.

---

### VI-17 · Problema 17 (pág. 47)

**Enunciado.** Los siguientes datos son consumos de electricidad (medidos en Kwh) de 100 usuarios de Buenos Aires y Gran Buenos Aires. Tabla: Consumos (en Kwh) | Cantidad de usuarios; 0-100 | 18; 100-200 | 34; 200-300 | 28; 300-400 | 12; 400-500 | 4; 500-600 | 2; 600-1400 | 2.

*Verificar si los datos permiten afirmar que los consumos de electricidad es una variable que se ajusta a un modelo Log-Normal.*

| Consumos (en Kwh) | Cantidad de usuarios |
|---|---|
| 0-100 | 18 |
| 100-200 | 34 |
| 200-300 | 28 |
| 300-400 | 12 |
| 400-500 | 4 |
| 500-600 | 2 |
| 600-1400 | 2 |

*Tema detectado por la app: Chi² — bondad de ajuste.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Bondad de ajuste χ² al modelo Log-Normal: se compara χ² calculado contra el crítico.

> ⚠️ Se amalgamaron clases con Fe < 5: de 7 a 6 clases efectivas.

- **— Modelo Log-Normal —**
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Log-Normal  vs  H1: no lo sigue.  α = 0,05.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe |
|---|---|---|---|
| 0 a 100 | 18 | 0,1866 | 18,663 |
| 100 a 200 | 34 | 0,382 | 38,197 |
| 200 a 300 | 28 | 0,218 | 21,802 |
| 300 a 400 | 12 | 0,1052 | 10,515 |
| 400 a 500 | 4 | 0,051 | 5,098 |
| 500 a 600 | 2 | 0,0257 | 2,566 |
| 600 a 1400 | 2 | 0,0316 | 3,159 |

- **Amalgamado** (Fe < 5 se une con la clase vecina):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| 0 a 100 | 18 | 0,1866 | 18,663 | 0,0235 |
| 100 a 200 | 34 | 0,382 | 38,197 | 0,4612 |
| 200 a 300 | 28 | 0,218 | 21,802 | 1,7621 |
| 300 a 400 | 12 | 0,1052 | 10,515 | 0,2096 |
| 400 a 500 | 4 | 0,051 | 5,098 | 0,2363 |
| 500 a 1400 | 4 | 0,0572 | 5,725 | 0,5197 |
| **Total** | **100** | **1** | **100** | **χ² = 3,2125** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 3,2125; ν = clases efectivas - 1 - p = 6 - 1 - 2 = 3; χ²(1-α; ν) = 7,8147.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **Estimación** (marcas de clase): x̄ = 221, S = 160,8343.
- **Parámetros del modelo**: m = 5,1856 (estimado), D = 0,6519 (estimado).
- **4 · Condición de rechazo (CR)**: si χ² > 7,8147 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² con las frecuencias observadas y las esperadas del modelo. Si χ² > 7,8147, se rechaza H0 → se puede asegurar que la variable no sigue el modelo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la variable no sigue el modelo.
- **6 · Cálculos y decisión**: χ² = 3,2125 ≤ 7,8147 ⇒ no se rechaza H0: el modelo Log-Normal es un buen candidato.

**Conclusión:** Con α = 0,05 no se rechaza H0: no hay evidencia suficiente para asegurar que la variable no siga el modelo Log-Normal; el modelo Log-Normal es un buen candidato.

**Respuesta de la guía:** Resp: No se puede asegurar que los consumos de electricidad, no se ajusten al modelo Log-Normal, por lo tanto, se considera que el modelo Log-Normal es un buen candidato para esta variable. Ver la resolución del problema en el apunte teórico (capítulo de Contrastes Chi – Cuadrado).

> 📝 *Notas de la transcripción:* La consigna no indica riesgo. Modelo log-normal sin parámetros dados (estimar). Último intervalo 600 – 1.400 (más ancho que los demás). La resolución remite al apunte teórico.

---

### VI-18 · Problema 18 (pág. 47)

**Enunciado.** El modelo de Vilfredo Pareto suele utilizarse para representar salarios de una empresa y también ofertas de licitaciones. Siendo “θ” el modo y el valor mínimo de la variable (salario mínimo), que generalmente se conoce, y “b” un parámetro de forma que puede calcularse en función de la media. Considere los siguientes datos de salarios de una empresa, en la cual el salario mínimo es de 400 U$s: Tabla: Salario (en U$s) | Cantidad de empleados; 400-500 | 59; 500-600 | 34; 600-700 | 26; 700-800 | 20; 800-1000 | 21; 1000-1200 | 15; 1200-1500 | 11; 1500-2000 | 10; 2000-3000 | 12; 3000-5000 | 6.

*Ensayar la hipótesis de que los salarios de esta empresa tienen un comportamiento según el modelo de Pareto.*

| Salario (en U$s) | Cantidad de empleados |
|---|---|
| 400-500 | 59 |
| 500-600 | 34 |
| 600-700 | 26 |
| 700-800 | 20 |
| 800-1000 | 21 |
| 1000-1200 | 15 |
| 1200-1500 | 11 |
| 1500-2000 | 10 |
| 2000-3000 | 12 |
| 3000-5000 | 6 |

*Tema detectado por la app: Chi² — bondad de ajuste.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Bondad de ajuste χ² al modelo Pareto: se compara χ² calculado contra el crítico.

- **— Modelo Pareto —**
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Pareto  vs  H1: no lo sigue.  α = 0,05.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| 400 a 500 | 59 | 0,3241 | 69,361 | 1,5476 |
| 500 a 600 | 34 | 0,1851 | 39,617 | 0,7963 |
| 600 a 700 | 26 | 0,1164 | 24,9 | 0,0486 |
| 700 a 800 | 20 | 0,0782 | 16,743 | 0,6335 |
| 800 a 1000 | 21 | 0,096 | 20,542 | 0,0102 |
| 1000 a 1200 | 15 | 0,0548 | 11,733 | 0,9096 |
| 1200 a 1500 | 11 | 0,0471 | 10,081 | 0,0837 |
| 1500 a 2000 | 10 | 0,039 | 8,336 | 0,3322 |
| 2000 a 3000 | 12 | 0,0302 | 6,461 | 4,7492 |
| 3000 a 5000 | 6 | 0,0291 | 6,226 | 0,0082 |
| **Total** | **214** | **1** | **214** | **χ² = 9,1192** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 9,1192; ν = clases efectivas - 1 - p = 10 - 1 - 2 = 7; χ²(1-α; ν) = 14,0671.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **Estimación** (marcas de clase): x̄ = 929,4393, S = 739,3517.
- **Parámetros del modelo**: θ (mínimo) = 400 (estimado), b = 1,7555 (estimado).
- **4 · Condición de rechazo (CR)**: si χ² > 14,0671 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² con las frecuencias observadas y las esperadas del modelo. Si χ² > 14,0671, se rechaza H0 → se puede asegurar que la variable no sigue el modelo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la variable no sigue el modelo.
- **6 · Cálculos y decisión**: χ² = 9,1192 ≤ 14,0671 ⇒ no se rechaza H0: el modelo Pareto es un buen candidato.

**Conclusión:** Con α = 0,05 no se rechaza H0: no hay evidencia suficiente para asegurar que la variable no siga el modelo Pareto; el modelo Pareto es un buen candidato.

**Respuesta de la guía:** Resp: No se puede afirmar que los salarios de esta empresa, no se comporten según el modelo de Pareto, por lo tanto, se considera que el modelo de Pareto es un buen candidato para esta variable.

> 📝 *Notas de la transcripción:* La consigna no indica riesgo. Modelo Pareto: θ = 400 U$s dado; b se estima en función de la media. n = 214.

---

### VI-19 · Problema 19 (pág. 47)

**Enunciado.** En una fábrica de baterías para uso industrial, para un determinado tipo se obtuvieron los siguientes datos de duración en días de uso continuo: Tabla: Duración (en días) | Cantidad de baterías; 0-40 | 38; 40-80 | 105; 80-120 | 120; 120-160 | 96; 160-200 | 80; 200-240 | 43; 240-280 | 15; 280-320 | 3.

*¿Se puede considerar que la duración se ajusta a un Modelo de Weibull?*

| Duración (en días) | Cantidad de baterías |
|---|---|
| 0-40 | 38 |
| 40-80 | 105 |
| 80-120 | 120 |
| 120-160 | 96 |
| 160-200 | 80 |
| 200-240 | 43 |
| 240-280 | 15 |
| 280-320 | 3 |

*Tema detectado por la app: Chi² — bondad de ajuste.*

#### Resolución (Ensayo de hipótesis (decidir)) ✅

*Qué pide:* Bondad de ajuste χ² al modelo Weibull: se compara χ² calculado contra el crítico.

- **— Modelo Weibull —**
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Weibull  vs  H1: no lo sigue.  α = 0,05.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| 0 a 40 | 38 | 0,0758 | 37,913 | 0,0002 |
| 40 a 80 | 105 | 0,2028 | 101,404 | 0,1275 |
| 80 a 120 | 120 | 0,249 | 124,501 | 0,1628 |
| 120 a 160 | 96 | 0,2138 | 106,921 | 1,1154 |
| 160 a 200 | 80 | 0,1406 | 70,29 | 1,3414 |
| 200 a 240 | 43 | 0,0732 | 36,591 | 1,1226 |
| 240 a 280 | 15 | 0,0307 | 15,327 | 0,007 |
| 280 a 320 | 3 | 0,0141 | 7,053 | 2,3293 |
| **Total** | **500** | **1** | **500** | **χ² = 6,2061** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 6,2061; ν = clases efectivas - 1 - p = 8 - 1 - 2 = 5; χ²(1-α; ν) = 11,0705.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **Estimación** (marcas de clase): x̄ = 122,32, S = 62,5271.
- **Parámetros del modelo**: w (forma) = 2,0503 (estimado), β = 138,0754 (estimado).
- **4 · Condición de rechazo (CR)**: si χ² > 11,0705 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² con las frecuencias observadas y las esperadas del modelo. Si χ² > 11,0705, se rechaza H0 → se puede asegurar que la variable no sigue el modelo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la variable no sigue el modelo.
- **6 · Cálculos y decisión**: χ² = 6,2061 ≤ 11,0705 ⇒ no se rechaza H0: el modelo Weibull es un buen candidato.

**Conclusión:** Con α = 0,05 no se rechaza H0: no hay evidencia suficiente para asegurar que la variable no siga el modelo Weibull; el modelo Weibull es un buen candidato.

**Respuesta de la guía:** Resp: No se puede afirmar que la duración de las baterías, no se comporta según el modelo de Weibull, por lo tanto, se considera que el modelo de Weibull es un buen candidato para esta variable.

> 📝 *Notas de la transcripción:* Tabla en p. 47; pregunta y Resp en p. 48. La consigna no indica riesgo. Modelo Weibull sin parámetros dados (estimar). n = 500.

---

### VI-20 · Problema 20 (pág. 48)

**Enunciado.** En ensayos de vida realizados sobre dos equipos similares de distintas marcas se obtienen los siguientes resultados: Tabla: Cantidad de conjuntos observados: Duración (en miles de horas) | Marca A | Marca B; 10-12 | 2 | None; 12-14 | 6 | 8; 14-16 | 13 | 18; 16-18 | 18 | 32; 18-20 | 30 | 57; 20-22 | 22 | 39; 22-24 | 16 | 26; 24-26 | 5 | 13; 26-28 | 1 | 10.

- **a)** ¿Qué marca se elegiría si no hay notoria diferencia de precios?
- **b)** Según especificación del fabricante la duración de los conjuntos de la marca "A" tienen distribución normal con un valor medio de 20.000 horas y un desvío estándar de 2.500 horas; verificar si cumple con la especificación del fabricante.
- **c)** Caso contrario verificar si sigue una distribución normal.
- **d)** Si por especificación se estipula una duración mínima de 14.000 hs, estimar para la marca “B” (con 5% de riesgo) el porcentaje de equipos que no cumplen con la especificación.

*Cantidad de conjuntos observados*

| Duración (en miles de horas) | Marca A | Marca B |
|---|---|---|
| 10-12 | 2 | — |
| 12-14 | 6 | 8 |
| 14-16 | 13 | 18 |
| 16-18 | 18 | 32 |
| 18-20 | 30 | 57 |
| 20-22 | 22 | 39 |
| 22-24 | 16 | 26 |
| 24-26 | 5 | 13 |
| 26-28 | 1 | 10 |

*Tema detectado por la app: Chi² — bondad de ajuste.*

#### a) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Comparación de dos medias con datos agrupados (test F previo y t).

> ⚠️ El enunciado no fija el riesgo α: se eligió α = 0,05. En el examen hay que elegirlo y JUSTIFICARLO antes de ver la muestra (p. ej. «0,05, no porque sea estándar, sino porque el perito tiene que ser imparcial»); una vez fijado, α no se toca. El valor a posteriori α* se muestra solo como dato: no se decide con él.

- **1 · Planteo de hipótesis**: H0: δ = μ(Marca B) - μ(Marca A) ≤ 0  vs  H1: δ = μ(Marca B) - μ(Marca A) > 0.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **3 · Estadístico de prueba**: **ensayo auxiliar** de desvíos (test F previo; no es parte del problema): como S(Marca B) > S(Marca A), lo único que se puede sospechar es σ(Marca B) > σ(Marca A) → unilateral, H0: φ = σ(Marca B)/σ(Marca A) ≤ 1, con un α propio y grande α = 0,1 (no el del problema: si no se rechaza se quiere poder suponerlos iguales). Jc = √F(0,9; ν₁ = 202; ν₂ = 112) = √1,2448 = 1,1157; J = S(Marca B)/S(Marca A) = 1,0179 → J ≤ Jc: no se rechaza H0 → no hay evidencia de que los desvíos difieran: se suponen IGUALES y se amalgaman (Sa).
- Sa = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)] = 3,327075; ν = n₁ + n₂ - 2 = 314.
- Diferencia observada (t con Sa (desvíos iguales)): d = x̄(Marca B) - x̄(Marca A) = 0,7154; σ(d) = 0,390498, ν = 314.
- **Modelos y distribuciones empleados**:  
• Las poblaciones se suponen Normales. Son apareadas solo si se mide el mismo individuo o la misma unidad experimental (no porque los n sean iguales): se trabaja con las diferencias dᵢ (d̄, S_D, t con ν = n-1).  
• Si son independientes y los desvíos son desconocidos, primero un ensayo auxiliar F (unilateral, la varianza muestral mayor sospechada mayor, con α propio = 0,10): si no se rechaza, t con Sa amalgamado (ν = n₁ + n₂ - 2); si se rechaza, t de Welch (ν truncado).  
• En comparaciones no hay ensayos bilaterales, y con t no se calculan β ni n.
- **4 · Condición de rechazo (CR)**: d_c = δ₀ + t·σ(d) = 0,6442. Si d > 0,6442 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula la diferencia d entre las medias muestrales. Si d > 0,6442, se rechaza H0 → se puede asegurar que δ = μ(Marca B) - μ(Marca A) > 0. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que δ = μ(Marca B) - μ(Marca A) > 0.
- **6 · Cálculos y decisión**: d = 0,7154 → se rechaza H0.
- Dato informativo (no es criterio de decisión): valor a posteriori α* = 0,034. La decisión se toma comparando el estimador con el valor crítico.
- **Orientación**: el enunciado no da dirección («¿difieren?»), pero en comparaciones no existen ensayos bilaterales: la muestra orienta el ensayo y lo único que se puede intentar probar es que μ(Marca B), el de mayor media muestral, supera a μ(Marca A).

**Conclusión:** Con α = 0,05, d = 0,7154 cae en la zona de rechazo ⇒ se rechaza la hipótesis nula H0: δ = μ(Marca B) - μ(Marca A) ≤ 0. Se puede asegurar que δ = μ(Marca B) - μ(Marca A) > 0.

**Respuesta de la guía:** a) nA = 113; x̄A = 19,0531 miles de horas; SA = 3,2892; nB = 203; x̄B = 19,7685; SB = 3,3479. Comparación de desvíos (H0: σB ≤ σA, α = 10%): jc = 1,1157 (jc² = 1,2448); j = 1,0179 (j² = 1,036): no se rechaza, se suponen desvíos iguales. Sa = 3,3271 miles de horas; ν = 314. H0) μB ≤ μA, α = 5%: dc = 0,6442 miles de horas; d = 0,7154 miles de horas. Se rechaza: se puede asegurar que la marca “B” tiene una mayor duración que la marca “A”, entonces se elegiría la marca “B”.

#### b) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Bondad de ajuste χ² al modelo Normal: se compara χ² calculado contra el crítico.

> ⚠️ El enunciado no fija el riesgo α: se eligió α = 0,05. En el examen hay que elegirlo y JUSTIFICARLO antes de ver la muestra (p. ej. «0,05, no porque sea estándar, sino porque el perito tiene que ser imparcial»); una vez fijado, α no se toca. El valor a posteriori α* se muestra solo como dato: no se decide con él.
> ⚠️ los parámetros dados se dividieron por 1000 (la tabla está en otra escala)
> ⚠️ Se amalgamaron clases con Fe < 5: de 9 a 6 clases efectivas.

- **— Modelo Normal —**
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Normal con μ = 20 (dado), σ = 2,5 (dado)  vs  H1: no lo sigue.  α = 0,05.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe |
|---|---|---|---|
| 10 a 12 | 2 | 0,0007 | 0,078 |
| 12 a 14 | 6 | 0,0075 | 0,849 |
| 14 a 16 | 13 | 0,0466 | 5,266 |
| 16 a 18 | 18 | 0,1571 | 17,747 |
| 18 a 20 | 30 | 0,2881 | 32,56 |
| 20 a 22 | 22 | 0,2881 | 32,56 |
| 22 a 24 | 16 | 0,1571 | 17,747 |
| 24 a 26 | 5 | 0,0466 | 5,266 |
| 26 a 28 | 1 | 0,0082 | 0,926 |

- **Amalgamado** (Fe < 5 se une con la clase vecina):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| 10 a 16 | 21 | 0,0548 | 6,192 | 35,4096 |
| 16 a 18 | 18 | 0,1571 | 17,747 | 0,0036 |
| 18 a 20 | 30 | 0,2881 | 32,56 | 0,2013 |
| 20 a 22 | 22 | 0,2881 | 32,56 | 3,425 |
| 22 a 24 | 16 | 0,1571 | 17,747 | 0,172 |
| 24 a 28 | 6 | 0,0548 | 6,192 | 0,006 |
| **Total** | **113** | **1** | **113** | **χ² = 39,2176** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 39,2176; ν = clases efectivas - 1 - p = 6 - 1 - 0 = 5; χ²(1-α; ν) = 11,0705.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **Estimación** (marcas de clase): x̄ = 19,0531, S = 3,2892.
- **Parámetros del modelo**: μ = 20 (dado), σ = 2,5 (dado).
- **4 · Condición de rechazo (CR)**: si χ² > 11,0705 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² con las frecuencias observadas y las esperadas del modelo. Si χ² > 11,0705, se rechaza H0 → se puede asegurar que la variable no sigue el modelo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la variable no sigue el modelo.
- **6 · Cálculos y decisión**: χ² = 39,2176 > 11,0705 ⇒ se rechaza H0: la variable NO sigue el modelo Normal.

**Conclusión:** Con α = 0,05 se rechaza H0: se puede asegurar que la variable no sigue el modelo Normal.

**Respuesta de la guía:** b) H0) La duración de la marca “A” se comporta normalmente con μ = 20.000 hs y σ = 2.500 hs. Amalgamando quedan 6 clases (FO: 21, 18, 30, 22, 16, 6; FE: 6,20; 17,75; 32,55; 32,55; 17,75; 6,20), ningún parámetro estimado, ν = 5; χ²(0,95;5) = 11,0705; χ²calc = 39,1307. Se rechaza: la duración de la marca “A” no sigue el modelo normal con los parámetros especificados por el fabricante.

> ≈ Coincide solo aproximadamente (39,1307): La cátedra usa probabilidades de la tabla normal (z con 2 decimales, P con 4) y Fe con 2 decimales; con precisión completa χ² difiere menos del 1 % y la decisión no cambia. Redondear solo P y Fe no alcanza para reproducirlo.

#### c) Ensayo de hipótesis (decidir) ✅

*Qué pide:* Bondad de ajuste χ² al modelo Normal: se compara χ² calculado contra el crítico.

> ⚠️ El enunciado no fija el riesgo α: se eligió α = 0,05. En el examen hay que elegirlo y JUSTIFICARLO antes de ver la muestra (p. ej. «0,05, no porque sea estándar, sino porque el perito tiene que ser imparcial»); una vez fijado, α no se toca. El valor a posteriori α* se muestra solo como dato: no se decide con él.
> ⚠️ Se amalgamaron clases con Fe < 5: de 9 a 7 clases efectivas.

- **— Modelo Normal —**
- **1 · Planteo de hipótesis**: H0: lo observado se ajusta al modelo Normal  vs  H1: no lo sigue.  α = 0,05.
- **2 · Nivel de significación**: α = 0,05 — riesgo máximo de cometer un error de tipo I (rechazar H0 siendo cierta).
- **Frecuencias esperadas** Feᵢ = N·P(clase i) (la primera y la última clase llegan al borde del dominio):

| Clase | Fo | P | Fe |
|---|---|---|---|
| 10 a 12 | 2 | 0,016 | 1,808 |
| 12 a 14 | 6 | 0,0462 | 5,224 |
| 14 a 16 | 13 | 0,1144 | 12,928 |
| 16 a 18 | 18 | 0,1978 | 22,349 |
| 18 a 20 | 30 | 0,2389 | 26,992 |
| 20 a 22 | 22 | 0,2016 | 22,778 |
| 22 a 24 | 16 | 0,1189 | 13,43 |
| 24 a 26 | 5 | 0,0489 | 5,531 |
| 26 a 28 | 1 | 0,0173 | 1,959 |

- **Amalgamado** (Fe < 5 se une con la clase vecina):

| Clase | Fo | P | Fe | (Fo - Fe)²/Fe |
|---|---|---|---|---|
| 10 a 14 | 8 | 0,0622 | 7,032 | 0,1331 |
| 14 a 16 | 13 | 0,1144 | 12,928 | 0,0004 |
| 16 a 18 | 18 | 0,1978 | 22,349 | 0,8461 |
| 18 a 20 | 30 | 0,2389 | 26,992 | 0,3353 |
| 20 a 22 | 22 | 0,2016 | 22,778 | 0,0266 |
| 22 a 24 | 16 | 0,1189 | 13,43 | 0,4917 |
| 24 a 28 | 6 | 0,0663 | 7,491 | 0,2967 |
| **Total** | **113** | **1** | **113** | **χ² = 2,13** |

- **3 · Estadístico de prueba**: χ² = Σ (Foᵢ - Feᵢ)²/Feᵢ = 2,13; ν = clases efectivas - 1 - p = 7 - 1 - 2 = 4; χ²(1-α; ν) = 9,4877.
- **Modelos y distribuciones empleados**:  
• El estadístico Σ(Fo - Fe)²/Fe sigue aproximadamente una χ² con ν = clases efectivas - 1 - (parámetros estimados con la muestra).  
• La aproximación exige N ≥ 60 y Fe ≥ 5 en cada clase (si no, se amalgaman clases). Si el modelo tiene un dominio más amplio, se completa con clases de O = 0 y probabilidad ACUMULADA (F o G), no puntual.
- **Estimación** (marcas de clase): x̄ = 19,0531, S = 3,2892.
- **Parámetros del modelo**: μ = 19,0531 (estimado), σ = 3,2892 (estimado).
- **4 · Condición de rechazo (CR)**: si χ² > 9,4877 ⇒ se rechaza H0.
- **5 · Regla de decisión (RD)**: Se calcula χ² con las frecuencias observadas y las esperadas del modelo. Si χ² > 9,4877, se rechaza H0 → se puede asegurar que la variable no sigue el modelo. En caso contrario no se rechaza H0 → no hay evidencia suficiente para asegurar que la variable no sigue el modelo.
- **6 · Cálculos y decisión**: χ² = 2,13 ≤ 9,4877 ⇒ no se rechaza H0: el modelo Normal es un buen candidato.

**Conclusión:** Con α = 0,05 no se rechaza H0: no hay evidencia suficiente para asegurar que la variable no siga el modelo Normal; el modelo Normal es un buen candidato.

**Respuesta de la guía:** c) H0) La duración de la marca “A” se comporta normalmente (parámetros estimados x̄A = 19,0531, SA = 3,2892). Amalgamando quedan 7 clases (FO: 8, 13, 18, 30, 22, 16, 6; FE: 7,03; 12,93; 22,35; 27,00; 22,78; 13,42; 7,49), dos parámetros estimados, ν = 4; χ²(0,95;4) = 9,4877; χ²calc = 2,1333. No se rechaza: el modelo normal es un buen candidato para la duración de la marca “A”.

> ≈ Coincide solo aproximadamente (2,1333): Ídem b): probabilidades de tabla en la guía; con precisión completa difiere menos del 1 % y la decisión no cambia.

#### d) Intervalo de confianza (estimar) ✅

*Qué pide:* Estimar la proporción poblacional p con un 95% de confianza mediante un intervalo de confianza. La cátedra usa el modelo exacto (Beta / F).

- **Modelos y distribuciones empleados**:  
• Cada unidad es una prueba de Bernoulli (cumple / no cumple) con probabilidad p, independientes entre sí.  
• La cantidad de casos r en una muestra de n sigue una Binomial: r ~ B(n; p).  
• El intervalo exacto usa la relación entre la Binomial y la distribución Beta (o F de Snedecor).
- **Datos**: n = 203, r = 8, p̂ = r/n = 0,0394.
- **Modelo exacto** (Beta / F, el que usa la cátedra): A = 0,0171 ; B = 0,0762.
- **Límite inferior (A)**: ν₁ = 2(n − r + 1) = 392, ν₂ = 2r = 16; F(0,975; 392; 16) = 2,3371; A = 1/[1 + (196/8)·2,3371] = 0,017165.
- **Límite superior (B)**: ν₁ = 2(r + 1) = 18, ν₂ = 2(n − r) = 390; F(0,975; 18; 390) = 1,7865; B = 1/[1 + 195/(9·1,7865)] = 0,076172.
- La estimación de p es siempre exacta (Beta / F). La aproximación normal NO se usa para estimar p: el profesor la llama «aberración»; las aproximaciones solo sirven para calcular n.

**Conclusión:** El porcentaje poblacional estará entre 1,71% y 7,62%, con un 95% de confianza: P(0,0171 ≤ p ≤ 0,0762) = 0,95 (límites redondeados hacia afuera; sin redondear: 0,017165 y 0,076172).

**Respuesta de la guía:** d) 8 de 203 equipos de la marca “B” con duración menor a 14.000 hs, p̂ = 0,0394 (3,94%). Con el modelo binomial: A = 0,0171, B = 0,0762; P(1,71% ≤ p ≤ 7,62%) = 0,95.

> 📝 *Notas de la transcripción:* Ejercicio resuelto (sin 'Resp:'); respuesta armada desde la Solución (p. 48-50). Marca B en 10-12 figura "---" (se pone null, equivale a 0). El riesgo varía por inciso: a) 10% para desvíos y 5% para medias; b), c) 5%; d) 5% (95% de confianza); alpha = 0.05 es el de la consigna d). En la Solución a) se usa t(0,95;314) = 1,6497. En d) la Solución usa "8 con duraciones menores a 14.000" (12-14 de la marca B).

<details><summary>Cómo lo concluye la guía</summary>

> De manera que la hipótesis no se rechaza por lo cual no se puede probar que los desvíos poblacionales sean distintos, de manera que se supone que los desvíos poblacionales son iguales.
> De manera que la hipótesis se rechaza, por lo cual se puede asegurar que la marca “B” tiene una mayor duración que la marca “A”, entonces se elegiría la marca “B”.
> Se rechaza la hipótesis planteada, de manera que se puede asegurar que la duración de la marca “A” no sigue el modelo normal con los parámetros especificados por el fabricante.
> No se rechaza la hipótesis planteada, de manera que no se puede asegurar que la duración de la marca “A” no sigue un modelo normal, por lo tanto, se considera que el modelo normal es un buen candidato para el ajuste del comportamiento de la duración de los conjuntos de la marca “A”.
> Se concluye que el porcentaje de equipos de la marca “B” con duración inferior a 14.000 horas estará comprendido entre 1,71% y 7,62%, afirmándolo con un 95% de confianza, o sea: P(1,71% ≤ p ≤ 7,62%) = 0,95.

</details>

---

## TEMA VII — Regresión y correlación simple

### VII-1 · Problema 1 (pág. 51)

**Enunciado.** Se desea establecer una ecuación para pronosticar el Producto Bruto Interno de un país correspondiente al Sector Agropecuario, Silvicultura y Pesca en función del área sembrada de las 5 oleaginosas principales (soja, maní, girasol, algodón y lino), a partir de los siguientes datos: [Tabla: Área sembrada (en 10^6 hectáreas) PBI (en millones de U$s) ; 3,0402 8,014 ; 2,9819 7,891 ; 3,0934 8,207 ; 3,805 8,31 ; 5,423 8,45]

- **a)** Calcular el estimador puntual del pronóstico de un año para un área sembrada de 5.401.000 hectáreas.
- **b)** Analizar el ajuste de los datos al modelo lineal mediante el coeficiente de correlación y ensayando la hipótesis de β1 = 0.
- **c)** Establecer límites del 90% de confianza para dicho pronóstico.

| Área sembrada (en 10^6 hectáreas) | PBI (en millones de U$s) |
|---|---|
| 3,0402 | 8,014 |
| 2,9819 | 7,891 |
| 3,0934 | 8,207 |
| 3,805 | 8,31 |
| 5,423 | 8,45 |

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 7,5091 + 0,1813·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 7,5091 + 0,1813·5,401 = 8,4885.

**Conclusión:** El pronóstico puntual para x₀ = 5,401 es ŷ₀ = 8,488544.

**Respuesta de la guía:** 8,488544 millones de U$s.

#### b) Validar el modelo (r, r², ensayo de β1 = 0) ✅

*Qué pide:* Validar el modelo: r, r² y ensayo de existencia (H0: β1 = 0, |t| > t(1-α; n-2)).

> ⚠️ El inciso no fija el riesgo α: se usó α = 0,05.

- **Sumatorias**: n = 5; Σx = 18,3435; Σx² = 71,5906; Σy = 40,872; Σy² = 334,3055; Σxy = 150,7258.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = 0,7787/4,2938 = 0,1813; b0 = ȳ - b1·x̄ = 8,1744 - 0,1813·3,6687 = 7,5091.
- **Recta**: ŷ = 7,5091 + 0,1813·x.
- **Ajuste**: S² = SCR/(n-2) = 0,0201; S = 0,1417; Sb1 = S/√(Σx² - n·x̄²) = 0,0684.
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = 0,8372; r² = 0,701.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = 2,6518; t(1-α; ν = 3) = 2,3534. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,6: válido para econometría (variables macro y microeconómicas).

**Conclusión:** Con α = 0,05, se puede asegurar que existe relación lineal entre las variables; r = 0,8372 (r² ≥ 0,6: válido para econometría (variables macro y microeconómicas)).

**Respuesta de la guía:** Se rechaza la hipótesis, por lo tanto, se puede afirmar que existe relación lineal entre las variables y como el valor de r = 0,8372 es alto, se puede considerar que dicha relación es fuerte para el uso dado.

#### c) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 7,5091 + 0,1813·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 7,5091 + 0,1813·5,401 = 8,4885.
- **Intervalo para un valor individual de y (intervalo de predicción)**: ŷ₀ ± t(1-α/2; ν)·S·√(1 + 1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α/2; ν) = 2,3534; error = 0,4595.

**Conclusión:** Con un 90% de confianza, el valor de y para x₀ = 5,401 estará entre 8,0289 y 8,9481: P(8,0289 ≤ y(x₀) ≤ 8,9481) = 0,9 (límites redondeados hacia afuera; sin redondear: 8,028998 y 8,94809).

**Respuesta de la guía:** Entre 8,028998 y 8,94809 millones de U$s.

> 📝 *Notas de la transcripción:* x0 = 5,401 (10^6 ha). La recta no figura en la guía; con los datos da ŷ ≈ 7,5091 + 0,1813·x (consistente con a). En c) no se aclara si es IC del valor medio o de predicción individual ('pronóstico de un año' sugiere individual).

---

### VII-2 · Problema 2 (pág. 51)

**Enunciado.** Los siguientes datos han sido tomados para estudiar la relación entre las ventas de un producto (en miles de unidades) y la relación precio del competidor/precio del propio producto: [Tabla: Relación precio de competidor/precio del propio producto Ventas (en miles de unidades) ; 0,8 36,4 ; 0,75 32,1 ; 0,6 32,3 ; 0,92 40,3 ; 0,86 37,1]

- **a)** Investigue la asociación lineal mediante los dos criterios básicos.
- **b)** Calcule la venta mínima que se obtendrá con un 90% de confianza para un mes en que la relación es igual a 0,80.

| Relación precio de competidor/precio del propio producto | Ventas (en miles de unidades) |
|---|---|
| 0,8 | 36,4 |
| 0,75 | 32,1 |
| 0,6 | 32,3 |
| 0,92 | 40,3 |
| 0,86 | 37,1 |

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Validar el modelo (r, r², ensayo de β1 = 0) ✅

*Qué pide:* Validar el modelo: r, r² y ensayo de existencia (H0: β1 = 0, |t| > t(1-α; n-2)).

> ⚠️ El inciso no fija el riesgo α: se usó α = 0,05.

- **Sumatorias**: n = 5; Σx = 3,93; Σx² = 3,1485; Σy = 178,2; Σy² = 6.399,16; Σxy = 141,557.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = 1,4918/0,0595 = 25,0638; b0 = ȳ - b1·x̄ = 35,64 - 25,0638·0,786 = 15,9398.
- **Recta**: ŷ = 15,9398 + 25,0638·x.
- **Ajuste**: S² = SCR/(n-2) = 3,5739; S = 1,8905; Sb1 = S/√(Σx² - n·x̄²) = 7,7489.
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = 0,8816; r² = 0,7772.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = 3,2345; t(1-α; ν = 3) = 2,3534. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,6: válido para econometría (variables macro y microeconómicas).

**Conclusión:** Con α = 0,05, se puede asegurar que existe relación lineal entre las variables; r = 0,8816 (r² ≥ 0,6: válido para econometría (variables macro y microeconómicas)).

**Respuesta de la guía:** Se rechaza la hipótesis, por lo tanto, se puede afirmar que existe relación lineal entre las variables y como el valor de r = 0,8816 es alto, se puede considerar que dicha relación es fuerte para el uso dado.

#### b) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 15,9398 + 25,0638·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 15,9398 + 25,0638·0,8 = 35,9909.
- **Intervalo para un valor individual de y (intervalo de predicción)**: ŷ₀ ± t(1-α; ν)·S·√(1 + 1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α; ν) = 1,6377; error = 3,3963.

**Conclusión:** Con un 90% de confianza el valor mínimo de y para x₀ = 0,8 es 32,5946 (redondeado hacia abajo; sin redondear 32,594608).

**Respuesta de la guía:** A = 32,594 miles de unidades.

> 📝 *Notas de la transcripción:* La Resp no rotula el inciso a). 'Dos criterios básicos' = ensayo de β1 = 0 y valor de r (riesgo no indicado). b) límite inferior unilateral (90%) de pronóstico individual en x0 = 0,80.

---

### VII-3 · Problema 3 (pág. 51)

**Enunciado.** Un ensayo de marketing se realizó para estudiar la relación entre el tiempo que requiere un comprador para decidirse en su compra y el número de presentaciones distintas del producto exhibidas. Las marcas se eliminaron de los productos para neutralizar el efecto de las preferencias. El estudio se realizó pidiéndoles a los compradores que seleccionen los artículos basándose exclusivamente en las descripciones y en los diseños de las presentaciones de cada producto. De los 15 participantes cada uno ha utilizado un tiempo hasta llegar a una selección que fue registrado en la siguiente tabla: [Tabla: Cantidad de presentaciones Tiempo (en segundos) ; 2 5 ; 2 8 ; 2 8 ; 2 7 ; 2 9 ; 3 7 ; 3 9 ; 3 8 ; 3 9 ; 3 10 ; 4 10 ; 4 11 ; 4 10 ; 4 12 ; 4 9]

- **a)** Hallar la recta de mínimos cuadrados.
- **b)** ¿Presentan los datos suficiente evidencia que indique que el tiempo requerido para decidir está linealmente relacionado al número de presentaciones?

| Cantidad de presentaciones | Tiempo (en segundos) |
|---|---|
| 2 | 5 |
| 2 | 8 |
| 2 | 8 |
| 2 | 7 |
| 2 | 9 |
| 3 | 7 |
| 3 | 9 |
| 3 | 8 |
| 3 | 9 |
| 3 | 10 |
| 4 | 10 |
| 4 | 11 |
| 4 | 10 |
| 4 | 12 |
| 4 | 9 |

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Recta de mínimos cuadrados (b0, b1) ✅

*Qué pide:* Recta de mínimos cuadrados: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²), b0 = ȳ - b1·x̄.

- **Sumatorias**: n = 15; Σx = 45; Σx² = 145; Σy = 132; Σy² = 1.204; Σxy = 411.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = 15/10 = 1,5; b0 = ȳ - b1·x̄ = 8,8 - 1,5·3 = 4,3.
- **Recta**: ŷ = 4,3000 + 1,5000·x.
- **Ajuste**: S² = SCR/(n-2) = 1,5308; S = 1,2372; Sb1 = S/√(Σx² - n·x̄²) = 0,3913.

**Conclusión:** b1 = 1,5: por cada unidad adicional de «Cantidad de presentaciones», «Tiempo (en segundos)» aumenta en promedio 1,5 unidades. b0 = 4,3: valor estimado de «Tiempo (en segundos)» cuando «Cantidad de presentaciones» vale 0 (ver si tiene sentido en el problema).

**Respuesta de la guía:** ŷ = 4,3 + 1,5·x

#### b) Validar el modelo (r, r², ensayo de β1 = 0) ✅

*Qué pide:* Validar el modelo: r, r² y ensayo de existencia (H0: β1 = 0, |t| > t(1-α; n-2)).

- **Sumatorias**: n = 15; Σx = 45; Σx² = 145; Σy = 132; Σy² = 1.204; Σxy = 411.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = 15/10 = 1,5; b0 = ȳ - b1·x̄ = 8,8 - 1,5·3 = 4,3.
- **Recta**: ŷ = 4,3000 + 1,5000·x.
- **Ajuste**: S² = SCR/(n-2) = 1,5308; S = 1,2372; Sb1 = S/√(Σx² - n·x̄²) = 0,3913.
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = 0,7285; r² = 0,5307.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = 3,8339; t(1-α; ν = 13) = 1,7709. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,4: válido solo para sociología o psicología.

**Conclusión:** Con α = 0,05, se puede asegurar que existe relación lineal entre las variables; r = 0,7285 (r² ≥ 0,4: válido solo para sociología o psicología).

**Respuesta de la guía:** Sí, se puede afirmar que existe relación lineal entre las variables y es válido para su uso, dado que el valor de r = 0,7285 puede considerarse una relación adecuada.

> 📝 *Notas de la transcripción:* En la guía la tabla está en filas, primero 'Tiempo (en segundos)' y luego 'Cantidad de presentaciones'; x = presentaciones, y = tiempo (verificado con la recta). Riesgo del ensayo no indicado.

---

### VII-4 · Problema 4 (pág. 51)

**Enunciado.** En un estudio de distintos fondos para inversión se desarrolló un procedimiento consistente en construir la llamada “recta característica” para cada posible fondo. Esta es la recta de regresión de la rentabilidad del fondo considerado sobre la rentabilidad promedio del mercado bursátil. Si para un fondo de inversión la pendiente de su recta es significativamente distinta de cero, se dice que el fondo es muy sensible a las fluctuaciones de la bolsa de valores y por ende es una inversión riesgosa. Si el fondo tiene una recta con pendiente cercana a cero se dice que es una inversión estable y de poco riesgo. La rentabilidad del fondo "Penn Square Mutual" y la rentabilidad promedio en el mercado bursátil se han observado en el período de 10 años consecutivos y se dan en la siguiente tabla (los valores negativos figuran entre paréntesis): [Tabla: Año Bolsa Fondo ; 1 12,9 18,4 ; 2 9,1 29,7 ; 3 -13,1 -12,3 ; 4 20,1 10,8 ; 5 7,7 23,6 ; 6 -11,4 -16,2 ; 7 0,1 5,8 ; 8 10,8 7,2 ; 9 15,6 7,7 ; 10 -17,4 -8,8]

- **a)** Hallar la recta de regresión de la rentabilidad del fondo "Penn Square Mutual" en función de la rentabilidad promedio en el mercado bursátil.
- **b)** Hallar un intervalo de confianza del 95% para el coeficiente de regresión.

| Año | Bolsa | Fondo |
|---|---|---|
| 1 | 12,9 | 18,4 |
| 2 | 9,1 | 29,7 |
| 3 | -13,1 | -12,3 |
| 4 | 20,1 | 10,8 |
| 5 | 7,7 | 23,6 |
| 6 | -11,4 | -16,2 |
| 7 | 0,1 | 5,8 |
| 8 | 10,8 | 7,2 |
| 9 | 15,6 | 7,7 |
| 10 | -17,4 | -8,8 |

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Recta de mínimos cuadrados (b0, b1) ✅

*Qué pide:* Recta de mínimos cuadrados: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²), b0 = ȳ - b1·x̄.

- **Sumatorias**: n = 10; Σx = 34,4; Σx² = 1.676,86; Σy = 65,9; Σy² = 2.530,19; Σxy = 1.603,82.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = 1.377,124/1.558,524 = 0,8836; b0 = ȳ - b1·x̄ = 6,59 - 0,8836·3,44 = 3,5504.
- **Recta**: ŷ = 3,5504 + 0,8836·x.
- **Ajuste**: S² = SCR/(n-2) = 109,8839; S = 10,4826; Sb1 = S/√(Σx² - n·x̄²) = 0,2655.

**Conclusión:** b1 = 0,8836: por cada unidad adicional de «Bolsa», «Fondo» aumenta en promedio 0,8836 unidades. b0 = 3,5504: valor estimado de «Fondo» cuando «Bolsa» vale 0 (ver si tiene sentido en el problema).

**Respuesta de la guía:** ŷ = 3,5504 + 0,8836·x

#### b) Intervalo de confianza para β1 (contribución marginal) ✅

*Qué pide:* Intervalo de confianza para β1: b1 ± t(1-α/2; n-2)·Sb1.

- **Recta**: ŷ = 3,5504 + 0,8836·x; Sb1 = 0,2655.
- **IC para β1**: b1 ± t(1-α/2; ν = 8)·Sb1 = 0,8836 ± 2,306·0,2655 = [0,2713 ; 1,4959].

**Conclusión:** Con un 95% de confianza, por cada unidad adicional de x, y cambia entre 0,2713 y 1,4959: P(0,2713 ≤ β1 ≤ 1,4959) = 0,95.

**Respuesta de la guía:** Por cada punto adicional en la rentabilidad promedio del mercado bursátil la rentabilidad del fondo aumenta entre 0,2712 (como mínimo) y 1,4960 (como máximo).

> 📝 *Notas de la transcripción:* Los valores entre paréntesis de la guía son negativos (transcriptos con signo menos). x = Bolsa, y = Fondo; la columna Año no interviene. Ejercicio empieza en p. 51 y sigue en p. 52.

---

### VII-5 · Problema 5 (pág. 52)

**Enunciado.** Considere una compañía distribuidora de gas natural que desea predecir la demanda diaria de una ciudad (medida en 10^5 m³), de un día para el siguiente, a partir del pronóstico de la temperatura media (en ºC). A tal efecto, se registraron datos de 10 días que, luego de procesados, arrojaron: Σx = 97 ; Σx² = 1.169 ; Σy = 21,16 ; Σy² = 48,68 ; Σy·x = 180,9326

- **a)** ¿Se puede asegurar que por cada grado que desciende la temperatura, la demanda de gas aumenta en más de 7.000 m³?
- **b)** Si para un día el pronóstico de temperatura media es de 5ºC, ¿qué demanda mínima de gas se puede asegurar con un 90% de confianza?

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Ensayo sobre β1 ('por cada unidad aumenta en más de ...') ✅

*Qué pide:* Afirmación sobre el cambio de y por unidad de x: ensayo de β1 contra un valor (caso I / II de la cátedra).

> ⚠️ El inciso no fija el riesgo α: se usó α = 0,05.

- **Recta**: ŷ = 3,1502 - 0,1066·x; Sb1 = 0,0268; ν = 8.
- **Hipótesis**: H0: β1 ≥ -0,07  vs  H1: β1 < -0,07  (α = 0,05).
- **Valor crítico** (planteo a priori): b1c = β1₀ - t(1-α; ν)·Sb1 = -0,07 - 1,8595·0,0268 = -0,1199.
- **Condición de rechazo**: si b1 < -0,1199 ⇒ se rechaza H0. b1 = -0,1066 ⇒ no se rechaza H0.

**Conclusión:** Con α = 0,05, no se puede asegurar que β1 < -0,07 (por cada unidad de x, y cambia menos que -0,07).

**Respuesta de la guía:** No se puede asegurar que por cada grado que desciende la temperatura la demanda aumente en más de 7.000 m³.

#### b) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 3,1502 - 0,1066·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 3,1502 + -0,1066·5 = 2,6171 → 261.710,12 en unidades.
- **Intervalo para un valor individual de y (intervalo de predicción)**: ŷ₀ ± t(1-α; ν)·S·√(1 + 1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α; ν) = 1,3968; error = 0,619.
- **En unidades**: × 100.000 → 199.812,46.

**Conclusión:** Con un 90% de confianza el valor mínimo de y para x₀ = 5 es 1,9981 (199.812,45 en unidades) (redondeado hacia abajo; sin redondear 1,998125).

**Respuesta de la guía:** A = 199.813,14 m³.

> ≈ Coincide solo aproximadamente (199.813,14): La guía usa t de tabla con 4 decimales (1,3968) y da 199.813,14; con el t exacto es 199.812,46. Usar t de tabla en toda la regresión empeora otros 16 límites, por eso la app usa el valor exacto.

> 📝 *Notas de la transcripción:* Datos resumidos (sumatorias, ver campo 'sumatorias'), n = 10; x = temperatura (ºC), y = demanda (10^5 m³). a) ensayo unilateral de β1 contra -0,07 (7.000 m³ = 0,07·10^5 m³); el riesgo no se indica. b) límite inferior unilateral (90%) de pronóstico individual en x0 = 5; la Resp está en m³ (= 1,9981314·10^5 m³).

---

### VII-6 · Problema 6 (pág. 52)

**Enunciado.** Un Jefe de Producto desea convencer a la Gerencia de que, por cada 1.000 dólares que se invierte en publicidad, pueden esperar un aumento de 2.500 dólares como mínimo en las ventas. A tal efecto, se presenta la siguiente tabla de datos históricos (valores expresados en miles de dólares): [Tabla: Gastos de publicidad Ventas ; 5 72 ; 7,2 79 ; 6,3 73 ; 4,2 59 ; 5,4 67 ; 6,8 69]

- **a)** ¿Se puede considerar que los datos confirman la afirmación del Jefe de Producto?
- **b)** Estimar con un 95% de confianza las ventas promedio si se decide no realizar ningún gasto de publicidad.

| Gastos de publicidad | Ventas |
|---|---|
| 5 | 72 |
| 7,2 | 79 |
| 6,3 | 73 |
| 4,2 | 59 |
| 5,4 | 67 |
| 6,8 | 69 |

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Ensayo sobre β1 ('por cada unidad aumenta en más de ...') ✅

*Qué pide:* Afirmación sobre el cambio de y por unidad de x: ensayo de β1 contra un valor (caso I / II de la cátedra).

> ⚠️ El inciso no fija el riesgo α: se usó α = 0,05.

- **Recta**: ŷ = 42,9860 + 4,6156·x; Sb1 = 1,7977; ν = 4.
- **Hipótesis**: H0: β1 ≤ 2,5  vs  H1: β1 > 2,5  (α = 0,05).
- **Valor crítico** (planteo a priori): b1c = β1₀ + t(1-α; ν)·Sb1 = 2,5 + 2,1318·1,7977 = 6,3323.
- **Condición de rechazo**: si b1 > 6,3323 ⇒ se rechaza H0. b1 = 4,6156 ⇒ no se rechaza H0.

**Conclusión:** Con α = 0,05, no se puede asegurar que β1 > 2,5 (por cada unidad de x, y cambia más que 2,5).

**Respuesta de la guía:** No se puede asegurar que por cada 1.000 dólares que se invierten en publicidad las ventas aumenten como mínimo en 2.500 dólares.

#### b) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 42,9860 + 4,6156·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 42,986 + 4,6156·0 = 42,986.
- **Intervalo para el valor promedio de y (ley promedio)**: ŷ₀ ± t(1-α/2; ν)·S·√(1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α/2; ν) = 2,7764; error = 29,4975.

**Conclusión:** Con un 95% de confianza, el promedio de y para x₀ = 0 estará entre 13,4885 y 72,4836: P(13,4885 ≤ μy(x₀) ≤ 72,4836) = 0,95 (límites redondeados hacia afuera; sin redondear: 13,488533 y 72,483556).

**Respuesta de la guía:** Entre 13,4885 y 72,4836 miles de U$s.

> 📝 *Notas de la transcripción:* a) ensayo unilateral de β1 contra 2,5 (riesgo no indicado). b) IC del valor medio en x0 = 0 (equivale a IC de β0). La recta no figura en la guía; con los datos da ŷ ≈ 42,986 + 4,6156·x.

---

### VII-7 · Problema 7 (pág. 52)

**Enunciado.** El continuo aumento en el precio del petróleo en los últimos años ha originado un aumento en los costos para el industrial que tiene que transportar sus bienes al mercado. Para abatir esos costos de transporte, el industrial ha sustituido los medios usuales de transporte por otros más baratos, por ejemplo, el flete ferroviario en lugar de carga aérea. En un estudio hecho en una compañía para estudiar los costos de transporte aéreo, se seleccionaron al azar 9 facturas para estimar la relación entre el costo por unidad transportada y la distancia recorrida. Los resultados se presentan en la siguiente tabla: [Tabla: Distancia recorrida (en cientos de Km) Costo (en U$s/unidad transportada) ; 6 49 ; 13 93 ; 27 159 ; 15 115 ; 9 66 ; 11 90 ; 21 139 ; 14 98 ; 12 88]

- **a)** Hallar la recta de mínimos cuadrados.
- **b)** Estimar, con un 90% de confianza, el costo medio de transporte por unidad para aquellas cargas que se enviarán a 1.700 km.
- **c)** Por lógica, si la distancia recorrida fuese de 0 km, entonces el costo debiera ser de 0 U$s. Explicar ¿por qué la recta de mínimos cuadrados no pasa por el origen?, ¿debería pasar por el origen?
- **d)** Analizar si el modelo doble logarítmico ajusta mejor al problema e indicar el significado de dicho modelo.

| Distancia recorrida (en cientos de Km) | Costo (en U$s/unidad transportada) |
|---|---|
| 6 | 49 |
| 13 | 93 |
| 27 | 159 |
| 15 | 115 |
| 9 | 66 |
| 11 | 90 |
| 21 | 139 |
| 14 | 98 |
| 12 | 88 |

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Recta de mínimos cuadrados (b0, b1) ✅

*Qué pide:* Recta de mínimos cuadrados: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²), b0 = ȳ - b1·x̄.

- **Sumatorias**: n = 9; Σx = 128; Σx² = 2.142; Σy = 897; Σy² = 98.681; Σxy = 14.452.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = 1.694,6667/321,5556 = 5,2702; b0 = ȳ - b1·x̄ = 99,6667 - 5,2702·14,2222 = 24,7125.
- **Recta**: ŷ = 24,7125 + 5,2702·x.
- **Ajuste**: S² = SCR/(n-2) = 49,8205; S = 7,0584; Sb1 = S/√(Σx² - n·x̄²) = 0,3936.

**Conclusión:** b1 = 5,2702: por cada unidad adicional de «Distancia recorrida (en cientos de Km)», «Costo (en U$s/unidad transportada)» aumenta en promedio 5,2702 unidades. b0 = 24,7125: valor estimado de «Costo (en U$s/unidad transportada)» cuando «Distancia recorrida (en cientos de Km)» vale 0 (ver si tiene sentido en el problema).

**Respuesta de la guía:** ŷ = 24,7125 + 5,2702·x

#### b) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 24,7125 + 5,2702·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 24,7125 + 5,2702·17 = 114,3062.
- **Intervalo para el valor promedio de y (ley promedio)**: ŷ₀ ± t(1-α/2; ν)·S·√(1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α/2; ν) = 1,8946; error = 4,9154.

**Conclusión:** Con un 90% de confianza, el promedio de y para x₀ = 17 estará entre 109,3907 y 119,2216: P(109,3907 ≤ μy(x₀) ≤ 119,2216) = 0,9 (límites redondeados hacia afuera; sin redondear: 109,390785 y 119,221517).

**Respuesta de la guía:** Entre 109,39 y 119,23 U$s/unidad transportada.

#### c) Recta por el origen (b0 = 0) ✅

*Qué pide:* Pide el modelo con intercepto 0: b1 = Σxy / Σx².

- **Sumatorias**: n = 9; Σx = 128; Σx² = 2.142; Σy = 897; Σy² = 98.681; Σxy = 14.452.
- **Recta por el origen**: b1 = Σxy / Σx² = 6,747.
- **Recta**: ŷ = 6,7470·x.
- **Ajuste**: S² = SCR/(n-1) = 146,7319; S = 12,1133; Sb1 = S/√(Σx² - n·x̄²) = 0,2617.

**Conclusión:** Con intercepto 0 el modelo es ŷ = 6,7470·x. b1 = 6,747: por cada unidad adicional de «Distancia recorrida (en cientos de Km)», «Costo (en U$s/unidad transportada)» aumenta en promedio 6,747 unidades. Solo conviene si el entorno de observación está cerca de x = 0.

**Respuesta de la guía:** La recta hallada no pasa por el origen porque la misma responde al entorno de observación (el cual no tiene a 0 como punto de observación). La recta debería pasar por el origen, por lo cual se debería hallar la recta con el intercepto igual a 0, que es: ŷ = 6,7470·x.

#### d) Modelo linealizable (doble logarítmico / logarítmico lineal) ✅

*Qué pide:* Pide probar un modelo linealizable: se ajusta la recta sobre las variables transformadas y se compara r².

- **Modelo**: ln ŷ = b0 + b1·ln x  (y = e^b0 · x^b1, elasticidad constante). Se trabaja con Y' = ln y y X' = ln x.
- **Sumatorias**: n = 9; Σx = 23,1242; Σx² = 60,9716; Σy = 40,9245; Σy² = 187,1179; Σxy = 106,3994.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = 1,2498/1,5573 = 0,8026; b0 = ȳ - b1·x̄ = 4,5472 - 0,8026·2,5694 = 2,4851.
- **Recta**: ln ŷ = 2,4851 + 0,8026·ln x.
- **Ajuste**: S² = SCR/(n-2) = 0,0035; S = 0,0589; Sb1 = S/√(Σx² - n·x̄²) = 0,0472.
- **Volviendo a la escala original**: y = 12,0026·x^0,8026.
- **Comparación**: r lineal = 0,981 (r² = 0,9624); r loglog = 0,9881 (r² = 0,9763).
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = 0,9881; r² = 0,9763.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = 16,9948; t(1-α; ν = 7) = 1,4149. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,9: el modelo es válido para cualquier campo de aplicación.
- **Pronóstico con este modelo**:
- **Recta**: ln ŷ = 2,4851 + 0,8026·ln x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 2,4851 + 0,8026·17 = 4,7589 (= 116,6207 en la escala original).
- **Intervalo para el valor promedio de y (ley promedio)**: ŷ₀ ± t(1-α/2; ν)·S·√(1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α/2; ν) = 1,8946; error = 0,0441.
- **Antitransformando** (e^límite): [111,5925 ; 121,8754].

**Conclusión:** El modelo doble logarítmico ajusta mejor que el lineal (r² 0,9763 vs 0,9624). b1 = 0,8026 es la elasticidad: si «Distancia recorrida (en cientos de Km)» aumenta 1%, «Costo (en U$s/unidad transportada)» cambia 0,8026%. Con un 90% de confianza, el promedio de y para x₀ = 17 estará entre 4,7148 y 4,8030: P(4,7148 ≤ μy(x₀) ≤ 4,8030) = 0,9 (límites redondeados hacia afuera; sin redondear: 4,714854 y 4,802999).

**Respuesta de la guía:** El modelo será: ŷ = 12,0026·x^0,8026, el modelo lineal nos queda ln(ŷ) = 2,4851 + 0,8026·ln(x). Este modelo ajusta mejor y además indica el cambio porcentual del costo de transporte ante un cambio porcentual en la distancia recorrida, o sea cuando la distancia recorrida aumenta en 1% el costo por unidad transportada aumenta en 0,8026%. Este modelo corresponde a la elasticidad del costo por unidad transportada respecto de la distancia recorrida. La respuesta para la pregunta b) sería: entre 111,59 y 121,88 U$s/unidad transportada.

> 📝 *Notas de la transcripción:* x en cientos de km: 1.700 km → x0 = 17. En d) el IC de b) se recalcula con el modelo doble logarítmico (en escala log y antitransformado). Resp en p. 53.

---

### VII-8 · Problema 8 (pág. 53)

**Enunciado.** Se condujo un experimento en un supermercado para estudiar la relación entre la cantidad de espacio destinado a un determinado café y su volumen de ventas semanales. La cantidad de espacio destinado en la estantería se varía en exhibidores de 3, 6 y 9 anaqueles al azar durante 12 semanas, mientras que, para las otras marcas de café, se mantuvieron constantes en exhibidores de 3 anaqueles. Los datos del experimento se dan a continuación: [Tabla: Cantidad de exhibidores Ventas semanales (en unidades) ; 6 526 ; 3 421 ; 6 581 ; 9 630 ; 3 412 ; 9 560 ; 6 434 ; 3 443 ; 9 590 ; 6 570 ; 3 346 ; 9 672]

- **a)** Hallar la recta de mínimos cuadrados, validar el modelo e interpretar ambos estimadores en términos del problema.
- **b)** Estimar la fuerza de la relación de ambas variables para un 90% de confianza.
- **c)** Indicar y estimar, para un 90% de confianza, la influencia porcentual que tiene la cantidad de anaqueles de exhibición en las ventas semanales.
- **d)** El gerente comercial afirma que por cada anaquel adicional en la exhibición las ventas semanales se incrementarán en 20 unidades, para un riesgo del 5%, ¿es correcta la afirmación del gerente?
- **e)** Estimar con un 90% de confianza la contribución marginal que tiene cada anaquel adicional en las ventas semanales.
- **f)** Hallar un intervalo de confianza del 90% para la venta media semanal de café si se presenta en exhibidores de 6 anaqueles.
- **g)** Si durante la semana entrante se va a presentar el café en un exhibidor de 6 anaqueles, hallar un intervalo de predicción del 90% para las ventas semanales. Explicar la diferencia entre este intervalo y el obtenido en el punto anterior.
- **h)** La recta por lógica tiene intercepto igual a 0, ¿cómo sería el modelo estimador?

| Cantidad de exhibidores | Ventas semanales (en unidades) |
|---|---|
| 6 | 526 |
| 3 | 421 |
| 6 | 581 |
| 9 | 630 |
| 3 | 412 |
| 9 | 560 |
| 6 | 434 |
| 3 | 443 |
| 9 | 590 |
| 6 | 570 |
| 3 | 346 |
| 9 | 672 |

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Validar el modelo (r, r², ensayo de β1 = 0) ✅

*Qué pide:* Validar el modelo: r, r² y ensayo de existencia (H0: β1 = 0, |t| > t(1-α; n-2)).

> ⚠️ El inciso no fija el riesgo α: se usó α = 0,05.

- **Sumatorias**: n = 12; Σx = 72; Σx² = 504; Σy = 6.185; Σy² = 3.300.627; Σxy = 39.600.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = 2.490/72 = 34,5833; b0 = ȳ - b1·x̄ = 515,4167 - 34,5833·6 = 307,9167.
- **Recta**: ŷ = 307,9167 + 34,5833·x.
- **Ajuste**: S² = SCR/(n-2) = 2.666,2417; S = 51,6357; Sb1 = S/√(Σx² - n·x̄²) = 6,0853.
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = 0,8738; r² = 0,7636.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = 5,6831; t(1-α; ν = 10) = 1,8125. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,6: válido para econometría (variables macro y microeconómicas).

**Conclusión:** Con α = 0,05, se puede asegurar que existe relación lineal entre las variables; r = 0,8738 (r² ≥ 0,6: válido para econometría (variables macro y microeconómicas)).

**Respuesta de la guía:** ŷ = 307,916̄ + 34,583̄·x, existe relación lineal entre variables, r = 0,8738 (se puede considerar que la relación es fuerte) o sea que el modelo se puede considerar válido para lo que se está empleando. El valor de b1 indica que por cada anaquel adicional en la exhibición del café las ventas semanales se incrementarán en aproximadamente 34,58 unidades, el valor de b0 indica que si no se exhibiera el café las ventas semanales serían aproximadamente de 307,92 unidades (esto es ridículo ya que, si el café no se exhibe, el mismo no se vende). Este es otro ejemplo de un modelo con intercepto igual a 0.

#### b) Intervalo de confianza para ρ (fuerza de la relación) ✅

*Qué pide:* Estimar ρ: transformación de Fisher Z = ½·ln((1+r)/(1-r)) ± z/√(n-3).

- **Coeficiente de correlación**: r = 0,8738 (n = 12).
- **Fisher**: Z = ½·ln((1+r)/(1-r)) = 1,3491; Z(1-α/2) /√(n-3) = 1,6449/√9 = 0,5483; Zmín = 0,8008; Zmáx = 1,8973.
- **Límites**: A = (e^(2Zmín) - 1)/(e^(2Zmín) + 1) = 0,6645; B = (e^(2Zmáx) - 1)/(e^(2Zmáx) + 1) = 0,956.

**Conclusión:** Con un 90% de confianza el coeficiente de correlación poblacional está entre 0,6645 y 0,956: P(0,6645 ≤ ρ ≤ 0,956) = 0,9.

**Respuesta de la guía:** Entre 0,6645 y 0,9561.

#### c) Intervalo para ρ² (influencia porcentual) ✅

*Qué pide:* Influencia porcentual: r² y su intervalo (los límites del IC de ρ al cuadrado).

- **Coeficiente de determinación**: r² = 0,7636 (76,36% de la variación de y se explica por x).
- **Fisher**: Z = ½·ln((1+r)/(1-r)) = 1,3491; Z(1-α/2) /√(n-3) = 1,6449/√9 = 0,5483; Zmín = 0,8008; Zmáx = 1,8973.
- **Límites**: A = (e^(2Zmín) - 1)/(e^(2Zmín) + 1) = 0,6645; B = (e^(2Zmáx) - 1)/(e^(2Zmáx) + 1) = 0,956.
- **IC para ρ²**: los límites al cuadrado → [0,4415 ; 0,914].

**Conclusión:** x influye en un 76,36% en la explicación de y; con un 90% de confianza la influencia porcentual está entre el 44,15% y el 91,4%.

**Respuesta de la guía:** r² = 0,7636, indica que la cantidad de anaqueles en la exhibición influyen, aproximadamente, en un 76,36% en las ventas semanales, se estima que la influencia porcentual se encuentra entre el 44,15% y 91,4%.

#### d) Ensayo sobre β1 ('por cada unidad aumenta en más de ...') ✅

*Qué pide:* Afirmación sobre el cambio de y por unidad de x: ensayo de β1 contra un valor (caso I / II de la cátedra).

- **Recta**: ŷ = 307,9167 + 34,5833·x; Sb1 = 6,0853; ν = 10.
- **Hipótesis**: H0: β1 ≤ 20  vs  H1: β1 > 20  (α = 0,05).
- **Valor crítico** (planteo a priori): b1c = β1₀ + t(1-α; ν)·Sb1 = 20 + 1,8125·6,0853 = 31,0294.
- **Condición de rechazo**: si b1 > 31,0294 ⇒ se rechaza H0. b1 = 34,5833 ⇒ se rechaza H0.

**Conclusión:** Con α = 0,05, se puede asegurar que β1 > 20 (por cada unidad de x, y cambia más que 20).

**Respuesta de la guía:** Se puede asegurar que por cada anaquel adicional en la exhibición las ventas semanales se incrementarán en más de 20 unidades, se considera correcta la afirmación del gerente.

#### e) Intervalo de confianza para β1 (contribución marginal) ✅

*Qué pide:* Intervalo de confianza para β1: b1 ± t(1-α/2; n-2)·Sb1.

- **Recta**: ŷ = 307,9167 + 34,5833·x; Sb1 = 6,0853.
- **IC para β1**: b1 ± t(1-α/2; ν = 10)·Sb1 = 34,5833 ± 1,8125·6,0853 = [23,5539 ; 45,6127].

**Conclusión:** Con un 90% de confianza, por cada unidad adicional de x, y cambia entre 23,5539 y 45,6127: P(23,5539 ≤ β1 ≤ 45,6127) = 0,9.

**Respuesta de la guía:** Entre 23,55 y 45,62 unidades/anaquel de exhibición.

#### f) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 307,9167 + 34,5833·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 307,9167 + 34,5833·6 = 515,4167.
- **Intervalo para el valor promedio de y (ley promedio)**: ŷ₀ ± t(1-α/2; ν)·S·√(1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α/2; ν) = 1,8125; error = 27,0164.

**Conclusión:** Con un 90% de confianza, el promedio de y para x₀ = 6 estará entre 488,4002 y 542,4331: P(488,4002 ≤ μy(x₀) ≤ 542,4331) = 0,9 (límites redondeados hacia afuera; sin redondear: 488,400245 y 542,433089).

**Respuesta de la guía:** Entre 488,40 y 542,44 unidades en promedio.

#### g) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 307,9167 + 34,5833·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 307,9167 + 34,5833·6 = 515,4167.
- **Intervalo para un valor individual de y (intervalo de predicción)**: ŷ₀ ± t(1-α/2; ν)·S·√(1 + 1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α/2; ν) = 1,8125; error = 97,4091.

**Conclusión:** Con un 90% de confianza, el valor de y para x₀ = 6 estará entre 418,0075 y 612,8258: P(418,0075 ≤ y(x₀) ≤ 612,8258) = 0,9 (límites redondeados hacia afuera; sin redondear: 418,007572 y 612,825762).

**Respuesta de la guía:** Entre 418 y 613 unidades.

#### h) Recta por el origen (b0 = 0) ✅

*Qué pide:* Pide el modelo con intercepto 0: b1 = Σxy / Σx².

- **Sumatorias**: n = 12; Σx = 72; Σx² = 504; Σy = 6.185; Σy² = 3.300.627; Σxy = 39.600.
- **Recta por el origen**: b1 = Σxy / Σx² = 78,5714.
- **Recta**: ŷ = 78,5714·x.
- **Ajuste**: S² = SCR/(n-1) = 17.199,8571; S = 131,1482; Sb1 = S/√(Σx² - n·x̄²) = 5,8418.

**Conclusión:** Con intercepto 0 el modelo es ŷ = 78,5714·x. b1 = 78,5714: por cada unidad adicional de «Cantidad de exhibidores», «Ventas semanales (en unidades)» aumenta en promedio 78,5714 unidades. Solo conviene si el entorno de observación está cerca de x = 0.

**Respuesta de la guía:** ŷ = 78,5714·x

> 📝 *Notas de la transcripción:* La guía escribe los coeficientes con período: 307,916̄ y 34,583̄ (= 307,9167 y 34,5833). En la tabla de la guía la fila de Ventas va primero; x = exhibidores. g) la Resp no incluye la explicación de la diferencia entre intervalos. d) no aclara la forma de H0 (unilateral β1 > 20).

---

### VII-9 · Problema 9 (pág. 53)

**Enunciado.** Una variable independiente que muestre una asociación negativa fuerte con la variable dependiente es tan útil como una que muestre una asociación positiva. El hecho importante es que la relación sea fuerte, esto es, la magnitud absoluta del coeficiente de correlación entre las 2 variables. Considerar por ejemplo a las tasas de interés y el número de nuevas construcciones. Las tasas de interés son indicadores clave para predecir el número de construcciones. Suponer que los datos de la siguiente tabla representan las tasas de interés en hipotecas y el registro de nuevas construcciones iniciadas en 8 años consecutivos: [Tabla: Año Tasa de interés (en %) Cantidad de licencias de construcción ; 1 6,5 2165 ; 2 6 2984 ; 3 6,5 2780 ; 4 7,5 1940 ; 5 8,5 1750 ; 6 9,5 1535 ; 7 10 962 ; 8 9 1310]

- **a)** Hallar la recta de mínimos cuadrados.
- **b)** Calcular el coeficiente de correlación.
- **c)** Si los indicadores económicos indican que la tasa de interés para hipotecas será del 8,5% para el próximo año, pronosticar el número de licencias de construcción que se otorgarán durante el año entrante mediante un intervalo de predicción del 95%.
- **d)** Analizar si el modelo logarítmico lineal ajusta mejor al problema e indicar el significado de dicho modelo.

| Año | Tasa de interés (en %) | Cantidad de licencias de construcción |
|---|---|---|
| 1 | 6,5 | 2165 |
| 2 | 6 | 2984 |
| 3 | 6,5 | 2780 |
| 4 | 7,5 | 1940 |
| 5 | 8,5 | 1750 |
| 6 | 9,5 | 1535 |
| 7 | 10 | 962 |
| 8 | 9 | 1310 |

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Recta de mínimos cuadrados (b0, b1) ✅

*Qué pide:* Recta de mínimos cuadrados: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²), b0 = ȳ - b1·x̄.

- **Sumatorias**: n = 8; Σx = 63,5; Σx² = 520,25; Σy = 15.426; Σy² = 33.143.750; Σxy = 115.464.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = -6.979,875/16,2188 = -430,3584; b0 = ȳ - b1·x̄ = 1.928,25 - -430,3584·7,9375 = 5.344,2197.
- **Recta**: ŷ = 5344,2197 - 430,3584·x.
- **Ajuste**: S² = SCR/(n-2) = 65.786,2987; S = 256,4884; Sb1 = S/√(Σx² - n·x̄²) = 63,6882.

**Conclusión:** b1 = -430,3584: por cada unidad adicional de «Tasa de interés (en %)», «Cantidad de licencias de construcción» disminuye en promedio 430,3584 unidades. b0 = 5.344,2197: valor estimado de «Cantidad de licencias de construcción» cuando «Tasa de interés (en %)» vale 0 (ver si tiene sentido en el problema).

**Respuesta de la guía:** ŷ = 5.344,2197 − 430,3584·x

#### b) Validar el modelo (r, r², ensayo de β1 = 0) ✅

*Qué pide:* Validar el modelo: r, r² y ensayo de existencia (H0: β1 = 0, |t| > t(1-α; n-2)).

> ⚠️ El inciso no fija el riesgo α: se usó α = 0,05.

- **Sumatorias**: n = 8; Σx = 63,5; Σx² = 520,25; Σy = 15.426; Σy² = 33.143.750; Σxy = 115.464.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = -6.979,875/16,2188 = -430,3584; b0 = ȳ - b1·x̄ = 1.928,25 - -430,3584·7,9375 = 5.344,2197.
- **Recta**: ŷ = 5344,2197 - 430,3584·x.
- **Ajuste**: S² = SCR/(n-2) = 65.786,2987; S = 256,4884; Sb1 = S/√(Σx² - n·x̄²) = 63,6882.
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = -0,9401; r² = 0,8839.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = -6,7573; t(1-α; ν = 6) = 1,9432. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,8: válido para procesos físicos e industriales.

**Conclusión:** Con α = 0,05, se puede asegurar que existe relación lineal entre las variables; r = -0,9401 (r² ≥ 0,8: válido para procesos físicos e industriales).

**Respuesta de la guía:** r = −0,9401

#### c) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 5344,2197 - 430,3584·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 5.344,2197 + -430,3584·8,5 = 1.686,1734.
- **Intervalo para un valor individual de y (intervalo de predicción)**: ŷ₀ ± t(1-α/2; ν)·S·√(1 + 1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α/2; ν) = 2,4469; error = 671,422.

**Conclusión:** Con un 95% de confianza, el valor de y para x₀ = 8,5 estará entre 1.014,7513 y 2.357,5955: P(1.014,7513 ≤ y(x₀) ≤ 2.357,5955) = 0,95 (límites redondeados hacia afuera; sin redondear: 1.014,751369 y 2.357,595452).

**Respuesta de la guía:** Entre 1.014 y 2.358 licencias.

#### d) Modelo linealizable (doble logarítmico / logarítmico lineal) ✅

*Qué pide:* Pide probar un modelo linealizable: se ajusta la recta sobre las variables transformadas y se compara r².

- **Modelo**: ln ŷ = b0 + b1·x  (y = e^b0 · e^(b1·x)). Se trabaja con Y' = ln y y X' = x.
- **Sumatorias**: n = 8; Σx = 63,5; Σx² = 520,25; Σy = 60,0323; Σy² = 451,4878; Σxy = 472,7095.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = -3,7969/16,2188 = -0,2341; b0 = ȳ - b1·x̄ = 7,504 - -0,2341·7,9375 = 9,3622.
- **Recta**: ln ŷ = 9,3622 - 0,2341·x.
- **Ajuste**: S² = SCR/(n-2) = 0,0191; S = 0,1381; Sb1 = S/√(Σx² - n·x̄²) = 0,0343.
- **Volviendo a la escala original**: y = 11.640,5002·0,7913^x.
- **Comparación**: r lineal = -0,9401 (r² = 0,8839); r loglin = -0,9413 (r² = 0,886).
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = -0,9413; r² = 0,886.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = -6,8291; t(1-α; ν = 6) = 1,9432. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,8: válido para procesos físicos e industriales.
- **Pronóstico con este modelo**:
- **Recta**: ln ŷ = 9,3622 - 0,2341·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 9,3622 + -0,2341·8,5 = 7,3724 (= 1.591,3743 en la escala original).
- **Intervalo para un valor individual de y (intervalo de predicción)**: ŷ₀ ± t(1-α/2; ν)·S·√(1 + 1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α/2; ν) = 2,4469; error = 0,3614.
- **Antitransformando** (e^límite): [1.108,716 ; 2.284,1488].

**Conclusión:** El modelo logarítmico lineal ajusta mejor que el lineal (r² 0,886 vs 0,8839). Por cada unidad adicional de «Tasa de interés (en %)», «Cantidad de licencias de construcción» cambia un -20,87% (factor e^b1 = 0,7913). Con un 95% de confianza, el valor de y para x₀ = 8,5 estará entre 7,0109 y 7,7338: P(7,0109 ≤ y(x₀) ≤ 7,7338) = 0,95 (límites redondeados hacia afuera; sin redondear: 7,010958 y 7,733749).

**Respuesta de la guía:** El modelo será: ŷ = 11.640,5·0,7913^x, el modelo lineal nos queda ln(ŷ) = 9,3623 − 0,2341·x. Este modelo ajusta mejor y además indica el cambio porcentual de las licencias de construcción ante un cambio unitario de la tasa de interés. o sea cuando la tasa de interés aumenta en 1% las licencias de construcción disminuyen en 23,41%. La respuesta para la pregunta c) sería: entre 1.108 y 2.285 licencias.

> 📝 *Notas de la transcripción:* Modelo log-lineal (exponencial): ln y = β0 + β1·x, ŷ = e^b0·(e^b1)^x. La guía interpreta b1 = -0,2341 como 'disminuyen en 23,41%' (aproximación; 1 − 0,7913 = 20,87%). La columna Año no interviene. Incisos y Resp en p. 54.

---

### VII-10 · Problema 10 (pág. 54)

**Enunciado.** ¿Existe relación entre el consumo de energía de un país y su P.B.I.? Se estaría dispuesto a suponer que un país con mayor ingreso per cápita requeriría de mayor consumo de energía. Para examinar esta cuestión se eligieron al azar 14 países obteniendo para ellos el consumo per cápita (en kWh) y el P.B.I. per cápita por año (en U$s), cuyos valores se presentan en la siguiente tabla: [Tabla Fuente: Banco Mundial, 2014 (Consumo) y Banco Mundial, 2018 (PBI): País Consumo de energía P.B.I. ; Noruega 23000 81807 ; Canadá 15588 46210 ; E.E.U.U. 12994 62641 ; Australia 10071 57305 ; Japón 7820 39287 ; Francia 6940 41464 ; Dinamarca 5859 60726 ; Grecia 5063 20324 ; Italia 5002 34318 ; Uruguay 3085 17278 ; Argentina 3075 11653 ; Venezuela 2719 16055 ; Brasil 2620 8921 ; India 805 2016]

- **a)** Determine mediante un coeficiente adecuado el grado de relación lineal entre el consumo de energía y el P.B.I.
- **b)** Estime con un 95% de confianza dicho coeficiente.
- **c)** ¿Presentan los datos suficiente evidencia sobre la existencia de una relación lineal entre ambas variables?
- **d)** Analizar si el modelo doble logarítmico es mejor que el modelo lineal, explicar el motivo.

*Fuente: Banco Mundial, 2014 (Consumo) y Banco Mundial, 2018 (PBI)*

| País | Consumo de energía | P.B.I. |
|---|---|---|
| Noruega | 23000 | 81807 |
| Canadá | 15588 | 46210 |
| E.E.U.U. | 12994 | 62641 |
| Australia | 10071 | 57305 |
| Japón | 7820 | 39287 |
| Francia | 6940 | 41464 |
| Dinamarca | 5859 | 60726 |
| Grecia | 5063 | 20324 |
| Italia | 5002 | 34318 |
| Uruguay | 3085 | 17278 |
| Argentina | 3075 | 11653 |
| Venezuela | 2719 | 16055 |
| Brasil | 2620 | 8921 |
| India | 805 | 2016 |

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Validar el modelo (r, r², ensayo de β1 = 0) ✅

*Qué pide:* Validar el modelo: r, r² y ensayo de existencia (H0: β1 = 0, |t| > t(1-α; n-2)).

> ⚠️ El inciso no fija el riesgo α: se usó α = 0,05.

- **Sumatorias**: n = 14; Σx = 500.005; Σx² = 25.352.409.311; Σy = 104.641; Σy² = 1.270.430.911; Σxy = 5.376.080.521.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = 1.638.864.577,7857/7.494.909.309,2143 = 0,2187; b0 = ȳ - b1·x̄ = 7.474,3571 - 0,2187·35.714,6429 = -335,1387.
- **Recta**: ŷ = -335,1387 + 0,2187·x.
- **Ajuste**: S² = SCR/(n-2) = 10.828.876,4876; S = 3.290,7258; Sb1 = S/√(Σx² - n·x̄²) = 0,038.
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = 0,8567; r² = 0,7339.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = 5,7527; t(1-α; ν = 12) = 1,7823. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,6: válido para econometría (variables macro y microeconómicas).

**Conclusión:** Con α = 0,05, se puede asegurar que existe relación lineal entre las variables; r = 0,8567 (r² ≥ 0,6: válido para econometría (variables macro y microeconómicas)).

**Respuesta de la guía:** r = 0,8567.

#### b) Intervalo de confianza para ρ (fuerza de la relación) ✅

*Qué pide:* Estimar ρ: transformación de Fisher Z = ½·ln((1+r)/(1-r)) ± z/√(n-3).

- **Coeficiente de correlación**: r = 0,8567 (n = 14).
- **Fisher**: Z = ½·ln((1+r)/(1-r)) = 1,2807; Z(1-α/2) /√(n-3) = 1,96/√11 = 0,591; Zmín = 0,6897; Zmáx = 1,8716.
- **Límites**: A = (e^(2Zmín) - 1)/(e^(2Zmín) + 1) = 0,5978; B = (e^(2Zmáx) - 1)/(e^(2Zmáx) + 1) = 0,9537.

**Conclusión:** Con un 95% de confianza el coeficiente de correlación poblacional está entre 0,5978 y 0,9537: P(0,5978 ≤ ρ ≤ 0,9537) = 0,95.

**Respuesta de la guía:** Entre 0,5978 y 0,9538.

#### c) Validar el modelo (r, r², ensayo de β1 = 0) ✅

*Qué pide:* Validar el modelo: r, r² y ensayo de existencia (H0: β1 = 0, |t| > t(1-α; n-2)).

- **Sumatorias**: n = 14; Σx = 500.005; Σx² = 25.352.409.311; Σy = 104.641; Σy² = 1.270.430.911; Σxy = 5.376.080.521.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = 1.638.864.577,7857/7.494.909.309,2143 = 0,2187; b0 = ȳ - b1·x̄ = 7.474,3571 - 0,2187·35.714,6429 = -335,1387.
- **Recta**: ŷ = -335,1387 + 0,2187·x.
- **Ajuste**: S² = SCR/(n-2) = 10.828.876,4876; S = 3.290,7258; Sb1 = S/√(Σx² - n·x̄²) = 0,038.
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = 0,8567; r² = 0,7339.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = 5,7527; t(1-α; ν = 12) = 1,7823. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,6: válido para econometría (variables macro y microeconómicas).

**Conclusión:** Con α = 0,05, se puede asegurar que existe relación lineal entre las variables; r = 0,8567 (r² ≥ 0,6: válido para econometría (variables macro y microeconómicas)).

**Respuesta de la guía:** Sí, se puede asegurar que existe relación lineal entre las variable y fuerte, de manera que el modelo es válido para el uso que se le está dando.

#### d) Modelo linealizable (doble logarítmico / logarítmico lineal) ✅

*Qué pide:* Pide probar un modelo linealizable: se ajusta la recta sobre las variables transformadas y se compara r².

- **Modelo**: ln ŷ = b0 + b1·ln x  (y = e^b0 · x^b1, elasticidad constante). Se trabaja con Y' = ln y y X' = ln x.
- **Sumatorias**: n = 14; Σx = 142,152; Σx² = 1.456,3835; Σy = 120,4549; Σy² = 1.046,2294; Σxy = 1.233,5873.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = 10,5227/13,0117 = 0,8087; b0 = ȳ - b1·x̄ = 8,6039 - 0,8087·10,1537 = 0,3926.
- **Recta**: ln ŷ = 0,3926 + 0,8087·ln x.
- **Ajuste**: S² = SCR/(n-2) = 0,1113; S = 0,3336; Sb1 = S/√(Σx² - n·x̄²) = 0,0925.
- **Volviendo a la escala original**: y = 1,4808·x^0,8087.
- **Comparación**: r lineal = 0,8567 (r² = 0,7339); r loglog = 0,9297 (r² = 0,8643).
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = 0,9297; r² = 0,8643.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = 8,7433; t(1-α; ν = 12) = 1,7823. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,8: válido para procesos físicos e industriales.

**Conclusión:** El modelo doble logarítmico ajusta mejor que el lineal (r² 0,8643 vs 0,7339). b1 = 0,8087 es la elasticidad: si «P.B.I.» aumenta 1%, «Consumo de energía» cambia 0,8087%.

**Respuesta de la guía:** El modelo doble logarítmico es mejor dado que su valor del coeficiente de correlación es r = 0,9297, dado que son variables econométricas referentes a individuos de una población. El modelo será: ŷ = 1,4808·x^0,8087, el modelo lineal nos queda ln(ŷ) = 0,3926 + 0,8087·ln(x). Indica el cambio porcentual del consumo de energía ante un cambio porcentual en el P.B.I., o sea cuando el P.B.I. aumenta en 1% el consumo de energía en 0,8087%. Este modelo corresponde a la elasticidad del consumo de energía respecto del P.B.I. del país.

> 📝 *Notas de la transcripción:* En el modelo doble log y = consumo, x = P.B.I. (verificado con los datos: ln ŷ = 0,3926 + 0,8087·ln x). 'el consumo de energía en 0,8087%' (falta 'aumenta', tal cual en la guía). Riesgo de c) no indicado.

---

### VII-11 · Problema 11 (pág. 54)

**Enunciado.** En el problema de la distribución de la energía eléctrica se trabaja con la relación entre el consumo de los usuarios y su máxima demanda de potencia. Considerar al respecto los siguientes datos: [Tabla: Consumo (en Kwh) Potencia (en Kw) ; 110 0,7 ; 568 2,41 ; 245 1,19 ; 324 1,53 ; 76 0,53]

- **a)** Si se supone que la relación es del tipo y = α·x^β, donde la variable “x” es el consumo y la variable “y” es la potencia, estimar los parámetros “α” y “β” e investigar la validez del modelo.
- **b)** Si el consumo de un usuario es de 450 Kwh, ¿cuál es la máxima demanda de potencia con una probabilidad de 0,05?

| Consumo (en Kwh) | Potencia (en Kw) |
|---|---|
| 110 | 0,7 |
| 568 | 2,41 |
| 245 | 1,19 |
| 324 | 1,53 |
| 76 | 0,53 |

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Modelo linealizable (doble logarítmico / logarítmico lineal) ✅

*Qué pide:* Pide probar un modelo linealizable: se ajusta la recta sobre las variables transformadas y se compara r².

> ⚠️ El inciso no fija el riesgo α: se usó α = 0,05.

- **Modelo**: ln ŷ = b0 + b1·ln x  (y = e^b0 · x^b1, elasticidad constante). Se trabaja con Y' = ln y y X' = ln x.
- **Sumatorias**: n = 5; Σx = 26,6553; Σx² = 144,7531; Σy = 0,4873; Σy² = 1,5151; Σxy = 4,568.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = 1,9702/2,6517 = 0,743; b0 = ȳ - b1·x̄ = 0,0975 - 0,743·5,3311 = -3,8635.
- **Recta**: ln ŷ = -3,8635 + 0,7430·ln x.
- **Ajuste**: S² = SCR/(n-2) = 0,0013; S = 0,0357; Sb1 = S/√(Σx² - n·x̄²) = 0,0219.
- **Volviendo a la escala original**: y = 0,021·x^0,743.
- **Comparación**: r lineal = 0,9995 (r² = 0,999); r loglog = 0,9987 (r² = 0,9974).
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = 0,9987; r² = 0,9974.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = 33,9067; t(1-α; ν = 3) = 2,3534. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,9: el modelo es válido para cualquier campo de aplicación.

**Conclusión:** El modelo doble logarítmico no ajusta mejor que el lineal (r² 0,9974 vs 0,999). b1 = 0,743 es la elasticidad: si «Consumo (en Kwh)» aumenta 1%, «Potencia (en Kw)» cambia 0,743%.

**Respuesta de la guía:** Se debe estudiar el siguiente modelo: ln y = ln α + β·ln x, el cual se estima con el modelo: ln ŷ = ln a + b·ln x, siendo a y b los estimadores de α y β: ln ŷ = −3,8635 + 0,743·ln x; a = 0,0210 y b = 0,7430. El modelo es válido para el uso correspondiente con un valor de r = 0,9987.

#### b) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ln ŷ = -3,8635 + 0,7430·ln x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = -3,8635 + 0,743·450 = 0,6756 (= 1,9653 en la escala original).
- **Intervalo para un valor individual de y (intervalo de predicción)**: ŷ₀ ± t(1-α; ν)·S·√(1 + 1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α; ν) = 2,3534; error = 0,1004.
- **Antitransformando** (e^límite): 2,1728.

**Conclusión:** Con un 95% de confianza el valor máximo de y para x₀ = 450 es 0,7761 (redondeado hacia arriba; sin redondear 0,776).

**Respuesta de la guía:** 2,1728 Kw.

> 📝 *Notas de la transcripción:* La Resp no rotula el inciso a). b) se interpreta como límite superior unilateral (95%) de pronóstico individual en x0 = 450, calculado en escala log y antitransformado. Incisos y Resp en p. 55.

---

### VII-12 · Problema 12 (pág. 55)

**Enunciado.** En la producción de herramientas, el método para deformar acero a temperatura normal mantiene una relación lineal con la dureza del mismo ya que, a medida que la deformación crece, se ve afectada la dureza del acero. Para investigar esta relación se evaluaron 12 muestras de acero, los resultados obtenidos se visualizan en la siguiente tabla: [Tabla: Deformación (en mm) Dureza Brinell (en kg/mm²) ; 6 70 ; 9 68 ; 10 66 ; 12 55 ; 14 52 ; 15 50 ; 18 48 ; 22 44 ; 26 40 ; 28 37 ; 33 35 ; 35 30]

- **a)** Hallar la recta de mínimos cuadrados, validar el modelo e interpretar ambos estimadores en términos del problema.
- **b)** Estimar la fuerza de la relación de ambas variables para un 95% de confianza.
- **c)** Indicar y estimar, para un 95% de confianza, la influencia porcentual que tiene la deformación del acero en la dureza del mismo.
- **d)** Se puede afirmar que, por cada milímetro adicional en la deformación del acero, la dureza brinell disminuye en más de 1 kg/mm², para un riesgo del 5%.
- **e)** Estimar con un 95% de confianza la contribución marginal que tiene cada milímetro de deformación del acero en la dureza brinell del mismo.
- **f)** Hallar un intervalo de confianza del 95% para la dureza brinell promedio del acero, si la deformación del mismo fuese de 10 mm.
- **g)** Si a un determinado acero se lo somete a una deformación de 10 mm, hallar un intervalo de predicción del 95% para la dureza brinell.

| Deformación (en mm) | Dureza Brinell (en kg/mm²) |
|---|---|
| 6 | 70 |
| 9 | 68 |
| 10 | 66 |
| 12 | 55 |
| 14 | 52 |
| 15 | 50 |
| 18 | 48 |
| 22 | 44 |
| 26 | 40 |
| 28 | 37 |
| 33 | 35 |
| 35 | 30 |

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Validar el modelo (r, r², ensayo de β1 = 0) ✅

*Qué pide:* Validar el modelo: r, r² y ensayo de existencia (H0: β1 = 0, |t| > t(1-α; n-2)).

> ⚠️ El inciso no fija el riesgo α: se usó α = 0,05.

- **Sumatorias**: n = 12; Σx = 228; Σx² = 5.364; Σy = 595; Σy² = 31.443; Σxy = 9.943.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = -1.362/1.032 = -1,3198; b0 = ȳ - b1·x̄ = 49,5833 - -1,3198·19 = 74,6589.
- **Recta**: ŷ = 74,6589 - 1,3198·x.
- **Ajuste**: S² = SCR/(n-2) = 14,3393; S = 3,7867; Sb1 = S/√(Σx² - n·x̄²) = 0,1179.
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = -0,9624; r² = 0,9261.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = -11,1963; t(1-α; ν = 10) = 1,8125. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,9: el modelo es válido para cualquier campo de aplicación.

**Conclusión:** Con α = 0,05, se puede asegurar que existe relación lineal entre las variables; r = -0,9624 (r² ≥ 0,9: el modelo es válido para cualquier campo de aplicación).

**Respuesta de la guía:** ŷ = 74,6589 − 1,3198·x; S = 3,7867; Sb1 = 0,1179; r = −0,9624; r² = 0,9261. H0) ρ = 0 (β1 = 0): t_obs = −11,1963 (|t_obs| = 11,1963) vs t(0,95;10) = 1,8125: se rechaza; existe relación lineal fuerte y el modelo es válido. b1: por cada mm adicional de deformación la dureza se reduce en promedio 1,3198 kg/mm²; b0: con deformación nula la dureza sería 74,6589 kg/mm².

#### b) Intervalo de confianza para ρ (fuerza de la relación) ✅

*Qué pide:* Estimar ρ: transformación de Fisher Z = ½·ln((1+r)/(1-r)) ± z/√(n-3).

- **Coeficiente de correlación**: r = -0,9624 (n = 12).
- **Fisher**: Z = ½·ln((1+r)/(1-r)) = -1,9768; Z(1-α/2) /√(n-3) = 1,96/√9 = 0,6533; Zmín = -2,6301; Zmáx = -1,3235.
- **Límites**: A = (e^(2Zmín) - 1)/(e^(2Zmín) + 1) = -0,9897; B = (e^(2Zmáx) - 1)/(e^(2Zmáx) + 1) = -0,8676.

**Conclusión:** Con un 95% de confianza el coeficiente de correlación poblacional está entre -0,9897 y -0,8676: P(-0,9897 ≤ ρ ≤ -0,8676) = 0,95.

**Respuesta de la guía:** Z = −3,9536 ± 0,6533: Zρmín = −2,6301; ZρMáx = −1,3235 (tal cual en la guía). P(−0,9897 ≤ ρ ≤ −0,8676) = 0,95.

#### c) Intervalo para ρ² (influencia porcentual) ✅

*Qué pide:* Influencia porcentual: r² y su intervalo (los límites del IC de ρ al cuadrado).

- **Coeficiente de determinación**: r² = 0,9261 (92,61% de la variación de y se explica por x).
- **Fisher**: Z = ½·ln((1+r)/(1-r)) = -1,9768; Z(1-α/2) /√(n-3) = 1,96/√9 = 0,6533; Zmín = -2,6301; Zmáx = -1,3235.
- **Límites**: A = (e^(2Zmín) - 1)/(e^(2Zmín) + 1) = -0,9897; B = (e^(2Zmáx) - 1)/(e^(2Zmáx) + 1) = -0,8676.
- **IC para ρ²**: los límites al cuadrado → [0,7528 ; 0,9794].

**Conclusión:** x influye en un 92,61% en la explicación de y; con un 95% de confianza la influencia porcentual está entre el 75,28% y el 97,94%.

**Respuesta de la guía:** r² = 0,9261 (92,61%); P(0,7528 ≤ ρ² ≤ 0,9795) = 0,95: la influencia se encuentra entre el 75,28% y el 97,95%.

#### d) Ensayo sobre β1 ('por cada unidad aumenta en más de ...') ✅

*Qué pide:* Afirmación sobre el cambio de y por unidad de x: ensayo de β1 contra un valor (caso I / II de la cátedra).

- **Recta**: ŷ = 74,6589 - 1,3198·x; Sb1 = 0,1179; ν = 10.
- **Hipótesis**: H0: β1 ≥ -1  vs  H1: β1 < -1  (α = 0,05).
- **Valor crítico** (planteo a priori): b1c = β1₀ - t(1-α; ν)·Sb1 = -1 - 1,8125·0,1179 = -1,2136.
- **Condición de rechazo**: si b1 < -1,2136 ⇒ se rechaza H0. b1 = -1,3198 ⇒ se rechaza H0.

**Conclusión:** Con α = 0,05, se puede asegurar que β1 < -1 (por cada unidad de x, y cambia menos que -1).

**Respuesta de la guía:** H0) β1 ≥ −1 kg/mm²; b1c = −1 − 1,8125·0,1179 = −1,2136; se rechaza la hipótesis nula: por cada mm de deformación la dureza brinell disminuye en más de 1 kg/mm².

#### e) Intervalo de confianza para β1 (contribución marginal) ✅

*Qué pide:* Intervalo de confianza para β1: b1 ± t(1-α/2; n-2)·Sb1.

- **Recta**: ŷ = 74,6589 - 1,3198·x; Sb1 = 0,1179.
- **IC para β1**: b1 ± t(1-α/2; ν = 10)·Sb1 = -1,3198 ± 2,2281·0,1179 = [-1,5824 ; -1,0571].

**Conclusión:** Con un 95% de confianza, por cada unidad adicional de x, y cambia entre -1,5824 y -1,0571: P(-1,5824 ≤ β1 ≤ -1,0571) = 0,95.

**Respuesta de la guía:** −1,3198 ± 2,2281·0,1179 = −1,3198 ± 0,2626: entre −1,5824 y −1,0572 (kg/mm²)/mm.

#### f) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 74,6589 - 1,3198·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 74,6589 + -1,3198·10 = 61,4612.
- **Intervalo para el valor promedio de y (ley promedio)**: ŷ₀ ± t(1-α/2; ν)·S·√(1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α/2; ν) = 2,2281; error = 3,3941.

**Conclusión:** Con un 95% de confianza, el promedio de y para x₀ = 10 estará entre 58,0671 y 64,8554: P(58,0671 ≤ μy(x₀) ≤ 64,8554) = 0,95 (límites redondeados hacia afuera; sin redondear: 58,067136 y 64,855345).

**Respuesta de la guía:** ŷ0 = 61,4612 kg/mm²; 61,4612 ± 2,2281·3,7867·√(1/12 + (10−19)²/(5.364−12·19²)) = 61,4612 ± 3,3941: entre 58,0671 y 64,8554 kg/mm².

#### g) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 74,6589 - 1,3198·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 74,6589 + -1,3198·10 = 61,4612.
- **Intervalo para un valor individual de y (intervalo de predicción)**: ŷ₀ ± t(1-α/2; ν)·S·√(1 + 1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α/2; ν) = 2,2281; error = 9,0945.

**Conclusión:** Con un 95% de confianza, el valor de y para x₀ = 10 estará entre 52,3667 y 70,5557: P(52,3667 ≤ y(x₀) ≤ 70,5557) = 0,95 (límites redondeados hacia afuera; sin redondear: 52,366787 y 70,555694).

**Respuesta de la guía:** 61,4612 ± 9,0943: entre 52,3667 y 70,5557 kg/mm².

> ≈ Coincide solo aproximadamente (9,0943): La guía informa la semiamplitud ±9,0943 calculada con t de tabla (2,2281); los límites del intervalo coinciden.

> 📝 *Notas de la transcripción:* Sin 'Resp:'; respuesta armada desde la Solución (pp. 55-56). En a) se plantea H0) ρ = 0 / β1 = 0 con riesgo 5% pero se compara con t(0,95;10) = 1,8125 (valor de tabla unilateral); los IC usan t(0,975;10) = 2,2281 y Z(0,975) = 1,96. b) Z = ½·ln((1+r)/(1−r)) ± Z·1/√(n−3) = −3,9536 ± 0,6533 en la guía, pero ½·ln((1−0,9624)/(1+0,9624)) = −1,98 y Zmín/Zmáx = −2,6301/−1,3235 corresponden a −1,9768 ± 0,6533; el '−3,9536' parece ser ln(...) sin el ½ (se transcribe igual). d) se resuelve por valor crítico: b1c = β1 − t(0,95;10)·Sb1 y se compara con b1.

<details><summary>Cómo lo concluye la guía</summary>

> n = 12; Σx = 228, x̄ = 19; Σx² = 5.364; Σy = 595, ȳ = 49,583̄; Σy² = 31.443; Σxy = 9.943.
> Quiere decir que, por cada milímetro adicional en la deformación del acero, la dureza brinell se reduce en promedio 1,3198 kg/mm².
> Quiere decir que, si la deformación en milímetros del acero fuese nula, la dureza brinell sería 74,6589 kg/mm².
> La recta de mínimos cuadrados queda: ŷ = 74,6589 − 1,3198·x.
> Se rechaza la hipótesis y se puede afirmar que existe relación lineal entre las variables, y como el valor de r es alto dicha relación es fuerte o consistente. De manera que el modelo es válido para cualquier campo de aplicación ya que el valor de r es mayor que 0,90.
> La relación es considerada fuerte y consistente para cualquier campo de aplicación.
> r² = 0,9261, o sea que el 92,61% de la dureza brinell del acero se explica por la deformación en milímetros. La influencia se encuentra entre el 75,28% y el 97,95% con un 95% de confianza.
> Se rechaza la hipótesis nula, entonces se puede afirmar que por cada milímetro de deformación en el acero la dureza brinell disminuye en más de 1 kg/mm².
> Con un 95% de seguridad los límites estarán comprendidos entre −1,5824 y −1,0572 (kg/mm²)/mm.
> Los límites de la dureza brinell promedio del acero estarán comprendidos entre 58,0671 kg/mm² y 64,8554 kg/mm², con un 95% de seguridad.
> Los límites de la dureza brinell del acero estarán comprendidos entre 52,3667 kg/mm² y 70,5557 kg/mm², con un 95% de seguridad.

</details>

---

### VII-13 · Problema 13 (pág. 57)

**Enunciado.** La carbonatación del hormigón armado influye en la duración de estructuras debido a la corrosión de las varillas de acero de refuerzo. La carbonatación del hormigón es el resultado de una reacción química que baja el pH lo suficiente para iniciar la corrosión de las varillas. Es muy importante controlar la penetración en profundidad de la carbonatación debida a la porosidad del hormigón. Se han tomado datos de varias muestras de una estructura de hormigón armado midiéndose la resistencia (a la rotura o quiebre) medida en mega pascales (MPa) y la profundidad de carbonatación medida en milímetros (mm). Se parte de la base que la carbonatación (X) es la variable que influye sobre la variable resistencia (Y). Los valores obtenidos de 18 muestras fueron: [Tabla: X = Carbonatación (en mm) Y = Resistencia al quiebre (en MPa) ; 8 22,8 ; 15 27,2 ; 16,5 23,7 ; 20 17,1 ; 20 21,5 ; 27,5 18,6 ; 30 16,1 ; 30 20,4 ; 35 13,4 ; 38 18,5 ; 40 12,4 ; 45 13,2 ; 50 11,4 ; 50 10,3 ; 55 14,1 ; 55 9,7 ; 59 12 ; 65 6,8]

- **a)** Hallar la recta de mínimos cuadrados, validar el modelo e interpretar ambos estimadores en términos del problema.
- **b)** Estimar la fuerza de la relación de ambas variables para un 95% de confianza.
- **c)** Indicar y estimar, para un 95% de confianza, la influencia porcentual que tiene la penetración del poro en el hormigón en la resistencia al quiebre del mismo.
- **d)** Se puede afirmar que, por cada milímetro en la penetración en el hormigón, la resistencia al quiebre disminuye en más de 0,25 Mpa, para un riesgo del 5%.
- **e)** Estimar con un 95% de confianza la contribución marginal que tiene cada milímetro de penetración en la resistencia al quiebre del hormigón.
- **f)** Hallar un intervalo de confianza del 95% para la resistencia al quiebre promedio, si la penetración fuese de 10 mm.
- **g)** Si en un determinado sector de la estructura del hormigón se encuentra una penetración de 10 mm, hallar un intervalo de predicción del 95% para la resistencia al quiebre.

| X = Carbonatación (en mm) | Y = Resistencia al quiebre (en MPa) |
|---|---|
| 8 | 22,8 |
| 15 | 27,2 |
| 16,5 | 23,7 |
| 20 | 17,1 |
| 20 | 21,5 |
| 27,5 | 18,6 |
| 30 | 16,1 |
| 30 | 20,4 |
| 35 | 13,4 |
| 38 | 18,5 |
| 40 | 12,4 |
| 45 | 13,2 |
| 50 | 11,4 |
| 50 | 10,3 |
| 55 | 14,1 |
| 55 | 9,7 |
| 59 | 12 |
| 65 | 6,8 |

*Tema detectado por la app: Regresión y correlación simple (TEMA VII).*

#### a) Validar el modelo (r, r², ensayo de β1 = 0) ✅

*Qué pide:* Validar el modelo: r, r² y ensayo de existencia (H0: β1 = 0, |t| > t(1-α; n-2)).

> ⚠️ El inciso no fija el riesgo α: se usó α = 0,05.

- **Sumatorias**: n = 18; Σx = 659; Σx² = 28.967,5; Σy = 289,2; Σy² = 5.166,36; Σxy = 9.165,95.
- **Estimadores**: b1 = (Σxy - n·x̄·ȳ)/(Σx² - n·x̄²) = -1.421,9833/4.840,7778 = -0,2938; b0 = ȳ - b1·x̄ = 16,0667 - -0,2938·36,6111 = 26,8212.
- **Recta**: ŷ = 26,8212 - 0,2938·x.
- **Ajuste**: S² = SCR/(n-2) = 6,3857; S = 2,527; Sb1 = S/√(Σx² - n·x̄²) = 0,0363.
- **Coeficiente de correlación**: r = Sxy/√(Sxx·Syy) = -0,8964; r² = 0,8035.
- **1er criterio (existencia de la relación)**: H0: β1 = 0 (ρ = 0)  vs  H1: β1 ≠ 0. tc = b1/Sb1 = r/√((1-r²)/(n-2)) = -8,0879; t(1-α; ν = 16) = 1,7459. |tc| > t ⇒ se rechaza H0: existe relación lineal.
- **2do criterio (fuerza de la relación)**: r² ≥ 0,8: válido para procesos físicos e industriales.

**Conclusión:** Con α = 0,05, se puede asegurar que existe relación lineal entre las variables; r = -0,8964 (r² ≥ 0,8: válido para procesos físicos e industriales).

**Respuesta de la guía:** ŷ = 26,8212 − 0,2938·x, existe relación lineal entre variables, r = 0,8964 (se puede considerar que la relación es fuerte) o sea que el modelo se puede considerar válido para lo que se está empleando. El valor de b1 indica que por cada mm de penetración en el hormigón, la resistencia al quiebre disminuye en aproximadamente 0,2937 Mpa, el valor de b0 indica que, si no se hubiera penetración en el hormigón, la resistencia al quiebre sería aproximadamente de 26,8212 Mpa.

#### b) Intervalo de confianza para ρ (fuerza de la relación) ✅

*Qué pide:* Estimar ρ: transformación de Fisher Z = ½·ln((1+r)/(1-r)) ± z/√(n-3).

- **Coeficiente de correlación**: r = -0,8964 (n = 18).
- **Fisher**: Z = ½·ln((1+r)/(1-r)) = -1,4534; Z(1-α/2) /√(n-3) = 1,96/√15 = 0,5061; Zmín = -1,9595; Zmáx = -0,9474.
- **Límites**: A = (e^(2Zmín) - 1)/(e^(2Zmín) + 1) = -0,961; B = (e^(2Zmáx) - 1)/(e^(2Zmáx) + 1) = -0,7386.

**Conclusión:** Con un 95% de confianza el coeficiente de correlación poblacional está entre -0,961 y -0,7386: P(-0,961 ≤ ρ ≤ -0,7386) = 0,95.

**Respuesta de la guía:** Entre (-0,96105) y (-0,73858).

#### c) Intervalo para ρ² (influencia porcentual) ✅

*Qué pide:* Influencia porcentual: r² y su intervalo (los límites del IC de ρ al cuadrado).

- **Coeficiente de determinación**: r² = 0,8035 (80,35% de la variación de y se explica por x).
- **Fisher**: Z = ½·ln((1+r)/(1-r)) = -1,4534; Z(1-α/2) /√(n-3) = 1,96/√15 = 0,5061; Zmín = -1,9595; Zmáx = -0,9474.
- **Límites**: A = (e^(2Zmín) - 1)/(e^(2Zmín) + 1) = -0,961; B = (e^(2Zmáx) - 1)/(e^(2Zmáx) + 1) = -0,7386.
- **IC para ρ²**: los límites al cuadrado → [0,5455 ; 0,9236].

**Conclusión:** x influye en un 80,35% en la explicación de y; con un 95% de confianza la influencia porcentual está entre el 54,55% y el 92,36%.

**Respuesta de la guía:** r² = 0,8035, indica que la penetración en el hormigón influye, aproximadamente, en un 80,35% en la resistencia al quiebre, se estima que la influencia porcentual se encuentra entre el 54,55% y 92,37%.

#### d) Ensayo sobre β1 ('por cada unidad aumenta en más de ...') ✅

*Qué pide:* Afirmación sobre el cambio de y por unidad de x: ensayo de β1 contra un valor (caso I / II de la cátedra).

- **Recta**: ŷ = 26,8212 - 0,2938·x; Sb1 = 0,0363; ν = 16.
- **Hipótesis**: H0: β1 ≥ -0,25  vs  H1: β1 < -0,25  (α = 0,05).
- **Valor crítico** (planteo a priori): b1c = β1₀ - t(1-α; ν)·Sb1 = -0,25 - 1,7459·0,0363 = -0,3134.
- **Condición de rechazo**: si b1 < -0,3134 ⇒ se rechaza H0. b1 = -0,2938 ⇒ no se rechaza H0.

**Conclusión:** Con α = 0,05, no se puede asegurar que β1 < -0,25 (por cada unidad de x, y cambia menos que -0,25).

**Respuesta de la guía:** No se puede asegurar que la resistencia al quiebre disminuya en más de 0,25 Mpa.

#### e) Intervalo de confianza para β1 (contribución marginal) ✅

*Qué pide:* Intervalo de confianza para β1: b1 ± t(1-α/2; n-2)·Sb1.

- **Recta**: ŷ = 26,8212 - 0,2938·x; Sb1 = 0,0363.
- **IC para β1**: b1 ± t(1-α/2; ν = 16)·Sb1 = -0,2938 ± 2,1199·0,0363 = [-0,3707 ; -0,2168].

**Conclusión:** Con un 95% de confianza, por cada unidad adicional de x, y cambia entre -0,3707 y -0,2168: P(-0,3707 ≤ β1 ≤ -0,2168) = 0,95.

**Respuesta de la guía:** Entre (-0,2937) y (-0,3708) Mpa/mm.

#### f) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 26,8212 - 0,2938·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 26,8212 + -0,2938·10 = 23,8837.
- **Intervalo para el valor promedio de y (ley promedio)**: ŷ₀ ± t(1-α/2; ν)·S·√(1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α/2; ν) = 2,1199; error = 2,4067.

**Conclusión:** Con un 95% de confianza, el promedio de y para x₀ = 10 estará entre 21,4769 y 26,2905: P(21,4769 ≤ μy(x₀) ≤ 26,2905) = 0,95 (límites redondeados hacia afuera; sin redondear: 21,476971 y 26,290443).

**Respuesta de la guía:** Entre 21,4769 y 26,2905 Mpa.

#### g) Pronóstico (puntual / intervalo para el promedio o para un valor individual) ✅

*Qué pide:* Pide un pronóstico de y para x₀: ŷ₀ = b0 + b1·x₀ y su intervalo.

- **Recta**: ŷ = 26,8212 - 0,2938·x.
- **Estimador puntual**: ŷ₀ = b0 + b1·x₀ = 26,8212 + -0,2938·10 = 23,8837.
- **Intervalo para un valor individual de y (intervalo de predicción)**: ŷ₀ ± t(1-α/2; ν)·S·√(1 + 1/n + (x₀ - x̄)²/(Σx² - n·x̄²)); t(1-α/2; ν) = 2,1199; error = 5,8728.

**Conclusión:** Con un 95% de confianza, el valor de y para x₀ = 10 estará entre 18,0109 y 29,7565: P(18,0109 ≤ y(x₀) ≤ 29,7565) = 0,95 (límites redondeados hacia afuera; sin redondear: 18,010919 y 29,756495).

**Respuesta de la guía:** Entre 18,0109 y 29,7565 Mpa.

> 📝 *Notas de la transcripción:* La Resp no rotula el inciso a) (se le agregó 'a)' en 'respuesta'). r = 0,8964 figura sin signo aunque la pendiente es negativa (con los datos r = −0,8964). La interpretación de b1 dice 0,2937 vs 0,2938 en la recta. e) 'Entre (-0,2937) y (-0,3708)' parece inconsistente: −0,2937 es la estimación puntual, no un límite (con los datos: b1 = −0,29375, Sb1 = 0,03632, t(0,975;16) = 2,1199 → IC entre −0,3707 y −0,2168). d) consistente con los datos (t = (−0,2938+0,25)/0,0363 ≈ −1,20, no se rechaza).

---

## TEMA VIII — Modelo lineal general

### VIII-1 · Problema 1 (pág. 58)

**Enunciado.** En la absorción de tierra y sedimento en la que se mide la magnitud en la que los productos químicos se acumulan en forma condensada en la superficie es una característica importante que influye en la eficiencia de insecticidas y varios productos químicos. Se presentan los siguientes datos en la siguiente tabla: [Tabla: Observación Índice de Absorción Cant. de hierro extraíble Cant. de aluminio extraíble ; 1 4 61 13 ; 2 18 175 21 ; 3 14 111 24 ; 4 18 124 23 ; 5 26 130 64 ; 6 26 173 38 ; 7 21 169 33 ; 8 30 169 61 ; 9 28 160 39 ; 10 36 244 71 ; 11 65 257 112 ; 12 62 333 88 ; 13 40 199 54] Se quiere averiguar la relación existente entre el índice de absorción de fosfato en función de la cantidad de hierro extraíble y la cantidad de aluminio extraíble. Realizar un análisis completo.

| Observación | Índice de Absorción | Cant. de hierro extraíble | Cant. de aluminio extraíble |
|---|---|---|---|
| 1 | 4 | 61 | 13 |
| 2 | 18 | 175 | 21 |
| 3 | 14 | 111 | 24 |
| 4 | 18 | 124 | 23 |
| 5 | 26 | 130 | 64 |
| 6 | 26 | 173 | 38 |
| 7 | 21 | 169 | 33 |
| 8 | 30 | 169 | 61 |
| 9 | 28 | 160 | 39 |
| 10 | 36 | 244 | 71 |
| 11 | 65 | 257 | 112 |
| 12 | 62 | 333 | 88 |
| 13 | 40 | 199 | 54 |

*Tema detectado por la app: Modelo lineal general / regresión múltiple (TEMA VIII).*

#### Resolución (Modelo lineal general: estimación y validación (F global, t parciales, R²)) ✅

*Qué pide:* Modelo lineal general: b = (X'X)⁻¹X'y, F global, t parciales, R² y R² ajustado.

- **Modelo**: ŷ = -7,3507 + 0,1127·x1 + 0,3490·x2  (n = 13, k = 2, p = 3).
- **Ajuste**: S² = SCR/(n-p) = 19,1789; S = 4,3794; R² = 0,9485; R² ajustado = 1 - (1-R²)·(n-1)/(n-p) = 0,9382.
- **Análisis global** (H0: β1 = ... = βk = 0): Fc = (R²/k)/((1-R²)/(n-p)) = 92,0256; F(1-α; 2; 10) = 4,1028 ⇒ se rechaza H0: el modelo en forma global es adecuado.
- **Análisis individual** (H0: βi = 0; se rechaza si |tc| > t(1-α; n-p) = 1,8125):

| Variable | bi | Cii | Sbi = S·√Cii | tc = bi/Sbi | ¿aporta? |
|---|---|---|---|---|---|
| x1 | 0,1127 | 0,000046 | 0,0297 | 3,7969 | sí |
| x2 | 0,349 | 0,000265 | 0,0713 | 4,8944 | sí |

- **Coeficientes de determinación parcial** (aporte de cada variable cuando están las demás): R²(x1) = 0,5904; R²(x2) = 0,7055.
- **Modelos simples** (para los coeficientes parciales, R²(xi) = (R² - r²sin xi)/(1 - r²sin xi)): ŷ = -10,6112 + 0,2282·x1 (r² = 0,825); ŷ = 2,0325 + 0,5641·x2 (r² = 0,8742).

**Conclusión:** El modelo, en forma global, es adecuado y todas las variables aportan significativamente a la explicación de Y. R² = 0,9485, R² ajustado = 0,9382.

**Respuesta de la guía:** Análisis de sensibilidad: queda solo el modelo completo y = f(x1; x2) (los demás se descartan por Cp > 5·p). ŷ = −7,3507 + 0,1127·x1 + 0,3490·x2; S = 4,3794; S² = 19,1789; C1 = 0,000046; C2 = 0,0002651; R² = 0,9485; R²Aj = 0,9438; Sb1 = 0,0297; Sb2 = 0,0713. Ensayo global H0) ρ² = 0 (β1 = β2 = 0): F = 92,0874 > F(0,95;2;10) = 4,1028, se rechaza: modelo globalmente adecuado. H0) β1 = 0: t = 3,7969 > t(0,95;10) = 1,8125, se rechaza (X1 aporta). H0) β2 = 0: t = 4,8944 > 1,8125, se rechaza (X2 aporta). El modelo completo es válido y explica el índice de absorción en un 94,38%. Coeficientes de determinación parciales: R²x1 = 0,7055 (calculado con el modelo simple ŷ = −10,6112 + 0,2282·x1): X1 aporta un 70,55% cuando además actúa X2; R²x2 = 0,5904 (con el modelo simple ŷ = 2,0325 + 0,5641·x2): X2 aporta un 59,04% cuando además actúa X1.

> ≈ Coincide solo aproximadamente (0,9438, 92,0874): F: la guía usa R² redondeado a 0,9485 y da 92,0874; exacto es 92,0256 (la decisión no cambia). El texto dice R²aj = 0,9438 (dígitos transpuestos): su propia tabla y el cálculo dan 0,9382.

> 📝 *Notas de la transcripción:* Sin 'Resp:'; respuesta armada desde la Solución (pp. 58-59). Sumatorias usadas en la Solución: Σy = 388, Σy·x1 = 82.252, Σy·x2 = 24.899, Σy² = 15.302. La Solución escribe Sb2 = S·√C1 (errata: debería ser √C2; el valor 0,0713 sí usa C2). R²Aj = 0,9438 en el texto vs 0,9382 en la tabla de sensibilidad (1 − 0,0515·12/10 = 0,9382, parece transposición de dígitos); el '94,38%' de la conclusión usa el del texto. Los ensayos t parciales (bilaterales, riesgo 5%) se comparan con t(0,95;10) = 1,8125. Los coeficientes de determinación parciales: R²x1 se calcula con la regresión simple de Y sobre X1 (y viceversa), aunque el texto dice 'X1 aporta ... cuando además actúa X2' (coeficiente parcial de la variable que se agrega: la nomenclatura parece cruzada; se transcribe igual). Coeficientes verificados con los datos.

<details><summary>Cómo lo concluye la guía</summary>

> Para el procesamiento de los datos y cálculos correspondientes se debe usar computadora.
> Primero se realiza el análisis de sensibilidad para saber cuál es el mejor modelo candidato (tabla: y=f(x1): DET 1, Cp/p 12,4775, R² 0,8250, R²Aj 0,8091, S² 59,2017, PRESS 913,7020; y=f(x2): DET 1, Cp/p 7,7082, R² 0,8742, R²Aj 0,8627, S² 42,5709, PRESS 634,4821; y=f(x1;x2): DET 0,3689, Cp/p 1, R² 0,9485, R²Aj 0,9382, S² 19,1789, PRESS 334,4554).
> El único modelo que queda del análisis es el modelo completo: y = f(x1 ; x2). Los demás se descartan por tener el “Cp” mayor a 5 veces el valor de “p”.
> El modelo es: ŷ = −7,3507 + 0,1127·x1 + 0,3490·x2.
> F_calc = (0,9485/2)/((1−0,9485)/(13−3)) = 92,0874; se compara con F(0,95;2;10) = 4,1028. Se rechaza la hipótesis, por lo tanto, se puede considerar al modelo en forma global adecuado.
> t_obs = 0,1127/0,0297 = 3,7969 vs t(0,95;10) = 1,8125. Se rechaza la hipótesis y se puede afirmar que la variable “X1” aporta significativamente un grado de explicación en el estudio de la variable “Y”.
> t_obs = 0,3490/0,0713 = 4,8944 vs t(0,95;10) = 1,8125. Se rechaza la hipótesis y se puede afirmar que la variable “X2” aporta significativamente un grado de explicación en el estudio de la variable “Y”.
> Se puede afirmar que el modelo completo es válido y adecuado. De manera que el modelo completo explica al índice de absorción en un 94,38% aproximadamente.
> Modelo de regresión simple con “X1”: ŷ = −10,6112 + 0,2282·x1 (b01 = −10,6112, b1' = 0,2282). R²x1 = [(b0−b01)·Σy + (b1−b1')·Σy·x1 + b2·Σy·x2] / [Σy² − b01·Σy − b1'·Σy·x1] = [(−7,3507+10,6112)·388 + (0,1127−0,2282)·82.252 + 0,349·24.899] / [15.302 + 10,6112·388 − 0,2282·82.252] = 0,7055. Quiere decir que la variable “X1” aporta un 70,55% de explicación en la variable “Y” cuando además actúa “X2”.
> Modelo de regresión simple con “X2”: ŷ = 2,0325 + 0,5641·x2 (b02 = 2,0325, b2' = 0,5641). R²x2 = [(−7,3507−2,0325)·388 + 0,1127·82.252 + (0,349−0,5641)·24.899] / [15.302 − 2,0325·388 − 0,5641·24.899] = 0,5904. Quiere decir que la variable “X2” aporta un 59,04% de explicación en la variable “Y” cuando además actúa “X1”.

</details>

---

### VIII-2 · Problema 2 (pág. 59)

**Enunciado.** Se ha registrado la producción anual de trigo en una región agrícola. Considere las variables: “Y” (Producción de trigo de la región, en miles de toneladas); “X1” (Área sembrada de trigo en una región agrícola, en miles de hectáreas), y, “X2” (Lluvia caída en los meses de setiembre y octubre, en mm). Los siguientes datos se han registrado en los últimos 10 años de las variables mencionadas: [Tabla: X1 X2 Y ; 24,81 46 43,127 ; 15,71 35 16,653 ; 14,58 135 92,322 ; 34,04 11 38,084 ; 27,09 57 61,939 ; 49,7 14 92,376 ; 20,37 12 24,373 ; 25,75 96 74,029 ; 36,09 32 70,772 ; 28,05 45 68,749]

- **a)** Efectúe la estimación de los parámetros del modelo lineal general y su validación global.
- **b)** Determinar los coeficientes de determinación múltiple (el común, el ajustado y los parciales).

| X1 | X2 | Y |
|---|---|---|
| 24,81 | 46 | 43,127 |
| 15,71 | 35 | 16,653 |
| 14,58 | 135 | 92,322 |
| 34,04 | 11 | 38,084 |
| 27,09 | 57 | 61,939 |
| 49,7 | 14 | 92,376 |
| 20,37 | 12 | 24,373 |
| 25,75 | 96 | 74,029 |
| 36,09 | 32 | 70,772 |
| 28,05 | 45 | 68,749 |

*Tema detectado por la app: Modelo lineal general / regresión múltiple (TEMA VIII).*

#### a) Modelo lineal general: estimación y validación (F global, t parciales, R²) ✅

*Qué pide:* Modelo lineal general: b = (X'X)⁻¹X'y, F global, t parciales, R² y R² ajustado.

- **Modelo**: ŷ = -40,2208 + 2,3931·x1 + 0,6702·x2  (n = 10, k = 2, p = 3).
- **Ajuste**: S² = SCR/(n-p) = 84,3591; S = 9,1847; R² = 0,9073; R² ajustado = 1 - (1-R²)·(n-1)/(n-p) = 0,8808.
- **Análisis global** (H0: β1 = ... = βk = 0): Fc = (R²/k)/((1-R²)/(n-p)) = 34,246; F(1-α; 2; 7) = 4,7374 ⇒ se rechaza H0: el modelo en forma global es adecuado.
- **Análisis individual** (H0: βi = 0; se rechaza si |tc| > t(1-α; n-p) = 1,8946):

| Variable | bi | Cii | Sbi = S·√Cii | tc = bi/Sbi | ¿aporta? |
|---|---|---|---|---|---|
| x1 | 2,3931 | 0,001401 | 0,3437 | 6,962 | sí |
| x2 | 0,6702 | 0,000096 | 0,0901 | 7,4368 | sí |

- **Coeficientes de determinación parcial** (aporte de cada variable cuando están las demás): R²(x1) = 0,8738; R²(x2) = 0,8877.
- **Modelos simples** (para los coeficientes parciales, R²(xi) = (R² - r²sin xi)/(1 - r²sin xi)): ŷ = 28,7691 + 1,0671·x1 (r² = 0,1747); ŷ = 41,5915 + 0,3447·x2 (r² = 0,2652).

**Conclusión:** El modelo, en forma global, es adecuado y todas las variables aportan significativamente a la explicación de Y. R² = 0,9073, R² ajustado = 0,8808.

**Respuesta de la guía:** ŷ = −40,2208 + 2,3931·x1 + 0,6702·x2; el modelo, en forma global, es adecuado; las variables X1 y X2 aportan significativamente un grado de explicación en el estudio de Y.

#### b) Modelo lineal general: estimación y validación (F global, t parciales, R²) ✅

*Qué pide:* Modelo lineal general: b = (X'X)⁻¹X'y, F global, t parciales, R² y R² ajustado.

- **Modelo**: ŷ = -40,2208 + 2,3931·x1 + 0,6702·x2  (n = 10, k = 2, p = 3).
- **Ajuste**: S² = SCR/(n-p) = 84,3591; S = 9,1847; R² = 0,9073; R² ajustado = 1 - (1-R²)·(n-1)/(n-p) = 0,8808.
- **Análisis global** (H0: β1 = ... = βk = 0): Fc = (R²/k)/((1-R²)/(n-p)) = 34,246; F(1-α; 2; 7) = 4,7374 ⇒ se rechaza H0: el modelo en forma global es adecuado.
- **Análisis individual** (H0: βi = 0; se rechaza si |tc| > t(1-α; n-p) = 1,8946):

| Variable | bi | Cii | Sbi = S·√Cii | tc = bi/Sbi | ¿aporta? |
|---|---|---|---|---|---|
| x1 | 2,3931 | 0,001401 | 0,3437 | 6,962 | sí |
| x2 | 0,6702 | 0,000096 | 0,0901 | 7,4368 | sí |

- **Coeficientes de determinación parcial** (aporte de cada variable cuando están las demás): R²(x1) = 0,8738; R²(x2) = 0,8877.
- **Modelos simples** (para los coeficientes parciales, R²(xi) = (R² - r²sin xi)/(1 - r²sin xi)): ŷ = 28,7691 + 1,0671·x1 (r² = 0,1747); ŷ = 41,5915 + 0,3447·x2 (r² = 0,2652).

**Conclusión:** El modelo, en forma global, es adecuado y todas las variables aportan significativamente a la explicación de Y. R² = 0,9073, R² ajustado = 0,8808.

**Respuesta de la guía:** R² = 0,9073 (90,73%), R²Aj = 0,8957 (89,57%), se puede decir que el modelo (en forma global) aporta para la explicación de “Y” el 89,57%; R²x1 = 0,8877 (88,77%), la variable “X1” aporta el 88,77% en la explicación de “Y” cuando está actuando “X2” y R²x2 = 0,8738 (87,38%), la variable “X2” aporta el 87,38% en la explicación de “Y” cuando está actuando “X1”.

> ≈ Coincide solo aproximadamente (0,8957): La guía da R²aj = 0,8957, que sale con (n − 1)/(n − k); con la fórmula de la teoría, (n − 1)/(n − p), es 0,8808.

> 📝 *Notas de la transcripción:* Coeficientes y R² = 0,9073 verificados con los datos. R²Aj con n = 10, p = 3 da 1 − 0,0927·9/7 = 0,8808, no 0,8957 como dice la guía (se transcribe igual). El riesgo de los ensayos no se indica (presumiblemente 5%).

---

### VIII-3 · Problema 3 (pág. 59)

**Enunciado.** Se quiere estudiar el tiempo para la realización de una prueba atlética de deportistas. Se han tomado datos de 6 atletas, de las siguientes variables: [Tabla: X1: Estatura (en cm) X2: Peso (en kg) X3: Edad (en años) Y: Tiempo de realización de la prueba (en segundos) ; 165 64 25 15 ; 175 68 40 25 ; 180 68 30 17 ; 200 72 42 30 ; 195 70 28 25 ; 183 68 45 32]

- **a)** Estime los parámetros del modelo lineal general y efectúe la validación.
- **b)** Considere el modelo con las variables X1 y X3 solamente y compárelo con el modelo completo, ¿cuál elegiría?

| X1: Estatura (en cm) | X2: Peso (en kg) | X3: Edad (en años) | Y: Tiempo de realización de la prueba (en segundos) |
|---|---|---|---|
| 165 | 64 | 25 | 15 |
| 175 | 68 | 40 | 25 |
| 180 | 68 | 30 | 17 |
| 200 | 72 | 42 | 30 |
| 195 | 70 | 28 | 25 |
| 183 | 68 | 45 | 32 |

*Tema detectado por la app: Modelo lineal general / regresión múltiple (TEMA VIII).*

#### a) Modelo lineal general: estimación y validación (F global, t parciales, R²) ✅

*Qué pide:* Modelo lineal general: b = (X'X)⁻¹X'y, F global, t parciales, R² y R² ajustado.

- **Modelo**: ŷ = 40,4622 + 0,6470·x1 - 2,3392·x2 + 0,7138·x3  (n = 6, k = 3, p = 4).
- **Ajuste**: S² = SCR/(n-p) = 7,5881; S = 2,7546; R² = 0,9346; R² ajustado = 1 - (1-R²)·(n-1)/(n-p) = 0,8365.
- **Análisis global** (H0: β1 = ... = βk = 0): Fc = (R²/k)/((1-R²)/(n-p)) = 9,5247; F(1-α; 3; 2) = 19,1643 ⇒ no se rechaza H0: el modelo en forma global no es adecuado.
- **Análisis individual** (H0: βi = 0; se rechaza si |tc| > t(1-α; n-p) = 2,92):

| Variable | bi | Cii | Sbi = S·√Cii | tc = bi/Sbi | ¿aporta? |
|---|---|---|---|---|---|
| x1 | 0,647 | 0,018202 | 0,3716 | 1,741 | no |
| x2 | -2,3392 | 0,490435 | 1,9291 | -1,2126 | no |
| x3 | 0,7138 | 0,004717 | 0,1892 | 3,7728 | sí |

- **Coeficientes de determinación parcial** (aporte de cada variable cuando están las demás): R²(x1) = 0,6025; R²(x2) = 0,4237; R²(x3) = 0,8768.
- **Modelos simples** (para los coeficientes parciales, R²(xi) = (R² - r²sin xi)/(1 - r²sin xi)): ŷ = -39,7193 + 0,3482·x1 (r² = 0,4337); ŷ = -95,9057 + 1,7547·x2 (r² = 0,4689); ŷ = -0,6408 + 0,704·x3 (r² = 0,7435).

**Conclusión:** El modelo, en forma global, no es adecuado para explicar Y. R² = 0,9346, R² ajustado = 0,8365.

**Respuesta de la guía:** ŷ = 40,4622 + 0,647·x1 − 2,3392·x2 + 0,7138·x3, el modelo en forma global no es adecuado para el análisis; según el análisis solamente nos quedamos con el modelo que contiene a la variable x3 (el cual es el modelo más simple y es la variable que aporta significativamente un grado de explicación en el estudio de Y).

#### b) Comparar un modelo con algunas variables contra el completo ✅

*Qué pide:* Compara el modelo con esas variables contra el completo (R² ajustado, S², tests t).

- **Modelo completo**: ŷ = 40,4622 + 0,6470·x1 - 2,3392·x2 + 0,7138·x3  (n = 6, k = 3, p = 4).
- **Ajuste**: S² = SCR/(n-p) = 7,5881; S = 2,7546; R² = 0,9346; R² ajustado = 1 - (1-R²)·(n-1)/(n-p) = 0,8365.
- **Análisis global** (H0: β1 = ... = βk = 0): Fc = (R²/k)/((1-R²)/(n-p)) = 9,5247; F(1-α; 3; 2) = 19,1643 ⇒ no se rechaza H0: el modelo en forma global no es adecuado.
- **Análisis individual** (H0: βi = 0; se rechaza si |tc| > t(1-α; n-p) = 2,92):

| Variable | bi | Cii | Sbi = S·√Cii | tc = bi/Sbi | ¿aporta? |
|---|---|---|---|---|---|
| x1 | 0,647 | 0,018202 | 0,3716 | 1,741 | no |
| x2 | -2,3392 | 0,490435 | 1,9291 | -1,2126 | no |
| x3 | 0,7138 | 0,004717 | 0,1892 | 3,7728 | sí |

- **Modelo reducido**: ŷ = -35,6717 + 0,2137·x1 + 0,5873·x3  (n = 6, k = 2, p = 3).
- **Ajuste**: S² = SCR/(n-p) = 8,7778; S = 2,9627; R² = 0,8865; R² ajustado = 1 - (1-R²)·(n-1)/(n-p) = 0,8108.
- **Análisis global** (H0: β1 = ... = βk = 0): Fc = (R²/k)/((1-R²)/(n-p)) = 11,7151; F(1-α; 2; 3) = 9,5521 ⇒ se rechaza H0: el modelo en forma global es adecuado.
- **Análisis individual** (H0: βi = 0; se rechaza si |tc| > t(1-α; n-p) = 2,3534):

| Variable | bi | Cii | Sbi = S·√Cii | tc = bi/Sbi | ¿aporta? |
|---|---|---|---|---|---|
| x1 | 0,2137 | 0,001377 | 0,1099 | 1,9442 | no |
| x3 | 0,5873 | 0,003284 | 0,1698 | 3,4592 | sí |


**Conclusión:** R² ajustado: 0,8108 el reducido vs 0,8365 el completo; S²: 8,7778 vs 7,5881. Conviene el modelo reducido porque es más simple (parsimonia) y el completo no es válido. Pero x1 no aporta explicación: el modelo válido es ŷ = -0,6408 + 0,7040·x3.

**Respuesta de la guía:** El modelo con x1 y x3 es mejor que el modelo completo, pero la variable x1 no aporta explicación en el estudio de Y. El modelo válido es: ŷ = −0,6408 + 0,7040·x3

> 📝 *Notas de la transcripción:* Coeficientes del modelo completo y del modelo con x3 verificados con los datos. En b) no se dan los coeficientes del modelo con X1 y X3. Riesgo no indicado.

---

### VIII-4 · Problema 4 (pág. 59)

**Enunciado.** La eficiencia en el diseño de ciertos incineradores de desperdicios, requieren información acerca del “Contenido Energético” de los desperdicios. Se proporcionan los siguientes datos acerca del contenido energético del compost de desperdicios (en Kcal/kg), en función de tres variables de composición física del compost: el “porcentaje de plásticos en peso” (X1), el “porcentaje de papel en peso” (X2), el “porcentaje de basura orgánica en peso” (X3) y el “porcentaje de humedad en peso” (X4). Se observan en la siguiente tabla una muestra de 30 datos proporcionados para desperdicios obtenidos en cierta región: [Tabla: Obs. Cont. energético (Y) % de plástico (X1) % de papel (X2) % de basura (X3) % de humedad (X4) ; 1 947 18,69 15,65 45,01 58,21 ; 2 1407 19,43 23,51 39,69 46,31 ; 3 1452 19,24 24,23 43,16 46,63 ; 4 1553 22,64 22,2 35,76 45,85 ; 5 989 16,54 23,56 41,2 55,14 ; 6 1162 21,44 23,65 35,56 54,24 ; 7 1466 19,53 24,45 40,18 47,2 ; 8 1656 23,97 19,39 44,11 43,82 ; 9 1254 21,45 23,84 35,41 51,01 ; 10 1336 20,34 26,5 34,21 49,06 ; 11 1097 17,03 23,46 32,45 53,23 ; 12 1266 21,03 26,99 38,19 51,78 ; 13 1401 20,49 19,87 41,35 46,69 ; 14 1223 20,45 23,03 43,59 53,57 ; 15 1216 18,81 22,62 42,2 52,98 ; 16 1334 18,28 21,87 41,5 47,44 ; 17 1155 21,41 20,47 41,2 54,68 ; 18 1453 25,11 22,59 37,02 48,74 ; 19 1278 21,04 26,27 38,66 53,22 ; 20 1153 17,99 28,22 44,18 53,37 ; 21 1225 18,73 29,39 34,77 51,06 ; 22 1237 18,49 26,58 37,55 50,66 ; 23 1327 22,08 24,88 37,07 50,72 ; 24 1229 14,28 26,27 35,8 48,24 ; 25 1205 17,74 23,61 37,36 49,92 ; 26 1221 20,54 26,58 35,4 53,58 ; 27 1138 18,25 13,77 51,32 51,38 ; 28 1295 19,09 25,62 39,54 50,13 ; 29 1391 21,25 20,63 40,72 48,67 ; 30 1372 21,62 22,71 36,22 48,19]

*Determinar cuál es el mejor modelo candidato.*

| Obs. | Cont. energético (Y) | % de plástico (X1) | % de papel (X2) | % de basura (X3) | % de humedad (X4) |
|---|---|---|---|---|---|
| 1 | 947 | 18,69 | 15,65 | 45,01 | 58,21 |
| 2 | 1407 | 19,43 | 23,51 | 39,69 | 46,31 |
| 3 | 1452 | 19,24 | 24,23 | 43,16 | 46,63 |
| 4 | 1553 | 22,64 | 22,2 | 35,76 | 45,85 |
| 5 | 989 | 16,54 | 23,56 | 41,2 | 55,14 |
| 6 | 1162 | 21,44 | 23,65 | 35,56 | 54,24 |
| 7 | 1466 | 19,53 | 24,45 | 40,18 | 47,2 |
| 8 | 1656 | 23,97 | 19,39 | 44,11 | 43,82 |
| 9 | 1254 | 21,45 | 23,84 | 35,41 | 51,01 |
| 10 | 1336 | 20,34 | 26,5 | 34,21 | 49,06 |
| 11 | 1097 | 17,03 | 23,46 | 32,45 | 53,23 |
| 12 | 1266 | 21,03 | 26,99 | 38,19 | 51,78 |
| 13 | 1401 | 20,49 | 19,87 | 41,35 | 46,69 |
| 14 | 1223 | 20,45 | 23,03 | 43,59 | 53,57 |
| 15 | 1216 | 18,81 | 22,62 | 42,2 | 52,98 |
| 16 | 1334 | 18,28 | 21,87 | 41,5 | 47,44 |
| 17 | 1155 | 21,41 | 20,47 | 41,2 | 54,68 |
| 18 | 1453 | 25,11 | 22,59 | 37,02 | 48,74 |
| 19 | 1278 | 21,04 | 26,27 | 38,66 | 53,22 |
| 20 | 1153 | 17,99 | 28,22 | 44,18 | 53,37 |
| 21 | 1225 | 18,73 | 29,39 | 34,77 | 51,06 |
| 22 | 1237 | 18,49 | 26,58 | 37,55 | 50,66 |
| 23 | 1327 | 22,08 | 24,88 | 37,07 | 50,72 |
| 24 | 1229 | 14,28 | 26,27 | 35,8 | 48,24 |
| 25 | 1205 | 17,74 | 23,61 | 37,36 | 49,92 |
| 26 | 1221 | 20,54 | 26,58 | 35,4 | 53,58 |
| 27 | 1138 | 18,25 | 13,77 | 51,32 | 51,38 |
| 28 | 1295 | 19,09 | 25,62 | 39,54 | 50,13 |
| 29 | 1391 | 21,25 | 20,63 | 40,72 | 48,67 |
| 30 | 1372 | 21,62 | 22,71 | 36,22 | 48,19 |

*Tema detectado por la app: Modelo lineal general / regresión múltiple (TEMA VIII).*

#### Resolución (Selección del mejor modelo candidato (DET, Cp, R² ajustado, S², PRESS)) ✅

*Qué pide:* Análisis exploratorio: tabla de todos los modelos candidatos (DET > 0,1, Cp/p < 5, R²aj, S², PRESS).

- **Análisis exploratorio**: 15 modelos candidatos (2^k - 1). Se descartan los que tienen DET ≤ 0,1 o Cp/p ≥ 5; entre los demás, R² ajustado alto, S² y PRESS bajos y el más simple (parsimonia).

| Modelo | p | R² aj | S² | PRESS | DET | Cp | Cp/p | VIF máx | ¿pasa DET y Cp? |
|---|---|---|---|---|---|---|---|---|---|
| x1 | 2 | 0,3243 | 16.070,532 | 533.814,4236 | 1 | 427,984 | 213,992 | 1 | no |
| x2 | 2 | -0,0342 | 24.596,8383 | 837.908,7496 | 1 | 668,848 | 334,424 | 1 | no |
| x3 | 2 | -0,0278 | 24.445,1767 | 804.905,1305 | 1 | 664,563 | 332,282 | 1 | no |
| x4 | 2 | 0,8055 | 4.626,9514 | 149.093,7461 | 1 | 104,709 | 52,354 | 1 | no |
| x1, x2 | 3 | 0,3168 | 16.249,4751 | 572.613,5995 | 0,9776 | 418,645 | 139,548 | 1,023 | no |
| x1, x3 | 3 | 0,3005 | 16.635,3527 | 578.681,1049 | 0,992 | 429,156 | 143,052 | 1,008 | no |
| x1, x4 | 3 | 0,9445 | 1.318,8197 | 42.351,8784 | 0,9331 | 11,925 | 3,975 | 1,072 | sí |
| x2, x3 | 3 | -0,0654 | 25.338,4103 | 898.858,6357 | 0,6026 | 666,233 | 222,078 | 1,659 | no |
| x2, x4 | 3 | 0,7994 | 4.770,0444 | 163.636,0845 | 1 | 105,939 | 35,313 | 1 | no |
| x3, x4 | 3 | 0,7988 | 4.784,7766 | 167.962,0717 | 0,9949 | 106,34 | 35,447 | 1,005 | no |
| x1, x2, x3 | 4 | 0,2952 | 16.763,3848 | 614.057,4962 | 0,5553 | 417,731 | 104,433 | 1,786 | no |
| x1, x2, x4 | 4 | 0,9519 | 1.144,7044 | 38.124,8927 | 0,9103 | 8,027 | 2,007 | 1,098 | sí |
| x1, x3, x4 | 4 | 0,9424 | 1.369,0611 | 49.495,1426 | 0,9233 | 13,913 | 3,478 | 1,078 | sí |
| x2, x3, x4 | 4 | 0,7917 | 4.953,3291 | 176.231,8588 | 0,598 | 107,934 | 26,984 | 1,672 | no |
| x1, x2, x3, x4 | 5 | 0,9583 | 991,169 | 37.618,2682 | 0,5167 | 5 | 1 | 1,787 | sí |

- **Descartados por DET o Cp**: x1; x2; x3; x4; x1, x2; x1, x3; x2, x3; x2, x4; x3, x4; x1, x2, x3; x2, x3, x4.
- **Modelo elegido (análisis confirmatorio)**: ŷ = 2244,9227 + 28,9250·x1 + 7,6436·x2 + 4,2966·x3 - 37,3538·x4  (n = 30, k = 4, p = 5).
- **Ajuste**: S² = SCR/(n-p) = 991,169; S = 31,4828; R² = 0,9641; R² ajustado = 1 - (1-R²)·(n-1)/(n-p) = 0,9583.
- **Análisis global** (H0: β1 = ... = βk = 0): Fc = (R²/k)/((1-R²)/(n-p)) = 167,7137; F(1-α; 4; 25) = 2,7587 ⇒ se rechaza H0: el modelo en forma global es adecuado.
- **Análisis individual** (H0: βi = 0; se rechaza si |tc| > t(1-α; n-p) = 1,7081):

| Variable | bi | Cii | Sbi = S·√Cii | tc = bi/Sbi | ¿aporta? |
|---|---|---|---|---|---|
| x1 | 28,925 | 0,008044 | 2,8237 | 10,2437 | sí |
| x2 | 7,6436 | 0,005402 | 2,3138 | 3,3034 | sí |
| x3 | 4,2966 | 0,003705 | 1,9163 | 2,2422 | sí |
| x4 | -37,3538 | 0,003394 | 1,8342 | -20,365 | sí |


**Conclusión:** El modelo más adecuado es el que contiene a x1, x2, x3, x4: ŷ = 2244,9227 + 28,9250·x1 + 7,6436·x2 + 4,2966·x3 - 37,3538·x4 (R² ajustado = 0,9583); sus variables aportan significativamente a la explicación de Y.

**Respuesta de la guía:** Hay 15 modelos candidatos, para saber cuál es el que mejor se ajusta, hay que hacer el análisis de sensibilidad: se descartan, por CP, los modelos con la variable X1, con la variable X2, con la variable X3, con la variable X4, con las variables X1 X2, con las variables X1 X3, con las variables X2 X3, con las variables X2 X4, con las variables X3 X4, con las variables X1 X2 X3, con las variables X2 X3 X4. Quedan como mejores candidatos los siguientes modelos en orden de importancia: con las variables X1 X2 X3 X4, con las variables X1 X2 X4, con las variables X1 X4, con las variables X1 X3 X4. Los dos modelos mejores son los primeros, el completo y el que no tiene el porcentaje de basura orgánica (X3). Por principio de Parsimonia se podría recomendar el que tiene las variables X1, X2, X4; pero la variable X3 se considera muy importante para el problema. No obstante si aplicamos el modelo logarítmico lineal: ln(y) = ln(β0) + ln(β1)·x1 + ln(β2)·x2 + ln(β3)·x3 + ln(β4)·x4, este ajusta mucho mejor y además todas las variables aportan significativamente un grado de explicación al modelo.

> 📝 *Notas de la transcripción:* El enunciado dice 'tres variables de composición física' pero enumera cuatro (X1..X4). La Resp no trae coeficientes ni valores de Cp. 'valores' = [15] (cantidad de modelos candidatos). Modelo log-lineal propuesto: ln y lineal en x1..x4. Planteo en p. 59, tabla y Resp en p. 60.

---

### VIII-5 · Problema 5 (pág. 60)

**Enunciado.** Se llevó a cabo un experimento para determinar la dureza de pastillas de freno, en función de los porcentajes de dos componentes fundamentales, azufre y neopreno, obteniéndose los siguientes datos: [Tabla: X1 (% de azufre) X2 (% de neopreno) Y (dureza en shore) ; 5 3 64,36 ; 5 4,23 61,92 ; 5 5,57 60,68 ; 5,26 3 63,76 ; 5,26 4,23 63,5 ; 5,26 5,57 62,64 ; 5,51 3 69,04 ; 5,51 4,23 63,88 ; 5,51 5,57 64,75] Investigue la validez del modelo lineal general para la relación entre estas variables.

| X1 (% de azufre) | X2 (% de neopreno) | Y (dureza en shore) |
|---|---|---|
| 5 | 3 | 64,36 |
| 5 | 4,23 | 61,92 |
| 5 | 5,57 | 60,68 |
| 5,26 | 3 | 63,76 |
| 5,26 | 4,23 | 63,5 |
| 5,26 | 5,57 | 62,64 |
| 5,51 | 3 | 69,04 |
| 5,51 | 4,23 | 63,88 |
| 5,51 | 5,57 | 64,75 |

*Tema detectado por la app: Modelo lineal general / regresión múltiple (TEMA VIII).*

#### Resolución (Modelo lineal general: estimación y validación (F global, t parciales, R²)) ✅

*Qué pide:* Modelo lineal general: b = (X'X)⁻¹X'y, F global, t parciales, R² y R² ajustado.

- **Modelo**: ŷ = 32,1281 + 6,9785·x1 - 1,1660·x2  (n = 9, k = 2, p = 3).
- **Ajuste**: S² = SCR/(n-p) = 1,8156; S = 1,3474; R² = 0,7488; R² ajustado = 1 - (1-R²)·(n-1)/(n-p) = 0,6651.
- **Análisis global** (H0: β1 = ... = βk = 0): Fc = (R²/k)/((1-R²)/(n-p)) = 8,9448; F(1-α; 2; 6) = 5,1433 ⇒ se rechaza H0: el modelo en forma global es adecuado.
- **Análisis individual** (H0: βi = 0; se rechaza si |tc| > t(1-α; n-p) = 1,9432):

| Variable | bi | Cii | Sbi = S·√Cii | tc = bi/Sbi | ¿aporta? |
|---|---|---|---|---|---|
| x1 | 6,9785 | 2,562788 | 2,1571 | 3,2351 | sí |
| x2 | -1,166 | 0,100874 | 0,428 | -2,7246 | sí |

- **Coeficientes de determinación parcial** (aporte de cada variable cuando están las demás): R²(x1) = 0,6356; R²(x2) = 0,553.
- **Modelos simples** (para los coeficientes parciales, R²(xi) = (R² - r²sin xi)/(1 - r²sin xi)): ŷ = 27,1532 + 6,9785·x1 (r² = 0,4381); ŷ = 68,8116 - 1,166·x2 (r² = 0,3107).

**Conclusión:** El modelo, en forma global, es adecuado y todas las variables aportan significativamente a la explicación de Y. R² = 0,7488, R² ajustado = 0,6651.

**Respuesta de la guía:** El modelo, en forma global, es adecuado; las variables X1 y X2 aportan significativamente un grado de explicación en el estudio de Y, el modelo es: ŷ = 32,1281 + 6,9785·x1 − 1,1660·x2.

> 📝 *Notas de la transcripción:* Coeficientes verificados con los datos (R² ≈ 0,7488, no figura en la guía). Riesgo no indicado. Consigna y Resp en p. 61.

---

### VIII-6 · Problema 6 (pág. 61)

**Enunciado.** La energía eléctrica (Y) consumida cada mes por una planta química se considera relacionada con la temperatura ambiente promedio (X1), el número de días del mes (X2), la pureza promedio del producto (X3) y las toneladas obtenidas del producto (X4). Se dispone de los datos históricos del año anterior: [Tabla: Y X1 X2 X3 X4 ; 240 25 24 91 100 ; 236 31 21 90 95 ; 290 45 24 88 110 ; 274 60 25 87 88 ; 301 65 25 91 94 ; 316 72 26 94 99 ; 300 80 25 87 97 ; 296 84 25 86 96 ; 267 75 24 88 110 ; 276 60 25 91 105 ; 288 50 25 90 100 ; 261 38 23 89 98]

- **a)** ¿Hay asociación lineal entre las variables?
- **b)** Determinar el mejor modelo de regresión correspondiente a la energía consumida.

| Y | X1 | X2 | X3 | X4 |
|---|---|---|---|---|
| 240 | 25 | 24 | 91 | 100 |
| 236 | 31 | 21 | 90 | 95 |
| 290 | 45 | 24 | 88 | 110 |
| 274 | 60 | 25 | 87 | 88 |
| 301 | 65 | 25 | 91 | 94 |
| 316 | 72 | 26 | 94 | 99 |
| 300 | 80 | 25 | 87 | 97 |
| 296 | 84 | 25 | 86 | 96 |
| 267 | 75 | 24 | 88 | 110 |
| 276 | 60 | 25 | 91 | 105 |
| 288 | 50 | 25 | 90 | 100 |
| 261 | 38 | 23 | 89 | 98 |

*Tema detectado por la app: Modelo lineal general / regresión múltiple (TEMA VIII).*

#### a) Modelo lineal general: estimación y validación (F global, t parciales, R²) ℹ️

*Qué pide:* Modelo lineal general: b = (X'X)⁻¹X'y, F global, t parciales, R² y R² ajustado.

- **Modelo**: ŷ = -102,7132 + 0,6054·x1 + 8,9236·x2 + 1,4375·x3 + 0,0136·x4  (n = 12, k = 4, p = 5).
- **Ajuste**: S² = SCR/(n-p) = 242,7156; S = 15,5793; R² = 0,7447; R² ajustado = 1 - (1-R²)·(n-1)/(n-p) = 0,5989.
- **Análisis global** (H0: β1 = ... = βk = 0): Fc = (R²/k)/((1-R²)/(n-p)) = 5,106; F(1-α; 4; 7) = 4,1203 ⇒ se rechaza H0: el modelo en forma global es adecuado.
- **Análisis individual** (H0: βi = 0; se rechaza si |tc| > t(1-α; n-p) = 1,8946):

| Variable | bi | Cii | Sbi = S·√Cii | tc = bi/Sbi | ¿aporta? |
|---|---|---|---|---|---|
| x1 | 0,6054 | 0,000561 | 0,3689 | 1,641 | no |
| x2 | 8,9236 | 0,115755 | 5,3005 | 1,6835 | no |
| x3 | 1,4375 | 0,023566 | 2,3916 | 0,601 | no |
| x4 | 0,0136 | 0,002219 | 0,7338 | 0,0185 | no |

- **Coeficientes de determinación parcial** (aporte de cada variable cuando están las demás): R²(x1) = 0,2778; R²(x2) = 0,2882; R²(x3) = 0,0491; R²(x4) = 0.
- **Modelos simples** (para los coeficientes parciales, R²(xi) = (R² - r²sin xi)/(1 - r²sin xi)): ŷ = 224,3764 + 0,9525·x1 (r² = 0,5647); ŷ = -90,1607 + 15,1607·x2 (r² = 0,6446); ŷ = 231,4559 + 0,5294·x3 (r² = 0,0024); ŷ = 282,2456 - 0,0352·x4 (r² = 0,0001).

**Conclusión:** El análisis global indica que el modelo sería adecuado, pero ninguna variable aporta explicación en forma individual: hay que hacer el análisis de sensibilidad (selección de modelos). R² = 0,7447, R² ajustado = 0,5989.

**Respuesta de la guía:** El análisis global me indica que el modelo en forma completa sería adecuado, pero ninguna de las variables “x” aporta explicación en el estudio de la variable “Y”, por lo cual el modelo completo no es válido.

#### b) Selección del mejor modelo candidato (DET, Cp, R² ajustado, S², PRESS) ✅

*Qué pide:* Análisis exploratorio: tabla de todos los modelos candidatos (DET > 0,1, Cp/p < 5, R²aj, S², PRESS).

- **Análisis exploratorio**: 15 modelos candidatos (2^k - 1). Se descartan los que tienen DET ≤ 0,1 o Cp/p ≥ 5; entre los demás, R² ajustado alto, S² y PRESS bajos y el más simple (parsimonia).

| Modelo | p | R² aj | S² | PRESS | DET | Cp | Cp/p | VIF máx | ¿pasa DET y Cp? |
|---|---|---|---|---|---|---|---|---|---|
| x1 | 2 | 0,5212 | 289,7331 | 4.087,166 | 1 | 3,937 | 1,969 | 1 | sí |
| x2 | 2 | 0,609 | 236,5768 | 3.472,6487 | 1 | 1,747 | 0,874 | 1 | sí |
| x3 | 2 | -0,0974 | 664,0368 | 11.496,4958 | 1 | 19,359 | 9,679 | 1 | no |
| x4 | 2 | -0,0999 | 665,5687 | 8.578,6478 | 1 | 19,422 | 9,711 | 1 | no |
| x1, x2 | 3 | 0,6717 | 198,6624 | 3.506,1414 | 0,5638 | 1,366 | 0,455 | 1,774 | sí |
| x1, x3 | 3 | 0,5615 | 265,3287 | 3.935,8931 | 0,9173 | 3,839 | 1,28 | 1,09 | sí |
| x1, x4 | 3 | 0,4681 | 321,8721 | 6.182,3438 | 0,9994 | 5,935 | 1,978 | 1,001 | sí |
| x2, x3 | 3 | 0,5677 | 261,5626 | 4.831,1495 | 0,9873 | 3,699 | 1,233 | 1,013 | sí |
| x2, x4 | 3 | 0,5657 | 262,7713 | 4.437,8353 | 0,9994 | 3,744 | 1,248 | 1,001 | sí |
| x3, x4 | 3 | -0,2191 | 737,6918 | 12.329,7589 | 0,9938 | 21,354 | 7,118 | 1,006 | no |
| x1, x2, x3 | 4 | 0,649 | 212,3866 | 3.757,3693 | 0,4256 | 3 | 0,75 | 2,32 | sí |
| x1, x2, x4 | 4 | 0,6309 | 223,3362 | 5.265,9534 | 0,5634 | 3,361 | 0,84 | 1,774 | sí |
| x1, x3, x4 | 4 | 0,5069 | 298,3675 | 6.651,617 | 0,9116 | 5,834 | 1,459 | 1,096 | sí |
| x2, x3, x4 | 4 | 0,514 | 294,0796 | 6.313,5786 | 0,98 | 5,693 | 1,423 | 1,02 | sí |
| x1, x2, x3, x4 | 5 | 0,5989 | 242,7156 | 6.140,4864 | 0,4219 | 5 | 1 | 2,323 | sí |

- **Descartados por DET o Cp**: x3; x4; x3, x4.
- **Modelo elegido (análisis confirmatorio)**: ŷ = -90,1607 + 15,1607·x2  (n = 12, k = 1, p = 2).
- **Ajuste**: S² = SCR/(n-p) = 236,5768; S = 15,3811; R² = 0,6446; R² ajustado = 1 - (1-R²)·(n-1)/(n-p) = 0,609.
- **Análisis global** (H0: β1 = ... = βk = 0): Fc = (R²/k)/((1-R²)/(n-p)) = 18,1357; F(1-α; 1; 10) = 4,9646 ⇒ se rechaza H0: el modelo en forma global es adecuado.
- **Análisis individual** (H0: βi = 0; se rechaza si |tc| > t(1-α; n-p) = 1,8125):

| Variable | bi | Cii | Sbi = S·√Cii | tc = bi/Sbi | ¿aporta? |
|---|---|---|---|---|---|
| x2 | 15,1607 | 0,053571 | 3,56 | 4,2586 | sí |


**Conclusión:** El modelo más adecuado es el que contiene a x2: ŷ = -90,1607 + 15,1607·x2 (R² ajustado = 0,609); sus variables aportan significativamente a la explicación de Y.

**Respuesta de la guía:** Hay 15 modelos candidatos como el modelo completo no es válido, hay que hacer el análisis de sensibilidad: no se descarta ninguno por DET; se descarta por CP el modelo con la variable X4, el modelo con la variable X3 y el modelo con las variables X3 y X4. Después de que quedan 12 modelos se determina que el mejor modelo es el que contiene solamente la variable X2; luego en orden de importancia le sigue el que contiene a las variables X1 y X2 (pero éste presenta, en el ensayo de β1 = 0, el inconveniente de no pasar dicho ensayo; la variable x1 no aporta explicación en el estudio de Y); siendo el modelo más adecuado: ŷ = −90,1607 + 15,1607·x2. A continuación, se presenta la tabla del análisis de sensibilidad (ver tablas_solucion).

> 📝 *Notas de la transcripción:* La tabla de sensibilidad de la Resp lista 12 modelos (faltan f(x3), f(x4) y f(x3;x4), descartados por Cp). Coeficientes de ŷ = −90,1607 + 15,1607·x2 verificados (R²Aj de f(x2) = 0,6090 coincide), pero los S² (≈0,02) y PRESS (≈0,004) de la tabla no corresponden a la escala de Y (S² del modelo f(x2) con Y lineal ≈ 236,6; con ln Y ≈ 0,0031): posible escala transformada, no se puede determinar. 'Hay 15 modelos candidatos como el modelo completo...' tal cual (falta puntuación).

<details><summary>Cómo lo concluye la guía</summary>

> Tabla del análisis de sensibilidad incluida en la Resp (12 modelos; ver 'tablas_solucion').

</details>

---

### VIII-7 · Problema 7 (pág. 61)

**Enunciado.** Se cree que la variable a explicar (cantidad de combustible en porcentaje con respecto a la cantidad del petróleo en crudo), se puede expresar como combinación lineal de cuatro variables: la gravedad del crudo (X1), la presión del vapor del crudo (X2), la temperatura para la cual se ha evaporado un 10% (X3) y la temperatura para la cual se ha evaporado el 100% (X4). A partir de los 20 datos que se muestran en la siguiente tabla, investigue cuál es el mejor modelo que explica la variable cantidad del combustible en porcentaje con respecto a la cantidad del petróleo en crudo. [Tabla: Y X1 X2 X3 X4 ; 6,9 38,4 6,1 220 235 ; 14,4 40,3 4,8 231 307 ; 7,4 40 6,1 217 212 ; 8,5 31,8 0,2 316 365 ; 8 40,8 3,5 210 218 ; 2,8 41,3 1,8 267 235 ; 5 38,1 1,2 274 285 ; 12,2 50,8 8,6 190 205 ; 10 32,2 5,2 236 267 ; 15,2 38,4 6,1 220 300 ; 26,8 40,3 4,8 213 367 ; 14 32,2 2,4 284 351 ; 14,7 31,8 0,2 316 379 ; 6,4 41,3 1,8 267 275 ; 17,6 38,1 1,2 274 365 ; 22,3 50,8 8,6 190 275 ; 24,8 32,2 5,2 236 360 ; 26 38,4 6,1 220 365 ; 34,9 40,3 4,8 231 395 ; 18,2 40 6,1 217 272]

| Y | X1 | X2 | X3 | X4 |
|---|---|---|---|---|
| 6,9 | 38,4 | 6,1 | 220 | 235 |
| 14,4 | 40,3 | 4,8 | 231 | 307 |
| 7,4 | 40 | 6,1 | 217 | 212 |
| 8,5 | 31,8 | 0,2 | 316 | 365 |
| 8 | 40,8 | 3,5 | 210 | 218 |
| 2,8 | 41,3 | 1,8 | 267 | 235 |
| 5 | 38,1 | 1,2 | 274 | 285 |
| 12,2 | 50,8 | 8,6 | 190 | 205 |
| 10 | 32,2 | 5,2 | 236 | 267 |
| 15,2 | 38,4 | 6,1 | 220 | 300 |
| 26,8 | 40,3 | 4,8 | 213 | 367 |
| 14 | 32,2 | 2,4 | 284 | 351 |
| 14,7 | 31,8 | 0,2 | 316 | 379 |
| 6,4 | 41,3 | 1,8 | 267 | 275 |
| 17,6 | 38,1 | 1,2 | 274 | 365 |
| 22,3 | 50,8 | 8,6 | 190 | 275 |
| 24,8 | 32,2 | 5,2 | 236 | 360 |
| 26 | 38,4 | 6,1 | 220 | 365 |
| 34,9 | 40,3 | 4,8 | 231 | 395 |
| 18,2 | 40 | 6,1 | 217 | 272 |

*Tema detectado por la app: Modelo lineal general / regresión múltiple (TEMA VIII).*

#### Resolución (Selección del mejor modelo candidato (DET, Cp, R² ajustado, S², PRESS)) ✅

*Qué pide:* Análisis exploratorio: tabla de todos los modelos candidatos (DET > 0,1, Cp/p < 5, R²aj, S², PRESS).

- **Análisis exploratorio**: 15 modelos candidatos (2^k - 1). Se descartan los que tienen DET ≤ 0,1 o Cp/p ≥ 5; entre los demás, R² ajustado alto, S² y PRESS bajos y el más simple (parsimonia).

| Modelo | p | R² aj | S² | PRESS | DET | Cp | Cp/p | VIF máx | ¿pasa DET y Cp? |
|---|---|---|---|---|---|---|---|---|---|
| x1 | 2 | -0,0512 | 77,099 | 1.640,3554 | 1 | 242,066 | 121,033 | 1 | no |
| x2 | 2 | 0,0753 | 67,8262 | 1.445,5827 | 1 | 211,028 | 105,514 | 1 | no |
| x3 | 2 | 0,0436 | 70,1459 | 1.483,6297 | 1 | 218,792 | 109,396 | 1 | no |
| x4 | 2 | 0,4106 | 43,2333 | 979,3797 | 1 | 128,711 | 64,355 | 1 | no |
| x1, x2 | 3 | 0,058 | 69,0937 | 1.519,6034 | 0,6424 | 204,422 | 68,141 | 1,557 | no |
| x1, x3 | 3 | 0,0307 | 71,0948 | 1.567,5114 | 0,5366 | 210,748 | 70,249 | 1,864 | no |
| x1, x4 | 3 | 0,6291 | 27,2058 | 623,4075 | 0,7333 | 72,004 | 24,001 | 1,364 | no |
| x2, x3 | 3 | 0,0237 | 71,6099 | 1.583,0007 | 0,1445 | 212,376 | 70,792 | 6,919 | no |
| x2, x4 | 3 | 0,8583 | 10,3911 | 252,3136 | 0,853 | 18,849 | 6,283 | 1,172 | no |
| x3, x4 | 3 | 0,9245 | 5,5364 | 137,4618 | 0,7795 | 3,502 | 1,167 | 1,283 | sí |
| x1, x2, x3 | 4 | 0,0001 | 73,3396 | 1.715,8298 | 0,0766 | 206,207 | 51,552 | 8,391 | no |
| x1, x2, x4 | 4 | 0,8824 | 8,6244 | 216,5543 | 0,4655 | 13,66 | 3,415 | 1,832 | sí |
| x1, x3, x4 | 4 | 0,9285 | 5,2425 | 127,4352 | 0,3796 | 3,598 | 0,899 | 2,054 | sí |
| x2, x3, x4 | 4 | 0,9219 | 5,7305 | 141,6322 | 0,1101 | 5,05 | 1,262 | 7,75 | sí |
| x1, x2, x3, x4 | 5 | 0,9267 | 5,3776 | 131,7502 | 0,0533 | 5 | 1 | 8,73 | no |

- **Descartados por DET o Cp**: x1; x2; x3; x4; x1, x2; x1, x3; x1, x4; x2, x3; x2, x4; x1, x2, x3; x1, x2, x3, x4.
- **Modelo elegido (análisis confirmatorio)**: ŷ = 15,9557 - 0,1827·x3 + 0,1424·x4  (n = 20, k = 2, p = 3).
- **Ajuste**: S² = SCR/(n-p) = 5,5364; S = 2,353; R² = 0,9325; R² ajustado = 1 - (1-R²)·(n-1)/(n-p) = 0,9245.
- **Análisis global** (H0: β1 = ... = βk = 0): Fc = (R²/k)/((1-R²)/(n-p)) = 117,3541; F(1-α; 2; 17) = 3,5915 ⇒ se rechaza H0: el modelo en forma global es adecuado.
- **Análisis individual** (H0: βi = 0; se rechaza si |tc| > t(1-α; n-p) = 1,7396):

| Variable | bi | Cii | Sbi = S·√Cii | tc = bi/Sbi | ¿aporta? |
|---|---|---|---|---|---|
| x3 | -0,1827 | 0,000049 | 0,0164 | -11,1157 | sí |
| x4 | 0,1424 | 0,000017 | 0,0098 | 14,5278 | sí |


**Conclusión:** El modelo más adecuado es el que contiene a x3, x4: ŷ = 15,9557 - 0,1827·x3 + 0,1424·x4 (R² ajustado = 0,9245); sus variables aportan significativamente a la explicación de Y.

**Respuesta de la guía:** El modelo más adecuado es el que contiene a las variables X3 y X4, las cuales aportan significativamente un grado de explicación en el estudio de Y, el modelo es: ŷ = 15,9557 − 0,1827·x3 + 0,1424·x4.

> 📝 *Notas de la transcripción:* La tabla está partida entre p. 61 (6 filas) y p. 62 (14 filas); total 20 filas. Coeficientes del modelo con X3 y X4 verificados con los datos.

---

## Discrepancias con la guía

Incisos donde lo calculado no coincide con la respuesta de la guía. Puede ser un error de la guía, un criterio distinto, o un error de interpretación de la app: hay que revisarlos uno por uno.

| Ejercicio | Inciso | Respuesta de la guía | Valores que no aparecen | La app da | Notas |
|---|---|---|---|---|---|
| III-3 | b | Entre 0 (0%) y 0,2589 (25,89%). | 0,2589 | IC p: [0 ; 0,2057] | Cambio a propósito (fuente: el profesor en clase, 17/09/2026): con r = 0 hay un solo límite y «no se divide el alfa por 2… todo el riesgo lo juntás en el límite superior»; sobre la guía dijo «lo hicieron con alfa sobre 2 |
| III-11 | c | n = 755 piezas, o n = 715 piezas (por aproximación normal), o n= 855 piezas (por aproximación de Poisson). En este caso la aproximación de Poisson no es correcta, la cual sería adecuada si n = 50. | 855 | n = 755; rc = 106 / normal: n = 715; rc = 101 | Cambio a propósito (fuente: el profesor en clase, 17/09/2026): el n = 855 por Poisson es incorrecto porque el criterio de aproximación se aplicó con el n inicial (50); con el n resultante (855·0,12 = 102,6 > 10 y 855·0,8 |
| III-15 | d | R = 1,44546 → R = 1,01182; n ≈ 22.255 árboles (aproximación normal); n ≈ 26.909 árboles (aproximación de Poisson). | 26.909 | n = 22255 | Poisson: la guía da 26.909 tanteando valores de n; la relación entre límites cambia apenas 4·10⁻⁷ por unidad de n, así que el n depende de cómo se tantea. La app informa la aproximación normal (22.255), que sí coincide. |
| III-16 | a | (Criterio pesimista) H0) p ≤ p0 = 0,12; CR: Si r ≥ rc = 233 éxitos se rechaza la H0 o r ≥ rc = 229 éxitos (por aproximación normal); RD: Si de una muestra de 1.675 encuestados por lo menos 233 se encuentran interesados,  | 228 | n = 1675; rc = 233 / normal: n = 1637; rc = 229 | Inconsistencia de la guía: la CR por aproximación normal dice r_c = 229 (conservador) y la RD dice 228 (con 228, α real = 0,0101 > 0,01). La app informa 229. |

## Coinciden solo aproximadamente

Valores que coinciden con tolerancia pero no en todos los dígitos que informa la guía. Casi siempre es un redondeo intermedio de la cátedra (valores de tabla) o una errata; la explicación está en `datos/diferencias_explicadas.json` y las reglas en `CONVENCIONES_CATEDRA.md`.

| Ejercicio | Inciso | Valores de la guía | Explicación |
|---|---|---|---|
| I-4 | a | 20.203,88 | Errata de la guía: el límite exacto 20.203,8696 se informa 20.203,88 (redondeado da 20.203,87). |
| III-16 | b | 0,5443 | La guía calcula la potencia con el r_c = 228 de su RD (0,5443); con el r_c conservador 229 la aproximación normal da 0,5159 y el plan exacto 0,5527. |
| III-18 | b | 0,2569 | La guía usa su plan 1.585 / 73, que cumple α y β pero no es el de n mínimo (1.561 / 72) ni el más próximo a las premisas (1.562 / 72): ninguna regla lo reproduce. |
| V-3 | b | 194,4482 | Errata de la guía: imprime e = 194,4494 en a) y 194,4482 en b); los límites (67,55 y 456,45) coinciden. |
| VI-20 | b | 39,1307 | La cátedra usa probabilidades de la tabla normal (z con 2 decimales, P con 4) y Fe con 2 decimales; con precisión completa χ² difiere menos del 1 % y la decisión no cambia. Redondear solo P y Fe no alcanza para reproducirlo. |
| VI-20 | c | 2,1333 | Ídem b): probabilidades de tabla en la guía; con precisión completa difiere menos del 1 % y la decisión no cambia. |
| VII-5 | b | 199.813,14 | La guía usa t de tabla con 4 decimales (1,3968) y da 199.813,14; con el t exacto es 199.812,46. Usar t de tabla en toda la regresión empeora otros 16 límites, por eso la app usa el valor exacto. |
| VII-12 | g | 9,0943 | La guía informa la semiamplitud ±9,0943 calculada con t de tabla (2,2281); los límites del intervalo coinciden. |
| VIII-1 | única | 0,9438, 92,0874 | F: la guía usa R² redondeado a 0,9485 y da 92,0874; exacto es 92,0256 (la decisión no cambia). El texto dice R²aj = 0,9438 (dígitos transpuestos): su propia tabla y el cálculo dan 0,9382. |
| VIII-2 | b | 0,8957 | La guía da R²aj = 0,8957, que sale con (n − 1)/(n − k); con la fórmula de la teoría, (n − 1)/(n − p), es 0,8808. |
