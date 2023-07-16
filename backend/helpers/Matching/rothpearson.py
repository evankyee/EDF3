import argparse

class Applicant:
    def __init__(self, name, score, pref, date):
        self.name = name
        self.score = score
        self.pref = pref
        self.date = date
        self.next = None
        self.assignment = None


class Org:
    def __init__(self, name, index, spots):
        self.name = name
        self.index = index
        self.spots = spots


def new_applicant(name, score, pref, date):
    return Applicant(name, score, pref, date)


def new_org(name, index, spots):
    return Org(name, index, spots)


def applicant_list(file):
    applicants = []
    with open(file, "r") as pizfile:
        for line in pizfile:
            tokens = line.strip().split(",")
            if tokens[0] == "END":
                break
            name, score, date, pref = tokens
            applicants.append(new_applicant(name, float(score), pref, int(date)))
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

        print(f"Name: {max_applicant.name} Date Submitted: {max_applicant.date} "
              f"Score: {max_applicant.score} Assignment: {max_applicant.assignment}")


if __name__ == "__main__":
    main()
