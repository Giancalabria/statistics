# Funcionalidades — Solver de Estadística Aplicada

Aplicación **Streamlit** (`app.py` + módulos en `pages/`) que resuelve ejercicios típicos de
Estadística Aplicada. El usuario indica **qué datos conoce** (no la fórmula a usar) y la app
elige automáticamente el camino correcto siguiendo el árbol de decisión documentado en
`esquema_teorico_examen_estadistica.md`. La lógica de cálculo vive en `solver/` y es independiente
de la interfaz (probada con `pytest` en `tests/`).

## Estructura del proyecto

| Carpeta/archivo | Contenido |
|---|---|
| `app.py` | Punto de entrada: la navegación entre páginas, la persistencia de los widgets (`persistencia.py`) y el aviso de las consultas a la IA que siguen corriendo en otra página. |
| `pages/0_Inicio.py` | Página de inicio, describe los módulos disponibles. |
| `pages/1_Intervalos_de_Confianza.py` | Módulo de Intervalos de Confianza. |
| `pages/2_Ensayo_de_Hipotesis.py` | Módulo de Ensayo de Hipótesis (1 población). |
| `pages/3_Comparacion_2_Poblaciones.py` | Módulo de Comparación de 2 Poblaciones. |
| `pages/4_Chi_Cuadrado.py` | Módulo de Contrastes Chi-Cuadrado. |
| `pages/5_Interpretar_Enunciado.py` | Intérprete de enunciados: se pega el problema (y opcionalmente la tabla de datos) y dice qué pide, qué datos hay y lo resuelve. |
| `pages/6_Regresion.py` | Regresión y correlación simple (TEMA VII) y modelo lineal general (TEMA VIII). |
| `pages/7_Guia_Resuelta.py` | La Guía de Problemas resuelta paso a paso (`Guia_resuelta.md`), con buscador y lista de discrepancias. |
| `pages/8_Asistente_IA.py` | Chat libre con la IA local (Ollama, sin internet): instrucciones editables, apuntes del repo opcionales, material propio (archivos o texto) y «Resolver mi mensaje con la app» (interpreta + solver + explicación). |
| `asistente/` | IA local opcional (ver `ASISTENTE_IA.md`): completa lo que las reglas del intérprete no entienden (solo si mejora la resolución), explica y redacta resoluciones del solver marcando números sin respaldo. Nunca calcula: los números son del solver. |
| `interprete/` | Lógica del intérprete (reglas offline, sin IA): `analizador.py`, `resolver.py`, `buscador.py`, `glosario.py`, `tablas.py` (tablas de datos en el texto), `chi_modelos.py` (TEMA VI), `regresion.py` (TEMAS VII y VIII). |
| `datos/verdad/tema_*.json` | Transcripción de la Guía de Problemas 2026 verificada página por página contra el PDF: enunciado, incisos, tablas estructuradas, respuesta de cada inciso y sus valores numéricos, notas sobre erratas de la guía. |
| `datos/guia_ejercicios.json` | Los 142 ejercicios unidos (`herramientas/armar_guia.py`). Es lo que usan el buscador, el evaluador y el generador de resueltos. |
| `Guia_resuelta.md` | Todos los ejercicios de la guía resueltos por la app paso a paso, con la respuesta de la guía al lado y la lista de discrepancias (`herramientas/generar_resueltos.py`). |
| `herramientas/` | Scripts de mantenimiento: `armar_guia.py` (verdad → JSON), `evaluar_guia.py` (mide el intérprete contra los valores de la guía, temas I–VIII, con tolerancia y dígito a dígito), `generar_resueltos.py` (arma `Guia_resuelta.md`), `extraer_guia.py` (extracción automática vieja del PDF, ya no se usa para el JSON), `ver_analisis.py`. |
| `solver/distributions.py` | Wrappers sobre `scipy.stats` (valores críticos e inversos para Z, t, χ², F, Beta, Binomial; factor de corrección por finitud). |
| `solver/intervals.py`, `hypothesis_one.py`, `two_samples.py`, `chi_square.py` | Lógica estadística de cada módulo. |
| `solver/ajuste.py` | Bondad de ajuste χ² calculando las frecuencias esperadas de un modelo (uniforme, binomial, Poisson, normal, log-normal, exponencial, gamma, Weibull, Gumbel máx/mín, Pareto), con estimación por momentos y amalgamado de clases. |
| `solver/regresion.py` | Regresión simple (recta, r, ensayos e intervalos, modelos linealizables, recta por el origen, desde sumatorias) y múltiple (b, R², R² ajustado, F global, t parciales, PRESS, DET, Cp, VIF, selección de modelos). |
| `interprete/redondeo.py` | Redondeo de presentación de la cátedra: intervalos y críticos hacia afuera, decimales por tipo de valor (ver `CONVENCIONES_CATEDRA.md`). |
| `datos/diferencias_explicadas.json` | Por qué cada valor de la guía que no coincide (o coincide solo aproximadamente) es distinto: errata, valor de tabla, etc. |
| `CONVENCIONES_CATEDRA.md` | Reglas de la cátedra verificadas contra la guía (población finita √((N-n)/N), β con crítico redondeado, planes de muestreo, etc.) y las evaluadas y descartadas. |
| `solver/wording.py` | Genera las conclusiones en lenguaje natural (redacción formal de resultados). |
| `esquema_teorico_examen_estadistica.md` | Árbol de decisión teórico que la app sigue. |

---

## 1. Intervalos de Confianza

Permite elegir el **parámetro** a estimar (Media, Varianza/Desvío o Proporción), el **objetivo**
(calcular el IC o el tamaño de muestra `n`) y el **nivel de confianza**. Opcionalmente admite
población finita (con `N` conocido), aplicando el factor de corrección por finitud de la cátedra, √((N−n)/N).

- **Media**
  - IC con σ conocido (distribución Z) o σ desconocido (distribución t, con grados de libertad).
  - Tamaño de muestra `n` dado un error muestral admitido `e`, con σ conocido o desconocido.
- **Varianza / Desvío**
  - IC para σ² y para σ (distribución χ²), calculados juntos a partir del desvío muestral.
  - Tamaño de muestra `n` por **relación entre límites** R' = B'/A' (Ecuación de García): se puede
    pedir una reducción porcentual de la relación actual (cargando los límites A' y B' del IC previo
    o R' directamente) o fijar la relación objetivo. Informa a, ν, n, el Δn respecto de la muestra
    preliminar y un control por búsqueda exacta sobre χ².
- **Proporción**
  - IC por **método exacto** (Clopper-Pearson / transformación F), y opcionalmente comparación con
    la **aproximación normal**.
  - Tamaño de muestra `n` dado un error admitido `e` y una proporción estimada `p̂` (0.5 por defecto
    si no hay estimación previa).

Cada resultado muestra el intervalo en notación matemática (`st.latex`), la redacción formal de la
conclusión, y un detalle expandible con distribución usada, grados de libertad, valor crítico,
error muestral y si se aplicó corrección por finitud.

## 2. Ensayo de Hipótesis (1 población)

Permite elegir el **parámetro** a contrastar (Media, Varianza o Proporción), el **nivel de
significación (α)** y el **tipo de ensayo** (unilateral derecha, unilateral izquierda o bilateral).

- **Media**
  - Ensayo con σ conocido (Z) o desconocido (t), dado x̄.
  - Cálculo de β (error Tipo II) y potencia (1-β) si se provee una media alternativa μ₁.
  - Cálculo de tamaño de muestra `n` para una potencia fijada (σ conocido validado contra ejercicios
    de cátedra; σ desconocido marcado como extensión analógica no validada).
- **Varianza**
  - Ensayo χ² sobre el desvío muestral vs. σ₀, con cálculo opcional de β/potencia dado σ₁ alternativo.
- **Proporción**
  - Ensayo exacto binomial (búsqueda de región crítica r_c), con cálculo opcional de β/potencia
    dado p₁ alternativo.

Cada resultado muestra el/los valor(es) crítico(s), la decisión (Rechaza / No rechaza H0), la
conclusión redactada formalmente, y detalle expandible con distribución, grados de libertad, β,
potencia y valor p (α*).

## 3. Comparación de 2 Poblaciones

- **Varianzas / desvíos (TEMA IV, distribución F)**: parámetro φ = σ₁/σ₂ con la muestra 1 en el numerador
  (si hay un grupo con el cambio —reacondicionado, propuesto, con aditivo— va arriba).
  - Ensayo contra cualquier φ₀ ("reducir el desvío un 12%" → H0: φ ≥ 0,88; j²c = φ₀²·F), con cola a elección
    y β / potencia para un φ₁ alternativo.
  - IC para σ₁²/σ₂² y σ₁/σ₂ (y sus inversas) con la relación entre límites B/A.
  - Tamaño de muestra (n₁ = n₂) para una potencia fijada y para una relación entre límites del IC
    (búsqueda exacta sobre F; coincide con la guía: IV-1 45 y 444, IV-2 483, IV-3 260 y 68, IV-4 128, IV-5 127 y 174).
- **Medias — Muestras independientes**: ejecuta automáticamente el **Test F** para decidir el
  método:
  - Si no se rechaza H0 (varianzas iguales) → método **pooled** (varianza combinada).
  - Si se rechaza H0 (varianzas distintas) → método **Welch**.
  
  Con el método elegido, permite calcular IC para la diferencia de medias δ, ensayo de hipótesis
  (dado δ₀ y tipo de cola), o tamaño de muestra `n` para un error deseado (pooled; en el intérprete también
  Welch y σ conocidos con Z). En el intérprete además: datos agrupados de dos grupos, varias comparaciones con/sin,
  "supera en un X%" (H0: μ₁ ≤ h·μ₂), β / potencia para una diferencia real δ₁, y el **criterio de la cátedra**
  para "¿difieren?": en una comparación el ensayo se plantea unilateral en el sentido de los datos (el bilateral
  se muestra como referencia).
- **Medias — Muestras apareadas**: el usuario ingresa las diferencias d_i entre pares (texto libre
  separado por comas o espacios). Se aplica el ensayo t de una muestra sobre esas diferencias:
  IC para δ, ensayo de hipótesis, o tamaño de muestra `n` (con S_d calculado a partir de las
  diferencias ingresadas).

## 4. Contrastes Chi-Cuadrado

(Planes de muestreo de proporciones, en el intérprete: además del plan binomial exacto de menor n se listan los
rangos de n válidos para los primeros r_c —la guía a veces informa el mayor— y la "aproximación de Poisson" como la
calcula la guía, con la tabla de Poisson (m al 0,1).)

- **Ajuste a un modelo (calcula las Fe)**: se carga la tabla de frecuencias (clases `20-30 ; 6` o valores `0 ; 26`)
  y el modelo: uniforme, binomial, Poisson, normal, log-normal, exponencial, gamma, Weibull, Gumbel del máximo y del
  mínimo, Pareto. Los parámetros que no se cargan se estiman por momentos con las marcas de clase (x̄ y S corregido;
  Weibull por el coeficiente de variación como la tabla de la cátedra; Pareto con el mínimo θ dado y b = μ/(μ-θ)) y
  cada uno resta un grado de libertad. La primera y la última clase llegan al borde del dominio y las clases con
  Fe < 5 se amalgaman con la vecina. Muestra la tabla Fo / P / Fe antes y después de amalgamar.
- **Bondad de ajuste (Fe ya calculadas)**: el usuario ingresa las frecuencias observadas (F_o) y esperadas (F_e) —ya
  calculadas para el modelo a probar— y la cantidad de parámetros estimados `p` (afecta los grados
  de libertad). Devuelve χ² calculado, χ² crítico, grados de libertad y decisión.
- **Tabla de contingencia** (independencia/homogeneidad): el usuario ingresa una tabla de
  frecuencias observadas (filas × columnas, texto libre). La app calcula automáticamente la tabla
  de frecuencias esperadas y el estadístico χ², mostrando ambas tablas.

Ambos casos muestran χ² calculado, χ² crítico, grados de libertad, decisión (rechaza/no rechaza
H0) y conclusión redactada formalmente.

## 5. Regresión y correlación (TEMAS VII y VIII)

Se pega la tabla de datos y se elige la variable a explicar y las explicativas.

- **Simple**: recta de mínimos cuadrados (también por el origen y modelos linealizables: doble logarítmico,
  logarítmico lineal, lineal-logarítmico, inverso), r y r², validación de la cátedra (H0: β1 = 0 con
  |tc| > t(1-α; n-2) y criterio de r² según el campo de aplicación), IC para β1, IC para ρ (Fisher) y ρ²,
  pronóstico puntual e intervalos para la ley promedio y de predicción (bilaterales o mínimo / máximo), ensayo de
  β1 contra un valor con el valor crítico b1c (casos I y II de la cátedra). También desde sumatorias (Σx, Σx², ...).
- **Múltiple (modelo lineal general)**: b = (X'X)⁻¹X'y, S², R², R² ajustado, análisis global (F), análisis individual
  (t con los Cii de (X'X)⁻¹), coeficientes de determinación parcial, y la tabla de selección de todos los modelos
  candidatos (R² ajustado, S², PRESS, DET, Cp, Cp/p, VIF) con el mejor candidato según DET > 0,1 y Cp/p < 5.

## 6. Guía resuelta

`Guia_resuelta.md` (y la página *Guía Resuelta*) tiene los 142 ejercicios de la guía resueltos por la app con los
pasos en el orden de la cátedra, la respuesta de la guía al lado, una marca ✅ / ⚠️ por inciso y al final la lista
de discrepancias con la guía para revisar. Se regenera con `python herramientas/generar_resueltos.py` cada vez que
se mejora el solver o el intérprete.

## 7. Interpretar un enunciado

Pantalla para cuando lo difícil es **entender qué pide el profesor**. Funciona 100% offline: no usa
modelos de lenguaje sino reglas armadas con el estilo de redacción de la Guía de Problemas, así que
todo lo que detecta se muestra con su justificación y es editable.

Flujo:

1. Se pega el **planteo** y se cargan los **incisos** (o se pega el enunciado completo y se usa
   *Separar incisos*).
2. **Interpretar** muestra:
   - **Tema** detectado (media, varianza, proporción, 2 poblaciones, χ², regresión, modelo lineal general) con
     el motivo. Se puede pegar aparte la **tabla de datos** (o la busca en el planteo).
   - **Criterio** para plantear H0 (optimista / pesimista) cuando corresponde. Se puede **cambiar a mano**:
     se invierte el planteo (en un diseño con α y β se intercambian μ₀↔μ₁ y α↔β; las colas unilaterales se
     dan vuelta; en un sistema de control, rechazar H0 pasa de "detener" a "seguir") y la pantalla lista
     qué cambió.
   - **Pistas de lectura**: frases típicas de la cátedra encontradas en el texto y qué significan
     ("desvío histórico" → σ conocido, "¿cuántos más?" → Δn, "probabilidad de no detectar" → β...).
   - **Datos** extraídos (n, x̄, σ/S, μ₀, α, e, N, r, p̂, datos crudos o tablas de frecuencias...) con
     el fragmento del enunciado del que salió cada uno. Se pueden corregir y agregar datos.
   - Para **cada inciso**: qué te pide, el tipo de pregunta (IC, tamaño de muestra, ensayo, β/potencia,
     diseño del ensayo, curvas OC), sus parámetros (cola, α del inciso, μ₁, reducción del error...) y
     **cómo presentarlo** según la cátedra.
   - **Ejercicios parecidos de la guía** (buscador TF-IDF), con la respuesta de la guía y, si está
     resuelto, sus conclusiones.
3. **Calcular** resuelve todos los incisos con `solver/` y muestra los pasos en el orden de la
   cátedra (hipótesis, distribución, condición de rechazo, regla de decisión, conclusión con
   P(A ≤ θ ≤ B) = 1-α). Como el examen lo pide en cada problema, antes de las hipótesis agrega una
   **Justificación de H0** (criterio, qué significan α y β en palabras del problema, cola) y después los
   **Modelos y distribuciones empleados** (X ~ N, x̄ ~ N(μ; σ²/n) → Z, t de Student, χ², Binomial...).
   Son plantillas por reglas: guían la redacción, conviene adaptarlas al enunciado. Los resultados de un inciso se usan en los siguientes (el n del diseño en la
   curva, el error del IC en "reducir el error un 30%").

Casos que resuelve además de los módulos 1–4: datos agrupados en tabla de frecuencias, datos "en
miles", totales ("40 personas en 68 minutos"), población finita también en ensayos (con valor a
posteriori α*), límites de confianza unilaterales ("desvío máximo", "fracción defectuosa máxima"),
"Ídem a) y b) con σ desconocido", n para una potencia fijada en varianza (χ²) y plan de muestreo
binomial (n, r_c) para proporciones, **sistemas de control** ("si μ = a no detener con probabilidad p; si
μ = b detener con probabilidad q": H0 = el proceso anda bien y detener = rechazar H0, sin importar el orden en que
se dan las condiciones) y **doble condición** ("se compra si el promedio es inferior a X y el desvío inferior a Y":
se hacen los dos ensayos y se estiman los dos parámetros).

**Precisión medida contra la guía** (`python herramientas/evaluar_guia.py`, alcance del primer
parcial: Tema I 1–34, Tema II 1–12, Tema III 1–8): el tema se detecta bien en 54/54 ejercicios y
coinciden ~84% de los números de las respuestas. En el Tema IV (`--todo`) coinciden 27/32; los que faltan son
números del texto de la respuesta, no resultados (los que no coinciden son en gran parte números que
aparecen en el texto de la respuesta, o ejercicios con dos alternativas / doble ensayo).

---

## Comportamientos transversales

- **Validación de inputs**: errores de dominio (valores inválidos, listas mal formateadas, tablas
  vacías) se capturan y muestran como mensajes de error (`st.error`) sin romper la app.
- **Warnings estadísticos**: cada resultado puede incluir advertencias (`result.warnings`) sobre
  supuestos no verificados o condiciones límite (p. ej. tamaño de muestra pequeño).
- **Redacción automática** (`solver/wording.py`): traduce cada resultado numérico a una conclusión
  en español, lista para copiar como respuesta de examen.
- **Independencia UI/lógica**: toda la matemática vive en `solver/`, cubierta por tests unitarios
  en `tests/`, lo que permite validar los cálculos sin depender de Streamlit.
