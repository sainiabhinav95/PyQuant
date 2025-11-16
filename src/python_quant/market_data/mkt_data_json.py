from python_quant.utils.json import json_file_to_dict
from datetime import datetime
from logging import Logger as logger
from typing import Union
from pathlib import Path

def json_market_data_loader(analysis_date: datetime, logger: logger,
                            json_path: Union[Path, str]) -> dict:
    """
    Load market data from a JSON file and return as a dictionary.

    Args:
        analysis_date (datetime): The date for which market data is to be loaded.
    Returns:
        dict: Market data as a dictionary.
    """
    date_str = analysis_date.strftime("%Y%m%d")
    file_path = Path(json_path) / f"{date_str}.json"
    logger.info(f"Loading market data from {file_path}")

    market_data = json_file_to_dict(file_path)
    logger.info("Market data successfully loaded.")
    logger.info(f"Market Data: {market_data}")
    return market_data