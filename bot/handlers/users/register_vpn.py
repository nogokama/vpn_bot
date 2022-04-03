from aiogram import types

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from bot.loader import dp
from bot.utils.notify_admins import send_incorrect_comment
from bot.data.config import ADMINS
from bot.keyboards.inline.approve_new_client import keyboard as approvement_keyboard


from wireguard_utils.loader import vpn_recorder


class RegistrationState(StatesGroup):
    comment = State()


@dp.message_handler(commands=["register"])
async def register_request_command(message: types.Message):
    print(message.from_user.id, message.from_user.full_name)
    await message.reply(
        text="Хорошая попытка, {}! Введите comment (для каждого нового устройства "
        "нужно будет запрашивать новый файлик) Комментарий состоит из латинских букв "
        "и цифр длины не больше 10 ! ".format(message.from_user.first_name)
    )
    await RegistrationState.comment.set()


@dp.message_handler(commands=["get_all_keys"])
async def get_all_keys(message: types.Message):
    await message.reply(text=vpn_recorder.get_all_records(message.from_user))


@dp.message_handler(state=RegistrationState.comment)
async def write_comment_request(message: types.Message, state: FSMContext):
    if vpn_recorder.comment_matches(message.text):
        await vpn_recorder.put_registration_request_to_queue(message.from_user, message.text)
        await state.finish()
    else:
        await send_incorrect_comment(message)


@dp.message_handler(commands=['apply'])
async def apply_or_reject_user(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.reply('Sorry, you are not admin.')
        return

    user_to_approve = vpn_recorder.get_first_user_from_queue()
    await dp.bot.send_message(
        message.from_user.id,
        text='Name: {}\nComment: {}'.format(user_to_approve.name, user_to_approve.comment),
        reply_markup=approvement_keyboard,
    )
