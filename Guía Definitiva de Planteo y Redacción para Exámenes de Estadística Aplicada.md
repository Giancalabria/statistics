### Metodología Definitiva para la Resolución de Exámenes de Estadística Aplicada (Cátedra Dopazo \- García)

Esta guía resume cómo plantear y redactar los problemas del examen. **Lo que dice el profesor en clase manda** sobre esta guía, la Guía de Problemas y el apunte (resumen en `estadistica/REGLAS_PROFESOR.md`, clases del 06/08 al 22/10/2026). El profesor corrige la interpretación, no solo los números: «Si falta alguno de esos elementos, considero que el problema está mal hecho, aunque los números estén bien». Los problemas se resuelven como en clase, mostrando el desarrollo y las iteraciones.

#### 1\. Fase de Diagnóstico: Identificación de Variables y Contexto Inicial

Antes de cualquier cálculo hay que transformar el enunciado en un modelo:

* **Definición de la Variable Aleatoria (**  **\$X**\$  **):**  el fenómeno en estudio, en palabras y con sus condiciones (ej. «consumo de combustible de un vehículo en una corrida», no «litros de cualquier cosa»). «Si no define la variable de estudio no sabe cómo sacar la muestra».  
* **Unidad de Medida:**  va en la variable, en los límites, en los críticos, en n («11 piezas») y en las varianzas (mm², g²).  
* **Muestras:**  todas las muestras de los problemas se suponen al azar; no hace falta discutir el tipo de muestreo.  
* **Clasificación de la Población:**  si se conoce \$N\$, se usan las ecuaciones de población finita (siempre, sin umbral de n/N). Bernoulli es siempre población infinita o proceso.  
* **Parámetros vs. Estimadores:**  el **parámetro** ( \$\\mu, \\sigma^2, p\$ ) es una constante fija y desconocida (letras griegas; p es la excepción); el **estimador** ( \$\\bar{x}, S^2, \\hat{p}\$ ) es una variable aleatoria (letras latinas). Las hipótesis y los supuestos se hacen siempre sobre parámetros, nunca sobre la muestra.

#### 2\. El Planteo de las Hipótesis: Criterios Pesimista y Optimista

* **Regla madre:**  \$H\_0\$ se plantea de modo que el **error de tipo I sea el más grave**.  
* **Orden para decidir:**  (1) si el enunciado dice qué se quiere probar, eso va en \$H\_1\$; (2) si no, el criterio; (3) si no alcanza, comparar la gravedad de los errores.  
* **Primero en palabras, después en símbolos.** La igualdad va siempre en \$H\_0\$. No asociar el criterio con ≤ o ≥.

| Criterio | Cuándo | Qué va en \$H\_0\$ |
| \------ | \------ | \------ |
| **Pesimista** | Riesgo económico: inversión, máquina o proveedor nuevo, producto nuevo, modificación, campaña publicitaria (aunque sea barata, si se quiere probar que fue efectiva). | «No funciona / no cumple». El cambio o la mejora va en \$H\_1\$. Ej. I-10: \$H\_0: \\mu \\ge 11,2\$ (el aditivo no reduce el consumo). |
| **Optimista** | Control de proceso, recepción de un **proveedor habitual**, controles de rutina. | «Cumple / está bajo control». Rechazar \$H\_0\$ = detener el proceso o rechazar el lote. Ej. I-8: \$H\_0: \\mu \\ge 250\$ g. |

* **Unilaterales:**  no existen bilaterales en \$\\sigma^2\$, \$\\sigma\$, \$p\$ ni en comparaciones de dos poblaciones. En \$\\mu\$, bilateral solo si el enunciado lo impone («diferente de», valor exacto).  
* **α:**  si no está en el enunciado, se elige y se justifica (chico ≤ 0,01, estándar 0,05, grande ≥ 0,10). Una vez fijado, no se toca. Nunca se fija después de ver la muestra ni se decide con el p-value.  
* **Las 4 probabilidades** (\$\\alpha\$, \$1-\\alpha\$, \$\\beta\$, \$1-\\beta\$) se escriben en términos del problema: \$\\alpha\$ = P(lanzar el aditivo | no reduce el consumo).

#### 3\. Los Pasos del Ensayo (en este orden)

1. **Variable**  en palabras, con unidad.  
2. **Hipótesis**  \$H\_0\$ y \$H\_1\$, con el criterio justificado en palabras.  
3. **Riesgos:**  \$\\alpha\$ (y \$\\beta\$ en el valor alternativo, si corresponde).  
4. **Tamaño de muestra**  \$n\$, si no está dado.  
5. **Valor crítico, Condición de Rechazo (CR) y Regla de Decisión (RD)**, antes de ver la muestra. La RD va en lenguaje de planta: «Si en 1637 encuestados hay 229 o más interesados, se inicia una nueva campaña».  
6. **Estimador**  de la muestra ( \$\\bar x\$, \$S\$, \$r\$, \$J\$, \$D\$ ).  
7. **Comparar el estimador contra el valor crítico y concluir.**  Se compara en unidades de la variable; nunca contra \$\\mu\_0\$ y nunca con estadísticos «observados» (Z, t, F o χ²) contra la tabla.

#### 4\. Criterios de Selección de Distribuciones

* **Fundamento de Z o t** (por la estructura, no por «conozco σ» / «no conozco σ»): \$\\bar{x}\$ es normal; al estandarizar dividiendo por un parámetro ( \$\\sigma\$ ) sigue siendo normal \$\\Rightarrow Z\$. Si se divide por \$S\$, que es una variable aleatoria (raíz de una \$\\chi^2\$), queda una **t de Student** con \$\\nu \= n-1\$, **sea cual sea n**. La regla «n ≥ 30 ⇒ normal» no se usa.  
* **Población finita:**  factor \$\\sqrt{\\frac{N-n}{N-1}}\$ siempre que se conoce \$N\$ (también en críticos, β y n).  
* **Valor Total Poblacional:**  \$\\tau \= \\mu \\cdot N\$.  
* **Chi-cuadrado:**  inferencia sobre la varianza (siempre con varianzas; los desvíos se elevan al cuadrado) y contrastes de frecuencias.  
* **Proporción p:**  la estimación es **siempre exacta** (binomial o F); las aproximaciones normal y Poisson sirven solo para calcular n, justificadas con el n resultante (normal si \$np > 10\$ y \$n(1-p) > 10\$; Poisson si \$p \\le 0,005\$; si no queda claro, criterio de Mermoz \$n\_0 \= 0,23(1-p)^2/p^3\$).  
* **Ecuación de García** (n para varianzas): \$\$\\nu \= \\frac{2}{9}\\left(a \+ \\sqrt{a^2 \+ 1}\\right)^2\$\$ con \$\\nu\$ al entero superior y \$n \= \\nu \+ 1\$. En estimación, \$a \= \\frac{Z\_{1-\\alpha/2} (\\sqrt\[3\]{R} \+ 1)}{2(\\sqrt\[3\]{R} \- 1)}\$; en ensayos, \$\\sqrt\[3\]{R}\$ multiplica a un solo Z (caso 1: \$a \= \\frac{Z\_{1-\\alpha} \+ Z\_{1-\\beta}\\sqrt\[3\]{R}}{2(\\sqrt\[3\]{R} \- 1)}\$). \$R\$ es siempre de varianzas (con desvíos, \$R \= R'^2\$).

#### 5\. Reglas de Cierre: Redondeo, Probabilidades y Conclusión

* **Decimales:**  mínimo 4 en todo el desarrollo y en los fractiles; los periódicos como fracción. El resultado final se expresa según la variable.  
* **Probabilidades:**  siempre entre 0 y 1, nunca en % («El primero que me ponga 30% de probabilidad, olvídate de aprobar»). Se admite «95 % de confianza».  
* **Redondeo:**  n y ν al entero superior (ν de Welch se trunca); en los intervalos, el límite inferior hacia abajo y el superior hacia arriba; en discretas, el valor crítico que deja α real ≤ α.  
* **Un solo límite** («mínimo», «máximo»): α entero, sin dividir por 2.  
* **Conclusión:**  se refiere al parámetro, en el contexto del problema. «Se rechaza \$H\_0\$: puedo asegurar que…» o «No se rechaza \$H\_0\$: no hay evidencia suficiente para asegurar que…». Nunca «acepto \$H\_0\$» ni «el producto es malo». La decisión de planta (rechazar el lote, lanzar el producto) va en la RD.

###### *Ejemplo de Conclusión*

**«Como \$\\bar x \= 10,6\$ L no es menor que \$\\bar x\_c \= 10,52\$ L, no se rechaza \$H\_0\$: con esta muestra no hay evidencia suficiente para asegurar que el aditivo reduzca el consumo medio de combustible.»** (I-10, resuelto en clase.)
