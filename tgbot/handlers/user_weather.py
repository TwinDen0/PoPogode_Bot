import random

from aiofiles import os
from aiogram import Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.input_media import InputMedia
from aiogram.dispatcher.filters import Text

from tgbot.database.db_clothes import get_clothes_sql
from tgbot.database.sqlite_db import create_user, get_coord_db, get_city_sql, check_user_exists, check_reminder_exists, \
	del_reminder, set_user_clock_reminder
from tgbot.handlers.user_reg import find_city
from tgbot.keyboards.reply import ReplyMarkupName, get_reply_user
from tgbot.misc.states import UserStates
from tgbot.keyboards.inline import get_inline_user, InlineMarkupName
from tgbot.models.Coordinates import Coordinates
from tgbot.models.SetClothes import SetClothes
from tgbot.services import layering
from tgbot.services.get_city import get_city
from tgbot.services.get_clothes import get_clothes
from tgbot.services.get_ip import get_coordinates, get_city_from_coord
from tgbot.services.get_weather import get_weather

from PIL import Image, ImageDraw, ImageFont


async def get_clothes_mess(call: types.CallbackQuery, state: FSMContext, test_data=None):
	await call.message.edit_text(f"Отлично! Теперь я могу подсказать, что вам надеть!", reply_markup=None)
	await mess_clothes(call.message, state, test_data)

async def mess_clothes(message: types.Message, state: FSMContext, test_data=None):
	user_exists = check_user_exists(message.chat.id)
	if not user_exists:
		await message.answer('<b>Для начала работы с ботом используйте команду: /start </b>',
		                     parse_mode="html")
		return
	# await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup = None)
	if not test_data:
		coord = get_coord_db(message.chat.id)
		simple_weather = get_weather(coord)
	else:
		simple_weather = test_data

	# написать взятие погоды и её анализ
	print(simple_weather)

	clothes = get_clothes(simple_weather)
	clothes = SetClothes(head=clothes.head, body=clothes.body, legs=clothes.legs, shoes=clothes.shoes,
	                     accessories=clothes.accessories)
	print(clothes)
	# count_clothes =

	if clothes.body.outerwear.name != '':
		bady_text = f'{clothes.body.outerwear.name} + {clothes.body.underwear.name}'
		outerwear = clothes.body.outerwear.img
	else:
		bady_text = f'{clothes.body.underwear.name}'
		outerwear = None

	res_accessorie = ''
	for i in range(0, len(clothes.accessories)):
		res_accessorie += clothes.accessories[i].name
		print(i, res_accessorie)
		if i < len(clothes.accessories) - 1:
			res_accessorie += " + "

	img_path = layering.clothes_layering(outerwear=outerwear, underwear=clothes.body.underwear.img, undies=None,
	                                     legs=clothes.legs.img, shoes=clothes.shoes.img, accessories=None)

	photo = open(img_path, 'rb')

	await message.answer_photo(photo, caption=f'Сегодня на улице: {simple_weather.weather_description}\n'
	                                               f'Температура: {"{:.0f}".format(float(simple_weather.cur_weather))}С°\n\n'
	                                               f'Рекомендации по одежде\n\n'
	                                               f'🧢 Головной убор: {clothes.head.name}\n'
	                                               f'👔 Тело: {bady_text}\n'
	                                               f'👖 Ноги: {clothes.legs.name}\n'
	                                               f'👟 Обувь: {clothes.shoes.name}\n\n'
	                                               f'🕶Рекомендую взять с собой следующие аксессуары: {res_accessorie}\n\n',
	                                parse_mode="html")


async def weather(message: types.Message, state: FSMContext, coord=[0, 0]):
	print(coord)
	text = get_weather(coord)

	# get_weather(coord)
	await message.answer(text)


async def test(message: types.Message, state: FSMContext):
	img_path = layering.clothes_layering('./tgbot/img/fon2.png',
	                                     ['./tgbot/img/insulated_trousers_2.png', './tgbot/img/down_jacket_2.png'],
	                                     ['./tgbot/img/down_jacket_1.png', './tgbot/img/sweater_yellow_1.png'])

	photo = open(img_path, 'rb')
	await message.answer_photo(photo,
	                           caption=f'✨ <i>Готово!</i> ✨\n\n',
	                           parse_mode='html')


# try:
# 	os.remove(reply_img)
# except Exception as e:
# 	print(e)

async def mess_weather(message: types.Message, state: FSMContext):
	user_exists = check_user_exists(message.chat.id)
	if not user_exists:
		await message.answer('<b>Для начала работы с ботом используйте команду: /start </b>',
		                     parse_mode="html")
		return
	coord = get_coord_db(message.chat.id)
	simple_weather = get_weather(coord)
	city = get_city_sql(message.chat.id)
	temp = round(int(simple_weather.cur_weather))
	if temp - int(simple_weather.cur_weather) >= 0.5:
		temp += 1
	await message.answer(f"<i>Погода в <b>{city}</b>:</i>\n"
	                     f"{simple_weather.weather_description}\n"
	                     f"Температура: <b>{temp}°С</b> 🌡\n"
	                     f"Ветер: <b>{simple_weather.wind} м/с</b> 🪁\n"
	                     f"Влажность: <b>{simple_weather.humidity}%</b> 💧")

async def mess_reminder(message: types.Message, state: FSMContext):
	flag_reminder = check_reminder_exists(message.from_user.id)
	if flag_reminder:
		markup = get_inline_user(InlineMarkupName.change_reminder)
		await message.answer(f"Хотите <b>изменить</b> или <b>удалить</b> ежедневное <b>напоминание</b>?", reply_markup=markup)
	else:
		markup = get_inline_user(InlineMarkupName.set_reminder)
		await message.answer(f"Хотите установить ежедневное <b>напоминание</b>?", reply_markup=markup)

async def set_reminder(call: types.CallbackQuery, state: FSMContext):
	markup = get_inline_user(InlineMarkupName.clok_reminder)
	await call.message.edit_text(f"Выберите время напоминания:", reply_markup=markup)

async def set_clock_reminder(call: types.CallbackQuery, state: FSMContext):
	hour = call.data.split("_")[1]
	minute = call.data.split("_")[2]
	set_user_clock_reminder(f"{hour}:{minute}", call.from_user.id)
	await call.message.edit_text(f"<b>Напоминание установлено!</b>🎉")

async def no_set_reminder(call: types.CallbackQuery, state: FSMContext):
	await call.message.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	await call.message.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)


async def another_clock_reminder(call: types.CallbackQuery, state: FSMContext):
	await UserStates.set_reminder.set()
	await call.message.edit_text(f'Введите время <b>в формате "9:00"</b> ↓ ')

async def set_another_clock_reminder(message: types.Message, state: FSMContext):
	try:
		hour = message.text.split(":")[0]
		minute = message.text.split(":")[1]
		if minute[0] == 0 and len(minute) > 1:
			minute = minute[1:]
		if not 0 <= int(hour) <= 23:
			raise Exception()
		if not 0 <= int(minute) <= 60:
			raise Exception()
		set_user_clock_reminder(f"{hour}:{minute}", message.from_user.id)
		await message.answer(f"<b>Напоминание установлено!</b>🎉")
		await state.reset_data()
	except Exception as e:
		await message.v(f'<b>Ошибка, неверный формат!</b>\nПопробуйте ещё раз:')


async def delete_reminder(call: types.CallbackQuery, state: FSMContext):
	del_reminder(call.message.from_user.id)
	await call.message.edit_text(f"Напоминание удалено")


async def mess_change_city(message: types.Message, state: FSMContext):
	user_exists = check_user_exists(message.chat.id)
	if not user_exists:
		await message.answer('<b>Для начала работы с ботом используйте команду: /start </b>',
		                     parse_mode="html")
		return
	await UserStates.pref_coord.set()
	await find_city(message, change=True)

async def mess_help(message: types.Message, state: FSMContext):
	user_exists = check_user_exists(message.chat.id)
	if not user_exists:
		await message.answer('<b>Для начала работы с ботом используйте команду: /start </b>',
		                     parse_mode="html")
		return
	await message.answer(f"<b>Команды бота: </b>\n\n"
							"/weather - Пришлю информацию о погоде на сегодня.\n\n"
							"/clothes - Подскажу, что лучше надеть сегодня, исходя из погоды и времени года.\n\n"
							"/sport - Подскажу, какие одежду лучше выбрать для занятий спортом.\n\n"
							"/reminder - Укажи время, в которое хочешь получать ежедневные советы о том, что надеть.\n\n"
							"/change_city - позволит тебе поменять город для получения информации о погоде и подсказок о том, что надеть.")


def register_user_weather(dp: Dispatcher):
	dp.register_message_handler(mess_clothes, commands="clothes", state='*')
	dp.register_callback_query_handler(get_clothes_mess, Text(startswith="get_clothes"), state=UserStates.weather)
	dp.register_message_handler(test, commands="test_img", state='*')
	dp.register_message_handler(mess_weather, commands="weather", state='*')
	dp.register_message_handler(mess_reminder, commands="reminder", state='*')
	dp.register_message_handler(mess_change_city, commands="change_city", state='*')
	dp.register_message_handler(mess_help, commands="help", state='*')
	dp.register_callback_query_handler(set_reminder, Text(startswith="set_reminder"), state='*')
	dp.register_callback_query_handler(no_set_reminder, Text(startswith="no_set_reminder"), state='*')
	dp.register_callback_query_handler(set_clock_reminder, Text(startswith="reminder_"), state='*')
	dp.register_callback_query_handler(another_clock_reminder, Text(startswith="another_clock_reminder"), state='*')
	dp.register_message_handler(set_another_clock_reminder, state=UserStates.set_reminder)
	dp.register_callback_query_handler(delete_reminder, Text(startswith="delete_reminder"), state='*')

