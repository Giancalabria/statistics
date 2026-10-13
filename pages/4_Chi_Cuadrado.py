import streamlit as st

import pandas as pd

from solver import ajuste as aj
from solver import chi_square as chi
from solver import wording

st.title("Contrastes Chi-Cuadrado")

tipo_contraste = st.selectbox(
    "¿Qué tipo de contraste querés realizar?",
    ["Ajuste a un modelo (calcula las Fe)", "Bondad de ajuste (Fe ya calculadas)", "Tabla de contingencia"]
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

if tipo_contraste.startswith("Ajuste a un modelo"):
    st.subheader("Ajuste a un modelo teórico")
    st.info("Cargá la tabla de frecuencias: una clase por renglón. Para un modelo continuo, los límites de la clase y "
            "la frecuencia (`20-30 ; 6`); para uno discreto, el valor y la frecuencia (`0 ; 26`). Los parámetros que "
            "no cargues se estiman con la muestra (marcas de clase, desvío corregido) y restan grados de libertad. "
            "La primera y la última clase se extienden al borde del dominio; las clases con Fe < 5 se amalgaman.")
    modelo = st.selectbox("Modelo", list(aj.NOMBRES), format_func=lambda m: aj.NOMBRES[m], index=list(aj.NOMBRES).index("normal"))
    tabla_txt = st.text_area("Tabla (clase ; frecuencia observada)", height=200,
                             value="20-30 ; 6\n30-40 ; 90\n40-50 ; 232\n50-60 ; 192\n60-70 ; 66\n70-80 ; 12\n80-90 ; 2")
    PARAMS = {"normal": ["mu", "sigma"], "lognormal": ["m", "D"], "exponencial": ["lambda"], "gamma": ["r", "lambda"],
              "weibull": ["w", "beta"], "gumbel_max": ["u", "beta"], "gumbel_min": ["u", "beta"],
              "pareto": ["alpha", "b"], "uniforme_continua": ["a", "b"], "poisson": ["m"], "binomial": ["n", "p"],
              "uniforme": []}
    st.caption("Parámetros conocidos (dejá vacío lo que haya que estimar). Pareto: alpha = valor mínimo θ. "
               "Gumbel: u = modo. Binomial: n es obligatorio.")
    conocidos = {}
    cols = st.columns(max(1, len(PARAMS[modelo])))
    for c, nombre in zip(cols, PARAMS[modelo]):
        v = c.text_input(nombre, value="", key=f"aj_{modelo}_{nombre}")
        if v.strip():
            conocidos[nombre] = float(v.replace(",", "."))
    if st.button("Calcular"):
        try:
            limites, valores, fo = [], [], []
            for linea in [l for l in tabla_txt.splitlines() if l.strip()]:
                clase, _, f = linea.rpartition(";")
                fo.append(float(f.strip().replace(",", ".")))
                clase = clase.strip()
                if "-" in clase.lstrip("-"):
                    a, b = clase.split("-", 1) if not clase.startswith("-") else ("-" + clase[1:].split("-", 1)[0], clase[1:].split("-", 1)[1])
                    limites.append((float(a.replace(",", ".")), float(b.replace(",", "."))))
                else:
                    valores.append(clase)
            if modelo in aj.DISCRETOS:
                vals = valores if modelo == "uniforme" else [float(v.replace(",", ".")) for v in valores]
                r = aj.ajuste_discreto(modelo, vals, fo, alpha, conocidos)
            else:
                r = aj.ajuste_continuo(modelo, limites, fo, alpha, conocidos)
        except (ValueError, IndexError) as e:
            st.error(f"No se pudo calcular: {e}")
        else:
            for a in r.avisos:
                st.info(a)
            if r.media is not None:
                st.write(f"x̄ = {r.media:.4f}" + (f" · S = {r.desvio:.4f}" if r.desvio else ""))
            st.write("**Parámetros:** " + ", ".join(f"{k} = {v:.5g}" + (" (estimado)" if k in r.estimados else "")
                                                    for k, v in r.parametros.items() if isinstance(v, (int, float))))
            st.write("**Tabla del modelo**")
            st.dataframe(pd.DataFrame([{"Clase": c.etiqueta, "Fo": c.fo, "P": round(c.prob, 5), "Fe": round(c.fe, 3)}
                                       for c in r.tabla]), hide_index=True)
            if len(r.tabla_final) < len(r.tabla):
                st.write("**Después de amalgamar (Fe ≥ 5)**")
                st.dataframe(pd.DataFrame([{"Clase": c.etiqueta, "Fo": c.fo, "Fe": round(c.fe, 3)}
                                           for c in r.tabla_final]), hide_index=True)
            res = chi.ChiSquareResult(chi2_calc=r.chi2_calc, df=r.df, chi2_critico=r.chi2_critico, rejects_h0=r.rechaza)
            st.caption(f"ν = k - 1 - p = {len(r.tabla_final)} - 1 - {len(r.estimados)} = {r.df}")
            mostrar_resultado_chi_square(res, f"la variable sigue el modelo {aj.NOMBRES[modelo]}")

elif tipo_contraste.startswith("Bondad de ajuste"):
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
