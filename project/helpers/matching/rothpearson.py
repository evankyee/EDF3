import argparse
from datetime import datetime
import csv

class Applicant:
    def __init__(self, name, email, score, pref, date, status):
        self.name = name
        self.email = email
        self.score = score
        self.pref = pref
        self.date = date
        self.next = None
        self.assignment = status

class Org:
    def __init__(self, name, index, spots):
        self.name = name
        self.index = index
        self.spots = spots

def new_applicant(name, email, score, pref, date, status):
    return Applicant(name, score, pref, date, status)

def new_org(name, index, spots):
    return Org(name, index, spots)

def preprocess_applicant_file(input_file):
    processed_data = []

    with open(input_file, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            email = row['email']
            score = row['average_score']
            pref = row['pref']
            datetime = row['datetime']
            status = row['status']
            
            processed_data.append({
                'name': name,
                'email': email,
                'average_score': score,
                'pref': pref,
                'datetime': datetime,
                'status': status
            })

    return processed_data

def app_cmp(a, b):
    if a.score != b.score:
        return a.score - b.score
    else:
        return a.date - b.date

def remove(head, rem):
    if head == rem:
        return head.next

    current = head
    while current.next != rem:
        current = current.next

    current.next = rem.next
    return head

def apply_roth_pearson(applicant_filepath, org_filepath, output_filepath, num_orgs):
    orgarray = []
    spots = [0] * num_orgs

    with open(org_filepath, "r") as orgfile:
        next(orgfile)  # Skip the header row
        for line in orgfile:
            tokens = line.strip().split(",")
            if tokens[0] == "END":
                break
            org_id, org_name, num_spots = tokens
            orgarray.append(new_org(org_name, org_id, int(num_spots)))

    waitlist = "waitlist"
    applicants = preprocess_applicant_file(applicant_filepath)

    # print("Name,Date,Score,Preference,Assignment")
    with open(output_filepath, "w", newline="") as outfile:
        fieldnames = ["name", "email", "average_score", "pref", "datetime", "status"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        while applicants:
            max_applicant = max(applicants, key=lambda x: (x['average_score'], -datetime.timestamp(datetime.strptime(x['datetime'], "%Y-%m-%d %H:%M:%S"))))
            preftok = max_applicant['pref'].split(";")

            matched = False
            for choice in preftok:
                if not choice:
                    continue  # Skip empty choices
                choice = int(choice)
                if orgarray[choice].spots > 0:
                    max_applicant['status'] = orgarray[choice].name
                    orgarray[choice].spots -= 1
                    matched = True
                    break

            if not matched:
                max_applicant['status'] = waitlist

            # Write the updated data to the output matching file
            writer.writerow(max_applicant)

            applicants.remove(max_applicant)