import streamlit as st

from solver import hypothesis_one as hyp
from solver import wording

st.title("Ensayo de Hipótesis (1 población)")

parametro = st.selectbox(
    "¿Qué parámetro querés contrastar?", ["Media", "Varianza", "Proporción"]
)

# Nivel de significación
alpha = st.number_input(
    "Nivel de significación (α)", min_value=0.001, max_value=0.5, value=0.05, step=0.01
)

# Cola del ensayo
cola = st.radio("¿Tipo de ensayo?", ["Unilateral cola derecha", "Unilateral cola izquierda", "Bilateral"])
tail = "derecha" if cola == "Unilateral cola derecha" else ("izquierda" if cola == "Unilateral cola izquierda" else "bilateral")

# Función para mostrar resultados
def mostrar_ensayo(result: hyp.HypothesisTestResult) -> None:
    for w in result.warnings:
        st.warning(w)

    # Mostrar valor crítico
    if isinstance(result.critical_value, tuple):
        c1, c2 = result.critical_value
        if result.distribution == "Binomial (exacto)":
            st.write(f"**Valores críticos**: r_c1 = {c1}, r_c2 = {c2}")
        else:
            st.write(f"**Valores críticos**: {c1:.4f} ≤ parámetro ≤ {c2:.4f}")
    else:
        if result.distribution == "Binomial (exacto)":
            st.write(f"**Valor crítico**: r_c = {result.critical_value}")
        else:
            st.write(f"**Valor crítico**: {result.critical_value:.4f}")

    # Decisión
    if result.rejects_h0:
        st.error("✓ Se RECHAZA H0")
    else:
        st.warning("✗ NO se rechaza H0")

    # Redacción formal
    st.write("**Conclusión:** " + wording.texto_ensayo(result, alpha))

    # Beta, potencia, p-value
    with st.expander("Detalle del cálculo"):
        st.write(f"Distribución utilizada: {result.distribution}")
        if result.df is not None:
            st.write(f"Grados de libertad: {result.df}")
        if result.beta is not None:
            st.write(f"Error Tipo II (β): {result.beta:.4f}")
        if result.power is not None:
            st.write(f"Potencia (1-β): {result.power:.4f}")
        if result.p_value is not None:
            st.write(f"Valor a posteriori (α*): {result.p_value:.4f}")


if parametro == "Media":
    sigma_conocido = st.radio("¿Se conoce el desvío poblacional σ?", ["Sí", "No"]) == "Sí"
    objetivo = st.radio(
        "¿Qué querés hacer?", ["Ensayar la hipótesis (dado x̄)", "Calcular n para una potencia fijada"]
    )

    mu0 = st.number_input("Media bajo H0 (μ₀)", value=0.0)

    if objetivo == "Ensayar la hipótesis (dado x̄)":
        xbar = st.number_input("Media muestral (x̄)", value=0.0)
        n = st.number_input("Tamaño de muestra (n)", min_value=2, step=1, value=30)

        if sigma_conocido:
            sigma = st.number_input("Desvío poblacional (σ)", min_value=1e-9, value=1.0)
        else:
            s = st.number_input("Desvío muestral (S)", min_value=1e-9, value=1.0)

        # Opcionalmente calcular β y potencia
        calcular_potencia = st.checkbox("¿Calcular β y potencia? (proporcionar μ₁ alternativa)")
        mu1 = None
        if calcular_potencia:
            mu1 = st.number_input("Media alternativa (μ₁)", value=1.0)

        if st.button("Calcular"):
            try:
                if sigma_conocido:
                    result = hyp.ensayo_media_sigma_conocido(
                        xbar=xbar, sigma=sigma, n=n, mu0=mu0, alpha=alpha, tail=tail, mu1=mu1
                    )
                else:
                    result = hyp.ensayo_media_sigma_desconocido(
                        xbar=xbar, s=s, n=n, mu0=mu0, alpha=alpha, tail=tail, mu1=mu1
                    )
                mostrar_ensayo(result)
            except ValueError as e:
                st.error(f"Error: {e}")

    else:  # Calcular n para potencia fijada
        mu1 = st.number_input("Media alternativa a detectar (μ₁)", value=1.0)
        beta_deseado = st.number_input(
            "Error Tipo II admitido (β)", min_value=0.001, max_value=0.5, value=0.20, step=0.01
        )

        if sigma_conocido:
            sigma = st.number_input("Desvío poblacional (σ)", min_value=1e-9, value=1.0)
        else:
            s = st.number_input("Desvío muestral (S)", min_value=1e-9, value=1.0)

        if st.button("Calcular"):
            try:
                if sigma_conocido:
                    n_resultado = hyp.n_media_sigma_conocido_para_potencia(
                        sigma=sigma, mu0=mu0, mu1=mu1, alpha=alpha, beta=beta_deseado, tail=tail
                    )
                else:
                    st.info(
                        "No se validó este caso (σ desconocido + potencia fijada) contra "
                        "ningún ejercicio real de la cátedra; es una extensión analógica."
                    )
                    n_resultado = hyp.n_media_sigma_desconocido_para_potencia(
                        s=s, mu0=mu0, mu1=mu1, alpha=alpha, beta=beta_deseado, tail=tail
                    )
                st.success(f"El tamaño de muestra necesario es n = {n_resultado}.")
            except ValueError as e:
                st.error(f"Error: {e}")

elif parametro == "Varianza":
    s = st.number_input("Desvío muestral (S)", min_value=1e-9, value=1.0)
    n = st.number_input("Tamaño de muestra (n)", min_value=2, step=1, value=30)
    sigma0 = st.number_input("Desvío bajo H0 (σ₀)", min_value=1e-9, value=1.0)

    # Opcionalmente β y potencia
    calcular_potencia = st.checkbox("¿Calcular β y potencia? (proporcionar σ₁ alternativa)")
    sigma1 = None
    if calcular_potencia:
        sigma1 = st.number_input("Desvío alternativo (σ₁)", min_value=1e-9, value=1.5)

    if st.button("Calcular"):
        try:
            s2 = s ** 2
            sigma0_2 = sigma0 ** 2
            sigma1_2 = sigma1 ** 2 if sigma1 is not None else None

            result = hyp.ensayo_varianza(
                s2=s2, n=n, sigma0_2=sigma0_2, alpha=alpha, tail=tail, sigma1_2=sigma1_2
            )
            mostrar_ensayo(result)
        except ValueError as e:
            st.error(f"Error: {e}")

else:  # Proporción
    r = st.number_input("Cantidad de éxitos (r)", min_value=0, step=1, value=1)
    n = st.number_input("Tamaño de muestra (n)", min_value=1, step=1, value=30)
    p0 = st.number_input("Proporción bajo H0 (p₀)", min_value=0.001, max_value=0.999, value=0.5)

    p_hat = r / n
    st.write(f"Proporción muestral: p̂ = {p_hat:.4f}")

    # Opcionalmente β y potencia
    calcular_potencia = st.checkbox("¿Calcular β y potencia? (proporcionar p₁ alternativa)")
    p1 = None
    if calcular_potencia:
        p1 = st.number_input("Proporción alternativa (p₁)", min_value=0.001, max_value=0.999, value=0.6)

    if st.button("Calcular"):
        try:
            result = hyp.ensayo_proporcion(
                r=int(r), n=int(n), p0=p0, alpha=alpha, tail=tail, p1=p1
            )
            mostrar_ensayo(result)
        except ValueError as e:
            st.error(f"Error: {e}")
