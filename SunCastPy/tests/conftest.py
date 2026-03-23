# Importing the Pytest library
import json
from pathlib import Path

import pytest
from SunCastPy.NOAA_Forecast import LocalWeather

TEST_DATA_DIR = Path(__file__).parent.joinpath("data")


@pytest.fixture
def sample_data(mock_get_request):
    data = {}
    data["LocalWeather"] = LocalWeather(0, 0)
    data["Forecast"] = data["LocalWeather"].forecast
    return data


@pytest.fixture
def mock_get_request(monkeypatch):
    """Mock test data using sample from San Juan 2026-03-22

    Raises:
        ValueError: Undefined url. No expected output was defined

    Returns:
        _type_: Mocked test data
    """

    details = json.loads(TEST_DATA_DIR.joinpath("NOAA_SJU.json").read_text(encoding="utf-8"))
    forecast = json.loads(
        TEST_DATA_DIR.joinpath("NOAA_SJU_forecastHourly.json").read_text(encoding="utf-8")
    )

    def fake_get_request(url: str):
        if url == "https://api.weather.gov/points/0,0":
            return details

        if details["properties"]["forecastHourly"] in url:
            return forecast

        raise ValueError(f"Unexpected URL: {url}")

    monkeypatch.setattr("SunCastPy.NOAA_Forecast.get_request", fake_get_request)
