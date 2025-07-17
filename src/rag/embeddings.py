from dataclasses import dataclass
from typing import Dict, Literal, Union

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_qdrant import FastEmbedSparse


@dataclass
class EmbeddingService:
    """
    Serviço para gerenciar embeddings densos e esparsos.

    Atributos:
        openai_api_key (str): Chave da API da OpenAI.
        dense_model (str): Modelo de embedding denso (padrão: "text-embedding-3-large").
        sparse_model (str): Modelo de embedding esparso (padrão: "Qdrant/bm25").
    """

    openai_api_key: str
    dense_model: str = 'text-embedding-3-small'
    sparse_model: str = 'Qdrant/bm25'

    def get_embedding(
        self, embedding_type: Literal['dense', 'sparse']
    ) -> Union[OpenAIEmbeddings, FastEmbedSparse]:
        """Retorna um embedder do tipo especificado ('dense' ou 'sparse')."""
        if embedding_type == 'dense':
            return OpenAIEmbeddings(
                model=self.dense_model, openai_api_key=self.openai_api_key
            )
        elif embedding_type == 'sparse':
            return FastEmbedSparse(model_name=self.sparse_model)
        raise ValueError(f'Invalid embedding type: {embedding_type}')

    def get_all_embeddings(
        self,
    ) -> Dict[str, Union[OpenAIEmbeddings, FastEmbedSparse]]:
        """Retorna um dicionário com os embedders disponíveis ('dense' e 'sparse')."""
        return {
            'dense': self.get_embedding('dense'),
            'sparse': self.get_embedding('sparse'),
        }
