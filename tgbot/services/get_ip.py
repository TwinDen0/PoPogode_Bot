from urllib.request import urlopen
import json
from translate import Translator

import requests
from environs import Env

from tgbot.models.Coordinates import Coordinates


def _get_ip_data() -> dict:
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    return json.load(response)

def get_coordinates() -> Coordinates:
    """Returns current coordinates using IP address"""
    data = _get_ip_data()
    latitude = data['loc'].split(',')[0]
    longitude = data['loc'].split(',')[1]

    return Coordinates(latitude=latitude, longitude=longitude)


def get_city_from_coord(Coordinates):
    translator = Translator(from_lang="English", to_lang="russian")

    env = Env()
    env.read_env(".env")
    open_weather_token = env.str("OPEN_WEATHER_TOKEN")
    r_weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={Coordinates.latitude}&lon={Coordinates.longitude}&appid={open_weather_token}"
        )
    data = r_weather.json()
    city = data["name"]
    city_Rus = translator.translate(city)
    return city_Rus