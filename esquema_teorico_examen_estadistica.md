# ESQUEMA TEÓRICO Y LÓGICA DE CÁLCULO PARA LOS EXÁMENES DE ESTADÍSTICA APLICADA
> **Materia**: Estadística Aplicada (UADE)  
> **Cátedra / Profesores**: Ing. Sergio Aníbal Dopazo, Ing. Roberto Mariano García  
> **Objetivo de este documento**: Servir como especificación técnica y base de conocimientos para la aplicación que resuelve los ejercicios de inferencia estadística de la guía.
>
> **Prioridad de las fuentes**: lo que dice el profesor en clase manda sobre la guía, el apunte y este documento (resumen en `estadistica/REGLAS_PROFESOR.md`, clases del 06/08 al 22/10/2026). Si algo de acá lo contradice, está mal.

---

## 0. GLOSARIO DE NOTACIÓN Y REGLAS GENERALES DE PENSAMIENTO

### 0.1 Distinción Parámetro vs. Estimador
- **Parámetro (Población - Desconocido/Teórico)**: Característica fija de toda la población. Representado con **letras griegas** ($p$ es la excepción). Los supuestos y las hipótesis se hacen siempre sobre parámetros, nunca sobre la muestra.
  - $\mu$: Media poblacional.
  - $\sigma$: Desvío estándar poblacional.
  - $\sigma^2$: Varianza poblacional.
  - $p$: Proporción poblacional.
  - $\psi^2$: Cociente de varianzas poblacionales ($\sigma_1^2 / \sigma_2^2$); $\varphi = \sigma_1/\sigma_2$ para desvíos.
  - $\Delta$: Diferencia de medias poblacionales ($\mu_1 - \mu_2$).
- **Estimador (Muestra - Variable Aleatoria)**: Medida calculada sobre una muestra aleatoria de tamaño $n$. Representado con **letras latinas**.
  - $\bar{x}$: Media muestral.
  - $S$: Desvío estándar muestral.
  - $S^2$: Varianza muestral (dividida por $n-1$).
  - $\hat{p} = r/n$: Proporción muestral ($r$ éxitos en $n$).
  - $J^2 = S_1^2 / S_2^2$: Estimador del cociente de varianzas ($J = S_1/S_2$ para desvíos).
  - $D = \bar{x}_1 - \bar{x}_2$: Estimador de la diferencia de medias ($\bar d$ en muestras apareadas).

### 0.2 Símbolos, distribuciones y notación exigida
- $N$: Tamaño de la población (si es finita). $n$: Tamaño de la muestra. $e$: Error muestral (semiamplitud del intervalo).
- $1 - \alpha$: Nivel de confianza (ej. $0{,}95$; se puede decir "95 % de confianza").
- $\alpha$: Riesgo de error de tipo I (ej. $0{,}05$). $\beta$: Riesgo de error de tipo II. $1 - \beta$: Potencia del ensayo. En recepción de partidas, $\alpha$ es el riesgo del proveedor y $\beta$ el del comprador.
- **Las probabilidades se expresan siempre entre 0 y 1, nunca en %.**
- $\nu$: número de grados de libertad ($n-1$, $n_1+n_2-2$, $(f-1)(c-1)$, etc.). Se escribe "ν = número de grados de libertad".
- **P** = probabilidad puntual, **F** = acumulada izquierda, **G** = acumulada derecha, **Φ** = F de la normal estándar. Escribir $P(X \le x)$ en lugar de $F$ es un error conceptual.
- $Z$: Normal estándar. $t$: t de Student ($\nu$). $\chi^2$: Chi-cuadrado ($\nu$). $F$: F de Fisher-Snedecor ($\nu_1$ del numerador, $\nu_2$ del denominador).
- **Decimales**: mínimo 4 en todo el desarrollo y en los fractiles; los periódicos como fracción ($1/37$). El resultado final se expresa según la variable, con unidades.
- **Fundamento de Z o t** (por la estructura, no por "conozco σ"): $\bar x$ es normal; al estandarizar dividiendo por un parámetro ($\sigma$) sigue siendo normal ⇒ $Z$. Si se divide por $S$, que es una variable aleatoria (raíz de una $\chi^2$), queda una $t$ con $\nu = n-1$, **sea cual sea $n$**. La regla "n ≥ 30 ⇒ normal" no se usa.

---

## 1. UNIDAD 1: ESTIMACIÓN DE PARÁMETROS POR INTERVALOS DE CONFIANZA

El objetivo es construir un intervalo $[A; B]$ tal que $P(A \le \text{Parámetro} \le B) = 1 - \alpha$.

- **Redondeo**: límite inferior hacia abajo y superior hacia arriba ("los redondeos en estadística son lógicos, no matemáticos").
- **Un solo límite** (piden "mínimo" o "máximo"): se usa **α entero**, sin dividir por 2.

---

### 1.1 Estimación de la Media Poblacional ($\mu$)

#### CASO A: Desvío Poblacional Conocido ($\sigma$)
- **Distribución**: Normal Estándar ($Z$).
- **Población Infinita**:
  $$\text{Límites } A; B = \bar{x} \pm Z_{(1 - \alpha/2)} \cdot \frac{\sigma}{\sqrt{n}}$$
  $$\text{Error Muestral } e = Z_{(1 - \alpha/2)} \cdot \frac{\sigma}{\sqrt{n}}$$
- **Población Finita ($N$ conocido)**: el factor se aplica siempre que se conoce $N$ (sin umbral de $n/N$).
  $$\text{Factor de Corrección por Finitud} = \sqrt{\frac{N - n}{N}}$$
  $$A; B = \bar{x} \pm Z_{(1 - \alpha/2)} \cdot \frac{\sigma}{\sqrt{n}} \cdot \sqrt{\frac{N - n}{N}}$$
  (Apunte y profesor, 20/08: "Algunos autores ponen sobre N − 1. El uno mucho no hace". Con $N$ se reproduce I-34.)

- **Cálculo del Tamaño de Muestra ($n$)**:
  - *Población Infinita*:
    $$n = \left\lceil \left( \frac{Z_{(1 - \alpha/2)} \cdot \sigma}{e} \right)^2 \right\rceil$$
  - *Población Finita*: Primero calcular $n_\infty = \left( \frac{Z_{(1 - \alpha/2)} \cdot \sigma}{e} \right)^2$, luego corregir:
    $$n = \left\lceil \frac{N \cdot n_\infty}{N + n_\infty} \right\rceil$$

---

#### CASO B: Desvío Poblacional Desconocido (se divide por $S$)
- **Distribución**: $t$ de Student con $\nu = n - 1$ grados de libertad, para cualquier $n$.
- **Población Infinita**:
  $$A; B = \bar{x} \pm t_{(1 - \alpha/2; \nu = n-1)} \cdot \frac{S}{\sqrt{n}}$$
- **Población Finita ($N$ conocido)**:
  $$A; B = \bar{x} \pm t_{(1 - \alpha/2; \nu = n-1)} \cdot \frac{S}{\sqrt{n}} \cdot \sqrt{\frac{N - n}{N}}$$

- **Cálculo del Tamaño de Muestra ($n$) - MÉTODO ITERATIVO**:
  - $n = \left[ \frac{t_{(1 - \alpha/2; \nu = n-1)} \cdot S}{e} \right]^2$. Como $t$ depende de $\nu = n-1$, $n$ aparece a ambos lados.
  - *Algoritmo*:
    1. Arrancar con un $n^{(0)}$ **bastante mayor que el de la muestra original** (nunca igual ni menor).
    2. Calcular $\nu^{(k)} = n^{(k)} - 1$ y el fractil $t_{(1 - \alpha/2; \nu^{(k)})}$.
    3. Recalcular $n^{(k+1)} = \left\lceil \left( \frac{t \cdot S}{e} \right)^2 \right\rceil$.
    4. Repetir hasta que $n^{(k+1)} = n^{(k)}$. Mostrar **todas** las iteraciones ("si necesita más de tres iteraciones, dude").
  - Para bajar el error se sube $n$; nunca se toca el riesgo.
  - *Si la población es finita ($N$)*: Resolver $n_\infty$ con el bucle y luego aplicar $n = \left\lceil \frac{N \cdot n_\infty}{N + n_\infty} \right\rceil$.

---

### 1.2 Estimación de la Varianza Poblacional ($\sigma^2$) y Desvío ($\sigma$)

- **Distribución**: Chi-Cuadrado ($\chi^2$) con $\nu = n - 1$ grados de libertad. Siempre con varianzas: si dan desvíos, se elevan al cuadrado.
- **Intervalo de Confianza para $\sigma^2$**:
  $$P\left( \frac{(n-1)S^2}{\chi^2_{(1 - \alpha/2; \nu)}} \le \sigma^2 \le \frac{(n-1)S^2}{\chi^2_{(\alpha/2; \nu)}} \right) = 1 - \alpha$$
- **Intervalo de Confianza para el Desvío ($\sigma$)**: $[\sqrt{A} \le \sigma \le \sqrt{B}]$.
- **Tamaño de muestra ($n$) — Ecuación de García (estimación)**: la precisión se mide con la **relación entre límites**:
  $$R' = \frac{B'}{A'} \qquad R = (R')^2 = \frac{\chi^2_{(1-\alpha/2;\nu)}}{\chi^2_{(\alpha/2;\nu)}}$$
  - Si el enunciado pide **disminuir un $k\%$** la relación anterior: $R'_{obj} = R'_{orig} \cdot (1 - k)$.
  $$a = \frac{Z_{(1-\alpha/2)} \cdot \left(\sqrt[3]{R} + 1\right)}{2 \cdot \left(\sqrt[3]{R} - 1\right)} \qquad \nu = \frac{2}{9}\left(a + \sqrt{a^2 + 1}\right)^2 \ (\text{al entero superior}) \qquad n = \nu + 1$$
  - El radical de $R$ es **cúbico** (viene de Wilson–Hilferty). $R$ es **de varianzas**: con desvíos, $R = R'^2$ (usar $R'$ es un error frecuente).
  - Si ya se relevó una muestra preliminar: $\Delta n = n - n_{prelim}$.

---

### 1.3 Estimación de la Proporción Poblacional ($p$)

- **Estimador Puntual**: $\hat{p} = r/n$. Bernoulli es población infinita o proceso; el muestreo es binomial.
- **Intervalo: siempre EXACTO** (binomial o distribución F). **Estimar $p$ con la aproximación normal está prohibido** ("aberración estadística"; fue uno de los errores más penalizados en el 1° parcial).
  $$A = \frac{1}{1 + \dfrac{(n-r+1) \cdot F_{(1-\alpha/2;\ 2n-2r+2;\ 2r)}}{r}} \qquad B = \frac{1}{1 + \dfrac{n-r}{(r+1) \cdot F_{(1-\alpha/2;\ 2r+2;\ 2n-2r)}}}$$
  - **Con $r = 0$**: $A = 0$ y hay un solo límite, así que $B$ va con **α entero** (F con $1-\alpha$). III-3b: $B = 0{,}2057$. La guía da 0,2589 (con α/2) y el profesor dijo que está mal.
- **Tamaño de muestra ($n$)** — las aproximaciones sirven **solo para calcular $n$**:
  $$n = \left\lceil \frac{Z_{(1 - \alpha/2)}^2 \cdot \hat{p}(1 - \hat{p})}{e^2} + 1 \right\rceil$$
  - Si $\hat p = 0$, la fórmula da algo "ridículo": se usa el tamaño **máximo** con $p(1-p) = 0{,}25$.
- **Criterios de aproximación** (los únicos que acepta; se aplican al **$n$ resultante**, no al inicial):
  - Normal si $n \cdot p > 10$ **y** $n \cdot (1-p) > 10$.
  - Poisson si $p \le 0{,}005$.
  - Si se cumplen los dos o ninguno: **criterio de Mermoz**: $n_0 = 0{,}23\,(1-p)^2/p^3$ (con $p \le 0{,}5$; con $p \ge 0{,}5$, $n_0 = 0{,}23\,p^2/(1-p)^3$). Si $n > n_0$, normal; si no, Poisson.
  - "No me usen otro criterio porque está mal": nada de $np \ge 5$ ni "n > 30".

---

## 2. UNIDAD 2: ENSAYOS DE HIPÓTESIS (1 POBLACIÓN)

### 2.1 Filosofía del Ensayo de Hipótesis y Matriz de Decisión

1. **Inocente hasta demostración de lo contrario**: $H_0$ se presume verdadera; la decisión contundente sale de rechazarla.
2. **Nunca se dice "Acepto $H_0$"**: "**Se rechaza $H_0$**: puedo asegurar que…" o "**No se rechaza $H_0$**: no hay evidencia suficiente para asegurar que…". Nunca se prueba la igualdad.
3. **Igualdad siempre en $H_0$**: $H_0$ lleva $=, \le, \ge$. $H_1$ (el complemento) lleva $\ne, >, <$.
4. **Pasos, en este orden**: variable (con unidad) → $H_0$/$H_1$ justificadas en palabras → $\alpha$ (y $\beta$) → $n$ → valor crítico, CR y RD (antes de ver la muestra) → estimador → comparar el **estimador contra el valor crítico** y concluir.
5. **Se compara el estimador contra el crítico en unidades de la variable** ($\bar x$ vs $\bar x_c$, $S^2$ vs $S^2_c$, $r$ vs $r_c$, $J^2$ vs $J^2_c$, $D$ vs $D_c$). Nunca contra $\mu_0$ ni con estadísticos observados ($Z$, $t$, $\chi^2$ o $F$ "observado").
6. **$\alpha$ se fija antes y no se toca.** Nunca decidir con el p-value ($\alpha^*$ a posteriori).

#### Matriz de Decisión y Errores
- **Error Tipo I ($\alpha$)**: Rechazar $H_0$ cuando es VERDADERA. Se fija *a priori*.
- **Error Tipo II ($\beta$)**: No rechazar $H_0$ cuando es FALSA.
- **Potencia ($1 - \beta$)**: Probabilidad de rechazar $H_0$ cuando es FALSA.
- Escribir **las 4 probabilidades** ($\alpha$, $1-\alpha$, $\beta$, $1-\beta$) en términos del problema. Ej. I-10: $\alpha$ = P(lanzar el aditivo | $\mu \ge 11{,}2$).

#### Criterios de Planteo para $H_0$:
- **Regla madre**: $H_0$ se plantea de modo que el **error de tipo I sea el más grave**.
- **Orden**: (1) si el enunciado dice qué se quiere probar, eso va en $H_1$; (2) si no, el criterio; (3) si no alcanza, comparar la gravedad de los errores.
- **Criterio Pesimista** (riesgo económico: inversión, máquina o proveedor nuevo, producto nuevo, modificación, campaña publicitaria): $H_0$ = "no funciona / no cumple" ($H_0: \mu \ge \mu_0$ o $\mu \le \mu_0$, según qué sea mejorar). Pesimista aunque la campaña sea barata, si se quiere probar que fue efectiva.
- **Criterio Optimista** (control de proceso, recepción de un **proveedor habitual**, controles de rutina): $H_0$ = "cumple / está bajo control", **con desigualdad** (ej. I-8: $H_0: \mu \ge 250$ g). Rechazar $H_0$ = detener el proceso o rechazar el lote.
- No asociar el criterio con $\le$ o $\ge$.
- **Bilateral solo cuando el enunciado lo impone** ("diferente de", valor exacto). **No existen bilaterales en $\sigma^2$, $\sigma$, $p$ ni en comparaciones de dos poblaciones.**
- $\alpha$ no dado: se elige y se justifica (chico ≤ 0,01, estándar 0,05, grande ≥ 0,10).

---

### 2.2 Ensayos para la Media Poblacional ($\mu$) con $\sigma$ Conocido

#### CASO I: Unilateral Cola Derecha ($H_0: \mu \le \mu_0$ vs $H_1: \mu > \mu_0$)
- **Valor Crítico**: $\bar{x}_c = \mu_0 + Z_{(1 - \alpha)} \cdot \frac{\sigma}{\sqrt{n}}$
- **Condición de Rechazo (CR)**: Si $\bar{x} > \bar{x}_c \implies \text{Se rechaza } H_0$.
- **Error Tipo II ($\beta$)** para $\mu_1 > \mu_0$ (con el crítico con todos sus decimales):
  $$\beta = \Phi\left(\frac{\bar{x}_c - \mu_1}{\sigma / \sqrt{n}}\right)$$
- **Tamaño de muestra para $\alpha$ y $\beta$ fijados** (fórmula de las dos condiciones; nunca reutilizar el $\bar x_c$ de otro $n$):
  $$n = \left\lceil \left[ \frac{(Z_{(1 - \alpha)} + Z_{(1 - \beta)}) \cdot \sigma}{\mu_1 - \mu_0} \right]^2 \right\rceil$$

#### CASO II: Unilateral Cola Izquierda ($H_0: \mu \ge \mu_0$ vs $H_1: \mu < \mu_0$)
- **Valor Crítico**: $\bar{x}_c = \mu_0 - Z_{(1 - \alpha)} \cdot \frac{\sigma}{\sqrt{n}}$
- **CR**: Si $\bar{x} < \bar{x}_c \implies \text{Se rechaza } H_0$.
- **Error Tipo II ($\beta$)** para $\mu_1 < \mu_0$:
  $$\beta = 1 - \Phi\left(\frac{\bar{x}_c - \mu_1}{\sigma / \sqrt{n}}\right)$$

#### CASO III: Bilateral ($H_0: \mu = \mu_0$ vs $H_1: \mu \ne \mu_0$), solo si el enunciado lo impone
- **Valores Críticos**: $\bar{x}_{c1;c2} = \mu_0 \mp Z_{(1 - \alpha/2)} \cdot \frac{\sigma}{\sqrt{n}}$
- **CR**: Si $\bar{x} < \bar{x}_{c1}$ o $\bar{x} > \bar{x}_{c2} \implies \text{Se rechaza } H_0$.
- $\beta = \Phi(z_2) - \Phi(z_1)$; $n$ con $Z_{(1-\alpha/2)}$.

---

### 2.3 Ensayos para la Media Poblacional ($\mu$) con $\sigma$ Desconocido

Se reemplaza $Z$ por $t_{(1-\alpha; \nu = n-1)}$ y $\sigma$ por $S$:
- **Cola Derecha**: $\bar{x}_c = \mu_0 + t_{(1 - \alpha; \nu)} \cdot \frac{S}{\sqrt{n}}$
- **Cola Izquierda**: $\bar{x}_c = \mu_0 - t_{(1 - \alpha; \nu)} \cdot \frac{S}{\sqrt{n}}$
- **Bilateral**: $\bar{x}_{c1;c2} = \mu_0 \pm t_{(1 - \alpha/2; \nu)} \cdot \frac{S}{\sqrt{n}}$
- **No se calculan $\beta$ ni $n$** (requieren la $t$ no central). Si el enunciado los pide, revisar si en realidad $\sigma$ es conocido.

---

### 2.4 Ensayos para la Varianza Poblacional ($\sigma^2$) — siempre unilaterales

- **Caso 1** ($H_0: \sigma^2 \le \sigma_0^2$ vs $H_1: \sigma^2 > \sigma_0^2$):
  - $S^2_c = \dfrac{\sigma_0^2 \cdot \chi^2_{(1 - \alpha; \nu)}}{\nu}$. CR: Si $S^2 > S^2_c \implies$ Se rechaza $H_0$.
  - $\beta = F_{\chi^2}\left(\dfrac{\nu \cdot S^2_c}{\sigma_1^2};\ \nu\right)$.
- **Caso 2** ($H_0: \sigma^2 \ge \sigma_0^2$ vs $H_1: \sigma^2 < \sigma_0^2$):
  - $S^2_c = \dfrac{\sigma_0^2 \cdot \chi^2_{(\alpha; \nu)}}{\nu}$. CR: Si $S^2 < S^2_c \implies$ Se rechaza $H_0$.
  - $\beta = G_{\chi^2}\left(\dfrac{\nu \cdot S^2_c}{\sigma_1^2};\ \nu\right) = 1 - F_{\chi^2}(\dots)$.
- **Si $H_0$ es sobre $\sigma$**: $S_c = \sqrt{S^2_c}$ y se compara $S$ con $S_c$; $\beta$ y $n$ se trabajan con varianzas.
- **$n$ por la ecuación de García (ensayo)**: $\nu = \frac{2}{9}\left(a + \sqrt{a^2 + 1}\right)^2$ (al entero superior), $n = \nu + 1$.
  - Caso 1: $R = \sigma_1^2/\sigma_0^2$, $a = \dfrac{Z_{(1-\alpha)} + Z_{(1-\beta)} \cdot \sqrt[3]{R}}{2(\sqrt[3]{R} - 1)}$.
  - Caso 2: $R = \sigma_0^2/\sigma_1^2$ (siempre > 1), $a = \dfrac{Z_{(1-\beta)} + Z_{(1-\alpha)} \cdot \sqrt[3]{R}}{2(\sqrt[3]{R} - 1)}$.
  - $\sqrt[3]{R}$ multiplica a **un solo** $Z$. Ejemplos de clase: II-8d $n = 540$; II-12c $n = 27$.

---

### 2.5 Ensayos para la Proporción ($p$) — siempre unilaterales

- Variable: $r$ = cantidad de éxitos en $n$ (binomial). Se decide con $r$ contra $r_c$.
- **Caso 1** ($H_0: p \le p_0$): $r_c$ tal que $G_b(r_c \mid n; p_0) \le \alpha$; CR: $r \ge r_c$; $\beta = F_b(r_c - 1 \mid n; p_1)$.
- **Caso 2** ($H_0: p \ge p_0$): $r_c$ tal que $F_b(r_c \mid n; p_0) \le \alpha$; CR: $r \le r_c$; $\beta = G_b(r_c + 1 \mid n; p_1)$.
- Entre los dos valores que da el aplicativo se elige el que deja **$\alpha$ real ≤ $\alpha$**.
- **$n$ del plan**: exacto (el menor $n$ con $G \le \alpha$ y $F \le \beta$). Aproximación normal: $n = \left[\dfrac{Z_{(1-\alpha)}\sqrt{p_0q_0} + Z_{(1-\beta)}\sqrt{p_1q_1}}{p_1 - p_0}\right]^2$. Aproximación Poisson: con $R = p_1/p_0$ y $\chi^2$ (Wilson-Hilferty); si los $n$ difieren, se toma el mayor. Justificar la aproximación con los criterios de 1.3 aplicados al $n$ resultante (con $p_0$).
- "Aumento de 3 **puntos**" es 0,12 → 0,15, no 0,12·1,03.
- III-11c: exacto $n = 755$; normal $n = 715$. La guía también da 855 por Poisson: es incorrecto (el criterio se aplicó con $n = 50$).

---

## 3. UNIDAD 3: COMPARACIÓN DE DOS POBLACIONES

Sin hipótesis bilaterales en los ensayos de comparación: la muestra orienta (si $S_2 > S_1$, lo único que se puede intentar probar es $\sigma_2 > \sigma_1$). Usar letras (A/B, CR/SR) en lugar de 1/2 y respetar la relación que pide el enunciado.

---

### 3.1 Comparación de Varianzas o Desvíos

- **Parámetro**: $\psi^2 = \sigma_1^2/\sigma_2^2$ (o $\varphi = \sigma_1/\sigma_2$). **Estimador**: $J^2 = S_1^2/S_2^2$ (o $J$).
- **Distribución**: $F$ con $\nu_1 = n_1 - 1$ (**lo que está en el numerador**) y $\nu_2 = n_2 - 1$.
- **IC**: $A = \dfrac{J^2}{F_{(1-\alpha/2;\nu_1;\nu_2)}}$, $B = \dfrac{J^2}{F_{(\alpha/2;\nu_1;\nu_2)}}$; para desvíos $A' = \sqrt A$, $B' = \sqrt B$. Interpretar como aumento o reducción porcentual ("σA² como mínimo 79,65 % menor y como máximo 11,36 % mayor que σB²"). Si no dicen la relación, se elige una, se dice cuál y se resuelve solo esa.
- **$n$ con $n_1 = n_2$** (relación entre límites): se itera $\nu$ hasta que $R = F_{(1-\alpha/2;\nu;\nu)}/F_{(\alpha/2;\nu;\nu)}$ alcance el objetivo; $n = \nu + 1$. Para desvíos, $R = R'^2$. (IV-1: $\nu = 44 \Rightarrow n = 45$; $\nu = 443 \Rightarrow n = 444$.)

#### Ensayos sobre $\psi^2$ o $\varphi$
- **Caso 1** ($H_0: \psi^2 \le \psi_0^2$): $J^2_c = \psi_0^2 \cdot F_{(1-\alpha)}$; CR: $J^2 > J^2_c$; $\beta = F_F\left(\frac{\psi_0^2}{\psi_1^2} F_{(1-\alpha)}\right)$.
- **Caso 2** ($H_0: \psi^2 \ge \psi_0^2$): $J^2_c = \psi_0^2 \cdot F_{(\alpha)}$; CR: $J^2 < J^2_c$; $\beta = 1 - F_F\left(\frac{\psi_0^2}{\psi_1^2} F_{(\alpha)}\right)$.
- Con desvíos "el φ va al cuadrado": $J_c = \sqrt{\varphi_0^2 \cdot F}$, y se compara $J$ con $J_c$. "Reducir el desvío un 12 %" ⇒ $H_0: \varphi \ge 0{,}88$ (IV-4: $J_c = 0{,}3859$, $J = 0{,}3729$ ⇒ se rechaza).
- **$n$ con $n_1 = n_2$**: $R = \psi_1^2/\psi_0^2$ (caso 1) o $\psi_0^2/\psi_1^2$ (caso 2), siempre > 1. La app busca el menor $\nu$ con $R \ge F_{(1-\alpha;\nu;\nu)} \cdot F_{(1-\beta;\nu;\nu)}$, que coincide con los resultados de clase (IV-4c: $\nu = 127$, $n = 128$). El profesor lo presenta como iteración con el apunte; mostrar la iteración.

---

### 3.2 Comparación de Medias ($\Delta = \mu_1 - \mu_2$)

**Elección del método (justificarla)**:
1. $\sigma_1$ y $\sigma_2$ conocidos ⇒ $Z$ (es teórico: "jamás vas a conocer ambos").
2. Desconocidos ⇒ **test F auxiliar previo** (no es parte del problema): **unilateral**, sospechando mayor la varianza de la muestra con $S$ mayor, con **α grande propio (0,10)**, no el del problema. No se rechaza ⇒ **amalgamado**; se rechaza ⇒ **Welch**. (V-8: $J_c = \sqrt{F_{(0,90;60;20)}} = 1{,}2949$, $J = 1{,}0417$ ⇒ amalgamado.)
3. Mismo individuo o misma unidad experimental ⇒ **apareadas**. **Que los $n$ sean iguales no las hace apareadas.**

#### CASO A: Amalgamado (varianzas supuestas iguales)
- $S_a^2 = \dfrac{(n_1 - 1)S_1^2 + (n_2 - 1)S_2^2}{n_1 + n_2 - 2}$, con $\nu = n_1 + n_2 - 2$. Control: $S_a^2$ queda entre $S_1^2$ y $S_2^2$.
- **IC**: $A; B = D \pm t_{(1 - \alpha/2; \nu)} \cdot S_a\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}$. Diferencia **mínima o máxima**: un solo límite con $t_{(1-\alpha)}$.
- **Ensayo**: caso 1 ($H_0: \Delta \le \Delta_0$): $D_c = \Delta_0 + t_{(1 - \alpha; \nu)} \cdot S_a\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}$, CR: $D > D_c$. Caso 2: $D_c = \Delta_0 - \dots$, CR: $D < D_c$.

#### CASO B: Welch (varianzas probadas distintas)
- Error: $\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}$.
- $$\nu = \frac{\left( \frac{S_1^2}{n_1} + \frac{S_2^2}{n_2} \right)^2}{\frac{1}{n_1 - 1} \left( \frac{S_1^2}{n_1} \right)^2 + \frac{1}{n_2 - 1} \left( \frac{S_2^2}{n_2} \right)^2} \quad \text{truncado (124,9 → 124)}$$
- IC y ensayos como en el caso A, con este error y este $\nu$.

#### CASO C: Apareadas
- $d_i$ = diferencia en cada individuo; estimador $\bar d$, desvío $S_D$, $t$ con $\nu = n - 1$. Ej. V-12: $\bar d = 5{,}75$, $S_D = 5{,}1200$, $\bar D_c = 5{,}4295$ ⇒ se rechaza $H_0: \Delta \le 2$.

#### Diferencias porcentuales
- "$\mu_1$ supera en un 10 % a $\mu_2$" ⇒ $\Delta^* = \mu_1 - 1{,}10\,\mu_2$ (no el cociente), estimador $D^* = \bar x_1 - 1{,}10\,\bar x_2$.
- Error: $S_a\sqrt{\frac{1}{n_1} + \frac{h^2}{n_2}}$: **$h^2$ va en el término de la población que lleva $h$** (en Welch, también dentro de $\nu$).
- **Porcentaje mínimo**: $h$ no se estima; se plantea la CR como inecuación en $h$, se eleva al cuadrado, se resuelve la cuadrática y **se verifica cada raíz** en la inecuación original (V-8d: sirve 1,0490 y no 1,1906 ⇒ aumento mínimo 4,90 %).
- El estimador tiene que ser coherente con el parámetro.

**En ensayos de medias con $t$ no se calculan $\beta$ ni $n$.**

---

## 4. UNIDAD 4: CONTRASTES CHI-CUADRADO ($\chi^2$)

Se contrastan las frecuencias observadas ($O_i$) contra las esperadas ($E_i$) de un patrón.

### 4.1 Cuál prueba usar
- "Asociación" ⇒ **independencia**. "Niveles, probabilidades o porcentajes" de varios grupos ⇒ **consistencia** (la comparación de dos proporciones se ve acá). "Se ajusta a / sigue un modelo / patrón" ⇒ **bondad de ajuste**.
- No hay criterio pesimista u optimista: la $H_0$ es fija por tipo. $\alpha$, en general, 0,05.

### 4.2 Estadístico y decisión
$$\chi^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i}$$
- Siempre cola derecha: se rechaza $H_0$ si $\chi^2 > \chi^2_{(1 - \alpha; \nu)}$.
- **Ajuste demasiado perfecto**: si $\chi^2 < \chi^2_{(\alpha; \nu)}$, sospechar de los datos (no del modelo).

### 4.3 Requisitos
1. $N_{total} \ge 60$.
2. Todos los $E_i \ge 5$ (los $O_i$ pueden ser 0). Si un $E_i < 5$, **se amalgama** con la clase vecina (en los extremos o en el medio), sumando observados y esperados.
3. Los observados no se tocan. Los esperados **llevan decimales** (nunca se redondean a enteros) y las sumas tienen que cerrar.

---

### 4.4 Pruebas de Bondad de Ajuste
- **Hipótesis**: $H_0$: lo observado se ajusta al modelo X (uniforme, Poisson, patrón histórico, etc.).
- **Esperados**: $E_i = N \cdot p_i$, con las $p_i$ sumando 1.
- **Completar el dominio**: se agrega una clase al final (y/o al principio) con $O = 0$ y probabilidad **acumulada** ($G$ en la última, $F$ en la primera), no la puntual. Ej. VI-16: clase "11 o más" con $G(11) = 0{,}0011$.
- **Grados de Libertad**: $\nu = k - 1 - p$, con $k$ = **clases efectivas** (después de amalgamar o agregar) y $p$ = parámetros estimados con la muestra (Poisson con $\bar x$ ⇒ 1; uniforme o patrón histórico ⇒ 0).
- **Discretas, 3 situaciones**: se rechaza ⇒ no sigue el modelo; no se rechaza y se cumple el proceso físico ⇒ "sigue el modelo"; no se rechaza y no se cumple ⇒ "es un buen candidato".
- Bondad de ajuste a modelos continuos: al 22/10 no se dio en clase.

---

### 4.5 Tablas de Contingencia (Independencia y Consistencia)
- **$H_0$ de independencia**: en palabras ("las fallas de pintura son independientes del color").
- **$H_0$ de consistencia**: **por categoría** ($p_{1ª,M} = p_{1ª,T} = p_{1ª,N}$, y lo mismo para cada categoría), no "p mañana = p tarde".
- **Esperados**: $E_{ij} = \dfrac{(\text{Total Fila } i) \cdot (\text{Total Columna } j)}{N}$ (en consistencia es lo mismo que $\hat p$ global de la categoría × $n$ del grupo).
- **Grados de Libertad**: $\nu = (f - 1)(c - 1)$.
- **Conclusiones**: al rechazar en consistencia, "algún nivel es distinto" (no "todos"); al no rechazar independencia, "no hay evidencia suficiente para asegurar que exista asociación" (nunca se prueba la independencia).

---

## 5. ESPECIFICACIONES TÉCNICAS PARA LA ARQUITECTURA DE LA APP (SOLVER)

```
                          [ INICIO: SELECCIÓN DE TEMA ]
                                        |
      +---------------------------------+---------------------------------+
      |                                 |                                 |
[1. ESTIMACIÓN IC]             [2. ENSAYO HIPÓTESIS]           [3. COMPARACIÓN 2 POBL.]
      |                                 |                                 |
      |-- ¿Se divide por σ o por S?     |-- H0/H1 (enunciado/criterio)    |-- ¿Apareadas? -> d, S_D, t
      |   |-- σ -> Z                    |-- Cola (bilateral solo en μ)     |-- Si no: test F auxiliar
      |   +-- S -> t (nu=n-1)           |-- Valor crítico (x_c, S2_c, r_c) |   unilateral, alfa 0,10
      |-- p -> exacto (F / binomial)    |-- Estimador vs crítico          |   |-- no rechaza -> amalgamado
      |-- ¿Calcular n?                  |-- Beta y n (no con t)            |   +-- rechaza -> Welch
      |   |-- σ -> Fórmula Z            +---------------------------------+-- IC o ensayo de Δ (unilateral)
      |   |-- S -> Bucle n_iter                                             |
      |   +-- p -> aprox. + criterio                                [4. CONTRASTE CHI^2]
      |-- ¿Población N finita?                                              |-- Cuál prueba
          +-- Aplicar factor finitud                                        |-- E_i con decimales
                                                                            |-- Completar dominio (F/G)
                                                                            |-- Amalgamar si E_i < 5
                                                                            |-- nu = clases efectivas - 1 - p
                                                                            |-- chi^2 vs chi^2(1-alfa; nu)
```

### Reglas de Carga de Parámetros para la App
1. **Redondeos** ("lógicos, no matemáticos"):
   - Muestras ($n$) y $\nu$ de García: **siempre hacia arriba**.
   - $\nu$ de Welch: **truncar**.
   - Límites de IC: inferior hacia abajo, superior hacia arriba.
   - Discretas: el $r_c$ que deja $\alpha$ real ≤ $\alpha$.
2. **Expresión Formal de Resultados**:
   - Intervalos: `$P(A \le \text{Parámetro} \le B) = 1 - \alpha$`.
   - Ensayos: comparar el estimador contra el valor crítico y concluir: *"Como $\bar{x} = \dots$ es mayor que $\bar{x}_c = \dots$, se rechaza $H_0$: puedo asegurar que…"* / *"…no se rechaza $H_0$: no hay evidencia suficiente para asegurar que…"*.
   - Probabilidades entre 0 y 1, nunca en %.
3. **p-value**: si se muestra, solo como dato informativo, nunca en la decisión.
