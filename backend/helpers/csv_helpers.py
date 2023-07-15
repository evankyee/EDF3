import pandas as pd
from fuzzywuzzy import fuzz
from helpers.fuzzy_helpers import fuzzy_match

def filter_csv_by_degree(input_csv_path, output_csv_path):
    # Read the input CSV into a pandas DataFrame
    df = pd.read_csv(input_csv_path)

    # Filter out rows where 'is_higher_level_degree' is 'no'
    df_filtered = df[df['is_higher_level_degree'] != 'no']

    # Write the filtered data to a new CSV file
    df_filtered.to_csv(output_csv_path, index=False)

def extract_keywords(input_csv_path, output_csv_path, keyword_bank):
    # Read the input CSV into a pandas DataFrame
    df = pd.read_csv(input_csv_path)

    # Create new columns for keywords in each 'why' column
    for col in ['why_edf', 'why_sus', 'why_cc']:
        df[col + '_keywords'] = df[col].apply(lambda text: [fuzzy_match(word, keyword_bank) for word in text.lower().split()])

    # Write the DataFrame with new columns to a new CSV file
    df.to_csv(output_csv_path, index=False)