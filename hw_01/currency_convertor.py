currencies = {
    "usd": {"eur": 0.85, "rub": 75, "cny": 6.45, "kzt": 430},
    "eur": {"usd": 1.18, "rub": 88.24, "cny": 7.59, "kzt": 505.88},
    "rub": {"usd": 0.013, "eur": 0.011, "cny": 0.086, "kzt": 5.73},
    "cny": {"usd": 0.155, "eur": 0.132, "rub": 11.63, "kzt": 66.67},
    "kzt": {"usd": 0.0023, "eur": 0.00198, "rub": 0.175, "cny": 0.015}
}


def get_amount_convert_currency(from_currency: str, to_currency: str, amount: float, commission: float):
    from_currency = from_currency.lower()
    to_currency = to_currency.lower()

    if from_currency not in currencies or to_currency not in currencies:
        raise ValueError

    from_currency_data = currencies[from_currency]
    return amount * from_currency_data[to_currency] / (commission+1)
