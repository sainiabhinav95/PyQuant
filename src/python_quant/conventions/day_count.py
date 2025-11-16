from datetime import datetime
class DayCount:
    """A class representing day count conventions for financial calculations."""
    
    def __init__(self, convention: str):
        self.convention = convention.upper()
    
    def year_fraction(self, start_date: datetime, end_date: datetime) -> float:
        """Calculate the year fraction between two dates based on the convention."""
        match self.convention:
            case "30/360":
                return self._year_fraction_30_360(start_date, end_date)
            case "ACT/360":
                return self._year_fraction_act_360(start_date, end_date)
            case "ACT/365":
                return self._year_fraction_act_365(start_date, end_date)
            case _:
                raise ValueError(f"Unsupported day count convention: {self.convention}")
    def _year_fraction_30_360(self, start_date: datetime, end_date: datetime) -> float:
        d1 = start_date.day
        d2 = end_date.day
        m1 = start_date.month
        m2 = end_date.month
        y1 = start_date.year
        y2 = end_date.year
        
        if d1 == 31:
            d1 = 30
        if d2 == 31 and d1 == 30:
            d2 = 30
        
        return ((360 * (y2 - y1)) + (30 * (m2 - m1)) + (d2 - d1)) / 360.0
    
    def _year_fraction_act_360(self, start_date: datetime, end_date: datetime) -> float:
        delta = end_date - start_date
        return delta.days / 360.0
    
    def _year_fraction_act_365(self, start_date: datetime, end_date: datetime) -> float:
        delta = end_date - start_date
        return delta.days / 365.0