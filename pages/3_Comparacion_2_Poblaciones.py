import streamlit as st

from solver import two_samples as ts
from solver import wording

st.title("Comparación de 2 Poblaciones")

# Seleccionar qué comparar
opcion = st.selectbox(
    "¿Qué querés comparar?",
    ["Varianzas (Test F)", "Medias - Muestras Independientes", "Medias - Muestras Apareadas"]
)

# Nivel de significación (aplica a todos)
alpha = st.number_input(
    "Nivel de significación (α)", min_value=0.001, max_value=0.5, value=0.05, step=0.01, format="%.5f"
)


# ---------------------------------------------------------------------------
# Función auxiliar para mostrar resultados de ensayo
# ---------------------------------------------------------------------------

def mostrar_ensayo(result) -> None:
    """Mostrar resultado de ensayo de hipótesis."""
    for w in result.warnings:
        st.warning(w)

    # Mostrar valor crítico
    if isinstance(result.critical_value, tuple):
        c1, c2 = result.critical_value
        if result.distribution == "F":
            st.write(f"**Valores críticos**: {c1:.5f} ≤ j² ≤ {c2:.5f}")
        else:
            st.write(f"**Valores críticos**: {c1:.5f} ≤ parámetro ≤ {c2:.5f}")
    else:
        st.write(f"**Valor crítico**: {result.critical_value:.5f}")

    # Decisión
    if result.rejects_h0:
        st.error("✓ Se RECHAZA H0")
    else:
        st.warning("✗ NO se rechaza H0")

    # Redacción formal
    st.write("**Conclusión:** " + wording.texto_ensayo(result, alpha))

    # Detalles
    with st.expander("Detalle del cálculo"):
        st.write(f"Distribución utilizada: {result.distribution}")
        if result.df is not None:
            st.write(f"Grados de libertad: {result.df}")


def mostrar_intervalo(parametro: str, result) -> None:
    """Mostrar resultado de intervalo de confianza."""
    for w in result.warnings:
        st.warning(w)
    st.latex(f"{result.a:.5f} \\le {parametro} \\le {result.b:.5f}")
    confianza = 1 - alpha
    st.write(wording.texto_intervalo(parametro, result, confianza))
    with st.expander("Detalle del cálculo"):
        st.write(f"Distribución utilizada: {result.distribution}")
        if result.df is not None:
            st.write(f"Grados de libertad: {result.df}")
        if result.critical_value is not None:
            st.write(f"Valor crítico: {wording.fmt_num(result.critical_value)}")
        if result.error is not None:
            st.write(f"Error muestral (e): {result.error:.5f}")


# ---------------------------------------------------------------------------
# CASO 1: Varianzas (Test F)
# ---------------------------------------------------------------------------

if opcion == "Varianzas (Test F)":
    st.subheader("Test F - Comparación de Varianzas")
    st.info("Se ensaya la hipótesis de igualdad de varianzas: H0: σ₁² = σ₂² (bilateral)")

    col1, col2 = st.columns(2)
    with col1:
        s1 = st.number_input("Desvío muestra 1 (S₁)", min_value=1e-9, value=1.0, format="%.5f")
        n1 = st.number_input("Tamaño muestra 1 (n₁)", min_value=2, step=1, value=30)
    with col2:
        s2 = st.number_input("Desvío muestra 2 (S₂)", min_value=1e-9, value=1.0, format="%.5f")
        n2 = st.number_input("Tamaño muestra 2 (n₂)", min_value=2, step=1, value=30)

    objetivo_f = st.radio("¿Qué querés calcular?", ["Ensayo de hipótesis", "Intervalo de confianza para razón de varianzas"])

    if st.button("Calcular", key="btn_f_test"):
        try:
            if objetivo_f == "Ensayo de hipótesis":
                result = ts.f_test_equal_variances(s1, n1, s2, n2, alpha)
                mostrar_ensayo(result)
            else:
                # IC de razón de varianzas
                result_dir, result_inv = ts.ic_ratio_varianzas(s1, n1, s2, n2, alpha)
                confianza = 1 - alpha

                st.subheader("IC para σ₁²/σ₂²")
                mostrar_intervalo("\\phi^2", result_dir)

                st.subheader("IC para σ₂²/σ₁² (razón inversa)")
                mostrar_intervalo("1/\\phi^2", result_inv)
        except ValueError as e:
            st.error(f"Error: {e}")


# ---------------------------------------------------------------------------
# CASO 2: Medias - Muestras Independientes (con test F automático)
# ---------------------------------------------------------------------------

elif opcion == "Medias - Muestras Independientes":
    st.subheader("Comparación de Medias - Muestras Independientes")
    st.info("Paso 1: Se automatiza el test F para decidir entre pooled (varianzas iguales) o Welch (varianzas distintas).")

    # Recolectar datos de ambas muestras
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Muestra 1:**")
        xbar1 = st.number_input("Media muestral (x̄₁)", value=0.0, key="xbar1", format="%.5f")
        s1 = st.number_input("Desvío muestral (S₁)", min_value=1e-9, value=1.0, key="s1_ind", format="%.5f")
        n1 = st.number_input("Tamaño muestra (n₁)", min_value=2, step=1, value=30, key="n1_ind")

    with col2:
        st.write("**Muestra 2:**")
        xbar2 = st.number_input("Media muestral (x̄₂)", value=0.0, key="xbar2", format="%.5f")
        s2 = st.number_input("Desvío muestral (S₂)", min_value=1e-9, value=1.0, key="s2_ind", format="%.5f")
        n2 = st.number_input("Tamaño muestra (n₂)", min_value=2, step=1, value=30, key="n2_ind")

    # Paso 1: Test F automático
    f_result = ts.f_test_equal_variances(s1, n1, s2, n2, alpha)

    if f_result.rejects_h0:
        st.warning("**Test F: Se RECHAZA H0 (varianzas distintas) → Se usa método de Welch**")
        metodo = "Welch"
    else:
        st.success("**Test F: NO se rechaza H0 (varianzas iguales) → Se usa método pooled**")
        metodo = "Pooled"

    # Paso 2: Recolectar parámetros del ensayo/IC
    st.divider()
    delta0 = st.number_input("Diferencia bajo H0 (δ₀)", value=0.0, format="%.5f")
    objetivo_ind = st.radio(
        "¿Qué querés calcular?",
        ["Intervalo de Confianza", "Ensayo de Hipótesis", "Tamaño de muestra (n)"]
    )

    if objetivo_ind == "Ensayo de Hipótesis":
        cola = st.radio("¿Tipo de ensayo?", ["Unilateral cola derecha", "Unilateral cola izquierda", "Bilateral"])
        tail = "derecha" if cola == "Unilateral cola derecha" else ("izquierda" if cola == "Unilateral cola izquierda" else "bilateral")

        if st.button("Calcular", key="btn_ensayo_ind"):
            try:
                if metodo == "Pooled":
                    result = ts.ensayo_media_diferencia_varianzas_iguales(
                        xbar1, s1, n1, xbar2, s2, n2, delta0, alpha, tail
                    )
                else:
                    result = ts.ensayo_media_diferencia_varianzas_distintas(
                        xbar1, s1, n1, xbar2, s2, n2, delta0, alpha, tail
                    )
                mostrar_ensayo(result)
            except ValueError as e:
                st.error(f"Error: {e}")

    elif objetivo_ind == "Intervalo de Confianza":
        if st.button("Calcular", key="btn_ic_ind"):
            try:
                if metodo == "Pooled":
                    result = ts.ic_media_diferencia_varianzas_iguales(
                        xbar1, s1, n1, xbar2, s2, n2, alpha
                    )
                else:
                    result = ts.ic_media_diferencia_varianzas_distintas(
                        xbar1, s1, n1, xbar2, s2, n2, alpha
                    )
                mostrar_intervalo("\\delta", result)
            except ValueError as e:
                st.error(f"Error: {e}")

    else:  # Tamaño de muestra
        e = st.number_input("Error muestral deseado (e)", min_value=1e-9, value=1.0, format="%.5f")
        if st.button("Calcular", key="btn_n_ind"):
            try:
                if metodo == "Pooled":
                    result = ts.n_media_diferencia_varianzas_iguales_para_error(s1, s2, e, alpha)
                else:
                    st.info("Nota: El cálculo de n para Welch aún no está implementado (requiere búsqueda iterativa específica).")
                    result = None

                if result:
                    st.success(wording.texto_tamano_muestra(result))
            except ValueError as e:
                st.error(f"Error: {e}")


# ---------------------------------------------------------------------------
# CASO 3: Medias - Muestras Apareadas
# ---------------------------------------------------------------------------

elif opcion == "Medias - Muestras Apareadas":
    st.subheader("Comparación de Medias - Muestras Apareadas")
    st.info("Se trabaja sobre las diferencias d_i = X₁ᵢ - X₂ᵢ. Se aplica el ensayo t de una muestra a las diferencias.")

    st.write("Ingresa las diferencias (d₁, d₂, ..., dₙ) separadas por comas o espacios:")
    diff_input = st.text_area("Diferencias", value="0, 0", height=100)

    # Parsear las diferencias
    try:
        diff_str = diff_input.replace(",", " ").split()
        differences = [float(d) for d in diff_str if d]
        if len(differences) < 2:
            st.error("Se necesitan al menos 2 diferencias (2 pares).")
            differences = None
    except ValueError:
        st.error("No se pudieron parsear las diferencias. Verifica el formato.")
        differences = None

    if differences is not None:
        st.success(f"✓ Se ingresaron {len(differences)} pares (diferencias: {differences})")

        delta0 = st.number_input("Diferencia bajo H0 (δ₀)", value=0.0, key="delta0_paired", format="%.5f")
        objetivo_paired = st.radio(
            "¿Qué querés calcular?",
            ["Intervalo de Confianza", "Ensayo de Hipótesis", "Tamaño de muestra (n)"]
        )

        if objetivo_paired == "Ensayo de Hipótesis":
            cola = st.radio("¿Tipo de ensayo?", ["Unilateral cola derecha", "Unilateral cola izquierda", "Bilateral"], key="cola_paired")
            tail = "derecha" if cola == "Unilateral cola derecha" else ("izquierda" if cola == "Unilateral cola izquierda" else "bilateral")

            if st.button("Calcular", key="btn_ensayo_paired"):
                try:
                    result = ts.ensayo_media_apareada(differences, delta0, alpha, tail)
                    mostrar_ensayo(result)
                except ValueError as e:
                    st.error(f"Error: {e}")

        elif objetivo_paired == "Intervalo de Confianza":
            if st.button("Calcular", key="btn_ic_paired"):
                try:
                    result = ts.ic_media_apareada(differences, alpha)
                    mostrar_intervalo("\\delta", result)
                except ValueError as e:
                    st.error(f"Error: {e}")

        else:  # Tamaño de muestra
            # Calcular S_d a partir de las diferencias
            import statistics
            mean_d = statistics.mean(differences)
            s_d = statistics.stdev(differences)
            e = st.number_input("Error muestral deseado (e)", min_value=1e-9, value=1.0, key="e_paired", format="%.5f")

            if st.button("Calcular", key="btn_n_paired"):
                try:
                    result = ts.n_media_apareada_para_error(s_d, e, alpha)
                    st.success(wording.texto_tamano_muestra(result))
                except ValueError as e:
                    st.error(f"Error: {e}")
