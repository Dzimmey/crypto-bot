from config import RSI_BUY_THRESHOLD, RSI_SELL_THRESHOLD

def decide(df):
    last = df.iloc[-1]
    if last['rsi'] < RSI_BUY_THRESHOLD and last['macd'] > last['macd_signal']:
        return "BUY"
    elif last['rsi'] > RSI_SELL_THRESHOLD and last['macd'] < last['macd_signal']:
        return "SELL"
    return "HOLD"