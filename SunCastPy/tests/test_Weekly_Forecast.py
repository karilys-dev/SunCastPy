# from SunCastPy.Forecast.Base_Forecast import Forecast
from datetime import datetime

import pytest
from SunCastPy.Forecast.Base_Forecast import Forecast
from SunCastPy.Forecast.NOAA_Local_Forecast import LocalWeather
from SunCastPy.Forecast.Weekly_Forecast import WeeklyForecast
from SunCastPy.utils.utils import format_date


class Test_Weekly_Forecast:
    @pytest.mark.parametrize(
        ("data_type"),
        (
            pytest.param("default", id="default_output"),
            pytest.param("flattened", id="flattened_output"),
        ),
    )
    def test_group_by_dayname(self, sample_data, data_type, mock_datetime_today, today_str):

        data: LocalWeather = sample_data[data_type]["LocalWeather"]
        weekly_object: WeeklyForecast = data.weekly()
        grouped: dict = weekly_object.weekly
        expected = sample_data["expected"]["group_by_dayname"]
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

            # The test data has 2 values from Sunday ensure the second doesn't overwrite current
            if day != duplicate_dayname:
                dayname = datetime.strptime(day, "%A %Y-%m-%d").strftime("%A").lower()
                assert getattr(weekly_object, dayname) == grouped[day]
                if day == format_date(today_str):
                    assert weekly_object.today == grouped[day]

    def test_get_next_days_limit(self, sample_data, mock_datetime_today, today_str):
        data: LocalWeather = sample_data["default"]["LocalWeather"]
        with pytest.raises(ValueError, match="Number of days is more than data contents"):
            data.weekly().get_next_days(days=10)

    def test_get_next_days(self, sample_data, mock_datetime_today, today_str):
        data: LocalWeather = sample_data["default"]["LocalWeather"]
        assert len(data.weekly().weekly) == 7 + 1
        limit = 3
        shortened_value = data.weekly().get_next_days(limit)
        assert len(shortened_value) == limit
        # Confirm ['Sunday 2026-03-22', 'Monday 2026-03-23', 'Tuesday 2026-03-24']
        assert (
            list(shortened_value.keys())[:limit]
            == list(sample_data["expected"]["group_by_dayname"].keys())[:limit]
        )
