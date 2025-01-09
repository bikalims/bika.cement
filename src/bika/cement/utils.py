# -*- coding: utf-8 -*-

def format_number(value, decimal_places=2):
    if value in (None, ""):
        return None
    
    if isinstance(value, int):
        return value  # Return as-is if it's an integer
    
    try:
        num = float(value)
        return num if num.is_integer() else round(num, decimal_places)
    except ValueError:
        return None  # Handle cases where conversion fails
