import re

def clean_price(price_string):
    # Logic: Find number and dots only. Ignores '£' or '$'
    # Formulation:  "£22.65" -> "22.65" -> 22.65 (float)
    match = re.search(r"(\d+\.\d+)", price_string)
    return float(match.group(1)) if match else 0.0

def clean_stock(stock_string):
    # Logic: Find the digits inside the parentheses
    # Formulation: "In stock (19 available)" -> "19" -> 19 (int)
    match = re.search(r"(\d+)", stock_string)
    return int(match.group(1)) if match  else 0
