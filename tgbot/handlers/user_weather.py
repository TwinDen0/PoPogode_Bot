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
from tgbot.services.get_city import get_city
from tgbot.services.get_clothes import get_clothes
from tgbot.services.get_ip import get_coordinates, get_city_from_coord
from tgbot.services.get_weather import get_weather


async def get_clothes_mess(call: types.CallbackQuery, state: FSMContext):
	coord = get_coord_db(call.message.chat.id)
	simple_weather = get_weather(coord)

	# написать взятие погоды и её анализ
	print(simple_weather)

	clothes = get_clothes(simple_weather)
	clothes = SetClothes(head=clothes.head, body=clothes.body, legs=clothes.head, shoes=clothes.head, accessories=clothes.head)
	print(clothes)

	if clothes.body.outerwear.name != '':
		bady_text = f'{clothes.body.outerwear.name} + {clothes.body.underwear.name}'
	else:
		bady_text = f'{clothes.body.underwear.name}'

	await call.message.answer(f'Сегодня на улице: {simple_weather.weather_description}\n'
                            f'Температура: {"{:.2f}".format(float(simple_weather.cur_weather))}С°\n\n'
							f'Рекомендации по одежде\n\n'
							f'🧢Головной убор: {clothes.head.name}\n'
							f'👔Тело: {bady_text}\n'
							f'👖Ноги: \n'
							f'👟Обувь: \n\n'
							f'🕶Рекомендую взять с собой следующие аксессуары: \n\n', parse_mode="html")


async def weather(message: types.Message, state: FSMContext, coord=[0, 0]):
	print(coord)
	text = get_weather(coord)

	# get_weather(coord)
	await message.answer(text)


def register_user_weather(dp: Dispatcher):
	dp.register_callback_query_handler(get_clothes_mess, Text(startswith="get_clothes"), state=UserStates.weather)

