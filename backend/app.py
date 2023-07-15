from flask import Flask, request, jsonify
import pandas as pd
from helpers.csv_helpers import filter_csv_by_degree, extract_keywords
from helpers.fuzzy_helpers import fuzzy_match
from helpers.sentiment_helpers import assign_sentiment_scores

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
    app.run(debug=True)
