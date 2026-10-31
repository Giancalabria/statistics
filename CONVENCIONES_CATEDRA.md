# Convenciones de la cátedra que aplica la app

Hay dos fuentes, y **lo que dijo el profesor en clase manda** sobre la guía y sobre el repo (ver
`../estadistica/REGLAS_PROFESOR.md` y los informes de las clases en `../estadistica/informes/`):

- **Profesor en clase**: reglas que el Ing. Dopazo dio en las clases del 06/08 al 22/10/2026.
- **Guía**: reglas deducidas recalculando las respuestas de la guía **dígito a dígito**. Varias salen del trabajo de
  un compañero ([royvicente/estadistica-avanzada](https://github.com/royvicente/estadistica-avanzada),
  `docs/conocimiento/convenciones-catedra.md`), y acá se verificaron con nuestro intérprete.

Cuando la guía y el profesor no coinciden, la app sigue al profesor y el inciso de la guía queda explicado en
`datos/diferencias_explicadas.json` (hoy: III-3b y III-11c).

Para medir, `python herramientas/evaluar_guia.py` tiene la columna **exactos**: cuántos valores de la
guía coinciden en todos sus dígitos (con redondeo común o hacia afuera), además de la columna con tolerancia.
`--fallas` marca con `OK~` los incisos que coinciden solo aproximadamente. Los ejercicios que el profesor resolvió
en clase están en `tests/test_clases_profesor.py`.

## Reglas del profesor en clase (mandan sobre la guía)

| Regla | Detalle en la app | Fuente: profesor en clase | Dónde |
|---|---|---|---|
| Un solo límite ⇒ α entero | Con r = 0 (o r = n) el IC de p tiene un solo límite y va con **α sin dividir**: III-3b → B = **0,2057** (la guía da 0,2589 y «está mal»). También en cotas «mínimo / máximo» de cualquier parámetro. | 10/09, 17/09, 15/10 | `solver/intervals.py`, `interprete/resolver.py` (`_cota`, `prop_ic`) |
| Estimación de p siempre exacta | El IC de p se calcula solo con Beta / F. La aproximación normal es «aberración»: no se informa; en la página 1 queda como comparación marcada «NO usar en el examen». | 10/09, 01/10 | `solver/intervals.py` (`ic_proporcion_normal`), `pages/1_…` |
| Criterio de aproximación con el n **resultante** | Normal si n·p > 10 y n·(1−p) > 10; Poisson si p ≤ 0,005; si se cumplen las dos o ninguna, **Mermoz**: n₀ = 0,23(1−p)²/p³ (p ≤ 0,5; si no 0,23p²/(1−p)³), n > n₀ ⇒ normal. En ensayos y planes se verifica con p₀. Nada de n ≥ 30 ni n·p ≥ 5. Si el criterio no habilita una aproximación, se muestra con ⚠️ y su n **no** se informa como respuesta. | 10/09, 17/09, 24/09 | `solver/aproximaciones.py`, `prop_n`, `prop_diseno` |
| III-11c: 855 por Poisson es incorrecto | Con n = 855, n·p₀ = 102,6 > 10 ⇒ normal. Valen el exacto 755 (r_c = 106) o la normal 715. | 17/09 | `prop_diseno` |
| Decisión en p con r contra r_c (a priori) | La decisión es r ≥ r_c (o r ≤ r_c). El α* se muestra solo como «dato informativo». Lo mismo en medias y comparaciones. | 20/08, 17/09 | `prop_ensayo`, `media_ensayo`, `dos_muestras.py` |
| Elección de r_c | Entre los dos valores del aplicativo, el que deja **α real ≤ α**; se muestran G_b (o F_b) de los dos vecinos. | 17/09, 01/10 | `_eleccion_rc` |
| Sin bilaterales en p, σ², σ ni comparaciones | Si se pide bilateral se avisa y se plantea el unilateral que sugiere el enunciado o la muestra; en comparaciones la muestra orienta («¿difieren?» ⇒ el de mayor media supera al otro). Ya no se muestra un «bilateral de referencia». Las páginas no ofrecen bilateral en esos casos. | 03/09, 10/09, 01/10 | `_sin_bilateral`, `_cola_relacion`, `dos_muestras.py`, páginas 2 y 3 |
| Ensayo auxiliar F (amalgamado o Welch) | Unilateral, la varianza muestral mayor se sospecha mayor (H0: σ(mayor)/σ(menor) ≤ 1), con **α propio = 0,10** (no el del problema); se informa J contra Jc. No se rechaza ⇒ amalgamado; se rechaza ⇒ Welch. | 08/10 | `dos_muestras._plantear`, `two_samples.f_test_equal_variances`, página 3 |
| Sin β ni n con t | En ensayos de medias con σ desconocido (una población) y en comparaciones con amalgamado, Welch o apareadas no se calculan β, potencia ni n (t no central): el intérprete responde «fuera de la cátedra» y la página 2 no lo ofrece. | 03/09, 08/10 | `FueraDeCatedra` en `resolver.py`, `dos_medias_beta`, página 2 |
| Welch y diferencias porcentuales | ν de Welch **truncado**; h² en el término de la población que lleva h, también dentro de ν. Porcentaje mínimo: inecuación en h, cuadrática y **verificación de cada raíz** (V-8d: sirve 1,0490, no 1,1906). | 08/10, 15/10 | `two_samples.error_dos_medias`, `dos_muestras._inecuacion_h` |
| Estimador contra crítico | Se compara el estimador en unidades (x̄ con x̄c, S con Sc, r con r_c, J con Jc, D con Dc), no estadísticos observados t / F / χ². El ν·S²/σ₀² queda como dato porque la guía lo informa (II-9). | 27/08, 08/10, 15/10 | `varianza_ensayo`, `dos_var_ensayo` |
| χ²: controles y dominio | N ≥ 60 y Fe ≥ 5 (amalgamar); ν con clases **efectivas**; en discretas se completa el dominio con una clase de O = 0 y probabilidad **acumulada** (G o F), no la puntual; aviso de **ajuste demasiado perfecto** si χ² < χ²(α; ν). H0 de independencia en palabras y la de consistencia por categoría; al rechazar consistencia, «alguno es distinto». Discretas: si no se rechaza y se cumple el proceso físico, «sigue el modelo»; si no, «buen candidato». | 22/10 | `solver/chi_square.py`, `solver/ajuste.py`, `chi_modelos.py`, `resolver._hipotesis_contingencia` |
| χ²: dominio en modelos continuos | Si el dominio del modelo excede el recorrido observado, se agregan clases **nuevas** con Fo = 0 y probabilidad acumulada (F al principio, G al final); no se estiran las clases observadas. Se amalgaman solo si Fe < 5. VI-15, Gumbel del mínimo: «≤ 0» con Fe 7,04 queda sola ⇒ χ² = 68,56, ν = 4 (antes 64,84, ν = 3). Continuas: no rechazar ⇒ «buen candidato»; el mejor ajuste es el de menor χ². | 29/10 | `solver/ajuste.ajuste_continuo` |
| Probabilidades nunca en % | α, β, 1−β y P(…) entre 0 y 1 («Con α = 0,05…»). Se admite «95 % de confianza» y una proporción en % si piden porcentaje. | 01/10 | `solver/wording.py`, `chi_modelos.py`, `regresion.py` |
| Conclusión | «Se rechaza H0: se puede asegurar que…» / «no hay evidencia suficiente para asegurar que…»; nunca «acepto H0». | 20/08, 27/08 | `wording.conclusion_formal` |
| Justificación de Z y t | Por la estructura: al estandarizar x̄ se divide por el parámetro σ (constante) ⇒ Z; se divide por S (variable aleatoria) ⇒ t con ν = n − 1. Nunca «uso Z porque conozco σ». Notación F / G / Φ (β = F_b(r_c − 1 | n; p₁)…). | 01/10, 08/10 | `resolver.py`, `presentacion.py` |
| Periódicos como fracción | p₀ = 1/37 se muestra como fracción, no truncado. | 01/10 | `hypothesis_one.p_txt` |
| Decimales | Mínimo **4 decimales** en el desarrollo (fractiles, críticos, n y ν sin redondear); el resultado final se expresa según la variable (ver «Decimales» abajo) y los cálculos encadenados usan siempre los valores exactos. | 20/08, 01/10 | `interprete/redondeo.py`, `resolver.py` |

## Aplicadas (deducidas de la guía)

| Regla | Detalle | Evidencia | Qué dice el profesor |
|---|---|---|---|
| Población finita | Factor **√((N − n)/N)** (no N − 1), siempre que el enunciado da N, sin umbral n/N. | I-34b/c solo se reproducen así (53.808,01 y 58.991,99). | Coincide: el apunte (cap. 1) y el profesor usan **√((N − n)/N)** y n = N·n∞/(N + n∞). «Algunos autores ponen sobre N − 1. El uno mucho no hace» (20/08). La app muestra también el valor con N − 1 como dato. |
| β en ensayos de medias | Se calcula con el valor crítico **redondeado hacia afuera a 4 decimales** (`hyp.critico_catedra`). | I-9b, I-11b, I-27b. | El profesor calcula β con el crítico **con todos sus decimales** («no es 11,55 exacto, sino que tiene varios decimales»). Es Tema I (1° parcial): se deja así para reproducir la guía; la diferencia está en el 4° decimal. |
| Intervalos | Límite inferior hacia abajo y superior hacia arriba; cotas: la máxima hacia arriba, la mínima hacia abajo (`interprete/redondeo.py`). Los cálculos encadenados usan siempre los valores exactos, que se muestran entre paréntesis. | Más de 50 límites de la guía (I-3b, II-1, III-4, IV-1a, V-17b, VII-12c…). | Coincide («esto es estadística, no matemática»). |
| Valores críticos | Se informan hacia afuera de μ₀: cola derecha hacia arriba, izquierda hacia abajo. La decisión usa el exacto. | I-16 37,5698 → 37,56; I-20 4,5822 → 4,59; I-36 1,0696 → 1,07. | Compatible (I-10: 10,5238 → 10,52). En el desarrollo se muestra el valor con 4 decimales. |
| Decimales (presentación final) | Base por tipo: medias y totales 2, σ 2, σ² 4, p y cocientes 4, predicciones de regresión 4. Se agregan decimales hasta mostrar 3 cifras significativas; en medias también del error e. Es solo la expresión del resultado: el desarrollo va con ≥ 4 decimales. | II-1 0,00158; II-5 1,56; I-36b 0,985 y 1,215. | «Cómo expresan los resultados dependerá de la variable»; pero el desarrollo, mínimo 4 decimales. |
| Hipótesis «a la luz de los datos» | Si la hipótesis se plantea después de ver la muestra, el ensayo es unilateral hacia donde apunta la muestra, aunque el problema sea de control. | I-36a (x̄c = 1,07), I-32a. | Correcto en comparaciones (01/10). En una población la dirección sale de lo que el enunciado quiere probar (ruleta, III-19: de la denuncia). |
| Plan de muestreo por Poisson | Ecuación de García: CASO I c = ⌊ν/2⌋, g.l. = 2c, n = máx[χ²(α; 2c)/(2p₀) ; χ²(1 − β; 2c)/(2p₁)], r_c = c + 1; CASO II r_c = ⌈(ν − 2)/2⌉, g.l. = 2r_c + 2. **Solo se informa si el criterio de aproximación con el n resultante habilita Poisson.** | III-17 (227), III-22a (325), III-22b (186), III-21 (30, con la tabla). | III-11c (855) **ya no**: el profesor dijo que es incorrecto. |
| Plan exacto «más próximo a las premisas» | Además del plan de n mínimo: entre los planes que cumplen α y β con r_c mínimo o el siguiente, el de menor \|α_real − α\| + \|β_real − β\|. | III-16c (3.667), III-17 (226), III-22b (218): 10 de 11 planes de la guía. | El profesor da el exacto como el menor n con G ≤ α y F ≤ β (III-16a: 1675 / 233): es el que la app informa primero. |
| Diseño del ensayo de relación de varianzas | Se informa ν además de n = ν + 1. | IV-2c (ν = 482, n = 483). | Coincide (IV-1: ν = 44 ⇒ n = 45; IV-4: ν = 127 ⇒ n = 128). |

## Evaluadas y NO aplicadas (a propósito)

| Idea | Por qué no |
|---|---|
| t de tabla con 4 decimales en regresión | Reproduce VII-5b (199.813,14) pero empeora otros 16 límites que con el valor exacto coinciden. |
| Probabilidades con 4 decimales y Fe con 2 en χ² | Probado en VI-20: no lo reproduce (la cátedra además usa z con 2 decimales en la tabla) y empeora c). |
| R² redondeado antes del F global | Solo hay un caso (VIII-1, 92,0874 contra 92,0256 exacto) y la decisión no cambia. |
| IC de p con α/2 cuando r = 0 (como la guía) | El profesor dijo que está mal (17/09). Se aplicaba antes; desde el 28/10/2026 la app usa α entero. |
| Plan por Poisson aunque el criterio no lo habilite (III-11c = 855) | El profesor dijo que es incorrecto (17/09). Se informaba antes «como referencia». |
| Bilateral «de referencia» en comparaciones | «Jamás me planteen una hipótesis bilateral en comparación» (01/10). Se mostraba antes como referencia. |

## Erratas y diferencias conocidas de la guía

Están explicadas inciso por inciso en `datos/diferencias_explicadas.json`, y `herramientas/generar_resueltos.py`
las muestra en `Guia_resuelta.md` (secciones «Discrepancias» y «Coinciden solo aproximadamente»). Resumen:
III-3b y III-11c (la app sigue al profesor), I-4a (20.203,88 por 20.203,87), III-16a (CR 229 y RD 228), V-3b
(e impreso distinto en a y b), VIII-1 (R²aj 0,9438 por 0,9382), VIII-2b (R²aj con n − k), III-18 (plan que ninguna
regla reproduce), III-15d (Poisson por tanteo).
