from aiogram import Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types.input_media import InputMedia
from aiogram.dispatcher.filters import Text

from tgbot.database.sqlite_db import create_user, set_coord_from_user
from tgbot.keyboards.reply import ReplyMarkupName, get_reply_user
from tgbot.misc.states import UserStates
from tgbot.keyboards.inline import get_inline_user, InlineMarkupName
from tgbot.services.get_city import get_city
from tgbot.services.get_weather import get_weather


async def start(message: types.Message):
    await message.bot.send_chat_action(message.chat.id, 'typing')
    await UserStates.location.set()
    markup = get_reply_user(ReplyMarkupName.start)
    await message.answer('👋🏻Привет! Я - твой персональный бот для погоды🌤\n\n'
                        '🔅 Я могу помочь узнать текущую погоду;\n'
                        '🔅 Дать рекомендации по выбору одежды/обуви/аксессуаров в зависимости от погоды;\n'
                        '🔅 Ты можешь посмотреть результаты и поучаствовать в опросе о том, как ощущается погода на улице\n'
                        '🔅 Я могу дать рекомендации по защите от солнца, учитывая УФ индекс;\n'
                        '🔅 Подскажу, когда начинается рассвет или закат;\n'
                        '🔅 Предоставлю рекомендации по занятию спортом на улице в зависимости от погоды;\n'
                        '🔅 Поделюсь информацией о текущем качестве воздуха.\n\n'
                        'Давай начнем!\n'
                        '✍🏻 Напиши название своего населенного пункта или\n'
                        '🗺 Отправьте свою геолокацию!',
                        parse_mode="html",
                        reply_markup=markup)

async def location(message: types.Message, state: FSMContext):
    # Получение геолокации от пользователя
    coord = [message.location.latitude, message.location.longitude]
    create_user(message.from_user.id, message.from_user.username, message.from_user.first_name, coord)
    # Вывод полученных координат
    await weather(message, state, coord)

    # get_weather(coord)

async def city(message: types.Message, state: FSMContext):
    city, coord = get_city(message.text)
    create_user(message.from_user.id, message.from_user.username, message.from_user.first_name, coord)
    markup = get_inline_user(InlineMarkupName.city)
    await message.answer(f"Указан город: {city}\n Верно?", reply_markup=markup)

async def city_yes(call: types.CallbackQuery, state: FSMContext):
    coord = set_coord_from_user(call.from_user.id)
    await weather(call.message, state, coord)

async def city_no(call: types.CallbackQuery, state: FSMContext):

    # city = get_city(message.text)
    #
    # markup = get_inline_user(InlineMarkupName.start)
    await call.message.answer(f"cryyy")

async def weather(message: types.Message, state: FSMContext, coord=[0,0]):
    print(coord)
    text = get_weather(coord)
    await message.answer(text)


def user(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state='*')
    dp.register_message_handler(location, content_types='location', state=UserStates.location)
    dp.register_message_handler(city, state=UserStates.location)
    dp.register_callback_query_handler(city_yes, Text(startswith="city_yes"), state=UserStates.location)
    dp.register_callback_query_handler(city_no, Text(startswith="city_no"), state=UserStates.location)