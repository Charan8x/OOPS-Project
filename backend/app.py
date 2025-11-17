from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os
import traceback
import yfinance as yf

app = Flask(__name__)
CORS(app)


def fetch_stock_json(symbol):
    data = yf.download(symbol, period="1y", interval="1d", progress=False)
    try:
        if hasattr(data.columns, "levels") and len(data.columns.levels) > 1:
            close_df = data.xs("Close", axis=1, level=0)
            close_series = close_df[symbol.upper()]
        else:
            close_series = data["Close"]
    except Exception as e:
        raise Exception(f"Error extracting close prices: {str(e)}")
    close_prices = close_series.dropna().tolist()
    if not close_prices:
        raise Exception(f"No close prices found for symbol: {symbol}")
    return {"close_prices": close_prices}


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    symbol = data.get("symbol", "").upper()
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400
    try:
        stock_json = fetch_stock_json(symbol)
        cpp_exe = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../cpp_core/main")
        )
        if os.name == "nt":
            cpp_exe += ".exe"
        if not os.path.isfile(cpp_exe):
            return (
                jsonify({"error": f"C++ executable not found at path: {cpp_exe}"}),
                500,
            )
        proc = subprocess.run(
            [cpp_exe],
            input=json.dumps(stock_json),
            text=True,
            capture_output=True,
            timeout=30,
        )
        if proc.returncode != 0:
            return (
                jsonify(
                    {
                        "error": "C++ error",
                        "details": proc.stderr,
                        "output": proc.stdout,
                    }
                ),
                500,
            )
        output = proc.stdout.strip()
        result = json.loads(output)
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/stock-info", methods=["POST"])
def stock_info():
    data = request.json
    symbol = data.get("symbol", "").upper()
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400
    try:
        stock_data = yf.download(symbol, period="6mo", interval="1d", progress=False)
        if stock_data.empty:
            return jsonify({"error": "No data found for symbol."}), 404
        if hasattr(stock_data.columns, "levels") and len(stock_data.columns.levels) > 1:
            close_df = stock_data.xs("Close", axis=1, level=0)
            close_series = close_df[symbol]
        else:
            close_series = stock_data["Close"]
        closes = close_series.dropna().tolist()
        dates = [str(date)[:10] for date in close_series.dropna().index]
        last_price = closes[-1] if closes else None
        return jsonify(
            {
                "symbol": symbol,
                "closes": closes,
                "dates": dates,
                "last_price": last_price,
            }
        )
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
