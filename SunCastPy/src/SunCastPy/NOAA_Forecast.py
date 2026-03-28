"""Get the weather forecast by coordinates from the NOAA API"""

from collections import defaultdict
from datetime import datetime

from pydantic import BaseModel, Field, model_validator
from SunCastPy.utils import get_request


class Forecast(BaseModel):
    """Extract the forecast and rain probability for each time frame"""

    short_forecast: str = Field(alias="shortForecast")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    temperature: int
    temperature_unit: str = Field(alias="temperatureUnit")
    wind_speed: str = Field(alias="windSpeed")
    wind_direction: str = Field(alias="windDirection")
    probability_of_precipitation: int

    @model_validator(mode="before")
    @classmethod
    def flatten_data(cls, data):
        pop = data.get("probabilityOfPrecipitation", {})
        data["probability_of_precipitation"] = pop.get("value")
        return data

    @property
    def day_name(self) -> str:
        return self.start_time.strftime("%A")


class LocalWeather:
    """Run an API call to NOAA given the coordinates to get the local weather"""

    def __init__(self, latitude: float, longitude: float, flatten: bool = False) -> None:
        _details = get_request(f"https://api.weather.gov/points/{latitude},{longitude}")
        _forecast = _details.get("properties", {}).get("forecastHourly")
        self.periods: list[dict] = get_request(_forecast)["properties"]["periods"]
        self.forecast: list[Forecast] = [Forecast(**p) for p in self.periods]
        if flatten:
            self.forecast = self._summarize_time_slots()

    def group_by_dayname(self) -> dict:
        """Group the forecast by day of the week

        Args:
            data (list[ShortForecast]): Forecast item containing the day of the week and
            the ShortForecast data

        Returns:
            dict: Data classified by the day of the week
        """
        result = defaultdict(list)

        for current in self.forecast:
            # Parse ISO 8601 string (handles timezone too)
            weekday = current.start_time.strftime("%A %Y-%m-%d")

            result[weekday].append(current)

        return dict(result)

    def group_by_forecast(self) -> dict:
        """Group the weather periods by forecast name.

        Args:
            data (list[ForecastSummary]): Data containing the forecast information
            flatten (bool, optional): Join concurrent time slots. Defaults to False.

        Returns:
            dict: Data with grouped weather forecast names.
        """
        result: dict = defaultdict(list)

        for current in self.forecast:
            result[current.short_forecast].append(current)

        return dict(result)

    def _summarize_time_slots(self) -> list[Forecast]:
        """Join concurrent time slots to tell when the forecast will change.
        E.g. Rain from 6 am - 10 am

        Args:
            data (list[ShortForecast]): Data containing the forecast information

        Returns:
            dict: Data with flattened time periods
        """
        # Start with an empty list to avoid having to check the first element in the loop
        result: list[Forecast] = []

        for current in self.forecast:
            # Make sure the climate stays the same before updating the end time
            current_forecast = current.short_forecast
            current_date = current.day_name
            if not result:
                result = [current]
            # See if the previous entry has the same value
            elif result[-1].short_forecast == current_forecast:
                # Verify that the previous end time matches the current start time
                # E.g [4-5, 5-6] -> [4-6]
                if result[-1].day_name != current_date:
                    result.append(current)
                elif (
                    result[-1].probability_of_precipitation == current.probability_of_precipitation
                ):
                    if result[-1].end_time == current.start_time:
                        result[-1].end_time = current.end_time
                else:
                    result.append(current)
            else:
                result.append(current)

        return result
