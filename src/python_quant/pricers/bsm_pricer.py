import numpy as np
from datetime import datetime
from typing import Dict
from scipy.stats import norm
from python_quant.instrument.option import Option
from logging import Logger
from scipy.optimize import brentq

class BSMPricer:
    def __init__(self, instrument: Option, as_of_date: datetime,
                 market_data: Dict[str, float], logger: Logger):
        self.logger = logger
        self.instrument = instrument
        self.as_of_date = as_of_date

        # Get inputs for BSM model from market data
        ticker_data = market_data[self.instrument.underlying['symbol']]
        if isinstance(ticker_data, dict):
            self.spot_price = ticker_data["spot_price"]
        else:
            self.spot_price = ticker_data
            
        self.volatility = instrument.volatility
        self.risk_free_rate = float(market_data["risk_free_rate"])
        self.dividend_yield = float(market_data["dividend_yield"])
        self.market_price = self.instrument.market_price

        self._input_data_check()

    def _input_data_check(self):
        if self.spot_price is None:
            raise ValueError("Spot price is required for BSM pricing.")
        if self.volatility == 0.0 and self.market_price is None:
            raise ValueError(
                "Either volatility or market price is required for BSM pricing."
                )
        if self.risk_free_rate is None:
            raise ValueError("Risk-free rate is required for BSM pricing.")
        if self.instrument.is_expired(self.as_of_date):
            raise ValueError("Cannot price an expired option.")
        
        # Calculate some important variables first
        self.time_to_maturity = self.instrument.time_to_maturity(self.as_of_date)
        self.cp_flag = 1.0 if self.instrument.call_put \
            == Option.CallPut.CALL else -1.0      

        self.logger.info(f"""
                         Initializing BSM Pricer with the following parameters:
                         Spot Price: {self.spot_price}
                         Volatility: {self.volatility}
                         Strike Price: {self.instrument.strike_price}
                         Risk-Free Rate: {self.risk_free_rate}
                         Dividend Yield: {self.dividend_yield}
                         Market Price: {self.market_price}
                         Time to Maturity: {self.time_to_maturity}   
                         Call/Put Flag: {
                             "CALL" if self.cp_flag==1.0 else "PUT"
                             }                        
                         """)
        
        if self.market_price is not None:
            self.logger.info("Calculating implied volatility from market price.")
            self.volatility = self._volatility_from_market_price(
                    S_o=self.spot_price,
                    K=self.instrument.strike_price,
                    r=self.risk_free_rate,
                    d=self.dividend_yield,
                    t=self.time_to_maturity,
                    market_price=self.market_price,
                    cp_flag=self.cp_flag
                )
        else:
            self.logger.info(f"Using provided volatility: {self.volatility}")
            self.market_price = self.price()
        
        
    def _bsm_price_from_vol(self, S_o: float, K: float,
                            r: float, d: float, t: float,
                            sigma: float, cp_flag: float) -> float:
        d1 = ((np.log(S_o/K) + (r - d + 0.5 * sigma **2) * t) / (sigma * np.sqrt (t)))
        d2 = d1 - sigma * np.sqrt(t)
        opt_price = cp_flag*S_o * (
            np.exp(-d*t)*
            norm.cdf(cp_flag*d1)
          ) - cp_flag* K * np.exp(-r*t) * norm.cdf(cp_flag*d2) # type: ignore
        self.logger.debug(f"BSM_PRICE_FROM_VOL: D1={d1}, D2={d2}, Price={opt_price}")
        self.d1, self.d2 = d1, d2
        return opt_price
    
    def _volatility_from_market_price(self, S_o: float, K: float,
                                    r: float, d: float, t: float,
                                    market_price: float,
                                    cp_flag: float,
                                    tol: float = 1e-6,
                                    max_iterations: int = 100) -> float:
        def objective_function(vol):
            price = self._bsm_price_from_vol(S_o, K, r, d, t, vol, cp_flag)
            error = price - market_price
            self.logger.debug(f"Error using vol={vol}: {error}")
            return error
        
        implied_vol = brentq(objective_function, 1e-8, 1.0, 
                             xtol=tol, maxiter=max_iterations)
        self.logger.info(
            f"Implied Volatility calculated from market price: {implied_vol}"
            )
        return float(implied_vol) # pyright: ignore[reportArgumentType]
        
    
    def price(self) -> float:
        if self.market_price is not None:
            self.logger.info(
                f"Using market price for option pricing: {self.market_price}"
                )
            return self.market_price
        else:
            option_price = self._bsm_price_from_vol(
                S_o=self.spot_price,
                K=self.instrument.strike_price,
                r=self.risk_free_rate,
                d=self.dividend_yield,
                t=self.time_to_maturity,
                sigma=self.volatility,
                cp_flag=self.cp_flag
            )
            return option_price
    def greeks(self) -> Dict[str, float]:
        option_price = self.market_price or self.price()
        delta = self.cp_flag * np.exp(
            -self.dividend_yield * self.time_to_maturity
            ) * norm.cdf(self.cp_flag * self.d1)  # type: ignore
        gamma = (np.exp(
            -self.dividend_yield * self.time_to_maturity
            ) * norm.pdf(self.d1)) / (
                self.spot_price * self.volatility * np.sqrt(self.time_to_maturity)
                )  # type: ignore
        theta = (- (self.spot_price * self.volatility * np.exp(
                    -self.dividend_yield * self.time_to_maturity
                    ) * norm.pdf(self.d1)) / (2 * np.sqrt(self.time_to_maturity))  # type: ignore
                 - self.cp_flag * self.risk_free_rate * self.instrument.strike_price \
                    * np.exp(
                        -self.risk_free_rate * self.time_to_maturity
                        ) * norm.cdf(self.cp_flag * self.d2)  # type: ignore
                 + self.cp_flag * self.dividend_yield * self.spot_price * np.exp(
                     -self.dividend_yield * self.time_to_maturity
                     ) * norm.cdf(self.cp_flag * self.d1))  # type: ignore
        rho = self.cp_flag * self.instrument.strike_price \
            * self.time_to_maturity * np.exp(
                -self.risk_free_rate * self.time_to_maturity
                ) * norm.cdf(self.cp_flag * self.d2)  # type: ignore
        vega = self.spot_price * np.exp(
            -self.dividend_yield * self.time_to_maturity
            ) * norm.pdf(self.d1) * np.sqrt(self.time_to_maturity)  # type: ignore

        greeks = {
            "price": option_price,
            "implied_volatility": self.volatility,
            "delta": delta,
            "gamma": gamma,
            "theta": theta,
            "rho": rho,
            "vega": vega
        }
        self.logger.info(f"Calculated Greeks: {greeks}")
        return greeks
    

        
        

        