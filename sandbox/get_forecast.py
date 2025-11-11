# only call when forecast mesurements are old

import urllib3
import json
from print_data import city_name

api = "https://api.met.no/weatherapi/locationforecast/2.0/"
oslo = "compact?lat=59.91&lon=10.75"

#city_name = input("Tast in bynavn: ")

# get forecast for a city
def city_finder(city):
    api_response = urllib3.request("get",api + city)
    json_data = json.loads(api_response.data.decode("utf-8"))
    data = json.dumps(json_data)
    return data

# put the cities forecast in a txt file
if city_name == "Oslo":
    city = oslo
    city_finder(city)
    forecast = city_finder()
    with open('Oslo_forecast.txt', 'w') as file:
        file.write(forecast)
    # File automatically closes after the 'with' block

