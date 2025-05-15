from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from executor import open_positions
from selector import get_top_symbols
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # (lub ["https://crypto-bot-seven-psi.vercel.app"] na produkcji)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")

@app.api_route("/positions", methods=["GET", "OPTIONS"])
async def positions(request: Request):
    # Obsługa preflight (CORS)
    if request.method == "OPTIONS":
        return Response(status_code=200)
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return open_positions

@app.api_route("/symbols", methods=["GET", "OPTIONS"])
async def symbols(request: Request):
    if request.method == "OPTIONS":
        return Response(status_code=200)
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return get_top_symbols()

@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Trading Bot API"}

@app.get("/status")
def get_status():
    return {"status": "bot online"}
