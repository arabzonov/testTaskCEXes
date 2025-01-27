from flask import Flask, request, jsonify
from exchanges.binance import get_last_trade_price as binance_price
from exchanges.kucoin import get_last_trade_price as kucoin_price
from utils import get_pair

app = Flask(__name__)

@app.route('/estimate', methods=['GET'])
def estimate():
    input_amount = float(request.args.get('inputAmount'))
    input_currency = request.args.get('inputCurrency')
    output_currency = request.args.get('outputCurrency')

    # Get the correct pair format for each exchange
    binance_pair = get_pair(input_currency, output_currency, exchange="binance")
    kucoin_pair = get_pair(input_currency, output_currency, exchange="kucoin")

    try:
        binance_rate = binance_price(binance_pair)
    except Exception as e:
        return jsonify({"error": f"Binance API error: {str(e)}"}), 500

    try:
        kucoin_rate = kucoin_price(kucoin_pair)
    except Exception as e:
        return jsonify({"error": f"KuCoin API error: {str(e)}"}), 500

    if binance_rate > kucoin_rate:
        exchange_name = 'binance'
        output_amount = input_amount * binance_rate
    else:
        exchange_name = 'kucoin'
        output_amount = input_amount * kucoin_rate

    return jsonify({
        'exchangeName': exchange_name,
        'outputAmount': output_amount
    })

@app.route('/getRates', methods=['GET'])
def get_rates():
    base_currency = request.args.get('baseCurrency')
    quote_currency = request.args.get('quoteCurrency')

    # Get the correct pair format for each exchange
    binance_pair = get_pair(base_currency, quote_currency, exchange="binance")
    kucoin_pair = get_pair(base_currency, quote_currency, exchange="kucoin")

    rates = []

    try:
        binance_rate = binance_price(binance_pair)
        rates.append({
            'exchangeName': 'binance',
            'rate': binance_rate
        })
    except Exception as e:
        print(f"Binance error: {e}")

    try:
        kucoin_rate = kucoin_price(kucoin_pair)
        rates.append({
            'exchangeName': 'kucoin',
            'rate': kucoin_rate
        })
    except Exception as e:
        print(f"KuCoin error: {e}")

    return jsonify(rates)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)