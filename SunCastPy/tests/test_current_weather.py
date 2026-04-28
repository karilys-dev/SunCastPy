import pytest

from SunCastPy.models.NOAA.local_forecast import LocalForecast
from SunCastPy.models.NOAA.weekly_forecast import Forecast
from SunCastPy.utils.current_weather import filter_current_weather
from SunCastPy.utils.utils import format_date


def test_raises_error():
    with pytest.raises(ValueError, match="No valid grouping method provided"):
        filter_current_weather(data={}, group_by="error", limit=1)


def test_group_by_dayname(sample_data, mock_datetime_today, today_str):
    limit: int = 3
    expected_day = format_date(today_str)
    data: LocalForecast = sample_data["default"]["LocalForecast"]
    tmp = filter_current_weather(data=data, group_by="date", limit=3)
    assert len(tmp) == limit
    assert expected_day in tmp
    assert isinstance(tmp[expected_day], list)
    assert isinstance(tmp[expected_day][0], Forecast)
