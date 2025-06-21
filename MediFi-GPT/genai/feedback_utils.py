import csv
from datetime import datetime
import os

def save_feedback(user_question, model_response, feedback_text, rating):
    file_path = "output/feedback_log.csv"
    write_header = not os.path.exists(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp", "question", "response", "feedback", "rating"])
        writer.writerow([
            datetime.now().isoformat(),
            user_question,
            model_response,
            feedback_text,
            rating
        ])
