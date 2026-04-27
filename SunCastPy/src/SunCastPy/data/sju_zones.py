"""Module that creates the json files used for getting NOAA cities and zones of Puerto Rico"""

import logging
from pathlib import Path

from SunCastPy.data import zones
from SunCastPy.utils.export_file import export_json
from SunCastPy.utils.logging_config import setup_logging
from SunCastPy.utils.utils import (
    get_api_details,
    get_forecast_location_name,
    get_hourly_forecast_url,
    get_hourly_forecast_zone_url,
)


def get_all_zones() -> dict[str, str]:
    """Iterate over the list of cities and get the urls and zones

    Returns:
        dict[str, str]: Data used for creating the json file of cities and zones
    """
    data: dict = zones.COORDINATES.copy()
    for city, kwargs in zones.COORDINATES.items():
        logging.info(f"Getting values for {city}")
        details = get_api_details(**kwargs, timeout=50)
        data[city]["url"] = get_hourly_forecast_url(details)
        data[city]["forecastZone"] = get_hourly_forecast_zone_url(details)
    return data


def group_zones(data: dict) -> dict:
    """Group each city into the same zone group

    Args:
        data (dict): output of get_all_zones

    Returns:
        dict: Cities grouped by zones
    """
    distinct: dict = {}
    for city, val in data.items():
        zone = val["forecastZone"].split("/")[-1]
        if zone not in distinct.keys():
            distinct[zone] = {}
            distinct[zone]["cities"] = [city]
            distinct[zone]["url"] = val["forecastZone"]
            distinct[zone]["location"] = get_forecast_location_name(val["forecastZone"])
        else:
            distinct[zone]["cities"].append(city)

    return {v["location"]: v for v in sorted(distinct.values(), key=lambda x: x["location"])}


def main():
    """Create the json files used for the zones in Puerto Rico"""
    setup_logging()
    data_path = Path(__file__).parent
    data = get_all_zones()
    export_json(data=data, data_file=data_path.joinpath("zones_url.json"))
    grouped: dict = group_zones(data=data)
    export_json(data=grouped, data_file=data_path.joinpath("zones_url_grouped.json"))


if __name__ == "__main__":
    main()
