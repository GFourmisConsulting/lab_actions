"""Módulo de transformación para el pipeline ETL de ventas."""
 
import pandas as pd
 
 
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y valida el DataFrame de ventas.
 
    Elimina filas con monto <= 0, normaliza tipos y resetea el índice.
 
    Args:
        df: DataFrame crudo con al menos las columnas ['id', 'producto', 'monto'].
 
    Returns:
        DataFrame limpio con índice reseteado y montos positivos garantizados.
 
    Raises:
        ValueError: Si el DataFrame no contiene la columna 'monto'.
    """
    if "monto" not in df.columns:
        raise ValueError("El DataFrame debe contener la columna 'monto'.")
 
    df_clean = df[df["monto"] > 0].copy()
    df_clean["monto"] = df_clean["monto"].astype(float)
    df_clean = df_clean.reset_index(drop=True)
    return df_clean
 