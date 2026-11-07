from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI()

@app.get(path = "/", response_class = RedirectResponse)
async def root():
    return "/docs"

@app.get("/api/ping")
async def ping_pong():
    return "pong"
