"""Module that creates html reports using jinja2"""

from importlib.resources import files
from pathlib import Path

from fastapi.templating import Jinja2Templates

from SunCastPy.models.NOAA.forecast import Forecast
from SunCastPy.utils.utils import format_hour

BASE_DIR = Path(files("SunCastPy").joinpath("web"))

templates = Jinja2Templates(directory=BASE_DIR / "templates")
env = templates.env


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
    grouped_data: dict[str, list[Forecast]], location: str, template: str
) -> str:
    """Create html page using the jinja2 template and data

    Args:
        grouped_data (dict[str, list[Forecast]]): Data grouped by days of the week
        location (str): Location for which the NOAA report reports the forecast

    Returns:
        str: html data for file creation
    """

    template = env.get_template(template)

    return template.render(
        grouped=grouped_data, format_hour=format_hour, location=location
    )
