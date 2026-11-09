"""Module that creates html reports using jinja2"""

from importlib.resources import files
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from SunCastPy.models.NOAA.forecast import Forecast
from SunCastPy.utils.utils import format_hour

BASE_DIR = Path(files("SunCastPy").joinpath("web"))

env = Environment(loader=FileSystemLoader(BASE_DIR / "templates"), autoescape=True)
templates = Environment(
    loader=FileSystemLoader([BASE_DIR / "templates", BASE_DIR / "static"])
)


def render_index(locations: list[dict]) -> str:
    """Create the index.html page when using zones report

    Args:
        locations (list[dict]): Names of the cities where child pages are created.

    Returns:
        str: data for the html file
    """
    template = env.get_template("index.html.j2")
    return template.render(locations=locations)


def render_html(
    grouped_data: dict[str, list[Forecast]],
    location: str,
    template: str,
    show_api_controls=False,
) -> str:
    """Create html page using the jinja2 template and data

    Args:
        grouped_data (dict[str, list[Forecast]]): Data grouped by days of the week
        location (str): Location for which the NOAA report reports the forecast

    Returns:
        str: html data for file creation
    """

    template = templates.get_template(template)

    return template.render(
        grouped=grouped_data,
        format_hour=format_hour,
        location=location,
        show_api_controls=show_api_controls,
    )
