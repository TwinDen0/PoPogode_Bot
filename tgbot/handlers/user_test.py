from aiogram import Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_media import InputMedia
from aiogram.dispatcher.filters import Text

from tgbot.database.sqlite_db import create_user, get_coord_db, get_city_sql
from tgbot.handlers.user_weather import get_clothes_mess
from tgbot.keyboards.reply import ReplyMarkupName, get_reply_user
from tgbot.misc.states import UserStates
from tgbot.keyboards.inline import get_inline_user, InlineMarkupName
from tgbot.models.Coordinates import Coordinates
from tgbot.models.SimpleWeather import SimpleWeather
from tgbot.services.get_city import get_city
from tgbot.services.get_ip import get_coordinates, get_city_from_coord
from tgbot.services.get_weather import get_weather
from aiogram.dispatcher.filters.state import State, StatesGroup


class TestStates(StatesGroup):
	temp = State()
	descript = State()
	weather = State()

async def start_test(message: types.Message):
	await message.bot.send_chat_action(message.chat.id, 'typing')
	await TestStates.temp.set()
	await message.answer('<i>Включен режим тестирования.</i>\n\n'
	                     'Необходимо ввести следующие данные:\n'
	                     '• Температура;\n'
	                     '• Описание погоды;\n\n'
	                     '<b>Введите температуру, например "-20":</b>',
	                     parse_mode="html",
	                     reply_markup=ReplyKeyboardRemove())

temp = "-10"

async def get_temp(message: types.Message, state: FSMContext):
	global temp
	temp = message.text
	await TestStates.descript.set()
	if int(temp) > 0:
		markup = InlineKeyboardMarkup(
			inline_keyboard=[
				[
					InlineKeyboardButton('Ясно☀️', callback_data='test_descript_clear'),
					InlineKeyboardButton('Облачно⛅️', callback_data='test_descript_clouds'),
				],
				[
					InlineKeyboardButton('Дождь🌦', callback_data='test_descript_rain'),
					InlineKeyboardButton('Ливень🌧', callback_data='test_descript_drizzle'),
				],
				[
					InlineKeyboardButton('Гроза🌩', callback_data='test_descript_thunderstorm'),
					InlineKeyboardButton('Туман🌫', callback_data='test_descript_mist'),
				],
			]
		)
	elif int(temp) < 0:
		markup = InlineKeyboardMarkup(
			inline_keyboard=[
				[
					InlineKeyboardButton('Ясно☀️', callback_data='test_descript_clear'),
					InlineKeyboardButton('Облачно⛅️', callback_data='test_descript_clouds'),
				],
				[
					InlineKeyboardButton('Снег❄️', callback_data='test_descript_snow'),
					InlineKeyboardButton('Туман🌫', callback_data='test_descript_mist'),
				],
			]
		)
	else:
		markup = InlineKeyboardMarkup(
			inline_keyboard=[
				[
					InlineKeyboardButton('Ясно☀️', callback_data='test_descript_clear'),
					InlineKeyboardButton('Облачно⛅️', callback_data='test_descript_clouds'),
				],
				[
					InlineKeyboardButton('Дождь🌦', callback_data='test_descript_rain'),
					InlineKeyboardButton('Ливень🌧', callback_data='test_descript_drizzle'),
				],
				[
					InlineKeyboardButton('Гроза🌩', callback_data='test_descript_thunderstorm'),
					InlineKeyboardButton('Туман🌫', callback_data='test_descript_mist'),
				],
				[
					InlineKeyboardButton('Снег❄️', callback_data='test_descript_snow'),
				],
			]
		)

	await message.answer('Температура введена.\n\n'
	                     '<b>Выберите описание погоды:</b>',
	                     parse_mode="html",
	                     reply_markup=markup)

async def get_descript(call: types.CallbackQuery, state: FSMContext):
	descript = call.data.split("_")[2]

	if descript == "clear":
		descript = "Ясно☀️"
	if descript == "clouds":
		descript = "Облачно⛅️"
	if descript == "rain":
		descript = "Дождь🌦"
	if descript == "drizzle":
		descript = "Ливень🌧"
	if descript == "thunderstorm":
		descript = "Гроза🌩"
	if descript == "snow":
		descript = "Снег❄️"
	if descript == "mist":
		descript = "Туман🌫"

	await call.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

	await call.message.answer('Получены следующие данные:\n'
		                      f'• Температура = {temp}\n'
		                      f'• Описание погоды = {descript}\n\n'
		                      f'<i>Запускаю подбор одежды</i>',
	                          parse_mode="html")


	test_data = SimpleWeather(weather_description=descript, cur_weather=temp, humidity='', pressure='', wind='',
                     uvi='')

	await state.reset_state()
	await get_clothes_mess(call, state, test_data)


def register_user_test(dp: Dispatcher):
	dp.register_message_handler(start_test, commands="test", state='*')
	dp.register_message_handler(get_temp, state=TestStates.temp)
	dp.register_callback_query_handler(get_descript, Text(startswith="test_descript"), state=TestStates.descript)
