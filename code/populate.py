#!/usr/bin/env python3

import os
import random
import calendar
import csv
import click
import sys
from datetime import datetime

def random_date(min_year: int, max_year: int) -> float:
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

def generate_player_input(filename: str, rows: int) -> None:
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
                random.choice([8, 414]),
                random.randint(0, 1),
                timestamp,
                int(random.uniform(0, 1000)),
                int(random.uniform(0, 1000))
            ]
            file.write(" ".join(map(str, data)) + "\n")

def fill_medication_csv(filename: str, site: int, rows: int) -> None:
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for _ in range(rows):
            random_year = str(random.randint(2000, 2022))
            random_month = random.randint(1, 12)
            max_day = calendar.monthrange(int(random_year), random_month)[1]  # Maximum number of days in the random month
            random_day = random.randint(1, max_day)  # Random day within the valid range for the random month
            last_column_date = datetime(int(random_year), random_month, random_day)

            row = [
                str(random.randint(1, 10)),  # First column (random number between 1 and 10)
                site,  # Second column (fixed value of 7)
                random_year,  # Third column (random year between 2000 and 2022)
                str(random_month),  # Fourth column (random month between 1 and 12)
                'aspirin',  # Fifth column (fixed value of 'aspirin')
                '10 mg',  # Sixth column (fixed value of '10 mg')
                'oral',  # Seventh column (fixed value of 'oral')
                last_column_date.strftime('%y/%m/%d')  # Eighth column (random date in the last 10 years with the same year as the third column)
            ]
            writer.writerow(row)

def fill_diagnoses_csv(filename: str, site: int, rows: int) -> None:
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for _ in range(rows):
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
                site,  # Second column (fixed value of 4)
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

def generate_player_input_union(filename: str, rows: int) -> None:
    files = [f"{filename}/Input-P{player}-0" for player in [0,1,2]]
    
    # Erstelle einen zentralen Pool von eindeutigen IDs für alle Dateien
    total_ids = rows * len(files)
    all_ids = list(range(1, total_ids + 1))
    random.shuffle(all_ids)  # Mische die IDs
    
    for idx, player_file in enumerate(files):
        with open(player_file, "w") as file:
            # Bestimme die IDs für diese Datei
            file_ids = all_ids[idx * rows:(idx + 1) * rows]
            
            for i in file_ids:
                year = random.randint(1900, 2100)
                timestamp = int(random_date(year, 2100))
                data = [
                    i,
                    random.randint(1, 10),
                    year,
                    random.randint(1, 10),
                    random.randint(0, 1),
                    random.randint(0, 1),
                    random.randint(0, 1),
                    random.randint(0, 1),
                    random.choice([8, 414]),
                    random.randint(0, 1),
                    timestamp,
                    int(random.uniform(0, 1000)),
                    int(random.uniform(0, 1000))
                ]
                file.write(" ".join(map(str, data)) + "\n")

@click.command()
@click.argument("system", type=click.Choice(["db", "secure", "union"]), required=True)
@click.argument("max_rows", type=int, required=True)
def main(system: str, max_rows: int) -> None:
    pwd = os.getcwd()
    if system == "db":
        if not os.path.exists(f"{pwd}/duckdb"):
            click.echo(f'Directory "{pwd}/duckdb" could not be found!')
            sys.exit()
        fill_medication_csv(
            f"{pwd}/duckdb/testData/1/medications.csv",
            site=4,
            rows=max_rows
        )
        fill_medication_csv(
            f"{pwd}/duckdb/testData/2/medications.csv",
            site=7,
            rows=max_rows
        )
        fill_diagnoses_csv(
            f"{pwd}/duckdb/testData/1/diagnoses.csv",
            site=4,
            rows=max_rows
        )
        fill_diagnoses_csv(
            f"{pwd}/duckdb/testData/2/diagnoses.csv",
            site=7,
            rows=max_rows
        )
    elif system == "secure":
        if not os.path.exists(f"{pwd}/MP-SPDZ/Player-Data"):
            click.echo(f'Directory "{pwd}/MP-SPDZ/Player-Data" could not be found!')
            sys.exit()
        generate_player_input(f"{pwd}/MP-SPDZ/Player-Data/Input-P0-0", max_rows)
        generate_player_input(f"{pwd}/MP-SPDZ/Player-Data/Input-P1-0", max_rows)
        generate_player_input(f"{pwd}/MP-SPDZ/Player-Data/Input-P2-0", max_rows)
    elif system == "union":
        if not os.path.exists(f"{pwd}/MP-SPDZ/Player-Data"):
            click.echo(f'Directory "{pwd}/MP-SPDZ/Player-Data" could not be found!')
            sys.exit()
        generate_player_input_union(f"{pwd}/MP-SPDZ/Player-Data/", max_rows)

if __name__ == "__main__":
    main()