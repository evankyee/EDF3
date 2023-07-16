import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration

def compute_summary(text):
    # Load the T5 tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    model = T5ForConditionalGeneration.from_pretrained('t5-small')

    # Prepare the input text for summarization
    input_text = f'summarize: {text}'

    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors='pt', max_length=512, truncation=True)

    # Generate the summary
    summary_ids = model.generate(inputs.input_ids, num_beams=4, min_length=30, max_length=150, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

def filter_csv_by_degree(input_csv_path, output_csv_path, keyword_bank):
    # Read the input CSV into a pandas DataFrame
    df = pd.read_csv(input_csv_path)

    # Filter out rows where 'is_higher_level_degree' is 'no'
    df_filtered = df[df['is_higher_level_degree'] != 'no']

    # Combine the 'why_edf', 'why_sus', and 'why_cc' columns into a single column
    df_filtered['all_responses'] = df_filtered['why_edf'] + ' ' + df_filtered['why_sus'] + ' ' + df_filtered['why_cc']

    # Create new columns for keywords in each 'why' column
    for col in ['why_edf', 'why_sus', 'why_cc']:
        df[col + '_keywords'] = df[col].apply(lambda text: [word for word in keyword_bank if word in text.lower()])

    # Compute the summary for the combined responses and add '_summary' to the new column name
    df_filtered['answer_summary'] = df_filtered['all_responses'].apply(compute_summary)

    # Drop the intermediate 'all_responses' column
    df_filtered.drop(columns=['all_responses'], inplace=True)

    # Write the filtered data with the summary to a new CSV file
    df_filtered.to_csv(output_csv_path, index=False)
