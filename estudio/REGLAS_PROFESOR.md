# Reglas del profesor (Dopazo) para el 2° parcial

Sacadas de las grabaciones de clase del 06/08 al 22/10/2026. El detalle, con citas y fechas, está en `informes/`. **Lo que dice el profesor manda sobre la guía, el apunte y el repo.**

---

## 1. Cómo corrige

- **Corrige la interpretación, no solo los números**: "Si falta alguno de esos elementos, considero que el problema está mal hecho, aunque los números estén bien".
- **Toma problemas ya resueltos de la guía y del apunte**, y los "tips" que da en clase. "Si hacés todos los problemas de la guía, 99% de seguridad que aprobás".
- **Se resuelve como en clase**, no como un profesor particular ni como la IA. "Al primero que veo resolviendo con la IA le pongo cero".
- **Mostrar el desarrollo y las iteraciones**: un resultado sin desarrollo "lo sacaste de la galera".
- **Justificar el método** (qué distribución, qué aproximación, qué caso de comparación).
- **Herramientas**: apuntes, computadora, Excel y programas propios, con wifi apagado y el celular en modo avión (escanea los equipos). Aplicativo *Probability Distributions* (Matthew Bognar) instalado, no la versión web. Probar los programas propios con la guía antes del examen.
- Las dudas se preguntan **antes** del examen, no durante.

## 2. Errores que penalizó en el 1° parcial (no repetir)

1. **Probabilidades en %.** α, β, 1−β y cualquier P(...) van entre 0 y 1. "El primero que me ponga 30% de probabilidad, olvídate de aprobar". Se admite "90% de confianza" y una proporción en % si piden "porcentaje".
2. **Hipótesis sin justificar en palabras.**
3. **Mal fundamento de la distribución.** No es "uso la normal porque conozco σ" ni "uso t porque no conozco σ". Es:
   - x̄ es normal; al estandarizar se divide por un parámetro (σ), y una normal dividida por una constante sigue siendo normal ⇒ Z.
   - Si se divide por S, que es una variable aleatoria (raíz de una gamma / χ²), queda una t de Student con ν = n−1.
4. **Estimar p con la aproximación normal** ("aberración"). La estimación de p es siempre exacta. Las aproximaciones solo sirven para calcular n.
5. **Trabajar con 2 decimales o truncar periódicos.** Mínimo 4 decimales en todo el desarrollo; los periódicos como fracción (1/37).
6. **Crítico del lado equivocado o comparado contra μ₀.** Se compara el **estimador** contra el **valor crítico**.

Errores que anticipó para el 2° parcial:
- Dividir α por 2 cuando piden **un solo límite** ("mínimo", "máximo"). Con un límite, α entero.
- Creer que **n iguales ⇒ muestras apareadas**. Son apareadas solo si es el mismo individuo o la misma unidad experimental.
- En bondad de ajuste, usar la probabilidad **puntual** en la clase que completa el dominio, en lugar de la **acumulada** (G o F).
- En n para desvíos, usar R' en lugar de **R = R'²**.
- Confundir α con β en la fórmula de n.

## 3. Planteo de H0 y H1

- **Regla madre**: H0 se plantea de modo que el **error de tipo I sea el más grave**.
- **Orden para decidir**: (1) si el enunciado dice qué se quiere probar, eso va en **H1**; (2) si no, criterio; (3) si no alcanza, comparar la gravedad de los errores.
- **Pesimista** (riesgo económico: inversión, máquina nueva, proveedor nuevo, producto nuevo, modificación, campaña publicitaria): H0 = "no funciona / no cumple". **Pesimista aunque la campaña sea barata**, si lo que se quiere es probar que fue efectiva.
- **Optimista** (control de proceso, control de recepción de un **proveedor habitual**, controles de rutina): H0 = "cumple / está bajo control". Rechazar H0 = detener o rechazar el lote.
- **La igualdad va siempre en H0.** Escribir primero en palabras y después en símbolos.
- **No hay bilaterales en σ², σ, p ni en comparaciones de dos poblaciones.** "Jamás me planteen una hipótesis bilateral en comparación". En comparaciones, la muestra orienta: si S₂ > S₁, lo único que se puede intentar probar es σ₂ > σ₁.
- **α**: si no lo dan, se elige y se justifica. Escala: chico ≤ 0,01, estándar 0,05, grande ≥ 0,10. Ejemplo de la ruleta: 0,05 "no porque sea estándar", sino porque el perito tiene que ser imparcial. **Una vez fijado, α no se toca.** Nunca fijar α después de ver la muestra ni decidir con el p-value.
- Escribir **las 4 probabilidades** (α, 1−α, β, 1−β) en términos del problema.

## 4. Pasos del ensayo (en este orden)

1. **Variable** en palabras, con unidad.
2. **H0 / H1** con el criterio justificado.
3. **α** (y β en el valor alternativo, si corresponde).
4. **n** (si no está dado).
5. **Valor crítico, CR y RD**, antes de ver la muestra. La RD va en lenguaje de planta: "si en 1637 encuestados hay 229 o más interesados, se inicia una nueva campaña".
6. **Estimador** de la muestra.
7. **Comparar estimador contra crítico y concluir.**
   - Se rechaza H0: "puedo asegurar que…".
   - No se rechaza: "no hay evidencia suficiente para asegurar que…". **Nunca "acepto H0"**: jamás se prueba la igualdad ni la independencia.

## 5. Notación y redondeos

- Parámetros con letras griegas (μ, σ, ψ, φ, Δ); p es la excepción. Estimadores con latinas (x̄, S, p̂, J, D).
- **P = puntual, F = acumulada izquierda, G = acumulada derecha, Φ = F de la normal estándar.** Escribir P(X ≤ x) en lugar de F es un "error conceptual".
- Escribir "ν = número de grados de libertad".
- Mínimo **4 decimales** en el desarrollo y los fractiles. El resultado final se expresa según la variable (con unidades).
- "Los redondeos en estadística son lógicos, no matemáticos":
  - n y ν al entero superior;
  - ν de Welch se **trunca** (124,9 → 124);
  - en los IC, el límite inferior hacia abajo y el superior hacia arriba;
  - en discretas, el rc tiene que cumplir α real ≤ α estipulado.
- "Aumento de 3 **puntos**" es 0,12 → 0,15, no 0,12·1,03.

---

## 6. Ensayos sobre p (Tema III)

- Siempre unilateral:
  - caso 1, H0: p ≤ p₀; rc tal que G_b(rc | n, p₀) ≤ α; CR: r ≥ rc; β = F_b(rc−1 | n, p₁);
  - caso 2, H0: p ≥ p₀; rc tal que F_b(rc | n, p₀) ≤ α; CR: r ≤ rc; β = G_b(rc+1 | n, p₁).
- El aplicativo da dos valores de rc: se elige el que deja **α real ≤ α**.
- Se decide con **r ≥ rc** (a priori). p̂ > p̂c es equivalente. El α* (p-value, a posteriori) "no me gusta": no usarlo para decidir.
- **n del plan**:
  - Exacto: el menor n con G ≤ α y F ≤ β (con programa o Excel).
  - Aproximación normal: n = [(z₁₋α·√(p₀q₀) + z₁₋β·√(p₁q₁)) / (p₁ − p₀)]².
  - Aproximación Poisson: con R = p₁/p₀ y χ² (Wilson-Hilferty). Si los n difieren, se toma el mayor.
  - **Justificar la aproximación con el n resultante**: normal si n·p > 10 y n·(1−p) > 10; Poisson si p ≤ 0,005; si se cumplen los dos o ninguno, **criterio de Mermoz**: n₀ = 0,23·(1−p)²/p³ (p ≤ 0,5); si n > n₀, normal, si no, Poisson. "No me usen otro criterio". Nada de "n ≥ 30" ni "np ≥ 5".
- Vocabulario de recepción: AQL = p₀ con α = riesgo del proveedor; RQL / LTPD = p₁ con β = riesgo del comprador.
- **IC de p con r = 0**: el límite superior va con **α entero** (B = 0,2057 en III-3b). La guía dice 0,2589 y el profesor dijo que está mal.
- **III-11c**: n = 855 por Poisson es incorrecto (el criterio se aplicó con el n inicial). Valen el exacto 755 o la normal 715.

## 7. Comparación de varianzas o desvíos (Tema IV, distribución F)

- ψ² = σ₁²/σ₂², con estimador J² = S₁²/S₂² y distribución F(ν₁ = n₁−1; ν₂ = n₂−1). **Pensar qué va en el numerador.** Usar letras (A/B, CR/SR) en lugar de 1/2.
- IC: A = J²/F(1−α/2; ν₁, ν₂) y B = J²/F(α/2; ν₁, ν₂). Para los desvíos, A' = √A y B' = √B.
- **Interpretar en %**: "σA² como mínimo 79,65% menor y como máximo 11,37% mayor que σB²".
- Relación entre límites R = B/A. n con n₁ = n₂, iterando ν (n = ν + 1). Para desvíos, **R = R'²**.
- Si no especifican la relación (A/B o B/A), se elige una, se dice cuál y se resuelve solo esa.
- **Ensayos**:
  - caso 1, H0: ψ² ≤ ψ₀²: J²c = ψ₀²·F(1−α), CR: J² > J²c, β = F_F(ψ₀²/ψ₁²·F(1−α));
  - caso 2, H0: ψ² ≥ ψ₀²: J²c = ψ₀²·F(α), CR: J² < J²c, β = 1 − F_F(ψ₀²/ψ₁²·F(α)).
  - Con desvíos, "el φ va al cuadrado": Jc = √(φ₀²·F). Comparar J con Jc.
  - "Reducir el desvío un 12%" ⇒ H0: φ ≥ 0,88.
  - n con n₁ = n₂: R = ψ₁²/ψ₀² en el caso 1 y ψ₀²/ψ₁² en el caso 2; tiene que dar > 1.

## 8. Comparación de medias (Tema V)

- **Elegir el método** (y justificarlo):
  1. σ₁ y σ₂ conocidos ⇒ Z (es teórico: "jamás vas a conocer ambos").
  2. Desconocidos ⇒ **test F auxiliar previo**:
     - unilateral, con la varianza muestral mayor sospechada mayor;
     - **α grande propio (0,10)**, no el del problema;
     - no se rechaza ⇒ **amalgamado**; se rechaza ⇒ **Welch**.
  3. Mismo individuo o unidad experimental ⇒ **apareadas** (d̄, S_D, t con n−1).
- **Amalgamado**: S²a = [(n₁−1)S₁² + (n₂−1)S₂²]/(n₁+n₂−2), con ν = n₁+n₂−2. Control: S²a tiene que quedar entre S₁² y S₂².
  - Caso 1 (H0: Δ ≤ Δ₀): Dc = Δ₀ + t(1−α)·Sa·√(1/n₁+1/n₂). Caso 2: con −.
- **Welch**: √(S₁²/n₁ + S₂²/n₂), con ν = (S₁²/n₁ + S₂²/n₂)² / [(S₁²/n₁)²/(n₁−1) + (S₂²/n₂)²/(n₂−1)], **truncado**.
- **Diferencias porcentuales**:
  - "μ₁ supera en un 10% a μ₂" ⇒ Δ* = μ₁ − 1,10·μ₂, con estimador D* = x̄₁ − 1,10·x̄₂.
  - Error: Sa·√(1/n₁ + h²/n₂). **h² va en el término de la población que lleva h**; en Welch también dentro de ν.
- **Porcentaje mínimo**: plantear la CR como inecuación en h, elevar al cuadrado y resolver la cuadrática. **Verificar cada raíz** en la inecuación original (en V-8d sirve 1,0490 y no 1,1906).
- El estimador tiene que ser coherente con el parámetro: nunca comparar contra Δ₀.
- **Sin β ni n en ensayos de medias con t** (necesitan la t no central).
- Diferencia mínima o máxima: un solo límite, con t(1−α).

## 9. Contrastes χ² (Tema VI)

- **Cuál usar**: "asociación" ⇒ independencia; "niveles, probabilidades o porcentajes" de varios grupos ⇒ consistencia; "se ajusta a / sigue un modelo" ⇒ bondad de ajuste.
- **H0**:
  - Consistencia: **por categoría**, p₁ª,M = p₁ª,T = p₁ª,N, y lo mismo para cada categoría ("no pongan P mañana, P tarde…").
  - Independencia: en palabras ("las fallas de pintura son independientes del color").
  - Bondad: "lo observado se ajusta al modelo X".
- Estadístico Σ(O−E)²/E, siempre con cola derecha: se rechaza si χ²obs > χ²(1−α; ν). α en general 0,05.
- Los observados no se tocan. Los esperados **llevan decimales** y las sumas tienen que cerrar. N ≥ 60 y todos los E ≥ 5 (los O pueden ser 0); si no, **amalgamar clases** (en los extremos o en el medio).
- ν:
  - tablas: (f−1)(c−1);
  - bondad: **clases efectivas** − 1 − (parámetros estimados con la muestra).
- **Completar el dominio**: agregar clase al final y/o al principio con O = 0 y probabilidad **acumulada** (G o F), no puntual.
  - Son clases **nuevas**: no se estiran las observadas. Se amalgaman solo si su E < 5. En VI-15 (Gumbel del mínimo), «≤ 0» da E = 7,04, queda sola y por eso ν = 4.
  - Depende del dominio del modelo: Gumbel y normal, en los dos extremos; Weibull, exponencial y gamma (x ≥ 0) con datos desde 0, solo al final.
- **Modelos continuos** (29/10):
  - Primero procesar los datos (x̄ y S con las marcas de clase). Las probabilidades siempre por intervalos.
  - Parámetros por momentos:
    - Gumbel: β = S·√6/π; θ = x̄ + 0,5772·β (mínimo) o θ = x̄ − 0,5772·β (máximo).
    - Weibull: por **Solver**, **Buscar objetivo** o la **tabla de ajuste por momentos** (CV = S/x̄). Cualquiera vale, pero **hay que decir cuál se usó**.
  - **No rechazar ⇒ «es un buen candidato»**, nunca «sigue el modelo», porque puede haber otro que ajuste mejor.
  - **Mejor ajuste** = el de menor χ² observado entre los que no se rechazan.
  - En el examen pide **un** modelo. VI-20 (comparación + ajuste) es el «típico problema».
  - Leer el apéndice del apunte (pp. 123 a 127) y los ejemplos resueltos de ajuste del apunte.
- **Ajuste demasiado perfecto**: si χ²obs < χ²(α; ν), sospechar de los datos.
- **Discretas, 3 situaciones**:
  - se rechaza ⇒ no sigue el modelo;
  - no se rechaza y se cumple el proceso físico ⇒ "sigue el modelo";
  - no se rechaza y no se cumple el proceso ⇒ "es un buen candidato".
- Al rechazar en consistencia: "alguna es distinta", no "todas son distintas".

## 10. Regresión (Temas VII y VIII)

Empezó el 29/10 (teoría y mínimos cuadrados). La validación queda para el 05/11. Detalle en `informes/informe_clase_13.md`.

- **«Lineal» = lineal en los parámetros**, no en X. Linealizables: los que se linealizan con logaritmo.
- **X = variable explicativa** (no decir «independiente»). Conviene que no sea aleatoria y que se pueda manipular. **Y = variable explicada**, siempre aleatoria. La dirección es única: Y en función de X.
- **β₀** = valor de Y cuando X no influye (grado de independencia de Y). **β₁** = **coeficiente de regresión** o **contribución marginal**, no solo «pendiente». **ε** = perturbación del entorno.
- Modelo promedio (β₀ + β₁X) y modelo puntual (+ ε).
  - Estimar el promedio = IC.
  - Estimar el valor puntual = **pronóstico** o predicción.
  - Ŷ sirve **solo si el modelo es válido**.
- Mínimos cuadrados: b₀ = ȳ − b₁x̄ (pasa por el baricentro) y b₁ = (Σxy − n·x̄·ȳ)/(Σx² − n·x̄²).
- Validar el modelo:
  1. H0: no hay relación.
  2. Que la relación sea fuerte.

  Son condiciones necesarias, no suficientes. Interesa causa-efecto, no relaciones casuales.
