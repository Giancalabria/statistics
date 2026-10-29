"""Criterio de aproximación de la binomial que exige el profesor (Ing. Dopazo, clases del 10/09, 17/09 y 24/09).

Las aproximaciones (normal o Poisson) solo sirven para calcular n: la estimación de p y el valor crítico del
ensayo son siempre exactos (binomial). Y la aproximación elegida se justifica con el n RESULTANTE, no con el
inicial: «siempre el criterio de aproximación se aplica al valor de n que vos calculaste, el n final».

- Normal si n·p > 10 y n·(1 − p) > 10.
- Poisson si p ≤ 0,005.
- Si se cumplen las dos o ninguna, criterio de Mermoz:
  n₀ = 0,23·(1 − p)²/p³ si p ≤ 0,5 (0,23·p²/(1 − p)³ si p ≥ 0,5); si n > n₀, normal; si no, Poisson.

«No me usen otro criterio porque está mal»: nada de n ≥ 30 ni n·p ≥ 5.
En un ensayo o un plan de muestreo se verifica con p₀ (la proporción de H0).
"""

from dataclasses import dataclass


def fmt(v: float, d: int = 4) -> str:
    """Número con hasta d decimales y coma decimal (sin ceros de más)."""
    t = f"{v:.{d}f}".rstrip("0").rstrip(".")
    return t.replace(".", ",")


@dataclass
class CriterioAproximacion:
    n: int
    p: float
    np: float
    nq: float
    normal_ok: bool          # n·p > 10 y n·(1-p) > 10
    poisson_ok: bool         # p ≤ 0,005
    n0: float = None         # n₀ de Mermoz (solo si hizo falta)
    elegida: str = ""        # "normal" | "poisson"
    texto: str = ""


def n0_mermoz(p: float) -> float:
    """n₀ del criterio de Mermoz."""
    if p <= 0.5:
        return 0.23 * (1 - p) ** 2 / p ** 3
    return 0.23 * p ** 2 / (1 - p) ** 3


def criterio_aproximacion(n: int, p: float) -> CriterioAproximacion:
    """Qué aproximación de la binomial corresponde con este n (el resultante) y esta p, según el profesor."""
    if not (0 < p < 1):
        raise ValueError(f"p debe estar entre 0 y 1, no {p}")
    np_, nq = n * p, n * (1 - p)
    normal_ok = np_ > 10 and nq > 10
    poisson_ok = p <= 0.005
    c = CriterioAproximacion(n=int(n), p=p, np=np_, nq=nq, normal_ok=normal_ok, poisson_ok=poisson_ok)
    cond_n = (f"n·p = {n}·{fmt(p, 4)} = {fmt(np_, 4)} y n·(1 − p) = {fmt(nq, 4)} "
              f"({'los dos > 10' if normal_ok else 'no son los dos > 10'})")
    cond_p = f"p = {fmt(p, 4)} {'≤' if poisson_ok else '>'} 0,005"
    if normal_ok != poisson_ok:
        c.elegida = "normal" if normal_ok else "poisson"
        c.texto = (f"Criterio de aproximación con el n resultante: {cond_n}; {cond_p} → "
                   f"{'aproximación normal' if normal_ok else 'aproximación de Poisson'}.")
        return c
    c.n0 = n0_mermoz(p)
    formula = "0,23·(1 − p)²/p³" if p <= 0.5 else "0,23·p²/(1 − p)³"
    c.elegida = "normal" if n > c.n0 else "poisson"
    c.texto = (f"Criterio de aproximación con el n resultante: {cond_n}; {cond_p} → "
               f"{'se cumplen las dos' if normal_ok else 'no se cumple ninguna'}, así que decide el criterio de Mermoz: n₀ = {formula} = "
               f"{fmt(c.n0, 2)}; n = {n} {'>' if n > c.n0 else '≤'} n₀ → "
               f"{'aproximación normal' if c.elegida == 'normal' else 'aproximación de Poisson'}.")
    return c
