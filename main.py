import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot) -> None:
    rkm = ReplyKeyboardBuilder()
    rkm.row(
        KeyboardButton(text='2'),
        KeyboardButton(text='2')
    )
    rkm.row(
        KeyboardButton(text='1'),
        KeyboardButton(text='1'),
        KeyboardButton(text='hello'),
    )

    await message.answer(f"Hello, Python!", reply_markup=rkm.as_markup())


@dp.message(F.text == 'hello')
async def echo_handler(message: Message) -> None:
    await message.answer("hello degan button bosildi")


async def main() -> None:
    bot = Bot("8329233522:AAGJWMJuYZPe2z1Qj-siN5glrk9bYu60r4U", default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


"""

7  8  9 ➕
4  5️⃣  6 -
1  2  3 *
0 <-  = ➗

"""