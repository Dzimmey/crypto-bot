from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from executor import open_positions
from selector import get_top_symbols
import os

app = FastAPI()

# --- Middleware CORS (PRZED endpointami!) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # docelowo ["https://crypto-bot-seven-psi.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")

# --- /positions endpoint z obsługą GET, OPTIONS, HEAD ---
@app.api_route("/positions", methods=["GET", "OPTIONS", "HEAD"])
async def positions(request: Request):
    # Preflight: odpowiedz na OPTIONS
    if request.method == "OPTIONS":
        return Response(status_code=200)
    # Health-check: HEAD
    if request.method == "HEAD":
        return Response(status_code=200)
    # GET: autoryzacja przez nagłówek
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return open_positions

# --- /symbols endpoint z obsługą GET, OPTIONS, HEAD ---
@app.api_route("/symbols", methods=["GET", "OPTIONS", "HEAD"])
async def symbols(request: Request):
    if request.method == "OPTIONS":
        return Response(status_code=200)
    if request.method == "HEAD":
        return Response(status_code=200)
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return get_top_symbols()

# --- Prosty root i status (nie wymagają API KEY) ---
@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Trading Bot API"}

@app.get("/status")
def get_status():
    return {"status": "bot online"}
