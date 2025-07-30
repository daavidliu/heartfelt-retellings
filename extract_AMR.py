import argparse
from prompts import SYSTEM_ROLE, extraction_prompt, extraction_prompt_PW_zero, extraction_prompt_PW_one, extraction_prompt_PW_few, reconstruction_prompt, evaluation_prompt, character_identification
from openai import OpenAI
import json
from dataset.dataset import get_narratives
from LLMClient import LLMClient
from tqdm import tqdm

import os
from datetime import datetime

def clean_text(text):
    # clean text by removing markdown formatting
    return text.strip("```json").strip("```").strip()

def extract_AMR(text, extraction_method=extraction_prompt_PW_one, provider="gemini"):
    client = LLMClient(provider=provider)
    response = client.chat(extraction_method(text), system_message=SYSTEM_ROLE)
    predicates = clean_text(response)
    return predicates

def retell_from_predicates(text, instructions = "", retell_method=reconstruction_prompt, provider="gemini"):
    client = LLMClient(provider=provider)
    response = client.chat(retell_method(text, instructions), system_message=SYSTEM_ROLE)
    retold = clean_text(response)
    return retold

def character_analysis(text, method=character_identification, provider="gemini"):
    client = LLMClient(provider=provider)
    response = client.chat(method(text))
    analysis = clean_text(response)
    return analysis

# def process_text(extraction_method, index):

#     output = {}
    
#     title = stories[index]["title"]
#     orig_text = stories[index]["text"]

#     print("Title:", title)

#     output["title"] = title
#     output["index"] = index
#     output["original_length"] = len(orig_text)
#     output["original_text"] = orig_text

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         temperature=0,
#         messages=[
#             {
#                 "role": "system", 
#                 "content": SYSTEM_ROLE
#             },
#             {   
#                 "role": "user", 
#                 "content": extraction_method(orig_text)}
#         ]
#     )

#     predicates = response.choices[0].message.content
#     predicates = clean_text(predicates)
#     predicates_list = [predicate.strip() for predicate in predicates.split('\n') if predicate.strip()]
#     output["predicates"] = predicates_list
#     output["predicates_length"] = len(clean_text(predicates))

#     print("Predicates:", predicates)  

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         temperature=0,
#         messages=[
#             {
#                 "role": "system", 
#                 "content": SYSTEM_ROLE
#             },
#             {   
#                 "role": "user", 
#                 "content": reconstruction_prompt(predicates)}
#         ]
#     )

#     reconstruction = response.choices[0].message.content
#     reconstruction = clean_text(reconstruction)
#     print("Reconstruction:", reconstruction)
#     print("Reconstruction length:", len(reconstruction))
#     try:
#         reconstruction_json = json.loads(clean_text(reconstruction))
#         output["reconstruction"] = reconstruction_json
#         output["reconstruction_length"] = len(reconstruction_json["Story"])
#     except json.JSONDecodeError:
#         output["reconstruction"] = clean_text(reconstruction)

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         temperature=0,
#         messages=[
#             {
#                 "role": "system", 
#                 "content": SYSTEM_ROLE
#             },
#             {   
#                 "role": "user", 
#                 "content": evaluation_prompt(orig_text, reconstruction)}
#         ]
#     )

#     evaluation = response.choices[0].message.content
#     evaluation = clean_text(evaluation)
#     print("Evaluation:", evaluation)
#     try:
#         evaluation_json = json.loads(clean_text(evaluation))
#         output["evaluation"] = evaluation_json
#     except json.JSONDecodeError:
#         output["evaluation"] = evaluation
#     with open(f"outputs/output_{index}.json", "w", encoding="utf-8") as f:
#         json.dump(output, f, ensure_ascii=False, indent=4)

#     return evaluation


non_linear_narrative_test = """
    The old man sat on the park bench, watching the children play. A lone red balloon drifted across the blue sky, catching his eye. It reminded him of a different day, a different park.

    Years earlier, a young woman with a bright smile had held that very balloon. She laughed, her hand intertwined with his. They had just shared a slice of strawberry cake at a small cafe. "Make a wish," she'd whispered, handing him the string. He'd wished for more moments just like that.

    The balloon, now a tiny speck, disappeared behind the tallest oak tree. The old man sighed, a bittersweet ache in his chest. He still remembered the taste of that cake, the warmth of her hand. The wish, he realised, had come true, in its own fleeting way.

"""

def data_analysis(number):
    results = []
    narratives = get_narratives(number)
    for narrative in narratives:
        new_result = {}
        try:
            new_result["story"] = narrative["story"]
            res = character_analysis(narrative["story"])

            # Try to parse the result as JSON, fallback to string
            try:
                res_json = json.loads(res)
                new_result["character_summary"] = res_json
            except Exception:
                new_result["character_summary"] = res
        except Exception as e:
            new_result = {
                "error": str(e)
            }
        results.append(new_result)
    return results


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

def test_first_run(number):
    results = []
    narratives = get_narratives(number)
    for narrative in tqdm(narratives, desc="Processing Narratives"):
        predicates = extract_AMR(narrative["story"])
        results.append({
            "narrative": narrative,
            "predicates": predicates,
            "narrative_length": len(narrative["story"]),
            "predicates_length": len(predicates)
        })
    
    save_results(results, folder="results", prefix="predicate_test_" + str(number))



if __name__ == "__main__":
    test_first_run(100)
    # # parser = argparse.ArgumentParser(description="Process text from stories.json")
    # # parser.add_argument("--text", type=int, required=True, help="Index of the text to process")
    # # args = parser.parse_args()

    # # process_text(extraction_prompt_PW_few, args.text)
    # print("this is extract_AMR")
    # # predicates = extract_AMR(non_linear_narrative_test)
    # # print(predicates)
    # narratives = get_narratives(2)
    # print(narratives[1]["story"])
    # predicates = extract_AMR(narratives[1]["story"])
    # print(predicates)
    
    # # for narrative in narratives:
    # #     print(narrative["story"])
    # #     predicates = extract_AMR(narrative["story"])
    # #     print(predicates)
    # #     # retold = retell_from_predicates(predicates, "rewrite the story from the 1st person point of view of the musician character instead of the original narrator")
    # #     # print(retold)
    # #     print(character_analysis(narrative))


    # # results = data_analysis(-1)
    # # save_results(results, folder="results", prefix="data_analysis_test_ALL")



    

