import logging
from datetime import datetime

import pytest
from SunCastPy.Forecast.Base_Forecast import Forecast
from SunCastPy.Forecast.NOAA_Local_Forecast import LocalWeather
from SunCastPy.Forecast.Weekly_Forecast import WeeklyForecast

logger = logging.getLogger(__name__)


class Test_LocalWeather:
    @pytest.mark.parametrize(
        ("attribute"),
        (
            pytest.param("periods"),
            pytest.param("forecast"),
        ),
    )
    def test_has_attributes(self, sample_data, attribute):
        data: LocalWeather = sample_data["default"]["LocalWeather"]
        match attribute:
            case "forecast":
                assert isinstance(data.forecast, list)
                assert isinstance(data.forecast[0], Forecast)
            case "periods":
                assert isinstance(getattr(data, attribute), list)
                assert isinstance(getattr(data, attribute)[0], dict)

    @pytest.mark.parametrize(
        ("data_type"),
        (
            pytest.param("default", id="default_output"),
            pytest.param("flattened", id="flattened_output"),
        ),
    )
    def test_group_by_dayname(self, sample_data, data_type):
        data: LocalWeather = sample_data[data_type]["LocalWeather"]
        assert isinstance(data.weekly(), WeeklyForecast)

    def test_flattened_data(self, sample_data):
        result: list[Forecast] = sample_data["flattened"]["Forecast"]
        expected_data = sample_data["expected"]["ForecastFlat"]

        for index, expected in enumerate(expected_data):
            for key, _ in expected.model_dump().items():
                if key in [
                    "short_forecast",
                    "start_time",
                    "end_time",
                    "probability_of_precipitation",
                ]:
                    assert getattr(expected, key) == getattr(result[index], key), (
                        f"Expected {getattr(expected, key)} got {getattr(result[index], key)}"
                    )

    @pytest.mark.parametrize(
        ("data_type"),
        (
            pytest.param("default", id="default_output"),
            pytest.param("flattened", id="flattened_output"),
        ),
    )
    def test_group_by_forecast(self, sample_data, data_type):
        data: LocalWeather = sample_data[data_type]["LocalWeather"]
        grouped = data.group_by_forecast()
        expected = sample_data["expected"]["group_by_forecast"]
        assert list(grouped.keys()) == list(expected.keys())
        for forecast in grouped.keys():
            assert isinstance(grouped[forecast], list)
            assert isinstance(grouped[forecast][0], Forecast)
            assert len(grouped[forecast]) == expected[forecast][data_type]


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
