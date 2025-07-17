from src.ai_engine.states.state import ChatGraphState


class CustomerServiceNode:
    def __call__(self, state: ChatGraphState) -> dict:
        mock_response = """
        Entendi sua solicitação!
        Para te ajudar melhor, vou te encaminhar
        para um de nossos atendentes. Por favor, aguarde um momento.
        """

        return {
            **state,
            'messages': [mock_response],
            'node_name': 'customer_service_node',
        }
