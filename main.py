from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from executor import open_positions
from selector import get_top_symbols
import os

app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Na produkcji: ['https://crypto-bot-git-master-dzimmeys-projects.vercel.app']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Key Security ---
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# --- Routes ---
@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Trading Bot API"}

@app.get("/status")
def get_status():
    return {"status": "bot online"}

@app.api_route("/positions", methods=["GET", "OPTIONS"])
def get_open_positions(request: Request, api_key: str = None):
    if request.method == "OPTIONS":
        # Preflight request (CORS) – nie wymaga autoryzacji
        return Response(status_code=200)
    # Sprawdzamy API Key tylko dla GET!
    if api_key is None:
        api_key = request.headers.get("X-API-Key")
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return open_positions

@app.get("/symbols")
def get_symbols(request: Request):
    api_key = request.headers.get("X-API-Key")
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return get_top_symbols()
