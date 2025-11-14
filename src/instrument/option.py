from datetime import datetime
from enum import Enum
from typing import Optional, Dict
from src.conventions.day_count import DayCount

class Option:
    class OptionType(Enum):
        AMERICAN = "American"
        EUROPEAN = "European"
        BERMUDAN = "Bermudan"
    class CallPut(Enum):
        CALL = "call"
        PUT = "put"
    def __init__(self, strike_price: float, expiration_date: datetime,
                  option_type: OptionType = OptionType.EUROPEAN,
                  call_put: CallPut = CallPut.CALL,
                  *, conventions: Optional[Dict[str,str]] = {"day_count_convention": "ACT/365"}):
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.option_type = option_type
        self.call_put = call_put

        if conventions:
            self.day_count_convention = DayCount(
                convention=conventions.get(
                    "day_count_convention", "ACT/365"
                )
            )
    def __repr__(self):
        return f"EquityOption(strike_price={self.strike_price}, \
        expiration_date={self.expiration_date}, \
        option_type='{self.option_type}'), call_put='{self.call_put}'"
    
    def is_expired(self, current_date: datetime) -> bool:
        return current_date > self.expiration_date
    
    
    