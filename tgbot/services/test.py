import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import types
from aiogram.utils import executor
from datetime import datetime, time

# Токен вашего бота
API_TOKEN = 'YOUR_API_TOKEN'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Функция, которая отправляет ежедневное сообщение "Добрый день!"
