### main.py
import time
from fetcher import fetch_ohlcv
from indicators import add_indicators
from strategy import decide
from executor import execute_trade
from selector import get_top_symbols

TRADE_SYMBOLS = get_top_symbols()  # inicjalizacja
last_selection_time = time.time()

if __name__ == "__main__":
    print("Crypto Trading Bot Started")

    while True:
        now = time.time()
        if now - last_selection_time > 3600:  # co godzinę
            TRADE_SYMBOLS = get_top_symbols()
            last_selection_time = now
            print(f"[SELECTOR] Updated trading symbols: {TRADE_SYMBOLS}")

        for symbol in TRADE_SYMBOLS:
            df = fetch_ohlcv(symbol)
            if df is not None:
                df = add_indicators(df)
                action = decide(df)
                print(f"{symbol}: RSI={df['rsi'].iloc[-1]:.2f}, MACD={df['macd'].iloc[-1]:.4f} → Action: {action}")
                execute_trade(symbol, action)

        time.sleep(300)