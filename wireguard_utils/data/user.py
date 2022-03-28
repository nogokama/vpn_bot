import random


class UsersList:
    def __init__(self):
        self.users = list()


class User:
    def __init__(self, id=-1, name="default name"):
        self.id = id
        self.name = name

    @staticmethod
    def construct_user():
        return User()

    def __hash__(self):
        return self.id


class UserRegisterQueue:
    def __init__(self):
        self.queue = set()

    def add_user(self, user: User):
        self.queue.add(user)

    def to_list(self) -> list:  # FIXME refactor
        return list(self.queue)

    def get_last_user(self) -> User:
        return random.choice(list(self.queue))
