from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from executor import open_positions
from selector import get_top_symbols
from dotenv import load_dotenv
import os

# --- Load .env variables ---
load_dotenv()

# --- API Init ---
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
    return get_top_symbols()
