from datetime import datetime
from SunCastPy.utils import get_request
from collections import defaultdict


class ShortForecast:
    def __init__(self, property) -> None:
        self.short_forecast = property["shortForecast"]
        self.probability_of_precipitation = property["probabilityOfPrecipitation"][
            "value"
        ]
        self.long_start_time = property["startTime"]
        self.long_end_time = property["endTime"]

    def __repr__(self) -> str:
        return f"forecast = {self.short_forecast} start = {self._format_hour(self.long_start_time)} end = {self._format_hour(self.long_end_time)} chance of rain = {self.probability_of_precipitation}"

    def _format_hour(self, s) -> str:
        return datetime.fromisoformat(s).strftime("%-I %p").lower()


class LocalWeather:
    def __init__(self, latitude: float, longitude: float) -> None:
        _details = get_request(f"https://api.weather.gov/points/{latitude},{longitude}")
        _forecast = _details.get("properties", {}).get("forecastHourly")
        self.periods: list[dict] = get_request(_forecast)["properties"]["periods"]
        self.short_forecast: list[ShortForecast] = [
            ShortForecast(property=p) for p in self.periods
        ]

    def sort_current_forecast(self, data: list[ShortForecast]) -> dict:
        result = defaultdict(list)

        for current in data:
            # Parse ISO 8601 string (handles timezone too)
            dt_str = current.long_start_time
            dt = datetime.fromisoformat(dt_str)

            # Get weekday name (e.g., 'Monday')
            weekday = dt.strftime("%A")

            # Add to dictionary
            result[weekday].append(current)

        # Convert back to normal dict if needed
        return dict(result)

    def classify_weather(self, data: list[ShortForecast]) -> dict:
        result: dict = defaultdict(list)
        for current in data:
            climate = current.short_forecast

            if result.get(climate, []):
                if result.get(climate, [])[-1].long_end_time == current.long_start_time:
                    result.get(climate, [])[-1].long_end_time = current.long_end_time
                else:
                    result[climate].append(current)
            else:
                result[climate].append(current)

        return dict(result)
