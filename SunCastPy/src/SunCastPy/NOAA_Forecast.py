"""Get the weather forecast by coordinates from the NOAA API"""

from collections import defaultdict
from datetime import datetime

from SunCastPy.utils import get_request


class ForecastSummary:
    """Extract the forecast and rain probability for each time frame"""

    def __init__(self, data: dict) -> None:
        self.short_forecast = data["shortForecast"]
        self.probability_of_precipitation = data["probabilityOfPrecipitation"]["value"]
        self.long_start_time = data["startTime"]
        self.long_end_time = data["endTime"]

    def __repr__(self) -> str:
        return (
            f"forecast = {self.short_forecast}"
            + f" start = {self._format_hour(self.long_start_time)}"
            + f" end = {self._format_hour(self.long_end_time)}"
            + f" chance of rain = {self.probability_of_precipitation}"
        )

    def _format_hour(self, s) -> str:
        return datetime.fromisoformat(s).strftime("%-I %p").lower()


class LocalWeather:
    """Run an API call to NOAA given the coordinates to get the local weather"""

    def __init__(self, latitude: float, longitude: float) -> None:
        _details = get_request(f"https://api.weather.gov/points/{latitude},{longitude}")
        _forecast = _details.get("properties", {}).get("forecastHourly")
        self.periods: list[dict] = get_request(_forecast)["properties"]["periods"]
        self.short_forecast: list[ForecastSummary] = [ForecastSummary(data=p) for p in self.periods]

    def group_by_day_name(self, data: list[ForecastSummary]) -> dict:
        """Group the forecast by day of the week

        Args:
            data (list[ShortForecast]): Forecast item containing the day of the week and
            the ShortForecast data

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

    def group_weather_periods(self, data: list[ForecastSummary], flatten: bool = False) -> dict:
        """Group the weather periods by forecast name.

        Args:
            data (list[ForecastSummary]): Data containing the forecast information
            flatten (bool, optional): Join concurrent time slots. Defaults to False.

        Returns:
            dict: Data with grouped weather forecast names.
        """
        result: dict = defaultdict(list)
        if flatten:
            data = self.summarize_time_slots(data=data)
        for current in data:
            result[current.short_forecast].append(current)

        return dict(result)

    def summarize_time_slots(self, data: list[ForecastSummary]) -> list[ForecastSummary]:
        """Join concurrent time slots to tell when the forecast will change.
        E.g. Rain from 6 am - 10 am

        Args:
            data (list[ShortForecast]): Data containing the forecast information

        Returns:
            dict: Data with flattened time periods
        """
        # Start with an empty list to avoid having to check the first element in the loop
        result: list[ForecastSummary] = []

        for current in data:
            # Make sure the climate stays the same before updating the end time
            current_forecast = current.short_forecast
            if not result:
                result = [current]
            # See if the previous entry has the same value
            elif result[-1].short_forecast == current_forecast:
                # Verify that the previous end time matches the current start time
                # E.g [4-5, 5-6] -> [4-6]
                if result[-1].probability_of_precipitation == current.probability_of_precipitation:
                    if result[-1].long_end_time == current.long_start_time:
                        result[-1].long_end_time = current.long_end_time
                else:
                    # raise ValueError("Expected the previous forecast and time to match but did not")
                    result.append(current)
            else:
                result.append(current)

        return result
