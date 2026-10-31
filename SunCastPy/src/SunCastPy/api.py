# mypy: disable-error-code="return, no-untyped-def"
"""Module used for forecast API"""

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import HTMLResponse
from starlette import status

from SunCastPy.report.city import get_city_forecast as city_forecast
from SunCastPy.report.city import main as city_report
from SunCastPy.report.zone import get_forecast_all_cities_in_zone as zone_report

app = FastAPI(title="SunCast API", version="1.0.0")


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


@app.get("/forecast/{city}", response_class=HTMLResponse)
def report_city(
    city: str = Path(min_length=3, max_length=12),
    flatten: bool = Query(default=True),
    limit: int = Query(ge=1, le=7, default=1),
    group_by: str | None = Query(min_length=3, max_length=12, default=None),
):
    """
    Returns the html report for the requested city.
    """

    try:
        return HTMLResponse(
            content=city_report(
                {
                    "city": city,
                    "flatten": flatten,
                    "limit": limit,
                },
                group_by=group_by,
                html_report=True,
            )
        )

    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
