import pandas as pd
from langchain.docstore.document import Document

from src.config import Config
from src.rag.embeddings import EmbeddingService
from src.rag.qdrant import QdrantService

settings = Config()
collection_name = settings.qdrant_settings()['collection_name']

df = pd.read_csv('hotmart_dataset.csv')

documents = []
for _, row in df.iterrows():
    content = row['article_content']
    metadata = {
        'article_url': row['article_url'],
        'article_name': row['article_name'],
    }
    documents.append(Document(page_content=content, metadata=metadata))

embedding_service = EmbeddingService(**settings.openai_settings())
embeddings = embedding_service.get_all_embeddings()

qdrant_service = QdrantService(
    host=settings.qdrant_settings()['host'],
    port=settings.qdrant_settings()['port'],
    collection_name=collection_name,
    dense_embeddings=embeddings['dense'],
    sparse_embeddings=embeddings['sparse'],
)

qdrant_service.create_collection(documents)
