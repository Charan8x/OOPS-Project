import yfinance as yf


def fetch_stock_json(symbol):
    data = yf.download(symbol, period="1y", interval="1d", progress=False)

    # Debug print the data structure:
    print(data.head())

    # Extract 'Close' column safely
    if "Close" not in data.columns:
        raise Exception(f"No 'Close' column in downloaded data for symbol: {symbol}")

    close_series = data["Close"]

    if close_series.empty:
        raise Exception(f"'Close' data is empty for symbol: {symbol}")

    close_prices = close_series.dropna().tolist()

    if not close_prices:
        raise Exception(
            f"No close prices found after dropping NaNs for symbol: {symbol}"
        )

    return {"close_prices": close_prices}
