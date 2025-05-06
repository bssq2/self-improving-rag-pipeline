import pinecone
import numpy as np
from config import Config
from transformers import AutoTokenizer, AutoModel

class PineconeRetriever:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("intfloat/e5-large-v2")
        self.model = AutoModel.from_pretrained("intfloat/e5-large-v2")
        pinecone.init(api_key=Config.PINECONE_API_KEY, environment=Config.PINECONE_ENV)
        self.index = pinecone.Index(Config.PINECONE_INDEX)

    def embed_text(self, text):
        # Minimalistic embedding with e5 or any model
        inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
        with np.no_grad():
            model_output = self.model(**inputs)
        # e5-large-v2 suggests using the [CLS] pooling or mean pooling
        # We'll do a simple mean pooling for demonstration
        embeddings = model_output.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
        # Normalize
        norm = np.linalg.norm(embeddings)
        embeddings = embeddings / norm
        return embeddings.tolist()

    def retrieve(self, query, top_k=5):
        query_embedding = self.embed_text(query)
        results = self.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        documents = [match.metadata["text"] for match in results.matches]
        return documents