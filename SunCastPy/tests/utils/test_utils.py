# pylint: disable=unused-argument
import logging
from datetime import datetime

import pytest

# from SunCastPy.Forecast.NOAA_Local_Forecast import Forecast, LocalForecast
from SunCastPy.utils import utils

logger = logging.getLogger(__name__)


class Test_Utils:
    date_string = "2024-12-25 15:30:00"
    # %Y = 4-digit year, %m = month, %d = day, %H:%M:%S = time
    date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    @pytest.mark.parametrize(
        ("attribute"),
        (
            pytest.param(date_string, id="string"),
            pytest.param(date_object, id="datetime"),
        ),
    )
    def test_format_hour(self, attribute):
        assert "3:30 pm" == utils.format_hour(attribute)

    @pytest.mark.parametrize(
        ("attribute"),
        (
            pytest.param(date_string, id="string"),
            pytest.param(date_object, id="datetime"),
        ),
    )
    def test_format_date(self, attribute):
        assert "Wednesday 2024-12-25" == utils.format_date(attribute, dayname=True)
        assert "2024-12-25" == utils.format_date(attribute, dayname=False)

    def test_coordinates(self, mock_get_request):
        data = utils.get_current_coordinates()
        assert data["latitude"] == "00.0000"
        assert data["longitude"] == "-11.1111"
