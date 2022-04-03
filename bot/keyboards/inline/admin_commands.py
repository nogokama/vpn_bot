from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


buttons = (
    InlineKeyboardButton(text="Get queued clients", callback_data="get_queued_clients"),
        InlineKeyboardButton(text="Approve client", callback_data="approve_client"),
            InlineKeyboardButton(text="Delete client", callback_data="delete_client")
)

def _construct_admin_keyboard():
    result = InlineKeyboardMarkup()
    for button in buttons:
        result = result.add(button)
    return result 


keyboard = _construct_admin_keyboard()
