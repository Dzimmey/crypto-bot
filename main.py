from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from executor import open_positions
from selector import get_top_symbols
import os

app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lub ["https://crypto-bot-seven-psi.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Key Security ---
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

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

@app.get("/positions")
def get_open_positions(dep: None = Depends(verify_api_key)):
    return open_positions

@app.get("/symbols")
def get_symbols(dep: None = Depends(verify_api_key)):
    return get_top_symbols()
