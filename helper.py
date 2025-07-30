import json
import os
from datetime import datetime

def clean_text(text):
    # clean text by removing markdown formatting
    return text.strip("```json").strip("```").strip()

def save_results(content, folder="results", prefix="data_analysis_test"):
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)
    # Get current time in YYYYMMDD_HHMMSS format
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{current_time}.json"
    filepath = os.path.join(folder, filename)
    # Save content as JSON
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=4)
    print(f"Saved to {filepath}")