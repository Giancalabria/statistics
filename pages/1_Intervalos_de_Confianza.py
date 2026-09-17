import streamlit as st

from solver import intervals, wording

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


def mostrar_n(n_result: intervals.SampleSizeResult) -> None:
    for w in n_result.warnings:
        st.warning(w)
    st.success(wording.texto_tamano_muestra(n_result))


if parametro == "Media":
    sigma_conocido = st.radio("¿Se conoce el desvío poblacional σ?", ["Sí", "No"]) == "Sí"

    if objetivo == "Intervalo de Confianza":
        xbar = st.number_input("Media muestral (x̄)", value=0.0, format="%.5f")
        n = st.number_input("Tamaño de muestra (n)", min_value=2, step=1, value=30)
        if sigma_conocido:
            sigma = st.number_input("Desvío poblacional (σ)", min_value=1e-9, value=1.0, format="%.5f")
        else:
            s = st.number_input("Desvío muestral (S)", min_value=1e-9, value=1.0, format="%.5f")

        if st.button("Calcular"):
            try:
                if sigma_conocido:
                    result = intervals.ic_media_sigma_conocido(xbar, sigma, n, alpha, N=N)
                else:
                    result = intervals.ic_media_sigma_desconocido(xbar, s, n, alpha, N=N)
                mostrar_intervalo("\\mu", result)
            except ValueError as e:
                st.error(f"Error: {e}")

    else:
        e = st.number_input("Error muestral admitido (e)", min_value=1e-9, value=1.0, format="%.5f")
        if sigma_conocido:
            sigma = st.number_input("Desvío poblacional (σ)", min_value=1e-9, value=1.0, format="%.5f")
        else:
            s = st.number_input("Desvío muestral (S)", min_value=1e-9, value=1.0, format="%.5f")

        if st.button("Calcular"):
            try:
                if sigma_conocido:
                    n_result = intervals.n_media_sigma_conocido(sigma, e, alpha, N=N)
                else:
                    n_result = intervals.n_media_sigma_desconocido(s, e, alpha, N=N)
                mostrar_n(n_result)
            except ValueError as e:
                st.error(f"Error: {e}")

elif parametro == "Varianza / Desvío":
    if objetivo == "Tamaño de muestra (n)":
        st.warning(
            "El esquema teórico no define una fórmula de tamaño de muestra para la "
            "varianza/desvío (solo para media y proporción)."
        )
    else:
        s = st.number_input("Desvío muestral (S)", min_value=1e-9, value=1.0, format="%.5f")
        n = st.number_input("Tamaño de muestra (n)", min_value=2, step=1, value=30)

        if st.button("Calcular"):
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

        if st.button("Calcular"):
            try:
                n_result = intervals.n_proporcion(p_hat, e, alpha)
                mostrar_n(n_result)
            except ValueError as e:
                st.error(f"Error: {e}")
