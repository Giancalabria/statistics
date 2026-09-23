# Funcionalidades — Solver de Estadística Aplicada

Aplicación **Streamlit** (`app.py` + módulos en `pages/`) que resuelve ejercicios típicos de
Estadística Aplicada. El usuario indica **qué datos conoce** (no la fórmula a usar) y la app
elige automáticamente el camino correcto siguiendo el árbol de decisión documentado en
`esquema_teorico_examen_estadistica.md`. La lógica de cálculo vive en `solver/` y es independiente
de la interfaz (probada con `pytest` en `tests/`).

## Estructura del proyecto

| Carpeta/archivo | Contenido |
|---|---|
| `app.py` | Página de inicio, describe los módulos disponibles. |
| `pages/1_Intervalos_de_Confianza.py` | Módulo de Intervalos de Confianza. |
| `pages/2_Ensayo_de_Hipotesis.py` | Módulo de Ensayo de Hipótesis (1 población). |
| `pages/3_Comparacion_2_Poblaciones.py` | Módulo de Comparación de 2 Poblaciones. |
| `pages/4_Chi_Cuadrado.py` | Módulo de Contrastes Chi-Cuadrado. |
| `pages/5_Interpretar_Enunciado.py` | Intérprete de enunciados: se pega el problema y dice qué pide, qué datos hay y lo resuelve. |
| `interprete/` | Lógica del intérprete (reglas offline, sin IA): `analizador.py`, `resolver.py`, `buscador.py`, `glosario.py`. |
| `datos/guia_ejercicios.json` | Los 142 ejercicios de la Guía de Problemas 2026 extraídos del PDF (enunciado, incisos, respuesta, resolución). |
| `herramientas/` | Scripts de mantenimiento: `extraer_guia.py` (PDF → JSON), `evaluar_guia.py` (mide el intérprete contra la guía), `ver_analisis.py`. `herramientas/tmp/` es temporal (no se versiona). |
| `solver/distributions.py` | Wrappers sobre `scipy.stats` (valores críticos e inversos para Z, t, χ², F, Beta, Binomial; factor de corrección por finitud). |
| `solver/intervals.py`, `hypothesis_one.py`, `two_samples.py`, `chi_square.py` | Lógica estadística de cada módulo. |
| `solver/wording.py` | Genera las conclusiones en lenguaje natural (redacción formal de resultados). |
| `esquema_teorico_examen_estadistica.md` | Árbol de decisión teórico que la app sigue. |

---

## 1. Intervalos de Confianza

Permite elegir el **parámetro** a estimar (Media, Varianza/Desvío o Proporción), el **objetivo**
(calcular el IC o el tamaño de muestra `n`) y el **nivel de confianza**. Opcionalmente admite
población finita (con `N` conocido), aplicando el factor de corrección por finitud (fpc).

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

- **Varianzas (Test F)**: ensaya H0: σ₁² = σ₂² (bilateral), o calcula el IC para la razón de
  varianzas σ₁²/σ₂² (y su inversa σ₂²/σ₁²).
- **Medias — Muestras independientes**: ejecuta automáticamente el **Test F** para decidir el
  método:
  - Si no se rechaza H0 (varianzas iguales) → método **pooled** (varianza combinada).
  - Si se rechaza H0 (varianzas distintas) → método **Welch**.
  
  Con el método elegido, permite calcular IC para la diferencia de medias δ, ensayo de hipótesis
  (dado δ₀ y tipo de cola), o tamaño de muestra `n` para un error deseado (solo implementado para
  el caso pooled; Welch requiere búsqueda iterativa no implementada).
- **Medias — Muestras apareadas**: el usuario ingresa las diferencias d_i entre pares (texto libre
  separado por comas o espacios). Se aplica el ensayo t de una muestra sobre esas diferencias:
  IC para δ, ensayo de hipótesis, o tamaño de muestra `n` (con S_d calculado a partir de las
  diferencias ingresadas).

## 4. Contrastes Chi-Cuadrado

- **Bondad de ajuste**: el usuario ingresa las frecuencias observadas (F_o) y esperadas (F_e) —ya
  calculadas para el modelo a probar— y la cantidad de parámetros estimados `p` (afecta los grados
  de libertad). Devuelve χ² calculado, χ² crítico, grados de libertad y decisión.
- **Tabla de contingencia** (independencia/homogeneidad): el usuario ingresa una tabla de
  frecuencias observadas (filas × columnas, texto libre). La app calcula automáticamente la tabla
  de frecuencias esperadas y el estadístico χ², mostrando ambas tablas.

Ambos casos muestran χ² calculado, χ² crítico, grados de libertad, decisión (rechaza/no rechaza
H0) y conclusión redactada formalmente.

## 5. Interpretar un enunciado

Pantalla para cuando lo difícil es **entender qué pide el profesor**. Funciona 100% offline: no usa
modelos de lenguaje sino reglas armadas con el estilo de redacción de la Guía de Problemas, así que
todo lo que detecta se muestra con su justificación y es editable.

Flujo:

1. Se pega el **planteo** y se cargan los **incisos** (o se pega el enunciado completo y se usa
   *Separar incisos*).
2. **Interpretar** muestra:
   - **Tema** detectado (media, varianza, proporción, 2 poblaciones, χ²) con el motivo, y si entra o
     no en el primer parcial.
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
coinciden ~83% de los números de las respuestas (los que no coinciden son en gran parte números que
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
