from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from executor import open_positions
from selector import get_top_symbols
import os

app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lub wpisz konkretniejszy: ["https://crypto-bot-seven-psi.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")

def check_api_key(request: Request):
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# --- Routes ---
@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Trading Bot API"}

@app.get("/status")
def get_status():
    return {"status": "bot online"}

@app.options("/positions")
def options_positions():
    return Response(status_code=204)

@app.get("/positions")
def get_open_positions(request: Request):
    check_api_key(request)
    return open_positions

@app.options("/symbols")
def options_symbols():
    return Response(status_code=204)

@app.get("/symbols")
def get_symbols(request: Request):
    check_api_key(request)
    return get_top_symbols()
