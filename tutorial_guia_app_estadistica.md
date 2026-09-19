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
   - 2.2 Ensayos de Hipótesis para Varianza Poblacional (σ²)
   - 2.3 Cálculo de Error Tipo II (β) en Ensayos de Varianza

3. [MÓDULO III: Inferencia sobre Proporciones Poblacionales (p)](#módulo-iii-inferencia-sobre-proporciones-poblacionales-p)
   - 3.1 Intervalo de Confianza Exacto para Proporción (p) mediante Distribución F
   - 3.2 Tamaño de Muestra (n) para Proporción Poblacional

4. [TABLA MASTER DE VALORES INTERMEDIOS PARA EXÁMENES](#tabla-master-de-valores-intermedios-para-exámenes)

---

# MÓDULO I: Inferencia sobre la Media Poblacional (μ)

---

## 1.1 Intervalo de Confianza para μ con σ Conocido (Normal Z)

### 🎯 ¿Cuándo se utiliza?
Cuando se quiere estimar el promedio real de toda la población ($\mu$) a partir de una muestra aleatoria de tamaño $n$, y **se conoce el desvío estándar poblacional ($\sigma$)** (por datos históricos, especificaciones de la máquina o procesos estables).

### 📋 Datos de entrada necesarios:
- Tamaño de muestra ($n$)
- Media muestral ($ar{x}$)
- Desvío estándar poblacional ($\sigma$)
- Nivel de confianza ($1 - lpha$) (ej: $95\% \implies 1-lpha = 0,95 \implies lpha = 0,05$)

### ⚙️ Valores Intermedios que suele pedir el examen:
1. **Riesgo por cola ($lpha/2$)**: $rac{lpha}{2}$
2. **Área acumulada a la izquierda**: $1 - rac{lpha}{2}$ (ej: $0,975$ para $95\%$)
3. **Fractil / Valor crítico $Z$**: $Z_{(1-lpha/2)}$ (obtenido de la Normal Estándar $\mu=0, \sigma=1$)
4. **Error estándar de la media (Desvío del promedio)**: $\sigma_{ar{x}} = rac{\sigma}{\sqrt{n}}$
5. **Error Muestral / Semi-amplitud del intervalo ($e$)**: $e = Z_{(1-lpha/2)} \cdot rac{\sigma}{\sqrt{n}}$

### 📐 Fórmulas del Intervalo:
$$A = ar{x} - e = ar{x} - Z_{(1-lpha/2)} \cdot rac{\sigma}{\sqrt{n}}$$
$$B = ar{x} + e = ar{x} + Z_{(1-lpha/2)} \cdot rac{\sigma}{\sqrt{n}}$$

### ✍️ Formato de Respuesta Formal:
$$P(A \le \mu \le B) = 1 - lpha$$
*"Se estima con un $(1-lpha)\%$ de confianza que la media poblacional real ($\mu$) se encuentra entre $A$ y $B$ [unidades]."*

---

## 1.2 Intervalo de Confianza para μ con σ Desconocido (t de Student)

### 🎯 ¿Cuándo se utiliza?
Cuando **no se conoce $\sigma$** y se debe estimar la dispersión utilizando el **desvío estándar de la muestra ($S$)** o la cuasivarianza muestral ($S^2$).

### 📋 Datos de entrada necesarios:
- Tamaño de muestra ($n$)
- Media muestral ($ar{x}$)
- Desvío estándar muestral ($S$) [Si te dan datos crudos $x_i$, $S = \sqrt{rac{\sum (x_i - ar{x})^2}{n-1}}$]
- Nivel de confianza ($1 - lpha$)

### ⚙️ Valores Intermedios que suele pedir el examen:
1. **Grados de Libertad ($
u$)**: $
u = n - 1$
2. **Error estándar del promedio muestral**: $S_{ar{x}} = rac{S}{\sqrt{n}}$
3. **Fractil / Valor crítico $t$**: $t_{(1-lpha/2; \; 
u=n-1)}$ (obtenido de la distribución $t$ con $
u$ grados de libertad)
4. **Error Muestral ($e$)**: $e = t_{(1-lpha/2; \; 
u=n-1)} \cdot rac{S}{\sqrt{n}}$

### 📐 Fórmulas del Intervalo:
$$A = ar{x} - t_{(1-lpha/2; \; 
u=n-1)} \cdot rac{S}{\sqrt{n}}$$
$$B = ar{x} + t_{(1-lpha/2; \; 
u=n-1)} \cdot rac{S}{\sqrt{n}}$$

---

## 1.3 Estimación del Total Poblacional (T = N · μ)

### 🎯 ¿Cuándo se utiliza?
Cuando el problema no pide la media por unidad (ej. peso promedio de un fardo), sino el **total acumulado de toda la producción** o lote de tamaño $N$ conocido (ej. peso total de $N = 500$ fardos).

### 📐 Fórmulas del Total:
- **Punto medio (Estimador del Total)**: $\hat{T} = N \cdot ar{x}$
- **Límite Inferior del Total**: $A_T = N \cdot A$
- **Límite Superior del Total**: $B_T = N \cdot B$
- **Error Muestral del Total ($e_T$)**: $e_T = N \cdot e$

### ✍️ Formato de Respuesta Formal:
$$P(A_T \le T \le B_T) = 1 - lpha$$

---

## 1.4 Tamaño de Muestra (n) para la Media

### CASO A: Con σ Conocido (Método Directo)
Fórmula directa:
$$n_{	ext{teórico}} = \left[ rac{Z_{(1-lpha/2)} \cdot \sigma}{e} ight]^2$$

1. **Redondeo obligatorio**: $n_{	ext{total}} = \lceil n_{	ext{teórico}} ceil$ (siempre al entero superior).
2. **Muestra adicional a medir**: $\Delta n = n_{	ext{total}} - n_{	ext{preliminar}}$.

### CASO B: Con σ Desconocido (Método Iterativo)
Se utiliza la fórmula $n = \left[ rac{t_{(1-lpha/2; \; 
u=n-1)} \cdot S}{e} ight]^2$. Como $t$ depende de $
u = n-1$, se resuelve por iteraciones:

1. **Paso 1**: Proponer un supuesto inicial $n_0$ (mayor a la muestra preliminar).
2. **Paso 2**: Obtener $t_0 = t_{(1-lpha/2; \; 
u = n_0 - 1)}$.
3. **Paso 3**: Calcular $n_1 = \lceil \left( rac{t_0 \cdot S}{e} ight)^2 ceil$.
4. **Paso 4**: Si $n_1 
e n_0$, repetir usando $n_1$ como nuevo supuesto hasta que $n_{k+1} = n_k$.
5. **Muestra adicional**: $\Delta n = n_{	ext{final}} - n_{	ext{preliminar}}$.

### CASO C: Ajuste por Población Finita (N conocido)
Si la población $N$ es conocida, primero se calcula $n_{\infty}$ (por método directo o iterativo) y luego se aplica la corrección:
$$n_{	ext{finito}} = \left\lceil rac{N \cdot n_{\infty}}{N + n_{\infty}} ightceil$$

---

## 1.5 Ensayos de Hipótesis para la Media (μ)

### 📋 Estructura de Planteos ($H_0$ vs $H_1$):

| Tipo de Ensayo | Hipótesis Nula ($H_0$) | Hipótesis Alternativa ($H_1$) | Criterio / Uso típico |
| :--- | :--- | :--- | :--- |
| **Unilateral Cola Izquierda** | $H_0: \mu \ge \mu_0$ | $H_1: \mu < \mu_0$ | **Pesimista**: Demostrar mejoras o reducción de consumo/costos. |
| **Unilateral Cola Derecha** | $H_0: \mu \le \mu_0$ | $H_1: \mu > \mu_0$ | **Optimista**: Control de recepción, verificar si supera un límite. |
| **Bilateral (2 Colas)** | $H_0: \mu = \mu_0$ | $H_1: \mu 
e \mu_0$ | **Control de Proceso / Calibración**: Detectar cualquier desvío. |

### ⚙️ Valores Intermedios y Cálculo de Valores Críticos ($ar{x}_c$):

#### Con σ Conocido (Normal Z):
- **Cola Izquierda**: $ar{x}_c = \mu_0 - Z_{(1-lpha)} \cdot rac{\sigma}{\sqrt{n}}$
- **Cola Derecha**: $ar{x}_c = \mu_0 + Z_{(1-lpha)} \cdot rac{\sigma}{\sqrt{n}}$
- **Bilateral**: $ar{x}_{c1} = \mu_0 - Z_{(1-lpha/2)} \cdot rac{\sigma}{\sqrt{n}}$, $\quad ar{x}_{c2} = \mu_0 + Z_{(1-lpha/2)} \cdot rac{\sigma}{\sqrt{n}}$

#### Con σ Desconocido (t de Student):
Reemplazar $Z$ por $t_{(1-lpha; \; 
u=n-1)}$ y $\sigma$ por $S$.

### 📊 Estadístico de Prueba Calculado (si se evalúa por valor estandarizado):
$$Z_{	ext{calc}} = rac{ar{x} - \mu_0}{\sigma / \sqrt{n}} \quad 	ext{o} \quad t_{	ext{calc}} = rac{ar{x} - \mu_0}{S / \sqrt{n}}$$

### 📝 Regla de Decisión (RD) para Exámenes:
*"Se toma una muestra de $n$ unidades y se calcula su media $ar{x}$. Si $ar{x} < ar{x}_c$ [o la condición según el ensayo], se rechaza $H_0$ con un nivel de significación del $lpha\%$. En caso contrario, no se rechaza $H_0$."*

---

## 1.6 Cálculo de Error Tipo II (β) y Potencia (1 - β) para la Media

### 🎯 ¿Qué representa?
- **$eta$**: Probabilidad de **no rechazar $H_0$ cuando es falsa** (cometer un error al no detectar una verdadera media alternativa $\mu_1$).
- **Potencia ($1 - eta$)**: Probabilidad de **hacer justicia** (rechazar $H_0$ exitosamente cuando la media real cambió a $\mu_1$).

### ⚙️ Algoritmo de Cálculo de β (Unilateral Cola Izquierda):
1. Obtener el valor crítico físico de la variable: $ar{x}_c$.
2. Asumir que la verdadera media poblacional es $\mu_1$.
3. Estandarizar el valor crítico bajo la nueva hipótesis real $\mu_1$:
   $$Z_eta = rac{ar{x}_c - \mu_1}{\sigma / \sqrt{n}}$$
4. Calcular $eta = P(Z > Z_eta) = 1 - \Phi(Z_eta)$.
5. Calcular la Potencia: $W = 1 - eta$.

---

## 1.7 Tamaño de Muestra para Potencia Deseada en Ensayos de Hipótesis

Para garantizar un riesgo $lpha$ y simultáneamente una potencia $1-eta$ al detectar una diferencia $|\mu_0 - \mu_1|$:

$$n = \left[ rac{(Z_{(1-lpha)} + Z_{(1-eta)}) \cdot \sigma}{\mu_0 - \mu_1} ight]^2$$

Redondear siempre hacia arriba: $n_{	ext{total}} = \lceil n ceil$.

---

# MÓDULO II: Inferencia sobre la Varianza (σ²) y Desvío Estándar (σ)

---

## 2.1 Intervalo de Confianza para Varianza (σ²) y Desvío (σ) con Chi-Cuadrado (χ²)

### 🎯 ¿Cuándo se utiliza?
Para estimar la dispersión o variabilidad poblacional ($\sigma^2$ o $\sigma$) en un proceso de fabricación o medición.

### 📋 Datos de entrada necesarios:
- Tamaño de muestra ($n$)
- Varianza muestral ($S^2$) o desvío muestral ($S$)
- Nivel de confianza ($1 - lpha$)

### ⚙️ Valores Intermedios que suele pedir el examen:
1. **Grados de libertad ($D$ o $
u$)**: $D = 
u = n - 1$
2. **Suma de Cuadrados de Desviaciones (Numerador de la Varianza)**:
   $$	ext{Suma de Cuadrados} = (n - 1) \cdot S^2 = D \cdot S^2 = \sum (x_i - ar{x})^2$$
3. **Fractil Chi-Cuadrado Inferior**: $\chi^2_{(lpha/2; \; 
u)}$ (área $lpha/2$ a la izquierda)
4. **Fractil Chi-Cuadrado Superior**: $\chi^2_{(1-lpha/2; \; 
u)}$ (área $1-lpha/2$ a la izquierda)

### 📐 Fórmulas del Intervalo para la Varianza (σ²):
$$A_{\sigma^2} = rac{(n-1) \cdot S^2}{\chi^2_{(1-lpha/2; \; 
u)}}$$
$$B_{\sigma^2} = rac{(n-1) \cdot S^2}{\chi^2_{(lpha/2; \; 
u)}}$$

*(Nota de oro: El denominador de $A$ lleva el fractil más grande $\chi^2_{(1-lpha/2)}$ porque al dividir por un número mayor da un límite inferior más chico).*

### 📐 Fórmulas del Intervalo para el Desvío Estándar (σ):
$$A_\sigma = \sqrt{A_{\sigma^2}}, \quad B_\sigma = \sqrt{B_{\sigma^2}}$$

---

## 2.2 Ensayos de Hipótesis para Varianza Poblacional (σ²)

### 📋 Planteo para Ensayo Unilateral Cola Derecha (Verificar exceso de variabilidad):
- $H_0: \sigma^2 \le \sigma_0^2$
- $H_1: \sigma^2 > \sigma_0^2$

### ⚙️ Valores Intermedios:
1. **Valor Crítico Chi-Cuadrado**: $\chi^2_c = \chi^2_{(1-lpha; \; 
u = n-1)}$
2. **Varianza Muestral Crítica ($S_c^2$)**:
   $$S_c^2 = rac{\sigma_0^2 \cdot \chi^2_c}{n - 1}$$
3. **Estadístico de prueba calculado**:
   $$\chi^2_{	ext{calc}} = rac{(n - 1) \cdot S^2}{\sigma_0^2}$$

### 📝 Condición de Rechazo:
Rechazar $H_0$ si $S^2 > S_c^2$ (o equivalentemente si $\chi^2_{	ext{calc}} > \chi^2_c$).

---

## 2.3 Cálculo de Error Tipo II (β) en Ensayos de Varianza

Si la verdadera varianza poblacional cambió a $\sigma_1^2$:
1. Calcular el valor crítico del test: $S_c^2$.
2. Calcular el valor de Chi-Cuadrado equivalente bajo $\sigma_1^2$:
   $$\chi^2_eta = rac{(n - 1) \cdot S_c^2}{\sigma_1^2}$$
3. Obtené $eta = P(\chi^2 \le \chi^2_eta)$ con la función acumulada de $\chi^2$ con $
u = n-1$.

---

# MÓDULO III: Inferencia sobre Proporciones Poblacionales (p)

---

## 3.1 Intervalo de Confianza Exacto para Proporción (p) mediante Distribución F

### ⚠️ ¡ADVERTENCIA DE CÁTEDRA!
**Jamás utilizar la aproximación Normal** $p \pm Z \sqrt{rac{\hat{p}(1-\hat{p})}{n}}$ para muestras pequeñas o cuando $r=0$. Se debe utilizar la fórmula exacta Clopper-Pearson basada en la distribución $F$ de Fisher-Snedecor.

### 📋 Datos de entrada:
- Tamaño de muestra ($n$)
- Cantidad de éxitos / defectuosos registrados ($r$)
- Nivel de confianza ($1 - lpha$)

### ⚙️ Valores Intermedios:
- **Proporción muestral (Estimador puntual)**: $\hat{p} = rac{r}{n}$

---

### 📐 Fórmulas Exactas (Clopper-Pearson via F):

#### CASO GENERAL ($0 < r < n$):
- **Límite Inferior ($A$)**:
  $$A = rac{1}{1 + \left(rac{n - r + 1}{r}ight) \cdot F_{(1-lpha/2; \; 
u_n = 2(n-r+1); \; 
u_d = 2r)}}$$
- **Límite Superior ($B$)**:
  $$B = rac{1}{1 + rac{n - r}{(r + 1) \cdot F_{(1-lpha/2; \; 
u_n = 2r + 2; \; 
u_d = 2n - 2r)}}}$$

#### CASO ESPECIAL 1: Cero éxitos ($r = 0$):
- $A = 0$
- $B = rac{1}{1 + rac{n}{F_{(1-lpha/2; \; 
u_n = 2; \; 
u_d = 2n)}}}$$

#### CASO ESPECIAL 2: Todos éxitos ($r = n$):
- $A = rac{1}{1 + rac{1}{n \cdot F_{(1-lpha/2; \; 
u_n = 2n; \; 
u_d = 2)}}}$$
- $B = 1$

---

## 3.2 Tamaño de Muestra (n) para Proporción Poblacional

Para lograr un Error Muestral deseado $e_{	ext{objetivo}}$:

### Fórmula con $\hat{p}$ preliminar conocida:
$$n_{	ext{teórico}} = \left[ rac{Z_{(1-lpha/2)}}{e_{	ext{objetivo}}} ight]^2 \cdot \hat{p} \cdot (1 - \hat{p})$$

### Fórmula sin información previa (Máxima Incertidumbre $\hat{p} = 0,5$):
$$n_{	ext{teórico}} = \left[ rac{Z_{(1-lpha/2)}}{e_{	ext{objetivo}}} ight]^2 \cdot 0,25$$

1. **Redondeo obligatorio**: $n_{	ext{total}} = \lceil n_{	ext{teórico}} ceil$.
2. **Muestra adicional**: $\Delta n = n_{	ext{total}} - n_{	ext{preliminar}}$.

---

# TABLA MASTER DE VALORES INTERMEDIOS PARA EXÁMENES

Si un ejercicio de examen te pide reportar valores intermedios durante el desarrollo, consulta esta tabla rápida:

| Tema / Problema | Valor Intermedio Solicitado | Nombre / Notación | Fórmula de Cálculo |
| :--- | :--- | :--- | :--- |
| **Media con Z** | Error estándar de la media | $\sigma_{ar{x}}$ | $\sigma / \sqrt{n}$ |
| **Media con Z** | Semi-amplitud / Error muestral | $e$ | $Z_{(1-lpha/2)} \cdot (\sigma / \sqrt{n})$ |
| **Media con t** | Grados de libertad | $
u$ | $n - 1$ |
| **Media con t** | Desvío muestral del promedio | $S_{ar{x}}$ | $S / \sqrt{n}$ |
| **Media (Total)** | Estimador del Total | $\hat{T}$ | $N \cdot ar{x}$ |
| **Ensayo Media** | Valor Crítico Físico | $ar{x}_c$ | $\mu_0 \pm Z_{(1-lpha)} \cdot (\sigma / \sqrt{n})$ |
| **Ensayo Media** | Z de Error Tipo II | $Z_eta$ | $(ar{x}_c - \mu_1) / (\sigma / \sqrt{n})$ |
| **Varianza χ²** | Suma de cuadrados de desvíos | $\sum (x_i - ar{x})^2$ | $(n - 1) \cdot S^2 = D \cdot S^2$ |
| **Varianza χ²** | Fractil Chi-Cuadrado Inferior | $\chi^2_{	ext{inf}}$ | $\chi^2_{(1-lpha/2; \; 
u)}$ |
| **Varianza χ²** | Fractil Chi-Cuadrado Superior | $\chi^2_{	ext{sup}}$ | $\chi^2_{(lpha/2; \; 
u)}$ |
| **Proporción F** | Grados de libertad Num/Den (A) | $
u_n, 
u_d$ | $
u_n = 2(n-r+1), \quad 
u_d = 2r$ |
| **Proporción F** | Grados de libertad Num/Den (B) | $
u_n, 
u_d$ | $
u_n = 2r+2, \quad 
u_d = 2n-2r$ |
| **Tamaños de Muestra** | Unidades adicionales a medir | $\Delta n$ | $n_{	ext{total}} - n_{	ext{preliminar}}$ |

---
