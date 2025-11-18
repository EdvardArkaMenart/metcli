import json

cities = {
    "bergen": (0.0, 0.0),
    "oslo": (59.91, 10.75)
}
json_cities = json.dumps(cities)
with open('coords.txt', 'w') as file:
        file.write(json_cities)