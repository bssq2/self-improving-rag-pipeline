import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from augmentation.azure_disambiguation import azure_query_disambiguation
from retrieval.hybrid_retriever import hybrid_retrieve
from augmentation.guardrails_wrapper import guard_response
from augmentation.metadata_filters import apply_metadata_filters
from adaptation.feedback import save_feedback

def main():
    print("Welcome to the Self-Improving RAG system!")
    while True:
        user_query = input("\nEnter your query (or 'exit' to quit): ").strip()
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # 1. Disambiguate query using Azure
        refined_query = azure_query_disambiguation(user_query)

        # 2. Retrieve from Pinecone + Weaviate
        retrieved_docs = hybrid_retrieve(refined_query, top_k=5)

        # 3. (Optional) Apply any custom metadata filters
        # filters = {"author": "John Doe"}  # example
        # retrieved_docs = apply_metadata_filters(retrieved_docs, filters)

        # 4. Summarize or generate final answer from retrieved_docs
        #    For demonstration, let's just join them as a naive "answer"
        naive_answer = " ".join(retrieved_docs)

        # 5. Use Guardrails to refine or validate the answer
        final_answer = guard_response(naive_answer)

        print("\nSystem answer:", final_answer)

        # 6. Collect user feedback
        user_feedback = input("\nWas this answer helpful? (positive/negative): ").strip()
        save_feedback(user_query, retrieved_docs, user_feedback)

if __name__ == "__main__":
    main()