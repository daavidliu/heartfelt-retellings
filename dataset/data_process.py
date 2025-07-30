import pandas as pd
import io
import json

csv_file_path = 'ALL_STORIES.csv'

# Use io.StringIO to simulate reading from a file
# In a real application, you would use:
# df = pd.read_csv('your_file_name.csv')
try:
    df_raw = pd.read_csv(csv_file_path)

    print("CSV Loaded Successfully!\n")

    # Select only the desired columns
    columns_to_keep = [
        "story",
        "Main Event",
        "Emotion Description",
        "Moral",
        "Empathy Reasons",
        "Empathizable",
        # "Well-Written",
        "num_sentences",
        "num_words"
    ]
    df = df_raw[columns_to_keep]


    # # --- Filter for BIO or MEM genres only ---
    # genre_column = 'Genre'
    # label_column = 'Label'
    # if genre_column in df.columns:
    #     df = df[df[genre_column].isin(['BIO', 'MEM']) & (df[label_column] != 'NEG')]
    #     print(f"Filtered to {len(df)} entries with Genre BIO or MEM.\n")
    # else:
    #     print(f"Warning: Column '{genre_column}' not found in the CSV. Cannot filter by genre.")

    # --- Print Column Names ---
    print("Columns in the CSV:")
    for column in df.columns:
        print(f"- {column}")
    print("\n") # Add a newline for better readability

    # --- Print Number of Rows ---
    # df.shape[0] gives the number of rows
    # df.shape[1] gives the number of columns
    print(f"Number of rows: {df.shape[0]}")

    # --- Data Analysis: Word Count Statistics for 'full_text' column ---
    column_to_analyse = 'story'

    if column_to_analyse in df.columns:
        print(f"Performing analysis on '{column_to_analyse}' column...\n")

        # Convert column to string type to handle potential non-string entries
        # and fill any NaN values with an empty string before counting words.
        df['word_count'] = df[column_to_analyse].astype(str).apply(lambda x: len(x.split()))

        # Calculate statistics
        word_count_mean = df['word_count'].mean()
        word_count_median = df['word_count'].median()
        word_count_max = df['word_count'].max()
        word_count_min = df['word_count'].min()
        word_count_std = df['word_count'].std() # Standard deviation for additional insight

        print(f"Statistics for word count in '{column_to_analyse}':")
        print(f"  Average (Mean) words: {word_count_mean:.2f}")
        print(f"  Median words: {word_count_median:.2f}")
        print(f"  Maximum words: {word_count_max}")
        print(f"  Minimum words: {word_count_min}")
        print(f"  Standard Deviation of words: {word_count_std:.2f}")
    else:
        print(f"Warning: Column '{column_to_analyse}' not found in the CSV. Cannot perform word count analysis.")
    
    print("\n" + "="*50 + "\n") # Separator for better readability

    # --- Data Analysis: Unique values and counts for 'genre' column ---
    genre_column = 'Well-Written'

    if genre_column in df.columns:
        print(f"Analysing unique types in '{genre_column}' column...\n")

        # Get the count of each unique value in the 'genre' column
        genre_counts = df[genre_column].value_counts()

        print(f"Counts for each type in '{genre_column}':")
        for genre_type, count in genre_counts.items():
            print(f"- {genre_type}: {count} entries")
    else:
        print(f"Warning: Column '{genre_column}' not found in the CSV. Cannot perform genre analysis.")


    print("\n" + "="*50 + "\n") # Separator for better readability

    # Filter for Empathizable == 5
    df_selected_filtered = df[df["Empathizable"] == 5]

    # Save to JSON file
    json_output_path = "heartfelt_selected.json"
    records = df_selected_filtered.to_dict(orient="records")
    with open(json_output_path, "w") as json_file:
        json.dump(records, json_file, indent=2)
    print(f"Selected columns saved to {json_output_path}")

except FileNotFoundError:
    print("Error: The specified CSV file was not found. Please check the file path.")
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty.")
except pd.errors.ParserError:
    print("Error: Could not parse the CSV file. Check its format.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")