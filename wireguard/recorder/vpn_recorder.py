from aiogram import types

from wireguard.data.user import User, UsersList, UserRegisterQueue

from bot.loader import dp as dispatcher
import bot.utils.notify_admins as notify_admins


class VpnRecorder:
    def __init__(self):
        self.users = UsersList()
        self.queue = UserRegisterQueue()
        self.user_to_approve = User()

    def load(self, user_list: UsersList):
        self.users = user_list

    async def register_new_user(self, new_user: types.User):
        user_record = User(new_user.id, new_user.full_name)
        self.queue.add_user(user_record)
        await notify_admins.text_notify(dispatcher, "Есть новые заявки на VPN")

    def get_queued_users(self) -> UserRegisterQueue:  # TODO list of users
        return self.queue

    def mark_last_user_to_approve(self):
        self.user_to_approve = self.queue.get_last_user()
        pass

    async def approve_last_user(self):
        await dispatcher.bot.send_message(
            self.user_to_approve.id, "Поздравляю, вас подтвердили!"
        )
