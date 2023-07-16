from transformers import pipeline
import pandas as pd

def assign_sentiment_scores(input_csv_path, output_csv_path):
    # Load the pre-trained sentiment analysis model (using the 'distilbert-base-uncased' model)
    sentiment_analyzer = pipeline('sentiment-analysis')

    # Read the input CSV into a pandas DataFrame
    df = pd.read_csv(input_csv_path)

    # Define the questions for each column
    questions = {
        "why_edf": "Why the Environmental Defense Fund?",
        "why_sus": "Why sustainability?",
        "why_cc": "Why climate corps fellowship?"
    }

    # Iterate through the DataFrame and calculate sentiment scores for each question
    for col, question in questions.items():
        df[col + '_score'] = df[col].apply(lambda text: sentiment_analyzer(question + ' ' + text)[0]['score'] * 10.0)

    # Write the filtered data with unique keywords to a new CSV file
    df.to_csv(output_csv_path, index=False)
