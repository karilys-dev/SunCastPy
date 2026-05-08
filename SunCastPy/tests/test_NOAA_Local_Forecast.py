import itertools
import logging
from datetime import datetime

import pytest

from SunCastPy.models.NOAA.base_local_forecast import LocalForecast
from SunCastPy.models.NOAA.forecast import Forecast
from SunCastPy.utils.cli_args import GROUP_BY_OPTIONS
from SunCastPy.utils.utils import format_date

logger = logging.getLogger(__name__)


class Test_LocalForecast:
    sources = ["default", "city"]
    attributes = ["periods", "forecast"]

    @pytest.mark.parametrize(
        ("source", "attribute"),
        itertools.product(sources, attributes),
    )
    def test_has_attributes(self, test_data, source, attribute):
        data: LocalForecast = test_data[source]["LocalForecast"]
        match attribute:
            case "forecast":
                assert isinstance(data.forecast, list)
                assert isinstance(data.forecast[0], Forecast)
            case "periods":
                assert isinstance(getattr(data, attribute), list)
                assert isinstance(getattr(data, attribute)[0], dict)

    def test_flattened_data(self, test_data, expected_data):
        result: list[Forecast] = test_data["flattened"]["Forecast"]
        expected_data = expected_data["ForecastFlat"]

        for index, expected in enumerate(expected_data):
            for key, _ in expected.model_dump().items():
                if key in [
                    "short_forecast",
                    "start_time",
                    "end_time",
                    "probability_of_precipitation",
                ]:
                    truth = getattr(expected, key)
                    got = getattr(result[index], key)
                    assert truth == got, f"Expected {truth} got {got}"

    @pytest.mark.parametrize(
        ("data_type"),
        (
            pytest.param("default", id="default_output"),
            pytest.param("flattened", id="flattened_output"),
        ),
    )
    def test_group_by_forecast(self, test_data, data_type, expected_data):
        data: LocalForecast = test_data[data_type]["LocalForecast"]
        grouped = data.group_by_forecast()
        expected = expected_data["group_by_forecast"]
        assert list(grouped.keys()) == list(expected.keys())
        for forecast in grouped.keys():
            assert isinstance(grouped[forecast], list)
            assert isinstance(grouped[forecast][0], Forecast)
            assert len(grouped[forecast]) == expected[forecast][data_type]

    def test_group_by_dayname(
        self, test_data, mock_datetime_today, today_str, expected_data
    ):
        name_key = format_date(today_str)
        limit: int = 3
        data: LocalForecast = test_data["limit_3"]["LocalForecast"]
        default_data = test_data["default"]["LocalForecast"]
        grouped_data = data.group_by(group_by="date")
        assert len(grouped_data) == limit
        assert name_key in grouped_data
        assert isinstance(grouped_data[name_key], list)
        assert isinstance(grouped_data[name_key][0], Forecast)
        assert data.forecast == default_data.limit_forecast(limit=limit)
        # Confirm ['Sunday 2026-03-22', 'Monday 2026-03-23', 'Tuesday 2026-03-24']
        assert (
            list(grouped_data.keys())[:limit]
            == list(expected_data["group_by_dayname"].keys())[:limit]
        )

    @pytest.mark.parametrize("arg", GROUP_BY_OPTIONS)
    def test_all_cli_args_defined(self, arg, test_data):
        assert isinstance(test_data["default"]["LocalForecast"].group_by(arg), dict)

    def test_invalid_group_by(self, test_data):
        with pytest.raises(ValueError, match="No valid grouping method provided"):
            test_data["default"]["LocalForecast"].group_by("invalid")

    def test_missing_city_or_coordinate(self):
        with pytest.raises(ValueError, match="Missing city or latitude and longitude"):
            LocalForecast()

    def test_get_next_days_limit(self, test_data, mock_datetime_today, today_str):
        data: LocalForecast = test_data["default"]["LocalForecast"]
        err_msg = "Invalid number of days to limit the forecast."
        with pytest.raises(ValueError, match=err_msg):
            data.limit_forecast(10)


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
    def test_has_attributes(self, test_data, param_name, dict_key, expected_data):
        class_data: Forecast = test_data["default"]["Forecast"][0]
        expected_data: dict = expected_data["Forecast"]["properties"]["periods"][0]
        if param_name == "probability_of_precipitation":
            value = int(expected_data[dict_key]["value"])
        elif param_name in ["start_time", "end_time"]:
            value = datetime.fromisoformat(expected_data[dict_key])
        elif param_name == "day_name":
            value = "Sunday"
        else:
            value = expected_data[dict_key]
        assert value == getattr(class_data, param_name)
