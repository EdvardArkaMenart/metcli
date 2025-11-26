import json
import urllib3
import os
from datetime import timedelta, date

cities = {
    "arendal": (58.46, 8.77),
    "bergen": (60.39, 5.32),
    "bodø": (67.28, 14.40),
    "drammen": (59.74, 10.20),
    "fredrikstad_sarpsborg": (59.21, 10.94),
    "gjøvik": (60.79, 10.69),
    "halden": (59.13, 11.38),
    "hamar": (60.79, 11.06),
    "haugesund": (59.41, 5.26),
    "kristiansand": (58.15, 8.01),
    "larvik": (59.05, 10.02),
    "moss": (59.42, 10.69),
    "oslo": (59.91, 10.75),
    "porsgrunn_skien": (59.13, 9.65),
    "sandefjord": (59.13, 10.21),
    "stavanger_sandnes": (58.97, 5.73),
    "tromsø": (69.64, 18.95),
    "trondheim": (63.43, 10.39),
    "tønsberg": (59.26, 10.40),
    "ålesund": (62.47, 6.14)
}

def filter_temperatures(forecast_data): 
    temperatures = []
    # henter timeseries array
    timeseries = json.loads(forecast_data).get("properties").get("timeseries")
    # set up datetime variables
    tomorrow = date.today() + timedelta(days=1)

    # Filtrerer timeseries, return nice dict
    for t in timeseries:
        # t["time"] inneholder dette formatet: 2025-11-10T23:00:00Z
        measured_time = t["time"]
    
        # extract first 10 chars
        measured_date = date.fromisoformat( measured_time[0:10])

        # sammenligne dato fra måling med dato for i morgen
        if  measured_date == tomorrow:
            measured_temperature = t["data"].get("instant").get("details").get("air_temperature")
            d = dict(time =  measured_time, temp = measured_temperature)
            temperatures.append((d))
    return(temperatures)

def get_cached_data(city_name):
    # leser json data fra fil 
    file_cache = f"cache\\{city_name}.json"
    with open(file_cache, 'r') as file:
        d = file.read()
    return(d)

def get_city_name(city_index, city_list):
    city_name = False
    if city_index >= 1 and city_index <= len(city_list):
        for index, city in enumerate(city_list, start = 1):
            if city_index == index:
                city_name = city
                return(city_name)
    else:
        # ugyldig valg
        print("Kan ikke finne en by med tallet", str(city_index))
        return(False)

# parse input og returner int, str eller bool 
def get_command():
    i = input("Velg by ved å taste inn ett tall, [L] for å vise byer: ")
    if not i:
        return(False)
    if i.lower() == "l":
        return("l")
    else:
        try:
            int(i)
            city_index = str(i)
            return(city_index)
        except ValueError:
            print("ugyldig valg du må skrive ett tall")
            return(False)

def get_coordinates(city_name):
    try:
        city_coordinates = cities[city_name]
    except KeyError:
        print("Kan ikke finne en by med navnet:", city_name)
        return(False)
    return(city_coordinates)
    
def get_file_date(city_name):
    # Get the last modification time
    file_path = f"cache\\{city_name}.json"
    try:
        modification_timestamp = os.path.getmtime(file_path)
        modified_date = date.fromtimestamp(modification_timestamp)
        return(modified_date)
    except FileNotFoundError:
        pass

def get_forecast(city_name):
    # Utfør HTTP request, returner forecast_data
    url = get_url(city_name)
    weather_data = met_api_get(url)
    write_city_weather_file(weather_data, city_name)
    d = get_cached_data(city_name)
    return(d)

def get_temperatures(city_name): 
    # Valider cache, last ned nye data hvis cache er invalid
    if validate_cache(city_name):
        forecast_data = get_cached_data(city_name)
        print("up to date")
    else:
        forecast_data = get_forecast(city_name)
        print("expired")
    return(filter_temperatures(forecast_data))

def get_url(city_name):
    # Henter ut cordinatene fra cities og legger dem til i en url
    coordinates = cities[city_name]
    latitude = coordinates[0]
    longitude = coordinates[1]
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}&lon={longitude}"
    return(url) 

def make_city_list():
    return(cities.keys())       

def met_api_get(url):
    # Utfør http request
    headers = {"User-Agent": "metcli/1.0 github.com/EdvardArkaMenart/metcli"}
    api_response = urllib3.request("GET", url, headers=headers)
    json_data = json.loads(api_response.data.decode("utf-8"))
    data = json.dumps(json_data)
    return(data)
    
def print_temperatures(temperatures : dict): 
    # Print nice dict
    for f in temperatures:
        f["time"] = f["time"].replace("T", " KL: ")
        f["time"] = f["time"].replace("00Z", "")
        num_chars_to_remove = 10
        # Using string slicing
        time_for_display = f["time"][num_chars_to_remove:]
        # converting measured_temp from float to string
        measured_temp = str(f["temp"])
        # using f str to set up the output
        tabel = f"{time_for_display} {measured_temp:>8} grader"
        print(tabel)

def show_cities(city_list):
    for x, y in enumerate(city_list, start = 1):
        print(f"{x:>3} {y.capitalize()} ")

def validate_cache(city_name): 
    # Sjekk timestamp på fil mot dagens dato
    file_date = get_file_date(city_name)
    if file_date == date.today():
        return(True)
    else:
        return(False)

def write_city_weather_file(weather_data, city_name):
    # write/overwrite a cities forecast file
    file_cache = f"cache\\{city_name}.json"
    with open(file_cache, 'w') as file:
        file.write(weather_data)
      