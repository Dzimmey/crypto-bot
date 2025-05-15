from fastapi import FastAPI, HTTPException, Request, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from executor import open_positions
from selector import get_top_symbols
import os

app = FastAPI()

# --- CORS ---
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

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# --- Routes ---
@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Trading Bot API"}

@app.get("/status")
def get_status():
    return {"status": "bot online"}

@app.api_route("/positions", methods=["GET", "OPTIONS"])
def get_open_positions(request: Request, api_key: str = Depends(api_key_header)):
    if request.method == "OPTIONS":
        # Odpowiedź preflight (przeglądarka CORS)
        return Response(status_code=200)
    # Sprawdzenie API Key przy GET (ale nie przy OPTIONS!)
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return open_positions

@app.get("/symbols", dependencies=[Depends(verify_api_key)])
def get_symbols():
    return get_top_symbols()
