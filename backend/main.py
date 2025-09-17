# backend/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from capture import start_capture

# 🔹 Lê do ambiente, se não existir usa localhost
SERVER_IP = os.getenv("SERVER_IP", "127.0.0.1")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Inicia a captura para o IP configurado
    start_capture(SERVER_IP)
    print(f"📡 Capturando tráfego para {SERVER_IP}")
