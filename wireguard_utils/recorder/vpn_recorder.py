import json
import string
import random
import re

import subprocess

from aiogram import types
import wgconfig

from config import config

from wireguard_utils.data.user import User, UsersList, UserRegisterQueue
from wireguard_utils.recorder.db_connector import DbConnector
from wireguard_utils.wg_generator import KeyPair, WgGenerator
from wireguard_utils.wg_generator import outline_generator

from bot.loader import dp as dispatcher
import bot.utils.notify_admins as notify_admins


class VpnRecorder:
    def __init__(self):
        self.wireguard_config = wgconfig.WGConfig("wg0")
        self.wireguard_config.read_file()
        print(json.dumps(self.wireguard_config.peers, indent=4))
        print(json.dumps(self.wireguard_config.interface, indent=4))

        self.users = UsersList()
        self.queue = UserRegisterQueue()
        self.user_to_approve = User()
        self.db_connector = DbConnector(config.db_path)

    def comment_matches(self, comment: str) -> bool:
        return len(comment) < 20 and re.match("[A-Za-z0-9]+", comment)

    def get_server_public_key(self) -> str:
        with open(config.server_public_key_path) as f:
            key = f.read()
        if key[-1] == "\n":
            key = key[:-1]

        return key

    def get_first_user_from_queue(self) -> User:
        return self.db_connector.get_first_user_from_queue()

    def load(self, user_list: UsersList):
        self.users = user_list

    def get_all_records(self, user: types.User) -> str:
        list_of_users = self.db_connector.get_user_records(user.id)
        ans = "\n".join([str(cur_user) for cur_user in list_of_users])
        print(ans)
        return ans

    def insert_client_if_not_exists(self, user: types.User) -> str:
        user_record = User(id=user.id, name=user.full_name, username=user.username)
        self.db_connector.insert_user_if_not_exists(user_record)

    async def put_registration_request_to_queue(
        self, new_user: types.User, comment: str
    ):
        self.insert_client_if_not_exists(new_user)
        await notify_admins.text_notify(dispatcher, "Есть новые заявки на VPN")
        user_record = User(id=new_user.id, comment=comment)
        self.db_connector.insert_into_queue(user_record)

    def remove_user_from_queue(self, user_record: User):
        self.db_connector.remove_from_queue(user_record)

    async def register_new_user(self, new_user: User):
        outline_key = outline_generator.generate_new_key(
            f"{new_user.id}_{new_user.name}_{new_user.comment}"
        )

        user_record = User(
            id=new_user.id,
            name=new_user.name,
            outline_key=outline_key,
            comment=new_user.comment,
        )

        print(str(user_record))

        self.db_connector.insert_new_key(user_record)
        self.db_connector.remove_from_queue(user_record)

        self.queue.add_user(user_record)

        await self.send_user_key(user_record)

    def modify_server_config_file(self, key_pair: KeyPair):
        cnt = self.db_connector.get_all_records_count()

        self.wireguard_config.add_peer(key_pair.public_key)
        self.wireguard_config.add_attr(
            key_pair.public_key, "AllowedIPs", "10.0.0.{}/32".format(cnt - 1)
        )
        self.wireguard_config.write_file()

    async def send_user_key(self, user_info: User):
        message = f"Here is your new outline key for Outline App. Use it for one device only: <code>{user_info.outline_key}</code>"
        await dispatcher.bot.send_message(
            user_info.id, text=message, parse_mode=types.ParseMode.HTML
        )

    def restart_vpn_server(self):
        subprocess.run(["systemctl", "restart", "wg-quick@wg0"])
        print("vpn server restarted!")

    async def approve_last_user(self):
        await dispatcher.bot.send_message(
            self.user_to_approve.id, "Поздравляю, вас подтвердили!"
        )
