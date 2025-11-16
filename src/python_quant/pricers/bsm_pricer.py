import numpy as np
from datetime import datetime
from typing import Dict, Union
from scipy.stats import norm
from python_quant.instrument.option import Option
from logging import Logger
from scipy.optimize import newton

class BSMPricer:
    def __init__(self, instrument: Option, as_of_date: datetime,
                 market_data: Dict[str, Union[dict, float]], logger: Logger):
        self.logger = logger
        self.instrument = instrument
        self.as_of_date = as_of_date

        # Get inputs for BSM model from market data
        ticker_data = market_data[self.instrument.underlying['symbol']]
        if isinstance(ticker_data, dict):
            self.spot_price = ticker_data["spot_price"]
        else:
            self.spot_price = ticker_data
            
        self.volatility = market_data.get("volatility", 0.0)
        self.risk_free_rate = market_data["risk_free_rate"]
        self.dividend_yield = market_data["dividend_yield"]
        self.market_price = self.instrument.market_price

        self._input_data_check()

    def _input_data_check(self):
        if self.spot_price is None:
            raise ValueError("Spot price is required for BSM pricing.")
        if self.volatility == 0.0 and self.market_price is None:
            raise ValueError("Either volatility or market price is required for BSM pricing.")
        if self.risk_free_rate is None:
            raise ValueError("Risk-free rate is required for BSM pricing.")
        if self.instrument.is_expired(self.as_of_date):
            raise ValueError("Cannot price an expired option.")
        
        # Calculate some important variables first
        self.time_to_maturity = self.instrument.time_to_maturity(self.as_of_date)
        self.cp_flag = 1.0 if self.instrument.call_put == Option.CallPut.CALL else -1.0      

        self.logger.info(f"""
                         Initializing BSM Pricer with the following parameters:
                         Spot Price: {self.spot_price}
                         Volatility: {self.volatility}
                         Strike Price: {self.instrument.strike_price}
                         Risk-Free Rate: {self.risk_free_rate}
                         Dividend Yield: {self.dividend_yield}
                         Market Price: {self.market_price}
                         Time to Maturity: {self.time_to_maturity}   
                         Call/Put Flag: {self.cp_flag}                        
                         """)
        
        if self.volatility == 0.0 and self.market_price is not None:
            self.volatility = self._volatility_from_market_price(
                    S_o=self.spot_price,
                    K=self.instrument.strike_price,
                    r=self.risk_free_rate,
                    d=self.dividend_yield,
                    t=self.time_to_maturity,
                    market_price=self.market_price,
                    cp_flag=self.cp_flag
                )
        
        
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
                                    max_iterations: int = 10) -> float:
        sigma = 0.2  # initial guess
        def objective_function(vol):
            if vol <= 0:
                return 1000000  # Return a large difference if vol is non-positive
            self.logger.debug(f"Calculating objective function with vol={vol}")
            price = self._bsm_price_from_vol(S_o, K, r, d, t, vol, cp_flag)
            return price - market_price
        
        implied_vol = newton(objective_function,
                             sigma,
                             tol=tol, maxiter=max_iterations)
        self.logger.info(f"Implied Volatility calculated from market price: {implied_vol}")
        return implied_vol
        
    
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
        option_price = self.price()
        delta = self.cp_flag * np.exp(-self.dividend_yield * self.time_to_maturity) * norm.cdf(self.cp_flag * self.d1)  # type: ignore
        gamma = (np.exp(-self.dividend_yield * self.time_to_maturity) * norm.pdf(self.d1)) / (self.spot_price * self.volatility * np.sqrt(self.time_to_maturity))  # type: ignore
        theta = (- (self.spot_price * self.volatility * np.exp(-self.dividend_yield * self.time_to_maturity) * norm.pdf(self.d1)) / (2 * np.sqrt(self.time_to_maturity))  # type: ignore
                 - self.cp_flag * self.risk_free_rate * self.instrument.strike_price * np.exp(-self.risk_free_rate * self.time_to_maturity) * norm.cdf(self.cp_flag * self.d2)  # type: ignore
                 + self.cp_flag * self.dividend_yield * self.spot_price * np.exp(-self.dividend_yield * self.time_to_maturity) * norm.cdf(self.cp_flag * self.d1))  # type: ignore
        rho = self.cp_flag * self.instrument.strike_price * self.time_to_maturity * np.exp(-self.risk_free_rate * self.time_to_maturity) * norm.cdf(self.cp_flag * self.d2)  # type: ignore
        vega = self.spot_price * np.exp(-self.dividend_yield * self.time_to_maturity) * norm.pdf(self.d1) * np.sqrt(self.time_to_maturity)  # type: ignore

        greeks = {
            "price": option_price,
            "delta": delta,
            "gamma": gamma,
            "theta": theta,
            "rho": rho,
            "vega": vega
        }
        self.logger.info(f"Calculated Greeks: {greeks}")
        return greeks
    

        
        

        