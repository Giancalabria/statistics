import streamlit as st

from solver import intervals, muestra, wording


def parse_numbers(texto: str):
    import re
    nums = re.split(r"[,\s]+", texto.strip())
    return [float(n) for n in nums if n]


def input_resumen_muestra(key_prefix: str, pedir_s: bool = True):
    """Deja elegir entre ingresar (n, x̄, S) a mano o pegar los datos crudos.

    Devuelve (n, xbar, s). Si pedir_s=False, s puede ser None (para el caso de
    media con sigma poblacional conocido, donde S no hace falta).
    """
    modo = st.radio(
        "¿Cómo ingresás los datos de la muestra?",
        ["Resumen (n, x̄, S)", "Datos crudos (lista)"],
        key=f"{key_prefix}_modo",
        horizontal=True,
    )
    if modo == "Datos crudos (lista)":
        texto = st.text_area(
            "Datos de la muestra (separados por comas o espacios)",
            value="", key=f"{key_prefix}_datos",
        )
        datos = parse_numbers(texto) if texto.strip() else []
        if len(datos) < 2:
            st.info("Ingresá al menos 2 datos para calcular n, x̄ y S.")
            return None, None, None
        resumen = muestra.resumen_muestra(datos)
        st.success(f"n = {resumen.n}, x̄ = {resumen.xbar:.4f}, S = {resumen.s:.4f}")
        return resumen.n, resumen.xbar, resumen.s
    else:
        xbar = st.number_input("Media muestral (x̄)", value=0.0, key=f"{key_prefix}_xbar")
        n = st.number_input("Tamaño de muestra (n)", min_value=2, step=1, value=30, key=f"{key_prefix}_n")
        s = None
        if pedir_s:
            s = st.number_input("Desvío muestral (S)", min_value=1e-9, value=1.0, key=f"{key_prefix}_s")
        return int(n), xbar, s

st.title("Intervalos de Confianza")

parametro = st.selectbox(
    "¿Qué parámetro querés estimar?", ["Media", "Varianza / Desvío", "Proporción"]
)
objetivo = st.radio("¿Qué querés calcular?", ["Intervalo de Confianza", "Tamaño de muestra (n)"])

confianza = st.number_input(
    "Nivel de confianza (1 - α)", min_value=0.5, max_value=0.999, value=0.95, step=0.01, format="%.5f"
)
alpha = 1 - confianza

poblacion_finita = st.checkbox("¿Población finita (N conocido)?")
N = None
if poblacion_finita:
    N = st.number_input("Tamaño de la población (N)", min_value=2, step=1, value=1000)


def mostrar_intervalo(nombre_parametro: str, result: intervals.IntervalResult) -> None:
    for w in result.warnings:
        st.warning(w)
    st.latex(f"{result.a:.5f} \\le {nombre_parametro} \\le {result.b:.5f}")
    st.write(wording.texto_intervalo(nombre_parametro, result, confianza))
    with st.expander("Detalle del cálculo"):
        st.write(f"Distribución utilizada: {result.distribution}")
        if result.df is not None:
            st.write(f"Grados de libertad: {result.df}")
        if result.critical_value is not None:
            st.write(f"Valor crítico: {wording.fmt_num(result.critical_value)}")
        if result.error is not None:
            st.write(f"Error muestral (e): {result.error:.5f}")
        if result.finite_population:
            st.write("Se aplicó factor de corrección por finitud.")


def mostrar_n(n_result: intervals.SampleSizeResult, n_preliminar: int = 0) -> None:
    for w in n_result.warnings:
        st.warning(w)
    st.success(wording.texto_tamano_muestra(n_result, n_preliminar=n_preliminar or None))
    if n_result.reduccion is not None:
        with st.expander("Detalle del cálculo (reducción del error)"):
            st.write(f"Error actual: e = {n_result.e_actual:.5f}")
            st.write(f"Reducción pedida: {n_result.reduccion * 100:g}%")
            st.write(
                f"Error nuevo: e = {n_result.e_actual:.5f} × "
                f"(1 - {n_result.reduccion:.2f}) = **{n_result.e_nuevo:.5f}**"
            )


def mostrar_n_varianza(result: intervals.VarianceSampleSizeResult, n_preliminar: int = 0) -> None:
    for w in result.warnings:
        st.warning(w)
    st.success(wording.texto_tamano_muestra_varianza(result, n_preliminar=n_preliminar or None))
    with st.expander("Detalle del cálculo (Ecuación de García)"):
        if result.r_sigma_actual is not None:
            st.write(f"Relación actual entre límites: R' = {result.r_sigma_actual:.5f}")
        if result.reduccion is not None:
            st.write(f"Reducción pedida: {result.reduccion * 100:g}%")
        st.write(f"Relación objetivo del desvío: R' = {result.r_sigma_objetivo:.5f}")
        st.write(f"Relación objetivo de varianzas: R = (R')² = {result.r_var_objetivo:.5f}")
        st.latex(
            r"a = \frac{Z_{(1-\alpha/2)}\,\left(\sqrt[3]{R}+1\right)}"
            r"{2\left(\sqrt[3]{R}-1\right)}"
            r"\qquad \nu = \frac{2}{9}\left(a+\sqrt{a^2+1}\right)^2"
        )
        st.write(f"∛R = {result.r_var_objetivo ** (1 / 3):.5f}")
        st.write(f"Variable auxiliar de García: a = {result.a:.5f}")
        st.write(f"Grados de libertad: ν = {result.nu:.5f}  →  n = ν + 1 = {result.nu + 1:.5f}")
        st.write(f"Redondeo hacia arriba: **n = {result.n}**")
        if result.n_exacto is not None:
            st.write(
                f"Control por búsqueda exacta sobre χ²: n = {result.n_exacto} "
                f"(da R' = {result.r_sigma_logrado:.5f})"
            )


if parametro == "Media":
    sigma_conocido = st.radio("¿Se conoce el desvío poblacional σ?", ["Sí", "No"]) == "Sí"

    if objetivo == "Intervalo de Confianza":
        n, xbar, s = input_resumen_muestra("media_ic", pedir_s=not sigma_conocido)
        if sigma_conocido:
            sigma = st.number_input("Desvío poblacional (σ)", min_value=1e-9, value=1.0, format="%.5f")

        calcular_total = False
        if poblacion_finita and N is not None:
            calcular_total = st.checkbox("¿Calcular también el Total Poblacional (T = N·μ)?")

        if st.button("Calcular") and n is not None:
            try:
                if sigma_conocido:
                    result = intervals.ic_media_sigma_conocido(xbar, sigma, n, alpha, N=N)
                else:
                    result = intervals.ic_media_sigma_desconocido(xbar, s, n, alpha, N=N)
                mostrar_intervalo("\\mu", result)

                if calcular_total:
                    st.subheader("Total Poblacional (T = N·μ)")
                    total_result = intervals.ic_total_poblacional(result, N)
                    mostrar_intervalo("T", total_result)
            except ValueError as e:
                st.error(f"Error: {e}")

    else:
        modo_precision = st.radio(
            "¿Cómo definís la precisión buscada?",
            ["Error muestral directo (e)", "Reducir un % el error actual"],
            key="media_n_modo",
        )

        e = None
        e_actual = None
        reduccion = None
        if modo_precision.startswith("Error muestral directo"):
            e = st.number_input("Error muestral admitido (e)", min_value=1e-9, value=1.0, format="%.5f")
        else:
            e_actual = st.number_input(
                "Error actual (e) del IC ya calculado", min_value=1e-9, value=1.0, format="%.5f"
            )
            reduccion_pct = st.number_input(
                "Reducción deseada del error (%)",
                min_value=0.1, max_value=99.9, value=30.0, step=1.0, format="%.2f",
            )
            reduccion = reduccion_pct / 100

        if sigma_conocido:
            sigma = st.number_input("Desvío poblacional (σ)", min_value=1e-9, value=1.0, format="%.5f")
        else:
            s = st.number_input("Desvío muestral (S)", min_value=1e-9, value=1.0, format="%.5f")
        n_preliminar = st.number_input(
            "Tamaño de muestra ya relevado (n preliminar, opcional)",
            min_value=0, step=1, value=0,
            help="Si ya mediste algunas unidades y querés saber cuántas más faltan (Δn).",
        )

        if st.button("Calcular"):
            try:
                if reduccion is not None:
                    if sigma_conocido:
                        n_result = intervals.n_media_sigma_conocido_por_reduccion(
                            sigma, e_actual, reduccion, alpha, N=N
                        )
                    else:
                        n_result = intervals.n_media_sigma_desconocido_por_reduccion(
                            s, e_actual, reduccion, alpha, N=N
                        )
                else:
                    if sigma_conocido:
                        n_result = intervals.n_media_sigma_conocido(sigma, e, alpha, N=N)
                    else:
                        n_result = intervals.n_media_sigma_desconocido(s, e, alpha, N=N)
                mostrar_n(n_result, n_preliminar=int(n_preliminar))
            except ValueError as e:
                st.error(f"Error: {e}")

elif parametro == "Varianza / Desvío":
    if objetivo == "Tamaño de muestra (n)":
        st.info(
            "En χ² el intervalo es asimétrico, así que la precisión no se mide con un "
            "error ±e sino con la **relación entre límites** R' = B'/A' del IC del "
            "desvío. Se calcula con la **Ecuación de García** (inversión de "
            "Wilson–Hilferty), que evita tantear la tabla de χ²."
        )

        modo_relacion = st.radio(
            "¿Cómo definís la precisión buscada?",
            [
                "Reducir un % la relación actual entre límites",
                "Relación objetivo R' = B'/A' directa",
            ],
            key="var_n_modo",
        )

        r_actual = None
        reduccion = None
        r_objetivo = None

        if modo_relacion.startswith("Reducir"):
            fuente = st.radio(
                "Relación actual (R')",
                ["Ingresar los límites A' y B' del IC previo", "Ingresar R' directamente"],
                key="var_n_fuente",
                horizontal=True,
            )
            if fuente.startswith("Ingresar los límites"):
                col_a, col_b = st.columns(2)
                with col_a:
                    a_prev = st.number_input(
                        "Límite inferior del desvío (A')", min_value=1e-9, value=159.70, format="%.5f"
                    )
                with col_b:
                    b_prev = st.number_input(
                        "Límite superior del desvío (B')", min_value=1e-9, value=306.73, format="%.5f"
                    )
                try:
                    r_actual = intervals.relacion_limites(a_prev, b_prev)
                    st.write(f"Relación actual: R' = {b_prev:g} / {a_prev:g} = **{r_actual:.5f}**")
                except ValueError as e:
                    st.error(f"Error: {e}")
            else:
                r_actual = st.number_input(
                    "Relación actual entre límites (R' = B'/A')",
                    min_value=1.000001, value=1.92066, format="%.5f",
                )
            reduccion_pct = st.number_input(
                "Reducción deseada de la relación (%)",
                min_value=0.1, max_value=99.9, value=30.0, step=1.0, format="%.2f",
            )
            reduccion = reduccion_pct / 100
        else:
            r_objetivo = st.number_input(
                "Relación objetivo entre límites (R' = B'/A')",
                min_value=1.000001, value=1.34446, format="%.5f",
            )

        n_preliminar = st.number_input(
            "Tamaño de muestra ya relevado (n preliminar, opcional)",
            min_value=0, step=1, value=20,
            help="Si ya mediste algunas unidades y querés saber cuántas más faltan (Δn).",
            key="var_n_preliminar",
        )

        if st.button("Calcular"):
            try:
                if reduccion is not None:
                    if r_actual is None:
                        raise ValueError("Falta la relación actual entre límites.")
                    result = intervals.n_varianza_por_reduccion(r_actual, reduccion, alpha)
                else:
                    result = intervals.n_varianza_por_relacion(r_objetivo, alpha)
                mostrar_n_varianza(result, n_preliminar=int(n_preliminar))
            except ValueError as e:
                st.error(f"Error: {e}")
    else:
        n, _, s = input_resumen_muestra("varianza_ic", pedir_s=True)

        if st.button("Calcular") and n is not None:
            try:
                var_result = intervals.ic_varianza(s ** 2, n, alpha)
                desvio_result = intervals.ic_desvio(s ** 2, n, alpha)
                st.subheader("Varianza (σ²)")
                mostrar_intervalo("\\sigma^2", var_result)
                st.subheader("Desvío (σ)")
                mostrar_intervalo("\\sigma", desvio_result)
            except ValueError as e:
                st.error(f"Error: {e}")

else:  # Proporción
    if objetivo == "Intervalo de Confianza":
        r = st.number_input("Cantidad de éxitos (r)", min_value=0, step=1, value=1)
        n = st.number_input("Tamaño de muestra (n)", min_value=1, step=1, value=30)

        if st.button("Calcular"):
            try:
                p_hat = r / n
                st.write(f"Proporción muestral: p̂ = {p_hat:.5f}")

                exacto = intervals.ic_proporcion_exacto(int(r), int(n), alpha)
                st.subheader("Método exacto (Clopper-Pearson / transformación F)")
                mostrar_intervalo("p", exacto)

                with st.expander("Comparar con aproximación normal"):
                    normal = intervals.ic_proporcion_normal(p_hat, n, alpha)
                    mostrar_intervalo("p", normal)
            except ValueError as e:
                st.error(f"Error: {e}")

    else:
        p_hat = st.number_input(
            "Proporción estimada (p̂) — usar 0.5 si no hay estimación previa",
            min_value=0.0, max_value=1.0, value=0.5, format="%.5f",
        )
        e = st.number_input("Error admitido (e)", min_value=1e-9, value=0.05, format="%.5f")
        n_preliminar = st.number_input(
            "Tamaño de muestra ya relevado (n preliminar, opcional)",
            min_value=0, step=1, value=0,
            help="Si ya encuestaste algunos casos y querés saber cuántos más faltan (Δn).",
        )

        if st.button("Calcular"):
            try:
                n_result = intervals.n_proporcion(p_hat, e, alpha)
                mostrar_n(n_result, n_preliminar=int(n_preliminar))
            except ValueError as e:
                st.error(f"Error: {e}")
