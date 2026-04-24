import logging
from pathlib import Path

from SunCastPy.data.zones_url import SJU_ZONES_GROUPED
from SunCastPy.Forecast.NOAA_Local_Forecast import LocalWeather
from SunCastPy.utils.current_weather import filter_current_weather
from SunCastPy.utils.export_file import create_html
from SunCastPy.utils.html_renderer import render_html, render_index
from SunCastPy.utils.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def get_forecast_all_cities_in_zone(
    zone_name: str, flatten: bool = True
) -> dict[str, LocalWeather]:
    """Given a zone name get the forecast for all of the corresponding cities

    Args:
        zone_name (str): Name of the zone
        flatten (bool): Group the timeframes when the values are similar. Defaults to True.

    Returns:
        dict[str, LocalWeather]: Forecasts for all of the cities in the zone
    """
    forecast_cities = {}
    logger.info(f"Initiating forecast retrieval for all cities in [{zone_name}]")
    for city in SJU_ZONES_GROUPED[zone_name]["cities"]:
        logger.info(f"Getting forecast for {city}")
        current_data = LocalWeather(city=city, flatten=flatten)
        grouped_weather = filter_current_weather(
            data=current_data,
            group_by="date",
            limit=3,
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
        html = render_html(grouped_data=grouped_weather, location=city, template="forecast.html.j2")
        create_html(data=html, output_dir=output_dir, name=city_file)

    index_html = render_index(locations=locations)

    create_html(data=index_html, output_dir=output_dir, name="index.html")
    logger.info("Created all reports for each city.")


def main(zone: str, output: Path) -> None:
    forecast_data = get_forecast_all_cities_in_zone(zone)
    create_html_multi_city(data=forecast_data, output_dir=output)
