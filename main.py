import asyncio
import logging
import os.path
import sys
from typing import Any, Union, Dict

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import Message, BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats, FSInputFile, \
    BotCommandScopeChatAdministrators, BotCommandScopeChatMember, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import settings
from models import User, Product
from models.base import db
from models.products import Category

dp = Dispatcher()

ADMIN_ID = 514411336


class IsAdminFilter(Filter):

    def __init__(self):
        super().__init__()

    async def __call__(self, message: Message):
        return message.from_user.id == ADMIN_ID


@dp.message(CommandStart())
async def start(message: Message):
    categories = Category.get_all()
    rkm = ReplyKeyboardBuilder()
    for category in categories:
        rkm.add(KeyboardButton(text=category.name))

    await message.answer("Menyuni tanlang!", reply_markup=rkm.as_markup())


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


@dp.message(IsAdminFilter(), Command('category'))
async def category_handler(message: Message):
    ikm = make_category_buttons()
    await message.answer('Category list', reply_markup=ikm.as_markup())


@dp.callback_query(F.data.startswith('change_'))
async def category_change_handler(callback_query: CallbackQuery):
    category_id = callback_query.data.removeprefix('change_')


@dp.callback_query(F.data.startswith('delete_'))
async def category_change_handler(callback_query: CallbackQuery):
    category_id = callback_query.data.removeprefix('delete_')
    Category.delete(category_id)
    ikm = make_category_buttons()

    await callback_query.message.edit_text('Category list', callback_query.inline_message_id,
                                           reply_markup=ikm.as_markup())
    await callback_query.answer(f'{category_id} deleted', show_alert=True)


@dp.message()
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


# MEDIA_FOLDER = 'media'
#
#
# async def even_id_filter(message: Message, **kwargs):
#     return message.from_user.id % 2 == 0
#
#
# class NumberFilter(Filter):
#     def __init__(self, my_text: str = 'even') -> None:
#         self.my_text = my_text
#
#     async def __call__(self, message: Message) -> bool:
#         if self.my_text == 'even' and message.from_user.id % 2 == 0:
#             return True
#         else:
#             return False
#
#
# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     user = User.get(message.from_user.id)
#     if user is None:
#         await message.answer("User not found")
#         user_data = message.from_user.model_dump(include={'id', 'first_name', 'last_name', 'username'})
#         user = User.create(**user_data)
#         await message.answer(f"Created user {user.id}")
#     else:
#         await message.answer(f"User {user.id} already exists")
#
#
# @dp.message(Command('drop-all'))
# async def command_drop_all_handler(message: Message) -> None:
#     db.drop_all()
#     await message.answer(f"Dropped all tables")
#
#
# @dp.message(Command("id"))
# async def command_start_handler(message: Message) -> None:
#     await message.answer(str(message.from_user.id))
#
#
# @dp.message(F.content_type.in_({ContentType.PHOTO}))
# async def command_photo_content_type_handler(message: Message, bot: Bot) -> None:
#     file_id = message.photo[-1].file_id
#     file = await bot.get_file(file_id)
#
#     folder_name = file.file_path.split('/')[0]
#     os.makedirs(MEDIA_FOLDER + "/" + folder_name, exist_ok=True)
#     # media/photos/file_5.jpg
#     await bot.download_file(file.file_path, MEDIA_FOLDER + "/" + file.file_path)
#     await message.answer(f"Downloaded photo {file.file_path}")
#
#
# @dp.message(even_id_filter)
# async def command_start_handler(message: Message, bot: Bot) -> None:
#     await message.answer("Button bosing")
#
# @dp.message(lambda msg: msg.from_user.id % 2 == 0)
# async def command_start_handler(message: Message, bot: Bot) -> None:
#     await message.answer("Button bosing")
#

async def startup(bot: Bot) -> None:
    db.create_all()
    # await bot.set_my_name('P34 ning Telegram boti')
    # await bot.send_message(ADMIN_ID, "Bot ishga tushdi")
    # await bot.set_chat_photo(8329233522, FSInputFile('image.jpeg'))
    list_commands = [
        BotCommand(command='start', description='Botni ishga tushirish'),
        BotCommand(command='id', description='Idni korish'),
    ]
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Botni ishga tushirish'),
            BotCommand(command='users_count', description='users count'),
            BotCommand(command='category', description='category larni korish'),
        ],
        scope=BotCommandScopeChat(chat_id=ADMIN_ID)
    )
    await bot.set_my_commands(
        list_commands,
        scope=BotCommandScopeAllPrivateChats()
    )


async def shutdown(bot: Bot) -> None:
    print('bot toxtadi')


async def main() -> None:
    bot = Bot(settings.TELEGRAM_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.shutdown.register(shutdown)
    dp.startup.register(startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

"""

@pdp_p34_bot



admin
/users - userlar soni
/category - category larni chiqarish (inline da)

users


product
users


users,admin

products


state


structure



forma

fio
telefon nomer
dasturlash tili
qaysi vaqt




"""
