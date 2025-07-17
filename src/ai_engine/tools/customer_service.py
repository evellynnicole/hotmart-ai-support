from langchain_core.tools import tool


@tool
def customer_service(query: str) -> str:
    """
    Encaminha o usuário para o atendimento humano
    quando nenhuma resposta relevante for encontrada.
    """
    return """
    Não encontrei uma resposta adequada para sua dúvida.
    Encaminhei sua solicitação para nossa equipe de atendimento.
    Eles entrarão em contato em breve!
    """
