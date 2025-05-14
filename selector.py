### selector.py
from binance.client import Client
from config import API_KEY, API_SECRET, TOP_SYMBOLS_LIMIT

client = Client(API_KEY, API_SECRET)

def get_top_symbols(quote_asset="USDC"):
    try:
        tickers = client.get_ticker_24hr()
        filtered = [t for t in tickers if t['symbol'].endswith(quote_asset)]
        sorted_by_volume = sorted(filtered, key=lambda x: float(x['quoteVolume']), reverse=True)
        top = [s['symbol'] for s in sorted_by_volume[:TOP_SYMBOLS_LIMIT]]
        return top
    except Exception as e:
        print(f"[SELECTOR ERROR] {e}")
        return []