#!/usr/bin/env -S uv run --active

from argparse import ArgumentParser
from typing import Any, Dict, Union
from pathlib import Path
from python_quant.utils.json import json_file_to_dict
from python_quant.mode_handler.risk_mode import risk_mode_main

def print_intro_message():
    intro_message = """
    ========================================
            Welcome to PyQuant
    A Comprehensive Quant Finance Library
    ========================================
           Created by Abhinav Saini
         Licensed under the MIT License
    """
    print(intro_message)
    

def risk_mode(instrument: Dict[str, Any], as_of_date: str,
               verbose: str, json_path: Union[str, Path]):
    
    risk_mode_main(
        instrument=instrument,
        as_of_date=as_of_date,
        verbose=verbose,
        json_path=json_path
    )

def price_mode(instrument: Dict[str, Any], as_of_date: str,
                verbose: str):
    pass

def simulate_mode(simulate: Dict[str, Any], as_of_date:str, verbose: str):
    pass

def main():
    parser = ArgumentParser(description="PyQuant Main Execution Script")
    parser.add_argument(
        "--mode",
        help="Mode [PRICE, RISK, SIMULATE]"
    )
    parser.add_argument(
        "--instrument",
        help="Instrument for PRICE/RISK mode to be passed as a JSON file",
    )
    parser.add_argument(
        "--simulate",
        help="Simulation parameters for SIMULATE mode",
    )
    parser.add_argument(
        "--as_of_date",
        help="As of date for pricing/risk calculations"
    )
    parser.add_argument(
        "--verbose",
        help="Logging (I for INFO, D for DEBUG) enabled if set to True",
    )
    parser.add_argument(
        "--input_data_path",
        help="Path for input market data JSON files",
    )

    args = parser.parse_args()
    instrument_data = json_file_to_dict(args.instrument) if args.instrument else {}

    print_intro_message()

    print(f"Logging Level: {'INFO' if args.verbose=='I' else 'DEBUG' if args.verbose=='D' else 'DISABLED'}")

    if args.mode == "PRICE":
        price_mode(
            instrument=instrument_data,
            as_of_date=args.as_of_date,
            verbose=args.verbose,
        )
    elif args.mode == "RISK":
        risk_mode(
            instrument=instrument_data,
            as_of_date=args.as_of_date,
            verbose=args.verbose,
            json_path=args.input_data_path
        )
    elif args.mode == "SIMULATE":
        simulate_mode(
            simulate=args.simulate,
            verbose=args.verbose,
            as_of_date=args.as_of_date,
        )
    else:
        print("Invalid mode selected. Please choose PRICE, RISK, or SIMULATE.")
    

if __name__ == "__main__":
    main()
