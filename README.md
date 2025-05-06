# Self-Improving Retrieval-Augmented Generation (RAG) System

**Author**: Samson Boicu

This repository contains a full **Self-Improving RAG** pipeline that demonstrates:

- **Hybrid Vector Search** with Pinecone (dense) and Weaviate (sparse BM25 + metadata filters)
- **Augmentation** with [Guardrails.ai](https://github.com/shreyar/guardrails) for hallucination prevention
- **Query Intent Disambiguation** with Azure AI Search
- **Feedback Loop** for user feedback → fine-tune retriever with [SentenceTransformers](https://www.sbert.net/)
- **Automated RAGAS Evaluation** pipeline

## Project Structure