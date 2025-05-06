import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Pinecone
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")
    PINECONE_INDEX = os.getenv("PINECONE_INDEX")

    # Weaviate
    WEAVIATE_URL = os.getenv("WEAVIATE_URL")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
    WEAVIATE_BATCH_SIZE = int(os.getenv("WEAVIATE_BATCH_SIZE", "50"))

    # Azure
    AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
    AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
    AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")

    # Fine-tuning
    FINE_TUNED_MODEL_PATH = os.getenv("FINE_TUNED_MODEL_PATH", "models/finetuned_model")

    # ... add other config items