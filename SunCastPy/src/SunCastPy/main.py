import logging

from SunCastPy.NOAA_Forecast import Forecast, LocalWeather
from SunCastPy.utils.cli_args import parse_args
from SunCastPy.utils.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def filter_current_weather(
    result: LocalWeather, group_by: str
) -> dict[str, list[Forecast]] | LocalWeather:
    match group_by:
        case "forecast":
            return result.group_by_forecast()
        case "date":
            return result.group_by_dayname()
        case _:
            logger.warning("Did not group the data")
            return result


def print_current_weather(current_weather: LocalWeather | dict[str, list[Forecast]]) -> None:
    if isinstance(current_weather, LocalWeather):
        for forecast in current_weather.forecast:
            logger.info(forecast)

    elif isinstance(current_weather, dict):
        for key, val in current_weather.items():
            logging.info(key)
            for item in val:
                logging.info(item)


def main(args=parse_args()):
    kwargs = {
        "latitude": args.latitude,
        "longitude": args.longitude,
        "flatten": args.flatten,
    }
    logger.debug(f"Latitude: {args.latitude}")
    logger.debug(f"Longitude: {args.longitude}")
    logger.debug(f"Flatten: {args.flatten}")
    logger.debug(f"Group By: {args.group_by}")

    current_weather: LocalWeather | dict[str, list[Forecast]] = LocalWeather(**kwargs)
    logger.info(f"Forecast for {current_weather.location}")

    if args.group_by:
        current_weather = filter_current_weather(result=current_weather, group_by=args.group_by)

    print_current_weather(current_weather=current_weather)


if __name__ == "__main__":
    main()
