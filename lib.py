import json
from datetime import timedelta, date

def filter_temperatures(forecast_data): 
    temperatures = []
    # henter timeseries array
    timeseries = json.loads(forecast_data).get("properties").get("timeseries")
    # set up datetime variables
    #tomorrow = date.today() + timedelta(days=1)
    tomorrow = date(2025, 11, 17)

    #Filtrerer timeseries, return nice dict
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

def get_forecast(city_name):
    #Utfør HTTP request, returner forecast_data
    file_coordinates = f"coordinates\\coords.txt"
    with open(file_coordinates, 'r') as file:
        c = file.read()
        city_coordinates = json.loads(file_coordinates).get(city_name)
    print(city_coordinates)

def get_temperatures(city_name): 
    #Valider cache, last ned nye data hvis cache er invalid
    if validate_cache(city_name):
        forecast_data = get_cached_data(city_name)
    else:
        forecast_data = get_forecast(city_name)
    #return(filter_temperatures(forecast_data))

def met_api_get(url):
    #Utfør http request
    pass

def print_temperatures(temperatures : dict): 
    #Print nice dict
    for f in temperatures:
        f["time"] = f["time"].replace("T", " KL: ")
        f["time"] = f["time"].replace("00Z", "")
        width = 10
        num_chars_to_remove = 10
        # Using string slicing
        time_for_display = f["time"][num_chars_to_remove:]
        # converting measured_temp from float to string
        measured_temp = str(f["temp"])
        # using f str to set up the output
        tabel = f"{time_for_display} {measured_temp.rjust(width)} grader"
        print(tabel)

def validate_cache(city_name): 
    #Sjekk timestamp på fil mot dagens dato
    return(False)
