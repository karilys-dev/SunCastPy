"""Module that creates a report for a zone"""

import logging
from pathlib import Path

from SunCastPy.data.zones_url import SJU_ZONES_GROUPED
from SunCastPy.models.NOAA.base_local_forecast import LocalForecast
from SunCastPy.utils.current_weather import filter_current_weather
from SunCastPy.utils.export_file import export_html
from SunCastPy.utils.html_renderer import render_html, render_index

logger = logging.getLogger(__name__)


def get_forecast_all_cities_in_zone(
    zone_name: str,
    flatten: bool,
    limit: int,
) -> dict[str, LocalForecast]:
    """Given a zone name get the forecast for all of the corresponding cities

    Args:
        zone_name (str): Name of the zone
        flatten (bool): Group the timeframes when the values are similar
        limit (int): limit of days to show

    Returns:
        dict[str, LocalForecast]: Forecasts for all of the cities in the zone
    """
    forecast_cities = {}
    logger.info(f"Initiating forecast retrieval for all cities in [{zone_name}]")
    for city in SJU_ZONES_GROUPED[zone_name]["cities"]:
        logger.info(f"Getting forecast for {city}")
        current_data = LocalForecast(
            city=city,
            flatten=flatten,
            limit=limit,
        )
        grouped_weather = filter_current_weather(
            data=current_data,
            group_by="date",
        )
        forecast_cities[city] = grouped_weather
    return forecast_cities


def create_html_multi_city(data: dict, output_dir: Path):
    """Create the html file for each city

    Args:
        data (dict): Dictionary with city and forecast values
        output_dir (Path): Where to save the files
    """
    locations: list[dict] = []
    for city, grouped_weather in data.items():
        city_file = f"{city}.html"
        locations.append({"file": city_file, "name": city})
        html = render_html(
            grouped_data=grouped_weather, location=city, template="forecast.html.j2"
        )
        export_html(data=html, output_dir=output_dir, name=city_file)

    index_html = render_index(locations=locations)

    export_html(data=index_html, output_dir=output_dir, name="index.html")
    logger.info("Created all reports for each city.")


def main(zone: str, output: Path, flatten: bool, limit: int) -> None:
    """Create the report for the zone

    Args:
        zone (str): Name of the zone
        output (Path): Where will the html pages be saved
        flatten (bool, optional): Join concurrent time slots.
        limit (int): limit of days to show
    """
    forecast_data = get_forecast_all_cities_in_zone(
        zone_name=zone,
        flatten=flatten,
        limit=limit,
    )
    create_html_multi_city(data=forecast_data, output_dir=output)
