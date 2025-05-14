import time
import requests

API_URL = "https://crypto-trading-bot-5ecx.onrender.com/status"
PING_INTERVAL_SECONDS = 300  # co 5 minut

def ping():
    try:
        response = requests.get(API_URL)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Status: {response.status_code}")
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Błąd: {e}")

if __name__ == "__main__":
    print(f"Start pingowania {API_URL} co {PING_INTERVAL_SECONDS} sekundy...")
    while True:
        ping()
        time.sleep(PING_INTERVAL_SECONDS)
