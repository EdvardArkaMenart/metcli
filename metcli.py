# Hente værdata
# Filtrere data
# Vis datasett

# call convert_data if file is too old

import json
from datetime import timedelta, date
from lib import get_temperatures, print_temperatures

num_chars_to_remove = 10
today = date.today()
tomorrow = today + timedelta(days=1)
city_coordinates = None
cities = {
    "bergen": (0.0, 0.0),
    "oslo": (59.91, 10.75)
}
# main loop
while True:
    # take user input and loop
    while not city_coordinates:
        city_name = input("Tast in et bynavn i Norge: ")
        try:
            city_coordinates = cities[city_name.lower()]
            #print(city_coordinates)
        except KeyError:
            print("Kan ikke finne en by med navnet:", city_name)    

    temperatures = get_temperatures(city_name)
    #print("temperatur for", city_name,"den", tomorrow.strftime("%d, %m, %Y"))
    #print_temperatures(temperatures)
    break







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