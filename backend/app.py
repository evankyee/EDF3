from flask import Flask, request, jsonify
import pandas as pd
from helpers.csv_helpers import init_input_csv 
from helpers.fuzzy_helpers import fuzzy_match
from helpers.sentiment_helpers import assign_sentiment_scores
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

@app.route('/process_csv', methods=['POST'])
def process_csv():
    try:
        # Check if the request contains a file named 'csv_file'
        if 'csv_file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['csv_file']

        # Check if the file has a filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        # Read the CSV file using pandas
        df = pd.read_csv(file)

        # Perform processing on the CSV data (you can add your processing logic here)
        processed_data = df.to_dict(orient='records')

        return jsonify({'data': processed_data})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Inherit the automated_scoring from the toggle on the front-end
    # TODO: Enable inheriting from the frontend -- currently just declare
    automated_scoring = True

    # Inherit the keywords needed for the keyword highlighting process 
    # TODO: Enable inheriting form the frontend -- currently just declare
    keywords = ["plastic", "law", "transportation", "urban"]
    
    # Obtain the filtered & extracted keywords csv file
    csv_file = "../data/syn_data_30.csv"
    filtered_csv_file = csv_file[:-4] + '_filter.csv' if csv_file.endswith('.csv') else csv_file + '_filter.csv'
    scored_csv_file = filtered_csv_file[:-4] + '_scored.csv' if filtered_csv_file.endswith('.csv') else filtered_csv_file + '_scored.csv' 
    init_input_csv(csv_file, filtered_csv_file, keywords)

    # Send the filtered csv file to the front-end for display
    # TODO: Create csv --> json and send to the front-end for display
    
    if automated_scoring: 
        assign_sentiment_scores(filtered_csv_file, scored_csv_file)
    
    # TODO: csv --> json to automatically populate the front-end with the sentiment scores

    app.run(debug=True)
