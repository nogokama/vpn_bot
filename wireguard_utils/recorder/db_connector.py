import sqlite3

from wireguard_utils.data.user import User


class DbConnector:
    def __init__(self, db_path):
        self.con = sqlite3.connect(db_path)
        self.cursor = self.con.cursor()
        self.on_startup()

    def on_startup(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Clients (
                    Id int PRIMARY KEY, 
                    Name varchar(255)
                )
            """
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Keys (
                    Id int,
                    PublicKey varchar(255) PRIMARY KEY,
                    Comment varchar (255)
                )
            """
        )

    def insert_new_key(self, user: User):
        user_info_count = len(
            list(
                self.cursor.execute(
                    """
                        select * from Clients where Id=:userId
                    """,
                    {"userId": user.id},
                )
            )
        )

        print('user_info_count: {}'.format(user_info_count))

        if user_info_count == 0:
            self.cursor.execute(
                """
                    insert into Clients (Id, Name) values (:id, :name)
                """,
                {"id": user.id, "name": user.name},
            )

        self.cursor.execute(
            """
                insert into Keys (Id, PublicKey, Comment) values (:id, :public_key, :comment) 
            """,
            {"id": user.id, "public_key": user.key, "comment": user.comment},
        )

        self.con.commit()

    def get_user_records(self, id) -> list:

        data = self.cursor.execute(
            """
            select (Clients.Id, Clients.Name, Keys.PublicKey, Keys.Comment) 
            from 
            Keys left join Clients 
            on Keys.Id=Clients.Id
            where
            Clients.Id=:target_id
            """,
            {"target_id": id},
        )

        return [User(*info) for info in data]
