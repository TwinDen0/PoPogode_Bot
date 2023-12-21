import random

from aiofiles import os
from aiogram import Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.input_media import InputMedia
from aiogram.dispatcher.filters import Text

from tgbot.database.db_clothes import get_clothes_sql
from tgbot.database.sqlite_db import create_user, get_coord_db
from tgbot.keyboards.reply import ReplyMarkupName, get_reply_user
from tgbot.misc.states import UserStates
from tgbot.keyboards.inline import get_inline_user, InlineMarkupName
from tgbot.models.SetClothes import SetClothes
from tgbot.services import layering
from tgbot.services.get_city import get_city
from tgbot.services.get_clothes import get_clothes
from tgbot.services.get_ip import get_coordinates, get_city_from_coord
from tgbot.services.get_weather import get_weather

from PIL import Image, ImageDraw, ImageFont


async def get_clothes_mess(call: types.CallbackQuery, state: FSMContext, test_data = None):
	if not test_data:
		coord = get_coord_db(call.message.chat.id)
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
	else:
		bady_text = f'{clothes.body.underwear.name}'

	res_accessorie = ''
	for i in range(0, len(clothes.accessories)):
		res_accessorie += clothes.accessories[i].name
		print(i, res_accessorie)
		if i < len(clothes.accessories) - 1:
			res_accessorie += " + "

	img_path = layering.clothes_layering('./tgbot/img/fon_4+ac.png',
	                                     [f'./tgbot/img/{clothes.legs.img}_2.png', f'./tgbot/img/{clothes.body.underwear.img}_2.png'],
	                                     [f'./tgbot/img/{clothes.legs.img}_1.png', f'./tgbot/img/{clothes.body.underwear.img}_1.png'])

	photo = open(img_path, 'rb')

	await call.message.answer_photo(photo, caption=f'Сегодня на улице: {simple_weather.weather_description}\n'
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


def register_user_weather(dp: Dispatcher):
	dp.register_callback_query_handler(get_clothes_mess, Text(startswith="get_clothes"), state=UserStates.weather)
	dp.register_message_handler(test, commands="test_img", state='*')
