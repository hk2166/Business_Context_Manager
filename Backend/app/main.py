from fastapi import FastAPI
from app.api import memory

app = FastAPI(title="Enterprise Memory Engine")

app.include_router(memory.router)