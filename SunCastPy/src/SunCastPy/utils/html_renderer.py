from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from SunCastPy.utils.utils import format_hour


def render_html(grouped_data: dict) -> str:
    template_dir = Path(__file__).parent.parent / "templates"

    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)

    template = env.get_template("index.html.j2")

    return template.render(grouped=grouped_data, format_hour=format_hour)
