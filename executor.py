from binance.client import Client
import os

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TRADE_QUANTITY_USD = float(os.getenv("TRADE_QUANTITY_USD", 100))

client = Client(API_KEY, API_SECRET)
open_positions = []

def execute_trade(symbol: str, action: str, quantity: float = None):
    if action not in ["BUY", "SELL"]:
        return

    side = Client.SIDE_BUY if action == "BUY" else Client.SIDE_SELL
    try:
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        if quantity is None:
            quantity = round(TRADE_QUANTITY_USD / price, 6)
        else:
            quantity = float(quantity)

        print(f"[EXECUTOR] {action} {quantity} {symbol} @ {price}")
        client.create_order(
            symbol=symbol,
            side=side,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )

        if action == "BUY":
            open_positions[symbol] = price
        elif action == "SELL" and symbol in open_positions:
            del open_positions[symbol]
    except Exception as e:
        print(f"[ERROR] Trade failed: {e}")
