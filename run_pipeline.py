"""Pipeline ETL de ventas: lee, limpia y exporta datos de ventas."""

import argparse
import sys
from pathlib import Path

import pandas as pd

from src.transform import clean_data


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parsea los argumentos de línea de comandos.

    Args:
        argv: Lista de argumentos. Si es None, usa sys.argv.

    Returns:
        Namespace con los atributos 'input' y 'output'.
    """
    parser = argparse.ArgumentParser(
        description="ETL pipeline: limpia el dataset de ventas."
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Ruta al CSV de entrada (ej: data/ventas.csv).",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Ruta al CSV de salida (ej: output/ventas_limpias.csv).",
    )
    return parser.parse_args(argv)


def run(input_path: Path, output_path: Path) -> None:
    """Ejecuta el pipeline completo: carga → transforma → exporta.

    Args:
        input_path: Path al archivo CSV de entrada.
        output_path: Path al archivo CSV de salida.

    Raises:
        FileNotFoundError: Si el archivo de entrada no existe.
        ValueError: Si el CSV no contiene la columna 'monto'.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Archivo de entrada no encontrado: {input_path}")

    # Garantizar existencia de directorios de salida
    output_path.parent.mkdir(parents=True, exist_ok=True)
    Path("reports").mkdir(parents=True, exist_ok=True)

    df_raw = pd.read_csv(input_path)
    df_clean = clean_data(df_raw)

    df_clean.to_csv(output_path, index=False)

    print(f"[OK] ETL completado: {len(df_clean)} registros → {output_path}")


def main() -> None:
    """Entry point del pipeline ETL."""
    args = parse_args()
    try:
        run(args.input, args.output)
    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()