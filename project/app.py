from flask import Flask, render_template, jsonify
import pandas as pd
from helpers.csv_helpers import init_input_csv, parse_company_vacancies, read_matching_file, read_csv_to_dict_list 
from helpers.sentiment_helpers import assign_sentiment_scores
from helpers.matching.rothpearson import apply_roth_pearson 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import csv

app = Flask(__name__, template_folder='static/templates')

# Inherit the keywords needed for the keyword highlighting process 
# TODO: Enable inheriting form the frontend -- currently just declare
keywords = ["plastic", "law", "transportation", "urban"]
candidate_csv_file = "../data/syn_data_30.csv"
org_csv_file = "../data/org_info.csv"
filtered_csv_file = candidate_csv_file[:-4] + '_filter.csv' if candidate_csv_file.endswith('.csv') else candidate_csv_file + '_filter.csv'
scored_csv_file = filtered_csv_file[:-4] + '_scored.csv' if filtered_csv_file.endswith('.csv') else filtered_csv_file + '_scored.csv' 
output_matching_file = candidate_csv_file[:-4] + '_matching.csv' if candidate_csv_file.endswith('.csv') else candidate_csv_file+ '_matching.csv' 

@app.route('/applications')
def applications():
    # Replace 'applicants.csv' with the path to your CSV file containing applicant data
    applicants_data = read_csv_to_dict_list('../data/syn_data_30_filter.csv')
    return render_template('/applications.html', applicants=applicants_data, rawr="xd")

# TODO: Get the actual correct csv for this one
@app.route('/matching')
def matchings():
    matching_data = read_csv_to_dict_list(output_matching_file)
    company_vacancy_data = parse_company_vacancies(org_csv_file)

    # Update the company vacancy data based on who people get matched too
    for key, v in matching_data.items():
        company_vacancy_data[key] -= v
    return render_template('/matching.html', matchings=matching_data, company_vacancies=company_vacancy_data)

# TODO: Get the correct csvs for this one
@app.route('/interview')
def interview():
    # Replace 'applicants.csv' with the path to your CSV file containing applicant data
    applicants_data = read_csv_to_dict_list('../data/syn_data_30_filter.csv')
    return render_template('/interview.html', applicants=applicants_data)

# TODO: Get the correct csvs to this one
@app.route('/offer')
def offer():
    # Replace 'applicants.csv' with the path to your CSV file containing applicant data
    applicants_data = read_csv_to_dict_list('../data/syn_data_30_filter.csv')
    return render_template('/offer.html', applicants=applicants_data)

# TODO: Get the correct csvs to this one
@app.route('/onboarding')
def onboarding():
    # Replace 'applicants.csv' with the path to your CSV file containing applicant data
    applicants_data = read_csv_to_dict_list('../data/syn_data_30_filter.csv')
    return render_template('/onboarding.html', applicants=applicants_data)

@app.route('/turn_on_ai_scoring', methods=['POST'])
def turn_on_ai_scoring():
    # Add your backend logic here to handle the AI Scoring toggle
    # For example, you can update a global variable or database flag to indicate AI Scoring is on
    assign_sentiment_scores(filtered_csv_file, filtered_csv_file)

    # Respond with a success message or relevant data in JSON format
    return jsonify({'message': 'AI Scoring has been turned on successfully.'}), 200

if __name__ == '__main__':
    # Do all pre-processing steps of candidate csv file: (1) filter out ineligible people, assign unassigned statuses, and "-" scores 
    init_input_csv(candidate_csv_file, filtered_csv_file, keywords)

    # TODO: Add as a toggle behavior
    # Currently just assign_sentiment_scores directly because I want average_score to be there :)
    assign_sentiment_scores(filtered_csv_file, filtered_csv_file)
    
    # TODO: Get the rothpearson working correctly
    # TODO: Move this to a button trigger and check if there is both the two following csvs:
        # (1) the org_csv
        # (2) the _filter_scored.csv
    apply_roth_pearson(filtered_csv_file, org_csv_file, output_matching_file, 15)

    # TODO: Get the running of Roth Pearson repeatedly from refreshing the waitlist correctly
    app.run(debug=True)
