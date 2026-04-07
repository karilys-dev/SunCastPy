import logging

from SunCastPy.Forecast.Base_Forecast import Forecast
from SunCastPy.Forecast.NOAA_Local_Forecast import LocalWeather
from SunCastPy.utils.cli_args import parse_args
from SunCastPy.utils.current_weather import filter_current_weather, print_current_weather
from SunCastPy.utils.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def main(args=parse_args()):
    """Get the weather forecast and print to command line

    Args:
        args (argument parser, optional): Argument parser values. Defaults to parse_args().
    """
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
        current_weather = filter_current_weather(
            result=current_weather,
            group_by=args.group_by,
            limit=args.limit,
        )

    print_current_weather(current_weather=current_weather)


if __name__ == "__main__":
    main()
