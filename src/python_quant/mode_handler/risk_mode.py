from logging import getLogger, INFO, basicConfig, DEBUG
from typing import Dict, Any, Union
from pathlib import Path
from datetime import datetime
from python_quant.market_data.mkt_data_json import json_market_data_loader
from python_quant.mode_handler.option.risk_mode_option_handler \
    import risk_mode_option_handler

def pretty_print_output(instrument: Dict[str, Any],
                         risk: Dict[str, Any], indent: int = 4):
    # Indent for better readability
    print("\t================================")
    print("\tRISK MODE OUTPUT")
    print("\t================================")
    print("\tInstrument Details\n")
    for key, value in instrument.items():
        print(f"\t{key}: {value}")
    print("\t================================")
    print("\tCalculated Risk Metrics\n")
    for key, value in risk.items():
        print(f"\t{key}: {value}")
    print("\t================================")


def risk_mode_main(instrument: Dict[str, Any], as_of_date: str,
                    verbose: str, json_path: Union[str, Path]):
    intro_message = """
    ========================================
            WELCOME TO PYQUANT RISK MODE
    ========================================
    """
    print(intro_message)
    logger = getLogger("pyquant.risk_mode")
    basicConfig(level=INFO)
    analysis_date = datetime.strptime(as_of_date, "%Y%m%d")

    match verbose and verbose.upper():
        case "I":
            logger.setLevel(INFO)
        case "D":
            logger.setLevel(DEBUG)
        case _:
            logger.disabled = True

    logger.info(f"Starting RISK mode as of date: {analysis_date}")


    logger.info(f"Getting Market Data for RISK mode as_of_date: {analysis_date}")
    market_data = json_market_data_loader(
        analysis_date=analysis_date,
        logger=logger,
        json_path=json_path
    ).get(as_of_date, {})
    logger.info(f"Instrument details:\n{instrument}")

    instrument_type = str(instrument.get("type"))

    match instrument_type.upper():
        case "OPTION":
            risk = risk_mode_option_handler(
                instrument=instrument,
                as_of_date=analysis_date,
                market_data=market_data,
                logger=logger,
            )
            pretty_print_output(instrument, risk)
        case _:
            raise NotImplementedError(
                f"RISK mode not implemented for instrument type: {
                    instrument.get('type')
                    }"
            )



    
