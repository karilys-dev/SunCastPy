from datetime import datetime
from SunCastPy.utils import get_request


class ShortForecast:
    def __init__(self, property) -> None:
        self.shortForecast = property["shortForecast"]
        self.longStartTime = property["startTime"]
        self.longEndTime = property["endTime"]
        fmt = lambda s: datetime.fromisoformat(s).strftime("%-I %p").lower()
        self.startTime = fmt(self.longStartTime)
        self.endTime = fmt(self.longEndTime)


class LocalWeather:
    def __init__(self, latitude: float, longitude: float) -> None:
        _details = get_request(f"https://api.weather.gov/points/{latitude},{longitude}")
        _forecast = _details.get("properties", {}).get("forecastHourly")
        self.periods: list[dict] = get_request(_forecast)["properties"]["periods"]
        self.shortForecast: list[ShortForecast] = [
            ShortForecast(property=p) for p in self.periods
        ]
