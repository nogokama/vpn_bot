from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

apply_button = InlineKeyboardButton(text="Approve", callback_data="client_approvement")
reject_button = InlineKeyboardButton(text="Reject", callback_data="client_rejection")

keyboard = InlineKeyboardMarkup(one_time_keyboard=True).add(apply_button).add(reject_button)
