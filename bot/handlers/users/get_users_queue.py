from aiogram import types

from wireguard.loader import vpn_recorder

from bot.loader import dp
from bot.keyboards.inline.approve_new_client import keyboard as reply_keyboard


@dp.message_handler(commands=["get_users_queue"])
async def get_full_users_queue(message: types.Message):  # TODO make for admins only

    await dp.bot.send_message(
        chat_id=message.from_user.id,
        text="\n".join(
            [
                "id: {}, name: {}".format(user.id, user.name)
                for user in list(vpn_recorder.get_queued_users().to_list())
            ]
        ),
    )


@dp.message_handler(commands=["get_last_queue_user"])
async def get_last_user_in_queue(message: types.Message):  # TODO make for admins only
    vpn_recorder.mark_last_user_to_approve()

    await dp.bot.send_message(
        message.from_user.id,
        text="Подтвердите, пожалуйста",
        reply_markup=reply_keyboard,
    )
