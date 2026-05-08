"""Module providing a class to create WeeklyForecast."""

from collections import defaultdict
from datetime import datetime

from SunCastPy.models.NOAA.forecast import Forecast
from SunCastPy.utils.utils import format_date


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class WeeklyForecast:
    """Class representing a forecast for each day of the week"""

    def __init__(self, forecast_list: list[Forecast]) -> None:
        self.weekly: dict[str, list[Forecast]] = self.group_by_date(forecast_list)
        # Initialize all days (important for autocomplete + safety)
        self.sunday = None
        self.monday = None
        self.tuesday = None
        self.wednesday = None
        self.thursday = None
        self.friday = None
        self.saturday = None
        self.today = None
        for key, value in self.weekly.items():
            day = key.split()[0].lower()

            if hasattr(self, day) and not getattr(self, day):
                setattr(self, day, value)
                if format_date(datetime.today()) == key:
                    setattr(self, "today", value)

    def group_by_date(self, forecast_list: list[Forecast]) -> dict:
        """Group the forecast by day of the week

        Args:
            data (list[ShortForecast]): Forecast item containing the day of the week and
            the ShortForecast data

        Returns:
            dict: Data classified by the day of the week
        """
        result = defaultdict(list)

        for current in forecast_list:
            # Parse ISO 8601 string (handles timezone too)
            weekday = format_date(current.start_time)

            result[weekday].append(current)

        return dict(result)
