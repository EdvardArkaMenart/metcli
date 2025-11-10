import json
from datetime import timedelta, date

with open('filtered_data.json', 'r') as file:
    forecast_tomorrow = file.read()

num_chars_to_remove = 10
today = date.today()

data = json.loads(forecast_tomorrow)
tomorrow = today + timedelta(days=1)

print("temperatur for Oslo", tomorrow.strftime("%d, %m, %Y"))

# filtrerer dataen og viser den i en tabel
for f in data:
    f["time"] = f["time"].replace("T", " KL: ")
    f["time"] = f["time"].replace("00Z", "")
    
    # Using string slicing
    otime = f["time"][num_chars_to_remove:]
    # converting mtemp from float to string
    mtemp = str(f["temp"])
    # using f str to set upp the output
    tabel = f"{otime}\t {mtemp} grader"
    print(tabel)