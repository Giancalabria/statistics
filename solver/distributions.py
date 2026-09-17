"""Wrappers finos sobre scipy.stats para las distribuciones del curso (Z, t, chi2, F).

Todas las funciones "_value" toman una probabilidad acumulada p y devuelven el
fractil correspondiente. Las variantes "_two_tailed" / "_one_tailed" hacen la
conversión desde alpha (nivel de riesgo), para no repetir esa cuenta en cada
módulo de solver.
"""

from scipy import stats


def z_value(p: float) -> float:
    return stats.norm.ppf(p)


def t_value(p: float, df: float) -> float:
    return stats.t.ppf(p, df)


def chi2_value(p: float, df: float) -> float:
    return stats.chi2.ppf(p, df)


def f_value(p: float, dfn: float, dfd: float) -> float:
    return stats.f.ppf(p, dfn, dfd)


def beta_value(p: float, a: float, b: float) -> float:
    return stats.beta.ppf(p, a, b)


def binom_cdf(k: int, n: int, p: float) -> float:
    """P(X <= k) para X ~ Binomial(n, p)."""
    return stats.binom.cdf(k, n, p)


def binom_upper_tail(k: int, n: int, p: float) -> float:
    """P(X >= k) para X ~ Binomial(n, p)."""
    return 1 - stats.binom.cdf(k - 1, n, p)


def norm_cdf(z: float) -> float:
    return stats.norm.cdf(z)


def chi2_cdf(x: float, df: float) -> float:
    """P(X <= x) para X ~ Chi2(df)."""
    return stats.chi2.cdf(x, df)


def z_two_tailed(alpha: float) -> float:
    return z_value(1 - alpha / 2)


def z_one_tailed(alpha: float) -> float:
    return z_value(1 - alpha)


def t_two_tailed(alpha: float, df: float) -> float:
    return t_value(1 - alpha / 2, df)


def t_one_tailed(alpha: float, df: float) -> float:
    return t_value(1 - alpha, df)


def chi2_lower(alpha: float, df: float) -> float:
    """Fractil chico (área alpha/2) — divide para el límite SUPERIOR del IC de varianza."""
    return chi2_value(alpha / 2, df)


def chi2_upper(alpha: float, df: float) -> float:
    """Fractil grande (área 1-alpha/2) — divide para el límite INFERIOR del IC de varianza."""
    return chi2_value(1 - alpha / 2, df)


def chi2_one_tailed(alpha: float, df: float) -> float:
    return chi2_value(1 - alpha, df)


def f_two_tailed(alpha: float, dfn: float, dfd: float) -> float:
    return f_value(1 - alpha / 2, dfn, dfd)


def f_one_tailed(alpha: float, dfn: float, dfd: float) -> float:
    return f_value(1 - alpha, dfn, dfd)


def fpc(N: float, n: float) -> float:
    """Factor de corrección por finitud: sqrt((N-n)/(N-1))."""
    return ((N - n) / (N - 1)) ** 0.5
