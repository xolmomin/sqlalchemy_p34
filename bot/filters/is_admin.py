from aiogram.filters import Filter
from aiogram.types import Message

from core import settings


class IsAdminFilter(Filter):

    def __init__(self):
        super().__init__()

    async def __call__(self, message: Message):
        return message.from_user.id == settings.ADMIN_LIST
