import csv
import json
import argparse

def csv_to_json(input_file, output_file):
    data = []
    with open(input_file, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    with open(output_file, "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV to JSON")
    parser.add_argument("input_csv", type=str, help="Path to the input CSV file")
    parser.add_argument("output_json", type=str, help="Path to the output JSON file")
    args = parser.parse_args()

    csv_to_json(args.input_csv, args.output_json)
