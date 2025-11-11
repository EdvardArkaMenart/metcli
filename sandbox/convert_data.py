# uppdate file if print_data.py says it's too old

import json
from datetime import timedelta, date
from print_data import city_name

temperatures = []

# use user input from print_data to find and update the citeis file
if city_name == "Oslo":
# run get_forecast to update the forecast data for a specific city
# Open and read entire file
    with open('Oslo_forecast.txt', 'r') as file:
        file_content = file.read()
elif city_name == "Bergen":
    pass
# henter timeseries array
timeseries = json.loads(file_content).get("properties").get("timeseries")

# set up datetime variables
tomorrow = date.today() + timedelta(days=1)

# filtrere målinger på dato
for t in timeseries:
    # t["time"] inneholder dette formatet: 2025-11-10T23:00:00Z
    measured_time = t["time"]
    
    # extract first 10 chars
    measured_date = date.fromisoformat( measured_time[0:10])

    # sammenligne dato fra måling med dato for i morgen
    if  measured_date == tomorrow:
        measured_temperatur = t["data"].get("instant").get("details").get("air_temperature")
        d = dict(time =  measured_time, temp = measured_temperatur)
        temperatures.append((d))

# skriv json data til fil    
with open("filtered_data_oslo.json", "w") as f:
    f.write(json.dumps(temperatures))  


