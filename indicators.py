import pandas as pd
import ta
from config import RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=RSI_PERIOD).rsi()

    macd = ta.trend.MACD(
        close=df['close'],
        window_fast=MACD_FAST,
        window_slow=MACD_SLOW,
        window_sign=MACD_SIGNAL
    )
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    return df