import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adaptation.feedback import get_all_feedback
from config import Config
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

def main():
    feedback_data = get_all_feedback()
    if len(feedback_data) == 0:
        print("No feedback data available. Exiting.")
        return

    # Load a base model
    model = SentenceTransformer("intfloat/e5-large-v2")

    # Build training examples
    # For demonstration, let's assume user_feedback is either 'positive' or 'negative'
    # We'll create pairs of (query, doc) with a certain score
    train_examples = []
    for record in feedback_data:
        query = record["query"]
        docs = record["retrieved_docs"]
        feedback = record["feedback"]
        # Example scoring
        score = 1.0 if feedback == "positive" else 0.0
        for doc in docs:
            train_examples.append(InputExample(texts=[query, doc], label=score))

    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=4)
    train_loss = losses.CosineSimilarityLoss(model)

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,  # adjust
        warmup_steps=10
    )

    # Save the fine-tuned model
    os.makedirs(Config.FINE_TUNED_MODEL_PATH, exist_ok=True)
    model.save(Config.FINE_TUNED_MODEL_PATH)
    print("Fine-tuning complete. Model saved to:", Config.FINE_TUNED_MODEL_PATH)

if __name__ == "__main__":
    main()