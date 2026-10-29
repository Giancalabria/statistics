# Estilo de resolución de la cátedra (Dopazo – García)

Este archivo es lo que lee la IA para **redactar la resolución como la quiere el profesor** (botón
*📝 Redactar como en el examen* en *Interpretar un enunciado*). Se puede editar libremente: agregar ejemplos,
frases que el profesor exige o correcciones, y la próxima redacción ya las usa. Los **números** nunca salen de
acá: los pone siempre el solver.

Fuente: lo que dijo el profesor en clase (06/08 a 22/10/2026), resumido en `estadistica/REGLAS_PROFESOR.md` y en
los informes de clase. **El profesor manda sobre la guía y sobre el apunte**; cuando la guía difiere, se sigue al
profesor y se anota la diferencia. Los ejemplos de los temas III a VI son los que él resolvió en clase; los números
se verificaron con scipy. La sección de regresión (VII y VIII) es **provisoria**: al 22/10 no se dio en clase.

**Cómo se arma el prompt**: este encabezado no se le pasa a la IA. Cada sección `##` o `###` con una línea
`<!-- temas: I II ... -->` justo debajo del título solo se incluye en los ejercicios de esos temas (las que no la
tienen van siempre). Así un ejercicio de χ² no recibe los ejemplos de intervalos ni el criterio pesimista /
optimista, que no le corresponden. Cada sección de un tema tiene que ser autocontenida y corta: el modelo local
tiene poco contexto.

De los ejemplos (`### Ejemplo …`) se manda **uno solo**: el que más comparte con el ejercicio según su línea
`<!-- tipos: ... -->` (tipos de inciso como `ic`, `ensayo`, `diseno`, `beta`, `curva`, o el tema `chi_ajuste` /
`chi_contingencia`). Con más ejemplos el modelo se confunde y copia números de otros ejercicios.

## 1. Criterios que no se negocian

- **Definir la variable antes de escribir un número**, en palabras, con su **unidad** y su entorno.
  Ej.: «X: consumo de combustible de un vehículo en una corrida, expresado en litros (L).»
- **Probabilidades siempre entre 0 y 1, nunca en %**: α = 0,05, β = 0,4769, 1 − β = 0,5231, P(…) = 0,90. Se admite
  «95 % de confianza», y una proporción en % solo si el enunciado pide un «porcentaje».
- **Mínimo 4 decimales** en todo el desarrollo y en los fractiles (Z(0,95) = 1,6449). Los periódicos como fracción
  (1/37, no 0,027). El resultado final se expresa según la variable, con unidades.
- **Notación**: P = probabilidad puntual, F = acumulada izquierda, G = acumulada derecha, Φ = F de la normal
  estándar. No escribir P(X ≤ x) en lugar de F. «ν = número de grados de libertad».
- **Redondeos lógicos**: n y ν al entero superior (salvo ν de Welch, que se trunca); en los intervalos el límite
  inferior hacia abajo y el superior hacia arriba; en discretas, el valor crítico que deja α real ≤ α.
- **Nunca escribir «Acepto H0»**: se escribe «**Se rechaza H0**: puedo asegurar que…» o «**No se rechaza H0**: no hay
  evidencia suficiente para asegurar que…». Nunca se prueba la igualdad ni la independencia, ni se dice que el
  producto «es malo».
- **Condición de rechazo (CR)**: la desigualdad matemática. **Regla de decisión (RD)**: el curso de acción en
  lenguaje de planta, para el operario, sin teoría. Ej.: «Si en 1637 encuestados hay 229 o más interesados, se
  inicia una nueva campaña; si no, no.»
- **α se fija antes de ver la muestra y no se toca.** Nunca decidir con el p-value (α a posteriori).

### 1.1 Parámetros, tamaños e intervalos
<!-- temas: I II III IV V VII VIII -->

- **Parámetros** con letras griegas (μ, σ², σ, ψ, φ, Δ; p es la excepción) y **estimadores** con latinas (x̄, S²,
  S, p̂, J², J, D).
- La **igualdad (=, ≤, ≥) va siempre en H0**.
- **Tamaños de muestra** al **entero superior**. Si ya había una muestra, informar cuántas unidades **más** hay que
  tomar (Δn = n_total − n_preliminar).
- **Intervalos**: cerrar con la expresión formal P(A ≤ θ ≤ B) = 1 − α y una conclusión en palabras.
- **Un solo límite** («mínimo», «máximo», o p con r = 0) ⇒ **α entero, sin dividir por 2**. α/2 solo con dos
  límites.

### 1.2 Planteo de H0 y H1
<!-- temas: I II III IV V -->

- **Regla madre**: H0 se plantea de modo que el **error de tipo I sea el más grave**.
- **Orden**: (1) si el enunciado dice qué se quiere probar («¿se puede asegurar que…?», «la denuncia dice que…»),
  eso va en **H1**; (2) si no, el criterio; (3) si no alcanza, comparar la gravedad de los errores.
- **Pesimista** (riesgo económico: inversión, máquina o proveedor nuevo, producto nuevo, modificación, campaña
  publicitaria): H0 = «no funciona / no cumple». **Pesimista aunque la campaña sea barata**, si lo que se quiere es
  probar que fue efectiva.
- **Optimista** (control de proceso, recepción de un **proveedor habitual**, controles de rutina): H0 = «cumple /
  está bajo control»; rechazar H0 = detener el proceso o rechazar el lote.
- No asociar el criterio con ≤ o ≥: depende de qué es «cumplir» en el problema.
- Primero **en palabras**, después en símbolos. Escribir H1 (el complemento).
- **No hay bilaterales en σ², σ, p ni en comparaciones de dos poblaciones.** En μ, bilateral solo si el enunciado lo
  impone («diferente de», valor exacto).
- **α no dado**: se elige y se justifica (chico ≤ 0,01, estándar 0,05, grande ≥ 0,10). Ej.: 0,05 «no porque sea
  estándar», sino porque el perito tiene que ser imparcial.

## 2. Pasos de un ensayo de hipótesis (en este orden)
<!-- temas: I II III IV V -->

1. **Variable** en palabras, con unidad, y el parámetro.
2. **H0 y H1** en palabras y en símbolos, con el criterio justificado.
3. **α** (y β en el valor alternativo, si corresponde). Escribir **las 4 probabilidades en términos del problema**:
   α = P(lanzar el aditivo | no reduce el consumo), 1 − α, β = P(no lanzar | lo reduce a μ₁), 1 − β.
4. **n**, si no está dado.
5. **Valor crítico, CR y RD**, antes de ver la muestra. Los críticos se calculan con la curva de H0.
6. **Estimador** de la muestra (x̄, S, r, J, D, d̄).
7. **Comparar el estimador contra el valor crítico** y concluir en el contexto del problema.

- Se compara **en unidades de la variable**: x̄ contra x̄c, S² contra S²c, r contra rc, J contra Jc, D contra Dc.
  **Nunca** el estimador contra μ₀ o Δ₀, ni estadísticos observados (Z, t, F o chi-cuadrado «observado») contra la tabla.
- **Fundamento de la distribución** por su estructura, no por «conozco σ»: x̄ es normal y al estandarizar se divide
  por un parámetro (σ), así que sigue siendo normal ⇒ Z. Si se divide por S, que es una variable aleatoria (raíz de
  una chi-cuadrado), queda una t de Student con ν = n − 1, **sea cual sea n**. Nada de «n ≥ 30 ⇒ normal».
- **Diseño** (no hay muestra todavía): pasos 1 a 5, hasta la CR y la RD.

## 3. Modelos y distribuciones
<!-- temas: I II III IV V -->

| Tema | Parámetro | Situación | Distribución | Notas |
|---|---|---|---|---|
| I | μ | se divide por σ (parámetro) | Normal estándar Z | n = (Z·σ/e)²; en ensayos, n por las dos condiciones (α y β) |
| I | μ | se divide por S (variable aleatoria) | t de Student, ν = n − 1 | n por método iterativo; en ensayos **no se calculan β ni n** (t no central) |
| I | total τ | población finita | — | τ = N·μ; factor √((N − n)/N) siempre que se conoce N (apunte y profesor; con N − 1 «el uno mucho no hace») |
| II | σ², σ | una población | Chi-cuadrado, ν = n − 1 | siempre con varianzas; n por la ecuación de García |
| III | p | Bernoulli / binomial | **exacta** (binomial o F) | aproximaciones normal o Poisson **solo para calcular n** |
| IV | ψ² = σ₁²/σ₂², φ = σ₁/σ₂ | dos poblaciones | F(ν₁ = n₁ − 1; ν₂ = n₂ − 1) | n con n₁ = n₂, iterando ν (n = ν + 1) |
| V | Δ = μ₁ − μ₂ | dos poblaciones | t (amalgamado, Welch o apareadas) | sin β ni n |

### 3.1 Ecuación de García (Tema II)
<!-- temas: II -->

ν = (2/9)·(a + √(a² + 1))², ν al entero superior y n = ν + 1.
- Estimación (relación entre límites R = R'²): a = Z(1 − α/2)·(∛R + 1)/[2(∛R − 1)].
- Ensayo, caso 1 (H0: σ² ≤ σ₀², R = σ₁²/σ₀²): a = [Z(1 − α) + Z(1 − β)·∛R]/[2(∛R − 1)].
- Ensayo, caso 2 (H0: σ² ≥ σ₀², R = σ₀²/σ₁²): a = [Z(1 − β) + Z(1 − α)·∛R]/[2(∛R − 1)].
- ∛R multiplica a **un solo** Z, y R es **de varianzas** (con desvíos, R = R'²).

## 4. Formato por tipo de inciso
<!-- temas: I II III IV V VII VIII -->

**Intervalo de confianza**
1. Definición de la variable (y el modelo, p. ej. X ~ Normal(μ; σ² = 15²)).
2. Datos: parámetros conocidos y estimadores de la muestra.
3. Confianza y fractil: 1 − α = 0,90 ⇒ α/2 = 0,05 ⇒ Z(0,95) = 1,6449 (con un solo límite, α entero).
4. Error muestral y límites A y B, con unidades.
5. Expresión formal P(A ≤ θ ≤ B) = 1 − α.
6. Conclusión: «Se estima con un 90 % de confianza que [el parámetro en palabras] se encuentra entre A y B.»

**Tamaño de muestra**: fórmula con los valores, resultado sin redondear ⇒ entero superior, y Δn si ya había
muestra. Si es iterativo, arrancar con un n bastante mayor y **mostrar todas las iteraciones**. Para un nuevo n en
un ensayo se usa la fórmula de las dos condiciones, **nunca** el crítico del n anterior.

**Ensayo**: los pasos de la sección 2.

**Probabilidad de error (β) o potencia (1 − β)**: decir qué evento es en palabras («no implementar la modificación
cuando la media real es 4,98»), la región de no rechazo, la cuenta con el crítico **con todos sus decimales** y la
probabilidad (entre 0 y 1), con una frase que la interprete. β no es 1 − α.

## 5. Ejemplos resueltos (temas I a III)

### Ejemplo 1 · Tema I · Intervalo y tamaño de muestra (Guía, Tema I, problema 1)
<!-- temas: I -->
<!-- tipos: ic n -->

> «Una máquina llenadora de latas de café dosifica cantidades variables con distribución Normal de desvío
> estándar 15 gramos. … muestras de 10 envases … una media de 246 gramos. Estimar la dosificación media con un
> 90 % de confianza y calcular cuántos envases más habría que pesar para reducir el error de muestreo a 5 gramos.»

1. **Variable**: X: cantidad de café dosificada en una lata, en gramos (g). X ~ Normal(μ; σ² = 15²).
2. **Datos**: σ = 15 g (de la variable, es un parámetro); n = 10 latas; x̄ = 246 g. Se divide por un parámetro ⇒ Z.
3. **Intervalo del 90 %**: 1 − α = 0,90 ⇒ α/2 = 0,05 ⇒ Z(0,95) = 1,6449.
   - e = 1,6449 · 15/√10 = 7,8024 g. A = 238,1976 ⇒ 238,19 g; B = 253,8024 ⇒ 253,81 g.
   - **Expresión formal**: P(238,19 g ≤ μ ≤ 253,81 g) = 0,90.
   - «Se estima con un 90 % de confianza que la dosificación media de todas las latas está entre 238,19 g y
     253,81 g.»
4. **n para e = 5 g**: n = [1,6449 · 15/5]² = 24,3511 ⇒ **25 latas**; Δn = **15 latas más**.

### Ejemplo 2 · Tema I · Diseño del ensayo con α y β (examen: modificación del sistema productivo)
<!-- temas: I -->
<!-- tipos: diseno beta -->

> «… el nuevo sistema aumentaría la productividad a un valor promedio de 5,8 piezas por minuto. El sistema actual
> tiene una productividad promedio de 4,2 piezas por minuto con un desvío estándar de 2,53 … probabilidad de 0,95
> de modificar el sistema cuando con la modificación se obtiene 5,8 …; el gerente desea la certeza del 99 % de no
> realizar la modificación cuando no se consigue el efecto deseado. Se asume que el desvío no se modificará.»

1. **Variable**: X: productividad del proceso, en piezas por minuto. σ = 2,53 piezas/min (no cambia). Se divide por
   un parámetro ⇒ Z.
2. **Hipótesis** (pesimista: modificar el proceso es una inversión; solo se hace con evidencia):
   H0: μ ≤ 4,2 (la modificación no aumenta la productividad) · H1: μ > 4,2.
3. **Riesgos**: 1 − α = 0,99 ⇒ α = 0,01 = P(modificar | no aumenta); 1 − α = P(no modificar | no aumenta);
   1 − β = 0,95 = P(modificar | μ = 5,8); β = 0,05 = P(no modificar | μ = 5,8).
4. **n** = [(2,3263 + 1,6449)·2,53/(5,8 − 4,2)]² = 39,4316 ⇒ **n = 40**.
5. x̄c = 4,2 + 2,3263 · 2,53/√40 = **5,1306 piezas/min**. **CR**: x̄ > 5,1306.
   **RD**: «Se mide la productividad en 40 minutos con el sistema modificado. Si el promedio supera 5,1306
   piezas/min, se implementa la modificación; si no, se mantiene el sistema actual.»

### Ejemplo 3 · Tema III · Intervalo exacto de una proporción (Guía, Tema III, problema 3)
<!-- temas: III -->
<!-- tipos: ic -->

> «Calcular los límites de confianza del 90 % de la fracción defectuosa, si de un proceso productivo se tomó una
> muestra de 10 unidades en la cual se encontró: a) 1 defectuosa; b) 0 defectuosas.»

1. **Variable**: atributo de Bernoulli de cada pieza (defectuosa o no). Parámetro p: proporción de defectuosas del
   proceso. La estimación de p es **siempre exacta** (nunca con la aproximación normal).
2. **a)** n = 10, r = 1, 1 − α = 0,90 ⇒ α/2 = 0,05.
   - A: ν₁ = 2n − 2r + 2 = 20, ν₂ = 2r = 2; F(0,95; 20; 2) = 19,4458; A = 1/[1 + (10/1)·19,4458] = **0,0051**.
   - B: ν₁ = 2r + 2 = 4, ν₂ = 2n − 2r = 18; F(0,95; 4; 18) = 2,9277; B = 1/[1 + 9/(2·2,9277)] = **0,3942**.
   - **Expresión formal**: P(0,0051 ≤ p ≤ 0,3942) = 0,90.
3. **b)** r = 0 ⇒ A = 0 y hay **un solo límite**: α entero. F(0,90; 2; 20) = 2,5893;
   B = 1/[1 + 10/2,5893] = **0,2057**. P(0 ≤ p ≤ 0,2057) = 0,90. (La guía da 0,2589 con α/2: el profesor dijo que
   está mal.)

### Ejemplo 4 · Tema II · Intervalo para el desvío (Guía, Tema II, problema 6)
<!-- temas: II -->
<!-- tipos: ic -->

> «… muestras de 20 ovillos. Una de dichas muestras arrojó un desvío de 15 gramos. Calcular los límites de
> confianza del 95 % para el desvío y determinar qué tamaño de muestra habría que tomar para que el límite superior
> sea un 50 % mayor que el inferior.»

1. **Variable**: X: peso de un ovillo, en gramos (g). Datos: n = 20 ⇒ ν = 19; S = 15 g.
2. **Intervalo del 95 %**: χ²(0,975; 19) = 32,8523 y χ²(0,025; 19) = 8,9065;
   A' = √(19·15²/32,8523) = **11,40 g**; B' = √(19·15²/8,9065) = **21,91 g**. P(11,40 g ≤ σ ≤ 21,91 g) = 0,95.
3. **Tamaño de muestra** (García, estimación): R' = 1,5 ⇒ R = R'² = 2,25 (no R'); a y ν con los pasos del solver ⇒
   **n = 49 ovillos** (ν = 48).

## 6. Tema III · Ensayos sobre p
<!-- temas: III -->

- Siempre **unilateral** (no existe el bilateral en p). Variable: r = cantidad de éxitos en n (binomial).
  - Caso 1, H0: p ≤ p₀: rc tal que G_b(rc | n; p₀) ≤ α; CR: r ≥ rc; β = F_b(rc − 1 | n; p₁).
  - Caso 2, H0: p ≥ p₀: rc tal que F_b(rc | n; p₀) ≤ α; CR: r ≤ rc; β = G_b(rc + 1 | n; p₁).
- El aplicativo da dos valores: se elige el rc que deja **α real ≤ α** y se muestran los dos. Se decide con r contra
  rc (a priori), nunca con el α* a posteriori.
- **n del plan**: exacto (el menor n con G ≤ α y F ≤ β). Aproximación normal:
  n = [(Z(1 − α)·√(p₀q₀) + Z(1 − β)·√(p₁q₁))/(p₁ − p₀)]². Aproximación Poisson: R = p₁/p₀ con la chi-cuadrado (Wilson-Hilferty).
- **Justificar la aproximación con el n resultante**: normal si n·p > 10 y n·(1 − p) > 10; Poisson si p ≤ 0,005;
  si se cumplen los dos o ninguno, **criterio de Mermoz**: n₀ = 0,23·(1 − p)²/p³ (p ≤ 0,5); n > n₀ ⇒ normal, si no,
  Poisson. Nada de «n ≥ 30» ni «np ≥ 5».
- «Aumento de 3 **puntos**» es 0,12 → 0,15 (no 0,12·1,03). Recepción: AQL = p₀ (α = riesgo del proveedor), RQL o
  LTPD = p₁ (β = riesgo del comprador).

### Ejemplo III-11 · Control de proceso (resuelto en clase)
<!-- temas: III -->
<!-- tipos: diseno beta -->

> «… trabaja en condiciones normales con un 12 % de unidades defectuosas … muestras de 50 unidades … Si el proceso
> está bajo control, la probabilidad de detenerlo y revisarlo debe valer 0,05. a) ¿Cuántas defectuosas … para
> detener el proceso? b) ¿Probabilidad de no detenerlo cuando el porcentaje es del 14 %? c) ¿Cuántas unidades para
> disminuir a 0,50 la probabilidad anterior?»

1. **Variable**: r: cantidad de piezas defectuosas en una muestra de 50 (cada pieza, defectuosa o no). p:
   proporción de defectuosas del proceso.
2. **H0: p ≤ 0,12** (el proceso está bajo control) · H1: p > 0,12. Criterio optimista: es un control de proceso, y
   lo grave es detenerlo cuando cumple.
3. α = 0,05 = P(detener y revisar | p ≤ 0,12).
4. **a)** G_b(10 | 50; 0,12) = 0,0708 > 0,05 y G_b(11 | 50; 0,12) = 0,0325 ≤ 0,05 ⇒ **rc = 11**. CR: r ≥ 11.
   RD: «Se revisan 50 piezas; si hay 11 o más defectuosas, se detiene el proceso y se revisa; si no, sigue.»
5. **b)** β = P(no detener | p = 0,14) = F_b(10 | 50; 0,14) = **0,9176**.
6. **c)** β = 0,50 en p₁ = 0,14 con α = 0,05 fijo: exacto **n = 755** (rc = 106). Normal: Z(0,50) = 0 ⇒
   n = [1,6449·√(0,12·0,88)/0,02]² = 714,2635 ⇒ **715**; verificación con el n resultante: 715·0,12 = 85,8 > 10 y
   715·0,88 = 629,2 > 10, y p₀ = 0,12 > 0,005 ⇒ corresponde la normal. (La guía también da 855 por Poisson: es
   incorrecto, el criterio se aplicó con n = 50.)

### Ejemplo III-16 · Campaña publicitaria (resuelto en clase)
<!-- temas: III -->
<!-- tipos: diseno beta curva -->

> «… jabón en polvo cuya penetración en el mercado era del 12 % … comprobar si la campaña ha sido efectiva … si no
> se ha conseguido el resultado deseado, probabilidad de 0,01 de tomar una decisión errónea … un aumento de 3
> puntos … probabilidad de decisión equivocada 0,10. a) H0, CR y RD. b) Probabilidad de efectuar otra campaña
> cuando se obtuvo un aumento de 2 puntos.»

1. **Variable**: r: cantidad de encuestados interesados en el jabón en una muestra de n. p: penetración en el
   mercado.
2. **H0: p ≤ 0,12** (la campaña no fue efectiva) · H1: p > 0,12. Pesimista: se quiere probar que fue efectiva, y
   hacer otra campaña sin efecto es lo grave (aunque la campaña fuera barata).
3. α = 0,01 = P(hacer otra campaña | p ≤ 0,12); β = 0,10 = P(no hacerla | p = 0,15) (3 puntos: 0,12 → 0,15).
4. **n**: exacto **n = 1675, rc = 233**. Normal: n = [(2,3263·√(0,12·0,88) + 1,2816·√(0,15·0,85))/0,03]² =
   1636,4156 ⇒ **1637**; 1637·0,12 = 196,44 > 10 y 1637·0,88 = 1440,56 > 10 ⇒ normal válida.
5. Con n = 1637: G_b(228 | 1637; 0,12) = 0,0101 > 0,01 y G_b(229) = 0,0083 ⇒ **rc = 229**. CR: r ≥ 229.
   RD: «Si en 1637 encuestados hay 229 o más interesados, se inicia una nueva campaña; si no, no.» (La guía pone
   228 en la RD: es una errata.)
6. **b)** p = 0,14: 1 − β = P(otra campaña | p = 0,14) = G_b(229 | 1637; 0,14) = **0,5159**. Con el plan exacto
   (1675; 233): 1 − β = 0,5527.

### Ejemplo III-19 · Ruleta (resuelto en clase)
<!-- temas: III -->
<!-- tipos: ensayo beta -->

> «Una persona denunció que en un casino había una ruleta adulterada pues el cero se producía con frecuencia
> excesiva … 1.000 bolas en las cuales el cero se presentó 42 veces. a) ¿La denuncia tiene fundamento estadístico?
> b) Si el cero tuviera probabilidad 0,05, ¿probabilidad de detectar la anomalía? (ruleta equilibrada: 1/37).»

1. **Variable**: r: cantidad de ceros en 1000 bolas. p: probabilidad de cero de la ruleta.
2. **H0: p ≤ 1/37** (la ruleta no favorece al cero) · H1: p > 1/37. No es bilateral: la denuncia dice que el cero
   sale **con mayor frecuencia**, y eso va en H1.
3. α no dado: **0,05**, no por ser estándar, sino porque el perito tiene que ser imparcial (un α chico favorece al
   casino y uno grande al denunciante).
4. G_b(36 | 1000; 1/37) = 0,0540 > 0,05 y G_b(37) = 0,0372 ⇒ **rc = 37**. CR: r ≥ 37.
5. **Estimador**: r = 42 ≥ 37 ⇒ **se rechaza H0**: «puedo asegurar que el cero sale con una frecuencia mayor que
   1/37: la denuncia tiene fundamento estadístico».
6. **b)** 1 − β = P(detectar | p = 0,05) = G_b(37 | 1000; 0,05) = **0,9788** (la guía da 0,9789).

## 7. Tema IV · Comparación de varianzas o desvíos
<!-- temas: IV -->

- ψ² = σ₁²/σ₂² con estimador J² = S₁²/S₂² y F(ν₁ = n₁ − 1; ν₂ = n₂ − 1): **pensar qué va en el numerador**. Usar
  letras (A/B, CR/SR) en lugar de 1/2. Para desvíos, φ = σ₁/σ₂ y J = S₁/S₂.
- IC: A = J²/F(1 − α/2; ν₁; ν₂), B = J²/F(α/2; ν₁; ν₂); desvíos: A' = √A, B' = √B. **Interpretar en %** de
  aumento o reducción. Si no dicen la relación, se elige una, se dice cuál y se resuelve solo esa.
- n con n₁ = n₂: se itera ν hasta que la relación entre límites R = F(1 − α/2; ν; ν)/F(α/2; ν; ν) llegue al
  objetivo; n = ν + 1. Para desvíos, **R = R'²**.
- **Ensayos** (sin bilaterales; la muestra orienta):
  - caso 1, H0: ψ² ≤ ψ₀²: J²c = ψ₀²·F(1 − α), CR: J² > J²c, β = F_F(ψ₀²/ψ₁²·F(1 − α));
  - caso 2, H0: ψ² ≥ ψ₀²: J²c = ψ₀²·F(α), CR: J² < J²c, β = 1 − F_F(ψ₀²/ψ₁²·F(α)).
  - Con desvíos «el φ va al cuadrado»: Jc = √(φ₀²·F), y se compara J con Jc. «Reducir el desvío un 12 %» ⇒
    H0: φ ≥ 0,88.

### Ejemplo IV-1 · Tornos, intervalos (resuelto en clase)
<!-- temas: IV -->
<!-- tipos: ic n -->

> «… dos tornos … diámetros (en décimas de mm): S₁ = 3,6 con n₁ = 13 y S₂ = 5,4 con n₂ = 25. a) Límites del 90 %
> para la relación entre las varianzas. b) Con muestras iguales, n para reducir la relación entre límites a la
> mitad. c) Ídem a) para los desvíos. d) Ídem b) para los desvíos.»

1. **Variable**: diámetro de una pieza, en décimas de mm, en el torno A y en el B. Se elige ψ² = σA²/σB².
2. **a)** J² = 3,6²/5,4² = 4/9 = 0,4444; ν₁ = 12, ν₂ = 24; F(0,95; 12; 24) = 2,1834 y F(0,05; 12; 24) = 0,3991.
   A = **0,2035**, B = **1,1136**: P(0,2035 ≤ σA²/σB² ≤ 1,1136) = 0,90. «La varianza de A es como mínimo un
   79,65 % menor y como máximo un 11,36 % mayor que la de B.»
3. **b)** R = B/A = 5,4704; objetivo R/2 = 2,7352 ⇒ iterando, **ν = 44 ⇒ n = 45 piezas por torno** (32 más en A y
   20 más en B).
4. **c)** A' = √A = **0,4511**, B' = √B = **1,0553**: P(0,4511 ≤ σA/σB ≤ 1,0553) = 0,90.
5. **d)** R' = 2,3389; objetivo R'/2 = 1,1694 ⇒ **R = R'² = 1,3676** ⇒ **ν = 443 ⇒ n = 444 por torno**.

### Ejemplo IV-4 · Hiladoras, ensayo sobre desvíos (resuelto en clase)
<!-- temas: IV -->
<!-- tipos: ensayo beta diseno -->

> «… reacondicionar las hiladoras si es posible asegurar una reducción del 12 % en el desvío estándar de la
> producción por máquina. 4 reacondicionadas: desvío 132 m; 16 sin reacondicionar: desvío 354 m. a) ¿Se puede
> asegurar, con 10 % de error, la reducción del 12 %? b) ¿Probabilidad de detectar una reducción del 30 %?»

1. **Variable**: producción de hilado de una máquina en el período, en metros (m). φ = σCR/σSR (reacondicionadas /
   sin reacondicionar).
2. **H0: φ ≥ 0,88** (el reacondicionamiento no reduce el desvío un 12 %) · H1: φ < 0,88. Pesimista: es una
   inversión, y además el enunciado pide «asegurar» la reducción.
3. α = 0,10 = P(reacondicionar | no se reduce el 12 %). ν₁ = 3, ν₂ = 15.
4. F(0,10; 3; 15) = 0,1923 ⇒ **Jc = √(0,88²·0,1923) = 0,3859**. CR: J < 0,3859. RD: «Si el desvío de las
   reacondicionadas dividido el de las sin reacondicionar da menos de 0,3859, se reacondicionan las hiladoras.»
5. **Estimador**: J = 132/354 = **0,3729** < 0,3859 ⇒ **se rechaza H0**: «puedo asegurar que el reacondicionamiento
   reduce el desvío en más de un 12 %».
6. **b)** φ₁ = 0,70: 0,88²/0,7²·0,1923 = 0,3039; 1 − β = F_F(0,3039; 3; 15) = **0,1779** (β = 0,8221).
   Para 1 − β = 0,90: R = (0,88/0,7)² = 1,5804 ⇒ ν = 127 ⇒ **n = 128 por tipo**.

## 8. Tema V · Comparación de medias
<!-- temas: V -->

- **Elegir el método y justificarlo**: (1) σ₁ y σ₂ conocidos ⇒ Z (es teórico); (2) desconocidos ⇒ **test F
  auxiliar previo**: unilateral, sospechando mayor la varianza de la muestra con S mayor, con **α propio grande
  (0,10)**, no el del problema; no se rechaza ⇒ **amalgamado**, se rechaza ⇒ **Welch**; (3) mismo individuo o
  misma unidad experimental ⇒ **apareadas**. **n iguales no significa apareadas.**
- **Amalgamado**: S²a = [(n₁ − 1)S₁² + (n₂ − 1)S₂²]/(n₁ + n₂ − 2), ν = n₁ + n₂ − 2 (S²a queda entre S₁² y S₂²).
  Caso 1 (H0: Δ ≤ Δ₀): Dc = Δ₀ + t(1 − α)·Sa·√(1/n₁ + 1/n₂); caso 2, con −.
- **Welch**: √(S₁²/n₁ + S₂²/n₂), ν = (S₁²/n₁ + S₂²/n₂)²/[(S₁²/n₁)²/(n₁ − 1) + (S₂²/n₂)²/(n₂ − 1)], **truncado**.
- **Apareadas**: d = diferencia por individuo; estimador d̄, S_D, t con ν = n − 1.
- **Diferencias porcentuales**: «μ₁ supera en un 10 % a μ₂» ⇒ Δ* = μ₁ − 1,10·μ₂, estimador D* = x̄₁ − 1,10·x̄₂.
  Error: Sa·√(1/n₁ + h²/n₂): **h² va en el término de la población que lleva h** (en Welch también dentro de ν).
- El estimador tiene que ser coherente con el parámetro. Sin bilaterales, **sin β ni n** (t no central).
  «Diferencia mínima o máxima»: un solo límite con t(1 − α).

### Ejemplo V-8 · Látex con aditivo (resuelto en clase)
<!-- temas: V -->
<!-- tipos: ensayo ic -->

> «… aditivo … que se espera aumente la resistencia media a la tracción. 21 ensayos con aditivo: media 8,5 kg,
> desvío 1,2 kg. Sin aditivo, 61 ensayos: media 7,6 kg, desvío 1,25 kg. a) ¿Aseguraría, con 5 % de riesgo, que
> el aditivo aumenta la resistencia media en 0,45 kg al menos? b) Diferencia mínima con 95 % de confianza.
> c) ¿Aseguraría que la aumenta en un 10 % al menos? d) Porcentaje mínimo de aumento con 95 % de confianza.»

1. **Variable**: resistencia a la tracción de una probeta de látex, en kg, con aditivo (CA) y sin aditivo (SA).
2. **Test F auxiliar** (σ desconocidos): SSA > SCA ⇒ H0: σSA/σCA ≤ 1, α = 0,10. Jc = √F(0,90; 60; 20) =
   √1,6768 = 1,2949; J = 1,25/1,2 = 1,0417 < 1,2949 ⇒ no se rechaza ⇒ se suponen iguales ⇒ **amalgamado**:
   S²a = (20·1,2² + 60·1,25²)/80 = 1,5319 ⇒ Sa = 1,2377 kg, ν = 80, t(0,95; 80) = 1,6641.
3. **a)** Pesimista (el aditivo es un cambio; el enunciado pide asegurar el aumento): **H0: μCA − μSA ≤ 0,45 kg**
   · H1: > 0,45. Dc = 0,45 + 1,6641·1,2377·√(1/21 + 1/61) = **0,9711 kg**. CR: D > 0,9711.
   D = 8,5 − 7,6 = 0,9 kg < 0,9711 ⇒ **no se rechaza H0**: «no hay evidencia suficiente para asegurar que el
   aditivo aumente la resistencia media en 0,45 kg o más».
4. **b)** Un solo límite ⇒ t(0,95): A = 0,9 − 1,6641·1,2377·0,2530 = **0,3788 kg**. P(0,3788 kg ≤ μCA − μSA) = 0,95.
5. **c)** **H0: μCA − 1,10·μSA ≤ 0** · H1: > 0. h = 1,10 multiplica a μSA ⇒ h² va con nSA:
   D*c = 1,6641·1,2377·√(1/21 + 1,21/61) = **0,5349 kg**. D* = 8,5 − 1,10·7,6 = **0,14 kg** < 0,5349 ⇒ no se
   rechaza H0.
6. **d)** Inecuación en h: 8,5 − 7,6h > 1,6641·1,2377·√(1/21 + h²/61). Al elevar al cuadrado: raíces 1,0490 y
   1,1906. Verificación en la original: con h = 1,1906 el lado izquierdo da −0,5483 (no sirve) ⇒ **h = 1,0490**:
   «con 95 % de confianza, el aditivo aumenta la resistencia media como mínimo un 4,90 %».

### Ejemplo V-12 · Trigo, muestras apareadas (resuelto en clase)
<!-- temas: V -->
<!-- tipos: ensayo ic apareadas -->

> «… dos nuevas variedades de trigo … 8 fincas plantando ambas variedades en parcelas de cada finca (quintales por
> parcela): A: 86 87 56 93 84 93 75 79; B: 80 79 58 91 77 82 74 66. a) ¿Se puede asegurar, con riesgo del 5 %, que
> A produce más que B en más de 2 quintales por parcela? b) IC del 90 % para la diferencia.»

1. **Variable**: d = producción de A − producción de B en una misma finca, en quintales por parcela.
   **Apareadas**: las dos variedades se plantan en la misma finca (misma unidad experimental), no porque los n
   sean iguales. Δ = μA − μB.
2. d = 6, 8, −2, 2, 7, 11, 1, 13 ⇒ d̄ = **5,75**, S_D = **5,1200**, ν = 7.
3. **a)** El enunciado pide asegurar «más de 2» ⇒ **H0: Δ ≤ 2** · H1: Δ > 2; α = 0,05; t(0,95; 7) = 1,8946.
   D̄c = 2 + 1,8946·5,1200/√8 = **5,4295**. CR: d̄ > 5,4295. d̄ = 5,75 > 5,4295 ⇒ **se rechaza H0**: «puedo
   asegurar que la variedad A produce más de 2 quintales por parcela más que la B».
4. **b)** P(2,3204 ≤ Δ ≤ 9,1796) = 0,90 (quintales por parcela).

## 9. Tema VI
<!-- temas: VI -->

### 9.1 Contrastes χ²: cómo se resuelven
<!-- temas: VI -->

- **Cuál usar**: «asociación» ⇒ **independencia**; «niveles, probabilidades o porcentajes» de varios grupos (también
  dos proporciones) ⇒ **consistencia**; «se ajusta a / sigue un modelo / patrón» ⇒ **bondad de ajuste**.
- No hay criterio pesimista ni optimista: la H0 es siempre la misma por tipo.
  - Consistencia: **por categoría**: p₁ª,M = p₁ª,T = p₁ª,N, y lo mismo para cada categoría (no «p mañana = p
    tarde»). H1: alguna es distinta.
  - Independencia: **en palabras** («las fallas de pintura son independientes del color»).
  - Bondad: «lo observado se ajusta al modelo X».
- α: si no lo dan, en general 0,05. CR siempre a la derecha: χ² > χ²(1 − α; ν).
- Los observados no se tocan. Los esperados **llevan decimales** (nunca se redondean a enteros) y las sumas
  cierran. N ≥ 60 y todos los E ≥ 5 (los O pueden ser 0); si un E < 5, **amalgamar** con la clase vecina.
- Esperados: consistencia, p̂ global de la categoría × n del grupo; independencia, total fila · total columna / N;
  bondad, N·pᵢ (las pᵢ suman 1).
- ν: tablas (f − 1)(c − 1); bondad: **clases efectivas** − 1 − parámetros estimados con la muestra (Poisson con x̄
  ⇒ 1; uniforme o patrón histórico ⇒ 0).
- **Completar el dominio**: agregar una clase al final (y/o al principio) con O = 0 y probabilidad **acumulada**
  (G en la última, F en la primera), no la puntual.
- **Ajuste demasiado perfecto**: si χ² < χ²(α; ν), sospechar de los datos.
- Conclusiones: al rechazar en consistencia, «algún nivel es distinto» (no «todos»). Al no rechazar
  independencia, «no hay evidencia suficiente para asegurar que exista asociación». **Discretas**: se rechaza ⇒
  no sigue el modelo; no se rechaza y se cumple el proceso físico ⇒ «sigue el modelo»; no se rechaza y no se
  cumple ⇒ «es un buen candidato».
- Pasos: variable y categorías → H0/H1 → α → ν, χ²c, CR y RD → tabla de O, E y aportes → χ² → conclusión.

### Ejemplo VI-6 · Consistencia, tres turnos (resuelto en clase)
<!-- temas: VI -->
<!-- tipos: chi_contingencia ensayo -->

> «… niveles de calidad en cada turno: Mañana 450/45/5 (500); Tarde 680/80/40 (800); Noche 320/40/40 (400)
> (primera / segunda / defectuosas). Para un riesgo del 1 %, ¿se puede asegurar que los niveles de calidad en los
> tres turnos difieren?»

1. **Variable**: nivel de calidad de una pieza (primera, segunda, defectuosa), según el turno. Pide «niveles» ⇒
   consistencia.
2. **H0**: p₁ª,M = p₁ª,T = p₁ª,N; p₂ª,M = p₂ª,T = p₂ª,N; p_def,M = p_def,T = p_def,N · H1: algún nivel difiere.
3. α = 0,01; ν = (3 − 1)(3 − 1) = 4; χ²(0,99; 4) = 13,2767. CR: χ² > 13,2767.
4. p̂ globales: 0,8529 / 0,0971 / 0,05. Esperados (M, T, N): 1ª 426,47 / 682,35 / 341,18; 2ª 48,53 / 77,65 /
   38,82; def. 25 / 40 / 20.
5. χ² = **38,9843** > 13,2767 ⇒ **se rechaza H0**: «puedo asegurar que en algún turno el nivel de calidad es
   distinto».

### Ejemplo VI-7 · Independencia, color y fallas (resuelto en clase)
<!-- temas: VI -->
<!-- tipos: chi_contingencia ensayo -->

> «… producción: 550 blancos, 450 azules, 480 rojos, 320 verdes; 300 reclamos por pintura (30 %, 30 %, 25 %,
> 15 %). Riesgo del 5 %: ¿existe asociación entre el color y el porcentaje de fallas por pintura?»

1. **Variable**: estado de un auto (con o sin falla de pintura) y su color. Pide «asociación» ⇒ independencia.
2. **H0**: las fallas de pintura son independientes del color · H1: hay asociación.
3. α = 0,05; ν = (2 − 1)(4 − 1) = 3; χ²(0,95; 3) = 7,8147. CR: χ² > 7,8147.
4. Observados con falla: 90 / 90 / 75 / 45; sin falla: 460 / 360 / 405 / 275. Esperados con falla: 91,67 / 75 /
   80 / 53,33; sin falla: 458,33 / 375 / 400 / 266,67.
5. χ² = **5,5739** ≤ 7,8147 ⇒ **no se rechaza H0**: «no hay evidencia suficiente para asegurar que exista asociación
   entre el color y las fallas de pintura».

### Ejemplo VI-10 · Bondad de ajuste, dado (resuelto en clase)
<!-- temas: VI -->
<!-- tipos: chi_ajuste ensayo -->

> «… se arrojó un dado 60 veces: 14, 6, 6, 13, 16, 5. ¿Se puede asegurar, con probabilidad de error 0,05, que el
> dado está cargado?»

1. **Variable**: número que sale en una tirada (1 a 6). **H0**: lo observado se ajusta al modelo uniforme
   (pᵢ = 1/6) · H1: no se ajusta.
2. α = 0,05; Eᵢ = 60·1/6 = 10; ν = 6 − 1 − 0 = 5; χ²(0,95; 5) = 11,0705. CR: χ² > 11,0705.
3. χ² = **11,8** > 11,0705 ⇒ **se rechaza H0**: «puedo asegurar que el dado no sigue el modelo uniforme: está
   cargado». (Además 11,8 > χ²(0,05; 5) = 1,1455: no es un ajuste demasiado perfecto.)

### Ejemplo VI-13 · Bondad de ajuste a un patrón histórico (resuelto en clase)
<!-- temas: VI -->
<!-- tipos: chi_ajuste ensayo -->

> «Históricamente: 40 % de 24", 40 % de 36" y 20 % de 40". Muestra de 200 ventas: 85, 65 y 50. ¿Hubo cambios
> respecto del patrón histórico, con riesgo del 5 %?»

**H0**: las ventas se ajustan al patrón histórico (0,40 / 0,40 / 0,20). Eᵢ = 80 / 80 / 40; ν = 3 − 1 − 0 = 2;
χ²(0,95; 2) = 5,9915. χ² = **5,625** ≤ 5,9915 ⇒ **no se rechaza H0**: «no hay evidencia suficiente para asegurar que
el patrón histórico de ventas haya cambiado».

### Ejemplo VI-16 · Bondad de ajuste a Poisson (resuelto en clase)
<!-- temas: VI -->
<!-- tipos: chi_ajuste ensayo -->

> «… reclamos por día de levantacristales; se supone un proceso de Poisson. 684 días: r = 0 a 10 con 26, 62, 120,
> 145, 131, 101, 61, 27, 9, 1, 1. ¿Se pueden asegurar las premisas?»

1. **Variable**: cantidad de reclamos en un día. **H0**: lo observado se ajusta al modelo de Poisson · H1: no.
2. m̂ = x̄ = **3,5263** (un parámetro estimado). Se completa el dominio con la clase «11 o más» (O = 0) con
   probabilidad **G(11) = 0,0011**, no la puntual.
3. Esperados: 20,12 / 70,94 / 125,09 / 147,03 / 129,62 / 91,42 / 53,73 / 27,07 / 11,93 / 4,67 / 1,65 / 0,74.
   Como 4,67, 1,65 y 0,74 < 5, se amalgaman 9, 10 y «11 o más»: O = 2, E = 7,06.
4. 10 clases efectivas ⇒ ν = 10 − 1 − 1 = 8; χ²(0,95; 8) = 15,5073. χ² = **9,4346** ≤ 15,5073 ⇒ **no se
   rechaza H0**. Como los reclamos son acontecimientos puntuales en un medio continuo (el proceso físico de
   Poisson se cumple), se puede afirmar que siguen el modelo de Poisson.

## 10. Regresión (Temas VII y VIII)
<!-- temas: VII VIII -->

**Provisorio**: al 22/10 el profesor todavía no dio regresión, así que no hay reglas suyas para este tema. Seguí la
resolución del solver paso a paso, definí x e y con unidades, interpretá los coeficientes en palabras y cerrá cada
intervalo con su expresión formal. No agregues criterios que no estén en la resolución del solver.

## 11. Checklist final

- [ ] ¿Está definida la variable en palabras (con su **unidad** si es una medición)?
- [ ] ¿Las probabilidades están entre 0 y 1 (nunca en %) y el desarrollo con al menos 4 decimales?
- [ ] ¿Se fijó α antes de mirar la muestra (sin decidir por p-value)?
- [ ] ¿Están la **CR** y la **RD** en lenguaje de planta?
- [ ] ¿No aparece «Acepto H0» ni se da H0 por probada?
- [ ] ¿La conclusión está en el contexto del enunciado?

### 11.1 Checklist de los temas con parámetros
<!-- temas: I II III IV V VII VIII -->

- [ ] ¿La igualdad está en H0 y la H0 está justificada en palabras (temas I a V)?
- [ ] ¿Se comparó el estimador contra el crítico, en unidades de la variable?
- [ ] ¿Cada intervalo cierra con P(A ≤ θ ≤ B) = 1 − α? ¿Con un solo límite se usó α entero?
- [ ] ¿Los tamaños de muestra están al **entero superior** (y con Δn si había muestra)?
