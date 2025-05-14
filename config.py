### config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

BASE_URL = "https://api.binance.com"

TRADE_SYMBOLS = ["BTCUSDT", "ETHUSDT"]  # zostanie nadpisane dynamicznie co godzinę
TRADE_QUANTITY_USD = 50

RSI_PERIOD = 14
RSI_BUY_THRESHOLD = 30
RSI_SELL_THRESHOLD = 70

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

INTERVAL = "1h"
CANDLE_LIMIT = 100
TOP_SYMBOLS_LIMIT = 5

SL_PCT = 0.05
TP_PCT = 0.10