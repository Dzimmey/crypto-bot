# auto_trader.py
"""
Automatyczny loop tradingowy: cyklicznie pobiera dane, liczy wskaźniki, podejmuje decyzje i wykonuje zlecenia.
"""
import time
from fetcher import fetch_ohlcv
from indicators import add_indicators
from strategy import decide
from selector import get_top_symbols
from executor import execute_trade, open_positions
import os

INTERVAL_SECONDS = int(os.getenv("AUTO_TRADE_INTERVAL", 300))  # domyślnie 5 minut
QUOTE_ASSET = os.getenv("QUOTE_ASSET", "USDT")


def auto_trading_loop():
    print("[AUTO-TRADER] Start loopu automatycznego tradingu...")
    while True:
        try:
            symbols = get_top_symbols(quote_asset=QUOTE_ASSET)
            print(f"[AUTO-TRADER] Top symbols: {symbols}")
            for symbol in symbols:
                df = fetch_ohlcv(symbol)
                if df is None or len(df) < 10:
                    print(f"[AUTO-TRADER] Brak danych dla {symbol}")
                    continue
                df = add_indicators(df)
                action = decide(df)
                print(f"[AUTO-TRADER] {symbol}: decyzja={action}")
                if action in ("BUY", "SELL"):
                    # Sprawdź czy już jest otwarta pozycja
                    already_open = any(pos["symbol"] == symbol for pos in open_positions)
                    if action == "BUY" and not already_open:
                        execute_trade(symbol, "BUY")
                    elif action == "SELL" and already_open:
                        execute_trade(symbol, "SELL")
            print(f"[AUTO-TRADER] Sleep {INTERVAL_SECONDS}s...")
            time.sleep(INTERVAL_SECONDS)
        except Exception as e:
            print(f"[AUTO-TRADER ERROR] {e}")
            time.sleep(30)

if __name__ == "__main__":
    auto_trading_loop()
