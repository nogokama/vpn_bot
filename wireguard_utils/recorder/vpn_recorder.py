import json
import string
import random

from aiogram import types
import wgconfig

from config import config

from wireguard_utils.data.user import User, UsersList, UserRegisterQueue
from wireguard_utils.recorder.db_connector import DbConnector

from bot.loader import dp as dispatcher
import bot.utils.notify_admins as notify_admins


class VpnRecorder:
    def __init__(self):
        wc = wgconfig.WGConfig('wg0')
        wc.read_file()
        print(json.dumps(wc.peers, indent=4))
        print(json.dumps(wc.interface, indent=4))

        self.users = UsersList()
        self.queue = UserRegisterQueue()
        self.user_to_approve = User()
        self.db_connector = DbConnector(config.db_path)

    def load(self, user_list: UsersList):
        self.users = user_list

    def get_all_records(self, user: types.User) -> str:
        list_of_users = self.db_connector.get_user_records(user.id)
        ans = '\n'.join([str(cur_user) for cur_user in list_of_users])
        print(ans)
        return ans

    async def register_new_user(self, new_user: types.User):
        user_record = User(
            new_user.id,
            new_user.full_name,
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        )
        self.db_connector.insert_new_key(user_record)
        self.queue.add_user(user_record)
        await notify_admins.text_notify(dispatcher, "Есть новые заявки на VPN")

    def get_queued_users(self) -> UserRegisterQueue:  # TODO list of users
        return self.queue

    def mark_last_user_to_approve(self):
        self.user_to_approve = self.queue.get_last_user()
        pass

    async def approve_last_user(self):
        await dispatcher.bot.send_message(self.user_to_approve.id, "Поздравляю, вас подтвердили!")
