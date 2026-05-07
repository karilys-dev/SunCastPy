"""Get the weather forecast by coordinates from the NOAA API"""

from collections import defaultdict
from datetime import datetime, time, timedelta

from SunCastPy.data.zones_url import SJU_ZONES
from SunCastPy.models.NOAA.forecast import Forecast
from SunCastPy.models.NOAA.weekly_forecast import WeeklyForecast
from SunCastPy.utils.utils import (
    get_api_details,
    get_forecast_location_name,
    get_hourly_forecast_url,
    get_hourly_forecast_zone_url,
    get_request,
)


# pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-arguments
class LocalForecast:
    """Run an API call to NOAA given the coordinates to get the local weather"""

    def __init__(
        self,
        latitude: float | None = None,
        longitude: float | None = None,
        city: str | None = None,
        flatten: bool = False,
        limit: int = 8,
    ) -> None:
        _details: dict[str, dict] = {}
        _periods: str = ""
        _max_limit = 9
        self.periods: list[dict] = [{}]
        self.location: str = ""
        if city:
            self.location = city
            _periods = SJU_ZONES[city]["url"]
        elif latitude is not None and longitude is not None:
            _details = get_api_details(latitude=latitude, longitude=longitude)
            self.location = get_forecast_location_name(
                get_hourly_forecast_zone_url(_details)
            )
            _periods = get_hourly_forecast_url(_details)
        else:
            raise ValueError("Missing city or latitude and longitude")
        if limit not in range(1, _max_limit):
            raise ValueError("Invalid number of days to limit the forecast.")

        self.periods = get_request(_periods)["properties"]["periods"]
        self.forecast: list[Forecast] = [Forecast(**p) for p in self.periods]
        self.forecast = self.limit_forecast(limit=limit)
        if flatten:
            self.forecast = self._summarize_time_slots()

    def group_by(self, group_by: str) -> dict[str, list[Forecast]]:
        """Filter the weather by forecast or date

        Args:
            data (LocalForecast): data to group
            group_by (str): [forecast, date]

        Returns:
            dict[str, list[Forecast]] | LocalForecast: Grouped data
        """
        match group_by:
            case "forecast":
                return self.group_by_forecast()
            case "date":
                return self.group_by_date().weekly
            case _:
                raise ValueError("No valid grouping method provided")

    def group_by_forecast(self) -> dict[str, list[Forecast]]:
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

    def group_by_date(self) -> WeeklyForecast:
        """Return a WeeklyForecast view of the data."""
        return WeeklyForecast(self.forecast)

    def limit_forecast(self, limit: int) -> list[Forecast]:
        """Limit the forecast to the next input days.

        Args:
            limit (int): Days to limit the forecast

        Returns:
            list[Forecast]: Forecast list with limited days
        """
        # Count starts at 0
        limit -= 1
        start_time = self.forecast[0].start_time
        tz = start_time.tzinfo

        # Get future date in SAME timezone
        future_date = (start_time + timedelta(days=limit)).date()

        # Build end-of-day WITH timezone
        deadline = datetime.combine(future_date, time.max, tzinfo=tz)

        tmp = []
        for item in self.forecast:
            target_date = item.start_time
            if start_time <= target_date < deadline:
                tmp.append(item)

        return tmp

    def _summarize_time_slots(self) -> list[Forecast]:
        """Join concurrent time slots to tell when the forecast will change.
        E.g. Rain from 6 am - 10 am

        Args:
            data (list[ShortForecast]): Data containing the forecast information

        Returns:
            dict: Data with flattened time periods
        """
        # Start with an empty list to avoid having to check the first element
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
                    result[-1].probability_of_precipitation
                    == current.probability_of_precipitation
                ):
                    if result[-1].end_time == current.start_time:
                        result[-1].end_time = current.end_time
                else:
                    result.append(current)
            else:
                result.append(current)

        return result
