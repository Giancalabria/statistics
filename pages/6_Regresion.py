"""Regresión y correlación simple (TEMA VII) y modelo lineal general (TEMA VIII)."""

import pandas as pd
import streamlit as st

from interprete.tablas import columnas_numericas, desde_texto_editado
from solver import regresion as rg

st.title("Regresión y correlación")
st.write("Pegá la tabla de datos (primer renglón con los encabezados, una observación por renglón; separá con `|`, "
         "`;` o tab) y elegí la variable a explicar **y**. Con una sola x es regresión simple; con varias, el modelo "
         "lineal general.")

tabla_txt = st.text_area("Tabla de datos", height=200,
                         value="Área sembrada (10^6 ha) | PBI (millones U$s)\n3,0402 | 8,014\n2,9819 | 7,891\n"
                               "3,0934 | 8,207\n3,805 | 8,31\n5,423 | 8,45")
tabla = desde_texto_editado(tabla_txt)
if not tabla:
    st.info("Cargá al menos dos renglones de datos.")
    st.stop()
nombres, cols = columnas_numericas(tabla)
if len(cols) < 2:
    st.error("Se necesitan al menos dos columnas numéricas (revisá los separadores).")
    st.stop()

c1, c2 = st.columns(2)
ny = c1.selectbox("Variable a explicar (y)", nombres, index=len(nombres) - 1)
xs_nom = c2.multiselect("Variables explicativas (x)", [n for n in nombres if n != ny],
                        default=[n for n in nombres if n != ny][:1 if len(nombres) == 2 else None])
alpha = st.number_input("Riesgo α", min_value=0.001, max_value=0.5, value=0.05, step=0.01, format="%.4f")
y = cols[nombres.index(ny)]
xs = [cols[nombres.index(n)] for n in xs_nom]
if not xs:
    st.stop()


def fmt(v, d=4):
    return f"{v:,.{d}f}".replace(",", "_").replace(".", ",").replace("_", ".")


# ---------------------------------------------------------------- simple
if len(xs) == 1:
    x = xs[0]
    modelo = st.radio("Modelo", list(rg.TRANSFORMACIONES), horizontal=True,
                      format_func=lambda m: rg.TRANSFORMACIONES[m][2])
    origen = st.checkbox("Recta por el origen (b0 = 0)")
    try:
        reg = rg.ajustar_simple(x, y, modelo=modelo, origen=origen)
    except ValueError as e:
        st.error(str(e))
        st.stop()
    st.subheader("Recta de mínimos cuadrados")
    st.markdown(f"**{reg.ecuacion()}**".replace(".", ","))
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("b0", fmt(reg.b0))
    m2.metric("b1", fmt(reg.b1))
    m3.metric("r", fmt(reg.r))
    m4.metric("r²", fmt(reg.r2))
    st.caption(f"n = {reg.n}; S² = {fmt(reg.S2)}; S = {fmt(reg.S)}; Sb1 = {fmt(reg.Sb1)}; ν = {reg.nu}")

    st.subheader("Validación")
    e = rg.ensayo_beta1(reg, alpha, 0.0, "existencia")
    st.write(f"H0: β1 = 0 → tc = {fmt(e.t_c)}; t(1-α; {e.nu}) = {fmt(e.t_critico)} ⇒ "
             + ("**se rechaza H0: existe relación lineal**." if e.rechaza else "**no se rechaza H0**."))
    st.write(rg.validez_por_r2(reg.r2))

    st.subheader("Estimaciones")
    ic_b = rg.ic_beta1(reg, alpha)
    st.write(f"IC β1 ({fmt(100 * (1 - alpha), 1)}%): [{fmt(ic_b.A)} ; {fmt(ic_b.B)}]")
    if not origen and abs(reg.r) < 1:
        ic_r = rg.ic_rho(reg, alpha)
        st.write(f"IC ρ (Fisher): [{fmt(ic_r.A)} ; {fmt(ic_r.B)}] · IC ρ²: "
                 f"[{fmt(min(ic_r.A ** 2, ic_r.B ** 2) if ic_r.A * ic_r.B > 0 else 0)} ; {fmt(max(ic_r.A ** 2, ic_r.B ** 2))}]")

    st.subheader("Pronóstico")
    c1, c2, c3 = st.columns(3)
    x0 = c1.number_input("x₀ (en las unidades de la tabla)", value=float(sum(x) / len(x)), format="%.6f")
    que = c2.radio("Para", ["un valor individual (predicción)", "el promedio (ley promedio)"])
    cola = c3.radio("Límites", ["bilateral", "inferior", "superior"],
                    format_func=lambda c: {"bilateral": "A y B", "inferior": "mínimo", "superior": "máximo"}[c])
    f = rg.ic_prediccion if que.startswith("un valor") else rg.ic_media_y
    ic = f(reg, x0, alpha, cola)
    st.write(f"ŷ₀ = {fmt(reg.predecir(x0))}; error = {fmt(ic.error)}; límites: "
             f"{fmt(ic.A) if ic.A is not None else '—'} ; {fmt(ic.B) if ic.B is not None else '—'}"
             + (f" → escala original: {fmt(ic.A_orig) if ic.A_orig else '—'} ; {fmt(ic.B_orig) if ic.B_orig else '—'}"
                if ic.centro_orig is not None else ""))

    st.subheader("Ensayo sobre β1 contra un valor")
    c1, c2 = st.columns(2)
    b10 = c1.number_input("β1₀", value=0.0, format="%.6f")
    tail = c2.radio("H1", ["derecha", "izquierda", "bilateral"],
                    format_func=lambda t: {"derecha": "β1 > β1₀", "izquierda": "β1 < β1₀", "bilateral": "β1 ≠ β1₀"}[t])
    en = rg.ensayo_beta1(reg, alpha, b10, tail)
    st.write(f"H0: {en.h0} vs H1: {en.h1}; tc = {fmt(en.t_c)}; t crítico = {fmt(en.t_critico)}; b1 crítico = "
             + " ; ".join(fmt(v) for v in en.b_critico) + " ⇒ " + ("**se rechaza H0**" if en.rechaza else "**no se rechaza H0**"))

# ---------------------------------------------------------------- múltiple
else:
    try:
        reg = rg.ajustar_multiple(xs, y, xs_nom)
    except (ValueError, Exception) as e:  # noqa: BLE001
        st.error(f"No se pudo ajustar: {e}")
        st.stop()
    st.subheader("Modelo lineal general")
    st.markdown(f"**{reg.ecuacion()}**".replace(".", ","))
    g = rg.ensayo_global(reg, alpha)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("R²", fmt(reg.R2))
    m2.metric("R² ajustado", fmt(reg.R2aj))
    m3.metric("S²", fmt(reg.S2))
    m4.metric("F calculado", fmt(g.F_c))
    st.write(f"Análisis global: F = {fmt(g.F_c)} vs F(1-α; {g.nu1}; {g.nu2}) = {fmt(g.F_critico)} ⇒ "
             + ("**el modelo es globalmente adecuado**" if g.rechaza else "**el modelo no es globalmente adecuado**"))
    parc = rg.ensayos_parciales(reg, alpha)
    st.write(f"Análisis individual (|tc| > t(1-α; {reg.n - reg.p}) = {fmt(parc[0].t_critico)}):")
    st.dataframe(pd.DataFrame([{"Variable": e.nombre, "bi": e.b, "Cii": reg.C[i + 1], "Sbi": e.Sb, "tc": e.t_c,
                                "¿aporta?": "sí" if e.rechaza else "no"} for i, e in enumerate(parc)]), hide_index=True)
    st.write("Coeficientes de determinación parcial: " + "; ".join(
        f"{k}: {fmt(v)}" for k, v in rg.determinacion_parcial(xs, y, xs_nom).items()))
    st.subheader("Selección de modelos (análisis exploratorio)")
    cands = rg.seleccion_modelos(xs, y, xs_nom)
    st.dataframe(pd.DataFrame([{"Modelo": ", ".join(c.variables), "p": c.p, "R² aj": c.R2aj, "S²": c.S2,
                                "PRESS": c.PRESS, "DET": c.DET, "Cp": c.Cp, "Cp/p": c.Cp_p, "VIF máx": c.VIF_max,
                                "pasa DET y Cp": "sí" if c.cumple else "no"} for c in cands]), hide_index=True)
    mejor = rg.mejor_candidato(cands)
    st.write(f"Mejor candidato (DET > 0,1, Cp/p < 5, mayor R² ajustado, parsimonia): **{', '.join(mejor.variables)}** → "
             f"{mejor.reg.ecuacion()}".replace(".", ","))
