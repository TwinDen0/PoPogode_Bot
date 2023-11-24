import datetime
import requests
from environs import Env


def get_weather(coord):
	env = Env()
	env.read_env(".env")
	open_weather_token = env.str("OPEN_WEATHER_TOKEN")

	code_to_smile = {
		"Clear": "Ясно☀️",
		"Clouds": "Облачно⛅️",
		"Rain": "Дождь🌦",
		"Drizzle": "Ливень🌧",
		"Thunderstorm": "Гроза🌩",
		"Snow": "Снег❄️",
		"Mist": "Туман🌫"
	}

	try:
		# Погода
		r_weather = requests.get(
			f"https://api.openweathermap.org/data/2.5/weather?lat={coord[0]}&lon={coord[1]}&appid={open_weather_token}"
		)
		data = r_weather.json()
		weather_description = data["weather"][0]["main"]
		if weather_description in code_to_smile:
			wd = code_to_smile[weather_description]
		else:
			wd = "Посмотри в окно, не пойму что там за погода!"

		city = data["name"]
		cur_weather = data["main"]["temp"]
		humidity = data["main"]["humidity"]
		pressure = data["main"]["pressure"]
		wind = data["wind"]["speed"]
		sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
		sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
		length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
			data["sys"]["sunrise"])

		# УФ индекс
		r_uvi = requests.get(
			f"https://currentuvindex.com/api/v1/uvi?latitude={coord[0]}&longitude={coord[1]}"
		)
		data = r_uvi.json()
		time = data["now"]["time"]
		uvi = data["now"]["uvi"]

		# Качество воздуха
		r_air_pollution = requests.get(
			f"http://api.openweathermap.org/data/2.5/air_pollution?lat={coord[0]}&lon={coord[1]}&appid={open_weather_token}"
		)
		data = r_air_pollution.json()
		air_pollution = data["list"][0]["main"]["aqi"]

		list = {
			1: "Отлично",
			2: "Хорошо",
			3: "Нормально",
			4: "Плохо",
			5: "Очень плохо"
		}

		# Вывод погодных условий
		return (f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"

		        f"Погода в городе: {city}\n\n"

		        f"{wd}\n\n"

		        f"🌡Температура: {cur_weather}F°\n"
		        f"💧Влажность: {humidity}%\n"
		        f"🌀Давление: {pressure} мм.рт.ст\n"
		        f"💨Ветер: {wind} м/с\n\n"

		        f"☀️ УФ-индекс: {uvi}\n"
		        f"🌇Восход солнца: {sunrise_timestamp}\n"
		        f"🌄Закат солнца: {sunset_timestamp}\n"
		        f"🏞Продолжительность дня: {length_of_the_day}\n\n"

		        f"🌫Качетсво воздуха: {list[air_pollution]}\n"
		        f"🏃Пробежка: Плохо\n\n"

		        f"Хорошего дня!"
		        )

	except Exception as ex:
		print(ex)
		print("Проверьте название города")
