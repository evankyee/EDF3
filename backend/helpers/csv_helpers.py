import pandas as pd
import csv
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

    # Process the summary to convert it into bullet points
    sentences = summary.split('. ')
    bullet_points = [f'• {sentence.strip().capitalize()}.'
                     for sentence in sentences if sentence.strip()]
    summary = '\n'.join(bullet_points)

    return summary

def parse_csv_to_dictionaries(csv_filepath):
    id_to_company = {}
    id_to_vacancies = {}

    with open(csv_filepath, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            company_id = int(row['company_id'])
            company_name = row['company_str']
            vacancies = int(row['vacancies'])

            id_to_company[company_id] = company_name
            id_to_vacancies[company_id] = vacancies

    return id_to_company, id_to_vacancies

def csv_to_json(csv_data):
    data = []
    for row in csv_data:
        data.append(dict(zip(row[0::2], row[1::2])))

    return json.dumps(data)

def init_input_csv(input_csv_path, output_csv_path, keyword_bank):
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

    # Add a new column 'status' and initialize all rows to have it be "waitlist"
    df_filtered['status'] = 'unassigned'

    # Write the filtered data with the summary to a new CSV file
    df_filtered.to_csv(output_csv_path, index=False)
