"""M4 — Contrastes chi-cuadrado (bondad de ajuste, tablas de contingencia).

Implementa §4 del esquema_teorico_examen_estadistica.md:
- Bondad de ajuste: recibe frecuencias observadas y esperadas ya calculadas.
- Tablas de contingencia: calcula frecuencias esperadas automáticamente.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from . import distributions as dist


@dataclass
class ChiSquareResult:
    """Resultado de un contraste chi-cuadrado."""
    chi2_calc: float
    df: int
    chi2_critico: float
    rejects_h0: bool
    warnings: List[str] = field(default_factory=list)
    expected_table: Optional[List[List[float]]] = None  # solo para tabla_contingencia


def bondad_de_ajuste(
    observados: List[float], esperados: List[float], p: int, alpha: float
) -> ChiSquareResult:
    """Bondad de ajuste chi-cuadrado.

    Args:
        observados: Lista de frecuencias observadas (F_o_i).
        esperados: Lista de frecuencias esperadas (F_e_i), ya calculadas por el usuario.
        p: Cantidad de parámetros estimados de la muestra (para cálculo de nu = k - 1 - p).
        alpha: Nivel de significación.

    Returns:
        ChiSquareResult con chi2_calc, grados de libertad, crítico, decisión y warnings.
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    warnings = []

    # Validaciones
    if len(observados) != len(esperados):
        raise ValueError(
            f"Observados y esperados deben tener la misma longitud. "
            f"Observados: {len(observados)}, Esperados: {len(esperados)}"
        )

    if len(observados) == 0:
        raise ValueError("No se pueden procesar listas vacías.")

    k = len(observados)

    # Validación de Fe_i >= 5 (avisar si hay celdas con Fe_i < 5)
    celdas_bajas = []
    for i, fe in enumerate(esperados):
        if fe < 5:
            celdas_bajas.append((i, fe))

    if celdas_bajas:
        indices_str = ", ".join(str(i) for i, _ in celdas_bajas)
        valores_str = ", ".join(f"{fe:.5f}" for _, fe in celdas_bajas)
        warnings.append(
            f"Celdas con F_e_i < 5 detectadas en posición(es) {indices_str} "
            f"(valores: {valores_str}). Se recomienda agrupar estas categorías "
            f"con adyacentes antes de recalcular."
        )

    # Validación de N_total >= 60
    n_total_obs = sum(observados)
    if n_total_obs < 60:
        warnings.append(
            f"Tamaño de muestra total N = {n_total_obs:.0f} < 60. "
            f"El test puede no ser robusto. Se recomienda aumentar la muestra."
        )

    # Cálculo del estadístico chi2
    chi2_calc = 0.0
    for fo, fe in zip(observados, esperados):
        chi2_calc += (fo - fe) ** 2 / fe

    # Grados de libertad: nu = k - 1 - p
    df = k - 1 - p

    if df <= 0:
        raise ValueError(
            f"Grados de libertad no válidos: nu = {k} - 1 - {p} = {df}. "
            f"Verificar cantidad de parámetros estimados (p)."
        )

    # Valor crítico
    chi2_critico = dist.chi2_one_tailed(alpha, df)

    # Decisión: se rechaza si chi2_calc > chi2_critico
    rejects = chi2_calc > chi2_critico

    return ChiSquareResult(
        chi2_calc=chi2_calc,
        df=df,
        chi2_critico=chi2_critico,
        rejects_h0=rejects,
        warnings=warnings,
    )


def tabla_contingencia(tabla_observada: List[List[float]], alpha: float) -> ChiSquareResult:
    """Tabla de contingencia (prueba de independencia/homogeneidad).

    Args:
        tabla_observada: Matriz de frecuencias observadas (lista de listas).
                         Ejemplo: [[35, 37], [165, 263], [300, 500]] para tabla 3x2.
        alpha: Nivel de significación.

    Returns:
        ChiSquareResult con chi2_calc, grados de libertad, crítico, decisión, warnings y tabla esperada.
    """
    if not (0 < alpha < 1):
        raise ValueError(f"alpha debe estar entre 0 y 1, no {alpha}")
    warnings = []

    if not tabla_observada or not tabla_observada[0]:
        raise ValueError("La tabla no puede estar vacía.")

    R = len(tabla_observada)  # número de filas
    C = len(tabla_observada[0])  # número de columnas

    # Verificar que todas las filas tengan el mismo número de columnas
    for i, fila in enumerate(tabla_observada):
        if len(fila) != C:
            raise ValueError(
                f"Fila {i} tiene {len(fila)} columnas, pero se esperaban {C}. "
                f"La tabla debe ser rectangular."
            )

    # Calcular totales de fila y columna
    totales_fila = [sum(fila) for fila in tabla_observada]
    totales_columna = [sum(tabla_observada[i][j] for i in range(R)) for j in range(C)]
    total_general = sum(totales_fila)

    if total_general < 60:
        warnings.append(
            f"Tamaño de muestra total N = {total_general:.0f} < 60. "
            f"El test puede no ser robusto. Se recomienda aumentar la muestra."
        )

    # Calcular frecuencias esperadas y chi2
    tabla_esperada = []
    chi2_calc = 0.0
    celdas_bajas = []

    for i in range(R):
        fila_esperada = []
        for j in range(C):
            e_ij = (totales_fila[i] * totales_columna[j]) / total_general
            fila_esperada.append(e_ij)

            # Validación de E_ij >= 5
            if e_ij < 5:
                celdas_bajas.append((i, j, e_ij))

            # Acumular chi2
            o_ij = tabla_observada[i][j]
            chi2_calc += (o_ij - e_ij) ** 2 / e_ij

        tabla_esperada.append(fila_esperada)

    if celdas_bajas:
        indices_str = ", ".join(f"({i},{j})" for i, j, _ in celdas_bajas)
        valores_str = ", ".join(f"{e:.5f}" for _, _, e in celdas_bajas)
        warnings.append(
            f"Celdas con E_ij < 5 detectadas en posición(es) {indices_str} "
            f"(valores: {valores_str}). Se recomienda agrupar filas o columnas "
            f"antes de recalcular."
        )

    # Grados de libertad: nu = (R - 1) * (C - 1)
    df = (R - 1) * (C - 1)

    # Valor crítico
    chi2_critico = dist.chi2_one_tailed(alpha, df)

    # Decisión: se rechaza si chi2_calc > chi2_critico
    rejects = chi2_calc > chi2_critico

    return ChiSquareResult(
        chi2_calc=chi2_calc,
        df=df,
        chi2_critico=chi2_critico,
        rejects_h0=rejects,
        warnings=warnings,
        expected_table=tabla_esperada,
    )
