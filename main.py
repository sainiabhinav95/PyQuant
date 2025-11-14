#!/usr/bin/env -S uv run --active

from argparse import ArgumentParser

def print_intro_message():
    intro_message = """
    ========================================
            Welcome to PyQuant
    A Comprehensive Quant Finance Library
    ========================================
        Copyright (c) 2025 Abhinav Saini
         Licensed under the MIT License
    """
    print(intro_message)

def risk_mode(instrument: str, as_of_date: str, verbose: bool):
    print(f"""Running RISK mode with instrument: {instrument}, as_of_date: {as_of_date}, Logging: {verbose}""")

def price_mode(instrument: str, as_of_date: str,
                verbose: bool):
    print(f"""Running PRICE mode with instrument: {instrument}, as_of_date: {as_of_date}, Logging: {verbose}""")

def simulate_mode(simulate: str, verbose: bool):
    print(f"""Running SIMULATE mode to simulate: {simulate}, Logging: {verbose}""")

if __name__ == "__main__":
    parser = ArgumentParser(description="PyQuant Main Execution Script")
    parser.add_argument(
        "--mode",
        help="Mode [PRICE, RISK, SIMULATE]"
    )
    parser.add_argument(
        "--instrument",
        help="Instrument input string for PRICE/RISK mode",
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
        action="store_true",
        help="Logging",
    )

    args = parser.parse_args()

    print_intro_message()

    if args.mode == "PRICE":
        price_mode(
            instrument=args.instrument,
            as_of_date=args.as_of_date,
            verbose=args.verbose,
        )
    elif args.mode == "RISK":
        risk_mode(
            instrument=args.instrument,
            as_of_date=args.as_of_date,
            verbose=args.verbose,
        )
    elif args.mode == "SIMULATE":
        simulate_mode(
            simulate=args.simulate,
            verbose=args.verbose,
        )
    else:
        print("Invalid mode selected. Please choose PRICE, RISK, or SIMULATE.")
    
