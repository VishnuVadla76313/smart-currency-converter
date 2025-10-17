# converter.py
import math

def convert_amount(amount, rate_from, rate_to):
    """
    Convert amount given rates relative to same base.
    If rates are direct to base, conversion factor = rate_to / rate_from
    """
    if amount < 0:
        raise ValueError("Amount must be non-negative")
    factor = rate_to / rate_from
    result = amount * factor
    # round sensibly to 2 decimal places for currency
    return round(result, 2)