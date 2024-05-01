import random
import calendar
import csv
from datetime import datetime, timedelta

def random_date(min_year, max_year):
    # Generate a random year between min_year and max_year
    year = random.randint(min_year, max_year)
    
    # Generate a random month and day
    month = random.randint(1, 12)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:  # February
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):  # Leap year
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    
    # Create a datetime object for the generated date
    date_object = datetime(year, month, day)
    
    # Convert the datetime object to a timestamp
    timestamp = date_object.timestamp()
    
    return timestamp

def generate_player_input(rows, player=0):
    filename = "/home/martin/Masterarbeit/MP-SPDZ_latest/Player-Data/Input-P{}-0".format(player)
    with open(filename, "w") as file:
        for i in range(1, rows + 1):
            year = random.randint(1900, 2100),
            timestamp = int(random_date(year[0], 2100))
            data = [
                i,
                random.randint(1, 10),
                year[0],
                random.randint(1, 10),
                random.randint(0, 1),
                random.randint(0, 1),
                random.randint(0, 1),
                random.randint(0, 1),
                int(random.uniform(0, 1000)),
                random.randint(0, 1),
                timestamp,
                int(random.uniform(0, 1000)),
                int(random.uniform(0, 1000))
            ]
            file.write(" ".join(map(str, data)) + "\n")

def fill_medication_csv(filename, site):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for _ in range(1000000):
            random_year = str(random.randint(2000, 2022))
            random_month = random.randint(1, 12)
            max_day = calendar.monthrange(int(random_year), random_month)[1]  # Maximum number of days in the random month
            random_day = random.randint(1, max_day)  # Random day within the valid range for the random month
            last_column_date = datetime(int(random_year), random_month, random_day)

            row = [
                str(random.randint(1, 10)),  # First column (random number between 1 and 10)
                '7',  # Second column (fixed value of 7)
                random_year,  # Third column (random year between 2000 and 2022)
                str(random_month),  # Fourth column (random month between 1 and 12)
                'aspirin',  # Fifth column (fixed value of 'aspirin')
                '10 mg',  # Sixth column (fixed value of '10 mg')
                'oral',  # Seventh column (fixed value of 'oral')
                last_column_date.strftime('%y/%m/%d')  # Eighth column (random date in the last 10 years with the same year as the third column)
            ]
            writer.writerow(row)

def fill_diagnoses_csv(filename, site):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for _ in range(1000000):
            # Generate random data for the row
            random_year = str(random.randint(2000, 2022))
            random_month = random.randint(1, 12)
            max_day = calendar.monthrange(int(random_year), random_month)[1]  # Maximum number of days in the random month
            random_day = random.randint(1, max_day)  # Random day within the valid range for the random month
            last_column_date = datetime(int(random_year), random_month, random_day)

            # Choose between 008.45 and 414.01 for the eighth column
            eighth_column_value = random.choice(['008.45', '414.01'])

            row = [
                str(random.randint(1, 10)),  # First column (random number between 1 and 10)
                '4',  # Second column (fixed value of 4)
                random_year,  # Third column (random year between 2000 and 2022)
                str(random.randint(1, 12)),  # Fourth column (random month between 1 and 12)
                '1', '1', '1', '1',  # Fifth to eighth columns (fixed value of 1)
                eighth_column_value,  # Ninth column (either 008.45 or 414.01)
                '1',  # Tenth column (fixed value of 1)
                last_column_date.strftime('%y/%m/%d'),  # Eleventh column (random date in the last 10 years with the same year as the third column)
                '{:.2f}'.format(random.uniform(100, 500)),  # Twelfth column (random float between 100 and 500 with two decimal places)
                '{:03d}'.format(random.randint(1, 999))  # Thirteenth column (random integer between 1 and 999 with leading zeros)
            ]
            writer.writerow(row)

# generate_player_input(100000000, player=0)
# generate_player_input(100000000, player=1)
# generate_player_input(100000000, player=2)

fill_medication_csv(
    "/home/martin/Masterarbeit/duckdb/testData/1/medications.csv",
    site=4
)
fill_medication_csv(
    "/home/martin/Masterarbeit/duckdb/testData/2/medications.csv",
    site=7
)
fill_diagnoses_csv(
    "/home/martin/Masterarbeit/duckdb/testData/1/diagnoses.csv",
    site=4
)
fill_diagnoses_csv(
    "/home/martin/Masterarbeit/duckdb/testData/2/diagnoses.csv",
    site=7
)