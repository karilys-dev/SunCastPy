"""Module providing a class to create WeeklyForecast."""

from collections import defaultdict
from datetime import datetime, timedelta

from SunCastPy.models.NOAA.base import Forecast
from SunCastPy.utils.utils import format_date


class WeeklyForecast:
    """Class representing a forecast for each day of the week"""

    def __init__(self, forecast_list: list[Forecast]) -> None:
        self.weekly: dict = self.group_by_date(forecast_list=forecast_list)
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

    def get_next_days(self, days: int) -> dict[str, list[Forecast]]:
        """Limit the forecast to the next input days

        Args:
            days (int): Days to limit the forecast

        Returns:
            dict[str, Forecast]: Dictionary of forecast list with limited days
        """
        current_day: datetime = datetime.today()
        result: dict[str, list[Forecast]] = {}
        if days > len(self.weekly.keys()):
            raise ValueError("Number of days is more than data contents")
        for i in range(days):
            day = current_day + timedelta(days=i)
            key = format_date(day)
            result[key] = self.weekly[key]
        return result

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
