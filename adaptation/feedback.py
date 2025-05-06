import json
import os

FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "feedback_store.json")

def save_feedback(query, retrieved_docs, user_feedback):
    """
    Store feedback for future fine-tuning.
    :param query: user query string
    :param retrieved_docs: list of docs returned
    :param user_feedback: rating or any feedback structure
    """
    data = {
        "query": query,
        "retrieved_docs": retrieved_docs,
        "feedback": user_feedback
    }
    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump([data], f, indent=2)
    else:
        with open(FEEDBACK_FILE, 'r') as f:
            existing_data = json.load(f)
        existing_data.append(data)
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump(existing_data, f, indent=2)

def get_all_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, 'r') as f:
        return json.load(f)