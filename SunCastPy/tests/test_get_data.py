from datetime import datetime

import pytest
from SunCastPy.NOAA_Forecast import Forecast, LocalWeather


class Test_LocalWeather:
    def test_has_attributes(self, sample_data):
        data: LocalWeather = sample_data["LocalWeather"]
        assert hasattr(data, "periods")
        assert hasattr(data, "forecast")
        assert isinstance(data.forecast, list)
        assert isinstance(data.forecast[0], Forecast)

    @pytest.mark.parametrize(
        ("flatten", "length"),
        (pytest.param(False, 24, id="full_data"), pytest.param(True, 6, id="flattened")),
    )
    def test_group_by_dayname(self, sample_data, flatten, length):
        data: LocalWeather = sample_data["LocalWeather"]
        grouped = data.group_by_dayname(flatten=flatten)
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
        class_data: Forecast = sample_data["Forecast"][0]
        expected_data: dict = sample_data["json_forecast"]["properties"]["periods"][0]
        if param_name == "probability_of_precipitation":
            value = int(expected_data[dict_key]["value"])
        elif param_name in ["start_time", "end_time"]:
            value = datetime.fromisoformat(expected_data[dict_key])
        elif param_name == "day_name":
            value = "Sunday"
        else:
            value = expected_data[dict_key]
        assert value == getattr(class_data, param_name)
