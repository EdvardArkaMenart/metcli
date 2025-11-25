# Hente værdata
# Filtrere data
# Vis datasett

from datetime import timedelta, date
from lib import get_temperatures, print_temperatures, get_coordinates, make_city_list, get_city_name, get_command, show_cities

today = date.today()
tomorrow = today + timedelta(days=1)
city_list = make_city_list()

show_cities(city_list)
 
# main loop
while True:
    # print byliste   
    command = get_command()
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
    # finn koordinater for by
    coordinates = get_coordinates(city_name)  
    # sjekk om man har gyldig koordinater
    if coordinates:
        temperatures = get_temperatures(city_name)
        print("temperatur for", city_name,"den", tomorrow.strftime("%d, %m, %Y"))
        print_temperatures(temperatures)
