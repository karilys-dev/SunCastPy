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
    def test_group_by_dayname(self, monkeypatch, sample_data, data_type):

        # Define the fake date
        today_mock = datetime(2026, 3, 22)

        class MockDate(datetime):
            @classmethod
            def today(cls):
                return today_mock

        # Replace the date class in the module where it's used
        monkeypatch.setattr("SunCastPy.Forecast.Weekly_Forecast.datetime", MockDate)

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
                if day == format_date(today_mock):
                    assert weekly_object.today == grouped[day]
