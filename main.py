from fastapi import FastAPI, HTTPException, Request, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from executor import open_positions
from selector import get_top_symbols
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Trading Bot API"}

@app.get("/status")
def get_status():
    return {"status": "bot online"}

@app.api_route("/positions", methods=["GET", "OPTIONS"], dependencies=[Depends(verify_api_key)])
def get_open_positions(request: Request):
    if request.method == "OPTIONS":
        return Response(status_code=200)
    return open_positions

@app.get("/symbols", dependencies=[Depends(verify_api_key)])
def get_symbols():
    return get_top_symbols()
