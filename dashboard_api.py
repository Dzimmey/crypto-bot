### dashboard_api.py
from fastapi import FastAPI
from executor import open_positions
from selector import get_top_symbols

app = FastAPI()

@app.get("/status")
def get_status():
    return {"status": "bot online"}

@app.get("/positions")
def get_open_positions():
    return open_positions

@app.get("/symbols")
def get_symbols():
    return get_top_symbols()

@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Trading Bot API"}
