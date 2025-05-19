from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import APIKeyHeader
from executor import open_positions, execute_trade
from selector import get_top_symbols
import os

app = FastAPI()

# --- API Key Security ---
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# --- Routes ---
@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Trading Bot API"}

@app.get("/status")
def get_status():
    return {"status": "bot online"}

@app.get("/positions", dependencies=[Depends(verify_api_key)])
def get_open_positions():
    return open_positions

@app.get("/symbols", dependencies=[Depends(verify_api_key)])
def get_symbols():
    return get_top_symbols

@app.post("/trade", dependencies=[Depends(verify_api_key)])
async def trade(request: Request):
    body = await request.json()
    symbol = body.get("symbol")
    action = body.get("action")
    quantity = body.get("quantity")
    if not symbol or not action or not quantity:
        raise HTTPException(status_code=400, detail="Missing data")
    try:
        execute_trade(symbol, action, float(quantity))
        return {"status": "success", "symbol": symbol, "action": action, "quantity": quantity}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trade failed: {str(e)}")

@app.options("/trade")
async def options_trade():
    return {"status": "ok"}
