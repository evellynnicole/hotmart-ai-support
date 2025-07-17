import json

from langchain_core.tools import tool

data_path = 'src/data/mock_billing_data.json'


@tool
def get_billing_info(user_id: int) -> str:
    """
    Retorna as informações de faturamento do usuário.
    """
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_data = next(
        (item for item in data if item['user_id'] == user_id), None
    )

    if user_data is None:
        return f'Usuário com ID {user_id} não encontrado.'

    return json.dumps(user_data, indent=2)
