"""Module that creates the Model of a Forecast Class"""

from datetime import datetime

from pydantic import BaseModel, Field, model_validator
from SunCastPy.utils.utils import format_date, format_hour


class Forecast(BaseModel):
    """Extract the forecast and rain probability for each time frame"""

    short_forecast: str = Field(alias="shortForecast")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    temperature: int
    temperature_unit: str = Field(alias="temperatureUnit")
    wind_speed: str = Field(alias="windSpeed")
    wind_direction: str = Field(alias="windDirection")
    probability_of_precipitation: int
    image_url: str = Field(alias="icon")

    @model_validator(mode="before")
    @classmethod
    def flatten_data(cls, data):
        """Function used with pydantic to get value from nested dict

        Args:
            data (pydantic): Raw data from input

        Returns:
            data: Formatted to move nested values to top
        """
        pop = data.get("probabilityOfPrecipitation", {})
        data["probability_of_precipitation"] = pop.get("value")
        return data

    @property
    def day_name(self) -> str:
        """Extract the day name from the data time"""
        return self.start_time.strftime("%A")

    def __str__(self) -> str:  # pragma: no cover
        return (
            f"{format_date(self.start_time, dayname=False)}"
            + f"\t{format_hour(self.start_time)} - {format_hour(self.end_time)}"
            + f"\tForecast = {self.short_forecast}\t"
            + f"\tProbability of Precipitation =  {self.probability_of_precipitation}"
        )
