from promptsv2 import SYSTEM_ROLE, extraction_prompt, extraction_prompt_PW_zero, extraction_prompt_PW_one, extraction_prompt_PW_few, reconstruction_prompt, evaluation_prompt, character_identification, narrative_QA_promp_predicates, narrative_QA_prompt, narrative_QA_promp_content
import json

import os
from LLMClient import LLMClient
from tqdm import tqdm
from datetime import datetime


# Replace 'your_file.txt' with the path to your file
with open('narrative_qa_test/TheAdventureOfADyingDetective.txt', 'r', encoding='utf-8') as file:
    content = file.read()

def extract_AMR(text, extraction_method=extraction_prompt_PW_one, provider="gemini"):
    client = LLMClient(provider=provider)
    response = client.chat(extraction_method(text), system_message=SYSTEM_ROLE)
    predicates = clean_text(response)
    return predicates

def clean_text(text):
    # clean text by removing markdown formatting
    return text.strip("```json").strip("```").strip()

def save_results(variable, folder="results", prefix="data_analysis_test"):
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)
    # Get current time in YYYYMMDD_HHMMSS format
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{current_time}.json"
    filepath = os.path.join(folder, filename)
    # Save variable as JSON
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(variable, f, ensure_ascii=False, indent=4)
    print(f"Saved to {filepath}")

# predicates = extract_AMR(content)
# results = {
#             "narrative": content,
#             "predicates": predicates,
#             "narrative_length": len(content),
#             "predicates_length": len(predicates)
#         }

# save_results(results, folder="narrative_qa_test/results", prefix="narrative_qa_test_" + str("sherlock"))



import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
df = pd.read_csv('narrative_qa_test/qaps.csv')


# Define your target document_id
myVar = '09333c7d604bd412e6aef5d3e56b046ed301c5e5'

# Filter the DataFrame
filtered_df = df[df['document_id'] == myVar]

# Replace 'your_file.txt' with the path to your file
with open('narrative_qa_test/results/narrative_qa_test_sherlock_20250730_153145.json', 'r', encoding='utf-8') as file:
    content = file.read()


answers = []

num_correct = 0
num_wrong = 0

for row in filtered_df.itertuples(index=True):
    print(f"Row {row.Index}: question = {row.question}")
    # Access other columns like row.answer1_tokenized

    client = LLMClient(provider="gemini")
    response = client.chat(narrative_QA_promp_content(row.question,content))
    answer = clean_text(response)

        
    try:
        answer = json.loads(answer)
    except json.JSONDecodeError:
        pass  # Do nothing if JSON is invalid


    answer["question"] = row.question 
    answer["answer1"] = row.answer1
    answer["answer2"] = row.answer2

    response = answer["answer"]
    print(response)

    correct = client.chat(f"""
        Help me mark short this short answer response. 
        Your job is to determine if the response is the same as the correct answers.
                          
        Is this response "{response}" correct?
        
        Correct answers are "{row.answer1}" or "{row.answer2}".
                          
        Reply with ONLY yes or no
    """)

    answer["correct"] = correct.lower()

    if (correct.lower() == "yes"):
        num_correct += 1
    elif (correct.lower() == "no"):
        num_correct += 1

    answers.append(answer)

save_results(answers, folder="narrative_qa_test/results", prefix="narrative_qa_answers_" + str("sherlock"))




