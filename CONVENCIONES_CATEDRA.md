# Convenciones de la cátedra que aplica la app

Reglas deducidas recalculando las respuestas de la guía **dígito a dígito**. Varias salen del trabajo de
un compañero ([royvicente/estadistica-avanzada](https://github.com/royvicente/estadistica-avanzada),
`docs/conocimiento/convenciones-catedra.md`), y acá se verificaron con nuestro intérprete.

Para medirlas, `python herramientas/evaluar_guia.py` tiene la columna **exactos**: cuántos valores de la
guía coinciden en todos sus dígitos (con redondeo común o hacia afuera), además de la columna con tolerancia.
`--fallas` marca con `OK~` los incisos que coinciden solo aproximadamente.

## Aplicadas

| Regla | Detalle | Evidencia |
|---|---|---|
| Población finita | Factor **√((N − n)/N)** (no N − 1), siempre que el enunciado da N, sin umbral n/N. | I-34b/c solo se reproducen así (53.808,01 y 58.991,99). |
| β en ensayos de medias | Se calcula con el valor crítico **redondeado hacia afuera a 4 decimales** (`hyp.critico_catedra`). | I-9b, I-11b, I-27b. |
| Intervalos | Límite inferior hacia abajo y superior hacia arriba; cotas: la máxima hacia arriba, la mínima hacia abajo (`interprete/redondeo.py`). Los cálculos encadenados usan siempre los valores exactos, que se muestran entre paréntesis. | Más de 50 límites de la guía (I-3b, II-1, III-4, IV-1a, V-17b, VII-12c…). |
| Valores críticos | Se informan hacia afuera de μ₀: cola derecha hacia arriba, izquierda hacia abajo. La decisión usa el exacto. | I-16 37,5698 → 37,56; I-20 4,5822 → 4,59; I-36 1,0696 → 1,07. |
| Decimales | Base por tipo: medias y totales 2, σ 2, σ² 4, p y cocientes 4, predicciones de regresión 4. Se agregan decimales hasta mostrar 3 cifras significativas; en medias también del error e. | II-1 0,00158; II-5 1,56; I-36b 0,985 y 1,215. |
| Hipótesis «a la luz de los datos» | Si la hipótesis se plantea después de ver la muestra, el ensayo es unilateral hacia donde apunta la muestra, aunque el problema sea de control. | I-36a (x̄c = 1,07), I-32a. |
| IC de p con r = 0 (o r = n) | La guía usa α/2 también en ese caso; la app la sigue y avisa el valor con α entero. | III-3b: 0,2589 (con α entero: 0,2057). |
| Plan de muestreo por Poisson | Ecuación de García: CASO I c = ⌊ν/2⌋, g.l. = 2c, n = máx[χ²(α; 2c)/(2p₀) ; χ²(1 − β; 2c)/(2p₁)], r_c = c + 1; CASO II r_c = ⌈(ν − 2)/2⌉, g.l. = 2r_c + 2. | III-11c (855), III-17 (227), III-22a (325), III-22b (186). |
| Plan exacto «más próximo a las premisas» | Además del plan de n mínimo: entre los planes que cumplen α y β con r_c mínimo o el siguiente, el de menor \|α_real − α\| + \|β_real − β\|. | III-16c (3.667), III-17 (226), III-22b (218): 10 de 11 planes de la guía. |
| Diseño del ensayo de relación de varianzas | Se informa ν además de n = ν + 1. | IV-2c (ν = 482, n = 483). |

## Evaluadas y NO aplicadas (a propósito)

| Idea | Por qué no |
|---|---|
| t de tabla con 4 decimales en regresión | Reproduce VII-5b (199.813,14) pero empeora otros 16 límites que con el valor exacto coinciden. |
| Probabilidades con 4 decimales y Fe con 2 en χ² | Probado en VI-20: no lo reproduce (la cátedra además usa z con 2 decimales en la tabla) y empeora c). |
| R² redondeado antes del F global | Solo hay un caso (VIII-1, 92,0874 contra 92,0256 exacto) y la decisión no cambia. |

## Erratas y diferencias conocidas de la guía

Están explicadas inciso por inciso en `datos/diferencias_explicadas.json`, y `herramientas/generar_resueltos.py`
las muestra en `Guia_resuelta.md` (secciones «Discrepancias» y «Coinciden solo aproximadamente»). Resumen:
I-4a (20.203,88 por 20.203,87), III-16a (CR 229 y RD 228), V-3b (e impreso distinto en a y b),
VIII-1 (R²aj 0,9438 por 0,9382), VIII-2b (R²aj con n − k), III-18 (plan que ninguna regla reproduce),
III-15d (Poisson por tanteo).
