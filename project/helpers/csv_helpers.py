import pandas as pd
import csv
from transformers import T5Tokenizer, T5ForConditionalGeneration
import json

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

def read_matching_file_for_company(matching_filepath):
    company_data = {}  # Dictionary to store company data

    with open(matching_filepath, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            company = row['status']
            name = row['name']
            email = row['email']
            
            # Create a tuple with name and email
            person_info = (name, email)

            # Add the person's info to the list for the company
            if company in company_data:
                company_data[company].append(person_info)
            else:
                company_data[company] = [person_info]

    return company_data

def read_matching_file_for_people(matching_filepath):
    company_data = {}  # Dictionary to store company data

    with open(matching_filepath, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            company = row['assignment']
            name = row['name']
            email = row['email']
            
            # Create a tuple with name and email
            person_info = (name, email)

            # Add the person's info to the list for the company
            if company in company_data:
                company_data[company].append(person_info)
            else:
                company_data[company] = [person_info]

    return company_data

def read_csv_to_dict_list(csv_path):
    df = pd.read_csv(csv_path)
    return df.to_dict(orient='records')

def parse_company_vacancies(file_path):
    org_dict = {}
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            company_id, company_str, vacancies = row
            org_dict[company_str] = int(vacancies)
    return org_dict

def is_csv_file_empty(file_path):
    try:
        with open(file_path, 'r', newline='') as csvfile:
            # Check if the file is empty
            csv_reader = csv.reader(csvfile)
            return not any(csv_reader)
    except FileNotFoundError:
        # If the file doesn't exist, it is considered empty
        return True
