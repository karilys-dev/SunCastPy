"""Module that provides functions for current weather"""

import logging

from SunCastPy.models.NOAA.base_local_forecast import LocalForecast
from SunCastPy.models.NOAA.forecast import Forecast

logger = logging.getLogger(__name__)


def print_current_weather(
    current_weather: LocalForecast | dict[str, list[Forecast]],
) -> None:
    """Use the logger to show the weather data

    Args:
        current_weather (LocalForecast | dict[str, list[Forecast]]): Data to print
    """
    if isinstance(current_weather, LocalForecast):
        for forecast in current_weather.forecast:
            logger.info(forecast)

    elif isinstance(current_weather, dict):
        for key, val in current_weather.items():
            logger.info(key)
            for item in val:
                logger.info(item)
