from binance.client import Client
import os

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TRADE_QUANTITY_USD = float(os.getenv("TRADE_QUANTITY_USD", 100))

client = Client(API_KEY, API_SECRET)
open_positions = []  # Zmieniamy na listę, żeby nie było błędu mapowania na froncie

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

        # Dodaj do listy open_positions (tu tylko prosty mock)
        if action == "BUY":
            open_positions.append({
                "symbol": symbol,
                "entryPrice": price,
                "quantity": quantity
            })
        elif action == "SELL":
            # Usuwamy pozycję po symbolu
            open_positions[:] = [pos for pos in open_positions if pos["symbol"] != symbol]
    except Exception as e:
        print(f"[ERROR] Trade failed: {e}")
