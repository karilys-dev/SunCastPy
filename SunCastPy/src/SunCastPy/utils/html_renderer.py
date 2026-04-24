from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from SunCastPy.Forecast.Base_Forecast import Forecast
from SunCastPy.utils.utils import format_hour

template_dir = Path(__file__).parent.parent / "templates"

env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)


def render_index(locations: list[dict]) -> str:

    template = env.get_template("index.html.j2")
    return template.render(locations=locations)


def render_html(grouped_data: dict[str, list[Forecast]], location: str, template: str) -> str:
    """Create html page using the jinja2 template and data

    Args:
        grouped_data (dict[str, list[Forecast]]): Data grouped by days of the week
        location (str): Location for which the NOAA report reports the forecast

    Returns:
        str: html data for file creation
    """

    template = env.get_template(template)

    return template.render(grouped=grouped_data, format_hour=format_hour, location=location)
