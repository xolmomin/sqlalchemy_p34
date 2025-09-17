from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.products import Category


def make_category_buttons():
    ikm = InlineKeyboardBuilder()
    categories = Category.get_all()
    for category in categories:
        ikm.row(
            InlineKeyboardButton(text=category.name, callback_data='123'),
            InlineKeyboardButton(text='✏️', callback_data=f'change_{category.id}'),
            InlineKeyboardButton(text='❌', callback_data=f'delete_{category.id}'),
        )
    return ikm
