import requests

import requests

def get_last_trade_price(pair):
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={pair}"
    response = requests.get(url)
    
    # Print the response for debugging
    print(f"requesting https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={pair}")
    print(f"KuCoin API Response: {response.status_code}, {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        if data and 'data' in data and 'price' in data['data']:
            return float(data['data']['price'])
        else:
            raise Exception(f"Invalid KuCoin API response: {data}")
    else:
        raise Exception(f"KuCoin API error: {response.status_code}, {response.text}")

def get_available_pairs():
    url = "https://api.kucoin.com/api/v1/symbols"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [symbol['symbol'] for symbol in data['data']]
    else:
        raise Exception(f"KuCoin API error: {response.status_code}")