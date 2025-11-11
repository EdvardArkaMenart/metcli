# call convert_data if file is too old

import json
from datetime import timedelta, date

num_chars_to_remove = 10
today = date.today()
tomorrow = today + timedelta(days=1)

# take user input and loop until one of the if statements are true
while True:
    #city_name = input("Tast in et bynavn i Norge med stor forbokstav: ")
    city_name = "Oslo"
    # open the cities file if valid city_name
    if city_name == "Oslo": 
        #check if the cities file is too old, if it is make convert_data get a new one
        with open('filtered_data_oslo.json', 'r') as file:
            forecast_tomorrow = file.read()
            break
    elif city_name == "Bergen":
        pass
    else:
        print("Kan ikke finne en by med navnet:", city_name)    

print("temperatur for", city_name, tomorrow.strftime("%d, %m, %Y"))
data = json.loads(forecast_tomorrow)

# filtrerer dataen og viser den i en tabel
for f in data:
    f["time"] = f["time"].replace("T", " KL: ")
    f["time"] = f["time"].replace("00Z", "")
    
    # Using string slicing
    time_for_display = f["time"][num_chars_to_remove:]
    # converting measured_temp from float to string
    measured_temp = str(f["temp"])
    # using f str to set up the output
    tabel = f"{time_for_display}\t {measured_temp} grader"
    print(tabel)