"""
services/chat_service.py
"""

import uuid
from datetime import datetime

from langchain_core.messages import HumanMessage

from src.ai_engine.graph.graph import ChatGraph
from src.ai_engine.states.state import ChatGraphState
from src.api.models.chat import ChatRequest

graph = ChatGraph().get_graph()


def handle_chat(request: ChatRequest) -> dict:
    state = ChatGraphState(
        messages=[HumanMessage(content=request.question)],
        user_id=request.user_id,
    )

    final_state = graph.invoke(state)

    final_message = final_state['messages'][-1]

    return {
        'answer': final_message.content,
        'agent_name': final_state['node_name'],
        'timestamp': datetime.now().isoformat(),
        'chat_id': str(uuid.uuid4()),
        'sources': final_state.get('sources', []),
    }
