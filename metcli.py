# Hente værdata
# Filtrere data
# Vis datasett

from datetime import timedelta, date
from lib import *

today = date.today()
tomorrow = today + timedelta(days=1)
city_list = make_city_list()
DAY_VIEW = 1
WEEK_VIEW = 2
show_cities(city_list)
 
# main loop
while True:
    # velg by  
    i = None
    command = get_command(i)
    if command == "l":
        show_cities(city_list)
        continue
    else:
        city_index = int(command)
    if not city_index:
        continue
    city_name = get_city_name(city_index, city_list)
    if not city_name:
        continue
    # velg modus (1d/7d)
    mode = False
    while mode is False:
        mode = get_command(command)
    # finn koordinater for by
    coordinates = get_coordinates(city_name)   
    # viser værdata for i morgen 
    if mode == DAY_VIEW:
        # sjekk om man har gyldig koordinater
        if coordinates:
            forecast_data = get_forecast_data(city_name)
            temperatures = filter_temperatures1d(forecast_data)
            print("temperatur for", city_name,"den", tomorrow.strftime("%d, %m, %Y"))
            print_temperatures(temperatures, mode)
    # viser værdata for syv dager
    if mode == WEEK_VIEW:
        if coordinates:
            forecast_data = get_forecast_data(city_name)
            temperatures = filter_temperatures7d(forecast_data)
            print_temperatures(temperatures, mode)
