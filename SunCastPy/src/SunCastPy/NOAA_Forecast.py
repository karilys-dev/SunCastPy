"""Get the weather forecast by coordinates from the NOAA API"""

from collections import defaultdict
from datetime import datetime

from SunCastPy.utils import get_request


class ShortForecast:
    """Extract the forecast and rain probability for each time frame"""

    def __init__(self, data: dict) -> None:
        self.short_forecast = data["shortForecast"]
        self.probability_of_precipitation = data["probabilityOfPrecipitation"]["value"]
        self.long_start_time = data["startTime"]
        self.long_end_time = data["endTime"]

    def __repr__(self) -> str:
        return f"forecast = {self.short_forecast} start = {self._format_hour(self.long_start_time)} end = {self._format_hour(self.long_end_time)} chance of rain = {self.probability_of_precipitation}"

    def _format_hour(self, s) -> str:
        return datetime.fromisoformat(s).strftime("%-I %p").lower()


class LocalWeather:
    """Run an API call to NOAA given the coordinates to get the local weather"""

    def __init__(self, latitude: float, longitude: float) -> None:
        _details = get_request(f"https://api.weather.gov/points/{latitude},{longitude}")
        _forecast = _details.get("properties", {}).get("forecastHourly")
        self.periods: list[dict] = get_request(_forecast)["properties"]["periods"]
        self.short_forecast: list[ShortForecast] = [ShortForecast(data=p) for p in self.periods]

    def group_by_day_name(self, data: list[ShortForecast]) -> dict:
        """Group the forecast by day of the week

        Args:
            data (list[ShortForecast]): Forecast item containing the day of the week and the ShortForecast data

        Returns:
            dict: Data classified by the day of the week
        """
        result = defaultdict(list)

        for current in data:
            # Parse ISO 8601 string (handles timezone too)
            dt_str = current.long_start_time
            dt = datetime.fromisoformat(dt_str)

            weekday = dt.strftime("%A")

            result[weekday].append(current)

        return dict(result)

    def group_weather_periods(self, data: list[ShortForecast]) -> dict:
        """Flatten the time periods to tell when the forecast will change instead of having to view all hours. E.g. Rain from 6 am - 10 am

        Args:
            data (list[ShortForecast]): Data containing the forecast information

        Returns:
            dict: Data classified by forecast and timeframe.
        """
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
