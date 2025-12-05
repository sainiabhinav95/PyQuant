#!/usr/bin/env -S uv run --active

from argparse import ArgumentParser
from typing import Any, Dict, Union
from pathlib import Path
from python_quant.utils.json import json_file_to_dict
from python_quant.mode_handler.risk_mode import risk_mode_main
from python_quant.app.app_main import WebApp
import os
import sys


def print_intro_message() -> None:
    intro_message = """
    ========================================
            Welcome to PyQuant
    A Comprehensive Quant Finance Library
    ========================================
           Created by Abhinav Saini
         Licensed under the MIT License
    """
    print(intro_message)


def start_app(debug: bool = False) -> None:
    webapp = WebApp()
    webapp.run()
    sys.exit(0)


def risk_mode(
    instrument: Dict[str, Any],
    as_of_date: str,
    verbose: str,
    json_path: Union[str, Path],
    write_csv: bool,
    csv_path: str,
) -> None:
    risk_mode_main(
        instrument=instrument,
        as_of_date=as_of_date,
        verbose=verbose,
        json_path=json_path,
        write_csv=write_csv,
        csv_path=csv_path,
    )


def price_mode(
    instrument: Dict[str, Any],
    as_of_date: str,
    verbose: str,
    write_csv: bool,
    csv_path: str,
) -> None:
    pass


def calibrate_mode(
    calibrate: Dict[str, Any],
    as_of_date: str,
    verbose: str,
    write_csv: bool,
    csv_path: str,
) -> None:
    pass


def main():
    dir_path = os.getcwd()
    parser = ArgumentParser(description="PyQuant Main Execution Script")
    parser.add_argument(
        "--web_app", help="Run the Dash web application", action="store_true"
    )

    parser.add_argument("--mode", help="Mode [PRICE, RISK, CALIBRATE]")
    parser.add_argument(
        "--instrument",
        help="Instrument for PRICE/RISK mode to be passed as a JSON file",
    )
    parser.add_argument(
        "--calibrate",
        help="Simulation parameters for calibrate mode",
    )
    parser.add_argument("--as_of_date", help="As of date for pricing/risk calculations")
    parser.add_argument(
        "--verbose", help="Logging (I for INFO, D for DEBUG) enabled if set to True"
    )
    parser.add_argument(
        "--input_data_path",
        help="Path for input market data JSON files",
    )
    parser.add_argument(
        "--write_csv",
        help="Enable writing output to CSV if set to True",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--csv_path",
        help="Path for input market data JSON files",
        default=os.path.join(dir_path, "output.csv"),
    )

    args = parser.parse_args()

    instrument_data = json_file_to_dict(args.instrument) if args.instrument else {}

    print_intro_message()

    logging_levels = {"I": "INFO", "D": "DEBUG"}
    logging_level = logging_levels.get(args.verbose, "DISABLED")
    print(f"\tLogging Level: {logging_level}")

    if args.web_app:
        start_app(debug=(logging_level == "DEBUG"))

    print(f"\tWrite CSV: {args.write_csv}")
    if args.write_csv:
        print(f"\tCSV Path: {args.csv_path}")

    if args.mode == "PRICE":
        price_mode(
            instrument=instrument_data,
            as_of_date=args.as_of_date,
            verbose=args.verbose,
            write_csv=args.write_csv,
            csv_path=args.csv_path,
        )
    elif args.mode == "RISK":
        risk_mode(
            instrument=instrument_data,
            as_of_date=args.as_of_date,
            verbose=args.verbose,
            json_path=args.input_data_path,
            write_csv=args.write_csv,
            csv_path=args.csv_path,
        )
    elif args.mode == "CALIBRATE":
        calibrate_mode(
            calibrate=args.calibrate,
            verbose=args.verbose,
            as_of_date=args.as_of_date,
            write_csv=args.write_csv,
            csv_path=args.csv_path,
        )
    else:
        print("Invalid mode selected. Please choose PRICE, RISK, or CALIBRATE.")


if __name__ == "__main__":
    main()
