from datetime import datetime
from typing import Dict
from src.instrument.option import Option

class BSMPricer:
    def __init__(self, instrument: Option, as_of_date: datetime,
                 market_data: Dict[str, float]):
        self.instrument = instrument
        self.as_of_date = as_of_date
        # Get inputs for BSM model from market data
        self.spot_price = float(market_data["spot_price"]) or None
        self.volatility = float(market_data["volatility"]) or None
        self.risk_free_rate = float(market_data["risk_free_rate"]) or None
        self.dividend_yield = float(market_data["dividend_yield"]) or None

        self._input_data_check()

    def _input_data_check(self):
        if self.spot_price is None:
            raise ValueError("Spot price is required for BSM pricing.")
        if self.volatility is None:
            raise ValueError("Volatility is required for BSM pricing.")
        if self.risk_free_rate is None:
            raise ValueError("Risk-free rate is required for BSM pricing.")
        if self.instrument.is_expired(self.as_of_date):
            raise ValueError("Cannot price an expired option.")