# Plan de estudio: 2° parcial de Estadística Aplicada

- **Fecha del parcial:** jueves 19/11/2026.
- **Materia:** Estadística Aplicada (UADE). Docente: Ing. Sergio Aníbal Dopazo.
- **Régimen:** final obligatorio (no se promociona), se puede recuperar **un solo** parcial. Final regular, probablemente el 17/12 (a confirmar).
- **Entra (deducido de las clases, el profesor no lo dijo):** todo lo dado después del 1° parcial.
  - Ensayos de hipótesis sobre p (Tema III).
  - Comparación de varianzas (Tema IV).
  - Comparación de medias: independientes y apareadas (Tema V).
  - Contrastes χ² (Tema VI).
  - Regresión (Tema VII). Se supone que entra lo dado el 29/10 (teoría y mínimos cuadrados) y lo que se dé el 05/11 y el 12/11 (validación). La regresión múltiple (VIII) no entra salvo que se dé.
  - **No entra** comparación de dos proporciones como tema propio (se ve dentro de χ² de consistencia).
- **Fuentes:** cuaderno "Estadistica" de NotebookLM (ver `CLAUDE.md`). Reglas del profesor en `REGLAS_PROFESOR.md`.
- **Herramientas en el examen:** apuntes, computadora con Excel o programas propios (como el solver de `../statistics`), el aplicativo *Probability Distributions* y calculadora. Wifi apagado y celular en modo avión.

---

## Estado actual

> Actualizar al final de cada sesión.

**Última actualización:** 31/10/2026. Plan revisado con las clases hasta el 29/10 y calendario armado (se supone que entra regresión); todavía no se empezó ningún tema.

| # | Tema | Estado |
|---|---|---|
| 0 | Reglas del profesor y errores del 1° parcial | ⬜ Pendiente |
| 1 | Repaso: estructura de un ensayo (μ y σ²) | ⬜ Pendiente |
| 2 | Ensayos de hipótesis sobre p (Tema III) | ⬜ Pendiente |
| 3 | Comparación de varianzas y desvíos (Tema IV) | ⬜ Pendiente |
| 4 | Comparación de medias independientes (Tema V) | ⬜ Pendiente |
| 5 | Muestras apareadas (Tema V) | ⬜ Pendiente |
| 6 | χ²: consistencia e independencia (Tema VI) | ⬜ Pendiente |
| 7 | χ²: bondad de ajuste (Tema VI) | ⬜ Pendiente |
| 8 | Regresión (Tema VII) | ⬜ Pendiente (validación: clase del 05/11) |
| 9 | Simulacro de parcial | ⬜ Pendiente |

Leyenda: ⬜ pendiente · 🟨 en curso · ✅ terminado

**Dudas / errores frecuentes:**
- (todavía nada)

**Para confirmar con el profesor o el campus:**
- Si entra regresión y hasta dónde (el plan supone que sí). Ojo: el recuperatorio del 2° parcial de 2024 (Notion compartido, revisado el 31/10) tuvo 4 problemas: ajuste a Poisson, **elección entre 4 modelos de regresión múltiple con R², S², PRESS, DET y Cp/p**, test F y regresión simple. Si en 2026 se da regresión múltiple, practicar ese tipo de pregunta.
- Si en el test F auxiliar acepta un α mayor que 0,10.
- Fecha del final: el 29/10 se mencionó «el 21 de diciembre» (el plan decía 17/12).

**El solver sigue al profesor donde la guía está mal** (corregido el 29/10):
- III-3b: 0,2057 (α entero). La guía dice 0,2589.
- III-11c: con el n resultante vale la normal (715). El exacto es 755. El 855 por Poisson de la guía es incorrecto.
- Cada aproximación se justifica con **su** n resultante y p₀. En III-17 valen las dos: normal 253 (n·p₀ = 10,37) y Poisson 227 (por Mermoz).

---

## Calendario hasta el parcial (31/10 → 19/11)

Las clases son los jueves (05/11 y 12/11). Calculé unos 3 a 5 ejercicios por día. Si un día se atrasa, se recorta de los marcados *(si da el tiempo)*, nunca de los simulacros.

Cómo encarar cada ejercicio:
1. Hacerlo en papel, como en el examen: planteo, H0 justificada, distribución justificada y 4 decimales.
2. Después controlar con el solver.
3. Anotar los errores abajo, en **Dudas / errores frecuentes**.

| Día | Tema | Qué hacer |
|---|---|---|
| Sáb 31/10 | 0 y 1 | Leer `REGLAS_PROFESOR.md` §1 a 5. Rehacer I-10 y II-12 controlando con los valores de clase. |
| Dom 01/11 | 2 (p) | Teoría §6. Rehacer III-16 y III-19 (casos de control). III-9 y III-10. |
| Lun 02/11 | 2 | n exacto, normal y Poisson con el criterio de Mermoz: III-11 (control), III-12, III-13, III-14. |
| Mar 03/11 | 2 | III-15, III-20, III-22, III-23. *(si da el tiempo: III-24, III-26)* |
| Mié 04/11 | 3 (varianzas) | Teoría §7. IV-1 e IV-4 (control). IV-2, IV-3, IV-5. |
| **Jue 05/11** | Clase | Validación de regresión. Después: bajar la transcripción y sumar reglas y ejercicios (pedírselo a Claude). |
| Vie 06/11 | 4 (medias) | Teoría §8. V-8 (control, con el test F auxiliar). V-1, V-2, V-3. |
| Sáb 07/11 | 4 | V-4, V-5, V-6, V-7. *(si da el tiempo: V-10, V-11)* |
| Dom 08/11 | 5 (apareadas) | V-12 (control). Clasificar V-9 y V-13 a V-21 (apareado o no, y por qué). Resolver V-9, V-13, V-14, V-15. |
| Lun 09/11 | 5 | V-16, V-17, V-18. *(si da el tiempo: V-19 a V-21)* |
| Mar 10/11 | 6 (tablas χ²) | Teoría §9. VI-6 y VI-7 (control). VI-1, VI-2, VI-3, VI-4. *(si da el tiempo: VI-5, VI-8, VI-9, VI-12)* |
| Mié 11/11 | 7 (ajuste discreto) | VI-10, VI-13 y VI-16 (control). VI-11. Ejemplos de ajuste discreto del apunte (empírico, uniforme, binomial, Poisson). |
| **Jue 12/11** | Clase | Procesar la clase como el 05/11. Si queda tiempo: rehacer VI-15 solo, sin mirar. |
| Vie 13/11 | 7 (ajuste continuo) | Ejemplos de ajuste continuo del apunte (normal, lognormal, Pareto, gamma). VI-14, VI-18, **VI-20** (el «típico problema»). *(si da el tiempo: VI-17, VI-19)* |
| Sáb 14/11 | 8 (regresión) | Ver la lista del tema 8. Practicar el modo regresión de la calculadora y la tabla x, y, x², y², xy. |
| Dom 15/11 | 9 | **Simulacro 1** con tiempo: un problema de los temas 2, 3, 4 o 5, 6 o 7 y 8. |
| Lun 16/11 | 9 | Corregir el simulacro con `REGLAS_PROFESOR.md` y rehacer los errores. Juntar las dudas para preguntarlas **antes** del examen. |
| Mar 17/11 | 9 | **Simulacro 2**: un problema combinado tipo VI-20 más uno de p y uno de regresión. |
| Mié 18/11 | Preparación | Repasar los errores anotados. Dejar la compu lista (ver abajo). Descansar. |
| **Jue 19/11** | **Parcial** | |

**Compu para el examen (probar el 18/11 con el wifi apagado):**
- El solver levanta sin internet.
- Excel tiene `GAMMA` o `GAMMA.LN`, y el Solver de Excel está activado (para la Weibull).
- *Probability Distributions* sin actualizar.
- La tabla de ajuste por momentos de la Weibull y el apunte, descargados.

---

## Temas (en orden)

### 0. Reglas del profesor y errores del 1° parcial

Leer `REGLAS_PROFESOR.md`, secciones 1 a 5. Lo que más penaliza:
- probabilidades en %;
- hipótesis sin justificar en palabras;
- justificar Z o t por "conozco o no conozco σ" (la razón es dividir por un parámetro o por la variable aleatoria S);
- menos de 4 decimales;
- comparar contra μ₀ en lugar de contra el crítico;
- dividir α por 2 con un solo límite.

**Práctica:** tomar una resolución vieja del 1° parcial y marcarle los errores con esa lista.

---

### 1. Repaso: estructura de un ensayo (μ y σ²)

Es la base de todo el 2° parcial: comparación y p usan los mismos 7 pasos.
- Pasos: variable → H0/H1 con criterio → α → n → crítico, CR y RD → estimador → conclusión.
- Criterio pesimista u optimista, la igualdad en H0, unilateral siempre que se pueda.
- β con el crítico **sin redondear**; no recalcular n reutilizando el x̄c viejo.

**Ejercicios hechos en clase (para controlar):**
- I-10: x̄c = 10,52; 1−β = 0,5231; n = 30.
- II-8: S²c = 0,16098; n = 540 (528 más), con García.
- II-12: Sc = 6,86; β = 0,3222; n = 27 (17 más).

---

### 2. Ensayos de hipótesis sobre p (Tema III, apunte cap. 2)

**Teoría:** `REGLAS_PROFESOR.md` §6.
- No hay bilateral. Se decide con r ≥ rc, eligiendo rc con α real ≤ α.
- Fórmulas de β en los dos casos.
- n exacto y aproximaciones normal y Poisson, **justificando** cuál vale con el n resultante (n·p > 10, n·q > 10, Mermoz).
- Vocabulario de recepción: AQL, RQL o LTPD, riesgo del proveedor y del comprador.

**Hechos en clase (casos de control):**
- **III-11** (control de proceso, optimista): rc = 11; β = 0,9176; c) exacto n = 755 (rc = 106), normal 715. El 855 de la guía por Poisson está mal.
- **III-16** (campaña, pesimista, "3 puntos" ⇒ p₁ = 0,15): exacto n = 1675 (rc = 233); normal n = 1637 (rc = 229); b) 1−β = 0,5159.
- **III-19** (ruleta, α = 0,05 justificado por imparcialidad): rc = 37; r = 42 ⇒ se rechaza; 1−β = 0,9788.
- **III-3b** (IC con r = 0): B = 0,2057 con α entero.

**Ejercicios:** III-9, III-10, III-12, III-13, III-14, III-15, III-20, III-22, III-23, III-24, III-26. Extra: III-17, III-18, III-21, III-25.

---

### 3. Comparación de varianzas y desvíos (Tema IV, apunte cap. 3)

**Teoría:** `REGLAS_PROFESOR.md` §7.
- ψ² = σ₁²/σ₂² con J² y F; pensar qué va en el numerador.
- IC e interpretación en % ("como mínimo X% menor, como máximo Y% mayor").
- Relación entre límites y n con n₁ = n₂ (R = R'² para desvíos).
- Ensayos caso 1 y caso 2, β y n. No hay bilaterales.

**Hechos en clase:**
- **IV-1** (tornos): A = 0,2036, B = 1,1135, R = 5,470; n = 45 por torno; desvíos A' = 0,4512, B' = 1,0552; n = 444.
- **IV-4** (hiladoras, H0: φ ≥ 0,88, α = 0,10): Jc = 0,3859, J = 0,3729 ⇒ se rechaza; β = 0,8221; n = 128 por tipo.

**Ejercicios:** IV-2, IV-3, IV-5.

---

### 4. Comparación de medias independientes (Tema V)

**Teoría:** `REGLAS_PROFESOR.md` §8.
- Test F auxiliar (unilateral, α = 0,10) ⇒ amalgamado o Welch.
- Diferencias porcentuales con h (h² en el término correcto).
- Porcentaje mínimo por inecuación, verificando las raíces.
- Diferencia mínima o máxima con un solo límite (α entero).
- Sin β ni n con t.

**Hecho en clase:**
- **V-8** (látex):
  - test F auxiliar: Jc = 1,2949, J = 1,0417 ⇒ amalgamado, con Sa = 1,2377;
  - a) Dc = 0,9711 contra D = 0,9 ⇒ no se rechaza;
  - b) mínimo 0,3788 kg;
  - c) D*c = 0,5349 contra D* = 0,14;
  - d) incremento mínimo 4,90%.

**Ejercicios:** V-1, V-2, V-3, V-4, V-5, V-6, V-7, V-10, V-11. Antes de resolverlos, decidir para cada uno si es independiente o apareado y por qué.

---

### 5. Muestras apareadas (Tema V)

- Se reconocen por el **mismo individuo o la misma unidad experimental**, no por los n iguales.
- d̄ y S_D de las diferencias por individuo; t con ν = n−1.

**Hecho en clase:**
- **V-12** (trigo): d̄ = 5,75; S_D = 5,12; D̄c = 5,4295 ⇒ se rechaza; IC 90%: 2,32 a 9,18.

**Ejercicios:** V-9, V-13 a V-21. Primero clasificar cada uno (apareado o no) y después resolver.

---

### 6. χ²: consistencia e independencia (Tema VI, apunte cap. 4)

**Teoría:** `REGLAS_PROFESOR.md` §9.
- "Asociación" ⇒ independencia; "niveles o porcentajes" ⇒ consistencia.
- H0 por categoría (consistencia) o en palabras (independencia).
- Esperados con decimales, N ≥ 60, E ≥ 5 (amalgamar si no se cumple), ν = (f−1)(c−1).
- Al rechazar: "alguna es distinta".

**Hechos en clase:**
- **VI-6** (turnos): χ² = 38,98 contra 13,2767 ⇒ se rechaza.
- **VI-7** (color de autos): χ² = 5,5739 contra 7,8147 ⇒ no se rechaza.

**Ejercicios:** VI-1, VI-2, VI-3, VI-4, VI-5, VI-8, VI-9, VI-12.

---

### 7. χ²: bondad de ajuste (Tema VI)

- Esperados Ei = N·pi; completar el dominio con F o G **acumuladas**; amalgamar.
- ν = clases efectivas − 1 − parámetros estimados.
- Ajuste demasiado perfecto (cola izquierda); las 3 situaciones de las discretas.
- Modelos continuos (dados el 29/10, ver `REGLAS_PROFESOR.md` §9 e `informes/informe_clase_13.md`):
  - las clases que completan el dominio van **aparte**, con O = 0;
  - parámetros por momentos (en Weibull, decir el método);
  - no rechazar ⇒ «buen candidato»;
  - mejor ajuste = menor χ².
- Leer los ejemplos de ajuste resueltos del apunte (el profesor insistió) y el apéndice de modelos (pp. 123 a 127).

**Hechos en clase:**
- **VI-13** (televisores, patrón histórico): χ² = 5,625 contra 5,9915.
- **VI-10** (dado): χ² = 11,8 contra 11,0705 ⇒ cargado.
- **VI-16** (Poisson, m̂ = 3,5263): χ² = 9,4346 contra 15,5073 con ν = 8.
- **VI-15** (herramientas de corte, α = 0,01, x̄ = 45,6818, S = 24,3257). Todos contra χ²(0,99; 4) = 13,2767:
  - Gumbel del mínimo: χ² = 68,56 ⇒ se rechaza;
  - Gumbel del máximo: 10,84 ⇒ buen candidato;
  - Weibull (ω = 1,9592, β = 51,52): 8,33 ⇒ buen candidato y **el mejor**.

**Ejercicios:** VI-11. Continuas: VI-14, VI-17, VI-18, VI-19, VI-20 (este es el «típico problema» de parcial: comparación + ajuste).

---

### 8. Regresión (Temas VII y VIII)

Empezó el 29/10 («es el último tema»). La validación se da el 05/11. Todavía no se sabe si entra en el 2° parcial.

Temas:
- recta de mínimos cuadrados;
- r y r²;
- validación (H0: no hay relación, y relación fuerte);
- intervalos para la ley promedio y de predicción;
- modelo lineal general con Excel.

Reglas del 29/10 en `REGLAS_PROFESOR.md` §10: vocabulario (variable explicativa y explicada, coeficiente de regresión o contribución marginal, perturbación del entorno), «lineal en los parámetros», b₀ y b₁.

**Ejercicios con lo dado el 29/10** (recta, interpretación, pronóstico puntual, linealizables):
- Recta de mínimos cuadrados e interpretación de b₀ y b₁ en términos del problema (coeficiente de regresión o contribución marginal, no «pendiente»): VII-3a, VII-4a, VII-7a; VII-12a y VII-13a sin la validación.
- Estimador puntual (pronóstico): VII-1a, VII-9a y VII-9c.
- Significado de β₀: VII-7c (por qué la recta no pasa por el origen).
- Modelo linealizable con logaritmos: VII-11a (y = α·x^β).

**Después del 05/11 (validación, r, intervalos):** VII-1b/c, VII-2, VII-3b, VII-5, VII-6, VII-8, VII-12 y VII-13 completos. Ajustar esta lista con lo que se dé en clase.

**No entra, salvo que se dé:** Tema VIII (regresión múltiple).

---

### 9. Simulacro de parcial

- Un problema de cada tema (2 a 8), con tiempo, apuntes y el aplicativo, sin mirar las resoluciones. Incluir uno combinado tipo VI-20.
- Corregir con `REGLAS_PROFESOR.md` (redacción, justificación, decimales) y verificar los números con el solver.
- Rehacer los que salieron mal.

---

## Fuentes en NotebookLM

| Fuente | ID (prefijo) | Tema |
|---|---|---|
| Guia Problemas Estadística Aplicada 2026.pdf | `35d7e4aa` | todos |
| 2 - Ensayos de Hipótesis.pdf | `86c936b8` | 1, 2 |
| 3 - Comparación de Parámetros.pdf | `87c43290` | 3, 4, 5 |
| 4 - Contrastes Chi Cuadrado.pdf | `1a475a44` | 6, 7 |
| 5 - Teoría de la Regresión.pdf | `490fa323` | 8 |
| 6 - Apéndice A - Resumen de los Modelos.pdf | `908d16a4` | 7 |
| Ajustes por momentos Distribución Weibull.pdf | `363bfffd` | 7 |
| Clase 17/09 (ensayos de p) | `74a36b3b` | 2 |
| Clase 24/09 (n exacto de p, III-16) | `c53e34bf` | 2 |
| Clase 01/10 (devolución del 1° parcial, IV-1) | `3871c490` | 0, 3 |
| Clase 08/10 (IV-4, medias, V-8) | `2c1ebc03` | 3, 4 |
| Clase 15/10 (V-8, apareadas, inicio de χ²) | `fef55656` | 4, 5, 6 |
| Clase 22/10 (χ²) | `7bf95c9c` | 6, 7 |
| Clase 29/10 (χ² continuas, VI-15, inicio de regresión) | `434667af` | 7, 8 |
| Clases 06/08 a 10/09 (1° parcial) | `490c7079` … `27fda49a` | 0, 1 |
