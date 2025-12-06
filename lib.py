# Ta med 6 dager til fra daten
# Beholde time for time outputen for i morgen og lag en som viser 4 perioder for alle dagene
# Rengn snittemperatur for hele dagen og timeperioden og ta det med i outputen
# vis laveste og høyeste periode 

import json
import urllib3
import os
import math
from datetime import timedelta, date, datetime

DAY_VIEW = 1
WEEK_VIEW = 2
TEMP = 1
PRECIPITATION = 2
WIND_SPEED = 3
RESET = "\033[0m"
RED = "\033[31m"
time_periods = ["00", "06", "12", "18"]

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

def dump_dict(h: dict):
    print(json.dumps(h, indent=4))

def filter_temperatures1d(forecast_data):
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
        measured_date = date.fromisoformat(measured_time[0:10])
        # sammenligne dato fra måling med dato for i morgen
        if  measured_date == tomorrow:
            if "next_6_hours" in t["data"]:
                precipitation = t["data"].get("next_6_hours").get("details").get("precipitation_amount")
            wind_speed = t["data"].get("instant").get("details").get("wind_speed")
            measured_temperature = t["data"].get("instant").get("details").get("air_temperature")
            d = dict(time = measured_time, temp = measured_temperature, wind_speed = wind_speed, precipitation = precipitation)
            temperatures.append((d))
    return(temperatures)

def filter_temperatures7d(forecast_data):  
    days = {}
    # henter timeseries array
    timeseries = json.loads(forecast_data).get("properties").get("timeseries")
    # set up datetime variables
    tomorrow = date.today() + timedelta(days=1)
    seven_dates = get_seven_dates(tomorrow)
    # prep days
    for t in timeseries:
        # t["time"] inneholder dette formatet: 2025-11-10T23:00:00Z
        measured_time = t["time"]
        # extract positions 12-13
        measured_hour = measured_time[11:13]
        # extract first 10 chars
        current_date = measured_time[0:10]
        if (date.fromisoformat(current_date) in seven_dates):
            days[current_date] = {}

    # build days dict
    for d in days.keys():
        day_periods = {}
        for t in timeseries:
            measured_time = t["time"]
            current_date = measured_time[0:10]
            measured_hour = measured_time[11:13]
            # tar ut riktige time perioder
            if (d == current_date) and (measured_hour in time_periods):
                day_periods[measured_hour] = get_period_data(t)
                days[d] = day_periods
    return(days)

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
def get_command(i):
    if not i:
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
                print("Ugyldig valg: du må skrive ett tall fra listen")
                return(False)
    if i == "variabler":
        parameter_list = [1, 2, 3]
        print("Angi ønskede felter (1. temperatur, 2. vind, 3. nedbør) eks: 1 2 3: ")
        try:
            i = [int(x) for x in input().split()]
        except ValueError:
            print("Ugyldig valg: felter må angis som en liste separert med mellomrom")
            return(False)
        if not i:
            return(False)
        else:   
            if set(i).isdisjoint(parameter_list):
                return(False)
            else:
                return(i)                    
    if i:
        i = input("[T] for vær i morgen. [W] for 7 dager fra og med i morgen:")
        if not i:
            return(False)
        if i.lower() == "t":
            return(DAY_VIEW)
        if i.lower() == "w":
            return(WEEK_VIEW)
        else:
            print("Ugyldig valg: bare [T] og [W] er gyldig")
            return(False)
        
def get_coordinates(city_name):
    city_coordinates = cities[city_name] 
    return(city_coordinates)

def get_date(d):
    tomorrow = date.today() + timedelta(days=d)
    return(tomorrow)

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

def get_forecast_data(city_name): 
    # Valider cache, last ned nye data hvis cache er invalid
    if validate_cache(city_name):
        forecast_data = get_cached_data(city_name)
    else:
        forecast_data = get_forecast(city_name)
    return(forecast_data)

def get_period_data(period_data):
    period = {}
    if "next_6_hours" in period_data["data"]:
        maximum_temp = period_data["data"].get("next_6_hours").get("details").get("air_temperature_max")
        minimum_temp = period_data["data"].get("next_6_hours").get("details").get("air_temperature_min")
        a = round((maximum_temp + minimum_temp) / 2, 1)
        period = dict(max_temp = maximum_temp, min_temp = minimum_temp, average = a)
    return(period)

def get_seven_dates(tomorrow):
    # lager en liste med syv datoer
    seven_dates = []
    for i in range(7):
        current_date = tomorrow + timedelta(days=i)
        seven_dates.append(current_date)
    return seven_dates

def get_url(city_name):
    # Henter ut cordinatene fra cities og legger dem til i en url
    coordinates = cities[city_name]
    latitude = coordinates[0]
    longitude = coordinates[1]
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={latitude}&lon={longitude}"
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

def print_graph(temperatures, day):
    # printer tabellen for dagen
    day_averages = []
    day_max = []
    day_min = []
    day_str = str(day)
    month = day.strftime("%B")
    display_day = day.strftime("%A")
    day_of_month = day.strftime("%d")
    year = day.strftime("%Y")
    for t in temperatures.keys():
        # bruker dataen til den relevante datoen
        if t == day_str:
            for p in time_periods:
                day_averages.append(temperatures[day_str].get(p).get("average"))
                maxi = temperatures[day_str].get(p).get("max_temp")
                day_max.append(math.ceil(maxi))
                mini = temperatures[day_str].get(p).get("min_temp")
                day_min.append(math.floor(mini))
            day_average_sum = sum(day_averages)
            day_average = round(day_average_sum / 4)
            print(f"{display_day.capitalize()} {day_of_month}. {month} {year} (snittemperatur {day_average} grader)")
            print(f"00-06: fra {day_min[0]:.0f} til {day_max[0]:.0f} grader (snittemperatur {day_averages[0]:.1f} grader)")
            print(f"06-12: fra {day_min[1]:.0f} til {day_max[1]:.0f} grader (snittemperatur {day_averages[1]:.1f} grader)")
            print(f"12-18: fra {day_min[2]:.0f} til {day_max[2]:.0f} grader (snittemperatur {day_averages[2]:.1f} grader)")
            print(f"18-00: fra {day_min[3]:.0f} til {day_max[3]:.0f} grader (snittemperatur {day_averages[3]:.1f} grader)")
            print("")

def print_temperatures(temperatures : dict, mode, params):
    if mode == DAY_VIEW: 
        # Print nice dict
        for f in temperatures:
            mm = ""
            p_txt = ""
            w_txt = ""
            m_txt = ""
            measured_temp = ""
            wind_speed = "" 
            precipitation = ""
            f["time"] = f["time"].replace("T", "")
            f["time"] = f["time"].replace("00Z", "")
            num_chars_to_remove = 10
            # Using string slicing
            time_for_display = f["time"][num_chars_to_remove:]
            if TEMP in params:
                # converting measured_temp from float to string
                measured_temp = str(f["temp"])
                m_txt = " grader"
            if WIND_SPEED in params:
                wind_speed = str(f["wind_speed"])
                w_txt = " regn"
                mm = "mm"
            if PRECIPITATION in params:
                precipitation = str(f["precipitation"])
                p_txt = " m/s"
            # using f str to set up the output
            tabel = f"KL {RED}{time_for_display}{measured_temp:>4}{RESET}{m_txt}{RED}{wind_speed:>4}{mm}{RESET}{w_txt}{RED}{precipitation:>4}{RESET}{p_txt}"
            print(tabel)
    if mode == WEEK_VIEW:
        # loop gjennom 7 dager
        for s in range(1, 8):
            day = get_date(s)
            print_graph(temperatures, day)

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
      