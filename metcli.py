from datetime import timedelta, date
from get_json import timeseries

temps = list(())
today = date.today()

tomorrow = today + timedelta(days=1)
print("temperatur for i morgen den", tomorrow.strftime("%d, %m, %Y"))

for t in timeseries:
    mtime = t["time"]
    mtemp = t["data"].get("instant").get("details").get("air_temperature")
    d = dict(time = mtime, temp = mtemp)
    temps.append((d))
    date_string = tomorrow.strftime("%Y-%m-%d")
    date_object = date.fromisoformat(date_string)

for h in temps:
    h["time"] = h["time"].replace("T", " KL: ")
    h["time"] = h["time"].replace("00Z", "")
    mtime = h["time"]
    mtemp = str(h["temp"])
    #print(h["time"], h["temp"])
    tabel = f"{mtime}\t {mtemp} grader"
    print(tabel)
#print(json.dumps(timeseries, indent=4))   
#print(type(tomorrow)) 
#print(temps)