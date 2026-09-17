# PLAN.md — App de Resolución de Ejercicios de Estadística Aplicada

> Estado: **Fase 0 y Fase 1 (M1 — Intervalos de Confianza) implementadas y testeadas.** Ver §7 para el detalle de fases.
> Fuentes: `esquema_teorico_examen_estadistica.md` (spec matemática, fuente de verdad de fórmulas) y `respuesta_gemini.md` (confirma arquitectura y detalla el caso IC-media-σ-desconocida + método iterativo de n).

---

## 1. Objetivo

Construir una aplicación **100% local**, en **Python**, con una interfaz simple tipo formulario, que resuelva los 4 bloques de ejercicios del primer examen de Estadística Aplicada, mostrando no solo el número final sino el razonamiento (caso elegido, fórmula usada, redacción formal del resultado), tal como la pide la cátedra.

No es una calculadora genérica: es un **solver guiado por árbol de decisión** — el usuario no elige la fórmula, elige qué sabe (¿conoce σ? ¿es bilateral o unilateral? ¿las varianzas son iguales?) y la app decide qué camino tomar, igual que tendría que razonarlo un alumno en el examen.

---

## 2. Alcance funcional

### 2.1 Incluido en el MVP (mapeado 1 a 1 con `esquema_teorico_examen_estadistica.md`)

| Módulo | Contenido | Sección del esquema |
|---|---|---|
| **M1 — Intervalos de Confianza** | Media (σ conocido/desconocido, población finita/infinita, cálculo de n incl. bucle iterativo con t) · Varianza/Desvío (χ²) · Proporción (**exacto Clopper-Pearson** + aprox. normal como referencia + cálculo de n) | §1.1, 1.2, 1.3 |
| **M2 — Ensayo de Hipótesis (1 población)** | Media con σ conocido (cola der./izq./bilateral, β, potencia, n para potencia fijada) · Media con σ desconocido (t) · Varianza (χ²) · **Proporción (Binomial exacto, cola der./izq./bilateral)** | §2 + extensión (ver nota) |
| **M3 — Comparación de 2 poblaciones** | Test F de igualdad de varianzas (paso obligatorio previo) · IC/ensayo de diferencia de medias con varianzas iguales (pooled) · Welch (varianzas distintas, ν_AW) · **Muestras apareadas (t sobre diferencias)** | §3 + extensión (ver nota §2.2b) |
| **M4 — Contrastes χ²** | Bondad de ajuste (con agrupación manual si Fe_i<5) · Tablas de contingencia (independencia/homogeneidad/**comparación de 2+ proporciones — método principal de la cátedra para esto, ver §2.2b**) | §4 |
| **Redacción formal** | Cada resultado se muestra con la notación `P(A ≤ parámetro ≤ B) = 1-α` o la frase de decisión de hipótesis, no solo el número | §5, reglas de la app |

### 2.2 CORRECCIÓN IMPORTANTE (post-validación) — proporciones usan el modelo EXACTO, no la aproximación normal

Al validar M1 contra la guía real de la cátedra (`D:\UADE\Estadistica\OneDrive_2_23-8-2026\Guia Problemas Estadística Aplicada 2026.pdf`, TEMA III) se encontró que la suposición original de este plan era **incorrecta**: la cátedra aclara explícitamente en TEMA III *"Todos los resultados están calculados de manera exacta y se indican los resultados calculados de manera aproximada, si correspondiera en cada caso"*. Es decir, para proporciones el método **principal** es el exacto (Binomial / transformación F, equivalente a Clopper-Pearson), y la aproximación normal es solo secundaria (se usa cuando no hay forma cerrada exacta, p. ej. para calcular n).

Esto ya se corrigió en M1 (`solver/intervals.py`): `ic_proporcion_exacto(r, n, alpha)` es el método principal (validado contra 8 ejercicios reales de la guía, con IC exactos por Clopper-Pearson vía `scipy.stats.beta`), y `ic_proporcion_normal(p_hat, n, alpha)` quedó como comparación secundaria. `n_proporcion` sigue usando la aproximación normal porque no existe forma cerrada exacta para tamaño de muestra (así lo hace la propia guía).

**Implicancia para M2 (ensayo de hipótesis de 1 proporción, Fase 2):** también debe usarse el modelo exacto binomial como método principal, no la aproximación Z por analogía que este plan proponía originalmente. El algoritmo verificado contra 3 ejercicios reales (ver `TEMA III`, problemas 12, 13, 15) es:

- **Cola derecha (H0: p ≤ p0)**: $r_c$ = mínimo entero tal que $P(X \ge r_c \mid n, p_0) \le \alpha$, calculado como `1 - binom.cdf(r_c - 1, n, p0)`. CR: se rechaza H0 si $r_{muestra} \ge r_c$. Potencia/β para una alternativa $p_1$: $\beta = P(X \le r_c - 1 \mid n, p_1)$ = `binom.cdf(r_c - 1, n, p1)`.
- **Cola izquierda (H0: p ≥ p0)**: por simetría, $r_c$ = máximo entero tal que $P(X \le r_c \mid n, p_0) \le \alpha$ (`binom.cdf(r_c, n, p0) <= alpha`). CR: se rechaza si $r_{muestra} \le r_c$.
- **Bilateral**: se reparte α/2 en cada cola con la misma lógica.
- El valor "a posteriori" (α* o p-valor) para un $r$ observado es directamente $P(X \ge r \mid n, p_0)$ (cola derecha) o $P(X \le r \mid n, p_0)$ (cola izquierda).
- $r_c$ se encuentra con una búsqueda simple (incrementar/decrementar r desde 0), no con una fórmula cerrada — mismo espíritu que el bucle iterativo de n en M1.

Verificado numéricamente: ejercicio 15a (n=30, p0=0,70, α=0,05) da $r_c=26$ ✓; ejercicio 12 (n=739, p0=0,11, α=0,05, p1=0,16) da $r_c=96$ y β=0,0098 ✓; ejercicio 13 (n=100, p0=0,05, $r_c$=9 dado) da α=0,0631 ✓.

### 2.2b CORRECCIÓN DE ALCANCE (post-investigación) — M3 pierde "comparación de 2 proporciones", M3 gana "muestras apareadas"

Al revisar TEMA IV, V y VI de la guía (antes de delegar Fase 3) se encontraron dos correcciones de alcance:

**1) La "comparación de 2 proporciones" NO se enseña como test Z independiente — se enseña como contraste χ² (TEMA VI).** El propio TEMA VI se titula *"CONTRASTES CHI-CUADRADO... Pruebas de Consistencia: Comparación en Bernoulli"* y el ejercicio 1 de esa sección compara 2 proporciones armando una tabla de contingencia 2×k (filas = atributos/resultados posibles, columnas = los 2 grupos a comparar) y aplicando el mismo χ² de bondad de independencia que ya estaba previsto para M4. El propio texto muestra el método Z (aproximación normal) y un método exacto (Fisher/hipergeométrico, funciones "Fh/Gh") solo **"a modo ilustrativo"** — el método principal enseñado es el χ². Conclusión: la fórmula Z "por analogía" que este plan tenía en §2.2 para comparación de 2 proporciones se elimina del alcance de M3; **cuando aparezca ese caso en un ejercicio, resolverlo con M4 (tabla de contingencia 2×k)**, que ya cubre exactamente este uso. No se pierde funcionalidad, se corrige dónde vive.

**2) "Muestras apareadas" (paired samples) SÍ es parte explícita de TEMA V** (el título completo es *"COMPARACIÓN DE DOS MEDIAS POBLACIONALES. MUESTRAS INDEPENDIENTES Y MUESTRAS APAREADAS"*), con un caso de uso claro: cuando la comparación se hace sobre la misma unidad experimental (ej. mismo trabajador con 2 métodos, mismo lote medido en 2 condiciones), se trabaja con las diferencias $d_i = X_{1i} - X_{2i}$ y se aplica un ensayo de una sola muestra sobre $\bar{d}$, $S_d$, con $\nu = n-1$ (n = cantidad de pares, no de observaciones sueltas) — es decir, es una reutilización directa del caso "media, σ desconocido" de M1/M2, no una fórmula nueva. Esto se agrega al alcance de M3.

**Fórmulas verificadas para M3 (con ejercicios reales, ver §2.3):**
- **Test F (igualdad de varianzas)**: $j^2_c = F_{(1-\alpha/2;\, n_{may}-1,\, n_{men}-1)}$ tomando la muestra de mayor varianza en el numerador (igual que en el esquema teórico §3.1), pero la guía también pide a veces el IC de la razón de varianzas en ambos sentidos ($\phi^2$ y $1/\phi^2$) y el cálculo de n igualando tamaños de muestra en ambos grupos (fórmula iterativa con F, no cerrada).
- **Medias, varianzas iguales (pooled)**: $S_p^2$, $\nu=n_1+n_2-2$, todo igual al esquema §3.2 CASO A. Verificado con ejercicio NDMA (TEMA V, problema 1): $S_a=0,9828$, $d_c=1,0064$, $d_{muestra}=3,75$ → rechaza; IC 90%: entre 3,06 y 4,44; n para reducir error a la mitad → n=45.
- **Medias, varianzas distintas (Welch)**: igual al esquema §3.2 CASO B. Verificado con ejercicio hiladora (TEMA V, problema 3/4): $\nu_{AW}=14$ (truncado de 14,2641), $d_c=194,4494$, $d_{muestra}=262$ → rechaza; IC 90%: entre 67,55 y 456,45 m.
- **Muestras apareadas**: verificado con ejercicio armado de circuitos (TEMA V, problema 17): $\bar{d}=4,75$, $S_d=3,6936$, $\nu=7$ (n=8 pares), $d_c=4,4741$ (cola derecha, H0: δ≤2) → rechaza; IC 90%: entre 2,27 y 7,23 min; n para reducir error a un tercio → n=57.

### 2.2c Diseño de M4 (Chi-cuadrado) — no auto-ajusta distribuciones, recibe Fo/Fe ya calculados

La bondad de ajuste requiere calcular las frecuencias esperadas ($F_{e_i}$) para el modelo teórico que se está probando (Normal, Poisson, Weibull, etc.), lo cual implica estimar parámetros (ej. $\bar x$, $S$ para Normal) y evaluar la función de distribución en cada intervalo — es un cálculo separado y no trivial de generalizar para cualquier distribución. **Decisión de diseño**: M4 NO intenta ajustar la distribución por el usuario; recibe directamente las frecuencias observadas ($F_{o_i}$) y esperadas ($F_{e_i}$, ya calculadas por el usuario para el modelo que esté probando) más la cantidad de parámetros estimados $p$ (para el cálculo de $\nu=k-1-p$), y hace el resto: $\chi^2_c=\sum(F_{o_i}-F_{e_i})^2/F_{e_i}$, comparación contra $\chi^2_{(1-\alpha;\nu)}$, decisión, y el aviso de $F_{e_i}<5$ (validar y avisar, no agrupar solo — decisión ya tomada en §8). Esto es consistente con cómo ya funciona el resto de la app: el usuario aporta los insumos que ya sabe calcular, la app hace el álgebra/estadística de decisión.

Para tablas de contingencia (independencia/homogeneidad, incluida la comparación de 2+ proporciones que se corrigió en §2.2b), la app SÍ calcula las frecuencias esperadas automáticamente a partir de los totales de fila/columna de la tabla observada — eso no requiere ajustar ninguna distribución, es una cuenta directa ($E_{ij}=T_i \cdot T_j/T_T$).

**Ejercicios reales verificados (todos con $p=0$, ya que son ajustes a modelo uniforme o a proporciones históricas dadas, no estimadas de la muestra):**
- Dado cargado (bondad de ajuste, uniforme, k=6, n=60): $\chi^2_c=11,80$, $\nu=5$, $\chi^2_{crit}(0,95;5)=11,07$ → se rechaza (dado cargado).
- Instalaciones de aire acondicionado (uniforme, k=4, n=80): $\chi^2_c=2,00$, $\nu=3$, crit=7,81 → no se rechaza.
- Ventas de TV (proporciones históricas 40/40/20%, k=3, n=200): $\chi^2_c=5,625$, $\nu=2$, crit=5,99 → no se rechaza (caso límite, bueno para testear precisión).
- Contingencia 3×2 ocupación laboral (TEMA VI, problema 1 — comparación de 2 proporciones vía χ², ver §2.2b): $\chi^2_c=3,4476$ (dado explícitamente en la guía), $\nu=2$, crit=5,99 (α=0,05) → no se rechaza.
- Contingencia 3×4 preferencia de fragancias (TEMA VI, problema 9): $\chi^2_c=13,5075$ (dado explícitamente), $\nu=6$, crit=10,6446 (α=0,10) → se rechaza.

### 2.3 Fuente de validación real: guía de problemas de la cátedra

En `D:\UADE\Estadistica\OneDrive_2_23-8-2026\` está la guía oficial de problemas (`Guia Problemas Estadística Aplicada 2026.pdf`, 62 páginas), con ejercicios resueltos completos (no solo la respuesta final) para cada tema, organizados así: TEMA I = medias (IC + ensayos), TEMA II = varianzas (χ²), TEMA III = proporciones (Bernoulli/Binomial), TEMA IV = comparación de varianzas (F), TEMA V = comparación de medias, TEMA VI = contrastes χ². Esta guía es ahora la fuente primaria de casos de validación (golden tests), reemplazando a los ejemplos inventados a mano. El texto completo se extrajo a un archivo de trabajo para poder buscarlo por palabra clave sin reabrir el PDF en cada sesión.

### 2.4 Explícitamente fuera de alcance del MVP

- **Decisión por p-valor para medias/varianzas**: el esquema trabaja todo por valor crítico (`x̄ vs x̄_c`). No se agrega cálculo de p-valor en el MVP para no desviarse del método que pide la cátedra, pero es una extensión trivial de agregar después (mismo `scipy.stats.cdf`). (Para proporciones el "valor a posteriori" sí se implementa, ver §2.2, porque la guía lo pide explícitamente.)

---

## 3. Decisiones de arquitectura

- **Lenguaje**: Python 3.11+.
- **Cálculo numérico**: `scipy.stats` (Z, t, χ², F — `.ppf` para críticos, `.cdf` para β/potencia) + `numpy`. Todo offline, sin tablas ni llamadas externas.
- **Interfaz**: **Streamlit**. Corre local (`streamlit run app.py` → `localhost`), no requiere separar backend/frontend, widgets nativos para forms y selects (ideal para el árbol de decisión), soporta LaTeX (`st.latex`) para mostrar fórmulas — igual que exige la redacción formal del punto 5 del esquema.
  - Alternativa descartada: Flask (más control pero hay que escribir HTML/JS a mano — no aporta nada para este caso de uso). Tkinter descartado por UI más pobre para mostrar fórmulas/LaTeX.
- **Separación de responsabilidades**: la lógica matemática vive en un paquete `solver/` puro (sin imports de Streamlit), testeable de forma aislada. La capa Streamlit solo arma inputs, llama al solver y renderiza el resultado. Esto permite tests unitarios sin depender de la UI.
- **Sin persistencia / sin backend / sin red**: cada ejecución es stateless; no hay base de datos ni login. Nada sale de la máquina del usuario.

---

## 4. Estructura de proyecto propuesta

```
code/
├── esquema_teorico_examen_estadistica.md   (fuente de verdad matemática)
├── respuesta_gemini.md
├── PLAN.md
├── requirements.txt                         (streamlit, scipy, numpy)
├── app.py                                   (entry point Streamlit: menú de módulos M1-M4)
├── solver/
│   ├── __init__.py
│   ├── distributions.py     # wrappers finos sobre scipy.stats (z_crit, t_crit, chi2_crit, f_crit, etc.)
│   ├── intervals.py         # M1: IC media / varianza / proporción + cálculo de n (incl. bucle iterativo)
│   ├── hypothesis_one.py    # M2: ensayos 1 población (media, varianza, proporción)
│   ├── two_samples.py       # M3: test F, medias pooled, Welch, comparación de 2 proporciones
│   ├── chi_square.py        # M4: bondad de ajuste, contingencia
│   └── wording.py           # generación de la redacción formal de resultados
├── pages/                    # páginas Streamlit (una por módulo, multipage app)
│   ├── 1_Intervalos_de_Confianza.py
│   ├── 2_Ensayo_de_Hipotesis.py
│   ├── 3_Comparacion_2_Poblaciones.py
│   └── 4_Chi_Cuadrado.py
└── tests/
    ├── test_intervals.py
    ├── test_hypothesis_one.py
    ├── test_two_samples.py
    └── test_chi_square.py
```

---

## 5. Flujo de usuario (UX)

1. Pantalla principal: elegir módulo (M1–M4), reflejando el árbol de decisión de §5 del esquema.
2. Dentro del módulo, preguntas cerradas tipo wizard (radio buttons / selects) que replican el árbol:
   - M1: ¿Media, varianza o proporción? → ¿σ conocido? → ¿población finita? → ¿querés el IC o el tamaño de muestra n?
   - M2: ¿Media o varianza? → ¿σ conocido (solo aplica a media)? → ¿cola derecha/izquierda/bilateral? → ¿querés también β/potencia o n para potencia fijada?
   - M3: siempre arranca por el test F (obligatorio) → según resultado, la app **elige sola** pooled o Welch → IC o ensayo de diferencia.
   - M4: ¿bondad de ajuste o contingencia? → carga de tabla de frecuencias (Streamlit `st.data_editor` o inputs numéricos) → validación automática de Fe_i≥5 con aviso si hay que agrupar.
3. Inputs numéricos según el caso (x̄, S, n, N, α, μ₀, etc.).
4. Resultado en dos partes:
   - **Resultado numérico** (valores A/B, estadístico calculado, valor crítico).
   - **Redacción formal** (texto tipo el que pide la cátedra, con la notación matemática vía `st.latex`).

---

## 6. Estrategia de testing

Cada función de `solver/` se valida con **casos conocidos**, no solo con inputs arbitrarios:
- El ejemplo desarrollado en `respuesta_gemini.md` (IC media, σ desconocido, con el resultado numérico de la iteración: n=100→ν=99→t≈1.9842→n≈13) se usa como test de regresión del bucle iterativo.
- Ejercicios resueltos que el usuario tenga de la cátedra (guías, prácticas) se usan como golden tests adicionales a medida que se implementa cada módulo — el usuario deberá aportar 1-2 ejercicios con resultado conocido por módulo para validar antes de darlo por cerrado.
- Casos límite: n pequeño, Fe_i<5 sin agrupar (debe alertar, no calcular silenciosamente), varianzas iguales vs distintas en el límite de F_c.

---

## 7. Plan de fases (entregables incrementales)

- ✅ **Fase 0 — Setup**: estructura de carpetas, `requirements.txt`, `app.py` esqueleto con navegación entre módulos vacíos.
- ✅ **Fase 1 — M1 Intervalos de Confianza**: `solver/distributions.py` + `solver/intervals.py` + `solver/wording.py` + `pages/1_Intervalos_de_Confianza.py` implementados (media σ conocido/desconocido con bucle iterativo de n, varianza/desvío, proporción). **Validado contra ~15 ejercicios reales resueltos de `Guia Problemas Estadística Aplicada 2026.pdf`** (no solo casos inventados a mano) — esta validación encontró y corrigió el error de §2.2 (proporción debía usar el modelo exacto, no la aproximación normal). 32 tests en `tests/test_intervals.py` en verde, y UI verificada de punta a punta con `streamlit.testing.v1.AppTest`.
- ✅ **Fase 2 — M2 Ensayo de Hipótesis (1 población)**: `solver/hypothesis_one.py` + `pages/2_Ensayo_de_Hipotesis.py` + `tests/test_hypothesis_one.py` implementados (media Z y t, varianza χ², proporción binomial exacto — todas con cola derecha/izquierda/bilateral, β, potencia). Implementado por un subagente (modelo económico) y luego **revisado y corregido**: se encontró y arregló un bug real (β y potencia quedaban invertidos en el ensayo bilateral de proporción cuando se pasaba p1) con test de regresión agregado; se completó una función que había quedado sin exponer en la UI (`n_media_sigma_desconocido_para_potencia`, sin validar contra ejercicio real — queda anotado como extensión analógica). 44 tests en verde, validados contra ~9 ejercicios reales de la guía (torno automático bilateral, control de suelas, control de recepción de proporciones, riesgo del proveedor), y UI verificada de punta a punta con `AppTest` (7 escenarios, sin excepciones).
- ✅ **Fase 3 — M3 Comparación de 2 poblaciones**: `solver/two_samples.py` + `pages/3_Comparacion_2_Poblaciones.py` + `tests/test_two_samples.py` implementados (test F, pooled/Welch automático, muestras apareadas). Implementado por un subagente (modelo económico) y luego **revisado y corregido**: se encontró y arregló un bug real de convención — el test F que decide entre pooled y Welch NO es bilateral con F_(1-α/2) como decía el esquema teórico, sino **unilateral con F_(1-α) (α completo)**, verificado exactamente contra el desarrollo textual de dos ejercicios reales (NDMA: F_(0.90;11,11)=2.2269; hiladora: F_(0.90;15,3)=5.2003). Con la fórmula vieja, la decisión automática pooled-vs-Welch en la UI habría elegido el método equivocado para el caso hiladora. También se corrigió un test que mezclaba dos niveles de riesgo distintos del mismo ejercicio (el enunciado de la hiladora usa α=0.10 solo para decidir el método, pero α=0.05 para el ensayo de medias en sí) y se reemplazó un test mal atribuido (decía validar "aleación" contra un ejercicio real pero en realidad ese ejercicio es un test de razón desplazada j₀=0.8, no de igualdad de varianzas — se reemplazó por los dos casos reales NDMA/hiladora que sí corresponden al test F de igualdad). 12 tests en verde (66 totales en el proyecto), validados contra ejercicios reales de TEMA IV/V (dos tornos, aleación NDMA, hiladora, armado de circuitos), y UI verificada con `AppTest` incluyendo la decisión automática pooled/Welch end-to-end.
  - **Limitación conocida (documentada, no bloqueante)**: la UI usa un único campo de α tanto para el test F de decisión de método como para el ensayo/IC posterior. La mayoría de los ejercicios de la guía usan el mismo α para ambos pasos; el caso hiladora es una excepción donde el enunciado fija riesgos distintos (10% para decidir método, 5% para el ensayo) — en ese caso el usuario debe correr el test F aparte con su propio α y luego cambiar el campo antes de calcular el ensayo/IC.
- ✅ **Fase 4 — M4 Chi-cuadrado**: `solver/chi_square.py` + `pages/4_Chi_Cuadrado.py` + `tests/test_chi_square.py` implementados (bondad de ajuste con Fo/Fe provistos por el usuario, tablas de contingencia con Fe auto-calculado, validación de Fe_i≥5 y N≥60 como warnings no bloqueantes). Implementado por un subagente (modelo económico) y **revisado**: sin bugs encontrados — los 5 casos verificados (dado cargado, aire acondicionado, ventas TV, contingencia ocupación laboral 3×2, contingencia fragancias 3×4) coinciden exactamente con recálculo independiente en scipy. 11 tests en verde, UI verificada con `AppTest` sin excepciones.
- ✅ **Fase 5 — Pulido**: validación de inputs agregada a las funciones públicas de los 4 módulos del solver (`alpha` debe estar en (0,1) en las ~23 funciones que lo reciben; `r` debe estar en [0,n] y `p_hat`/`n` con sus propios límites en las funciones de proporción), con `raise ValueError` y mensajes claros, sin tocar ninguna fórmula ni lógica existente. Las 4 páginas Streamlit envuelven ahora las llamadas al solver en `try/except ValueError` mostrando `st.error(...)` en vez de un traceback (página 4 ya lo tenía desde Fase 4). Implementado por un subagente (modelo económico) y **revisado**: sin bugs — se confirmó que los checks de r/n usan límites inclusivos correctos (r=0 y r=n siguen siendo válidos) y que ninguna fórmula fue tocada. 34 tests nuevos en verde (100 tests totales en el proyecto), UI verificada de punta a punta con `AppTest` en las 5 páginas (incluida `app.py`) sin excepciones, y se probó manualmente que un input inválido (r>n) muestra un error claro en vez de romper la app.

Cada fase se da por cerrada cuando pasa sus tests y se valida el resultado contra al menos un ejercicio real de la materia (fuente: `Guia Problemas Estadística Aplicada 2026.pdf`).

---

## 8. Decisiones cerradas con el usuario (previamente puntos abiertos)

1. **Proporciones**: se suma al MVP el ensayo de hipótesis para 1 proporción (M2). La comparación de 2 proporciones NO se suma como test aparte en M3: se corrigió en §2.2b que la cátedra la resuelve con tabla de contingencia χ² (M4), no con un test Z independiente.
2. **Agrupación en χ² (Fe_i<5)**: la app **valida y avisa**, no agrupa sola. El criterio de qué celdas agrupar queda a cargo del usuario.
3. **Front**: confirmado **Streamlit**.

No quedan puntos abiertos de alcance/arquitectura. Se puede pasar a Fase 0.

---

## 9. Definition of Done (MVP completo)

- Los 4 módulos (M1–M4) resuelven correctamente los casos de §1–§4 del esquema teórico.
- Cada resultado se muestra con redacción formal, no solo el número.
- El árbol de decisión (σ conocido/desconocido, F antes de comparar medias, agrupación en χ²) lo aplica la app automáticamente, no el usuario.
- Suite de tests con al menos un caso conocido por módulo, todos en verde.
- La app corre 100% local con `streamlit run app.py`, sin dependencias de red.
