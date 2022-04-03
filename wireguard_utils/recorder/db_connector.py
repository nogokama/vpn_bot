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
                    PrivateKey varchar(255),
                    Comment varchar (255)
                )
            """
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Queue (
                    Id int,
                    Comment varchar (255),
                    Timestamp int
                )
            """
        )

    def insert_into_queue(self, user: User):
        self.cursor.execute(
            """
            insert into Queue (Id, Comment)
            values
            (:id, :comment)
            """,
            {"id": user.id, "comment": user.comment},
        )
        self.con.commit()

    def get_all_queued_requests(self) -> list:
        data = self.cursor.execute(
            """
            select (Id, Comment) from Queued
            """
        )
        return [User(id=cur[0], comment=cur[1]) for cur in data]

    def get_user_queued_requests(self, user: User) -> list:
        data = self.cursor.execute(
            """
            select (Id, Comment) from Queued 
            where Queued.Id = :id
            """,
            {"id": user.id},
        )
        return [User(id=cur[0], comment=cur[1]) for cur in data]

    def get_first_user_from_queue(self) -> User:
        data = self.cursor.execute(
            """
            select Queue.Id, Clients.Name, Queue.Comment 
            from Queue left join Clients on Queue.Id=Clients.Id
            order by Queue.Id, Clients.Name, Queue.Comment ASC
            """
        )
        row = list(data)[0]
        return User(id=row[0], name=row[1], comment=row[2])

    def remove_from_queue(self, user: User):
        self.cursor.execute(
            """
            delete from Queue 
            where Queue.Id = :id and Queue.Comment = :comment
            """,
            {"id": user.id, "comment": user.comment},
        )
        self.con.commit()

    def insert_user_if_not_exists(self, user: User):
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

        print("user_info_count: {}".format(user_info_count))

        if user_info_count == 0:
            self.cursor.execute(
                """
                    insert into Clients (Id, Name) values (:id, :name)
                """,
                {"id": user.id, "name": user.name},
            )
        self.con.commit()

    def insert_new_key(self, user: User):
        self.insert_user_if_not_exists(user)

        self.cursor.execute(
            """
                insert into Keys 
                (Id, PublicKey, PrivateKey, Comment) 
                values 
                (:id, :public_key, :private_key, :comment) 
            """,
            {
                "id": user.id,
                "public_key": user.public_key,
                "private_key": user.private_key,
                "comment": user.comment,
            },
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

    def get_user_records_count(self, id) -> int:
        data = self.cursor.execute(
            """
            select count(*) from Keys
            where 
            Keys.Id = :target_id
            """,
            {"target_id": id},
        )
        return int(list(data)[0][0])

    def get_all_records_count(self) -> int:
        data = self.cursor.execute(
            """
            select count(*) from Keys
            """
        )

        return int(list(data)[0][0])
