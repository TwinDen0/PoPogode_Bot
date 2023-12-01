from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
import enum

class InlineMarkupName(enum.Enum):
    city = 1
    pref_coord = 2
    end_reg = 3

def get_inline_user(markup_name, param=None):
    markup = None

    if (markup_name == InlineMarkupName.city):
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                InlineKeyboardButton('Да', callback_data='city_yes'),
                InlineKeyboardButton('Нет', callback_data='city_no'),
                ],
            ]
        )
        return markup

    if (markup_name == InlineMarkupName.pref_coord):
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                InlineKeyboardButton('Верно', callback_data='pref_yes'),
                ],
                [
                InlineKeyboardButton('Нет', callback_data='pref_no'),
                ],
            ]
        )
        return markup

    if (markup_name == InlineMarkupName.end_reg):
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                InlineKeyboardButton('Подбор одежды', callback_data='get_clothes'),
                ],
                # [
                # InlineKeyboardButton('Узнать УФ индекс', callback_data='get_uv_index'),
                # ],
                # [
                # InlineKeyboardButton('Изменить город', callback_data='change_city'),
                # ]
            ]
        )
        return markup

    return markup

