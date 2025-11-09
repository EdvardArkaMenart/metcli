import urllib3
import json

api= urllib3.request("get", "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.91&lon=10.75")
json_data = json.loads(api.data.decode("utf-8"))
data = json.dumps(json_data)

with open('test_json.txt', 'w') as file:
    file.write(data)
# File automatically closes after the 'with' block