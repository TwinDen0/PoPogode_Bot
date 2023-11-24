from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
import enum

class InlineMarkupName(enum.Enum):
    city = 1

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

    return markup

