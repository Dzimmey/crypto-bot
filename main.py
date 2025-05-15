from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from executor import open_positions
from selector import get_top_symbols
import os

app = FastAPI()

# --- CORS MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # możesz ograniczyć np. do domeny Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.api_route("/positions", methods=["GET", "OPTIONS"])
def positions(request: Request, api_key: str = Depends(api_key_header)):
    # Jeśli to OPTIONS, ręcznie zwróć odpowiedź 200 z nagłówkami CORS
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "X-API-Key,Content-Type",
        }
        return Response(status_code=200, headers=headers)
    # Jeśli GET, autoryzacja
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return open_positions

@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Trading Bot API"}

@app.get("/status")
def get_status():
    return {"status": "bot online"}

@app.api_route("/symbols", methods=["GET", "OPTIONS"])
def symbols(request: Request, api_key: str = Depends(api_key_header)):
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "X-API-Key,Content-Type",
        }
        return Response(status_code=200, headers=headers)
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return get_top_symbols()
