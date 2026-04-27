# Importing the Pytest library
import json
from datetime import datetime
from pathlib import Path

import pytest
from data.expected_forecast_flat import EXPECTED_FLATTENED_FORECAST
from SunCastPy.models.NOAA.local_forecast import LocalForecast
from SunCastPy.utils.logging_config import setup_logging


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    setup_logging()


TEST_DATA_DIR = Path(__file__).parent.joinpath("data")
DATA_DETAILS = json.loads(TEST_DATA_DIR.joinpath("NOAA_SJU.json").read_text(encoding="utf-8"))
DATA_FORECAST = json.loads(
    TEST_DATA_DIR.joinpath("NOAA_SJU_forecastHourly.json").read_text(encoding="utf-8")
)


@pytest.fixture
def sample_data(mock_get_request, mock_city):
    data = {"expected": {}, "flattened": {}, "default": {}, "city": {}}
    data["default"]["LocalForecast"] = LocalForecast(0, 0)
    data["default"]["Forecast"] = data["default"]["LocalForecast"].forecast
    data["flattened"]["LocalForecast"] = LocalForecast(0, 0, flatten=True)
    data["flattened"]["Forecast"] = data["flattened"]["LocalForecast"].forecast
    data["expected"]["LocalForecast"] = DATA_DETAILS
    data["expected"]["Forecast"] = DATA_FORECAST
    data["expected"]["ForecastFlat"] = EXPECTED_FLATTENED_FORECAST
    data["expected"]["group_by_dayname"] = {
        "Sunday 2026-03-22": {"default": 8, "flattened": 3},
        "Monday 2026-03-23": {"default": 24, "flattened": 6},
        "Tuesday 2026-03-24": {"default": 24, "flattened": 4},
        "Wednesday 2026-03-25": {"default": 24, "flattened": 3},
        "Thursday 2026-03-26": {"default": 24, "flattened": 2},
        "Friday 2026-03-27": {"default": 24, "flattened": 3},
        "Saturday 2026-03-28": {"default": 24, "flattened": 3},
        "Sunday 2026-03-29": {"default": 4, "flattened": 1},
    }
    data["expected"]["group_by_forecast"] = {
        "Chance Rain Showers": {"default": 29, "flattened": 6},
        "Scattered Rain Showers": {"default": 70, "flattened": 9},
        "Isolated Rain Showers": {"default": 3, "flattened": 1},
        "Scattered Showers And Thunderstorms": {"default": 42, "flattened": 7},
        "Chance Showers And Thunderstorms": {"default": 12, "flattened": 2},
    }
    data["city"]["LocalForecast"] = LocalForecast(city="Test")
    data["city"]["Forecast"] = data["city"]["LocalForecast"].forecast

    return data


@pytest.fixture
def mock_city(monkeypatch):
    monkeypatch.setattr(
        "SunCastPy.models.NOAA.local_forecast.SJU_ZONES",
        {
            "Test": {
                "latitude": 0,
                "longitude": 0,
                "url": DATA_DETAILS["properties"]["forecastHourly"],
                "forecastZone": DATA_DETAILS["properties"]["forecastZone"],
            }
        },
    )


@pytest.fixture
def mock_get_request(monkeypatch):
    """Mock test data using sample from San Juan 2026-03-22

    Raises:
        ValueError: Undefined url. No expected output was defined

    Returns:
        _type_: Mocked test data
    """

    def fake_get_request(url: str):
        if url == "https://api.weather.gov/points/0,0":
            return DATA_DETAILS
        elif DATA_DETAILS["properties"]["forecastHourly"] in url:
            return DATA_FORECAST
        elif DATA_DETAILS["properties"]["forecastZone"] in url:
            return {"properties": {"name": "San Juan and Vicinity"}}
        elif url == "https://ipinfo.io":
            return {"loc": "00.0000,-11.1111"}
        raise ValueError(f"Unexpected URL: {url}")

    monkeypatch.setattr("SunCastPy.models.NOAA.local_forecast.get_request", fake_get_request)
    monkeypatch.setattr("SunCastPy.utils.utils.get_request", fake_get_request)


@pytest.fixture
def today_str():
    return datetime(2026, 3, 22)


@pytest.fixture
def mock_datetime_today(monkeypatch, today_str):
    class MockDateTime:
        @classmethod
        def today(cls):
            return today_str

    monkeypatch.setattr("SunCastPy.models.NOAA.weekly_forecast.datetime", MockDateTime)
