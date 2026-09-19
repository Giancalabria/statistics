"""Redacción formal de resultados, tal como la pide la cátedra (ver §5 del esquema).

No alcanza con mostrar el número: se acompaña con la notación
P(A ≤ parámetro ≤ B) = 1-α o la frase de decisión correspondiente.
"""

from typing import Optional

from .intervals import IntervalResult, SampleSizeResult
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

    # Decidir si se rechaza o no
    if result.rejects_h0:
        decision = "se RECHAZA"
    else:
        decision = "NO se rechaza"

    alpha_pct = alpha * 100
    texto = (
        f"De acuerdo a la evidencia muestral ({obs_str}), al nivel de significación "
        f"del {alpha_pct:g}%, {decision} la hipótesis nula: {result.h0_text}."
    )

    return texto


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
    alpha_pct = alpha * 100

    # Decidir si se rechaza o no
    if result.rejects_h0:
        decision = "se RECHAZA"
    else:
        decision = "NO se rechaza"

    texto = (
        f"De acuerdo al estadístico de prueba χ² = {result.chi2_calc:.5f} "
        f"(valor crítico: {result.chi2_critico:.5f}, gl = {result.df}), "
        f"al nivel de significación del {alpha_pct:g}%, {decision} "
        f"la hipótesis nula de que {contexto}."
    )

    return texto
