from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SimpleWeather:
	weather_description: str
	cur_weather: str
	humidity: str
	pressure: str
	wind: str
	uvi: str
