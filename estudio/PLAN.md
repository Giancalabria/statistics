# Plan de estudio: 2° parcial de Estadística Aplicada

- **Fecha del parcial:** jueves 19/11/2026. Duración: mínimo 120 minutos.
- **Materia:** Estadística Aplicada (UADE). Docente: Ing. Sergio Aníbal Dopazo.
- **Régimen:** final obligatorio (no se promociona), se puede recuperar **un solo** parcial. Final regular, probablemente el 17/12 o el 21/12 (a confirmar).
- **Entra (deducido de las clases):** ensayos sobre p (III), comparación de varianzas (IV), comparación de medias independientes y apareadas (V), χ² (VI) y regresión (VII; la múltiple solo si se da).
- **Herramientas en el examen:** apuntes, computadora con programas propios (este repo, con la IA local), *Probability Distributions*, Excel y calculadora. Wifi apagado y celular en modo avión.

---

## Enfoque (desde el 31/10)

En el examen **el solver resuelve y yo controlo**. No voy a hacer cuentas a mano, así que no se estudian cuentas. Las cuentas del solver están verificadas (532/536 en la guía y sin errores de cálculo en los exámenes reales); **lo que falla es el planteo**: qué tema es, qué parámetro se estima, H0 y la cola, α, qué grupo va primero, qué datos se tomaron. Ver [GUIA_CONTROL.md](GUIA_CONTROL.md).

Lo que hay que entrenar:
1. **Controlar el planteo** que muestra la app con la guía de control, y corregirlo cuando está mal.
2. **Pasarlo a la hoja** como lo corrige el profesor: H0 justificada en palabras, distribución justificada, 4 decimales, conclusión en términos del problema, «no se rechaza» (nunca «se acepta»). Ver [REGLAS_PROFESOR.md](REGLAS_PROFESOR.md).
3. **El circuito completo con tiempo**: cargar → controlar → corregir → escribir, para 4 problemas en 120 minutos.

La teoría se estudia **solo en lo conceptual**: cuándo se usa cada test, cómo se plantea H0, qué significa el resultado. Cada vez que la app se equivoca en una práctica, se anota el caso en la guía de control.

---

## Cómo es una sesión de práctica

1. Claude me da un examen real (o un problema de la guía) **sin la resolución**.
2. Lo cargo en la app (modo 🗳️ Consenso), con el reloj corriendo.
3. Controlo cada inciso con [GUIA_CONTROL.md](GUIA_CONTROL.md) y corrijo lo que esté mal.
4. Escribo la respuesta como la entregaría.
5. Claude la compara con la referencia y con `REGLAS_PROFESOR.md`: qué se me escapó del planteo, qué falta en la redacción y cuánto tardé.
6. Lo que la app hizo mal (y si lo detecté o no) se anota en la guía de control y en **Errores detectados** abajo. Si es un error general de la app, se corrige el solver.

Cada examen nuevo sirve además como **prueba a ciegas de la app** (se corre `python herramientas/evaluar_examenes.py --ia` antes de tocar nada).

---

## Estado actual

> Actualizar al final de cada sesión.

**Última actualización:** 31/10/2026. Plan reemplazado por el enfoque «el solver resuelve, yo controlo». El plan anterior (resolver en papel) quedó en `informes/plan_anterior_31-10.md`, con los valores de los ejercicios hechos en clase.

| Fecha | Qué | Estado |
|---|---|---|
| Sáb 31/10 | Plan nuevo y guía de control | ✅ |
| Dom 01/11 | Examen 1: 2° parcial 23/06/25 (Q) + teoría mínima de p y comparación de medias | ⬜ |
| Lun 02/11 | Examen 2: recuperatorio del 2° parcial 2024 (R) + teoría mínima de varianzas y χ² de ajuste | ⬜ |
| Mar 03/11 | Examen 3: final 12/12/2024 (F) + teoría mínima de regresión | ⬜ |
| Mié 04/11 | Examen 4: final 15/12/25 (P) | ⬜ |
| **Jue 05/11** | Clase (validación de regresión). Procesarla: reglas nuevas a `REGLAS_PROFESOR.md`, solver y guía de control | ⬜ |
| Vie 06/11 | Examen 5: 2° parcial 10/11/25 (T) con el circuito completo y cronómetro | ⬜ |
| Sáb 07/11 | Temas que no salieron en los exámenes: apareadas (V-12 a V-21) | ⬜ |
| Dom 08/11 | χ² de consistencia e independencia (VI-1 a VI-9) | ⬜ |
| Lun 09/11 | Diseño de p con α y β (III-16, III-22) y varianzas (IV-1, IV-4) | ⬜ |
| Mar 10/11 | Problema combinado tipo VI-20 y bondad de ajuste continua (VI-15, VI-18) | ⬜ |
| Mié 11/11 | Regresión con validación (VII-12, VII-13) | ⬜ |
| **Jue 12/11** | Clase. Procesarla como la del 05/11 | ⬜ |
| Vie 13/11 | Lo nuevo de la clase del 12/11 | ⬜ |
| Sáb 14/11 | **Simulacro 1**: examen armado por Claude con problemas que la app no vio, 120 minutos | ⬜ |
| Dom 15/11 | Corregir el simulacro; repasar los errores no detectados | ⬜ |
| Lun 16/11 | **Simulacro 2** | ⬜ |
| Mar 17/11 | Corregir; repasar la guía de control completa | ⬜ |
| Mié 18/11 | Compu lista y probada sin wifi (ver abajo). Descansar | ⬜ |
| **Jue 19/11** | **Parcial** | |

Leyenda: ⬜ pendiente · 🟨 en curso · ✅ terminado

**Errores detectados en las prácticas** (míos al controlar o al redactar):
- (todavía nada)

**Para confirmar con el profesor o el campus:**
- Si entra regresión múltiple. El recuperatorio del 2° parcial de 2024 tuvo **elección entre 4 modelos de regresión múltiple con R², S², PRESS, DET y Cp/p**: la app no está probada en eso.
- Si en el test F auxiliar acepta un α mayor que 0,10.
- Fecha del final (17/12 o 21/12).

---

## Banco de exámenes reales

Están en `datos/examenes_reales.json`, con la referencia de cada inciso.

| Id | Examen | Temas | Practicado |
|---|---|---|---|
| Q1–Q2 | 2° parcial 23/06/25 | diseño de p con α y β; dos medias con tabla de clases + ajuste Normal | no |
| R1, R3, R4 | Recuperatorio del 2° parcial 2024 (Notion) | ajuste Poisson; dos varianzas; regresión simple | no |
| F1–F4 | Final 12/12/2024 (Notion) | dos medias con tabla de resumen; regresión | no |
| P1–P3 | Final 15/12/25 | regresión; dos medias + ajuste Exponencial; p | no |
| T1–T2 | 2° parcial 10/11/25 | dos medias % con tabla de clases + Gamma; p | no |
| E1–E2 | 1° parcial 29/04/25 (corregido) | μ y σ² (no entra; sirve para ver cómo corrige) | — |

Si consigo más exámenes (sobre todo 2° parciales corregidos), son lo más valioso: se agregan al banco y se usan como práctica y como prueba a ciegas.

---

## Compu para el examen (probar el 18/11 con el wifi apagado)

- El solver levanta sin internet y Ollama responde con `qwen3:8b` (modo 🗳️ Consenso, sin «pensar»).
- Plan B si la IA no anda: la app funciona solo con reglas (modo reglas); controlar más todavía el planteo.
- *Probability Distributions* sin actualizar; Excel con `GAMMA.LN` y el Solver activado (Weibull).
- Apuntes, la guía de control y `REGLAS_PROFESOR.md` descargados o impresos.

---

## Fuentes en NotebookLM

| Fuente | ID (prefijo) | Tema |
|---|---|---|
| Guia Problemas Estadística Aplicada 2026.pdf | `35d7e4aa` | todos |
| 2 - Ensayos de Hipótesis.pdf | `86c936b8` | p |
| 3 - Comparación de Parámetros.pdf | `87c43290` | varianzas, medias |
| 4 - Contrastes Chi Cuadrado.pdf | `1a475a44` | χ² |
| 5 - Teoría de la Regresión.pdf | `490fa323` | regresión |
| 6 - Apéndice A - Resumen de los Modelos.pdf | `908d16a4` | ajuste |
| Ajustes por momentos Distribución Weibull.pdf | `363bfffd` | ajuste |
| Clase 17/09 (ensayos de p) | `74a36b3b` | p |
| Clase 24/09 (n exacto de p, III-16) | `c53e34bf` | p |
| Clase 01/10 (devolución del 1° parcial, IV-1) | `3871c490` | reglas, varianzas |
| Clase 08/10 (IV-4, medias, V-8) | `2c1ebc03` | varianzas, medias |
| Clase 15/10 (V-8, apareadas, inicio de χ²) | `fef55656` | medias, apareadas, χ² |
| Clase 22/10 (χ²) | `7bf95c9c` | χ² |
| Clase 29/10 (χ² continuas, VI-15, inicio de regresión) | `434667af` | ajuste, regresión |
| Clases 06/08 a 10/09 (1° parcial) | `490c7079` … `27fda49a` | reglas |
