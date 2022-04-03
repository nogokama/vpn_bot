import random


class UsersList:
    def __init__(self):
        self.users = list()


class User:
    def __init__(self, id=-1, name="default name", public_key="", private_key="", comment=""):
        self.id = id
        self.name = name
        self.public_key = str(public_key)
        self.private_key = str(private_key)
        self.comment = comment

    @staticmethod
    def construct_user():
        return User()

    def __hash__(self):
        return self.id

    def __repr__(self):
        return "id: {}, name: {}, public_key: {}, private_key: {}, comment: {}".format(
            self.id, self.name, self.public_key, self.private_key, self.comment
        )

    __str__ = __repr__


class UserRegisterQueue:
    def __init__(self):
        self.queue = set()

    def add_user(self, user: User):
        self.queue.add(user)

    def to_list(self) -> list:  # FIXME refactor
        return list(self.queue)

    def get_last_user(self) -> User:
        return random.choice(list(self.queue))
