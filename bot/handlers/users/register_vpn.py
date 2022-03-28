from aiogram import types

from bot.loader import dp

from wireguard_utils.loader import vpn_recorder


@dp.message_handler(commands=["register"])
async def register_request_command(message: types.Message):
    await vpn_recorder.register_new_user(message.from_user)
    print(message.from_user.id, message.from_user.full_name)
    await message.reply(
        text="Хорошая попытка, {}! Ваш ответ записан! "
        "Ждите подтверждения администратора".format(message.from_user.first_name)
    )
