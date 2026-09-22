# ESQUEMA TEÓRICO Y LÓGICA DE CÁLCULO PARA EL PRIMER EXAMEN DE ESTADÍSTICA APLICADA
> **Materia**: Estadística Aplicada (UTN / FIUBA)  
> **Cátedra / Profesores**: Ing. Sergio Aníbal Dopazo, Ing. Roberto Mariano García  
> **Objetivo de este documento**: Servir como especificación técnica completa y base de conocimientos para que un Agente de IA / Desarrollador construya una aplicación web o ejecutable de resolución automática de ejercicios de inferencia estadística.

---

## 0. GLOSARIO DE NOTACIÓN Y REGLAS GENERALES DE PENSAMIENTO

### 0.1 Distinción Parámetro vs. Estimador
- **Parámetro (Población - Desconocido/Teórico)**: Característica fija de toda la población. Representado con **letras griegas**.
  - $\mu$: Media poblacional.
  - $\sigma$: Desvío estándar poblacional.
  - $\sigma^2$: Varianza poblacional.
  - $p$: Proporción poblacional.
  - $\phi^2$: Cociente de varianzas poblacionales ($\sigma_1^2 / \sigma_2^2$).
  - $\delta$: Diferencia de medias poblacionales ($\mu_1 - \mu_2$).
- **Estimador / Estadístico (Muestra - Variable Aleatoria)**: Medida calculada sobre una muestra aleatoria de tamaño $n$. Representado con **letras latinas**.
  - $\bar{x}$: Media muestral (estimador insesgado de $\mu$).
  - $S$: Desvío estándar muestral.
  - $S^2$: Cuasivarianza muestral (divida por $n-1$ para ser insesgada).
  - $\hat{p} = r/n$: Proporción muestral (éxitos $r$ sobre muestra $n$).
  - $j^2 = S_1^2 / S_2^2$: Estimador del cociente de varianzas.
  - $d = \bar{x}_1 - \bar{x}_2$: Estimador de la diferencia de medias.

### 0.2 Símbolos de Incertidumbre y Distribuciones
- $N$: Tamaño de la población (si es finita).
- $n$: Tamaño de la muestra.
- $e$: Error muestral o semi-amplitud del intervalo de confianza.
- $1 - \alpha$: Nivel de Confianza (ej. $0,95$ o $95\%$).
- $\alpha$: Nivel de Riesgo o Significación (Error Tipo I, ej. $0,05$ o $5\%$).
- $\beta$: Error Tipo II (Riesgo del Consumidor).
- $1 - \beta$: Potencia del Ensayo (probabilidad de detectar una hipótesis falsa).
- $\nu$ o $D$: Grados de Libertad ($n-1$, $n_1+n_2-2$, $(R-1)(C-1)$, etc.).
- $Z$: Variable Normal Estándar ($\mu=0, \sigma=1$).
- $t$: Variable $t$ de Student ($\mu=0$, depende de $\nu$).
- $\chi^2$: Variable Chi-Cuadrado (asimétrica, positiva, depende de $\nu$).
- $F$: Variable $F$ de Fisher-Snedecor (asimétrica, positiva, depende de $\nu_n$ y $\nu_d$).

---

## 1. UNIDAD 1: ESTIMACIÓN DE PARÁMETROS POR INTERVALOS DE CONFIANZA

El objetivo es construir un intervalo $[A; B]$ tal que $P(A \le \text{Parámetro} \le B) = 1 - \alpha$.

---

### 1.1 Estimación de la Media Poblacional ($\mu$)

#### CASO A: Desvío Poblacional Conocido ($\sigma$)
- **Distribución**: Normal Estándar ($Z$).
- **Población Infinita**:
  $$\text{Límites } A; B = \bar{x} \pm Z_{(1 - \alpha/2)} \cdot \frac{\sigma}{\sqrt{n}}$$
  $$\text{Error Muestral } e = Z_{(1 - \alpha/2)} \cdot \frac{\sigma}{\sqrt{n}}$$
- **Población Finita ($N$ conocido)**:
  $$\text{Factor de Corrección por Finitud} = \sqrt{\frac{N - n}{N - 1}}$$
  $$A; B = \bar{x} \pm Z_{(1 - \alpha/2)} \cdot \frac{\sigma}{\sqrt{n}} \cdot \sqrt{\frac{N - n}{N - 1}}$$
  $$e = Z_{(1 - \alpha/2)} \cdot \frac{\sigma}{\sqrt{n}} \cdot \sqrt{\frac{N - n}{N - 1}}$$

- **Cálculo del Tamaño de Muestra ($n$)**:
  - *Población Infinita*:
    $$n = \left\lceil \left( \frac{Z_{(1 - \alpha/2)} \cdot \sigma}{e} \right)^2 \right\rceil$$
  - *Población Finita*: Primero calcular $n_\infty = \left( \frac{Z_{(1 - \alpha/2)} \cdot \sigma}{e} \right)^2$, luego corregir:
    $$n = \left\lceil \frac{N \cdot n_\infty}{N + n_\infty} \right\rceil$$

---

#### CASO B: Desvío Poblacional Desconocido ($\sigma$ desconocido)
- **Distribución**: $t$ de Student con $\nu = n - 1$ grados de libertad.
- **Población Infinita**:
  $$A; B = \bar{x} \pm t_{(1 - \alpha/2; \nu = n-1)} \cdot \frac{S}{\sqrt{n}}$$
  $$e = t_{(1 - \alpha/2; \nu = n-1)} \cdot \frac{S}{\sqrt{n}}$$
- **Población Finita ($N$ conocido)**:
  $$A; B = \bar{x} \pm t_{(1 - \alpha/2; \nu = n-1)} \cdot \frac{S}{\sqrt{n}} \cdot \sqrt{\frac{N - n}{N - 1}}$$

- **Cálculo del Tamaño de Muestra ($n$) - MÉTODO ITERATIVO**:
  - *Problema Teórico*: $n = \left[ \frac{t_{(1 - \alpha/2; \nu = n-1)} \cdot S}{e} \right]^2$. Como $t$ depende de $\nu = n-1$, $n$ aparece a ambos lados.
  - *Algoritmo de Bucle Iterativo (para codificar en la App)*:
    1. Tomar un supuesto inicial $n^{(0)} = 100$ (o asumirlo amplio).
    2. Calcular $\nu^{(k)} = n^{(k)} - 1$.
    3. Buscar en la distribución $t$ el fractil $t_{(1 - \alpha/2; \nu^{(k)})}$.
    4. Recalcular $n^{(k+1)} = \left\lceil \left( \frac{t \cdot S}{e} \right)^2 \right\rceil$.
    5. Repetir hasta que $n^{(k+1)} == n^{(k)}$. (Garantizado en $\le 3$ iteraciones).
  - *Si la población es finita ($N$)*: Resolver $n_\infty$ con el bucle iterativo anterior y luego aplicar $n = \left\lceil \frac{N \cdot n_\infty}{N + n_\infty} \right\rceil$.

---

### 1.2 Estimación de la Varianza Poblacional ($\sigma^2$) y Desvío ($\sigma$)

- **Distribución**: Chi-Cuadrado ($\chi^2$) con $\nu = n - 1$ grados de libertad.
- **Variable Estandarizada**: $\chi^2 = \frac{(n-1) S^2}{\sigma^2}$.
- **Intervalo de Confianza para $\sigma^2$**:
  $$P\left( \frac{(n-1)S^2}{\chi^2_{(1 - \alpha/2; \nu)}} \le \sigma^2 \le \frac{(n-1)S^2}{\chi^2_{(\alpha/2; \nu)}} \right) = 1 - \alpha$$
  - **Límite Inferior ($A$)**: $A = \frac{(n-1)S^2}{\chi^2_{(1 - \alpha/2; \nu)}}$ (se divide por la $\chi^2$ grande de área $1-\alpha/2$).
  - **Límite Superior ($B$)**: $B = \frac{(n-1)S^2}{\chi^2_{(\alpha/2; \nu)}}$ (se divide por la $\chi^2$ chica de área $\alpha/2$).
- **Intervalo de Confianza para el Desvío ($\sigma$)**:
  $$[\sqrt{A} \le \sigma \le \sqrt{B}]$$
- **Tamaño de muestra ($n$) — Ecuación de García**: como el intervalo es asimétrico, la precisión no se mide con un error $\pm e$ sino con la **relación entre límites** del IC del desvío:
  $$R' = \frac{B'}{A'} = \frac{\sqrt{B}}{\sqrt{A}} \qquad R = (R')^2 = \frac{\chi^2_{(1-\alpha/2;\nu)}}{\chi^2_{(\alpha/2;\nu)}}$$
  - Si el enunciado pide **disminuir un $k\%$** la relación anterior: $R'_{obj} = R'_{orig} \cdot (1 - k)$.
  - Invirtiendo la aproximación de Wilson–Hilferty $\chi^2_{(p;\nu)} \approx \nu\left(1 - \frac{2}{9\nu} + Z_p\sqrt{\frac{2}{9\nu}}\right)^3$ se obtiene, sin tantear la tabla:
    $$a = \frac{Z_{(1-\alpha/2)} \cdot \left(\sqrt[3]{R} + 1\right)}{2 \cdot \left(\sqrt[3]{R} - 1\right)} \qquad \nu = \frac{2}{9}\left(a + \sqrt{a^2 + 1}\right)^2 \qquad n = \lceil \nu + 1 \rceil$$
  - **Atención a la notación**: el radical de $R$ es **cúbico** (viene del cubo de Wilson–Hilferty), equivalente a $(R')^{2/3}$. Varios apuntes lo transcriben como $\sqrt{R}$ por error, aunque después calculan la raíz cúbica.
  - Si ya se relevó una muestra preliminar: $\Delta n = n - n_{prelim}$.

---

### 1.3 Estimación de la Proporción Poblacional ($p$)

- **Estimador Puntual**: $\hat{p} = \frac{r}{n}$ (donde $r$ es la cantidad de éxitos).
- **Aproximación Normal** (requiere $n\hat{p} \ge 5$ y $n(1-\hat{p}) \ge 5$):
  $$A; B = \hat{p} \pm Z_{(1 - \alpha/2)} \cdot \sqrt{\frac{\hat{p}(1 - \hat{p})}{n - 1}}$$
  $$e = Z_{(1 - \alpha/2)} \cdot \sqrt{\frac{\hat{p}(1 - \hat{p})}{n - 1}}$$
- **Tamaño de muestra ($n_0$)**:
  $$n_0 = \left\lceil \frac{Z_{(1 - \alpha/2)}^2 \cdot \hat{p}(1 - \hat{p})}{e^2} + 1 \right\rceil$$
- **Modelo Exacto (Binomial / Fisher)**: Cuando $n$ es pequeño o $r=0$, la app debe recurrir a la distribución Binomial acumulada o transformación a $F$.

---

## 2. UNIDAD 2: ENSAYOS DE HIPÓTESIS (1 POBLACIÓN)

### 2.1 Filosofía del Ensayo de Hipótesis y Matriz de Decisión

1. **Inocente hasta demostración de lo contrario**: La Hipótesis Nula ($H_0$) es el acusado. Se presume verdadera.
2. **Nunca se dice "Acepto $H_0$"**: Se dice **"No se rechaza $H_0$"** (falta de pruebas) o **"Se rechaza $H_0$"** (evidencia suficiente).
3. **Igualdad siempre en $H_0$**: $H_0$ lleva los signos $=, \le, \ge$. $H_1$ lleva $\ne, >, <$.

#### Matriz de Decisión y Errores
- **Error Tipo I ($\alpha$)**: Rechazar $H_0$ cuando es VERDADERA. "Condenar a un inocente". Se fija *a priori* (ej. 5%).
- **Error Tipo II ($\beta$)**: No rechazar $H_0$ cuando es FALSA. "Absolver a un culpable".
- **Potencia del Ensayo ($1 - \beta$)**: Probabilidad de rechazar $H_0$ cuando realmente es FALSA (hacer justicia).

#### Criterios de Planteo para $H_0$:
- **Criterio Pesimista (Inversiones / Cambios de proceso)**: Asume que el producto o aditivo **no funciona** ($H_0: \mu \ge \mu_0$ o $\mu \le \mu_0$). Exige a la muestra pruebas abrumadoras para autorizar el gasto.
- **Criterio Optimista (Control de Recepción / Calidad)**: Asume que el lote **cumple la especificación** ($H_0: \mu = \mu_0$).

---

### 2.2 Ensayos para la Media Poblacional ($\mu$) con $\sigma$ Conocido

#### CASO I: Unilateral Cola Derecha ($H_0: \mu \le \mu_0$ vs $H_1: \mu > \mu_0$)
- **Valor Crítico**: $\bar{x}_c = \mu_0 + Z_{(1 - \alpha)} \cdot \frac{\sigma}{\sqrt{n}}$
- **Condición de Rechazo (CR)**: Si $\bar{x} > \bar{x}_c \implies \text{Rechazo } H_0$.
- **Error Tipo II ($\beta$)** para una media alternativa $\mu_1 > \mu_0$:
  $$Z_\beta = \frac{\bar{x}_c - \mu_1}{\sigma / \sqrt{n}} \implies \beta = \Phi(Z_\beta) = P(Z \le Z_\beta)$$
- **Potencia**: $1 - \beta = 1 - \Phi(Z_\beta)$.
- **Tamaño de muestra para Potencia $1-\beta$ fijada**:
  $$n = \left\lceil \left[ \frac{(Z_{(1 - \alpha)} + Z_{(1 - \beta)}) \cdot \sigma}{\mu_0 - \mu_1} \right]^2 \right\rceil$$

#### CASO II: Unilateral Cola Izquierda ($H_0: \mu \ge \mu_0$ vs $H_1: \mu < \mu_0$)
- **Valor Crítico**: $\bar{x}_c = \mu_0 - Z_{(1 - \alpha)} \cdot \frac{\sigma}{\sqrt{n}}$
- **Condición de Rechazo (CR)**: Si $\bar{x} < \bar{x}_c \implies \text{Rechazo } H_0$.
- **Error Tipo II ($\beta$)** para una media alternativa $\mu_1 < \mu_0$:
  $$Z_\beta = \frac{\bar{x}_c - \mu_1}{\sigma / \sqrt{n}} \implies \beta = 1 - \Phi(Z_\beta) = P(Z \ge Z_\beta)$$

#### CASO III: Bilateral ($H_0: \mu = \mu_0$ vs $H_1: \mu \ne \mu_0$)
- **Valores Críticos**:
  $$\bar{x}_{c1} = \mu_0 - Z_{(1 - \alpha/2)} \cdot \frac{\sigma}{\sqrt{n}}$$
  $$\bar{x}_{c2} = \mu_0 + Z_{(1 - \alpha/2)} \cdot \frac{\sigma}{\sqrt{n}}$$
- **Condición de Rechazo (CR)**: Si $\bar{x} < \bar{x}_{c1}$ o $\bar{x} > \bar{x}_{c2} \implies \text{Rechazo } H_0$.

---

### 2.3 Ensayos para la Media Poblacional ($\mu$) con $\sigma$ Desconocido

Se reemplaza $Z$ por $t_{(1-\alpha; \nu = n-1)}$ y $\sigma$ por $S$:
- **Cola Derecha**: $\bar{x}_c = \mu_0 + t_{(1 - \alpha; \nu)} \cdot \frac{S}{\sqrt{n}}$
- **Cola Izquierda**: $\bar{x}_c = \mu_0 - t_{(1 - \alpha; \nu)} \cdot \frac{S}{\sqrt{n}}$
- **Bilateral**: $\bar{x}_{c1;c2} = \mu_0 \pm t_{(1 - \alpha/2; \nu)} \cdot \frac{S}{\sqrt{n}}$

---

### 2.4 Ensayos para la Varianza Poblacional ($\sigma^2$)

- **Estadístico de Prueba**: $\chi^2_c = \frac{(n-1)S^2}{\sigma_0^2}$.
- **Unilateral Cola Derecha ($H_0: \sigma^2 \le \sigma_0^2$ vs $H_1: \sigma^2 > \sigma_0^2$)**:
  - Valor Crítico de la Cuasivarianza: $S^2_c = \frac{\sigma_0^2 \cdot \chi^2_{(1 - \alpha; \nu)}}{n - 1}$.
  - CR: Si $S^2 > S^2_c$ (o si $\chi^2_c > \chi^2_{(1 - \alpha; \nu)}$) $\implies \text{Rechazo } H_0$.

---

## 3. UNIDAD 3: COMPARACIÓN DE PARÁMETROS (2 POBLACIONES INDEPENDIENTES)

---

### 3.1 Comparación de Varianzas ($\sigma_1^2$ vs $\sigma_2^2$)
Antes de comparar medias de dos poblaciones, **es obligatorio ensayar la igualdad de varianzas**.

- **Parámetro**: $\phi^2 = \frac{\sigma_1^2}{\sigma_2^2}$.
- **Estimador Muestral**: $j^2 = \frac{S_1^2}{S_2^2}$.
- **Distribución**: $F$ de Fisher-Snedecor con $\nu_1 = n_1 - 1$ (numerador) y $\nu_2 = n_2 - 1$ (denominador).

#### Ensayo Bilateral ($H_0: \phi^2 = 1$ vs $H_1: \phi^2 \ne 1$):
- **Convención práctica para la App**: Colocar la varianza muestral mayor en el numerador para que $j^2 \ge 1$:
  $$j^2_{calc} = \frac{\max(S_1^2, S_2^2)}{\min(S_1^2, S_2^2)}$$
- **Valor Crítico**: $F_c = F_{(1 - \alpha/2; \nu_{num}, \nu_{den})}$.
- **Condición de Rechazo**: Si $j^2_{calc} > F_c \implies \text{Se prueban Varianzas Distintas } (\sigma_1^2 \ne \sigma_2^2)$. Caso contrario, **se suponen Varianzas Iguales** ($\sigma_1^2 = \sigma_2^2$).

---

### 3.2 Comparación de Medias Poblacionales ($\mu_1 - \mu_2 = \delta$)

#### CASO A: Varianzas Poblacionales Desconocidas pero Supuestas Iguales ($\sigma_1^2 = \sigma_2^2$)
- **Cuasivarianza Amalgamada (Pooled Variance $S_p^2$)**:
  $$S_p^2 = \frac{(n_1 - 1)S_1^2 + (n_2 - 1)S_2^2}{n_1 + n_2 - 2}$$
- **Desvío Estándar de la Diferencia ($\hat{\sigma}_d$)**:
  $$\hat{\sigma}_d = S_p \cdot \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}$$
- **Grados de Libertad del Sistema**: $\nu = n_1 + n_2 - 2$.
- **Intervalo de Confianza para $\delta = \mu_1 - \mu_2$**:
  $$A; B = (\bar{x}_1 - \bar{x}_2) \pm t_{(1 - \alpha/2; \nu = n_1+n_2-2)} \cdot \hat{\sigma}_d$$
- **Valor Crítico de Diferencia ($d_c$) para Ensayo Cola Derecha ($H_0: \delta \le \delta_0$)**:
  $$d_c = \delta_0 + t_{(1 - \alpha; \nu)} \cdot \hat{\sigma}_d$$

---

#### CASO B: Varianzas Poblacionales Desconocidas y Probadas Distintas ($\sigma_1^2 \ne \sigma_2^2$) — TEST DE WELCH
- **Desvío Estándar de la Diferencia ($\hat{\sigma}_d$)**:
  $$\hat{\sigma}_d = \sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}$$
- **Grados de Libertad Efectivos de Welch ($\nu_{AW}$)** (Ecuación de Aspin-Welch-Satterthwaite):
  $$\nu_{AW} = \left\lfloor \frac{\left( \frac{S_1^2}{n_1} + \frac{S_2^2}{n_2} \right)^2}{\frac{1}{n_1 - 1} \left( \frac{S_1^2}{n_1} \right)^2 + \frac{1}{n_2 - 1} \left( \frac{S_2^2}{n_2} \right)^2} \right\rfloor$$
  *(Se redondea al entero inferior $\lfloor \dots \rfloor$)*.
- **Intervalo de Confianza**:
  $$A; B = (\bar{x}_1 - \bar{x}_2) \pm t_{(1 - \alpha/2; \nu_{AW})} \cdot \sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}$$

---

## 4. UNIDAD 4: CONTRASTES CHI-CUADRADO ($\chi^2$)

Procedimientos para comparar frecuencias observadas ($F_{o_i}$) de una muestra con frecuencias esperadas ($F_{e_i}$) teóricas.

### 4.1 Estadístico General de Prueba
$$\chi^2_c = \sum_{i=1}^{k} \frac{(F_{o_i} - F_{e_i})^2}{F_{e_i}}$$

### 4.2 Requisitos Obligatorios de Robustez
1. Tamaños de muestra grande: $N_{total} \ge 60$.
2. Frecuencia esperada mínima por celda: $F_{e_i} \ge 5$. Si $F_{e_i} < 5$, **se deben agrupar celdas/categorías adyacentes** sumando sus frecuencias observadas y esperadas.

---

### 4.3 Pruebas de Bondad de Ajuste
- **Hipótesis**: $H_0$: Los datos siguen la distribución especificada (Normal, Binomial, Poisson, Weibull, etc.).
- **Grados de Libertad**:
  $$\nu = k - 1 - p$$
  - $k$: Cantidad de categorías/intervalos efectivos (después de agrupar si hubo $F_{e_i} < 5$).
  - $p$: Cantidad de parámetros estimados a partir de los datos muestrales (ej. si para la Normal se estimó $\bar{x}$ y $S$, entonces $p=2$; si los parámetros estaban fijos por especificación, $p=0$).
- **Regla de Decisión**: Si $\chi^2_c > \chi^2_{(1 - \alpha; \nu)} \implies \text{Se rechaza } H_0$ (los datos no se ajustan al modelo).

---

### 4.4 Tablas de Contingencia (Pruebas de Independencia y Homogeneidad)
- **Matriz**: $R$ filas por $C$ columnas.
- **Frecuencia Esperada Teórica de la Celda $(i, j)$**:
  $$E_{ij} = \frac{T_i \cdot T_j}{T_T} = \frac{(\text{Total Fila } i) \cdot (\text{Total Columna } j)}{\text{Total General}}$$
- **Grados de Libertad**:
  $$\nu = (R - 1) \cdot (C - 1)$$
- **Condición de Rechazo**: Si $\chi^2_c > \chi^2_{(1 - \alpha; \nu)} \implies \text{Se rechaza } H_0$ (las variables están asociadas / no son independientes).

---

## 5. ESPECIFICACIONES TÉCNICAS PARA LA ARQUITECTURA DE LA APP (SOLVER)

Para que el Agente Programador construya la aplicación sin ambigüedades, debe implementar el siguiente flujo lógico:

```
                          [ INICIO: SELECCIÓN DE TEMA ]
                                        |
      +---------------------------------+---------------------------------+
      |                                 |                                 |
[1. ESTIMACIÓN IC]             [2. ENSAYO HIPÓTESIS]           [3. COMPARACIÓN 2 POBL.]
      |                                 |                                 |
      |-- ¿Conoce sigma?                |-- Definir H0/H1 (Pesim./Optim.) |-- Paso 1: Test F (S1^2 vs S2^2)
      |   |-- Sí -> Usar Z              |-- Determinar cola (Der, Izq, Bil)|   |-- S1^2 = S2^2 -> t Amalgamada
      |   +-- No -> Usar t (nu=n-1)     |-- Calcular valor crítico x_c     |   +-- S1^2 != S2^2 -> Test Welch (nu_AW)
      |-- ¿Calcular n?                  |-- Evaluar x_muestra vs x_c      |-- Paso 2: Calcular IC o Ensayo d
      |   |-- Con sigma -> Formula Z    |-- Calcular Beta y Potencia      |
      |   +-- Sin sigma -> Bucle n_iter |-- Calcular n para Potencia fida +---------------------------------+
      |-- ¿Poblacion N finita?          +---------------------------------+                                 |
          +-- Aplicar factor finitud                                                               [4. CONTRASTE CHI^2]
                                                                                                            |
                                                                                                            |-- Calcular Fe_i
                                                                                                            |-- Agrupar si Fe_i < 5
                                                                                                            |-- nu = k - 1 - p
                                                                                                            |-- Comparar chi^2_calc vs crit
```

### Reglas de Carga de Parámetros para la App
1. **Redondeos Obligatorios**:
   - Muestras ($n$): **Siempre redondear hacia arriba** ($\lceil n \rceil$). Nunca redondear hacia abajo.
   - Grados de Libertad de Welch ($\nu_{AW}$): **Siempre truncar / redondear hacia abajo** ($\lfloor \nu_{AW} \rfloor$).
2. **Expresión Formal de Resultados**:
   La App no debe mostrar solo números, sino la redacción formal:
   - Para Intervalos: `$P(A \le \text{Parámetro} \le B) = 1 - \alpha$`.
   - Para Ensayos: *"De acuerdo a la evidencia muestral ($\bar{x} = \dots$), al nivel de significación del $\alpha\%$, (se rechaza / no se rechaza) la hipótesis nula..."*.
