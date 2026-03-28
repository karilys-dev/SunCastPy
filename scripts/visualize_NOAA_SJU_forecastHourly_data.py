import json
from datetime import datetime

with open("tests/data/NOAA_SJU_forecastHourly.json") as fp:
    data = json.load(fp)


prev_day = datetime.fromisoformat(data["properties"]["periods"][0]["startTime"]).strftime("%A")
prev_forecast = data["properties"]["periods"][0]["shortForecast"]

for y in data["properties"]["periods"]:
    current_day = datetime.fromisoformat(y["startTime"]).strftime("%A")
    current_forecast = y["shortForecast"]
    if prev_day != current_day:
        print(f"//{'='.center(100, '=')}")
        prev_day = current_day
    elif prev_forecast != current_forecast:
        print(f"//{'-'.center(100, '-')}")
        prev_forecast = current_forecast

    print(f"Forecast(**{json.dumps(y)}),")
