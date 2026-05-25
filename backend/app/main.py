from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import transcription_route
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from dotenv import load_dotenv
import os

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / "backend" / ".env")

print(f"DB: {os.getenv('DB_HOST')}")

app.mount("/static", StaticFiles(directory = BASE_DIR/"backend"/"app"/"static"), name="static")
#app.mount("/", StaticFiles(directory = BASE_DIR/ "frontend" / "dist", html = True), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return FileResponse(BASE_DIR / "static" / "index.html")


app.include_router(transcription_route.router, prefix="/api")