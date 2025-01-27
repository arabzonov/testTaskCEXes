import requests

def get_last_trade_price(pair):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return float(data['price'])
    else:
        raise Exception(f"Binance API error: {response.status_code}")

def get_available_pairs():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [symbol['symbol'] for symbol in data['symbols']]
    else:
        raise Exception(f"Binance API error: {response.status_code}")