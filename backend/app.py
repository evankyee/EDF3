from flask import Flask, request, jsonify, render_template
import pandas as pd
from helpers.csv_helpers import init_input_csv, parse_csv_to_dictionaries 
from helpers.fuzzy_helpers import fuzzy_match
from helpers.sentiment_helpers import assign_sentiment_scores
import helpers.matching.rothpearson as rothpearson
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__, template_folder='static/templates')

@app.route('/applications')
def applications():
    # Replace 'applicants.csv' with the path to your CSV file containing applicant data
    applicants_data = read_csv_to_dict_list('../data/syn_data_30_filter.csv')
    return render_template('/applications.html', applicants=applicants_data, rawr="xd")

# TODO: Get the actual correct csv for this one
@app.route('/matching')
def matchings():
    # Replace 'applicants.csv' with the path to your CSV file containing applicant data
    applicants_data = read_csv_to_dict_list('../data/syn_data_30_filter.csv')
    return render_template('/matching.html', applicants=applicants_data)

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

def read_csv_to_dict_list(csv_path):
    df = pd.read_csv(csv_path)
    return df.to_dict(orient='records')

if __name__ == '__main__':
    # Inherit the automated_scoring from the toggle on the front-end
    # TODO: Enable inheriting from the frontend -- currently just declare
    automated_scoring = True

    # Inherit the keywords needed for the keyword highlighting process 
    # TODO: Enable inheriting form the frontend -- currently just declare
    keywords = ["plastic", "law", "transportation", "urban"]
    
    candidate_csv_file = "../data/syn_data_30.csv"
    company_csv_file = "../data/company_info.csv"
    filtered_csv_file = candidate_csv_file[:-4] + '_filter.csv' if candidate_csv_file.endswith('.csv') else candidate_csv_file + '_filter.csv'
    scored_csv_file = filtered_csv_file[:-4] + '_scored.csv' if filtered_csv_file.endswith('.csv') else filtered_csv_file + '_scored.csv' 

    # Do all pre-processing steps of candidate csv file: (1) filter out ineligible people, assign unassigned statuses, and "-" scores 
    init_input_csv(candidate_csv_file, filtered_csv_file, keywords)

    # TODO: Check if the overwriting process is ok
    if automated_scoring: 
        assign_sentiment_scores(filtered_csv_file, filtered_csv_file)
    
    # Do pre-processing of the id_to_company & vacancies_to_company from the company_csv_file
    id_to_company, vacancies_to_company = parse_csv_to_dictionaries(company_csv_file)

    # TODO: Get the rothpearson working correctly
    rothpearson.main()

    app.run(debug=True)
