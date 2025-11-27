import json
import urllib3
from datetime import date, timedelta

#url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=62.47&lon=6.14"
#url = "https://api.met.no/weatherapi/locationforecast/2.0/complete?lat=-16.516667&lon=-68.166667&altitude=4150"
#headers = {"User-Agent": "metcli/1.0 github.com/EdvardArkaMenart/metcli"}
#api_response = urllib3.request("GET", url, headers=headers)
#json_data = json.loads(api_response.data.decode("utf-8"))
#print(json.dumps(json_data, indent=4))

tommorow = date.today() + timedelta(days=1)

def get_dates_seven_days_from_date(start_date):
    """
    Returns a list of all dates within a 7-day period starting from the given date.

    Args:
        start_date (date): The starting date.

    Returns:
        list: A list of date objects covering the 7-day period.
    """
    date_list = []
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        date_list.append(current_date)
    return date_list

# Example usage:
seven_day_period = get_dates_seven_days_from_date(tommorow)

print(f"Dates for the 7-day period starting from {tommorow}:")
for d in seven_day_period:
    print(d)