# mypy: disable-error-code="return, no-untyped-def"
"""Module used for forecast API"""

from collections import namedtuple

from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette import status

from SunCastPy.data.zones_url import SJU_ZONES
from SunCastPy.report.city import get_city_forecast as city_forecast
from SunCastPy.report.zone import get_forecast_all_cities_in_zone as zone_report
from SunCastPy.utils.html_renderer import BASE_DIR
from SunCastPy.utils.utils import format_hour

templates = Jinja2Templates(directory=BASE_DIR / "templates")
app = FastAPI(title="SunCast API", version="1.0.0")
env = templates.env
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


@app.get("/api/city/{city}", status_code=status.HTTP_200_OK)
def forecast_city(
    city: str = Path(min_length=3, max_length=12),
    flatten: bool = Query(default=True),
    limit: int = Query(ge=1, le=7, default=1),
):
    """
    Returns the forecast for the requested city.
    """

    try:
        return (
            city_forecast(
                {
                    "city": city,
                    "flatten": flatten,
                    "limit": limit,
                }
            )
            .group_by_date()
            .weekly
        )

    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/zone/{zone_name}", status_code=status.HTTP_200_OK)
def forecast_zone(
    zone_name: str = Path(min_length=3, max_length=50),
    flatten: bool = Query(default=True),
    limit: int = Query(ge=1, le=7, default=1),
):
    """
    Returns the forecast for the requested city.
    """

    try:
        return zone_report(zone_name, flatten, limit)

    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/forecast/{city}", response_class=HTMLResponse, name="forecast")
def report_city(
    request: Request,
    city: str = Path(min_length=3, max_length=12),
    summarize: bool = Query(default=True),
    limit: int = Query(ge=1, le=7, default=1),
):
    """
    Returns the html report for the requested city.
    """

    try:
        data = city_forecast(
            kwargs={
                "city": city,
                "flatten": summarize,
                "limit": limit,
            }
        )
        template = env.get_template("forecast.html.j2")
        html_content = template.render(
            request=request,
            summarize=summarize,
            limit=limit,
            grouped=data.group_by("date"),
            format_hour=format_hour,
            location=data.location,
            show_api_controls=True,
        )

        return HTMLResponse(content=html_content)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    """
    Returns the html index for all cities.
    """
    try:
        Location = namedtuple("Location", "file name")
        location = [
            Location(file=f"/forecast/{zone}", name=zone) for zone in SJU_ZONES.keys()
        ]
        template = env.get_template("index.html.j2")
        html_content = template.render(
            request=request,
            locations=location,
        )
        return HTMLResponse(content=html_content)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
