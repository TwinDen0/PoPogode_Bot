from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
import enum

class InlineMarkupName(enum.Enum):
    city = 1
    pref_coord = 2
    end_reg = 3
    change_reminder = 4
    set_reminder = 5
    clok_reminder = 6

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

    if (markup_name == InlineMarkupName.change_reminder):
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                InlineKeyboardButton('Изменить', callback_data='set_reminder'),
                InlineKeyboardButton('Удалить', callback_data='delete_reminder'),
                ],
            ]
        )
        return markup

    if (markup_name == InlineMarkupName.set_reminder):
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                InlineKeyboardButton('Да', callback_data='set_reminder'),
                InlineKeyboardButton('Нет', callback_data='no_set_reminder'),
                ],
            ]
        )
        return markup

    if (markup_name == InlineMarkupName.clok_reminder):
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                InlineKeyboardButton('7:00', callback_data='reminder_7_00'),
                InlineKeyboardButton('7:30', callback_data='reminder_7_30'),
                InlineKeyboardButton('8:00', callback_data='reminder_8_00'),
                ],
                [
                InlineKeyboardButton('8:30', callback_data='reminder_8_30'),
                InlineKeyboardButton('9:00', callback_data='reminder_9_00'),
                InlineKeyboardButton('9:30', callback_data='reminder_9_30'),
                ],
                [
                InlineKeyboardButton('Указать другое время', callback_data='another_clock_reminder'),
                ],
            ]
        )
        return markup

    return markup

