# Hente værdata
# Filtrere data
# Vis datasett

# call convert_data if file is too old

from datetime import timedelta, date
from lib import get_temperatures, print_temperatures, get_coordinates

today = date.today()
tomorrow = today + timedelta(days=1)

# main loop
while True:

    
    i = input("Tast in et bynavn i Norge: ")
    city_name = i.lower()
    # finn koordinater for by
    coordinates = get_coordinates(city_name)  
    # sjekk om man har gyldig koordinater
    if coordinates:
        temperatures = get_temperatures(city_name)
        print("temperatur for", city_name,"den", tomorrow.strftime("%d, %m, %Y"))
        print_temperatures(temperatures)
