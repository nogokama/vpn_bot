from aiogram import types

from bot.loader import dp

from wireguard_utils.loader import vpn_recorder


@dp.callback_query_handler(text_contains='client_approvement')
async def approve_client(call: types.CallbackQuery):
    await vpn_recorder.approve_last_user()
