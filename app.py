import streamlit as st

st.set_page_config(page_title="Solver de Estadística Aplicada", layout="centered")

st.title("Solver de Estadística Aplicada")
st.write(
    "Elegí un módulo en la barra lateral izquierda. Cada módulo pregunta lo que sabés "
    "del problema (no la fórmula a usar) y arma el camino correcto siguiendo el árbol "
    "de decisión de `esquema_teorico_examen_estadistica.md`."
)

st.markdown(
    """
- **Intervalos de Confianza**: media, varianza/desvío, proporción — IC y tamaño de muestra.
- **Ensayo de Hipótesis (1 población)**: media (Z y t), varianza (χ²), proporción (binomial exacto) — decisión, β/potencia y n para potencia fijada.
- **Comparación de 2 poblaciones**: test F (varianzas), pooled/Welch automático (medias, muestras independientes), muestras apareadas.
- **Contrastes chi-cuadrado**: bondad de ajuste (Fo/Fe provistos), tablas de contingencia (Fe auto-calculado).
"""
)
