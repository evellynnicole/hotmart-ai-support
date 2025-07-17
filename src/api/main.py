from fastapi import FastAPI

from src.api.routes import chat

app = FastAPI()

app.include_router(chat.router, prefix='/chat', tags=['Chat'])
