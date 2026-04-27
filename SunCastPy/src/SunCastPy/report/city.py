"""Module that creates a report for a city"""

import logging
from pathlib import Path

from SunCastPy.Forecast.Base_Forecast import Forecast
from SunCastPy.Forecast.NOAA_Local_Forecast import LocalWeather
from SunCastPy.utils.current_weather import filter_current_weather, print_current_weather
from SunCastPy.utils.export_file import export_html
from SunCastPy.utils.html_renderer import render_html

logger = logging.getLogger(__name__)


def get_city_forecast(kwargs: dict) -> LocalWeather:
    """Get the forecast for the city

    Args:
        kwargs (dict): Values required for LocalWeather class

    Returns:
        LocalWeather: Local Weather for the specified city
    """
    current_weather: LocalWeather | dict[str, list[Forecast]] = LocalWeather(**kwargs)
    logger.info(f"Forecast for {current_weather.location}")
    return current_weather


def report_forecast(
    data: LocalWeather,
    limit: int,
    output: Path | None = None,
    group_by: str | None = "",
):
    """Create a report for the city.
    If output is provided it will create html. Otherwise print to console.

    Args:
        data (LocalWeather): Data containing the weather info
        limit (int): limit of days to show
        output (Path | None, optional): Location to save html files. Defaults to None.
        group_by (str | None, optional): Group the data.
    """
    location: str = data.location
    if output:
        grouped_weather: dict[str, list[Forecast]] = filter_current_weather(
            data=data,
            group_by="date",
            limit=limit,
        )
        logger.info("Creating html report")
        html = render_html(
            grouped_data=grouped_weather,
            location=location,
            template="forecast.html.j2",
        )
        export_html(data=html, output_dir=output, name="index.html")
        logger.info("Report saved to output directory.")

    else:
        new_data: LocalWeather | dict[str, list[Forecast]] = data
        if limit:
            if group_by != "date":
                logger.warning("Limit was selected but the group by needed to be changed to date.")
            group_by = "date"
        if group_by:
            new_data = filter_current_weather(
                data=new_data,
                group_by=group_by,
                limit=limit,
            )
        print_current_weather(current_weather=new_data)


def main(
    kwargs: dict,
    limit: int,
    output: Path | None = None,
    group_by: str | None = "",
):
    """Create the report for the city

    Args:
        kwargs (dict): Values required for LocalWeather class
        limit (int): limit of days to show
        output (Path): Where will the html pages be saved
        flatten (bool, optional): Join concurrent time slots.
    """

    report_forecast(
        data=get_city_forecast(kwargs=kwargs),
        limit=limit,
        output=output,
        group_by=group_by,
    )
