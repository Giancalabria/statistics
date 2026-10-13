# Resolución de Problemas — Estadística Aplicada

Resolución siguiendo los 7 pasos de la cátedra: hipótesis, nivel de significación, estadístico, condición de rechazo (CR), regla de decisión (RD), cálculos y conclusión. Todos los valores fueron verificados con `scipy`.

---

## Problema 1 — Modificación del sistema productivo

### Enunciado

El departamento de I+D de una empresa ha desarrollado un nuevo sistema de producción que quiere implementar para modificar su proceso de fabricación. Luego de pruebas experimentales, se piensa que el nuevo sistema aumentaría la productividad a un valor promedio de 5.8 piezas por minuto. El sistema actual del proceso de fabricación tiene una productividad promedio de 4.2 piezas por minuto con un desvío estándar de 2.53 piezas por minuto. A fin de tomar una decisión sobre la modificación del sistema productivo, se estipulan las siguientes condiciones: el departamento de ingeniería propone que es conveniente establecer una probabilidad de 0.95 de modificar el sistema productivo cuando con la modificación se obtiene un valor promedio de 5.8 piezas por minuto; en cambio el gerente general desea asumir la certeza del 99% de no realizar la modificación en el sistema productivo, cuando con la modificación no se consigue el efecto deseado. Se asume que el desvío estándar no se modificará.

a) Indicar el tamaño de la muestra y la hipótesis adecuada, también establecer condición de rechazo y la regla de decisión.

b) ¿Cuál es la probabilidad de no realizar la modificación en el sistema productivo si la productividad promedio, con la modificación, es de 4.98 piezas por minuto?

c) Suponga que se realizó la modificación y se sacó la muestra calculada en el inciso a), y se encontraron 10 piezas sin defectos. Estimar con un 99% de confianza el porcentaje de piezas malas fabricadas por la empresa.

### Diagnóstico

- **Variable:** $X$ = productividad del proceso [piezas/min].
- **σ conocido:** $\sigma = 2.53$ piezas/min, y no cambia con la modificación. Por lo tanto se usa la **distribución Normal (Z)**.
- **Población:** infinita (proceso productivo).

### a) Hipótesis, tamaño de muestra, CR y RD

**1. Hipótesis.** Se usa el criterio pesimista: la mejora va en $H_1$.

- $H_0: \mu = 4.2$. La modificación no mejora, se mantiene el sistema actual.
- $H_1: \mu > 4.2$. La modificación aumenta la productividad.

**2. Riesgos.**

- El gerente quiere un 99% de certeza de **no** modificar cuando no se logra el efecto. Eso es $1-\alpha = 0.99$, o sea $\alpha = 0.01$.
- Ingeniería quiere una probabilidad de 0.95 de modificar cuando $\mu = 5.8$. Eso es $1-\beta = 0.95$, o sea $\beta = 0.05$ en $\mu_1 = 5.8$.

**Tamaño de muestra:**

$$n = \left[\frac{(z_{0.99}+z_{0.95})\,\sigma}{\mu_1-\mu_0}\right]^2 = \left[\frac{(2.326+1.645)\cdot 2.53}{5.8-4.2}\right]^2 = 39.43 \;\Rightarrow\; \boxed{n = 40}$$

**3. Estadístico de prueba:**

$$Z = \frac{\bar x - 4.2}{\sigma/\sqrt{n}} \sim N(0,1), \qquad \sigma_{\bar x} = \frac{2.53}{\sqrt{40}} = 0.40$$

**4. Condición de rechazo.** Se rechaza $H_0$ si $Z > z_{0.99} = 2.326$. En unidades de la variable:

$$\bar x_c = 4.2 + 2.326\cdot 0.40 = \mathbf{5.13\ \text{piezas/min}}$$

**5. Regla de decisión.** *"Si en una muestra de 40 mediciones la productividad promedio supera 5.13 piezas/min, se rechaza $H_0$ y se modifica el sistema productivo. Si no la supera, se mantiene el sistema actual."*

### b) Probabilidad de no modificar si μ = 4.98

No modificar significa no rechazar $H_0$. Siendo $H_1$ verdadera, esa probabilidad es el error tipo II, $\beta$, evaluado en $\mu = 4.98$:

$$\beta = P(\bar x < 5.1306 \mid \mu = 4.98) = \Phi\!\left(\frac{5.1306-4.98}{0.40}\right) = \Phi(0.377) = \boxed{0.6467}$$

**Conclusión:** si la productividad real con la modificación es 4.98 piezas/min, hay un **64.7%** de probabilidad de no hacer la modificación. La mejora real (0.78 piezas/min) es bastante menor que la diferencia de 1.6 para la que se diseñó el ensayo, y por eso la potencia es baja.

### c) IC 99% para la proporción de piezas malas

Con $n = 40$ y 10 piezas **sin defectos**, hay $40 - 10 = 30$ piezas malas:

$$\hat p = \frac{30}{40} = 0.75$$

Como $n\hat p = 30 \ge 5$ y $n(1-\hat p) = 10 \ge 5$, se puede usar la aproximación Normal:

$$\hat p \pm z_{0.995}\sqrt{\frac{\hat p(1-\hat p)}{n}} = 0.75 \pm 2.576\sqrt{\frac{0.75\cdot 0.25}{40}} = 0.75 \pm 2.576\cdot 0.0685 = 0.75 \pm 0.176$$

$$\boxed{57.4\% \le p \le 92.6\%}$$

**Conclusión:** con un 99% de confianza, el porcentaje de piezas malas fabricadas está entre el 57.4% y el 92.6%.

> ⚠️ **Nota:** si el enunciado original decía "10 piezas **defectuosas**" (es la versión más habitual de esta consigna), entonces $\hat p = 0.25$ y el intervalo es **7.4% ≤ p ≤ 42.6%**. El error de estimación es el mismo: ±0.176.

---

## Problema 2 — Faena de conejos

### Enunciado

Un criador de conejos para faena desea estudiar las características de la población de estos en el establecimiento. Con el motivo de efectuar la próxima faena decide efectuar un control del lote de conejos, de manera que si el lote pesa en promedio más de 4.6 kg y un desvío estándar menor a 0.55 kg, efectuará la faena. Caso contrario se esperará más tiempo para la misma. Se desea asumir el riesgo de 1% de efectuar equivocadamente la faena de conejos. A tal efecto se tomó una muestra de 20 conejos elegidos al azar obteniéndose los siguientes resultados de pesos medidos en kg:

5.01 - 5.11 - 5.08 - 4.41 - 4.37 - 4.31 - 5.05 - 4.35 - 4.25 - 5.15 - 5.02 - 5.09 - 5.08 - 5.15 - 4.23 - 5.18 - 5.14 - 5.17 - 4.21 - 5.06

a) ¿Considera que los datos son concluyentes para realizar la correspondiente faena?

b) ¿Cuál es la probabilidad de no detectar que el desvío estándar es de 0.3 kg?

c) Estimar el peso promedio y el desvío estándar de todo el lote de conejos del establecimiento. Tomar un nivel de confianza de 99%.

d) ¿Cuántos conejos más se deben pesar para reducir en un 15% el error de estimación del valor promedio calculado anteriormente?

### Diagnóstico

- **Variable:** $X$ = peso de un conejo [kg]. Se supone $X \sim N(\mu, \sigma)$.
- **σ desconocido:** se usa el cuasi-desvío $S$. Para la media corresponde **t de Student** y para la varianza **χ²**.
- **Muestra:** $n = 20$, muestreo aleatorio simple.

**Estadísticos muestrales:**

| Estimador | Valor |
|---|---|
| $\bar x$ | 4.821 kg |
| $S$ | 0.3939 kg |
| $S^2$ | 0.1551 kg² |

### a) ¿Son concluyentes los datos para faenar?

Se faena solo si se cumplen **las dos** condiciones. Faenar es el cambio respecto del status quo, así que va en $H_1$. Se usa $\alpha = 0.01$ en cada ensayo.

#### Ensayo sobre la media

1. **Hipótesis:**
   - $H_0: \mu \le 4.6$
   - $H_1: \mu > 4.6$
2. **Nivel de significación:** $\alpha = 0.01$
3. **Estadístico:** $t = \dfrac{\bar x - 4.6}{S/\sqrt{n}} \sim t_{19}$
4. **Condición de rechazo:** se rechaza $H_0$ si $t > t_{0.99;19} = 2.539$. Equivale a $\bar x > 4.6 + 2.539\cdot\dfrac{0.3939}{\sqrt{20}} = 4.824$ kg.
5. **Regla de decisión:** *"Si el peso promedio de los 20 conejos supera 4.824 kg, se concluye que el lote pesa en promedio más de 4.6 kg."*
6. **Cálculo:**
   $$t = \frac{4.821-4.6}{0.3939/\sqrt{20}} = 2.509$$
7. **Conclusión:** $2.509 < 2.539$, así que **no se rechaza $H_0$**. No hay evidencia suficiente de que el peso promedio supere 4.6 kg. El valor observado queda muy cerca del límite.

#### Ensayo sobre el desvío estándar

1. **Hipótesis:**
   - $H_0: \sigma \ge 0.55$
   - $H_1: \sigma < 0.55$
2. **Nivel de significación:** $\alpha = 0.01$
3. **Estadístico:** $\chi^2 = \dfrac{(n-1)S^2}{\sigma_0^2} \sim \chi^2_{19}$
4. **Condición de rechazo:** se rechaza $H_0$ si $\chi^2 < \chi^2_{0.01;19} = 7.633$. Equivale a $S^2 < \dfrac{0.3025\cdot 7.633}{19} = 0.1215$, es decir $S < 0.349$ kg.
5. **Regla de decisión:** *"Si el desvío muestral es menor que 0.349 kg, se concluye que el desvío del lote es menor a 0.55 kg."*
6. **Cálculo:**
   $$\chi^2 = \frac{19\cdot 0.1551}{0.55^2} = 9.745$$
7. **Conclusión:** $9.745 > 7.633$, así que **no se rechaza $H_0$**. No hay evidencia suficiente de que el desvío sea menor a 0.55 kg.

#### Conclusión general

Con un riesgo del 1% de faenar equivocadamente, **los datos no son concluyentes para realizar la faena**. No se puede afirmar que el peso medio supere 4.6 kg ni que el desvío sea menor a 0.55 kg, por lo que conviene **esperar**.

### b) Probabilidad de no detectar que σ = 0.3 kg

Es el error tipo II del ensayo de varianza evaluado en $\sigma = 0.3$: la probabilidad de que $S^2$ caiga en la zona de no rechazo ($S^2 \ge 0.1215$) cuando en realidad $\sigma = 0.3$.

$$\beta = P\!\left(S^2 > 0.1215 \mid \sigma = 0.3\right) = P\!\left(\chi^2_{19} > \frac{19\cdot 0.1215}{0.3^2}\right) = P(\chi^2_{19} > 25.65) = \boxed{0.140}$$

**Conclusión:** hay un **14%** de probabilidad de no detectar que el desvío del lote es 0.3 kg.

### c) Intervalos de confianza al 99%

**Peso promedio** (t de Student, con $t_{0.995;19} = 2.861$):

$$\bar x \pm t_{0.995;19}\frac{S}{\sqrt n} = 4.821 \pm 2.861\cdot\frac{0.3939}{\sqrt{20}} = 4.821 \pm 0.252$$

$$\boxed{4.569\ \text{kg} \le \mu \le 5.073\ \text{kg}}$$

**Desvío estándar** (χ², con $\chi^2_{0.995;19} = 38.582$ y $\chi^2_{0.005;19} = 6.844$):

$$\sqrt{\frac{(n-1)S^2}{\chi^2_{0.995;19}}} \le \sigma \le \sqrt{\frac{(n-1)S^2}{\chi^2_{0.005;19}}}$$

$$\sqrt{\frac{19\cdot 0.1551}{38.582}} \le \sigma \le \sqrt{\frac{19\cdot 0.1551}{6.844}}$$

$$\boxed{0.276\ \text{kg} \le \sigma \le 0.656\ \text{kg}}$$

**Conclusión:** con un 99% de confianza, el peso promedio del lote está entre 4.569 y 5.073 kg, y su desvío estándar entre 0.276 y 0.656 kg.

### d) Conejos adicionales para reducir el error un 15%

- Error actual: $e = 0.252$ kg
- Error nuevo: $e' = 0.85 \cdot 0.252 = 0.214$ kg

Se despeja $n$ de la fórmula del error:

$$n' = \left(\frac{t_{0.995}\cdot S}{e'}\right)^2 = \left(\frac{2.861\cdot 0.3939}{0.214}\right)^2 = \frac{20}{0.85^2} = 27.7 \;\Rightarrow\; n' = 28$$

$$\boxed{\text{Se deben pesar } 28 - 20 = 8 \text{ conejos más}}$$

> **Nota:** si se recalcula $t$ con los nuevos grados de libertad (proceso iterativo), alcanza con $n' = 27$, es decir 7 conejos más. La respuesta de 8 es la conservadora.
