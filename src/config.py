import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    def qdrant_settings():
        return {
            'host': os.getenv('QDRANT_HOST'),
            'port': os.getenv('QDRANT_PORT'),
            'collection_name': os.getenv('COLLECTION_NAME'),
        }

    def openai_settings():
        return {'openai_api_key': os.getenv('OPENAI_API_KEY')}
