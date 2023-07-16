import argparse
import csv

class Applicant:
    def __init__(self, name, score, pref, date, status):
        self.name = name
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

def new_applicant(name, score, pref, date, status):
    return Applicant(name, score, pref, date, status)

def new_org(name, index, spots):
    return Org(name, index, spots)

def applicant_list(file):
    applicants = []
    with open(file, "r", newline="") as pizfile:
        reader = csv.reader(pizfile)
        next(reader)  # Skip the header row
        for line in reader:
            if "END" in line:
                continue  # Skip the line with "END"
            
            name, score, date, pref, status = line

            # Check if the score field is empty or invalid
            if not score.strip():
                score = 0.0  # Set a default value, you can change this as needed
            else:
                score = float(score)

            # Check if the date field is empty or invalid
            if not date.strip():
                date = 0  # Set a default value, you can change this as needed
            else:
                date = int(date)

            applicants.append(new_applicant(name, score, pref, date, status))
    return applicants


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

def main():
    parser = argparse.ArgumentParser(description="Applicant Assignment Program")
    parser.add_argument("applicant_file", type=str, help="Path to the applicant file")
    parser.add_argument("org_file", type=str, help="Path to the organization file")
    parser.add_argument("num_orgs", type=int, help="Number of organizations")
    args = parser.parse_args()

    orgarray = []
    spots = [0] * args.num_orgs

    with open(args.org_file, "r") as orgfile:
        for line in orgfile:
            tokens = line.strip().split(",")
            if tokens[0] == "END":
                break
            name, num_spots = tokens
            orgarray.append(new_org(name, len(orgarray), int(num_spots)))

    waitlist = "waitlist"
    applicants = applicant_list(args.applicant_file)

    print("Name,Date,Score,Preference,Assignment")
    while applicants:
        max_applicant = max(applicants, key=lambda x: (x.score, -x.date))
        applicants.remove(max_applicant)
        preftok = max_applicant.pref.split(";")

        matched = False
        for choice in preftok:
            if not choice:
                continue  # Skip empty choices
            choice = int(choice)
            if orgarray[choice].spots > 0:
                max_applicant.assignment = orgarray[choice].name
                orgarray[choice].spots -= 1
                matched = True
                break

        if not matched:
            max_applicant.assignment = waitlist

        print(f"{max_applicant.name},{max_applicant.date},{max_applicant.score},{max_applicant.pref},{max_applicant.assignment}")

    print("END")

if __name__ == "__main__":
    main()
