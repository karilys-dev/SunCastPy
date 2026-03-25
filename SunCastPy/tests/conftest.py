# Importing the Pytest library
import json
from pathlib import Path

import pytest
from SunCastPy.NOAA_Forecast import LocalWeather

TEST_DATA_DIR = Path(__file__).parent.joinpath("data")
DATA_DETAILS = json.loads(TEST_DATA_DIR.joinpath("NOAA_SJU.json").read_text(encoding="utf-8"))
DATA_FORECAST = json.loads(
    TEST_DATA_DIR.joinpath("NOAA_SJU_forecastHourly.json").read_text(encoding="utf-8")
)


@pytest.fixture
def sample_data(mock_get_request):
    data = {}
    data["LocalWeather"] = LocalWeather(0, 0)
    data["Forecast"] = data["LocalWeather"].forecast
    data["json_forecast"] = DATA_FORECAST
    data["json_local_weather_details"] = DATA_DETAILS
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
