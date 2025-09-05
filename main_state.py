import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import settings

dp = Dispatcher()


class Form(StatesGroup):
    full_name = State()
    phone = State()
    programming_language = State()
    schedule_time = State()


@dp.message(CommandStart())
async def start_command_handler(message: Message):
    rkm = ReplyKeyboardBuilder()
    rkm.add(KeyboardButton(text='Kursga yozilish ☎️'))
    await message.answer("Menyular", reply_markup=rkm.as_markup(resize_keyboard=True))


@dp.message(F.text == 'Kursga yozilish ☎️')
async def start_handler(message: Message, state: FSMContext):
    await state.set_state(Form.full_name)
    rkm = ReplyKeyboardRemove()
    await message.answer('Ismingizni kiriting', reply_markup=rkm)


@dp.message(Form.full_name)
async def get_full_name_handler(message: Message, state: FSMContext):
    full_name = message.text  # botir
    await state.update_data({'full_name': full_name})

    await state.set_state(Form.phone)
    rkm = ReplyKeyboardBuilder()
    rkm.add(KeyboardButton(text='Nomer yuborish', request_contact=True))

    await message.answer('Telefon nomerni kiritish uchun tugmani bosing',
                         reply_markup=rkm.as_markup(resize_keyboard=True))


@dp.message(Form.phone, F.content_type.in_({ContentType.CONTACT}))
async def get_phone_handler(message: Message, state: FSMContext):
    phone = message.contact.phone_number.removeprefix('+')  # 998901001010
    await state.update_data({'phone': phone})

    await state.set_state(Form.programming_language)
    rkm = ReplyKeyboardBuilder()
    rkm.row(
        KeyboardButton(text='Java'),
        KeyboardButton(text='Python'),
        KeyboardButton(text='Js'),
    )
    await message.answer('Dasturlash tilini kiriting', reply_markup=rkm.as_markup(resize_keyboard=True))


@dp.message(Form.programming_language, F.text.func(lambda text: text.lower() in ('python', 'java', 'js')))
async def get_programming_language(message: Message, state: FSMContext):
    programming_language = message.text  # python
    await state.update_data({'programming_language': programming_language.title()})

    await state.set_state(Form.schedule_time)
    rkm = ReplyKeyboardRemove()
    await message.answer('Vaqtini kiriting', reply_markup=rkm)


@dp.message(Form.schedule_time)
async def get_schedule_time(message: Message, state: FSMContext):
    schedule_time = message.text  # 15:00
    await state.update_data({'schedule_time': schedule_time})

    data = await state.get_data()
    text = (
        f"_Hurmatli {message.from_user.full_name}\n"
        f"Siz kiritgan malumotlar:_\n"
        f"*Fio*: {data['full_name']}\n"
        f"*Nomer*: ||{data['phone']}||\n"
        f"*Til*: {data['programming_language']}\n"
        f"*Vaqti*: {data['schedule_time']}"
    )

    ikm = InlineKeyboardBuilder()
    ikm.add(InlineKeyboardButton(text='Tasdiqlash ✅', callback_data='confirm'))

    await message.answer(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=ikm.as_markup())


@dp.callback_query(F.data == 'confirm')
async def confirm_handler(callback_data: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    text = (
        f"*Tlg:*: {callback_data.from_user.full_name}\n"
        f"*Fio*: {data['full_name']}\n"
        f"*Nomer*: ||{data['phone']}||\n"
        f"*Til*: {data['programming_language']}\n"
        f"*Vaqti*: {data['schedule_time']}"
    )
    ikm = InlineKeyboardBuilder()
    ikm.add(
        InlineKeyboardButton(text="Qabul qilish ✅", callback_data=f'accept_{callback_data.from_user.id}'),
        InlineKeyboardButton(text="Rad etish ❌", callback_data=f'reject_{callback_data.from_user.id}'),
    )
    await bot.send_message(514411336, text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=ikm.as_markup())
    await state.clear()

    text = "Adminlarga yuborildi, tez orada aloqaga chiqamiz!"
    await callback_data.answer(text, show_alert=True)


@dp.callback_query(F.data.func(lambda data: data.startswith('accept_') or data.startswith('reject_')))
async def confirm_handler(callback_data: CallbackQuery, bot: Bot):
    ikm = InlineKeyboardBuilder()
    if callback_data.data.startswith('accept_'):
        text = "Admin sizni qabul qildi"
        _id = callback_data.data.removeprefix('accept_')
        await bot.send_message(_id, text)
        ikm.add(InlineKeyboardButton(text='Qabul qilingan ✅✅✅', callback_data="df72732g"))
    else:
        text = "Afsuski, kursga qabul qilinmadingiz"
        _id = callback_data.data.removeprefix('reject_')
        await bot.send_message(_id, text)
        ikm.add(InlineKeyboardButton(text='Rad etilgan ❌❌❌', callback_data="df72732g"))

    await callback_data.message.edit_reply_markup(callback_data.inline_message_id, reply_markup=ikm.as_markup())


async def main() -> None:
    bot = Bot(settings.TELEGRAM_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# @pdp_p34_bot
