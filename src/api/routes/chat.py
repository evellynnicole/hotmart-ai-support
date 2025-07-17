"""
routes/chat.py
"""

from fastapi import APIRouter

from src.api.models.chat import ChatRequest, ChatResponse
from src.api.services.chat_service import handle_chat

router = APIRouter()


@router.get('/health')
def health_check():
    return {'status': 'ok'}


@router.post('/')
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    response = handle_chat(request)
    return ChatResponse(**response)
