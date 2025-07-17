from langchain_core.tools import tool

from src.config import Config
from src.rag.embeddings import EmbeddingService
from src.rag.qdrant import QdrantService

settings = Config()
embedding_service = EmbeddingService(**settings.openai_settings())
collection_name = settings.qdrant_settings()['collection_name']
embeddings = embedding_service.get_all_embeddings()

qdrant_service = QdrantService(
    host=settings.qdrant_settings()['host'],
    port=settings.qdrant_settings()['port'],
    collection_name=collection_name,
    dense_embeddings=embeddings['dense'],
    sparse_embeddings=embeddings['sparse'],
)


@tool
def retrieve_faq(query: str) -> dict:
    """
    Retorna resposta baseada em similaridade + metadados (nome e URL do artigo).

    Args:
        query: Pergunta do usuário.

    Returns:
        dict: {'answer': ..., 'sources': [...]}.
    """
    try:
        results = qdrant_service.search(query, 5)

        if not results:
            return {
                'answer': 'Não foi encontrada informação relevante para sua pergunta.',
                'sources': [],
            }

        sources = [
            {
                'article_name': doc.metadata.get('article_name'),
                'article_url': doc.metadata.get('article_url'),
                'id': doc.metadata.get('_id'),
                'score': f'{score:.3f}',  # convertendo para string formatada
            }
            for doc, score in results
        ]

        combined_answer = '\n\n'.join([
            f'{i + 1}. {doc.metadata.get("article_name")} - '
            f'{doc.metadata.get("article_url")} (Score: {score:.2f})'
            for i, (doc, score) in enumerate(results)
        ])
        return {'answer': combined_answer, 'sources': sources}

    except Exception as e:
        return {
            'answer': f'Erro ao buscar informações: {str(e)}',
            'sources': [],
        }
