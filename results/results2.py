import json
import pandas as pd
from collections import Counter

with open("results/predicate_test_100_20250725_175402.json", "r", encoding="utf-8") as f:
    results = json.load(f)

length = (len(results))

errors = 0

total_narrative_characters = 0
total_predicate_characters = 0
total_TW = []
total_BW = []
total_OW = []
total_WW = []
total_Other = []

def process_string(text_string):
    tw_lines = []
    bw_lines = []
    ow_lines = []
    ww_lines = []
    other_lines = []

    lines = text_string.splitlines() # This splits by various newline characters

    for line in lines:
        if line.startswith("TW"):
            tw_lines.append(line)
        elif line.startswith("BW"):
            bw_lines.append(line)
        elif line.startswith("OW"):
            ow_lines.append(line)
        elif line.startswith("WW"):
            ww_lines.append(line)
        else:
            other_lines.append(line)
            
    return {
        "TW": tw_lines,
        "BW": bw_lines,
        "OW": ow_lines,
        "WW": ww_lines,
        "Other": other_lines
    }

for result in results:
    try:
        total_predicate_characters += result["predicates_length"]
        total_narrative_characters += result["narrative_length"]

        processed = process_string(result["predicates"])

        total_TW.extend(processed["TW"])
        total_BW.extend(processed["BW"])
        total_OW.extend(processed["OW"])
        total_WW.extend(processed["WW"])
        total_Other.extend(processed["Other"])

    except Exception as e:
        print("ERROR", e)
        errors += 1

record = {
    "average_narrative_char_length": total_narrative_characters/length,
    "average_predicates_char_length": total_predicate_characters/length,
    "average_TW": len(total_TW)/length,
    "average_OW": len(total_OW)/length,
    "average_WW": len(total_WW)/length,
    "average_BW": len(total_BW)/length,
    "average_Other": len(total_Other)/length,
    "Other": total_Other,
    "OW": total_OW,
    "WW": total_WW,
    "BW": total_BW,
    "TW": total_TW

}

print(record)

# Define the filename
filename = "my_object.json"

# Open the file in write mode ('w') and use json.dump()
with open(filename, 'w') as f:
    json.dump(record, f, indent=4) # indent=4 makes the JSON file human-readable


# print(avg_character)
# print(length)
# print(errors)

# def word_frequency(words):
#     # Convert all words to lowercase
#     lowercase_words = [word.lower() for word in words]

#     # Count the frequency of each word
#     word_counts = Counter(lowercase_words)

#     # Convert to a pandas DataFrame for better presentation
#     df_word_counts = pd.DataFrame(word_counts.items(), columns=['Word', 'Frequency'])

#     # Sort the DataFrame by frequency in descending order
#     df_word_counts_sorted = df_word_counts.sort_values(by='Frequency', ascending=False)

#     # Display the table
#     print("Word Frequency Table:")
#     print(df_word_counts_sorted.to_markdown(index=False, numalign="left", stralign="left"))

# word_frequency(narrator_sex)
# word_frequency(other_characters)
# word_frequency(other_characters_sex)