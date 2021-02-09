import csv
import sys
import datetime
import glob

# A place to store shit.
bucket = {}

# Grab all the CSV files in this directory
csvfiles = glob.glob("*.csv")

# Iterate over all the CSV files to determine collect evidence.
for csvfile in csvfiles:
    with open(csvfile, newline='') as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row['Name']
            late = row['Lateness (H:M:S)']
            email = row['Email']
            key = f"{name} - {email}"

            if late != "0:00:00":

                if not key in bucket:
                    bucket[key] = []

                h, m, s = map(int, late.split(':'))
                dur = datetime.timedelta(hours=h, minutes=m, seconds=s)

                bucket[key].append(f"{csvfile} -- {dur}")

# Report students who are submitting late more than they should.
# Depending on how you want to handle this:
# (1) email student to let them know they are on the fence
# (2) email student that they are going to be penalized based on course contract
with open("report.md", "w") as f: 
    for k in sorted(bucket, key=lambda k: len(bucket[k]), reverse=True):
        # Determine if this student is an offender
        offender = ""
        times = len(bucket[k])
        if times <= 2:
            offender = "[SAFE]"
        elif times <= 3:
            offender = "[ON THE FENCE]"
        elif times <= 9:
            offender = "[OFFENDER]"

        # Write to the report for this student.
        # Use the their email to let them know of their lateness.
        f.write(f"# {k} {offender}\n")
        for i in bucket[k]:
            f.write(f"* {i}\n")
        f.write("\n")

