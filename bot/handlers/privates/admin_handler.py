from aiogram import Router

from bot.filters import IsAdminFilter

admin_router = Router()
admin_router.message.filter(IsAdminFilter())
