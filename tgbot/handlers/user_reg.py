from aiogram import Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.input_media import InputMedia
from aiogram.dispatcher.filters import Text

from tgbot.database.sqlite_db import create_user, get_coord_db, get_city_sql
from tgbot.keyboards.reply import ReplyMarkupName, get_reply_user
from tgbot.misc.states import UserStates
from tgbot.keyboards.inline import get_inline_user, InlineMarkupName
from tgbot.models.Coordinates import Coordinates
from tgbot.services.get_city import get_city
from tgbot.services.get_ip import get_coordinates, get_city_from_coord
from tgbot.services.get_weather import get_weather


async def start(message: types.Message):
	await message.bot.send_chat_action(message.chat.id, 'typing')
	await UserStates.pref_coord.set()
	await message.answer('👋🏻Привет! Я - твой персональный бот для погоды🌤\n\n'
	                     '• Я могу помочь узнать текущую погоду;\n'
	                     '• Дать рекомендации по выбору одежды/обуви/аксессуаров в зависимости от погоды;\n'
	                     '• Ты можешь посмотреть результаты и поучаствовать в опросе о том, как ощущается погода на улице\n'
	                     '• Я могу дать рекомендации по защите от солнца, учитывая УФ индекс;\n'
	                     '• Подскажу, когда начинается рассвет или закат;\n'
	                     '• Предоставлю рекомендации по занятию спортом на улице в зависимости от погоды;\n'
	                     '• Поделюсь информацией о текущем качестве воздуха.\n\n'
	                     '<i>Узнаю ваш город...</i>',
	                     parse_mode="html",
	                     reply_markup=ReplyKeyboardRemove())
	await pref_coord(message)


async def pref_coord(message: types.Message):
	coord = get_coordinates()
	city = get_city_from_coord(coord)
	markup = get_inline_user(InlineMarkupName.pref_coord)
	create_user(message.from_user.id, message.from_user.username, message.from_user.first_name, city,
	            [coord.latitude, coord.longitude])
	await message.answer(f"Ваш город: <b>{city}</b>\nВерно?", parse_mode="html", reply_markup=markup)


async def pref_coord_yes(call: types.CallbackQuery, state: FSMContext):
	await UserStates.weather.set()
	await end_reg(call.message)


async def pref_coord_no(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
	await UserStates.location.set()
	markup = get_reply_user(ReplyMarkupName.locale)
	await call.message.answer("Тогда:\n"
	                          "✍🏻 Напиши название своего населенного пункта или\n"
	                          "🗺 Отправь свою геолокацию!", parse_mode="html", reply_markup=markup)


async def location(message: types.Message, state: FSMContext):
	# Получение геолокации от пользователя
	coord = [message.location.latitude, message.location.longitude]
	city = get_city_from_coord(Coordinates(latitude=coord[0], longitude=coord[1]))
	create_user(message.from_user.id, message.from_user.username, message.from_user.first_name, city, coord)
	# Вывод полученных координат
	await end_reg(message)


async def city(message: types.Message, state: FSMContext):
	city, coord = get_city(message.text)
	create_user(message.from_user.id, message.from_user.username, message.from_user.first_name, city, coord)
	markup = get_inline_user(InlineMarkupName.city)
	await message.answer(f"Указан город: <b>{city}</b>\nВерно?", reply_markup=markup)
async def city_yes(call: types.CallbackQuery, state: FSMContext):
	await UserStates.weather.set()
	await end_reg(call.message)
async def city_no(call: types.CallbackQuery, state: FSMContext):
	await call.message.answer(f"Напиши город ещё раз:")


async def end_reg(message: types.Message):
	city = get_city_sql(message.chat.id)
	await message.edit_text(f"Ваш город: <b>{city}</b>", reply_markup=None)
	await UserStates.weather.set()
	markup = get_inline_user(InlineMarkupName.end_reg)
	await message.answer(f"Отлично! Теперь я могу подсказать, что вам надеть!", reply_markup=markup)


def register_user_reg(dp: Dispatcher):
	dp.register_message_handler(start, commands="start", state='*')
	dp.register_callback_query_handler(pref_coord_yes, Text(startswith="pref_yes"), state=UserStates.pref_coord)
	dp.register_callback_query_handler(pref_coord_no, Text(startswith="pref_no"), state=UserStates.pref_coord)
	dp.register_message_handler(location, content_types='location', state=UserStates.location)
	dp.register_message_handler(city, state=UserStates.location)
	dp.register_callback_query_handler(city_yes, Text(startswith="city_yes"), state=UserStates.location)
	dp.register_callback_query_handler(city_no, Text(startswith="city_no"), state=UserStates.location)
