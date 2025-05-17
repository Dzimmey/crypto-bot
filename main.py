from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from executor import open_positions, execute_trade
from selector import get_top_symbols
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Zmień na domenę frontu na produkcji!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")

def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.api_route("/positions", methods=["GET", "OPTIONS"])
async def positions(request: Request):
    if request.method == "OPTIONS":
        return Response(status_code=200)
    verify_api_key(request)
    return open_positions

@app.api_route("/symbols", methods=["GET", "OPTIONS"])
async def symbols(request: Request):
    if request.method == "OPTIONS":
        return Response(status_code=200)
    verify_api_key(request)
    return get_top_symbols()

@app.post("/trade")
async def trade(request: Request):
    verify_api_key(request)
    body = await request.json()
    symbol = body.get("symbol")
    action = body.get("action")
    quantity = body.get("quantity")
    if not symbol or not action or quantity is None:
        raise HTTPException(status_code=400, detail="Missing data")
    try:
        execute_trade(symbol, action, float(quantity))
        return {"status": "success", "symbol": symbol, "action": action, "quantity": quantity}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trade failed: {str(e)}")

@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Trading Bot API"}

@app.get("/status")
def get_status():
    return {"status": "bot online"}
