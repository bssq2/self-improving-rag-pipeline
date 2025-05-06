import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ragas import evaluate_responses  # example import, confirm usage
from adaptation.feedback import get_all_feedback

def main():
    # Load feedback or generate queries/answers to evaluate
    feedback_data = get_all_feedback()

    # RAGAS expects a certain format: list of {query, context, ground_truth, answer, ...}
    # We'll just stub an example
    data_for_ragas = []
    for record in feedback_data:
        data_for_ragas.append({
            "query": record["query"],
            "context": record["retrieved_docs"],
            "ground_truth": "N/A",  # or actual ground truth
            "answer": "Sample answer"  # or actual answer from your pipeline
        })
    # Evaluate
    ragas_scores = evaluate_responses(data_for_ragas, parallel=False)
    print("RAGAS evaluation complete. Results:")
    print(ragas_scores)

if __name__ == "__main__":
    main()