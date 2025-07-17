# ruff: noqa
from typing import Literal

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from src.ai_engine.states.state import ChatGraphState

SYSTEM_MESSAGE = """
Você é um agente especializado em atendimento ao cliente da Hotmart.

Seu objetivo é classificar e direcionar para um especialista de acordo com a intenção do usuário.
"""


class Roteador(BaseModel):
    next: Literal['faq', 'journey', 'atendente'] = Field(
        description='O próximo especialista ser executado. Opções:'
        "'faq': Para perguntas frequentes sobre produtos, serviços ou assuntos relacionados à Hotmart."
        "'journey': Para perguntas sobre a Hotmart Journey/Jornada. Sendo Starts ou Legacy."
        "'atendente': Para perguntas que não se encaixam nas categorias anteriores."
    )
    reason: str = Field(
        description='O motivo da escolha do tipo de especialista'
    )


class RouterNode:
    def __init__(self):
        self.model = ChatOpenAI(model='gpt-4o-mini', temperature=0)

    def __call__(self, state: ChatGraphState) -> dict:
        messages = state['messages'].copy()
        messages.insert(
            0,
            SystemMessage(
                content=SYSTEM_MESSAGE,
            ),
        )
        response = self.model.with_structured_output(Roteador).invoke(messages)

        return {
            **state,  # preserva o estado anterior
            'router_response': response.next,
            'node_name': 'router_node',
        }
