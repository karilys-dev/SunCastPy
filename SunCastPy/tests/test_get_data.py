from SunCastPy.NOAA_Forecast import Forecast, LocalWeather


class Test_LocalWeather:
    def test_has_attributes(self, sample_data):
        data: LocalWeather = sample_data["LocalWeather"]
        assert hasattr(data, "periods")
        assert hasattr(data, "forecast")
        assert isinstance(data.forecast, list)
        assert isinstance(data.forecast[0], Forecast)


class Test_Forecast:
    def test_has_attributes(self, sample_data):
        data: Forecast = sample_data["Forecast"][0]
        expected_attributes: list[str] = [
            "short_forecast",
            "probability_of_precipitation",
            "start_time",
            "end_time",
            "temperature",
            "temperature_unit",
            "wind_speed",
            "wind_direction",
        ]
        for item in expected_attributes:
            assert hasattr(data, item), f"Attribute [{item}] not found."

    def test_repr(self, sample_data):
        data: Forecast = sample_data["Forecast"][0]
        assert data._format_hour(data.start_time) == "4 pm"
        assert (
            repr(data)
            == "forecast = Chance Rain Showers start = 4 pm end = 5 pm chance of rain = 60"
        )
