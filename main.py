import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats

from bot.handlers import admin_router, user_router
from core.config import settings
from models import User
from models.base import db

dp = Dispatcher()


async def startup(bot: Bot) -> None:
    db.create_all()
    # await bot.send_message(ADMIN_ID, "Bot ishga tushdi")

    admin_list: list[User] = User.filter(type=User.Type.ADMIN.name)
    # admin commands
    for admin in admin_list:
        await bot.set_my_commands(
            [
                BotCommand(command='start', description='Botni ishga tushirish'),
                BotCommand(command='channel', description='Kanal edit qilish'),
                # BotCommand(command='users_count', description='users count'),
                # BotCommand(command='category', description='category larni korish'),
                BotCommand(command='drop_all', description='drop all tables'),
            ],
            scope=BotCommandScopeChat(chat_id=admin.id),
        )

    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Botni ishga tushirish'),
            BotCommand(command='id', description='Idni korish'),
        ],
        scope=BotCommandScopeAllPrivateChats()
    )


async def shutdown(bot: Bot) -> None:
    print('bot toxtadi')


async def main() -> None:
    bot = Bot(settings.TELEGRAM_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.shutdown.register(shutdown)
    dp.startup.register(startup)

    dp.include_routers(*[
        admin_router,
        user_router,
    ])
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
