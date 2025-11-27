import polars as pl
from pathlib import Path
from typing import Dict, Any


def write_output_to_csv(data: Dict[str, Any], csv_path: str) -> None:
    """
    Write the given data to a CSV file.
    Format of data:
     {
        "instrument_details": { ... },
        "risk_metrics": { ... }
     }

    Args:
        data (Dict[str, Any]): The data to write to CSV.
        csv_path (str): The path to the CSV file.
    """
    instrument_details = data.get("instrument_details") or {}
    risk_metrics = data.get("risk_metrics") or {}
    # Combine both dictionaries for CSV output
    combined_data = {**instrument_details, **risk_metrics}
    df = pl.DataFrame([combined_data])
    csv_file = Path(csv_path)
    csv_file.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(csv_file)


def read_csv_to_df(csv_path: str) -> pl.DataFrame:
    """
    Read a CSV file into a Polars DataFrame.

    Args:
        csv_path (str): The path to the CSV file.

    Returns:
        pl.DataFrame: The DataFrame containing the CSV data.
    """
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found at path: {csv_path}")
    df = pl.read_csv(csv_file)
    return df
