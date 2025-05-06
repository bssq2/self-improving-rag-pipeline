import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
import pinecone
import weaviate
import requests

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

def pinecone_ingest(texts):
    pinecone.init(api_key=Config.PINECONE_API_KEY, environment=Config.PINECONE_ENV)
    if Config.PINECONE_INDEX not in pinecone.list_indexes():
        pinecone.create_index(name=Config.PINECONE_INDEX, dimension=1024)  # dimension depends on embed model
    index = pinecone.Index(Config.PINECONE_INDEX)

    # Example: Using e5-large-v2 or any embedding logic you prefer
    # For demonstration, we'll mock embeddings with random vectors
    import numpy as np
    for i, text in enumerate(texts):
        vector = np.random.rand(1024).tolist()  # replace with real embeddings
        index.upsert([(f"id-{i}", vector, {"text": text})])

def weaviate_ingest(texts):
    client = weaviate.Client(
        url=Config.WEAVIATE_URL,
        additional_headers={
            "X-OpenAI-Api-Key": Config.WEAVIATE_API_KEY  # if using Weaviate cloud or a token
        }
    )

    # Create a schema class if not existing
    class_obj = {
        "class": "Document",
        "description": "A document containing text",
        "vectorizer": "text2vec-openai",  # or 'none' if you handle embeddings yourself
        "properties": [
            {
                "name": "content",
                "dataType": ["text"]
            }
        ]
    }

    try:
        client.schema.create_class(class_obj)
    except weaviate.exceptions.RequestsConnectionError:
        print("Error connecting to Weaviate. Check your URL/API key.")
        return
    except weaviate.exceptions.UnexpectedStatusCodeException as e:
        if "already exists" in str(e):
            pass
        else:
            print(e)
            return

    # Batch ingestion
    with client.batch as batch:
        for i, text in enumerate(texts):
            props = {
                "content": text
            }
            batch.add_data_object(props, "Document")

def main():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.txt")
    texts = load_data(file_path)

    # Ingest into Pinecone
    pinecone_ingest(texts)

    # Ingest into Weaviate
    weaviate_ingest(texts)

    print("Ingestion complete.")

if __name__ == "__main__":
    main()