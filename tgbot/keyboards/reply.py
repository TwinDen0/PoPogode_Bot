from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import enum

class ReplyMarkupName(enum.Enum):
    start = 1
    profile = 2

def get_reply_user(markup_name, param=None):
    markup = None
    if (markup_name == ReplyMarkupName.start):
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                KeyboardButton('Поделиться геолокацией📍', request_location=True)
                ]
            ], resize_keyboard=True
            )
        return markup
    return markup