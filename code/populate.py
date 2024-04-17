import random
from datetime import datetime

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

def generate_player_input(rows, player_file=0):
    with open("./Player-Data/Input-P{}-0".format(player_file), "w") as file:
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

generate_player_input(50, player_file=0)
generate_player_input(50, player_file=1)
generate_player_input(50, player_file=2)