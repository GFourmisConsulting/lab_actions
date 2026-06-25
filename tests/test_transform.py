"""Tests unitarios para src.transform.clean_data."""

import pandas as pd
import pytest

from src.transform import clean_data


@pytest.fixture()
def sample_df() -> pd.DataFrame:
    """DataFrame de prueba con filas válidas e inválidas."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "producto": ["Laptop", "Monitor", "Teclado", "Mouse"],
            "monto": [1200.00, 350.50, 89.99, -50.00],
        }
    )


def test_clean_data_removes_non_positive_amounts(sample_df: pd.DataFrame) -> None:
    """clean_data debe eliminar filas con monto <= 0."""
    result = clean_data(sample_df)
    assert (result["monto"] > 0).all(), "Existen montos no positivos en el resultado."
    assert len(result) == 3, f"Se esperaban 3 filas, se obtuvieron {len(result)}."


def test_clean_data_output_columns(sample_df: pd.DataFrame) -> None:
    """clean_data debe preservar las columnas originales del DataFrame."""
    result = clean_data(sample_df)
    expected_columns = {"id", "producto", "monto"}
    assert expected_columns.issubset(
        set(result.columns)
    ), f"Columnas faltantes: {expected_columns - set(result.columns)}"


def test_clean_data_resets_index(sample_df: pd.DataFrame) -> None:
    """El índice del DataFrame resultante debe comenzar en 0 sin gaps."""
    result = clean_data(sample_df)
    assert list(result.index) == list(
        range(len(result))
    ), "El índice no fue reseteado correctamente."


def test_clean_data_raises_on_missing_column() -> None:
    """clean_data debe lanzar ValueError si falta la columna 'monto'."""
    df_bad = pd.DataFrame({"id": [1], "producto": ["X"]})
    with pytest.raises(ValueError, match="monto"):
        clean_data(df_bad)


def test_clean_data_monto_is_float(sample_df: pd.DataFrame) -> None:
    """La columna 'monto' del resultado debe ser de tipo float."""
    result = clean_data(sample_df)
    assert result["monto"].dtype == float, "La columna 'monto' no es de tipo float."