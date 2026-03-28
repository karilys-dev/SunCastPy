import logging
from datetime import datetime

import pytest
from SunCastPy.NOAA_Forecast import Forecast, LocalWeather

logger = logging.getLogger(__name__)


class Test_LocalWeather:
    @pytest.mark.skip("Replace with expected values")
    def test_has_attributes(self, sample_data):
        data: LocalWeather = sample_data["LocalWeather"]
        assert hasattr(data, "periods")
        assert hasattr(data, "forecast")
        assert isinstance(data.forecast, list)
        assert isinstance(data.forecast[0], Forecast)

    @pytest.mark.parametrize(
        ("data_type", "length"),
        (
            pytest.param("default", 24, id="default_output"),
            pytest.param("flattened", 6, id="flattened_output"),
        ),
    )
    def test_group_by_dayname(self, sample_data, data_type, length):
        data: LocalWeather = sample_data[data_type]["LocalWeather"]
        grouped = data.group_by_dayname()
        assert list(grouped.keys()) == [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        assert isinstance(grouped["Monday"], list)
        assert isinstance(grouped["Monday"][0], Forecast)
        assert len(grouped["Monday"]) == length

    def test_flattened_data(self, sample_data):
        result: list[Forecast] = sample_data["flattened"]["Forecast"]
        expected_data = sample_data["expected"]["ForecastFlat"]

        for index, expected in enumerate(expected_data):
            for key, _ in expected.dict().items():
                if key in [
                    "short_forecast",
                    "start_time",
                    "end_time",
                    "probability_of_precipitation",
                ]:
                    assert getattr(expected, key) == getattr(result[index], key), (
                        f"Expected {getattr(expected, key)} got {getattr(result[index], key)}"
                    )


class Test_Forecast:
    @pytest.mark.parametrize(
        ("param_name", "dict_key"),
        (
            pytest.param("short_forecast", "shortForecast", id="short_forecast"),
            pytest.param("start_time", "startTime", id="start_time"),
            pytest.param("end_time", "endTime", id="end_time"),
            pytest.param("temperature", "temperature", id="temperature"),
            pytest.param("temperature_unit", "temperatureUnit", id="temperature_unit"),
            pytest.param("wind_speed", "windSpeed", id="wind_speed"),
            pytest.param("wind_direction", "windDirection", id="wind_direction"),
            pytest.param("day_name", "day_name", id="day_name"),
            pytest.param(
                "probability_of_precipitation",
                "probabilityOfPrecipitation",
                id="probability_of_precipitation",
            ),
        ),
    )
    def test_has_attributes(self, sample_data, param_name, dict_key):
        class_data: Forecast = sample_data["default"]["Forecast"][0]
        expected_data: dict = sample_data["expected"]["Forecast"]["properties"]["periods"][0]
        if param_name == "probability_of_precipitation":
            value = int(expected_data[dict_key]["value"])
        elif param_name in ["start_time", "end_time"]:
            value = datetime.fromisoformat(expected_data[dict_key])
        elif param_name == "day_name":
            value = "Sunday"
        else:
            value = expected_data[dict_key]
        assert value == getattr(class_data, param_name)
