from fuzzywuzzy import fuzz
import pandas as pd

def extract_and_highlight_keywords(input_csv_path, keyword_bank):
    # Read the input CSV into a pandas DataFrame
    df = pd.read_csv(input_csv_path)

    # Create new columns for keywords in each 'why' column
    for col in ['why_edf', 'why_sus', 'why_cc']:
        df[col + '_highlighted'] = df[col].apply(lambda text: [highlight_keyword(word, keyword_bank) for word in text.lower().split()])

    # Convert the DataFrame to a list of dictionaries (JSON format)
    highlighted_data = df.to_dict(orient='records')

    return highlighted_data

def highlight_keyword(word, keyword_bank):
    # Find the most similar keyword in the keyword bank to the given word
    best_match = max(keyword_bank, key=lambda keyword: fuzz.ratio(word.lower(), keyword.lower()))

    # Highlight the keyword (e.g., by wrapping it in HTML <mark> tag)
    return f"<mark>{word}</mark>" if word.lower() == best_match.lower() else word
