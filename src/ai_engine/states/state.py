from typing import Dict, List, Union

from langgraph.graph import MessagesState


class ChatGraphState(MessagesState):
    """ChatGraph State"""

    node_name: str = ''
    router_response: str = ''
    guardrail_response: str = ''
    user_id: int = None
    sources: List[Dict[str, Union[str, None]]] = []
