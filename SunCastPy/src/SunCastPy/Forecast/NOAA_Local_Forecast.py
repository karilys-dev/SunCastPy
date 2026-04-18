"""Get the weather forecast by coordinates from the NOAA API"""

from collections import defaultdict

from SunCastPy.data.zones_url import SJU_ZONES
from SunCastPy.Forecast.Base_Forecast import Forecast
from SunCastPy.Forecast.Weekly_Forecast import WeeklyForecast
from SunCastPy.utils.utils import (
    get_api_details,
    get_hourly_forecast_url,
    get_hourly_forecast_zone_url,
    get_request,
)


class LocalWeather:
    """Run an API call to NOAA given the coordinates to get the local weather"""

    def __init__(
        self,
        latitude: float | None = None,
        longitude: float | None = None,
        city: str | None = None,
        flatten: bool = False,
    ) -> None:
        _details: dict[str, dict] = {}
        _periods: str = ""
        self.periods: list[dict] = [{}]
        self.location: str = ""
        if latitude is not None and longitude is not None:
            _details = get_api_details(latitude=latitude, longitude=longitude)
            self.location = get_request(get_hourly_forecast_zone_url(_details))["properties"][
                "name"
            ]
            _periods = get_hourly_forecast_url(_details)
        elif city:
            self.location = SJU_ZONES[city]["forecastZone"]
            _periods = SJU_ZONES[city]["url"]
        else:
            raise ValueError("Missing city or latitude and longitude")
        self.periods = get_request(_periods)["properties"]["periods"]
        self.forecast: list[Forecast] = [Forecast(**p) for p in self.periods]
        if flatten:
            self.forecast = self._summarize_time_slots()

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

    def weekly(self) -> WeeklyForecast:
        """Return a WeeklyForecast view of the data."""
        return WeeklyForecast(self.forecast)

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
