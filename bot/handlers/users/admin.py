from aiogram import types

from bot.loader import dp
from bot.data.config import ADMINS
from bot.keyboards.inline.admin_commands import keyboard as admin_keyboard


@dp.message_handler(commands=["admin"])
async def admin_commands(message: types.Message):  # only for admins
    if message.from_user.id not in ADMINS:
        await dp.bot.send_message(message.from_user.id, "Not permited, you are not admin(")
        return

    await dp.bot.send_message(message.from_user.id, "Commands:", reply_markup=admin_keyboard)
