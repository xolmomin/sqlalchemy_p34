from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from database import Product
from database.products import Category

user_router = Router()


@user_router.message(CommandStart())
async def start(message: Message):
    categories = Category.get_all()
    rkm = ReplyKeyboardBuilder()
    for category in categories:
        rkm.add(KeyboardButton(text=category.name))

    await message.answer("Menyuni tanlang!", reply_markup=rkm.as_markup())


@user_router.message(Command("id"))
async def command_start_handler(message: Message) -> None:
    await message.answer(str(message.from_user.id))


@user_router.message()
async def product_list(message: Message):
    rkm = ReplyKeyboardRemove()
    await message.answer('Productlar royhati', reply_markup=rkm)

    category = Category.get_by_name(message.text)
    products = Product.get_by_category(category.id)
    for product in products:
        text = f"{product.name} | {product.price}"
        ikm = InlineKeyboardBuilder()
        ikm.row(
            InlineKeyboardButton(text='⬅️', callback_data='1234'),
            InlineKeyboardButton(text='Add Cart 🛒', callback_data='1234'),
            InlineKeyboardButton(text='➡️', callback_data='1234'),
        )
        await message.answer(text, reply_markup=ikm.as_markup())
