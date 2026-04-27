"""Module that provides functions for current weather"""

import logging

from SunCastPy.models.NOAA.base import Forecast
from SunCastPy.models.NOAA.local_forecast import LocalForecast
from SunCastPy.utils.cli_args import GROUP_BY_OPTIONS

logger = logging.getLogger(__name__)


def filter_current_weather(
    data: LocalForecast, group_by: str, limit: int
) -> dict[str, list[Forecast]]:
    """Filter the weather by forecast or date

    Args:
        data (LocalForecast): data to group
        group_by (str): [forecast, date]
        limit (int): limit of days to show

    Returns:
        dict[str, list[Forecast]] | LocalForecast: Grouped data
    """
    if group_by not in GROUP_BY_OPTIONS:
        logger.error("Did not group the data")
        raise ValueError("No valid grouping method provided")
    match group_by:
        case "forecast":
            return data.group_by_forecast()
        case "date":
            return data.weekly().get_next_days(days=limit)


def print_current_weather(current_weather: LocalForecast | dict[str, list[Forecast]]) -> None:
    """Use the logger to show the weather data

    Args:
        current_weather (LocalForecast | dict[str, list[Forecast]]): Data to print
    """
    if isinstance(current_weather, LocalForecast):
        for forecast in current_weather.forecast:
            logger.info(forecast)

    elif isinstance(current_weather, dict):
        for key, val in current_weather.items():
            logging.info(key)
            for item in val:
                logging.info(item)
