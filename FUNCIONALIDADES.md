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
