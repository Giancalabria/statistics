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
    st.subheader("Comparación de varianzas / desvíos (TEMA IV)")
    st.info("Parámetro φ = σ₁/σ₂ con la muestra 1 en el NUMERADOR (j² = S₁²/S₂²). Si hay un grupo con el cambio "
            "(reacondicionado, propuesto, con aditivo) va como muestra 1: 'reducir el desvío un 12%' es φ < 0,88.")

    objetivo_f = st.radio("¿Qué querés calcular?", [
        "Ensayo de hipótesis (φ₀ y cola a elección, con β opcional)",
        "Intervalo de confianza para la relación de varianzas / desvíos",
        "Tamaño de muestra para una potencia fijada (n₁ = n₂)",
        "Tamaño de muestra por relación entre límites del IC (n₁ = n₂)",
    ])
    necesita_muestras = objetivo_f.startswith(("Ensayo", "Intervalo"))

    if necesita_muestras:
        col1, col2 = st.columns(2)
        with col1:
            s1 = st.number_input("Desvío muestra 1 (S₁, numerador)", min_value=1e-9, value=1.0, format="%.5f")
            n1 = st.number_input("Tamaño muestra 1 (n₁)", min_value=2, step=1, value=30)
        with col2:
            s2 = st.number_input("Desvío muestra 2 (S₂, denominador)", min_value=1e-9, value=1.0, format="%.5f")
            n2 = st.number_input("Tamaño muestra 2 (n₂)", min_value=2, step=1, value=30)

    colas = {"Unilateral izquierda (H1: φ < φ₀, p. ej. reducción)": "izquierda",
             "Unilateral derecha (H1: φ > φ₀, p. ej. aumento)": "derecha",
             "Bilateral (H1: φ ≠ φ₀)": "bilateral"}

    if objetivo_f.startswith("Ensayo"):
        phi0 = st.number_input("φ₀ = σ₁/σ₂ de H0 (1 = desvíos iguales; 0,88 = reducción del 12%)",
                               min_value=1e-6, value=1.0, format="%.4f")
        tail = colas[st.selectbox("Tipo de ensayo", list(colas))]
        con_beta = st.checkbox("Calcular β / potencia para una relación alternativa φ₁")
        phi1 = st.number_input("φ₁ alternativo (0,70 = reducción del 30%)", min_value=1e-6, value=0.7,
                               format="%.4f") if con_beta else None
    elif objetivo_f.startswith("Tamaño de muestra para una potencia"):
        phi0 = st.number_input("φ₀ de H0", min_value=1e-6, value=1.0, format="%.4f")
        phi1 = st.number_input("φ₁ alternativo", min_value=1e-6, value=0.7, format="%.4f")
        beta = st.number_input("β (1 - potencia)", min_value=0.001, max_value=0.5, value=0.10, format="%.4f")
    elif objetivo_f.startswith("Tamaño de muestra por relación"):
        sobre = st.radio("La relación entre límites es de…", ["desvíos (σ₁/σ₂)", "varianzas (σ₁²/σ₂²)"])
        r_obj = st.number_input("Relación buscada B/A (p. ej. 1,5 = límite superior 50% mayor)", min_value=1.0001,
                                value=1.5, format="%.4f")

    if st.button("Calcular", key="btn_f_test"):
        try:
            if objetivo_f.startswith("Ensayo"):
                result = ts.ensayo_relacion_desvios(s1, int(n1), s2, int(n2), alpha, phi0=phi0, tail=tail, phi1=phi1)
                st.write(f"**Hipótesis**: H0: {result.h0_text}  vs  H1: {result.h1_text}")
                st.write(f"**Estadístico**: j² = S₁²/S₂² = {result.observed_value:.5f} (j = {result.observed_value ** 0.5:.4f}); "
                         f"bajo H0, j²/φ₀² ~ F({int(n1) - 1}; {int(n2) - 1}).")
                mostrar_ensayo(result)
                if result.power is not None:
                    st.write(f"**Con φ = {phi1:g}**: β = {result.beta:.4f} ; potencia 1-β = {result.power:.4f}")
            elif objetivo_f.startswith("Intervalo"):
                result_dir, result_inv = ts.ic_ratio_varianzas(s1, int(n1), s2, int(n2), alpha)
                st.subheader("IC para σ₁²/σ₂² y para σ₁/σ₂")
                mostrar_intervalo("\\phi^2", result_dir)
                st.latex(f"{result_dir.a ** 0.5:.5f} \\le \\phi \\le {result_dir.b ** 0.5:.5f}")
                st.subheader("Razón inversa σ₂²/σ₁²")
                mostrar_intervalo("1/\\phi^2", result_inv)
                st.write(f"Relación entre límites B/A: {result_dir.b / result_dir.a:.4f} (varianzas) ; "
                         f"{(result_dir.b / result_dir.a) ** 0.5:.4f} (desvíos).")
            elif objetivo_f.startswith("Tamaño de muestra para una potencia"):
                r = ts.n_relacion_desvios_para_potencia(phi0, phi1, alpha, beta)
                st.success(f"n = {r.n} en cada muestra")
                st.write(f"H0: {r.h0_text}  vs  H1: {r.h1_text}")
                st.write(f"Condición de rechazo: j²c = {r.j2_c:.5f} (jc = {r.j2_c ** 0.5:.4f}). "
                         f"β real = {r.beta_real:.4f}, potencia real = {r.potencia_real:.4f}.")
            else:
                r = ts.n_relacion_por_limites(r_obj, alpha, sobre="desvios" if sobre.startswith("desv") else "varianzas")
                st.success(f"n = {r.n} en cada muestra")
                st.write(f"Relación lograda B/A = {r.r_logrado:.4f} ≤ {r_obj:.4f}.")
        except (ValueError, RuntimeError) as e:
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
        n_preliminar_ind = st.number_input(
            "Tamaño de muestra ya relevado por grupo (n preliminar, opcional)",
            min_value=0, step=1, value=0,
            help="Si ya mediste algunas unidades por grupo y querés saber cuántas más faltan (Δn).",
        )
        if st.button("Calcular", key="btn_n_ind"):
            try:
                if metodo == "Pooled":
                    result = ts.n_media_diferencia_varianzas_iguales_para_error(s1, s2, e, alpha)
                else:
                    st.info("Nota: El cálculo de n para Welch aún no está implementado (requiere búsqueda iterativa específica).")
                    result = None

                if result:
                    st.success(wording.texto_tamano_muestra(result, n_preliminar=int(n_preliminar_ind) or None))
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
            n_preliminar_paired = st.number_input(
                "Tamaño de muestra ya relevado (n preliminar, opcional)",
                min_value=0, step=1, value=0, key="n_prelim_paired",
                help="Si ya mediste algunos pares y querés saber cuántos más faltan (Δn).",
            )

            if st.button("Calcular", key="btn_n_paired"):
                try:
                    result = ts.n_media_apareada_para_error(s_d, e, alpha)
                    st.success(wording.texto_tamano_muestra(result, n_preliminar=int(n_preliminar_paired) or None))
                except ValueError as e:
                    st.error(f"Error: {e}")
