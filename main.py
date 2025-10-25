# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import random

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Proyecto CICD - API", version="1.0")

# CORS para el cliente web (si se sirve desde otro origen)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

# Servir cliente estático (index.html)
app.mount("/", StaticFiles(directory="client", html=True), name="client")
