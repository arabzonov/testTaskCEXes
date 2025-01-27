def get_pair(base_currency, quote_currency, exchange):
    """
    Formats the trading pair based on the exchange.
    - KuCoin uses a hyphen (e.g., BTC-USDT).
    - Binance uses no separator (e.g., BTCUSDT).
    """
    if exchange == "kucoin":
        return f"{base_currency}-{quote_currency}"
    elif exchange == "binance":
        return f"{base_currency}{quote_currency}"
    else:
        raise ValueError(f"Unsupported exchange: {exchange}")
    
def get_exchange_rates(base_currency, quote_currency):
    from .exchanges.binance import get_last_trade_price as binance_price
    from .exchanges.kucoin import get_last_trade_price as kucoin_price

    pair = get_pair(base_currency, quote_currency)
    rates = []

    try:
        rates.append({
            'exchangeName': 'binance',
            'rate': binance_price(pair)
        })
    except Exception as e:
        print(f"Binance error: {e}")

    try:
        rates.append({
            'exchangeName': 'kucoin',
            'rate': kucoin_price(pair)
        })
    except Exception as e:
        print(f"KuCoin error: {e}")

    return rates