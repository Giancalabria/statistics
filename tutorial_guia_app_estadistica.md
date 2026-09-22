# 📚 MANUAL Y TUTORIAL DE RESOLUCIÓN PASO A PASO

## Estadística Aplicada - Guía de Soporte para Solver App (Primer Parcial)

---

## 📌 ÍNDICE DE MÓDULOS

1. [MÓDULO I: Inferencia sobre la Media Poblacional (μ)](#módulo-i-inferencia-sobre-la-media-poblacional-μ)
   - 1.1 Intervalo de Confianza para μ con σ Conocido (Normal Z)
   - 1.2 Intervalo de Confianza para μ con σ Desconocido (t de Student)
   - 1.3 Estimación del Total Poblacional (T = N · μ)
   - 1.4 Tamaño de Muestra (n) para la Media (Método Directo e Iterativo)
   - 1.5 Ensayos de Hipótesis para la Media (μ)
   - 1.6 Cálculo de Error Tipo II (β) y Potencia (1 - β) para la Media
   - 1.7 Tamaño de Muestra para Potencia Deseada en Ensayos de Hipótesis

2. [MÓDULO II: Inferencia sobre la Varianza (σ²) y Desvío Estándar (σ)](#módulo-ii-inferencia-sobre-la-varianza-σ²-y-desvío-estándar-σ)
   - 2.1 Intervalo de Confianza para Varianza (σ²) y Desvío (σ) con Chi-Cuadrado (χ²)
     - Tamaño de muestra (n) por relación entre límites — Ecuación de García
   - 2.2 Ensayos de Hipótesis para Varianza Poblacional (σ²)
   - 2.3 Cálculo de Error Tipo II (β) en Ensayos de Varianza

3. [MÓDULO III: Inferencia sobre Proporciones Poblacionales (p)](#módulo-iii-inferencia-sobre-proporciones-poblacionales-p)
   - 3.1 Intervalo de Confianza Exacto para Proporción (p) mediante Distribución F
   - 3.2 Tamaño de Muestra (n) para Proporción Poblacional

4. [MATRIZ DE DECISIÓN: α, 1-α, β y 1-β](#matriz-de-decisión-α-1-α-β-y-1-β)

5. [TABLA MASTER DE VALORES INTERMEDIOS PARA EXÁMENES](#tabla-master-de-valores-intermedios-para-exámenes)

---

# MÓDULO I: Inferencia sobre la Media Poblacional (μ)

---

## 1.1 Intervalo de Confianza para μ con σ Conocido (Normal Z)

### 🎯 ¿Cuándo se utiliza?

Cuando se quiere estimar el promedio real de toda la población ($\mu$) a partir de una muestra aleatoria de tamaño $n$, y **se conoce el desvío estándar poblacional ($\sigma$)** (por datos históricos, especificaciones de la máquina o procesos estables).

### 📋 Datos de entrada necesarios:

- Tamaño de muestra ($n$)
- Media muestral ($\bar{x}$)
- Desvío estándar poblacional ($\sigma$)
- Nivel de confianza ($1 - \alpha$) (ej: $95\% \implies 1-\alpha = 0,95 \implies \alpha = 0,05$)

### ⚙️ Valores Intermedios que suele pedir el examen:

1. **Riesgo por cola ($\alpha/2$)**: $\frac{\alpha}{2}$
2. **Área acumulada a la izquierda**: $1 - \frac{\alpha}{2}$ (ej: $0,975$ para $95\%$)
3. **Fractil / Valor crítico $Z$**: $Z_{(1-\alpha/2)}$ (obtenido de la Normal Estándar $\mu=0, \sigma=1$)
4. **Error estándar de la media (Desvío del promedio)**: $\sigma_{\bar{x}} = \frac{\sigma}{\sqrt{n}}$
5. **Error Muestral / Semi-amplitud del intervalo ($e$)**: $e = Z_{(1-\alpha/2)} \cdot \frac{\sigma}{\sqrt{n}}$

### 📐 Fórmulas del Intervalo:

$$A = \bar{x} - e = \bar{x} - Z_{(1-\alpha/2)} \cdot \frac{\sigma}{\sqrt{n}}$$
$$B = \bar{x} + e = \bar{x} + Z_{(1-\alpha/2)} \cdot \frac{\sigma}{\sqrt{n}}$$

### ✍️ Formato de Respuesta Formal:

$$P(A \le \mu \le B) = 1 - \alpha$$
_"Se estima con un $(1-\alpha)\%$ de confianza que la media poblacional real ($\mu$) se encuentra entre $A$ y $B$ [unidades]."_

---

## 1.2 Intervalo de Confianza para μ con σ Desconocido (t de Student)

### 🎯 ¿Cuándo se utiliza?

Cuando **no se conoce $\sigma$** y se debe estimar la dispersión utilizando el **desvío estándar de la muestra ($S$)** o la cuasivarianza muestral ($S^2$).

### 📋 Datos de entrada necesarios:

- Tamaño de muestra ($n$)
- Media muestral ($\bar{x}$)
- Desvío estándar muestral ($S$) [Si te dan datos crudos $x_i$, $S = \sqrt{\frac{\sum (x_i - \bar{x})^2}{n-1}}$]
- Nivel de confianza ($1 - \alpha$)

### ⚙️ Valores Intermedios que suele pedir el examen:

1. **Grados de Libertad ($\nu$)**: $\nu = n - 1$
2. **Error estándar del promedio muestral**: $S_{\bar{x}} = \frac{S}{\sqrt{n}}$
3. **Fractil / Valor crítico $t$**: $t_{(1-\alpha/2; \; \nu=n-1)}$ (obtenido de la distribución $t$ con $\nu$ grados de libertad)
4. **Error Muestral ($e$)**: $e = t_{(1-\alpha/2; \; \nu=n-1)} \cdot \frac{S}{\sqrt{n}}$

### 📐 Fórmulas del Intervalo:

$$A = \bar{x} - t_{(1-\alpha/2; \; \nu=n-1)} \cdot \frac{S}{\sqrt{n}}$$
$$B = \bar{x} + t_{(1-\alpha/2; \; \nu=n-1)} \cdot \frac{S}{\sqrt{n}}$$

---

## 1.3 Estimación del Total Poblacional (T = N · μ)

### 🎯 ¿Cuándo se utiliza?

Cuando el problema no pide la media por unidad (ej. peso promedio de un fardo), sino el **total acumulado de toda la producción** o lote de tamaño $N$ conocido (ej. peso total de $N = 500$ fardos).

### 📐 Fórmulas del Total:

- **Punto medio (Estimador del Total)**: $\hat{T} = N \cdot \bar{x}$
- **Límite Inferior del Total**: $A_T = N \cdot A$
- **Límite Superior del Total**: $B_T = N \cdot B$
- **Error Muestral del Total ($e_T$)**: $e_T = N \cdot e$

### ✍️ Formato de Respuesta Formal:

$$P(A_T \le T \le B_T) = 1 - \alpha$$

---

## 1.4 Tamaño de Muestra (n) para la Media

### CASO A: Con σ Conocido (Método Directo)

Fórmula directa:
$$n_{\text{teórico}} = \left[ \frac{Z_{(1-\alpha/2)} \cdot \sigma}{e} \right]^2$$

1. **Redondeo obligatorio**: $n_{\text{total}} = \lceil n_{\text{teórico}} \rceil$ (siempre al entero superior).
2. **Muestra adicional a medir**: $\Delta n = n_{\text{total}} - n_{\text{preliminar}}$.

### CASO B: Con σ Desconocido (Método Iterativo)

Se utiliza la fórmula $n = \left[ \frac{t_{(1-\alpha/2; \; \nu=n-1)} \cdot S}{e} \right]^2$. Como $t$ depende de $\nu = n-1$, se resuelve por iteraciones:

1. **Paso 1**: Proponer un supuesto inicial $n_0$ (mayor a la muestra preliminar).
2. **Paso 2**: Obtener $t_0 = t_{(1-\alpha/2; \; \nu = n_0 - 1)}$.
3. **Paso 3**: Calcular $n_1 = \lceil \left( \frac{t_0 \cdot S}{e} \right)^2 \rceil$.
4. **Paso 4**: Si $n_1 \ne n_0$, repetir usando $n_1$ como nuevo supuesto hasta que $n_{k+1} = n_k$.
5. **Muestra adicional**: $\Delta n = n_{\text{final}} - n_{\text{preliminar}}$.

### CASO C: Ajuste por Población Finita (N conocido)

Si la población $N$ es conocida, primero se calcula $n_{\infty}$ (por método directo o iterativo) y luego se aplica la corrección:
$$n_{\text{finito}} = \left\lceil \frac{N \cdot n_{\infty}}{N + n_{\infty}} \right\rceil$$

---

## 1.5 Ensayos de Hipótesis para la Media (μ)

### 📋 Estructura de Planteos ($H_0$ vs $H_1$):

| Tipo de Ensayo                | Hipótesis Nula ($H_0$) | Hipótesis Alternativa ($H_1$) |
| :---------------------------- | :--------------------- | :---------------------------- |
| **Unilateral Cola Izquierda** | $H_0: \mu \ge \mu_0$   | $H_1: \mu < \mu_0$            |
| **Bilateral (2 Colas)**       | $H_0: \mu = \mu_0$     | $H_1: \mu \ne \mu_0$          |

### ⚙️ Valores Intermedios y Cálculo de Valores Críticos ($\bar{x}_c$):

#### Con σ Conocido (Normal Z):

- **Cola Izquierda**: $\bar{x}_c = \mu_0 - Z_{(1-\alpha)} \cdot \frac{\sigma}{\sqrt{n}}$
- **Cola Derecha**: $\bar{x}_c = \mu_0 + Z_{(1-\alpha)} \cdot \frac{\sigma}{\sqrt{n}}$
- **Bilateral**: $\bar{x}_{c1} = \mu_0 - Z_{(1-\alpha/2)} \cdot \frac{\sigma}{\sqrt{n}}$, $\quad \bar{x}_{c2} = \mu_0 + Z_{(1-\alpha/2)} \cdot \frac{\sigma}{\sqrt{n}}$

#### Con σ Desconocido (t de Student):

Reemplazar $Z$ por $t_{(1-\alpha; \; \nu=n-1)}$ y $\sigma$ por $S$.

### 📊 Estadístico de Prueba Calculado (si se evalúa por valor estandarizado):

$$Z_{\text{calc}} = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}} \quad \text{o} \quad t_{\text{calc}} = \frac{\bar{x} - \mu_0}{S / \sqrt{n}}$$

### 📝 Regla de Decisión (RD) para Exámenes:

_"Se toma una muestra de $n$ unidades y se calcula su media $\bar{x}$. Si $\bar{x} < \bar{x}_c$ [o la condición según el ensayo], se rechaza $H_0$ con un nivel de significación del $\alpha\%$. En caso contrario, no se rechaza $H_0$."_

---

## 1.6 Cálculo de Error Tipo II (β) y Potencia (1 - β) para la Media

### 🎯 ¿Qué representa?

- **$\beta$**: Probabilidad de **no rechazar $H_0$ cuando es falsa** (cometer un error al no detectar una verdadera media alternativa $\mu_1$).
- **Potencia ($1 - \beta$)**: Probabilidad de **hacer justicia** (rechazar $H_0$ exitosamente cuando la media real cambió a $\mu_1$).

### ⚙️ Algoritmo de Cálculo de β (Unilateral Cola Izquierda):

1. Obtener el valor crítico físico de la variable: $\bar{x}_c$.
2. Asumir que la verdadera media poblacional es $\mu_1$.
3. Estandarizar el valor crítico bajo la nueva hipótesis real $\mu_1$:
   $$Z_\beta = \frac{\bar{x}_c - \mu_1}{\sigma / \sqrt{n}}$$
4. Calcular $\beta = P(Z > Z_\beta) = 1 - \Phi(Z_\beta)$.
5. Calcular la Potencia: $W = 1 - \beta$.

---

## 1.7 Tamaño de Muestra para Potencia Deseada en Ensayos de Hipótesis

Para garantizar un riesgo $\alpha$ y simultáneamente una potencia $1-\beta$ al detectar una diferencia $|\mu_0 - \mu_1|$:

$$n = \left[ \frac{(Z_{(1-\alpha)} + Z_{(1-\beta)}) \cdot \sigma}{\mu_0 - \mu_1} \right]^2$$

Redondear siempre hacia arriba: $n_{\text{total}} = \lceil n \rceil$.

---

# MÓDULO II: Inferencia sobre la Varianza (σ²) y Desvío Estándar (σ)

---

## 2.1 Intervalo de Confianza para Varianza (σ²) y Desvío (σ) con Chi-Cuadrado (χ²)

### 🎯 ¿Cuándo se utiliza?

Para estimar la dispersión o variabilidad poblacional ($\sigma^2$ o $\sigma$) en un proceso de fabricación o medición.

### 📋 Datos de entrada necesarios:

- Tamaño de muestra ($n$)
- Varianza muestral ($S^2$) o desvío muestral ($S$)
- Nivel de confianza ($1 - \alpha$)

### ⚙️ Valores Intermedios que suele pedir el examen:

1. **Grados de libertad ($D$ o $\nu$)**: $D = \nu = n - 1$
2. **Suma de Cuadrados de Desviaciones (Numerador de la Varianza)**:
   $$\text{Suma de Cuadrados} = (n - 1) \cdot S^2 = D \cdot S^2 = \sum (x_i - \bar{x})^2$$
3. **Fractil Chi-Cuadrado Inferior**: $\chi^2_{(\alpha/2; \; \nu)}$ (área $\alpha/2$ a la izquierda)
4. **Fractil Chi-Cuadrado Superior**: $\chi^2_{(1-\alpha/2; \; \nu)}$ (área $1-\alpha/2$ a la izquierda)

### 📐 Fórmulas del Intervalo para la Varianza (σ²):

$$A_{\sigma^2} = \frac{(n-1) \cdot S^2}{\chi^2_{(1-\alpha/2; \; \nu)}}$$
$$B_{\sigma^2} = \frac{(n-1) \cdot S^2}{\chi^2_{(\alpha/2; \; \nu)}}$$

_(Nota de oro: El denominador de $A$ lleva el fractil más grande $\chi^2_{(1-\alpha/2)}$ porque al dividir por un número mayor da un límite inferior más chico).\_

### 📐 Fórmulas del Intervalo para el Desvío Estándar (σ):

$$A_\sigma = \sqrt{A_{\sigma^2}}, \quad B_\sigma = \sqrt{B_{\sigma^2}}$$

### 📐 Tamaño de muestra (n) para σ² / σ — Ecuación de García

En χ² el intervalo es **asimétrico**, así que la precisión no se mide restando límites (no hay un
$\pm e$ como en la media) sino con el **cociente** entre ellos:

$$R' = \frac{B_\sigma}{A_\sigma} \qquad R = (R')^2 = \frac{B_{\sigma^2}}{A_{\sigma^2}}$$

Si el enunciado pide **disminuir un $k\%$** la relación anterior, la nueva conserva $(1-k)$ de la
original: $R'_{obj} = R'_{orig} \cdot (1 - k)$.

Invirtiendo la aproximación de Wilson–Hilferty se llega al $\nu$ buscado sin tantear la tabla de χ²:

$$a = \frac{Z_{(1-\alpha/2)} \cdot \left(\sqrt[3]{R} + 1\right)}{2 \cdot \left(\sqrt[3]{R} - 1\right)}
\qquad \nu = \frac{2}{9}\left(a + \sqrt{a^2 + 1}\right)^2 \qquad n = \lceil \nu + 1 \rceil$$

⚠️ El radical de $R$ es **cúbico**, no cuadrado (sale del cubo de Wilson–Hilferty). Equivale a
$(R')^{2/3}$. Varios apuntes lo escriben como $\sqrt{R}$ pero después calculan la raíz cúbica.

Si ya hay una muestra preliminar: $\Delta n = n - n_{prelim}$.

**Ejemplo (TEMA II, problema 7b)**: del inciso a salen $A' = 159{,}70$ y $B' = 306{,}73$ con
$n = 20$, o sea $R'_{orig} = 1{,}9207$. Pedir un 30% menos da $R'_{obj} = 1{,}3445$,
$R = 1{,}8076$, $\sqrt[3]{R} = 1{,}2181$, $a = 9{,}9646$, $\nu = 88{,}70$ y
$n = 90$ supermercados → $\Delta n = 70$ adicionales.

**En la app**: `Intervalos de Confianza` → `Varianza / Desvío` → `Tamaño de muestra (n)`.

---

## 2.2 Ensayos de Hipótesis para Varianza Poblacional (σ²)

### 📋 Planteo para Ensayo Unilateral Cola Derecha (Verificar exceso de variabilidad):

- $H_0: \sigma^2 \le \sigma_0^2$
- $H_1: \sigma^2 > \sigma_0^2$

### ⚙️ Valores Intermedios:

1. **Valor Crítico Chi-Cuadrado**: $\chi^2_c = \chi^2_{(1-\alpha; \; \nu = n-1)}$
2. **Varianza Muestral Crítica ($S_c^2$)**:
   $$S_c^2 = \frac{\sigma_0^2 \cdot \chi^2_c}{n - 1}$$
3. **Estadístico de prueba calculado**:
   $$\chi^2_{\text{calc}} = \frac{(n - 1) \cdot S^2}{\sigma_0^2}$$

### 📝 Condición de Rechazo:

Rechazar $H_0$ si $S^2 > S_c^2$ (o equivalentemente si $\chi^2_{\text{calc}} > \chi^2_c$).

---

## 2.3 Cálculo de Error Tipo II (β) en Ensayos de Varianza

Si la verdadera varianza poblacional cambió a $\sigma_1^2$:

1. Calcular el valor crítico del test: $S_c^2$.
2. Calcular el valor de Chi-Cuadrado equivalente bajo $\sigma_1^2$:
   $$\chi^2_\beta = \frac{(n - 1) \cdot S_c^2}{\sigma_1^2}$$
3. Obtené $\beta = P(\chi^2 \le \chi^2_\beta)$ con la función acumulada de $\chi^2$ con $\nu = n-1$.

---

# MÓDULO III: Inferencia sobre Proporciones Poblacionales (p)

---

## 3.1 Intervalo de Confianza Exacto para Proporción (p) mediante Distribución F

### ⚠️ ¡ADVERTENCIA DE CÁTEDRA!

**Jamás utilizar la aproximación Normal** $p \pm Z \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$ para muestras pequeñas o cuando $r=0$. Se debe utilizar la fórmula exacta Clopper-Pearson basada en la distribución $F$ de Fisher-Snedecor.

### 📋 Datos de entrada:

- Tamaño de muestra ($n$)
- Cantidad de éxitos / defectuosos registrados ($r$)
- Nivel de confianza ($1 - \alpha$)

### ⚙️ Valores Intermedios:

- **Proporción muestral (Estimador puntual)**: $\hat{p} = \frac{r}{n}$

---

### 📐 Fórmulas Exactas (Clopper-Pearson via F):

#### CASO GENERAL ($0 < r < n$):

- **Límite Inferior ($A$)**:
  $$A = \frac{1}{1 + \left(\frac{n - r + 1}{r}\right) \cdot F_{(1-\alpha/2; \; \nu_n = 2(n-r+1); \; \nu_d = 2r)}}$$
- **Límite Superior ($B$)**:
  $$B = \frac{1}{1 + \frac{n - r}{(r + 1) \cdot F_{(1-\alpha/2; \; \nu_n = 2r + 2; \; \nu_d = 2n - 2r)}}}$$

#### CASO ESPECIAL 1: Cero éxitos ($r = 0$):

- $A = 0$
- $B = \frac{1}{1 + \frac{n}{F_{(1-\alpha/2; \; \nu_n = 2; \; \nu_d = 2n)}}}$

#### CASO ESPECIAL 2: Todos éxitos ($r = n$):

- $A = \frac{1}{1 + \frac{1}{n \cdot F_{(1-\alpha/2; \; \nu_n = 2n; \; \nu_d = 2)}}}$
- $B = 1$

---

## 3.2 Tamaño de Muestra (n) para Proporción Poblacional

Para lograr un Error Muestral deseado $e_{\text{objetivo}}$:

### Fórmula con $\hat{p}$ preliminar conocida:

$$n_{\text{teórico}} = \left[ \frac{Z_{(1-\alpha/2)}}{e_{\text{objetivo}}} \right]^2 \cdot \hat{p} \cdot (1 - \hat{p})$$

### Fórmula sin información previa (Máxima Incertidumbre $\hat{p} = 0,5$):

$$n_{\text{teórico}} = \left[ \frac{Z_{(1-\alpha/2)}}{e_{\text{objetivo}}} \right]^2 \cdot 0,25$$

1. **Redondeo obligatorio**: $n_{\text{total}} = \lceil n_{\text{teórico}} \rceil$.
2. **Muestra adicional**: $\Delta n = n_{\text{total}} - n_{\text{preliminar}}$.

---

# MATRIZ DE DECISIÓN: α, 1-α, β y 1-β

---

## 4.1 La matriz de los cuatro resultados posibles

En todo ensayo de hipótesis hay **dos realidades posibles** (que $H_0$ sea verdadera o falsa) y **dos decisiones posibles** (rechazar o no rechazar $H_0$). El cruce da cuatro casilleros, dos correctos y dos erróneos:

|                            | **Realidad: $H_0$ es VERDADERA**                                       | **Realidad: $H_0$ es FALSA (vale $H_1$)**                    |
| :------------------------- | :--------------------------------------------------------------------- | :----------------------------------------------------------- |
| **No se rechaza $H_0$**    | ✅ Decisión correcta<br>$1 - \alpha$ = **Nivel de confianza**           | ❌ **Error de Tipo II**<br>$\beta$ = riesgo del comprador     |
| **Se rechaza $H_0$**       | ❌ **Error de Tipo I**<br>$\alpha$ = **Nivel de significación**         | ✅ Decisión correcta<br>$1 - \beta$ = **Potencia del ensayo** |

Las probabilidades se leen **por columna** (condicionadas a la realidad), no por fila:

$$\alpha + (1 - \alpha) = 1 \quad \text{(columna } H_0 \text{ verdadera)}$$
$$\beta + (1 - \beta) = 1 \quad \text{(columna } H_0 \text{ falsa)}$$

⚠️ **Error típico de examen**: creer que $\alpha + \beta = 1$. Es **falso**: pertenecen a columnas distintas (escenarios distintos de la realidad).

---

## 4.2 Qué significa cada valor

| Símbolo      | Nombre                                    | Definición formal                             | Lectura en criollo                                                       |
| :----------- | :---------------------------------------- | :-------------------------------------------- | :----------------------------------------------------------------------- |
| $\alpha$     | Error Tipo I / Nivel de significación     | $P(\text{rechazar } H_0 \mid H_0 \text{ V})$   | Condenar a un inocente: rechazo $H_0$ siendo verdadera. Lo **fijo yo**.   |
| $1 - \alpha$ | Nivel de confianza                        | $P(\text{no rechazar } H_0 \mid H_0 \text{ V})$ | Absolver a un inocente: acierto cuando $H_0$ es verdadera.               |
| $\beta$      | Error Tipo II                             | $P(\text{no rechazar } H_0 \mid H_0 \text{ F})$ | Absolver a un culpable: no detecto el cambio real a $\mu_1$ / $\sigma_1$. |
| $1 - \beta$  | Potencia del ensayo ($W$)                 | $P(\text{rechazar } H_0 \mid H_0 \text{ F})$   | Condenar a un culpable: detecto correctamente el cambio real.            |

### 🔑 Puntos clave para el parcial

1. $\alpha$ es un **dato del enunciado** (lo fija quien diseña el ensayo); $\beta$ es un **resultado calculado** y solo existe si se especifica un valor alternativo concreto ($\mu_1$, $\sigma_1^2$, $p_1$).
2. $\beta$ **no es único**: hay un $\beta$ distinto para cada $\mu_1$ posible. Cuanto más lejos esté $\mu_1$ de $\mu_0$, más chico es $\beta$ y mayor la potencia.
3. Con $n$ fijo, $\alpha$ y $\beta$ se mueven **en sentido contrario**: bajar $\alpha$ (ser más exigente para rechazar) agranda la zona de no rechazo y por lo tanto **sube** $\beta$.
4. La única forma de bajar $\alpha$ y $\beta$ al mismo tiempo es **aumentar $n$** (ver 1.7: $n = \left[\frac{(Z_{(1-\alpha)} + Z_{(1-\beta)}) \cdot \sigma}{\mu_0 - \mu_1}\right]^2$).
5. Nunca se "acepta" $H_0$: se **no rechaza**, porque el riesgo $\beta$ de esa decisión no está controlado.

---

# TABLA MASTER DE VALORES INTERMEDIOS PARA EXÁMENES

Si un ejercicio de examen te pide reportar valores intermedios durante el desarrollo, consulta esta tabla rápida:

| Tema / Problema        | Valor Intermedio Solicitado    | Nombre / Notación        | Fórmula de Cálculo                                   |
| :--------------------- | :----------------------------- | :----------------------- | :--------------------------------------------------- |
| **Media con Z**        | Error estándar de la media     | $\sigma_{\bar{x}}$       | $\sigma / \sqrt{n}$                                  |
| **Media con Z**        | Semi-amplitud / Error muestral | $e$                      | $Z_{(1-\alpha/2)} \cdot (\sigma / \sqrt{n})$         |
| **Media con t**        | Grados de libertad             | $\nu$                    | $n - 1$                                              |
| **Media con t**        | Desvío muestral del promedio   | $S_{\bar{x}}$            | $S / \sqrt{n}$                                       |
| **Media (Total)**      | Estimador del Total            | $\hat{T}$                | $N \cdot \bar{x}$                                    |
| **Ensayo Media**       | Valor Crítico Físico           | $\bar{x}_c$              | $\mu_0 \pm Z_{(1-\alpha)} \cdot (\sigma / \sqrt{n})$ |
| **Ensayo Media**       | Z de Error Tipo II             | $Z_\beta$                | $(\bar{x}_c - \mu_1) / (\sigma / \sqrt{n})$          |
| **Varianza χ²**        | Suma de cuadrados de desvíos   | $\sum (x_i - \bar{x})^2$ | $(n - 1) \cdot S^2 = D \cdot S^2$                    |
| **Varianza χ²**        | Fractil Chi-Cuadrado Inferior  | $\chi^2_{\text{inf}}$    | $\chi^2_{(1-\alpha/2; \; \nu)}$                      |
| **Varianza χ²**        | Fractil Chi-Cuadrado Superior  | $\chi^2_{\text{sup}}$    | $\chi^2_{(\alpha/2; \; \nu)}$                        |
| **Proporción F**       | Grados de libertad Num/Den (A) | $\nu_n, \nu_d$           | $\nu_n = 2(n-r+1), \quad \nu_d = 2r$                 |
| **Proporción F**       | Grados de libertad Num/Den (B) | $\nu_n, \nu_d$           | $\nu_n = 2r+2, \quad \nu_d = 2n-2r$                  |
| **Tamaños de Muestra** | Unidades adicionales a medir   | $\Delta n$               | $n_{\text{total}} - n_{\text{preliminar}}$           |

---
