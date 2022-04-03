from aiogram import types

from bot.loader import dp

from wireguard_utils.loader import vpn_recorder


@dp.callback_query_handler(text_contains="client_approvement")
async def approve_client(call: types.CallbackQuery):
    user_to_apply = vpn_recorder.get_first_user_from_queue()
    await vpn_recorder.register_new_user(user_to_apply)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()


@dp.callback_query_handler(text_contains="client_rejection")
async def approve_client(call: types.CallbackQuery):
    user_to_apply = vpn_recorder.get_first_user_from_queue()
    vpn_recorder.remove_user_from_queue(user_to_apply)

    await dp.bot.send_message(
        user_to_apply.id,
        text='К сожалению ваш запрос на {} отклонили'.format(user_to_apply.comment),
    )
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
