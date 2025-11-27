from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from python_quant.conventions.day_count import DayCount


class Option:
    class OptionType(Enum):
        AMERICAN = "American"
        EUROPEAN = "European"
        BERMUDAN = "Bermudan"

    class CallPut(Enum):
        CALL = "call"
        PUT = "put"

    def __init__(
        self,
        strike_price: float,
        expiration_date: datetime,
        underlying_ticker: str,
        underlying_type: str,
        market_price: float | None,
        volatility: float,
        option_type: OptionType = OptionType.EUROPEAN,
        call_put: CallPut = CallPut.CALL,
        *,
        conventions: Optional[Dict[str, str]] = None,
    ) -> None:
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.option_type = option_type
        self.call_put = call_put
        self.underlying = {"symbol": underlying_ticker, "type": underlying_type}
        self.market_price = market_price or None
        self.volatility = volatility

        if conventions:
            self.day_count_convention = DayCount(
                convention=conventions.get("day_count_convention", "ACT/365")
            )
        else:
            self.day_count_convention = DayCount(convention="ACT/365")

    def __repr__(self) -> str:
        return f"EquityOption(strike_price={self.strike_price}, \
        expiration_date={self.expiration_date}, \
        option_type='{self.option_type}'), call_put='{self.call_put}', \
        underlying_ticker='{self.underlying['symbol']}', \
        underlying_type='{self.underlying['type']}', \
        market_price={self.market_price}, volatility={self.volatility})"

    def is_expired(self, current_date: datetime) -> bool:
        return current_date > self.expiration_date

    def time_to_maturity(self, as_of_date: datetime) -> float:
        if self.is_expired(as_of_date):
            return 0.0
        return self.day_count_convention.year_fraction(
            start_date=as_of_date, end_date=self.expiration_date
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strike_price": self.strike_price,
            "expiration_date": self.expiration_date.strftime("%Y-%m-%d"),
            "option_type": self.option_type.value,
            "call_put": self.call_put.value,
            "underlying_ticker": self.underlying.get("symbol"),
            "underlying_type": self.underlying.get("type"),
            "market_price": self.market_price,
            "volatility": self.volatility,
            "day_count_convention": self.day_count_convention.convention,
        }
