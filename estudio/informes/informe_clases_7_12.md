# Informe: clases 7 a 12 (17/09 al 22/10/2026), Estadística Aplicada, Ing. S. A. Dopazo

Fuentes: transcripciones automáticas de las clases del 17/09, 24/09, 01/10, 08/10, 15/10 y 22/10. El archivo del 01/10 «(1)-converted» es **el mismo audio con otra pasada de ASR**: unas 700 palabras distintas sobre 15.000 y ningún contenido nuevo. También usé el chat del 06/08 para la logística, los chats de Gemini, los apuntes 2 a 6 y la guía.
Las citas están **textuales del ASR** (con sus errores). Los números de los ejercicios los **recalculé con scipy** (`.venv` del repo); cuando el ASR no se entiende, pongo el valor recalculado.
Para numerar uso la **guía** (Tema III = Bernoulli, IV = comparación de varianzas, V = dos medias, VI = χ², VII y VIII = regresión). Los capítulos del **apunte** se numeran distinto: 2 = ensayos, 3 = comparación, 4 = χ², 5 = regresión.

---

## 0. LO PRIMERO: el 2° parcial

### 0.1 Fecha y temario: lo que se sabe y lo que no
- **En las clases 7 a 12 el profesor no dice ni la fecha ni el temario del 2° parcial.** Las fechas se mostraron en pantalla en la primera clase (06/08): «ahí tienen la fecha de los del primero y segundo parcial … esto ustedes tienen todo esto lo tien subido». **Hay que sacarlas del campus.**
- Reglas generales que dio el 06/08:
  - Los parciales toman «lo que tomamos en función de hasta dónde llegamos». En el final se toma todo.
  - «Se puede recuperar un solo parcial».
  - Después del 2° parcial hay una clase más.
  - El final es obligatorio: «La materia no es promocionable».
  - Los que aprobaron los dos parciales pueden rendir el final anticipado (con toda la materia).
  - El final regular sería «el 17, el 12» (17/12, dato a confirmar).
- **Temario probable (es una inferencia, no lo dijo):** todo lo que se dio después de estimación de p.
  1. **Ensayos de hipótesis de p** (Tema III, apunte cap. 2). El 17/09 dijo: «ensayo de hipótesis que no va a entrar para el parcial, pero sí va a entrar para final». Se dio el 17/09 y el 24/09, y se resolvieron III-11, III-16 y III-19.
  2. **Comparación de dos poblaciones**: varianzas y desvíos (Tema IV) y medias (Tema V), independientes y apareadas.
  3. **Contrastes χ²** (Tema VI). Al 22/10 se dieron consistencia, independencia y bondad de ajuste a modelos empíricos y discretos (uniforme y Poisson). **Falta bondad de ajuste a modelos continuos** (Normal, Weibull, etc.).
  4. **Regresión (Temas VII y VIII): no se empezó al 22/10.** Que entre o no depende de la fecha del parcial.
  - Contexto del 1° parcial: entró todo el cap. 1 (estimación) más los ensayos de μ y σ² del cap. 2, pero no los ensayos de p. Lo confirma el 15/10: «Esto es lo mismo que hicieron para el primer parcial el x raya crítico».
- **No entra comparación de dos proporciones como tema propio.** El 15/10 dijo: «no va a haber problemas de comparaciones de proporciones puras, sino que lo vamos a ver dentro de otro tema» (χ² de consistencia).

### 0.2 Cómo toma el examen (todas las clases)
- **Se permite** carpeta y apuntes abiertos, computadora, Excel, programas propios, calculadoras programables y el aplicativo de distribuciones descargado.
  - 08/10: «yo les permito usar la computadora y trabajar con Excel».
  - 08/10: «si vos me resolvés con tu programa que te lo hiciste, correcto, bienvenido sea».
- **Sin internet:**
  - 17/09: «te voy a pedir que lo pongas en modo avión … voy a escanear todos los celulares y también voy a escanear las computadoras … wifi apagado».
  - 08/10: «Lo único que controlo es que no tengas conexión a internet».
  - Los apuntes tienen que estar descargados o impresos. La versión online del aplicativo (Matthew Bognar) no sirve: hay que tener la app instalada.
- Programas propios: «antes de usarlo en un examen, pruébenlo en las [de la guía] no van a ser que tengas errores» (24/09).
- Recomienda Excel (Solver / Buscar objetivo, tablas tipo «vector») y Python (bien para la binomial, «Python es una porquería» para otros modelos). Prefiere Java o R.
- **El estilo de resolución del examen es el de clase:** «los problemas se hacen como se resuelve en clase, no como te lo haga un [profesor] particular» (17/09).
- Sobre la guía (17/09): «si vos hacés todos los problemas de la guía, 99% de seguridad que aprobase». También pide hacer los resueltos.
- **Hay que justificar el método elegido** (24/09): «si usa la aproximación normal y no me dice por qué la está usando … uno cuando corrige se da cuenta si uno estudió o lo está haciendo mecánicamente».
- No preguntar durante el examen: «el día del examen … No me acuerdo de nada … Pregunten antes» (03/09).

### 0.3 Errores del 1° parcial según el profesor (devolución del 01/10)
Cita de contexto: «cometieron los errores que yo dije que iban a cometer en clase».

1. **Probabilidades expresadas en porcentaje.** «¿Cuántas veces dije que una [probabilidad] no se expresa en [porcentaje]? … muchos me expresaban las probabilidades en [porcentaje] … un error conceptual».
2. **No justificar las hipótesis en palabras.** «la mayoría ni justificó las hipótesis … Hay que justificarlo en palabras, hay que escribir».
3. **Mal fundamento de la distribución** («uso Normal porque conozco σ», «uso t porque no conozco σ»).
   - Cita: «No usas normal porque conoces [σ]; usas normal porque la variable que es la estimadora x raya es una variable normal y cuando vos estandarizás … normal dividido un parámetro me da normal … sigma no afecta el comportamiento de la variable».
   - La t sale porque «dividen por S … una variable aleatoria». Lo repitió el 08/10: «la normal divido la raíz cuadrada [de] una gama me da una t».
4. **Estimar p con la aproximación normal.** «solamente se usan aproximaciones para calcular el tamaño de muestra, no para estimar … Dije, no lo copien porque seguro que lo van a repetir en el examen. Lo repitieron».
5. **Trabajar con 2 decimales y truncar números periódicos.** «muchos también trabajaron con dos decimales … Dije, mínimo cuatro decimales. Mínimo». Sobre 1/37: «0,027 periódico … no [trunquen] los números periódicos» (usar la fracción).
6. **Valor crítico mal ubicado o comparado contra el valor de la hipótesis.** «Me compararon el [x raya] crítico que usted lo calculó con mu cero» y «con esta hipótesis me pusieron menos». O sea, pusieron la cola del lado equivocado o compararon el crítico contra μ0 en lugar de comparar el estimador contra el crítico.
7. Usar IA o profesores particulares (01/10 y 08/10): «no le pregunten a la IA porque la IA no sabe … no puede razonar» y «no voy a admitir que ustedes resuelvan problema o lo resuelve la [IA]». Lo dijo por «las cosas que he visto en los exámenes».

Errores que anticipó para el 2° parcial:
- «uno de los errores que cometen … ah, me están pidiendo estimación, divido el alfa por 2» cuando piden **un solo límite** (15/10).
- «uno de los grandes errores que cometen [en] los exámenes: tengo muestras iguales, entonces [no] son independientes. Nada que ver» (15/10).
- En la última clase de bondad de ajuste, calcular la puntual en lugar de la acumulada: «estos suelen equivocarse … siempre se equivocan» (22/10).
- En el tamaño de muestra de desvíos, usar R' en lugar de R = R'²: «Error común que cometieron muchos» (01/10).
- «Traten de no confundir los alfas con los betas. Y algunos confundieron» en la fórmula de n (08/10).

---

## 1. Resumen por clase

| Fecha | Temas (guía / apunte) | Ejercicios |
|---|---|---|
| **17/09** | Repaso de estimación de p (exacta con F; aproximaciones solo para n). Error muestral con p̂ = 0: tamaño **máximo** con p(1−p) = 0,25. **Ensayos de hipótesis de p** (apunte cap. 2): no hay bilateral; caso 1 H0 p ≤ p0 y caso 2 H0 p ≥ p0. Tres condiciones de rechazo: r ≥ rc (preferida, «a priori»), p̂ > p̂c y α* < α (p-value, «a posteriori»: «no me gusta»). β, n exacto (programa, Excel, nomograma binomial) y aproximaciones normal y Poisson. Léxico de recepción de partidas: AQL, riesgo del proveedor, RQL/LTPD, riesgo del comprador; MIL-STD «obsoleta». | **III-3** (a y b, con preguntas extra a' y b'), **III-11** |
| **24/09** | Demostración de su Excel y de su programa para el n exacto. Arranca cerca del n de la aproximación normal: «N 30 ya es normal … Mentira». Hay que justificar qué aproximación se usa. Anuncia comparación. | Ejemplo p0 = 0,05 / α = 0,01 / p1 = 0,06 / β = 0,05; **III-16** |
| **01/10** | **Devolución del 1° parcial.** Inicio de **comparación** (apunte cap. 3): diseño de experimentos y unidad experimental (no al azar). Parámetro de comparación ψ² = σ1²/σ2² con estimador J² = S1²/S2² y distribución F. Estimación y relación entre límites, n con n1 = n2, desvíos. **En comparaciones no hay hipótesis bilaterales.** | **III-19** (ruleta), **IV-1** |
| **08/10** | Ensayos de ψ² y φ (casos 1 y 2, β y n). **Medias**: cuadro de 4 métodos (σ conocidos; supuestos iguales → amalgamado; probados distintos → Welch; no independientes → apareadas). Amalgamado, Welch, **diferencias porcentuales (h)**. Recomienda Excel y programas propios. | **IV-4**; **V-8** (planteo y test F auxiliar) |
| **15/10** | Final de V-8 (a a d, incluida la inecuación en h). **Apareadas**: cómo reconocerlas (V-9, V-12 a V-21). Inicio de **χ²** (apunte cap. 4): contrastar contra un patrón; pruebas de consistencia, independencia y bondad de ajuste. | **V-8**, **V-12** |
| **22/10** | χ²: consistencia multinomial, independencia y bondad de ajuste a un modelo empírico, a la uniforme y a Poisson. Amalgamado de clases, clases efectivas, completar el dominio, ajuste «demasiado perfecto». | **VI-6**, **VI-7**, **VI-13**, **VI-10** (dado), **VI-16** |

---

## 2. Logística (más allá de §0)
- Horario 18:45 a 22:15 con un recreo. Asistencia del 75% con QR, Bluetooth y ubicación (06/08).
- Clase complementaria virtual (17/09, docente «Cáceres»): «suele usar la aproximación». O sea, **no seguir** lo que se haga ahí si contradice la regla del exacto.
- Las notas del 1° parcial ya están cargadas y mostró los exámenes en el recreo del 01/10. Hay una frase confusa, «30 en la otra semana. 15 días» (01/10); ver §6.

---

## 3. Reglas del profesor para resolver y redactar

### 3.1 Generales
- **Probabilidades nunca en %** (α, β, 1−β, P(...)). Una *proporción o fracción* estimada sí se puede informar en % si el enunciado pide «porcentaje» (17/09: «si me piden el porcentaje … 0,51%»).
- **Mínimo 4 decimales** en todo el cálculo (01/10). Ideal: todos los de la calculadora. Los periódicos se tratan como fracción (1/37; «0,4 periódico» en IV-1).
- Pasos en orden: «Recuerden siempre seguir los pasos ordenadamente». Hipótesis → α → n → crítico → CR → muestra → conclusión. Si α no se da, se elige y **se justifica** (§3.2).
- **Comparar el estimador contra el valor crítico.** Nunca usar estadísticos de prueba tipo «F observado» o «t observado» (08/10): «la empresa no entiende que vos le pongas … F observado … comparar el estimador con un valor crítico. Eso es lo más lógico». Tampoco comparar el crítico con μ0 o Δ0 (15/10: «nunca con la diferencia [hipotética] 0,45 … es un supuesto»).
- **El estimador tiene que ser coherente con el parámetro** (15/10). Si el parámetro es μCA − 1,10·μSA, el estimador es x̄CA − 1,10·x̄SA, no x̄CA − x̄SA.
- **Un solo límite ⇒ α sin dividir** (17/09 y 15/10): «El alfa se divide por dos cuando tengo dos límites, no cuando tengo un límite». Vale para «valor mínimo / máximo» y para p con r = 0.
- **Discretas: el α real nunca puede superar el estipulado** (17/09 y 01/10): entre los dos valores que da el aplicativo se elige el rc con G ≤ α. «Nunca el valor de alfa puede ser [mayor] al valor estipulado».
- **«Puntos» no es lo mismo que «%»** (24/09): «aumento de tres puntos» es 0,12 → 0,15; no es 0,12·1,03. «Ojo con esto que suelen equivocarse».
- No rechazar no prueba H0: «Jamás se puede probar la igualdad … supongo que son iguales porque no [rechacé]» (08/10). En independencia: «nunca puedo probar la independencia» (15/10).
- Conclusión al rechazar en consistencia: «hay alguna que es distinta», no «todas son distintas».
- Redondeos: «los [redondeos] en estadística son lógicos, no matemáticos» (08/10). Ejemplos: Welch se trunca (124,9 → 124); tamaños de muestra al entero que cumpla; rc según α.
- Recibe la regla de decisión en lenguaje de planta: «si en 1637 encuentro 229 o más interesados … inicio una nueva campaña» (24/09).

### 3.2 Planteo de H0/H1 y elección de α
- Siempre se lee **qué se quiere probar** y eso va en H1. Ruleta (III-19): parece bilateral, pero «lo que el juez pide es si la denuncia tiene fundamento … que el cero se daba con mayor frecuencia» ⇒ H0: p ≤ 1/37.
- **En p no hay bilateral** (17/09): «a nadie se le va a ocurrir [pedir] un porcentaje defectuoso exactamente igual a tanto».
- **Optimista**:
  - Control de proceso (III-11): «quiero que se cumpla ese 12%» ⇒ H0 p ≤ 0,12.
  - Recepción de partidas de un **proveedor habitual** (AQL = p0 con α como riesgo del proveedor; RQL = p1 con β como riesgo del comprador). Un proveedor nuevo «ya es otro concepto».
- **Pesimista**: campaña publicitaria (III-16), por dos motivos: «Una campaña publicitaria es muy cara» y «lo que yo quiero comprobar [es] si realmente la campaña fue efectiva». **Aunque sea barata, igual pesimista**: «siempre hay que ser pesimista, aunque me salga barato la campaña».
- **α no dado: «α estándar intermedio» con fundamento** (01/10, ruleta). Un α chico favorece al casino y uno grande al denunciante. El perito judicial debe ser imparcial ⇒ 0,05. Cita: «vamos a poner 0,05, no porque sea estándar, sino porque justamente tiene esto razón de ser. Tenemos que ser [imparciales]» y «Los alfas extremos no son imparciales. A veces conviene no ser imparcial».
- En χ², el apunte dice: «En general, salvo contadas excepciones, el … error de tipo I … es 0,05». En el dado (VI-10) tomó 0,05 sin más.
- **Comparaciones: siempre unilaterales y a posteriori.**
  - 01/10: «Las hipótesis bilaterales no existen en comparaciones … jamás me planteen una hipótesis bilateral en comparación … la IA les va a hacer todas las comparaciones bilaterales … todos los profesores particulares hacen comparaciones bilaterales».
  - La muestra orienta: si S2 > S1, lo único que se puede intentar probar es σ2 > σ1.
- **El planteo verbal se traduce a un parámetro de comparación.** «σCR ≥ 0,88·σSR» se convierte en H0 φ = σCR/σSR ≥ 0,88. Recomienda «pongan en letra» (A y B, CR y SR, CA y SA) en lugar de 1 y 2, y respetar la relación que pide el enunciado.

### 3.3 Inferencia sobre p (Tema III)
- **Estimación siempre exacta**, con el aplicativo binomial o con las fórmulas F. ν para A: (2n−2r+2; 2r); ν para B: (2r+2; 2n−2r). Prohibido usar normal o Poisson para estimar.
- **Tamaño de muestra**:
  1. Primero la aproximación normal: n = (z/e)²·p̂(1−p̂) + 1.
  2. **Verificar con el n RESULTANTE**: n·p ≥ 10 y n·(1−p) ≥ 10 («los dos valores son mayores que 10»). En el ensayo se verifica con p0.
  3. Si no se cumple, criterio de Mermoz para elegir entre normal y Poisson.
  4. «Siempre [el criterio] de aproximación se aplica al valor de n que vos calculaste, el n final … no con el inicial».
- Poisson solo sirve para la **relación entre límites**. Para el error muestral, la única fórmula es la normal.
- Si p̂ = 0, la fórmula del error da algo «ridículo». Alternativa: tamaño **máximo** con p(1−p) = 0,25.
- Ensayo:
  - rc: G_b(rc | n, p0) = α en el caso 1; F_b en el caso 2.
  - β = F_b(rc−1 | n, p1) en el caso 1; β = G_b(rc+1 | n, p1) en el caso 2.
  - n exacto resolviendo las dos ecuaciones a la vez (G ≤ α, F ≤ β, mínima diferencia).
  - Aproximación normal: n = [(z1−α·√(p0q0) + z1−β·√(p1q1)) / (p1−p0)]².
  - Aproximación Poisson con la ecuación de Wilson-Hilferty, R = p1/p0 y χ². Si los dos n difieren, «siempre se toma el mayor».
- Hay que **justificar** la aproximación elegida.

### 3.4 Comparación de dos poblaciones (Temas IV y V)
- **Varianzas**: ψ² = σ1²/σ2², estimador J² = S1²/S2², F con ν1 = n1−1 (**lo que está en el numerador**) y ν2 = n2−1. «Siempre piensen qué van a poner en el numerador».
  - Intervalo: A = J²/F(1−α/2; ν1, ν2) y B = J²/F(α/2; ν1, ν2).
  - Relación entre límites: R = B/A = F(1−α/2)/F(α/2).
  - **n solo con n1 = n2**. Es iterativo con t y n = ν+1.
  - Desvíos: A' = √A y B' = √B; para el tamaño de muestra usar R = R'².
  - **Interpretar como incremento o decremento porcentual.** Ejemplo: «la varianza A como mínimo … 79,65% menor … como máximo 11,37% mayor».
  - Si no especifican la relación, **se elige una, se dice cuál y se resuelve solo esa**: «Yo en la guía puse los dos resultados para no … que ustedes me hagan los dos».
- **Ensayos ψ²**:
  - Caso 1, H0 ψ² ≤ ψ0²: J²c = ψ0²·F(1−α; ν1, ν2) y se rechaza si J² > J²c. β = F_F(ψ0²/ψ1² · F(1−α)).
  - Caso 2, H0 ψ² ≥ ψ0²: J²c = ψ0²·F(α) y se rechaza si J² < J²c. β = 1 − F_F(ψ0²/ψ1² · F(α)).
  - Con desvíos, «el φ tiene que ir en los cuadrados»: Jc = √(φ0²·F).
  - n con n1 = n2: R = ψ1²/ψ0² en el caso 1 y R = ψ0²/ψ1² en el caso 2, «siempre … mayor que uno; si da menor, algo mal planteado».
- **Medias: elección del método.**
  1. σ1 y σ2 conocidos → Normal. Es solo teórico: «Jamás vas a conocer ambos». No existe el caso «uno conocido y otro no».
  2. Desconocidos → **test F auxiliar previo** («no es parte del problema»):
     - **unilateral, orientado por la evidencia**, con la varianza muestral mayor sospechada mayor;
     - **con α grande y no el del problema**: «En ninguna parte de los problemas te van a dar el riesgo para la comparación de varianzas … El alfa … siempre debe ser un alfa grande». En V-8 usó 0,10. Se toma grande porque, si no se rechaza, uno quiere poder suponerlas iguales;
     - si no se rechaza → **amalgamado**; si se rechaza → **Welch**;
     - si «por experiencia» se sabe con certeza, se puede omitir; si no, «hagan siempre el [ensayo]».
  3. **Apareadas** cuando hay **mismo individuo o misma unidad experimental**, no cuando los n son iguales. Estimador: d̄ (promedio de las diferencias por individuo, «consistente con el parámetro»), S_D y t con n−1.
- Amalgamado:
  - S²a = [(n1−1)S1² + (n2−1)S2²]/(n1+n2−2), con ν = n1+n2−2.
  - Control: «tiene que estar entre medio de esos dos».
  - Intervalo: D ± t(1−α/2)·Sa·√(1/n1+1/n2).
  - Ensayo caso 1: Dc = Δ0 + t(1−α)·Sa·√(1/n1+1/n2). Caso 2: Dc = Δ0 − ….
  - **No se calculan β ni n en ensayos de medias con t** («t no centrada … no lo vamos a generar para ustedes»).
- **Diferencias porcentuales**: parámetro Δ* = μ1 − h·μ2 (no el cociente, porque la «división de dos normales» no tiene distribución conocida).
  - Estimador D* = x̄1 − h·x̄2.
  - D*c = ± t·Sa·√(1/n1 + h²/n2). **h² afecta a la población que lleva h.**
- **Porcentaje mínimo**: h no se estima («es una constante … no un parámetro»). Se plantea la condición de rechazo como inecuación en h, se eleva al cuadrado y se resuelve la cuadrática. **Cada raíz se verifica en la inecuación original**, porque una puede no servir.
- Welch:
  - √(S1²/n1 + S2²/n2) y ν = (S1²/n1 + S2²/n2)² / [(S1²/n1)²/(n1−1) + (S2²/n2)²/(n2−1)].
  - **Se toma la parte entera** (124,9 → 124).
  - En comparaciones porcentuales, h² multiplica a S2²/n2 también dentro de ν.
  - El n es iterativo y en cada paso se recalcula ν.

### 3.5 χ² (Tema VI)
- Se **contrasta contra un patrón**. Las tres pruebas usan el mismo estadístico Σ(O−E)²/E y siempre la **cola derecha**: rechazo si χ²obs > χ²(1−α; ν).
- **Qué prueba usar** (22/10): «Siempre que se pida si hay asociación, eso es una prueba [de] independencia. Si se pide niveles, probabilidades, porcentajes, es una prueba de consistencia». La bondad de ajuste es «se ajusta / sigue un modelo».
- **H0 siempre la misma por tipo**:
  - Consistencia: igualdad de proporciones **escrita categoría por categoría**: p1ª,M = p1ª,T = p1ª,N, y lo mismo para 2ª y defectuosas. «No me pongan P mañana, P tarde, P noche porque no es correcto».
  - Independencia: **en palabras**, «las fallas por pintura son independientes del color».
  - Bondad: «lo observado se ajusta a [modelo]». Habla de «modelo», no de «ley».
- La tabla de observados es «la cruda realidad» y no se toca. Los esperados son esperanzas y **llevan decimales** («Jamás se [redondean a enteros]»). Las sumas de filas y columnas tienen que cerrar.
- Restricciones: **N total ≥ 60** y **todos los esperados ≥ 5**; los observados pueden ser 0 o 1. Si un esperado es < 5, se **amalgaman clases** con la de arriba o la de abajo, en general en los extremos pero también en el medio.
- Esperados:
  - Consistencia: p̂ global de cada categoría por el n de cada grupo.
  - Independencia: Eij = total de fila · total de columna / N.
  - Bondad: Ei = N·pi, con una columna de pi que sume 1.
- ν:
  - Tablas: (f−1)(c−1). Lo explica como «valores libres».
  - Bondad: **clases efectivas** (las que quedaron después de amalgamar o agregar) − 1 − p, donde p son los parámetros estimados con la muestra (Poisson con x̄ ⇒ p = 1; uniforme o patrón histórico ⇒ p = 0).
- **Completar el dominio del modelo**: se agrega una clase al final (y/o al principio) con frecuencia observada 0. Su probabilidad es la **acumulada** (G(11) = P(R ≥ 11)), no la puntual: «estos suelen equivocarse … siempre se equivocan». El apunte hace lo mismo en continuas, con F_N en la primera clase y G_N en la última.
- **Ajuste demasiado perfecto** («no está [en] ningún libro»): si χ²obs < χ²(α; ν) (cola izquierda), se sospecha de los **datos** (cocinados), no del modelo. Ejemplo: 11/9/11/9… da χ² = 0,6 < χ²(0,05; 5) = 1,1455.
- **Variables discretas, tres situaciones**:
  - Si se rechaza, no sigue el modelo.
  - Si se cumple el proceso físico (por ejemplo, acontecimientos puntuales en un medio continuo para Poisson) y no se rechaza, «sí puedo afirmar que sigue el modelo».
  - Si no se cumple el proceso y no se rechaza, «el modelo es un buen candidato».
- Después de rechazar en consistencia, para saber cuál difiere hay que comparar de a pares. Lo anunció pero todavía no lo explicó.
- Weibull (anécdota): «Weibull para viento es un modelo incorrecto». Para velocidad corresponde Rayleigh. Hay una tabla de ajuste por momentos de Weibull (w, d = s/m, m/b) en las fuentes, que sirve para la bondad de ajuste continua.

### 3.6 Regresión
- **Todavía no se dio** (al 22/10). No hay reglas del profesor. El 06/08 dijo que «al final de la materia hay temas que se resuelven sí o sí con Excel», presumiblemente regresión.

### 3.7 Software
- Usa el aplicativo de distribuciones (Matthew Bognar, offline). Para discretas, cargar primero los parámetros (n, p), después la probabilidad y el tipo (≥ o ≤); el aplicativo devuelve **dos** valores y se elige con criterio.
- Usa su calculadora programable, su Excel con vector para el n exacto de p y su programa. **No los comparte**: «Hacéptelo vos».
- Recomienda Excel con Solver o Buscar objetivo para las ecuaciones iterativas. La iteración converge «en no más de tres pasos» y el arranque es libre.

---

## 4. Ejercicios resueltos en clase (casos de prueba)

Todos los valores están verificados con scipy. Si el ASR o el profesor daba otro dígito, lo indico.

**III-3** (17/09). «Calcular los límites de confianza del 90% de la fracción defectuosa, si de un proceso productivo se tomó una muestra de 10 unidades en la cual se encontró: a) 1 defectuosa; b) 0 defectuosas».
- a) p̂ = 0,10.
  - A = 1/[1 + (n−r+1)/r·F(0,95; 20; 2)], con F = 19,4458 ⇒ **A = 0,0051**.
  - B con F(0,95; 4; 18) = 2,9277 ⇒ **B = 0,3942**.
  - Error muestral (B−A)/2 = **0,1945**.
- Pregunta extra a': ¿cuántas unidades más para reducir el error un 80%?
  - e' = 0,1945·0,2 = 0,03891.
  - n = (1,6449/0,03891)²·0,1·0,9 + 1 = **162**, o sea **152 más**.
  - Verificación: 162·0,1 = 16,2 y 162·0,9 = 145,8, ambos > 10 ⇒ la normal es válida.
- b) r = 0 ⇒ A = 0 y **B = 1/[1 + 10/F(0,90; 2; 20)] = 0,2057** (α **sin dividir**, F = 2,5893).
  - **La guía dice 0,2589 (con α/2): «lo hicieron con alfa sobre 2 y está mal».**
  - Coincide con III-20 de la propia guía (LTPD = 0,2057).
- Pregunta extra b': reducir un 80% el error 0,10285 ⇒ e = 0,02057. La fórmula con p̂ = 0 da n ≈ 1 («ridículo»). El máximo con 0,25 es **≈ 1600** (con z = 1,6449 da 1600 en el redondeo del profesor).

**III-11** (17/09). Proceso con 12% de defectuosas, muestras de 50, P(detener | bajo control) = **0,05** (el ASR dice «0,06»; la guía dice 0,05). Criterio optimista: H0 p ≤ 0,12.
- a) G_b(10 | 50; 0,12) = 0,0708 > 0,05 y G_b(11) = 0,0325 ⇒ **rc = 11** (CR: r ≥ 11).
- b) p1 = 0,14: **β = F_b(10 | 50; 0,14) = 0,9176**.
- c) β = 0,50 en p1 = 0,14, sin tocar α:
  - **exacto n = 755, rc = 106**;
  - normal: n = [1,6449·√(0,12·0,88) + 0·…]/0,02 al cuadrado = 714,26 ⇒ **715**; verificación 85,8 y 629,2 > 10.
  - **Poisson (n = 855) es incorrecto**: se aplicó el criterio con n = 50 en lugar del n resultante.

**Ejemplo de software** (24/09). H0 p ≤ 0,05, α = 0,01, p1 = 0,06, β = 0,05. Normal **n ≈ 8058**; exacto **n = 8142, rc = 454** (α real 0,0100, β real 0,0499).

**III-16** (24/09). Jabón con penetración del 12%, campaña. Criterio pesimista: H0 p ≤ 0,12, α = 0,01; «aumento de 3 puntos» ⇒ p1 = 0,15 con β = 0,10.
- a) **Exacto n = 1675, rc = 233** (el ASR dice «223»; la guía y scipy dan 233).
- Normal: z(0,99) = 2,3263 y z(0,90) = 1,2816 ⇒ n = 1636,4 ⇒ **1637**; verificación 1637·0,12 = 196,44 > 10.
- Con n = 1637: G(228) = 0,0101 > 0,01 y G(229) = 0,0083 ⇒ **rc = 229**.
- RD: «si en 1637 encuentro 229 o más interesados … inicio una nueva campaña».
- b) p = 0,14 («dos puntos»): β = F_b(228 | 1637; 0,14) = **0,4841** ⇒ **1−β = 0,5159**. Con el plan exacto (1675; 233): β = 0,4473.
- c) n para que 1−β = 0,90 en p = 0,14: quedó planteado y no se resolvió.

**III-19, ruleta** (01/10). 1000 bolas, 42 ceros.
- H0 p ≤ 1/37 (por lo que dice la denuncia). α no dado ⇒ **0,05 justificado por la imparcialidad del perito**.
- G(36 | 1000; 1/37) = 0,05401 y G(37) = 0,03717 ⇒ **rc = 37**.
- r = 42 ≥ 37 ⇒ se rechaza: «la denuncia tiene fundamento estadístico».
- b) p = 0,05: β = F_b(36 | 1000; 0,05) ⇒ **1−β = 0,9788**. El ASR dice «0 97 81» y la guía 0,9789.

**IV-1, tornos** (01/10). nA = 13 con sA = 3,6 y nB = 25 con sB = 5,4 (décimas de mm). Se elige estudiar A/B.
- a) Intervalo 90%:
  - J² = 0,4 periódico; F(0,95; 12; 24) = 2,1834 y F(0,05; 12; 24) = 0,3991.
  - **A = 0,2036** (el profesor dijo 0,2035) y **B = 1,1135** (dijo 1,1137).
  - R = B/A = **5,470** (dijo 5,4708).
  - Interpretación: «σA² como mínimo 79,65% menor y como máximo 11,37% mayor que σB²».
  - Con la relación B/A los límites serían 0,898 y 4,92.
- b) n iguales para R/2 = 2,7354: iterando ⇒ **ν = 44 ⇒ n = 45 por torno** (32 más en A y 20 más en B). Da lo mismo con la otra relación.
- c) Desvíos: J = 0,6 periódico, **A' = 0,4512** (dijo 0,4511), **B' = 1,0552**, R' = 2,339.
- d) R'/2 = 1,1695 ⇒ R = 1,3677 ⇒ **ν = 443 ⇒ n = 444** (431 más en A y 419 más en B).
- Para el solver: los ν 44 y 443 coinciden exactamente con la búsqueda exacta de F(0,95; ν; ν)/F(0,05; ν; ν) ≤ R.

**IV-4, hiladoras** (08/10). Reacondicionadas (CR): n = 4, x̄ = 1470 m, s = 132. Sin reacondicionar (SR): n = 16, x̄ = 1208, s = 354.
- H0 φ = σCR/σSR ≥ 0,88 contra H1 < 0,88, con α = 0,10, ν1 = 3 y ν2 = 15.
- a) F(0,10; 3; 15) = 0,1923; **Jc = √(0,88²·0,1923) = 0,3859**; J = 132/354 = **0,3729** < Jc ⇒ se rechaza: conviene reacondicionar.
- b) φ1 = 0,7: argumento 0,88²/0,7²·0,1923 = 0,3039; F_F = 0,1779 ⇒ **β = 0,8221** y **1−β = 0,1779**.
- c) 1−β = 0,90: R = (0,88/0,7)² = 1,5804. Iterando: t(0,90; 100) = 1,2902 → 127; t(0,90; 127) = 1,2883 → 127. **ν = 127 ⇒ n = 128 por tipo** (124 más CR y 112 más SR).
  - scipy: el criterio R ≥ F(0,9; ν; ν)² da exactamente ν = 127.

**V-8, látex** (08/10 y 15/10). Con aditivo: n = 21, x̄ = 8,5 kg, s = 1,2. Sin aditivo: n = 61, x̄ = 7,6, s = 1,25.
- **Test F auxiliar**: sospecha σSA > σCA ⇒ H0 σSA/σCA ≤ 1, α = 0,10. Jc = √F(0,90; 60; 20) = √1,6768 = **1,2949**; J = 1,25/1,2 = **1,0417** ⇒ no se rechaza ⇒ amalgamado.
- **Sa = 1,2377 kg** con ν = 80 y t(0,95; 80) = 1,6641.
- a) H0 μCA − μSA ≤ 0,45: **Dc = 0,9711**; D = 0,9 ⇒ no se rechaza.
- b) Diferencia **mínima** al 95%: un solo límite con t(0,95). **A = 0,9 − 1,6641·1,2377·√(1/21+1/61) = 0,3788 kg**. Coherente con a): el mínimo 0,3788 < 0,45.
- c) H0 μCA ≤ 1,10·μSA: **D*c = 0,5349**; D* = 8,5 − 1,1·7,6 = **0,14** ⇒ no se rechaza.
- d) Inecuación 8,5 − 7,6h > 1,6641·1,2377·√(1/21 + h²/61):
  - raíces **1,0490** y **1,1906**;
  - h = 1,1906 da el lado izquierdo negativo (−0,548) ⇒ no es solución;
  - **h = 1,0490 ⇒ incremento mínimo 4,90%** (coincide con la guía).

**V-12, trigo** (15/10). 8 fincas.
- A: 86, 87, 56, 93, 84, 93, 75, 79. B: 80, 79, 58, 91, 77, 82, 74, 66. Apareadas (la unidad experimental es la parcela).
- d = 6, 8, −2, 2, 7, 11, 1, 13 ⇒ **d̄ = 5,75** y **S_D = 5,12**.
- a) H0 Δ ≤ 2, α = 0,05, t(0,95; 7) = 1,8946 ⇒ **D̄c = 5,4295**; 5,75 > 5,4295 ⇒ se rechaza.
- b) IC 90% para A−B: **2,32 ≤ Δ ≤ 9,18** quintales por parcela.

**VI-6, tres turnos** (22/10). Mañana: 450 / 45 / 5 (n = 500). Tarde: 680 / 80 / 40 (n = 800). Noche: 320 / 40 / 40 (n = 400). α = 0,01.
- p̂ globales: 0,8529, 0,0971 y 0,05.
- Esperados:
  - 1ª: 426,47 / 682,35 / 341,18;
  - 2ª: 48,53 / 77,65 / 38,82;
  - defectuosas: 25 / 40 / 20.
- **χ² = 38,98** contra χ²(0,99; 4) = **13,2767** ⇒ se rechaza: «algún nivel de calidad es diferente».

**VI-7, color de autos** (22/10). Producción 550 / 450 / 480 / 320 (blanco, azul, rojo, verde); 300 reclamos (30%, 30%, 25%, 15%). α = 0,05.
- Observados con falla: 90 / 90 / 75 / 45. Sin falla: 460 / 360 / 405 / 275.
- Esperados con falla: 91,67 / 75 / 80 / 53,33. Sin falla: 458,33 / 375 / 400 / 266,67.
- **χ² = 5,5739** (dijo 5,5735), con ν = 3 y χ²c = 7,8147 ⇒ no se rechaza.

**VI-13, televisores** (22/10). Patrón 40/40/20; muestra 85/65/50 de 200; esperados 80/80/40.
- **χ² = 5,625** con ν = 2 y χ²c = 5,9915 ⇒ no se rechaza (el patrón histórico se mantiene).

**VI-10, dado** (22/10). 60 tiradas: 14, 6, 6, 13, 16, 5. Modelo uniforme con E = 10.
- **χ² = 11,8** con ν = 5 y χ²(0,95; 5) = **11,0705** ⇒ se rechaza (dado cargado).
- Cota inferior para «demasiado perfecto»: χ²(0,05; 5) = 1,1455.

**VI-16, levantacristales con Poisson** (22/10). 684 días; r = 0 a 10 con frecuencias 26, 62, 120, 145, 131, 101, 61, 27, 9, 1, 1.
- **m̂ = 3,5263**. Se agrega la clase «11 o más» con frecuencia 0 y probabilidad G(11) = 0,0011.
- Probabilidades: 0,0294 / 0,1037 / 0,1829 / 0,2150 / 0,1895 / 0,1336 / 0,0785 / 0,0396 / 0,0174 / 0,0068 / 0,0024 / 0,0011.
- Esperados: 20,12 / 70,94 / 125,09 / 147,03 / 129,62 / 91,42 / 53,73 / 27,07 / 11,93 / 4,67 / 1,65 / 0,74.
- Se amalgaman 9, 10 y ≥ 11: O = 2 y E = 7,06.
- **χ² = 9,4346**. Al principio dijo «14,5073» y se corrigió: «esto no me da y me da 9,4346».
- 10 clases efectivas ⇒ ν = 8 y χ²c = 15,5073 ⇒ no se rechaza. Como el proceso es Poisson, se puede afirmar que sigue el modelo.

---

## 5. Contraste con los .md del repo

Severidad: **A** = cambia el resultado o la nota; **M** = media; **B** = baja.

| # | Documento | Qué dice el repo | Qué dice el profesor | Sev. |
|---|---|---|---|---|
| 1 | CONVENCIONES («IC de p con r = 0») | La app **sigue a la guía con α/2** (III-3b = 0,2589) | α sin dividir ⇒ **0,2057**; «está mal» en la guía (17/09) | **A** |
| 2 | CONVENCIONES («Plan de muestreo por Poisson», evidencia III-11c = 855) | Toma 855 por Poisson como convención | 855 por Poisson es **incorrecto** (el criterio se aplicó con n inicial). Respuestas válidas: exacto **755** o normal 715. La propia guía lo aclara | **A** |
| 3 | esquema §1.3 y Resolución «Conejos» 1c | Estimación de p por **aproximación normal** (n·p̂ ≥ 5), con √(p̂q̂/(n−1)) | **Prohibido**: siempre exacta. Fue el error nº 4 del 1° parcial. El umbral para n es **≥ 10** y se verifica con el n resultante | **A** |
| 4 | esquema §3.1 («obligatorio ensayar igualdad de varianzas», H0 φ² = 1 bilateral, varianza mayor en el numerador, F(1−α/2)) | Test F **bilateral** con el α del problema | En comparaciones **no hay bilaterales**. El test auxiliar es **unilateral orientado por la evidencia**, con **α grande (0,10)** que no es el del problema, y no es parte del problema | **A** |
| 5 | esquema §2.1 (optimista ⇒ H0 μ = μ0) y §2.2 caso III bilateral; Conejos 1a (H0 μ = 4,2) | El optimista lleva a bilateral | En p **no existe bilateral**; en comparaciones tampoco. El optimista se escribe con desigualdad (p ≤ p0). Para μ, H0 «μ = 4,2 contra μ > 4,2» no es lo que hace en clase (escribe H0 con ≤ o ≥) | **A** (p y comparaciones) / M (μ) |
| 6 | Conejos (b: «14%», a: «64,7%»); Gemini («0,6388 (63,88%)»); ESTILO ej. 3 «0,0051 (0,51%)» | Probabilidades en % | **Error conceptual** (error nº 1 del 1° parcial). Una proporción estimada se puede mostrar en % solo si piden «porcentaje»; α, β y 1−β **nunca** | **A** |
| 7 | CONVENCIONES («Decimales: medias 2, σ 2, …»); Conejos (3 decimales); ESTILO ej. 1 (e = 7,81) | Mostrar 2 o 3 decimales | «**mínimo cuatro decimales**» en el desarrollo; periódicos como fracción. Mostrar el final redondeado es tolerable, pero el desarrollo tiene que ir con ≥ 4 | **A** |
| 8 | esquema §2.4, Guía Definitiva paso 3, Conejos (t = 2,509 contra 2,539; χ² = 9,745) | Estadístico de prueba Z, t, χ² o F observado contra tabla | **No usar F u otros estadísticos observados**: comparar el **estimador** contra el **valor crítico** en unidades de la variable (08/10) | **A** (estilo exigido) |
| 9 | Gemini «Guía con Scripts» (y en parte esquema §0 y Guía Definitiva paso 3) | «Como no conoces σ, jamás debes usar la Normal»; «Usar Z con S es un error de concepto» | La regla está bien, pero **el fundamento del repo y de Gemini es el que el profesor marcó como error**. Hay que justificar por la estructura (normal dividida por un parámetro, o por la raíz de una gamma) | **A** (en redacción) |
| 10 | ESTILO §6 (V a VIII «provisoria») | Solo indica «test F con su conclusión». No hay ejemplos | Faltan todos los ejemplos del profesor: IV-1, IV-4, V-8 (a a d), V-12, VI-6, VI-7, VI-10, VI-13, VI-16 (§4). Hay que reemplazar la sección provisoria | **A** |
| 11 | ESTILO y esquema | No mencionan **diferencias porcentuales** (Δ* = μ1 − hμ2, h² en el término de n2) ni el **h mínimo por inecuación** con verificación de raíces | Se dio y lo pregunta la guía (V-8c y d) | **A** |
| 12 | ESTILO y esquema | Un solo límite («mínimo» o «máximo») no está contemplado | **α sin dividir** (error frecuente anunciado) | **A** |
| 13 | esquema y ESTILO | Apareadas: solo «definir D». No hay criterio para reconocerlas | Mismo individuo o unidad experimental, **no n iguales**. La guía las clasifica (§3.4) | M |
| 14 | ESTILO 6.4 (postes) | Lo llama «homogeneidad», con H1 p_A ≠ p_B, y concluye «el método A es mejor que el B» | Es **consistencia**: H0 escrita por categoría. Al rechazar: «alguna es distinta»; decir cuál requiere comparar de a pares (todavía no explicado). Afirmar «A es mejor» no está respaldado | M |
| 15 | ESTILO 6.2 («H0 siempre sin cambios; no justifiques criterio») | — | Coincide. Agregar: consistencia **por categoría** («no pongan P mañana, P tarde…»), independencia **en palabras**, y la regla de lectura «asociación ⇒ independencia; niveles o porcentajes ⇒ consistencia» | M |
| 16 | esquema §4 | Agrupar si Fe < 5 y ν = k − 1 − p | Coincide. **Falta**: completar el dominio con clases al principio o al final con F o G acumuladas (no la puntual); esperados con decimales; sumas que cierren; **ajuste demasiado perfecto** (cola izquierda); **3 situaciones de las discretas**; «clases efectivas» | M |
| 17 | esquema §3.2 caso B (Welch, ⌊ν⌋) | Truncar | Coincide («se toma la parte entera») | — |
| 18 | esquema §3.2 caso A | No dice que **no hay β ni n** en ensayos de medias | Correcto omitirlo, pero conviene que el solver **no ofrezca** β ni n para medias con t | B |
| 19 | esquema §3.1 (n para φ: «menor n con φ0²/φ1² ≥ F·F, se itera sobre F») | — | El profesor usa la fórmula iterativa con t del apunte, pero sus resultados (IV-1: 44 y 443; IV-4c: 127) coinciden con la búsqueda exacta en F. **Sin conflicto numérico**; mostrar la iteración con t si se puede | B |
| 20 | CONVENCIONES («Hipótesis a la luz de los datos: unilateral hacia donde apunta la muestra») | — | **Correcto en comparaciones** (01/10). En una población (ruleta) la dirección sale **del enunciado o de la denuncia**, no de la muestra. Acotar la regla | M |
| 21 | esquema y Guía Definitiva (criterios) | «pesimista = inversión», «optimista = control o recepción» | Coincide. Agregar matices: recepción de un **proveedor habitual** (un proveedor nuevo es otro caso); **pesimista aunque sea barato** cuando se quiere probar efectividad; α «estándar intermedio» **justificado** (imparcialidad) cuando no lo dan | M |
| 22 | Guía Definitiva §4 («n ≥ 30 ⇒ Normal»; finitud si n/N > 0,20 con (N−n)/(N−1)) | — | «N 30 ya es normal … **Mentira**» (24/09, binomial). La finitud corresponde al 1° parcial; CONVENCIONES usa √((N−n)/N) y se contradice con el esquema | M (contradicción interna) |
| 23 | Conejos 2d («n' = 28 conservador, sin iterar») | No itera | Hay que **iterar**; la iteración da 27 según la propia nota. Pedido explícito del método iterativo | M |
| 24 | ESTILO §1.1 (n al entero superior) / CONVENCIONES (redondeos «hacia afuera») | — | Compatible («redondeos lógicos»). En p **discreta** la elección de rc no es «al superior», sino la que cumple α ≤ estipulado (y β ≤ estipulado en el plan) | B |
| 25 | Gemini «Metodología» y «Asistente» (H0 siempre pesimista; «igualdad en H0») | — | La igualdad va en H0: coincide. Pero **no siempre pesimista** (III-11 optimista; ruleta según la denuncia) | M |
| 26 | Repo en general | Numeración de temas I a VIII | Coincide con la guía. En clase el profesor cita «problema N de la página P». El solver debería aceptar las dos formas | B |
| 27 | ESTILO ej. 4 compara j² contra j²c (0,1390 contra 0,1489) | — | En clase comparó J contra Jc (0,3729 contra 0,3859). Es equivalente, pero conviene mostrar la forma del profesor cuando el parámetro es φ (desvíos) | B |

Afirmaciones del repo **sin respaldo** en las clases (ni a favor ni en contra):
- La «Guía Definitiva» dice que la omisión de un paso es «reprobación inmediata del ítem» y pide determinar el «tipo de muestreo».
- ESTILO pide cerrar los intervalos con «P(A ≤ θ ≤ B) = 1 − α». El profesor dijo «lo afirmo con un 90% de seguridad o con una probabilidad de 0,9»; no lo contradice.
- ESTILO pide «conclusión que empieza por el nivel de significación»: no lo exigió en voz alta.

---

## 6. Dudas y ambigüedades
- **Fecha y temario exactos del 2° parcial**: no están en el audio. Revisar el campus o la diapositiva del 06/08. Tampoco está claro si entra regresión ni bondad de ajuste continua.
- 01/10, recreo: «30 en la otra semana. 15 días 15 días». Podría ser la fecha de revisión, el recuperatorio o el plazo para algo. Ininteligible.
- 01/10, recreo: un comentario a un alumno sobre «optimista … implementar un proceso que no produce ningún efecto … alfa 0,05». Parece la corrección de un problema del parcial, pero no se reconstruye.
- **Fórmula de n para relación de varianzas y desvíos** (ν iterativo con t): el texto del apunte está mutilado y lo que se oye no reproduce sus resultados. Sus números sí coinciden con la búsqueda exacta en F. Conviene confirmar la fórmula en el PDF original (apunte cap. 3, págs. ≈ 55-57).
- Umbral de la aproximación normal en p: dijo «mayores que 10» (n·p y n·q); el repo usa 5. Para Poisson dijo «p̂ menor a 0,005» (posible error del ASR: el apunte suele usar p ≤ 0,05 o 0,1). Verificar en el apunte cap. 1.
- α del test F auxiliar: dijo «como mínimo de …» (cortado) y usó 0,10. No queda claro si acepta valores mayores (0,20, 0,25).
- III-11: el ASR dice «0,06» en el enunciado, pero el cálculo y la guía usan 0,05.
- III-16: el ASR dice «R crítico 223»; la guía y scipy dan 233.
- III-19 b: el ASR dice «0,9781»; la guía da 0,9789 y scipy 0,9788.
- VI-16: primero dijo 14,5073 y después lo corrigió a 9,4346.
- VI-7: «no puedo asegurar que el color influya … se puede considerar que los sucesos son independientes», pero antes había dicho «nunca puedo probar la independencia». Conviene redactar «no hay evidencia de asociación».
- No explicó todavía cómo identificar qué grupo difiere después de rechazar consistencia (comparaciones de a pares).
