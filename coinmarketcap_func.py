import requests
from config import COINMARKETCAP_API_KEY


def get_crypto_prices(symbols):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY
    }
    params = {
        "symbol": ",".join(symbols)
    }
    response = requests.get(url, headers=headers, params=params)
    token_details = response.json()["data"]
    prices = {}
    for symbol in symbols:
        try:
            price = token_details[symbol]["quote"]["USD"]["price"]
            prices[symbol] = price
        except KeyError:
            continue
    return prices
