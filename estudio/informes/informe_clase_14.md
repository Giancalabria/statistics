# Informe: clase 14 (05/11/2026), Estadística Aplicada, Ing. S. A. Dopazo

Fuente: transcripción automática de NotebookLM de «Reunión en General-20261105_184328-Grabación de la reunión-converted.mp3» (fuente `a6806e52`), leída completa, y capturas del video (el pizarrón con VII-13 resuelto). Los números de VII-13 los **verifiqué con el solver**: coinciden todos con los del pizarrón.

---

## 0. Logística

- **«Hasta acá entra el parcial»: regresión simple completo. Regresión múltiple NO entra en el parcial.** La múltiple se sigue dando la clase que viene (primera parte de la clase del 12/11) y entra **para el final**.
- En múltiple «es todo por computadora»: el profesor va a dar **la salida del Excel** y pedir que se interprete algo. No hay que calcular nada a mano.
- Excel: *Complementos → Herramientas para análisis*; *Datos → Análisis de datos → Regresión*, con «Rótulos» tildado y nivel de confianza (95 % por defecto). También mostró el complemento gratuito **Real Statistics**.
- **El análisis de varianza (ANOVA, el F global) «no sirve para nada»**: es como ponerle un 7 a un grupo de cinco sin saber quién trabajó. Lo que interesa es si **cada variable** aporta (t individual). Excel informa el t observado y el p-value («probabilidad»), no el t crítico.
- Excel ordena el IC de β₁ bien (el más negativo como límite inferior); «el error que no tienen que cometer ustedes» es ponerlo al revés.

## 1. Validación del modelo (análisis confirmatorio)

- Se valida **siempre, aunque no lo pidan**: «la validación la vas a tener que hacer aunque no te la pida». Si piden estimar Y, lo primero es validar; **si el modelo no es válido, la pregunta no tiene sentido**.
- Dos condiciones, ambas **necesarias** (ninguna suficiente):
  1. **Existencia de la relación**: H0: ρ = 0 (o β₁ = 0, da exactamente lo mismo; los «puros matemáticos» prefieren β₁). t_obs = r/√((1 − r²)/(n − 2)) = b₁/S_b₁, **en valor absoluto**. CR: |t_obs| > t(1 − α; ν), ν = n − 2 (siempre n − 2 en simple: se estiman dos parámetros). Si no dan α, se elige.
  2. **Fuerza de la relación** según el uso, con r² (orientativo, no taxativo): ≥ 0,4 sociología / psicología; ≥ 0,6 problemas económicos (macro y micro); ≥ 0,8 técnicos o industriales.
- Recién con el modelo validado b₀, b₁ e ŷ son buenos estimadores.

## 2. Conceptos y notación

- **r (coeficiente de correlación)**: mide cuán fuerte es la relación; entre −1 y 1, con el **signo de b₁** (algunas calculadoras dan |r|: ponerle el signo de la pendiente).
- **r² (coeficiente de determinación)**: «influencia porcentual que tiene X en la explicación de Y». El resto lo explica la perturbación del entorno u otra variable que no está en el modelo. Ningún modelo explica el 100 %.
- No confundir **coeficiente de correlación, de determinación y de regresión** (β₁, contribución marginal).
- S² = (Σy² − b₀Σy − b₁Σxy)/(n − 2): varianza del **modelo** (no de una variable; la calculadora no la da). S_b₁² = S²/(Σx² − n·x̄²).
- **β₀ no se estima**. El modelo se valida solo en el **entorno observado** (x mínimo a x máximo); fuera de él no se sabe qué pasa (saturación del mercado, de la producción). b₀ se interpreta «en teoría» y aclarando que no se puede asegurar.
- **Extrapolar** (x₀ fuera del entorno) tiene mucho error: el intervalo «se abre» al alejarse del baricentro (x̄).
- **Inferencias**:
  - IC de β₁: b₁ ± t(1 − α/2; n − 2)·S_b₁. Con valores negativos, **A es el más negativo**.
  - Promedio de Y para x₀: E(y | x₀) entre ŷ₀ ± t(1 − α/2; n − 2)·S·√(1/n + (x₀ − x̄)²/(Σx² − n·x̄²)).
  - Valor individual (**intervalo de predicción = pronóstico**): lo mismo con «1 +» dentro de la raíz (la perturbación del entorno). Un pronóstico es un intervalo, no un valor.
  - IC de ρ por Fisher: Zρ = ½·ln((1 + r)/(1 − r)) ± Z(1 − α/2)·√(1/(n − 3)); A = (e^(2Zρmín) − 1)/(e^(2Zρmín) + 1), B igual con Zρmáx. Para **ρ²**, los límites al cuadrado. Rara vez pide ρ: pide la influencia (ρ²).
  - Ensayo de β₁: **no hay bilateral**. H0: β₁ ≤ β₁₀ ⇒ b₁c = β₁₀ + t(1 − α)·S_b₁, rechazo si b₁ > b₁c; H0: β₁ ≥ β₁₀ ⇒ b₁c = β₁₀ − t(1 − α)·S_b₁, rechazo si b₁ < b₁c.
- **«Promedio o no promedio»**: si el inciso dice «promedio» (o «toda la estructura»), es E(y | x₀); si no (un sector, un acero en particular), es predicción.

## 3. Modelos linealizables: cómo se interpretan

| Modelo | Forma | b₁ significa |
|---|---|---|
| Lineal | y = β₀ + β₁x + ε | cambio **absoluto** de Y por cada unidad de X |
| Doble logarítmico (elasticidad constante) | ln y = ln β₀ + β₁ ln x + ε | si X sube 1 %, Y cambia β₁ % |
| Logarítmico lineal | ln y = ln β₀ + (ln β₁)·x + ε | (coeficiente de x)·100 = cambio % de Y por cada unidad de X (helados: −0,015·100 = −1,5 %) |
| Lineal logarítmico | y = β₀ + β₁ ln x + ε | si X sube 1 %, Y cambia β₁/100 unidades (helados: −120/100 = −1,2 miles de kg) |

- Las variables económicas casi siempre se trabajan con logaritmo.
- **Si X ya está en %** (porcentaje de carbono): aumentar «un punto porcentual» (5 % → 6 %) no es aumentar «un 1 %» (5 % → 5,05 %).

## 4. VII-13 (hormigón, pág. 57), resuelto en clase

Y = resistencia al quiebre (MPa); X = profundidad de carbonatación (mm). Pizarrón:

- n = 18; Σx = 659; x̄ = 36,61; Σx² = 28967,5; Σy = 289,2; ȳ = 16,06; Σy² = 5166,36; Σxy = 9165,95.
- b₀ = 26,821217 MPa; b₁ = −0,293751 MPa/mm; r = −0,896366; R² = 0,803472 (80,35 %); S² = 6,385686; S = 2,526991; S_b₁ = 0,03632. **ŷ = 26,82 − 0,29x**.
- Validación: H0: ρ = 0 (β₁ = 0), α = 0,05; |t_obs| = 8,0879; ν = 16; t(0,95; 16) = 1,7459 ⇒ R H0. Uso técnico ⇒ r² ≥ 0,8 y r² = 0,8035 ⇒ **se valida**.
- Interpretación: «por cada milímetro que aumente la profundidad del poro, la resistencia al quiebre disminuye en 0,29 MPa». r²: «la profundidad influye sobre la resistencia en un 80,35 % aproximadamente». β₀ «en teoría» (sin poros, 26,82 MPa), pero el entorno observado es de 8 a 65 mm.
- b) y c) P(A ≤ ρ² ≤ B) = 0,95: A = 0,5455 (54,55 %), B = 0,9237 (92,37 %). «Con 18 datos el error es grande»; para achicarlo hay que agrandar la muestra.
- d) «¿Disminuye en más de 0,25 MPa?»: más negativo ⇒ H0: β₁ ≥ −0,25 vs H1: β₁ < −0,25; b₁c = −0,25 − 1,7459·0,0363 = −0,3134; b₁ = −0,2937 no es menor ⇒ **no se rechaza**: va a disminuir, pero no se puede asegurar que en más de 0,25 MPa. (Error típico: plantear con el signo positivo.)
- e) P(A ≤ β₁ ≤ B) = 0,95: A = −0,3708 MPa/mm, B = −0,2167 MPa/mm.
- f) promedio, x₀ = 10: ŷ₀ = 23,8838; entre 21,4769 y 26,2905 MPa.
- g) un sector, x₀ = 10, predicción: entre 18,01 y 29,76 MPa («al tener en cuenta la perturbación, los límites se amplían»).

## 5. Qué cambió en la app (05/11)

- Regresión simple: variables con unidad (del encabezado de la tabla, editables), bloque de procesamiento como el pizarrón, **validación siempre** (aunque el inciso no la pida), interpretación de b₁, b₀ y r² en términos del problema, límites **hacia afuera** con unidades (antes el IC de β₁ y el de ρ² redondeaban al más cercano: −0,3707 / −0,2168 / 0,9236), aviso de **extrapolación**, interpretación de los modelos log según la tabla de arriba (antes el lineal logarítmico no se interpretaba y el log-lineal usaba (e^b₁ − 1)·100), «punto porcentual» si X está en %.
- Múltiple: la conclusión decide por el **análisis individual** (t); el F global queda como dato.
- Todos los temas con una variable medida (I, II, IV, V): paso **«Variable»** al principio y unidad detectada del enunciado en las conclusiones.
- Error de la app encontrado: los **números negativos escritos en la pantalla perdían el signo** (β₁₀ = −0,25 pasaba a +0,25 y VII-13 d) daba «se rechaza»). Corregido.
