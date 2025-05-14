### fetcher.py
from binance.client import Client
import pandas as pd
import time
from config import API_KEY, API_SECRET, INTERVAL, CANDLE_LIMIT

client = Client(API_KEY, API_SECRET)

def fetch_ohlcv(symbol: str):
    try:
        klines = client.get_klines(symbol=symbol, interval=INTERVAL, limit=CANDLE_LIMIT)
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None