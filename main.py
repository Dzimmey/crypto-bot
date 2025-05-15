from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from executor import open_positions
from selector import get_top_symbols
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W produkcji możesz wpisać swoją domenę Vercel!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")

@app.api_route("/positions", methods=["GET", "OPTIONS"])
async def get_positions(request: Request):
    if request.method == "OPTIONS":
        return Response(status_code=200)
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return open_positions

@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Trading Bot API"}

@app.get("/status")
def get_status():
    return {"status": "bot online"}

@app.api_route("/symbols", methods=["GET", "OPTIONS"])
async def get_symbols(request: Request):
    if request.method == "OPTIONS":
        return Response(status_code=200)
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return get_top_symbols()
