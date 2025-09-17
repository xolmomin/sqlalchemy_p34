from aiogram import BaseMiddleware
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models import User, Channel


class JoinChannelRequiredMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.channel_list = []
        for channel in Channel.get_all():
            self.channel_list.append(channel.chat_id)

    async def __call__(self, handler, event: Message, data):
        user = User.get(event.from_user.id)
        if user and user.is_admin:
            return await handler(event, data)

        ikm = InlineKeyboardBuilder()
        for channel_id in self.channel_list:
            member = await event.bot.get_chat_member(channel_id, event.from_user.id)
            if member.status not in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
                channel = await event.bot.get_chat(channel_id)
                ikm.row(InlineKeyboardButton(text=channel.full_name, url=channel.invite_link))

        ikm.row(InlineKeyboardButton(text="Azo bo'ldim ✅", callback_data='joined_channels'))
        await event.answer('Kanalda azo boling', reply_markup=ikm.as_markup())
        return None
