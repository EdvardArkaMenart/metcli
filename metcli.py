# Hente værdata
# Filtrere data
# Vis datasett

# call convert_data if file is too old

import json
from datetime import timedelta, date
from lib import get_temperatures, print_temperatures, get_coordinates

num_chars_to_remove = 10
today = date.today()
tomorrow = today + timedelta(days=1)
city_name = None

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
    
    







    #with open('filtered_data_oslo.json', 'r') as file:
                #forecast_tomorrow = file.read()

    #print("temperatur for", city_name, tomorrow.strftime("%d, %m, %Y"))
    #data = json.loads(forecast_tomorrow)

    # filtrerer dataen og viser den i en tabel
    #for f in data:
        #f["time"] = f["time"].replace("T", " KL: ")
        #f["time"] = f["time"].replace("00Z", "")
    
        # Using string slicing
        #time_for_display = f["time"][num_chars_to_remove:]
        # converting measured_temp from float to string
        #measured_temp = str(f["temp"])
        # using f str to set up the output
        #tabel = f"{time_for_display}\t {measured_temp} grader"
        #print(tabel)   