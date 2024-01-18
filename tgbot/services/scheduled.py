import asyncio
from datetime import datetime

import pytz
from timezonefinder import TimezoneFinder
from tgbot.database.sqlite_db import get_all_users
from tgbot.services.get_weather import get_weather


async def scheduled(wait_for, bot):
    code_to_smile = {
        "Ясно☀️":"☀️",
        "Облачно⛅️":"⛅️",
        "Дождь🌦":"🌦",
        "Ливень🌧":"🌧",
        "Гроза🌩":"🌩",
        "Снег❄️":"❄️",
        "Туман🌫":"🌫"
    }

    while True:
        users = get_all_users()

        for user in users:
            tf = TimezoneFinder()
            user_tz = pytz.timezone(tf.timezone_at(lng=user['lon'], lat=user['lat']))
            user_now = datetime.now(user_tz)
            if user_now.hour == 12 and user_now.minute == 51:  # Проверяем, что местное время пользователя 9:00 утра

                simple_weather = get_weather((user['lat'], user['lon']))

                temp = round(int(simple_weather.cur_weather))
                if temp - int(simple_weather.cur_weather) >= 0.5:
                    temp += 1

                if temp > 0:
                    temp = "+" + str(temp)
                emoji = code_to_smile[simple_weather.weather_description]
                await bot.send_message(user["id"], f"Сегодня на улице <b>{temp}°C</b> {emoji}\n<b>Хотите узнать, что лучше сегодня надеть?</b>")

        await asyncio.sleep(60)  # Проверяем время каждую минуту