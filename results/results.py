import json
import pandas as pd
from collections import Counter

with open("results/data_analysis_test_ALL_20250725_155648.json", "r", encoding="utf-8") as f:
    results = json.load(f)

length = (len(results))

total_characters = 0
errors = 0
i = 0

error_index = []

narrator_sex = []
other_characters = []
other_characters_sex = []

for result in results:
    try:
        var = result["character_summary"]["total_num_of_characters_including_narrator"]
        var = int(var)
        assert var < 1000
        total_characters += var

        narrator_sex.append(result["character_summary"]["narrator"]["sex"])
        for character in result["character_summary"]["other_characters"]:
            for name, info in character.items():
                sex = info.get("sex", "unspecified")
                print(f"Name: {name}, Sex: {sex}")
                other_characters.append(name)
                other_characters_sex.append(sex)
    except Exception as e:
        print("ERROR", e)
        print(i)
        errors += 1
        error_index.append(i)
    i += 1

avg_character = total_characters / length

print(avg_character)
print(length)
print(errors)

def word_frequency(words):
    # Convert all words to lowercase
    lowercase_words = [word.lower() for word in words]

    # Count the frequency of each word
    word_counts = Counter(lowercase_words)

    # Convert to a pandas DataFrame for better presentation
    df_word_counts = pd.DataFrame(word_counts.items(), columns=['Word', 'Frequency'])

    # Sort the DataFrame by frequency in descending order
    df_word_counts_sorted = df_word_counts.sort_values(by='Frequency', ascending=False)

    # Display the table
    print("Word Frequency Table:")
    print(df_word_counts_sorted.to_markdown(index=False, numalign="left", stralign="left"))

word_frequency(narrator_sex)
word_frequency(other_characters)
word_frequency(other_characters_sex)