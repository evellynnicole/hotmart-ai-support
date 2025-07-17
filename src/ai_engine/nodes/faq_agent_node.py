# ruff: noqa
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI

from src.ai_engine.states.state import ChatGraphState
from src.ai_engine.tools import tools_faq
from src.ai_engine.tools.retriever import retrieve_faq

PROMPT_FAQ_AGENT = """
Você é um agente especializado em atendimento ao cliente da Hotmart.

Seu objetivo é responder a dúvidas frequentes sobre produtos, 
serviços ou assuntos relacionados à Hotmart.

Para isso, você pode usar a ferramenta de retriever para buscar informações relevantes no banco de dados de perguntas frequentes.
Observe a similaridade entre a pergunta do usuário e a pergunta feita.
Responde de maneira contextualizada, com base nas informações encontradas no banco de dados de perguntas frequentes.

Jamais responda com se você não tem a resposta, sempre use as informações encontradas
no banco de dados de perguntas frequentes.

Caso não encontre a resposta ou a similaridade não seja suficiente, encaminhe para o atendimento humano através da ferramenta customer_service.
"""


class FAQAgentNode:
    def __init__(self):
        self.model = ChatOpenAI(model='gpt-4o-mini', temperature=0).bind_tools(
            tools_faq
        )

    def __call__(self, state: ChatGraphState) -> dict:
        messages = state['messages'].copy()
        messages.insert(0, SystemMessage(content=PROMPT_FAQ_AGENT))
        response = self.model.invoke(messages)
        tool_calls = response.tool_calls
        sources = []

        if tool_calls:
            for tool_call in tool_calls:
                if tool_call['name'] == 'retrieve_faq':
                    tool_result = retrieve_faq(tool_call['args']['query'])
                    sources.extend(tool_result.get('sources', []))

                    tool_message = ToolMessage(
                        content=str(tool_result), tool_call_id=tool_call['id']
                    )
                    messages.extend([response, tool_message])

            final_response = self.model.invoke(messages)

            return {
                **state,
                'node_name': 'faq_agent_node',
                'messages': [final_response],
                'sources': sources,
            }

        return {
            **state,
            'node_name': 'faq_agent_node',
            'messages': [response],
            'sources': [],
        }
