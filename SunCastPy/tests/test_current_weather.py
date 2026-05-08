import pytest
from SunCastPy.utils.current_weather import (
    print_current_weather,
)

from SunCastPy.utils.cli_args import GROUP_BY_OPTIONS


@pytest.mark.parametrize(
    ("group_by"),
    [None] + GROUP_BY_OPTIONS,
)
def test_print_LocalForecast(
    group_by, caplog, test_data, mock_datetime_today, expected_day
):
    data = test_data["default"]["LocalForecast"]
    first_forecast = data.forecast[0]
    # data.forecast = [first_forecast]
    if group_by:
        data = data.group_by(group_by)
    print_current_weather(data)
    assert str(first_forecast.probability_of_precipitation) in caplog.text
    assert first_forecast.short_forecast in caplog.text
    assert expected_day in caplog.text

    if group_by == "date":
        assert first_forecast.day_name in caplog.text
    else:
        assert first_forecast.day_name not in caplog.text
