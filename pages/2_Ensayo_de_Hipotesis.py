import streamlit as st

from solver import hypothesis_one as hyp
from solver import wording


def parse_numbers(texto: str):
    import re
    nums = re.split(r"[,\s]+", texto.strip())
    return [float(n) for n in nums if n]

st.title("Ensayo de Hipótesis (1 población)")

parametro = st.selectbox(
    "¿Qué parámetro querés contrastar?", ["Media", "Varianza", "Proporción"]
)

# Nivel de significación
alpha = st.number_input(
    "Nivel de significación (α)", min_value=0.001, max_value=0.5, value=0.05, step=0.01, format="%.5f"
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
            st.write(f"**Valores críticos**: {c1:.5f} ≤ parámetro ≤ {c2:.5f}")
    else:
        if result.distribution == "Binomial (exacto)":
            st.write(f"**Valor crítico**: r_c = {result.critical_value}")
        else:
            st.write(f"**Valor crítico**: {result.critical_value:.5f}")

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
            st.write(f"Error Tipo II (β): {result.beta:.5f}")
        if result.power is not None:
            st.write(f"Potencia (1-β): {result.power:.5f}")
        if result.p_value is not None:
            st.write(f"Valor a posteriori (α*): {result.p_value:.5f}")


if parametro == "Media":
    sigma_conocido = st.radio("¿Se conoce el desvío poblacional σ?", ["Sí", "No"]) == "Sí"
    objetivo = st.radio(
        "¿Qué querés hacer?", ["Ensayar la hipótesis (dado x̄)", "Calcular n para una potencia fijada"]
    )

    mu0 = st.number_input("Media bajo H0 (μ₀)", value=0.0, format="%.5f")

    if objetivo == "Ensayar la hipótesis (dado x̄)":
        xbar = st.number_input("Media muestral (x̄)", value=0.0, format="%.5f")
        n = st.number_input("Tamaño de muestra (n)", min_value=2, step=1, value=30)

        if sigma_conocido:
            sigma = st.number_input("Desvío poblacional (σ)", min_value=1e-9, value=1.0, format="%.5f")
        else:
            s = st.number_input("Desvío muestral (S)", min_value=1e-9, value=1.0, format="%.5f")

        # Opcionalmente calcular β y potencia
        calcular_potencia = st.checkbox("¿Calcular β y potencia? (proporcionar μ₁ alternativa)")
        mu1 = None
        if calcular_potencia:
            mu1 = st.number_input("Media alternativa (μ₁)", value=1.0, format="%.5f")

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

        with st.expander("Tabla de curva de potencia (OC) para varios μ₁"):
            st.write(
                "Ingresá una lista de valores μ₁ (separados por comas o espacios) para ver "
                "β y la potencia (1-β) en cada uno, sin tener que repetir el cálculo a mano."
            )
            mu1_texto = st.text_area("Valores de μ₁", value="", key="mu1_curva")
            if st.button("Generar tabla", key="btn_curva_potencia"):
                try:
                    mu1_list = parse_numbers(mu1_texto)
                    if not mu1_list:
                        st.error("Ingresá al menos un valor de μ₁.")
                    else:
                        tabla = hyp.curva_potencia_media(
                            mu0=mu0,
                            sigma_or_s=sigma if sigma_conocido else s,
                            n=n,
                            alpha=alpha,
                            mu1_list=mu1_list,
                            tail=tail,
                            sigma_conocido=sigma_conocido,
                        )
                        import pandas as pd
                        df = pd.DataFrame(tabla, columns=["μ₁", "β", "Potencia (1-β)"])
                        st.dataframe(df.round(4), hide_index=True)
                except ValueError as e:
                    st.error(f"Error: {e}")

    else:  # Calcular n para potencia fijada
        mu1 = st.number_input("Media alternativa a detectar (μ₁)", value=1.0, format="%.5f")
        beta_deseado = st.number_input(
            "Error Tipo II admitido (β)", min_value=0.001, max_value=0.5, value=0.20, step=0.01, format="%.5f"
        )

        if sigma_conocido:
            sigma = st.number_input("Desvío poblacional (σ)", min_value=1e-9, value=1.0, format="%.5f")
        else:
            s = st.number_input("Desvío muestral (S)", min_value=1e-9, value=1.0, format="%.5f")

        if st.button("Calcular"):
            try:
                if sigma_conocido:
                    d = hyp.disenar_ensayo_media_sigma_conocido(
                        sigma=sigma, mu0=mu0, mu1=mu1, alpha=alpha, beta=beta_deseado, tail=tail
                    )
                else:
                    d = hyp.disenar_ensayo_media_sigma_desconocido(
                        s=s, mu0=mu0, mu1=mu1, alpha=alpha, beta=beta_deseado, tail=tail
                    )
                st.session_state["diseno"] = d
                st.session_state["diseno_sigma"] = sigma if sigma_conocido else s
                st.session_state["diseno_sigma_conocido"] = sigma_conocido
            except ValueError as e:
                st.error(f"Error: {e}")
                st.session_state.pop("diseno", None)

        d = st.session_state.get("diseno")
        if d is not None:
            for w in d.warnings:
                st.warning(w)

            st.write(f"**Hipótesis nula (H0):** {d.h0_text}   |   **H1:** {d.h1_text}")

            if isinstance(d.critical_value, tuple):
                c1, c2 = d.critical_value
                st.write(
                    f"**Condición de rechazo:** se rechaza H0 si x̄ < {c1:.4f} o x̄ > {c2:.4f}"
                )
            else:
                signo = ">" if d.tail == "derecha" else "<"
                st.write(
                    f"**Condición de rechazo (CR):** si x̄ {signo} x̄_c = "
                    f"**{d.critical_value:.4f}** ⇒ se rechaza H0"
                )

            st.success(f"**Tamaño de muestra: n = {d.n}**")
            st.write(f"**Regla de decisión:** {d.regla_decision}")

            with st.expander("Detalle del cálculo"):
                st.write(f"Distribución utilizada: {d.distribution}")
                if d.df is not None:
                    st.write(f"Grados de libertad: {d.df}")
                etiqueta = "Z" if d.distribution == "Z" else "t"
                st.write(f"{etiqueta}_α = {d.z_alpha:.4f}  |  {etiqueta}_β = {d.z_beta:.4f}")
                st.write(f"n sin redondear = {d.n_exacto:.4f} → n = {d.n}")
                st.write(f"Error estándar con el n final: σ/√n = {d.se:.5f}")
                if d.xc_sistema is not None:
                    st.write(
                        f"x̄_c resolviendo el sistema sin redondear n = {d.xc_sistema:.4f} "
                        "(es el valor que suelen traer las respuestas de la guía; "
                        f"al redondear n a {d.n} el punto crítico que mantiene α exacto "
                        f"pasa a ser {d.critical_value:.4f} si el ensayo es unilateral)."
                    )
                st.write(
                    f"Con n = {d.n} y x̄_c, en μ₁ = {d.mu1}: "
                    f"β = {d.beta_real:.4f}, potencia = {d.potencia_real:.4f} "
                    f"(objetivo: potencia ≥ {1 - d.beta_objetivo:.4f})"
                )

            st.subheader("Potencia en otros valores de μ")
            st.write(
                "Probabilidad de rechazar H0 (de 'detectar') si la media verdadera es μ. "
                "Sirve para la parte de 'calcular la probabilidad de detectar que μ vale X'."
            )
            mu_texto = st.text_input(
                "Valores de μ (separados por comas o espacios)", value="", key="mu_diseno"
            )
            if mu_texto.strip():
                try:
                    mu_list = parse_numbers(mu_texto)
                    tabla = hyp.curva_potencia_media(
                        mu0=d.mu0,
                        sigma_or_s=st.session_state["diseno_sigma"],
                        n=d.n,
                        alpha=d.alpha,
                        mu1_list=mu_list,
                        tail=d.tail,
                        sigma_conocido=st.session_state["diseno_sigma_conocido"],
                    )
                    import pandas as pd
                    st.dataframe(
                        pd.DataFrame(tabla, columns=["μ", "β", "Potencia (1-β)"]).round(4),
                        hide_index=True,
                    )
                except ValueError as e:
                    st.error(f"Error: {e}")

            with st.expander("Curva de potencia del ensayo"):
                import numpy as np
                import pandas as pd

                delta = abs(d.mu0 - d.mu1)
                centro = (d.mu0 + d.mu1) / 2
                grilla = np.linspace(centro - 1.5 * delta, centro + 1.5 * delta, 60)
                curva = hyp.curva_potencia_media(
                    mu0=d.mu0,
                    sigma_or_s=st.session_state["diseno_sigma"],
                    n=d.n,
                    alpha=d.alpha,
                    mu1_list=list(grilla),
                    tail=d.tail,
                    sigma_conocido=st.session_state["diseno_sigma_conocido"],
                )
                df_curva = pd.DataFrame(curva, columns=["μ", "β", "Potencia (1-β)"])
                st.line_chart(df_curva.set_index("μ")[["Potencia (1-β)"]])

elif parametro == "Varianza":
    s = st.number_input("Desvío muestral (S)", min_value=1e-9, value=1.0, format="%.5f")
    n = st.number_input("Tamaño de muestra (n)", min_value=2, step=1, value=30)
    sigma0 = st.number_input("Desvío bajo H0 (σ₀)", min_value=1e-9, value=1.0, format="%.5f")

    # Opcionalmente β y potencia
    calcular_potencia = st.checkbox("¿Calcular β y potencia? (proporcionar σ₁ alternativa)")
    sigma1 = None
    if calcular_potencia:
        sigma1 = st.number_input("Desvío alternativo (σ₁)", min_value=1e-9, value=1.5, format="%.5f")

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
    p0 = st.number_input("Proporción bajo H0 (p₀)", min_value=0.001, max_value=0.999, value=0.5, format="%.5f")

    p_hat = r / n
    st.write(f"Proporción muestral: p̂ = {p_hat:.5f}")

    # Opcionalmente β y potencia
    calcular_potencia = st.checkbox("¿Calcular β y potencia? (proporcionar p₁ alternativa)")
    p1 = None
    if calcular_potencia:
        p1 = st.number_input("Proporción alternativa (p₁)", min_value=0.001, max_value=0.999, value=0.6, format="%.5f")

    if st.button("Calcular"):
        try:
            result = hyp.ensayo_proporcion(
                r=int(r), n=int(n), p0=p0, alpha=alpha, tail=tail, p1=p1
            )
            mostrar_ensayo(result)
        except ValueError as e:
            st.error(f"Error: {e}")
