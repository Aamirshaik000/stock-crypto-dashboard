
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import pandas as pd

API_KEY = "AC3KN1S09U2EBH1R" 

# Initialize Alpha Vantage objects
ts = TimeSeries(key=API_KEY, output_format='pandas')
cc = CryptoCurrencies(key=API_KEY, output_format='pandas')

# -----------------------------
# Fetch Stocks
# -----------------------------
stocks = ["AAPL", "TSLA", "AMZN"]

for symbol in stocks:
    data, meta = ts.get_daily(symbol=symbol, outputsize="full")
    data = data.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    data.to_csv(f"data/{symbol}.csv")
    print(f"Saved stock data: {symbol}.csv")

# -----------------------------
# Fetch Cryptos
# -----------------------------
cryptos = ["BTC", "ETH"]
market = "USD"

for symbol in cryptos:
    data, meta = cc.get_digital_currency_daily(symbol=symbol, market=market)
    data = data.rename(columns={
        "1a. open (USD)": "Open",
        "2a. high (USD)": "High",
        "3a. low (USD)": "Low",
        "4a. close (USD)": "Close",
        "5. volume": "Volume",
        "6. market cap (USD)": "Market Cap"
    })
    data.to_csv(f"data/{symbol}-{market}.csv")
    print(f"Saved crypto data: {symbol}-{market}.csv")
