import csv
import json
import sys

def csv_to_json(csv_data):
    data = []
    for row in csv_data:
        data.append(dict(zip(row[0::2], row[1::2])))

    return json.dumps(data)

def main():
    csv_data = sys.stdin.readlines()
    json_data = csv_to_json(csv_data)
    print(json_data)

if __name__ == '__main__':
    main()
