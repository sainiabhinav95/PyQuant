from typing import Dict, Any
from datetime import datetime
from logging import Logger
from python_quant.instrument.option import Option

def risk_mode_option_handler(
    instrument: Dict[str, Any],
    as_of_date: datetime,
    market_data: Dict[str, Any],
    logger: Logger,
):
    option = Option(
        strike_price=float(instrument["strike"]),
        expiration_date= datetime.strptime(
            instrument["expiry"], "%Y%m%d"
        ),
        market_price=instrument["market_price"],
        underlying_ticker=instrument["underlying"]["symbol"],
        underlying_type=instrument["underlying"]["type"],
        call_put=Option.CallPut.CALL
        if instrument["option_type"].upper() == "CALL"
        else Option.CallPut.PUT,
        option_type=Option.OptionType.EUROPEAN
    )
    style = instrument.get("style") or ""



    match style.upper():
        case "EUROPEAN":
            logger.info("Processing EUROPEAN option in RISK mode.")
            logger.info(f"Using BSM Pricer for option: {option}")
            from python_quant.pricers.bsm_pricer import BSMPricer
            pricer = BSMPricer(
                instrument=option,
                as_of_date=as_of_date,
                market_data=market_data[as_of_date.strftime("%Y%m%d")],
                logger=logger
            )
            return pricer.greeks()
            
        case _:
            raise NotImplementedError(
                f"RISK mode not implemented for option style: {style}"
            )