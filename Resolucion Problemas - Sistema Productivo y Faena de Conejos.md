# Resolución de Problemas — Estadística Aplicada

Resolución con los pasos que exige el profesor: variable, hipótesis justificadas en palabras, riesgos, tamaño de muestra, valor crítico, condición de rechazo (CR) y regla de decisión (RD), estimador y conclusión. Se compara siempre el **estimador contra el valor crítico** (en unidades de la variable), las probabilidades van entre 0 y 1 y el desarrollo lleva al menos 4 decimales. Todos los valores fueron verificados con `scipy`.

---

## Problema 1 — Modificación del sistema productivo

### Enunciado

El departamento de I+D de una empresa ha desarrollado un nuevo sistema de producción que quiere implementar para modificar su proceso de fabricación. Luego de pruebas experimentales, se piensa que el nuevo sistema aumentaría la productividad a un valor promedio de 5.8 piezas por minuto. El sistema actual del proceso de fabricación tiene una productividad promedio de 4.2 piezas por minuto con un desvío estándar de 2.53 piezas por minuto. A fin de tomar una decisión sobre la modificación del sistema productivo, se estipulan las siguientes condiciones: el departamento de ingeniería propone que es conveniente establecer una probabilidad de 0.95 de modificar el sistema productivo cuando con la modificación se obtiene un valor promedio de 5.8 piezas por minuto; en cambio el gerente general desea asumir la certeza del 99% de no realizar la modificación en el sistema productivo, cuando con la modificación no se consigue el efecto deseado. Se asume que el desvío estándar no se modificará.

a) Indicar el tamaño de la muestra y la hipótesis adecuada, también establecer condición de rechazo y la regla de decisión.

b) ¿Cuál es la probabilidad de no realizar la modificación en el sistema productivo si la productividad promedio, con la modificación, es de 4.98 piezas por minuto?

c) Suponga que se realizó la modificación y se sacó la muestra calculada en el inciso a), y se encontraron 10 piezas sin defectos. Estimar con un 99% de confianza el porcentaje de piezas malas fabricadas por la empresa.

### Diagnóstico

- **Variable:** $X$ = productividad del proceso con el sistema modificado, en piezas por minuto.
- **Distribución:** $\sigma = 2{,}53$ piezas/min es un parámetro (el enunciado dice que no se modifica). $\bar x$ es normal y, al estandarizar, se divide por un parámetro, así que sigue siendo normal ⇒ **Z**.
- **Población:** infinita (proceso productivo).

### a) Hipótesis, tamaño de muestra, CR y RD

**1. Hipótesis.** Criterio pesimista: modificar el proceso es una inversión con riesgo económico, y lo grave es modificarlo cuando no mejora (error de tipo I).

- $H_0: \mu \le 4{,}2$ piezas/min. La modificación no aumenta la productividad.
- $H_1: \mu > 4{,}2$ piezas/min. La modificación aumenta la productividad.

**2. Riesgos, en términos del problema.**

- $1-\alpha = 0{,}99$ = P(no modificar | la modificación no aumenta la productividad) ⇒ $\alpha = 0{,}01$ = P(modificar | no la aumenta).
- $1-\beta = 0{,}95$ = P(modificar | $\mu = 5{,}8$) ⇒ $\beta = 0{,}05$ = P(no modificar | $\mu = 5{,}8$).

**3. Tamaño de muestra** (con $Z_{(0,99)} = 2{,}3263$ y $Z_{(0,95)} = 1{,}6449$):

$$n = \left[\frac{(Z_{(0,99)}+Z_{(0,95)})\,\sigma}{\mu_1-\mu_0}\right]^2 = \left[\frac{(2{,}3263+1{,}6449)\cdot 2{,}53}{5{,}8-4{,}2}\right]^2 = 39{,}4316 \;\Rightarrow\; \boxed{n = 40 \text{ minutos de producción}}$$

**4. Valor crítico** ($\sigma/\sqrt{n} = 2{,}53/\sqrt{40} = 0{,}4000$):

$$\bar x_c = \mu_0 + Z_{(0,99)}\cdot\frac{\sigma}{\sqrt n} = 4{,}2 + 2{,}3263\cdot 0{,}4000 = \mathbf{5{,}1306\ \text{piezas/min}}$$

**5. Condición de rechazo.** Si $\bar x > 5{,}1306$ piezas/min ⇒ se rechaza $H_0$.

**6. Regla de decisión.** *"Se mide la productividad del sistema modificado en 40 minutos. Si la productividad promedio supera 5,1306 piezas/min, se implementa la modificación; si no, se mantiene el sistema actual."*

### b) Probabilidad de no modificar si μ = 4,98

No modificar es no rechazar $H_0$ cuando la media real es 4,98 piezas/min: es el error de tipo II evaluado en ese valor (se usa el crítico con todos sus decimales).

$$\beta = \Phi\!\left(\frac{\bar x_c-4{,}98}{\sigma/\sqrt n}\right) = \Phi\!\left(\frac{5{,}1306-4{,}98}{0{,}4000}\right) = \Phi(0{,}3765) = \boxed{0{,}6467}$$

**Conclusión:** si con la modificación la productividad media es 4,98 piezas/min, la probabilidad de no hacer la modificación es 0,6467. La mejora real (0,78 piezas/min) es bastante menor que la de 1,6 para la que se diseñó el ensayo, y por eso la potencia ($1-\beta = 0{,}3533$) es baja.

### c) Intervalo del 99 % para la proporción de piezas malas

- **Variable:** atributo de Bernoulli de cada pieza (mala o buena). Parámetro $p$: proporción de piezas malas del proceso.
- **Método:** la estimación de $p$ es **siempre exacta** (binomial o F). La aproximación normal no se usa para estimar: el profesor la llama "aberración" y fue uno de los errores más penalizados del 1° parcial.
- Con $n = 40$ y 10 piezas **sin defectos**, hay $r = 30$ piezas malas, $\hat p = 30/40 = 0{,}75$. $1-\alpha = 0{,}99$ ⇒ $\alpha/2 = 0{,}005$.

**Límite inferior** ($\nu_1 = 2n-2r+2 = 22$, $\nu_2 = 2r = 60$; $F_{(0,995;\,22;\,60)} = 2{,}3346$):

$$A = \frac{1}{1 + \dfrac{(n-r+1)\cdot F}{r}} = \frac{1}{1 + \dfrac{11\cdot 2{,}3346}{30}} = 0{,}5387$$

**Límite superior** ($\nu_1 = 2r+2 = 62$, $\nu_2 = 2n-2r = 20$; $F_{(0,995;\,62;\,20)} = 2{,}9089$):

$$B = \frac{1}{1 + \dfrac{n-r}{(r+1)\cdot F}} = \frac{1}{1 + \dfrac{10}{31\cdot 2{,}9089}} = 0{,}9002$$

$$\boxed{P(0{,}5387 \le p \le 0{,}9002) = 0{,}99}$$

**Conclusión:** con un 99 % de confianza, el porcentaje de piezas malas fabricadas está entre el 53,87 % y el 90,02 % (se informa en % porque el enunciado pide un porcentaje; la probabilidad del intervalo es 0,99).

> **Nota:** si el enunciado original decía "10 piezas **defectuosas**" (la versión más habitual de esta consigna), entonces $r = 10$, $\hat p = 0{,}25$, y con los mismos fractiles intercambiados: $A = 1/[1 + 31\cdot 2{,}9089/10] = 0{,}0998$ y $B = 1/[1 + 30/(11\cdot 2{,}3346)] = 0{,}4613$, es decir $P(0{,}0998 \le p \le 0{,}4613) = 0{,}99$ (entre el 9,98 % y el 46,13 %).

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

- **Variable:** $X$ = peso de un conejo del lote, en kg. Se supone $X$ normal.
- **Distribución:** $\sigma$ no es dato; se usa el desvío muestral $S$, que es una variable aleatoria. Al estandarizar $\bar x$ dividiendo por $S$ (raíz de una $\chi^2$) queda una **t de Student** con $\nu = n-1 = 19$, sea cual sea $n$. Para la varianza, **χ²** con $\nu = 19$.
- **Estimadores** (con la calculadora, $n = 20$):

| Estimador | Valor |
|---|---|
| $\bar x$ | 4,8210 kg |
| $S$ | 0,3939 kg |
| $S^2$ | 0,1551 kg² |

### a) ¿Son concluyentes los datos para faenar?

Se faena solo si se cumplen **las dos** condiciones. Lo grave es faenar equivocadamente (riesgo de 0,01 que fija el enunciado), así que eso es el error de tipo I de cada ensayo: en $H_0$ va "no se cumple la condición" y la condición para faenar va en $H_1$. Se usa $\alpha = 0{,}01$ en cada ensayo (supuesto: el enunciado da un único riesgo y no dice cómo repartirlo).

#### Ensayo sobre la media

1. **Hipótesis:** $H_0: \mu \le 4{,}6$ kg (el lote no pesa en promedio más de 4,6 kg) · $H_1: \mu > 4{,}6$ kg.
2. **Riesgo:** $\alpha = 0{,}01$ = P(faenar | $\mu \le 4{,}6$).
3. **Valor crítico** ($t_{(0,99;\,19)} = 2{,}5395$; $S/\sqrt n = 0{,}3939/\sqrt{20} = 0{,}0881$):
   $$\bar x_c = 4{,}6 + 2{,}5395\cdot\frac{0{,}3939}{\sqrt{20}} = 4{,}8237 \text{ kg}$$
4. **CR:** si $\bar x > 4{,}8237$ kg ⇒ se rechaza $H_0$.
5. **RD:** *"Se pesan 20 conejos al azar. Si el peso promedio supera 4,8237 kg, la condición del peso para faenar se cumple; si no, no."*
6. **Estimador:** $\bar x = 4{,}8210$ kg.
7. **Conclusión:** $4{,}8210$ no es mayor que $4{,}8237$, así que **no se rechaza $H_0$**: no hay evidencia suficiente para asegurar que el peso promedio del lote supere 4,6 kg. El estimador queda muy cerca del crítico, pero el límite es estricto.

#### Ensayo sobre el desvío estándar

1. **Hipótesis:** $H_0: \sigma \ge 0{,}55$ kg (el desvío del lote no es menor a 0,55 kg) · $H_1: \sigma < 0{,}55$ kg. Unilateral, como todo ensayo de varianza; se trabaja con varianzas: $\sigma_0^2 = 0{,}3025$ kg².
2. **Riesgo:** $\alpha = 0{,}01$.
3. **Valor crítico** ($\chi^2_{(0,01;\,19)} = 7{,}6327$):
   $$S^2_c = \frac{\sigma_0^2\cdot\chi^2_{(0,01;\,19)}}{\nu} = \frac{0{,}3025\cdot 7{,}6327}{19} = 0{,}1215 \text{ kg}^2 \;\Rightarrow\; S_c = \sqrt{0{,}1215} = 0{,}3486 \text{ kg}$$
4. **CR:** si $S < 0{,}3486$ kg ⇒ se rechaza $H_0$.
5. **RD:** *"Si el desvío de los pesos de los 20 conejos es menor que 0,3486 kg, la condición del desvío para faenar se cumple; si no, no."*
6. **Estimador:** $S = 0{,}3939$ kg.
7. **Conclusión:** $0{,}3939$ no es menor que $0{,}3486$, así que **no se rechaza $H_0$**: no hay evidencia suficiente para asegurar que el desvío del lote sea menor a 0,55 kg.

#### Conclusión general

Con un riesgo de 0,01 de faenar equivocadamente, **los datos no son concluyentes para realizar la faena**: no se puede asegurar que el peso medio supere 4,6 kg ni que el desvío sea menor a 0,55 kg, así que conviene **esperar**.

### b) Probabilidad de no detectar que σ = 0,3 kg

Es el error de tipo II del ensayo del desvío evaluado en $\sigma_1 = 0{,}3$ kg ($\sigma_1^2 = 0{,}09$ kg²): la probabilidad de no rechazar $H_0$ ($S^2 \ge S^2_c$) cuando en realidad $\sigma = 0{,}3$. En el caso 2, β es la acumulada derecha:

$$\beta = G_{\chi^2}\!\left(\frac{\nu\cdot S^2_c}{\sigma_1^2};\ 19\right) = G_{\chi^2}\!\left(\frac{19\cdot 0{,}121521}{0{,}09};\ 19\right) = G_{\chi^2}(25{,}6545;\ 19) = \boxed{0{,}1401}$$

**Conclusión:** la probabilidad de no detectar que el desvío del lote es 0,3 kg (y no faenar) es 0,1401.

### c) Intervalos de confianza del 99 %

**Peso promedio** ($t_{(0,995;\,19)} = 2{,}8609$):

$$e = t_{(0,995;\,19)}\cdot\frac{S}{\sqrt n} = 2{,}8609\cdot\frac{0{,}3939}{\sqrt{20}} = 0{,}2520 \text{ kg}$$

$$\boxed{P(4{,}5690 \text{ kg} \le \mu \le 5{,}0730 \text{ kg}) = 0{,}99}$$

**Desvío estándar** ($\chi^2_{(0,995;\,19)} = 38{,}5823$ y $\chi^2_{(0,005;\,19)} = 6{,}8440$):

$$A' = \sqrt{\frac{19\cdot 0{,}1551}{38{,}5823}} = 0{,}2764 \text{ kg} \qquad B' = \sqrt{\frac{19\cdot 0{,}1551}{6{,}8440}} = 0{,}6563 \text{ kg}$$

$$\boxed{P(0{,}2764 \text{ kg} \le \sigma \le 0{,}6563 \text{ kg}) = 0{,}99}$$

(Límite inferior redondeado hacia abajo y superior hacia arriba.)

**Conclusión:** con un 99 % de confianza, el peso promedio del lote está entre 4,5690 y 5,0730 kg, y su desvío estándar entre 0,2764 y 0,6563 kg.

### d) Conejos adicionales para reducir el error un 15 %

- Error actual: $e = 0{,}2520$ kg. Error nuevo: $e' = 0{,}85\cdot 0{,}2520 = 0{,}2142$ kg.
- Como $t$ depende de $\nu = n-1$, el $n$ se calcula **iterando** $n = (t_{(0,995;\,n-1)}\cdot S/e')^2$, arrancando con un $n$ bastante mayor que el de la muestra (20):

| Iteración | $n$ de entrada | $t_{(0,995;\,n-1)}$ | $n = (t\cdot S/e')^2$ | $n$ de salida |
|---|---|---|---|---|
| 1 | 40 | 2,7079 | 24,7997 | 25 |
| 2 | 25 | 2,7969 | 26,4571 | 27 |
| 3 | 27 | 2,7787 | 26,1134 | 27 |

$$\boxed{n = 27 \Rightarrow \text{se deben pesar } 27 - 20 = 7 \text{ conejos más}}$$

> La versión anterior de este archivo daba $n = 28$ (8 más) sin iterar, dejando fijo el $t$ de 19 grados de libertad. El profesor exige el método iterativo y mostrar las iteraciones.
