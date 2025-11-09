import json
from datetime import timedelta, date

temps = []

# Open and read entire file
with open('test_json.txt', 'r') as file:
    file_content = file.read()

# henter timeseries array
timeseries = json.loads(file_content).get("properties").get("timeseries")

# set up datetime variables
tomorrow = date.today() + timedelta(days=1)

# filtrere målinger på dato
for t in timeseries:
    # t["time"] inneholder dette formatet: 2025-11-10T23:00:00Z
    mtime = t["time"]
    
    # extract first 10 chars
    mdate = date.fromisoformat(mtime[0:10])

    # sammenligne dato fra måling med dato for i morgen
    if mdate == tomorrow:
        mtemp = t["data"].get("instant").get("details").get("air_temperature")
        d = dict(time = mtime, temp = mtemp)
        temps.append((d))

# skriv json data til fil    
with open("filtered_data.json", "w") as f:
    f.write(json.dumps(temps))  


