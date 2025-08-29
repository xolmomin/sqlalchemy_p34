import asyncio
import logging
import os.path
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import Message, BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats, FSInputFile, \
    BotCommandScopeChatAdministrators, BotCommandScopeChatMember

from models import User
from models.base import db

dp = Dispatcher()

ADMIN_ID = 514411336
MEDIA_FOLDER = 'media'


async def even_id_filter(message: Message, **kwargs):
    return message.from_user.id % 2 == 0


# class NumberFilter(Filter):
#     def __init__(self, my_text: str = 'even') -> None:
#         self.my_text = my_text
#
#     async def __call__(self, message: Message) -> bool:
#         if self.my_text == 'even' and message.from_user.id % 2 == 0:
#             return True
#         else:
#             return False


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = User.get(message.from_user.id)
    if user is None:
        await message.answer("User not found")
        user_data = message.from_user.model_dump(include={'id', 'first_name', 'last_name', 'username'})
        user = User.create(**user_data)
        await message.answer(f"Created user {user.id}")
    else:
        await message.answer(f"User {user.id} already exists")


@dp.message(Command('drop-all'))
async def command_drop_all_handler(message: Message) -> None:
    db.drop_all()
    await message.answer(f"Dropped all tables")


@dp.message(Command("id"))
async def command_start_handler(message: Message) -> None:
    await message.answer(str(message.from_user.id))


@dp.message(F.content_type.in_({ContentType.PHOTO}))
async def command_photo_content_type_handler(message: Message, bot: Bot) -> None:
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)

    folder_name = file.file_path.split('/')[0]
    os.makedirs(MEDIA_FOLDER + "/" + folder_name, exist_ok=True)
    # media/photos/file_5.jpg
    await bot.download_file(file.file_path, MEDIA_FOLDER + "/" + file.file_path)
    await message.answer(f"Downloaded photo {file.file_path}")


# @dp.message(even_id_filter)
# async def command_start_handler(message: Message, bot: Bot) -> None:
#     await message.answer("Button bosing")
#
# @dp.message(lambda msg: msg.from_user.id % 2 == 0)
# async def command_start_handler(message: Message, bot: Bot) -> None:
#     await message.answer("Button bosing")


async def startup(bot: Bot) -> None:
    db.create_all()
    # await bot.set_my_name('P34 ning Telegram boti')
    await bot.send_message(ADMIN_ID, "Bot ishga tushdi")
    # await bot.set_chat_photo(8329233522, FSInputFile('image.jpeg'))
    list_commands = [
        BotCommand(command='start', description='Botni ishga tushirish'),
        BotCommand(command='id', description='Idni korish'),
    ]
    await bot.set_my_commands(
        [BotCommand(command='drop_all', description='drop all tables')],
        scope=BotCommandScopeChat(chat_id=ADMIN_ID)
    )
    await bot.set_my_commands(
        list_commands,
        scope=BotCommandScopeAllPrivateChats()
    )


async def shutdown(bot: Bot) -> None:
    print('bot toxtadi')


async def main() -> None:
    bot = Bot("8329233522:AAGJWMJuYZPe2z1Qj-siN5glrk9bYu60r4U", default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.shutdown.register(shutdown)
    dp.startup.register(startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

"""

@pdp_p34_bot


"""
