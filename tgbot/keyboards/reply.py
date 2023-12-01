from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import enum

class ReplyMarkupName(enum.Enum):
    standard = 0
    locale = 1
    profile = 2


def get_reply_user(markup_name, param=None):
    markup = None
    if (markup_name == ReplyMarkupName.standard):
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                KeyboardButton('Поделиться', request_location=True)
                ]
            ], resize_keyboard=True
            )
        return markup
    if (markup_name == ReplyMarkupName.locale):
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                KeyboardButton('Поделиться геолокацией📍', request_location=True)
                ]
            ], resize_keyboard=True
            )
        return markup
    return markup