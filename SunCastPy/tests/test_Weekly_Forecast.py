# from SunCastPy.Forecast.Base_Forecast import Forecast
from datetime import datetime

import pytest

from SunCastPy.models.NOAA.base_local_forecast import LocalForecast
from SunCastPy.models.NOAA.forecast import Forecast
from SunCastPy.models.NOAA.weekly_forecast import WeeklyForecast
from SunCastPy.utils.utils import format_date


class Test_weekly_forecast:
    @pytest.mark.parametrize(
        ("data_type"),
        (
            pytest.param("default", id="default_output"),
            pytest.param("flattened", id="flattened_output"),
        ),
    )
    def test_weekly_forecast_object(
        self, test_data, data_type, mock_datetime_today, today_str, expected_data
    ):
        data: LocalForecast = test_data[data_type]["LocalForecast"]
        weekly_object: WeeklyForecast = data.group_by_date()
        grouped: dict = weekly_object.weekly
        expected = expected_data["group_by_dayname"]
        duplicate_dayname = "Sunday 2026-03-29"

        # Confirm that the object is of the correct type
        assert isinstance(weekly_object, WeeklyForecast)

        # Confirm that they keys exist with format A Y-m-d
        assert list(grouped.keys()) == list(expected.keys())

        # Confirm each day of the week is in the dictionary and has the correct type
        for day in grouped.keys():
            assert isinstance(grouped[day], list)
            assert isinstance(grouped[day][0], Forecast)
            assert len(grouped[day]) == expected[day][data_type]

            # The test data has 2 values from Sunday
            # ensure the second doesn't overwrite current
            if day != duplicate_dayname:
                dayname = datetime.strptime(day, "%A %Y-%m-%d").strftime("%A").lower()
                assert getattr(weekly_object, dayname) == grouped[day]
                if day == format_date(today_str):
                    assert weekly_object.today == grouped[day]
