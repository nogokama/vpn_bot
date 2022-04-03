import logging

from aiogram import Dispatcher, types

from bot.data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)


async def text_notify(dp: Dispatcher, notification_text: str):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, text=notification_text)
        except Exception as err:
            logging.exception(err)


async def send_incorrect_comment(message: types.Message):
    await message.reply('incorrect comment string')
