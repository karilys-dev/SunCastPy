import pytest

from SunCastPy.models.NOAA.base_local_forecast import LocalForecast
from SunCastPy.models.NOAA.weekly_forecast import Forecast
from SunCastPy.utils.cli_args import GROUP_BY_OPTIONS
from SunCastPy.utils.current_weather import (
    print_current_weather,
)
from SunCastPy.utils.utils import format_date


@pytest.fixture
def expected_day(today_str):
    return format_date(today_str, dayname=False)


def test_group_by_dayname(test_data, mock_datetime_today, today_str):
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


@pytest.mark.parametrize(
    ("group_by"),
    [None] + GROUP_BY_OPTIONS,
)
def test_print_LocalForecast(
    group_by, caplog, test_data, mock_datetime_today, expected_day
):
    if group_by == "forecast":
        pytest.skip("Not yet implemented")
    data = test_data["default"]["LocalForecast"]
    first_forecast = data.forecast[0]
    data.forecast = [first_forecast]
    if group_by:
        data = data.group_by(group_by="date")
    print_current_weather(data)
    assert str(first_forecast.probability_of_precipitation) in caplog.text
    assert first_forecast.short_forecast in caplog.text
    assert expected_day in caplog.text

    if not group_by:
        assert first_forecast.day_name not in caplog.text
    else:
        assert first_forecast.day_name in caplog.text
