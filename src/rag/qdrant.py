import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from uuid import uuid4

from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QdrantService:
    """
    Serviço para gerenciar uma coleção Qdrant.

    Atributos:
        url (str): URL do servidor Qdrant.
        collection_name (str): Nome da coleção no Qdrant.
        dense_embeddings (Any): Modelo de embeddings densos.
        sparse_embeddings (Any): Modelo de embeddings esparsos.
        connection (Optional[QdrantVectorStore]): Conexão ativa com a coleção.
        client (Optional[QdrantClient]): Cliente Qdrant.
    """

    host: str
    port: str
    collection_name: str
    dense_embeddings: Any
    sparse_embeddings: Any
    connection: Optional[QdrantVectorStore] = None
    client: Optional[QdrantClient] = None

    def __post_init__(self):
        """
        Inicializa a conexão com o Qdrant após a criação da instância.

        Lança:
            Exception: Se houver erro ao conectar ao Qdrant.
        """
        self.client = QdrantClient(host=self.host, port=self.port)
        self.connection = self.collection_connect()

    def _get_store_params(self) -> Dict[str, Any]:
        """
        Retorna parâmetros comuns para criar uma loja de vetores Qdrant.

        Inclui modelos de embeddings.
        """
        return {
            'embedding': self.dense_embeddings,
            'sparse_embedding': self.sparse_embeddings,
            'host': self.host,
            'port': self.port,
            'prefer_grpc': False,
            'collection_name': self.collection_name,
            'retrieval_mode': RetrievalMode.HYBRID,
            'content_payload_key': 'page_content',
            'metadata_payload_key': 'metadata',
        }

    def collection_connect(self) -> Optional[QdrantVectorStore]:
        """
        Conecta a uma coleção Qdrant existente.

        Returns:
            Conexão estabelecida ou None em caso de falha.
        """
        try:
            logger.info('Connecting to collection')
            connection = QdrantVectorStore.from_existing_collection(
                **self._get_store_params()
            )
            logger.info('Connection successful!')
            return connection
        except Exception as e:
            logger.error(f'Error connecting to collection: {e}')
            return None

    def create_collection(
        self, documents: List[Any]
    ) -> Optional[QdrantVectorStore]:
        """
        Cria uma nova coleção Qdrant e adiciona documentos.

        Args:
            documents: Lista de documentos a serem adicionados.

        Returns:
            Conexão estabelecida ou None em caso de falha.
        """
        try:
            logger.info('Creating collection and add documents')
            self.connection = QdrantVectorStore.from_documents(
                documents=documents, **self._get_store_params()
            )
            logger.info('Collection created and documents added successfully!')
            return self.connection
        except Exception as e:
            logger.error(f'Error creating collection: {e}')
            return None

    def add_documents(self, documents: List[Any]) -> None:
        """
        Adiciona documentos a uma coleção existente.

        Args:
            documents: Lista de documentos a serem adicionados.
        """
        if not self.connection:
            logger.error('Error: Not connected to any collection')
            return

        try:
            ids = [str(uuid4()) for _ in documents]
            logger.info(f'Add {len(documents)} documents.')
            self.connection.add_documents(documents=documents, ids=ids)
            logger.info('Documents added successfully!')
        except Exception as e:
            logger.error(f'Error adding documents: {e}')

    def search(self, query: str, k: int):
        """
        Realiza uma busca por similaridade com filtro específico.

        Args:
            query: Consulta de busca.
            filter_type: Tipo de filtro.
            k: Número de resultados.

        Returns:
            Resultados da busca ou None se não estiver conectado.
        """
        if not self.connection:
            logger.error('Error: Not connected to any collection')
            return None

        # filter_obj = QueryFilters.create_filter(filter_type)
        return self.connection.similarity_search_with_score(query=query, k=k)

    def get_ids(self) -> List[str]:
        """
        Recupera IDs de documentos de uma coleção.

        Returns:
            Lista de IDs ou uma lista vazia se não estiver conectado.
        """
        if not self.connection:
            logger.error('Error: Not connected to any collection')
            return []

        try:
            logger.info('Fetching document IDs')
            records, _ = self.client.scroll(
                collection_name=self.collection_name,
                limit=10_000,
                with_payload=True,
                with_vectors=False,
            )

            documents = [
                {'id': str(record.id), 'payload': record.payload}
                for record in records
            ]

            logger.info(f'Retrieved {len(documents)} documents successfully!')
            return documents
        except Exception as e:
            logger.error(f'Error fetching document IDs: {e}')
            return []

    def delete(self, ids: List[str | int]) -> bool:
        """
        Exclui documentos por seus IDs.

        Args:
            ids: Lista de IDs dos documentos a serem excluídos.

        Returns:
            True se a exclusão for bem-sucedida, False caso contrário.
        """

        if not self.connection:
            logger.error('Error: Not connected to any collection')
            return False

        try:
            logger.info(f'Delete {len(ids)} documents.')
            self.connection.delete(ids=ids)
            logger.info('Documents deleted successfully!')
            return True
        except Exception as e:
            logger.error(f'Error delete documents: {e}')
            return False
