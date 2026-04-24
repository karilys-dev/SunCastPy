import logging

from SunCastPy.Forecast.Base_Forecast import Forecast
from SunCastPy.Forecast.NOAA_Local_Forecast import LocalWeather

logger = logging.getLogger(__name__)


def filter_current_weather(
    data: LocalWeather, group_by: str, limit: int
) -> dict[str, list[Forecast]] | LocalWeather:
    """Filter the weather by forecast or date

    Args:
        data (LocalWeather): data to group
        group_by (str): [forecast, date]
        limit (int): limit of days to show

    Returns:
        dict[str, list[Forecast]] | LocalWeather: Grouped data
    """
    match group_by:
        case "forecast":
            return data.group_by_forecast()
        case "date":
            return data.weekly().get_next_days(days=limit)
        case _:
            logger.warning("Did not group the data")
            return data


def print_current_weather(current_weather: LocalWeather | dict[str, list[Forecast]]) -> None:
    """Use the logger to show the weather data

    Args:
        current_weather (LocalWeather | dict[str, list[Forecast]]): Data to print
    """
    if isinstance(current_weather, LocalWeather):
        for forecast in current_weather.forecast:
            logger.info(forecast)

    elif isinstance(current_weather, dict):
        for key, val in current_weather.items():
            logging.info(key)
            for item in val:
                logging.info(item)
