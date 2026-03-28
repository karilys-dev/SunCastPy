# Importing the Pytest library
import json
from pathlib import Path

import pytest
from data.expected_forecast_flat import EXPECTED_FLATTENED_FORECAST
from SunCastPy.logging_config import setup_logging
from SunCastPy.NOAA_Forecast import LocalWeather


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    setup_logging()


TEST_DATA_DIR = Path(__file__).parent.joinpath("data")
DATA_DETAILS = json.loads(TEST_DATA_DIR.joinpath("NOAA_SJU.json").read_text(encoding="utf-8"))
DATA_FORECAST = json.loads(
    TEST_DATA_DIR.joinpath("NOAA_SJU_forecastHourly.json").read_text(encoding="utf-8")
)


@pytest.fixture
def sample_data(mock_get_request):
    data = {"expected": {}, "flattened": {}, "default": {}}
    data["default"]["LocalWeather"] = LocalWeather(0, 0)
    data["default"]["Forecast"] = data["default"]["LocalWeather"].forecast
    data["flattened"]["LocalWeather"] = LocalWeather(0, 0, flatten=True)
    data["flattened"]["Forecast"] = data["flattened"]["LocalWeather"].forecast
    data["expected"]["LocalWeather"] = DATA_DETAILS
    data["expected"]["Forecast"] = DATA_FORECAST
    data["expected"]["ForecastFlat"] = EXPECTED_FLATTENED_FORECAST
    return data


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

        if DATA_DETAILS["properties"]["forecastHourly"] in url:
            return DATA_FORECAST

        raise ValueError(f"Unexpected URL: {url}")

    monkeypatch.setattr("SunCastPy.NOAA_Forecast.get_request", fake_get_request)
