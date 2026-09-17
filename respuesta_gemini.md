La idea de armar una webapp liviana (por ejemplo, usando Python con Streamlit o Flask) que corra de manera local es **excelente** y está totalmente alineada con lo que pide la cátedra. El profesor menciona explícitamente: *"Voy a decir que programen en Python. ¿Cuál es el problema? Y hagan sus propios programas para resolver los problemas"*. Además, destaca que un ingeniero del siglo XXI debe saber usar la computadora para procesar datos en lugar de hacer cálculos manuales con tablas.

Para empezar a armar la lógica de tu aplicación, vamos a tomar el **Ejercicio 6 de la página 3**, sugerido por el profesor, el cual pide **estimar la media poblacional cuando el desvío estándar de la población ($\sigma$) es desconocido**.

Aquí te explico paso a paso la teoría, el por qué, y cómo deberías programar la lógica (el algoritmo) en tu webapp.

### El Problema: Estimación de la Media con Varianza Desconocida

**¿Por qué este caso?** En la vida real, es casi imposible conocer el desvío estándar exacto de toda una población ($\sigma$). Lo que hacemos es extraer una muestra, calcular su promedio ($\bar{x}$) y su desvío estándar ($S$), y usar esos datos para estimar la realidad.

#### 1. Diccionario de Variables para tu App

Tu aplicación deberá pedirle al usuario que ingrese los siguientes datos (Inputs):

* **$\bar{x}$ (Media muestral):** Es el promedio de los datos de la muestra que sacaste.
* **$S$ (Desvío estándar muestral):** Es la dispersión de tu muestra. Como no conoces $\sigma$ (el desvío de la población), usas $S$ como su mejor estimador.


* **$n$ (Tamaño de la muestra):** La cantidad de elementos que mediste.
* **$1 - \alpha$ (Nivel de confianza):** La probabilidad (ej. 0.95 o 95%) de que los límites que vas a calcular efectivamente contengan a la media real.



#### 2. La Lógica Interna (Lo que hará tu código)

Una vez que el usuario ingresa esos datos, tu código debe calcular los límites. Aquí entra la teoría fuerte:

* **Paso A: Calcular los Grados de Libertad ($\nu$)**
* **Fórmula:** $\nu = n - 1$.


* **¿Por qué?** Porque al usar $S$ en lugar de $\sigma$, pierdes un "grado de libertad" en tu información matemática.




* **Paso B: Buscar el Valor Crítico de "t de Student"**
* **Teoría:** Como no conoces $\sigma$, **jamás debes usar la distribución Normal ($Z$)**. Debes usar la distribución "t de Student", la cual es más achatada y dispersa que la Normal para compensar la incertidumbre adicional que genera no conocer la población real.


* **En tu código:** No dependerás de tablas ni de internet. En Python, usarás la librería `scipy` (que funciona offline). El código sería algo como `scipy.stats.t.ppf(1 - alpha/2, df)`.


* **Paso C: Calcular el Error Muestral ($e$)**
* **Fórmula:** $e = t \cdot \frac{S}{\sqrt{n}}$.


* **¿Qué significa?** Es la precisión de tu estimación; el margen de error (el "más/menos") que le aplicarás a tu promedio.




* **Paso D: Calcular los Límites de Estimación (A y B)**
* **Límite Inferior (A):** $A = \bar{x} - e$.


* **Límite Superior (B):** $B = \bar{x} + e$.


* **Resultado final:** Le mostrarás al usuario que la media poblacional $\mu$ se encuentra entre los valores $[A, B]$ con una confianza del $(1 - \alpha)$%.





---

### La "Joya" para tu WebApp: El Método Iterativo para calcular $n$

El profesor hace muchísimo énfasis en un problema clásico de ingeniería: a veces no te dan $n$, sino que te exigen que el error muestral ($e$) sea uno en particular, y te preguntan **qué tamaño de muestra ($n$) necesitas**.

Si intentas despejar $n$ de la fórmula del error, te queda:
$n = \left( \frac{t \cdot S}{e} \right)^2$.

**¿Cuál es el problema teórico aquí?**
Que el valor de $t$ depende de los grados de libertad ($\nu$), y los grados de libertad dependen de $n$ ($\nu = n - 1$). Es decir, ¡tienes $n$ de ambos lados de la ecuación! No puedes calcular $n$ si no sabes con qué valor de $t$ entrar, y no tienes $t$ si no sabes $n$.

**La solución: El Método Iterativo (Prueba y Error)**
Esto es ideal para programarlo en tu aplicación con un bucle `while`. Así es como lo explica el profesor y como debes codificarlo:

* **Iteración 1:** El código "adivina" un valor grande de $n$ (el profesor sugiere arrancar con $n = 100$ o asumir población infinita donde $t \approx Z$).


* **Iteración 2:** Con ese $n=100$, calcula los grados de libertad ($\nu = 99$), busca el valor de $t$ (que dará aprox 1.9842) y resuelve la ecuación. Esa cuenta te dará un nuevo valor de $n$ (por ejemplo, $n = 13$).


* **Iteración 3:** Ahora tu código toma ese $n=13$, calcula un nuevo $\nu = 12$, busca el nuevo $t$, y vuelve a calcular la ecuación.


* **Condición de corte:** El bucle se detiene cuando el $n$ que entra a la ecuación es exactamente igual al $n$ que sale como resultado. El profesor garantiza que este método es tan potente que nunca necesita más de 3 iteraciones para llegar al resultado final.



Al tener esto programado, en el examen solo tendrás que ingresar tu Error ($e$), tu Desvío ($S$) y tu Confianza ($\alpha$), y tu programa hará el bucle en milisegundos, dándote el $n$ exacto sin que tengas que iterar manualmente con la calculadora.

¿Se entiende bien la diferencia entre los parámetros de la realidad ($\mu$, $\sigma$) que nunca vemos, y los de nuestra muestra ($\bar{x}$, $S$) que usamos como evidencia? Si quieres, podemos armar la estructura lógica para los **Ensayos de Hipótesis** que es el siguiente tema fuerte.