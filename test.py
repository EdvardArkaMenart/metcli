import urllib3
import json
import datetime
from datetime import datetime, timedelta

temps = list(())
api_endpoint = "https://api.met.no/weatherapi/locationforecast/2.0/"
query = "compact?lat=59.91&lon=10.75"
x = 0
today = datetime.now()

resp = urllib3.request("GET", api_endpoint + query)
json_data = json.loads(resp.data.decode("utf-8"))
timeseries = json_data.get("properties").get("timeseries")
tomorrow = today + timedelta(days=1)
print("temperatur for i morgen den", tomorrow.strftime("%d, %m, %Y"))

for t in timeseries:
    mtime = t["time"]
    mtemp = t["data"].get("instant").get("details").get("air_temperature")
    d = dict(time = mtime, temp = mtemp)
    d["time"] = d["time"].replace("T", " KL: ")
    d["time"] = d["time"].replace("00Z", "")
    d["data"] = int(t["data"].get("instant").get("details").get("air_temperature"))
    temps.append((d))

for h in temps:
    print(temps[x])
    x += 1
    
#print(temps)