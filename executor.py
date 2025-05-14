### executor.py
from binance.client import Client
from config import API_KEY, API_SECRET, TRADE_QUANTITY_USD

client = Client(API_KEY, API_SECRET)

def execute_trade(symbol: str, action: str):
    if action not in ["BUY", "SELL"]:
        return

    side = Client.SIDE_BUY if action == "BUY" else Client.SIDE_SELL
    try:
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        quantity = round(TRADE_QUANTITY_USD / price, 6)  # 6 miejsc dla USDT par

        print(f"[EXECUTOR] {action} {quantity} {symbol} @ {price}")
        # Tu można aktywować zlecenie:
         client.create_order(
             symbol=symbol,
             side=side,
             type=Client.ORDER_TYPE_MARKET,
             quantity=quantity
         )
    except Exception as e:
        print(f"[ERROR] Trade failed: {e}")