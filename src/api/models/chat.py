from typing import Dict, List, Union
from uuid import UUID

from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: int
    question: str


class ChatResponse(BaseModel):
    answer: str
    agent_name: str
    timestamp: str
    chat_id: UUID
    sources: List[Dict[str, Union[str, None]]]
