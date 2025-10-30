import urllib3
import json

temps = list(())
api_endpoint = "https://api.met.no/weatherapi/locationforecast/2.0/"
query = "compact?lat=59.91&lon=10.75"

resp = urllib3.request("GET", api_endpoint + query)
json_data = json.loads(resp.data.decode("utf-8"))
timeseries = json_data.get("properties").get("timeseries")

for t in timeseries:
    mtime = t["time"]
    mtemp = t["data"].get("instant").get("details").get("air_temperature")
    d = dict(time = mtime, temp = mtemp)
    temps.append((d))
    
print(temps)