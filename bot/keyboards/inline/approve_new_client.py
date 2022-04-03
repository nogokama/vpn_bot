from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button = InlineKeyboardButton(text="Approve", callback_data="client_approvement")
keyboard = InlineKeyboardMarkup().add(button)


