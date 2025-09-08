from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.filters import IsAdminFilter
from bot.keyboards import make_category_buttons
from database.base import db
from database.products import Category

admin_router = Router()
admin_router.message.filter(IsAdminFilter())


@admin_router.message(Command('drop-all'))
async def command_drop_all_handler(message: Message) -> None:
    db.drop_all()
    await message.answer(f"Dropped all tables")


@admin_router.message(Command('category'))
async def category_handler(message: Message):
    ikm = make_category_buttons()
    await message.answer('Category list', reply_markup=ikm.as_markup())


@admin_router.callback_query(F.data.startswith('change_'))
async def category_change_handler(callback_query: CallbackQuery):
    category_id = callback_query.data.removeprefix('change_')
    # TODO


@admin_router.callback_query(F.data.startswith('delete_'))
async def category_change_handler(callback_query: CallbackQuery):
    category_id = callback_query.data.removeprefix('delete_')
    Category.delete(category_id)
    ikm = make_category_buttons()

    await callback_query.message.edit_text('Category list', callback_query.inline_message_id,
                                           reply_markup=ikm.as_markup())
    await callback_query.answer(f'{category_id} deleted', show_alert=True)
