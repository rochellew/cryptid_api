from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cryptids
from scripts.populate_db import populate
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    populate()
    yield

def start():
    """Launched with `uv run dev`"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI(lifespan = lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cryptids.router)