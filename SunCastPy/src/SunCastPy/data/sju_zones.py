import json
import logging
from pathlib import Path

from SunCastPy.data import zones
from SunCastPy.utils.logging_config import setup_logging
from SunCastPy.utils.utils import (
    get_api_details,
    get_hourly_forecast_url,
    get_hourly_forecast_zone_url,
)


def get_all_zones() -> dict[str, str]:
    data: dict = zones.COORDINATES.copy()
    for city, kwargs in zones.COORDINATES.items():
        logging.info(f"Getting values for {city}")
        details = get_api_details(**kwargs, timeout=50)
        data[city]["url"] = get_hourly_forecast_url(details)
        data[city]["forecastZone"] = get_hourly_forecast_zone_url(details)
    return data


def export_zones_url(data, data_file) -> None:
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    logging.info("File was successfully updated.")


def main():
    setup_logging()
    data_path = Path(__file__).parent.joinpath("zones_url.json")
    data = get_all_zones()
    export_zones_url(data=data, data_file=data_path)


if __name__ == "__main__":
    main()
