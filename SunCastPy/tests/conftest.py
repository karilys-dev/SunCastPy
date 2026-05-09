# pylint: disable=redefined-outer-name,unused-argument

# Importing the Pytest library
import json
from datetime import datetime
from pathlib import Path

import pytest
from data.expected_forecast_flat import EXPECTED_FLATTENED_FORECAST
from data.grouped_url import MOCK_GROUPED_URL

from SunCastPy.models.NOAA.base_local_forecast import LocalForecast
from SunCastPy.utils.logging_config import setup_logging
from SunCastPy.utils.utils import format_date

TEST_DATA_DIR = Path(__file__).parent.joinpath("data")


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    setup_logging()


@pytest.fixture()
def sju_forecast():
    return json.loads(
        TEST_DATA_DIR.joinpath("NOAA_SJU_forecastHourly.json").read_text(
            encoding="utf-8"
        )
    )


@pytest.fixture
def sju_data():
    return json.loads(
        TEST_DATA_DIR.joinpath("NOAA_SJU.json").read_text(encoding="utf-8")
    )


def _get_sample_data(kwargs):
    data = LocalForecast(0, 0, **kwargs)
    return {"LocalForecast": data, "Forecast": data.forecast}


@pytest.fixture
def test_data(mock_get_request, mock_city, sju_data, sju_forecast):
    data = {"expected": {}, "flattened": {}, "default": {}, "city": {}}

    data["default"] = _get_sample_data({"flatten": False})
    data["flattened"] = _get_sample_data({"flatten": True})
    data["city"] = _get_sample_data({"city": "Test"})
    data["limit_3"] = _get_sample_data({"city": "Test", "limit": 3})
    return data


@pytest.fixture
def expected_data(mock_get_request, mock_city, sju_data, sju_forecast):
    data = {}
    data["LocalForecast"] = sju_data
    data["Forecast"] = sju_forecast
    data["ForecastFlat"] = EXPECTED_FLATTENED_FORECAST
    data["group_by_dayname"] = {
        "Sunday 2026-03-22": {"default": 8, "flattened": 3},
        "Monday 2026-03-23": {"default": 24, "flattened": 6},
        "Tuesday 2026-03-24": {"default": 24, "flattened": 4},
        "Wednesday 2026-03-25": {"default": 24, "flattened": 3},
        "Thursday 2026-03-26": {"default": 24, "flattened": 2},
        "Friday 2026-03-27": {"default": 24, "flattened": 3},
        "Saturday 2026-03-28": {"default": 24, "flattened": 3},
        "Sunday 2026-03-29": {"default": 4, "flattened": 1},
    }
    data["group_by_forecast"] = {
        "Chance Rain Showers": {"default": 29, "flattened": 6},
        "Scattered Rain Showers": {"default": 70, "flattened": 9},
        "Isolated Rain Showers": {"default": 3, "flattened": 1},
        "Scattered Showers And Thunderstorms": {"default": 42, "flattened": 7},
        "Chance Showers And Thunderstorms": {"default": 12, "flattened": 2},
    }
    return data


@pytest.fixture
def mock_city(monkeypatch, sju_data):
    fake_city = {
        "Test": {
            "latitude": 0,
            "longitude": 0,
            "url": sju_data["properties"]["forecastHourly"],
            "forecastZone": sju_data["properties"]["forecastZone"],
        }
    }

    monkeypatch.setattr(
        "SunCastPy.models.NOAA.base_local_forecast.SJU_ZONES", fake_city
    )
    monkeypatch.setattr("SunCastPy.data.zones.COORDINATES", fake_city)


@pytest.fixture
def mock_city_url(monkeypatch, sju_data):
    def mock_get_api_details(**kwargs):
        return sju_data

    monkeypatch.setattr(
        "SunCastPy.data.sju_zones.get_api_details", mock_get_api_details
    )


@pytest.fixture
def mock_get_request(monkeypatch, sju_data, sju_forecast):
    """Mock test data using sample from San Juan 2026-03-22

    Raises:
        ValueError: Undefined url. No expected output was defined

    Returns:
        _type_: Mocked test data
    """

    def fake_get_request(url: str):
        if url == "https://api.weather.gov/points/0,0":
            return sju_data
        if sju_data["properties"]["forecastHourly"] in url:
            return sju_forecast
        if sju_data["properties"]["forecastZone"] in url:
            return {"properties": {"name": "San Juan and Vicinity"}}
        if url == "https://ipinfo.io":
            return {"loc": "00.0000,-11.1111"}
        if url in MOCK_GROUPED_URL.keys():
            return {"properties": {"name": MOCK_GROUPED_URL.get(url)}}
        raise ValueError(f"Unexpected URL: {url}")

    monkeypatch.setattr(
        "SunCastPy.models.NOAA.base_local_forecast.get_request", fake_get_request
    )
    monkeypatch.setattr("SunCastPy.utils.utils.get_request", fake_get_request)


@pytest.fixture
def today_str():
    return datetime(2026, 3, 22)


@pytest.fixture
def expected_day(today_str):
    return format_date(today_str, dayname=False)


@pytest.fixture
def mock_datetime_today(monkeypatch, today_str):
    class MockDateTime:
        @classmethod
        def today(cls):
            return today_str

    monkeypatch.setattr("SunCastPy.models.NOAA.weekly_forecast.datetime", MockDateTime)
