import streamlit as st

from solver import chi_square as chi
from solver import wording

st.title("Contrastes Chi-Cuadrado")

tipo_contraste = st.selectbox(
    "¿Qué tipo de contraste querés realizar?",
    ["Bondad de ajuste", "Tabla de contingencia"]
)

# Nivel de significación (igual para ambos)
alpha = st.number_input(
    "Nivel de significación (alpha)", min_value=0.001, max_value=0.5, value=0.05, step=0.01, format="%.5f"
)


def mostrar_resultado_chi_square(result: chi.ChiSquareResult, contexto: str) -> None:
    """Muestra el resultado de un contraste chi-cuadrado."""
    # Mostrar warnings si los hay
    for w in result.warnings:
        st.warning(w)

    # Mostrar valores clave
    st.subheader("Resultado del Cálculo")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("chi2 calculado", f"{result.chi2_calc:.5f}")
    with col2:
        st.metric("chi2 critico (gl={})".format(result.df), f"{result.chi2_critico:.5f}")

    st.metric("Grados de libertad (nu)", result.df)

    # Decisión
    if result.rejects_h0:
        st.error("[RECHAZA] Se RECHAZA H0")
    else:
        st.warning("[NO RECHAZA] NO se rechaza H0")

    # Redacción formal
    texto = wording.texto_chi_cuadrado(result, contexto, alpha)
    st.write("**Conclusión:** " + texto)


# ============================================================================
# BONDAD DE AJUSTE
# ============================================================================

if tipo_contraste == "Bondad de ajuste":
    st.subheader("Bondad de Ajuste")
    st.info(
        "Ingresa las frecuencias observadas y esperadas (ya calculadas para el modelo que querés probar).\n"
        "Separa los valores con comas o espacios."
    )

    # Input de frecuencias observadas
    obs_input = st.text_area(
        "Frecuencias observadas (F_o_i):",
        value="14, 6, 6, 13, 16, 5",
        help="Ejemplo: 14, 6, 6, 13, 16, 5"
    )

    # Input de frecuencias esperadas
    exp_input = st.text_area(
        "Frecuencias esperadas (F_e_i):",
        value="10, 10, 10, 10, 10, 10",
        help="Ejemplo: 10, 10, 10, 10, 10, 10"
    )

    # Cantidad de parámetros estimados
    p = st.number_input(
        "Cantidad de parámetros estimados (p):",
        min_value=0,
        step=1,
        value=0,
        help="p = 0 si los parámetros estaban fijos; p = 2 si se estimaron media y desvío (Normal), etc."
    )

    if st.button("Calcular"):
        try:
            # Parsear las listas
            def parse_numbers(s):
                import re
                # Reemplazar comas por espacios y splitear
                nums = re.split(r'[,\s]+', s.strip())
                return [float(n) for n in nums if n]

            observados = parse_numbers(obs_input)
            esperados = parse_numbers(exp_input)

            if not observados or not esperados:
                st.error("Ingresa valores validos en ambas listas.")
            else:
                result = chi.bondad_de_ajuste(observados, esperados, p, alpha)
                contexto = "los datos siguen el modelo especificado"
                mostrar_resultado_chi_square(result, contexto)

        except ValueError as e:
            st.error(f"Error: {e}")


# ============================================================================
# TABLA DE CONTINGENCIA
# ============================================================================

else:  # Tabla de contingencia
    st.subheader("Tabla de Contingencia (Independencia/Homogeneidad)")
    st.info(
        "Ingresa la tabla de frecuencias observadas.\n"
        "Cada fila es una linea con valores separados por comas."
    )

    # Input de tabla
    tabla_input = st.text_area(
        "Tabla de frecuencias observadas (filas x columnas):",
        value="35, 37\n165, 263\n300, 500",
        help="Ejemplo para tabla 3x2:\n35, 37\n165, 263\n300, 500"
    )

    if st.button("Calcular"):
        try:
            # Parsear la tabla
            def parse_numbers(s):
                import re
                nums = re.split(r'[,\s]+', s.strip())
                return [float(n) for n in nums if n]

            filas = [line.strip() for line in tabla_input.strip().split('\n') if line.strip()]
            tabla = []
            for fila in filas:
                tabla.append(parse_numbers(fila))

            if not tabla or not tabla[0]:
                st.error("Ingresa una tabla valida.")
            else:
                result = chi.tabla_contingencia(tabla, alpha)
                contexto = "las variables son independientes"
                mostrar_resultado_chi_square(result, contexto)

                # Mostrar tabla esperada si está disponible
                if result.expected_table:
                    st.subheader("Tabla de Frecuencias Esperadas")
                    import pandas as pd
                    df_expected = pd.DataFrame(result.expected_table)
                    st.dataframe(df_expected.round(5))

        except ValueError as e:
            st.error(f"Error: {e}")
