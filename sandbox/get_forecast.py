# only call when forecast mesurements are old

import urllib3
import json
#from print_data import city_name

api = "https://api.met.no/weatherapi/locationforecast/2.0/compact?"
oslo = "lat=59.91&lon=10.75"
headers = {"User-Agent": "metcli/1.0 github.com/EdvardArkaMenart/metcli"}
city_name = "Oslo"
#city_name = input("Tast in bynavn: ")

# get forecast for a city
def city_finder(city):
    api_response = urllib3.request("GET", api + city, headers=headers)
    json_data = json.loads(api_response.data.decode("utf-8"))
    data = json.dumps(json_data)
    return data

# put the cities forecast in a txt file
if city_name == "Oslo":
    city = oslo
    forecast = city_finder(city)
    with open('Oslo_forecast.txt', 'w') as file:
        file.write(forecast)
    # File automatically closes after the 'with' block

