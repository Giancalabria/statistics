# Informe: clase 13 (29/10/2026), Estadística Aplicada, Ing. S. A. Dopazo

Fuente: transcripción automática de NotebookLM de «Reunión en General-20261029_184339-Grabación de la reunión (1)-converted.mp3» (fuente `434667af`). La leí completa.
Los números de VI-15 los **recalculé con scipy**. Cuando el ASR dicta mal un número, pongo el recalculado y lo aclaro.

---

## 0. Logística

- Χ² para variables continuas cierra el Tema VI. Después del descanso **empezó regresión**: «es el último tema».
- La validación del modelo de regresión queda para la clase siguiente (05/11).
- Hubo cambios de cronograma («le agregaron un sábado más», «tener que dar el examen el 21 de diciembre»). El ASR no deja claro si habla del final o de otra materia. **Hay que confirmarlo en el campus.**
- **Aplicativo *Probability Distributions*:** la versión nueva sacó modelos para cobrarlos. «Jamás usted tiene que poner actualización automática». La Gumbel no está en el aplicativo; la Weibull sí (en la versión vieja).
- Excel: `GAMMA()` existe desde la versión 2019. Si no está, usar `EXP(GAMMA.LN(x))`.
- **Apéndice del apunte, pp. 123 a 127:** explica todos los modelos, sus parámetros y cómo estimarlos. «Lo que yo tomo está en el apunte».
- **El apunte tiene ejemplos resueltos de ajuste** (la guía no):
  - empírico;
  - uniforme;
  - binomial (con p conocido y con p estimado);
  - Poisson;
  - normal (con parámetros conocidos y desconocidos);
  - lognormal, Pareto y gamma.

  Dijo que esta vez lo van a tener que leer.
- **VI-20** (el último de la guía, resuelto) es «un típico problema»: junta comparación de dos marcas con bondad de ajuste para una de ellas.
- En el examen **no** va a pedir varios modelos como en VI-15: pide el ajuste a **un** modelo y la respuesta es «rechazo» o «es un buen candidato».

## 1. Reglas nuevas: χ² de bondad de ajuste con modelos continuos

- **Procesar siempre los datos primero:** x̄ y S con las marcas de clase.
- **Las probabilidades se calculan siempre por intervalos.** En una continua, la probabilidad puntual es nula.
- **Completar el dominio del modelo con clases nuevas, con Fo = 0 y probabilidad acumulada.**
  - Gumbel (dominio ℝ) con datos que empiezan en 0: se agrega «0 o menos» **y** «105 o más».
  - Weibull (dominio x ≥ 0): **solo** se agrega la clase final, porque los datos ya arrancan en 0.
  - Las clases agregadas se amalgaman solo si su Fe < 5. En Gumbel del mínimo, la clase «≤ 0» tiene Fe = 7,04 y **queda sola**. Eso suma una clase efectiva (ν = 4, no 3).
- **Estimación de parámetros por momentos** (μ ≈ x̄, σ ≈ S):
  - Gumbel: σ = β·π/√6 ⇒ β = S·√6/π.
    - Del mínimo: μ = θ − 0,5772·β ⇒ θ = x̄ + 0,5772·β.
    - Del máximo: μ = θ + 0,5772·β ⇒ θ = x̄ − 0,5772·β.
    - 0,5772156649 es la constante de Euler-Mascheroni («no confundir con el número e»).
  - Gumbel del mínimo: G(x) = e^(−e^((x−θ)/β)). Gumbel del máximo: F(x) = e^(−e^(−(x−θ)/β)), con los dos exponentes negativos.
  - Weibull: G(x) = e^(−(x/β)^ω), con μ = β·Γ(1+1/ω) y σ = β·√(Γ(1+2/ω) − Γ²(1+1/ω)). ω (forma) no tiene unidades.
  - **Tres métodos válidos para la Weibull (decir cuál se usó):**
    1. **Solver de Excel** (el más exacto): celda objetivo = (β·Γ(1+1/ω) − x̄)² + (β·√(…) − S)², igualada a 0 cambiando β y ω, con valores iniciales mayores que 1.
    2. **Buscar objetivo** (Datos → Análisis de hipótesis): β = x̄/Γ(1+1/ω) y se busca ω.
    3. **Tabla «Ajuste por momentos Distribución Weibull»** (en los materiales): con CV = S/x̄ se busca ω y la columna μ/β, y β = x̄/(μ/β). Es la menos precisa.
- **Grados de libertad:** ν = clases efectivas − 1 − parámetros estimados.
- **Conclusión en continuas:** no rechazar H0 **no** prueba que la variable siga el modelo. Se escribe «el modelo X **es un buen candidato** para modelar…». La razón es que puede haber otro modelo que ajuste mejor.
- **Mejor ajuste:** entre los modelos que no se rechazan, el de **menor χ² observado** (con el mismo ν).
- **Proceso físico** (para justificar la sospecha):
  - Gumbel del mínimo: vida de seres vivientes («si una herramienta de corte le habló, vaya urgente al psicólogo»);
  - Gumbel del máximo: estiramiento hasta la ruptura de materiales.
- **En la práctica** se prueban todos los modelos conocidos, se descartan los que se rechazan y se usa el que mejor ajusta. No hay que afirmar «la variable es normal» sin haberlo probado.

## 2. Regresión (inicio, Temas VII y VIII)

- La regresión busca **relaciones funcionales**: simple (una X) o múltiple. Se ven modelos lineales o linealizables.
- **«Lineal» = lineal en los parámetros**, no en X: Y = β₀ + β₁X² es lineal porque X es dato.
  - No lineales: β₁² o e^(β₁X).
  - Linealizables con logaritmo: β₀·X^β₁·e^ε, β₀·β₁^X·e^ε, etc.
- **Dirección única:** Y en función de X, nunca al revés.
- **X es la variable explicativa** (no «independiente»). Lo que tiene que ser independiente son las X entre sí, no X de Y. Conviene que X **no sea aleatoria** y que se pueda manipular (gastos de publicidad sí, precio de la competencia no).
- **Y es la variable explicada**, siempre aleatoria.
- **β₀** es el valor de Y cuando X no influye: mide el grado de independencia de Y respecto de X. Y depende totalmente de X solo si β₀ = 0.
- **β₁** es el **coeficiente de regresión** (no siempre «pendiente») o la **contribución marginal**: cuánto aumenta Y por cada unidad de X. Si β₁ = 0, X no explica a Y.
- **ε** es la **perturbación del entorno**, estocástica pura, que no se puede cuantificar.
- **Modelos:**
  - Y = β₀ + β₁X es el modelo promedio.
  - Y = β₀ + β₁X + ε es el modelo puntual (el valor verdadero).
  - Ŷ = b₀ + b₁X es el estimador. Sirve **solo si el modelo es válido**.
  - Estimar el promedio es un IC «entre A y B con cierta confianza». Predecir el valor puntual es un **pronóstico**.
- **Mínimos cuadrados** (Gauss y Laplace): minimizar Q = Σ(yᵢ − b₀ − b₁xᵢ)².
  - b₀ = ȳ − b₁x̄, así que la recta pasa por el baricentro (x̄, ȳ).
  - b₁ = (Σxy − n·x̄·ȳ)/(Σx² − n·x̄²).
  - Se arma una tabla con x, y, x², y², xy. La calculadora en modo regresión da A = b₀ y B = b₁.
- **Hacen falta muchos puntos:** dos puntos «no me dicen nada» (estimación inconsistente).
- **Validación (se ve el 05/11):**
  1. Ensayo con H0: no hay relación entre las variables.
  2. Que la relación, si existe, sea **fuerte** («no sirven las relaciones platónicas»).

  Son condiciones necesarias, no suficientes. Interesan las relaciones **causa-efecto**, no las casuales (ejemplo: canguros en Australia y trigo en América Latina).

## 3. Ejercicio resuelto en clase: VI-15 (herramientas de corte, p. 46)

Datos:
- Clases 0-15, 15-30, …, 90-105, con Fo = 8, 40, 30, 25, 18, 15, 7 (N = 143); α = 0,01.
- x̄ = 45,6818 h y S = 24,3257 h, con las marcas de clase.

| Modelo | Parámetros | Clases (antes de amalgamar → después) | χ² | ν | χ²(0,99; ν) | Decisión |
|---|---|---|---|---|---|---|
| Gumbel del mínimo | β = 18,9667 h; θ = 56,6297 h | ≤0 (Fe 7,04) + 7 + ≥105 (Fe 0,00); se unen las 3 últimas (Fo 22, Fe 10,26) → 7 | **68,5632** (prof.: 68,55) | 4 | 13,2767 | Se rechaza |
| Gumbel del máximo | β = 18,9667 h; θ = 34,7339 h | ≤0 + 0-15 (Fo 8, Fe 8,43); 90-105 + ≥105 (Fo 7, Fe 7,55) → 7 | **10,8569** (prof.: 10,8398) | 4 | 13,2767 | Buen candidato |
| Weibull | ω = 1,9592; β = 51,52 h | sin clase inicial; 90-105 + ≥105 (Fo 7, Fe 7,24) → 7 | **8,3167** (prof.: 8,3318) | 4 | 13,2767 | Buen candidato, **el mejor** |

Notas:
- El ASR dicta ω = «1 com 95 47», pero las probabilidades que lee el profesor (0,0853; 0,2076; 0,2427; 0,2046; 0,1357; 0,0734; 0,0330; 0,0177) son las de ω = 1,9592. Con la tabla: CV = 0,5325 ⇒ ω ≈ 1,95, μ/β ≈ 0,8865 y β = 51,51.
- Las diferencias en la segunda o tercera cifra decimal de χ² vienen de que el profesor redondeó las Fe (12,2 en lugar de 12,19).
- La guía coincide: a) se rechaza Gumbel del mínimo; b) Gumbel del máximo y Weibull son buenos candidatos y el mejor es Weibull.

## 4. Contraste con el solver (este repo)

- **Corregido:** el solver estiraba la primera y la última clase observadas hasta el borde del dominio, en lugar de agregar clases nuevas con Fo = 0.
  - En Gumbel del mínimo eso daba χ² = 64,8385, con ν = 3 y crítico 11,3449. La decisión era la misma, pero los números no coincidían con los de clase.
  - Ahora agrega las clases aparte y da 68,5632, con ν = 4 y crítico 13,2767.
  - En los demás ejercicios de la guía no cambia ninguna decisión ni ningún χ².
- La estimación por momentos de Gumbel y de Weibull ya coincidía con la de clase.
