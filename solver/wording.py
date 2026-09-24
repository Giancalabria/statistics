"""Redacción formal de resultados, tal como la pide la cátedra (ver §5 del esquema).

No alcanza con mostrar el número: se acompaña con la notación
P(A ≤ parámetro ≤ B) = 1-α o la frase de decisión correspondiente.
"""

from typing import Optional

from .intervals import IntervalResult, SampleSizeResult, VarianceSampleSizeResult
from .hypothesis_one import HypothesisTestResult
from .chi_square import ChiSquareResult


DECIMALES = 5


def fmt_num(value, decimals: int = DECIMALES) -> str:
    """Formatea un valor numérico (o una tupla de valores) con `decimals` decimales."""
    if isinstance(value, (tuple, list)):
        return ", ".join(fmt_num(v, decimals) for v in value)
    if isinstance(value, float):
        return f"{value:.{decimals}f}"
    return str(value)


def texto_intervalo(parametro: str, result: IntervalResult, confianza: float) -> str:
    conf_pct = confianza * 100
    return (
        f"Con un nivel de confianza del {conf_pct:g}%, "
        f"P({result.a:.5f} ≤ {parametro} ≤ {result.b:.5f}) = {confianza:.4g}."
    )


def texto_tamano_muestra(n_result: SampleSizeResult, n_preliminar: Optional[int] = None) -> str:
    if n_result.reduccion is not None:
        texto = (
            f"Para reducir un {n_result.reduccion * 100:g}% el error (de e = "
            f"{n_result.e_actual:.5f} a e = {n_result.e_nuevo:.5f}), "
            f"el tamaño de muestra necesario es n = {n_result.n}."
        )
    else:
        texto = f"El tamaño de muestra necesario es n = {n_result.n}."
    if n_result.iterations > 1:
        texto += (
            f" Calculado con el método iterativo en {n_result.iterations} iteración(es) "
            f"(valores intermedios de n: {n_result.converged_values})."
        )
    if n_preliminar is not None and n_preliminar > 0:
        delta = max(0, n_result.n - n_preliminar)
        texto += (
            f" Como ya se relevaron n_preliminar = {n_preliminar} unidades, "
            f"hay que tomar Δn = {n_result.n} - {n_preliminar} = {delta} unidades adicionales."
        )
    return texto


def texto_tamano_muestra_varianza(
    result: VarianceSampleSizeResult, n_preliminar: Optional[int] = None
) -> str:
    """Redacción del n para σ²/σ obtenido por relación entre límites (García)."""
    if result.reduccion is not None and result.r_sigma_actual is not None:
        texto = (
            f"Para reducir un {result.reduccion * 100:g}% la relación entre límites "
            f"(de R' = {result.r_sigma_actual:.4f} a R' = {result.r_sigma_objetivo:.4f}), "
            f"el tamaño de muestra necesario es n = {result.n}."
        )
    else:
        texto = (
            f"Para lograr una relación entre límites R' = {result.r_sigma_objetivo:.4f}, "
            f"el tamaño de muestra necesario es n = {result.n}."
        )
    texto += f" (Ecuación de García: a = {result.a:.4f}, ν = {result.nu:.2f}.)"
    if n_preliminar is not None and n_preliminar > 0:
        delta = max(0, result.n - n_preliminar)
        texto += (
            f" Como ya se relevaron n_preliminar = {n_preliminar} unidades, "
            f"hay que tomar Δn = {result.n} - {n_preliminar} = {delta} unidades adicionales."
        )
    return texto


def conclusion_formal(alpha: float, rechaza: bool, h0: str, h1: str, obs: str,
                      si_rechaza: Optional[str] = None, si_no_rechaza: Optional[str] = None) -> str:
    """Conclusión formal (paso 7 de la cátedra): arranca con el nivel de significación,
    dice si hay evidencia para rechazar H0 y cierra con la acción que se sigue.

    Nunca dice "se acepta H0": no rechazarla no equivale a probarla.
    """
    pct = f"{alpha * 100:g}"
    if rechaza:
        accion = si_rechaza or f"se da por probado que {h1}"
        return (f"A un nivel de significación del {pct}%, existe evidencia estadística suficiente para rechazar "
                f"la hipótesis nula {h0} ({obs} cae en la zona de rechazo). Por consiguiente, {accion}.")
    accion = si_no_rechaza or (f"no se puede afirmar que {h1}: se mantiene H0 "
                               f"(no rechazarla no equivale a probarla)")
    return (f"A un nivel de significación del {pct}%, no existe evidencia estadística suficiente para rechazar "
            f"la hipótesis nula {h0} ({obs} no cae en la zona de rechazo). Por consiguiente, {accion}.")


def texto_ensayo(result, alpha: float) -> str:
    """Redacción formal de un ensayo de hipótesis, siguiendo §5 del esquema.

    Nunca dice "se acepta H0", solo "se rechaza" o "no se rechaza".
    """
    # Obtener el valor observado con formato apropiado
    if result.distribution == "Binomial (exacto)":
        obs_str = f"r = {int(result.observed_value)}"
    elif "chi2" in result.distribution:
        obs_str = f"S² = {result.observed_value:.5f}"
    elif result.distribution == "F":
        obs_str = f"j² = {result.observed_value:.5f}"
    else:  # media (Z o t) o diferencia
        obs_str = f"x̄ = {result.observed_value:.5f}"

    return conclusion_formal(alpha, result.rejects_h0, f"H0: {result.h0_text}", result.h1_text, obs_str)


def texto_chi_cuadrado(result: ChiSquareResult, contexto: str, alpha: float) -> str:
    """Redacción formal de un contraste chi-cuadrado.

    Args:
        result: ChiSquareResult del cálculo.
        contexto: Frase corta describiendo qué se está probando.
                  Ej. "los datos siguen el modelo propuesto" o "las variables son independientes".
        alpha: Nivel de significación.

    Returns:
        Texto formal siguiendo las convenciones de redacción.
    """
    obs = f"χ² = {result.chi2_calc:.5f} [χ²c = {result.chi2_critico:.5f}; ν = {result.df}]"
    return conclusion_formal(alpha, result.rejects_h0, f"de que {contexto}", f"no es cierto que {contexto}", obs)
