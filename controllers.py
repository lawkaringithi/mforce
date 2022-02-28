import csv
import itertools
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import asdict

from common import User, UserT

# alias to expect either User or UserT
UserObj = User | UserT


class Controller(ABC):
    """
    Base data controller
    """

    @abstractmethod
    def create(self, data: UserObj) -> UserObj:
        pass

    @abstractmethod
    def get(self, obj_id: int) -> UserObj | None:
        pass


class CSVController(Controller):
    """
    Controller to write / read data from csv file
    When initialized all data in the csv file is loaded into memory
    """

    def __init__(self) -> None:
        super(CSVController, self).__init__()
        self.store: dict[int, UserObj] = {}

        """
        initialize local store with csv records
        ignore error if file does not exist, we'll create it during first write
        """
        last_id = 0
        try:
            with open(self.csv_file_name, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    user_id = int(row[0])
                    self.store[user_id] = User(id=user_id, name=row[1], age=int(row[2]))
                    last_id = user_id
        except FileNotFoundError:
            pass

        self.counter = itertools.count(last_id + 1)

    @property
    def csv_file_name(self) -> str:
        return "user_file.csv"

    def create(self, data: UserObj) -> UserObj:
        """
        write to csv file everytime there is a new user
        can be optimised later if necessary
        """
        new_id = next(self.counter)

        user = User(id=new_id, name=data.name, age=data.age)
        self.store[new_id] = user

        with open(self.csv_file_name, "a") as file:
            writer = csv.writer(file)
            writer.writerow([user.id, user.name, user.age])

        return user

    def get(self, obj_id: int) -> UserObj | None:
        """
        returns a records with the given id from the local store
        """
        return self.store.get(obj_id)


class SQLiteController(Controller):
    """
    Controller to write and read data from sqlite
    When initialized, a new sqlite database will be created with an empty user table and each call to
    create or get will establish a new db connection that will be closed on completion of the operation
    """

    def __init__(self) -> None:
        with sqlite3.connect(self.db_file) as connection:
            connection.execute(
                """
                create table if not exists users (
                    id integer primary key autoincrement,
                    name varchar(255),
                    age integer
                );
                """
            )

    @property
    def db_file(self) -> str:
        return "db.sqlite3"

    def create(self, data: UserObj) -> UserObj:
        with sqlite3.connect(self.db_file) as connection:
            cursor = connection.execute(
                "insert into users (name, age) values (?, ?)", (data.name, data.age)
            )
            return User(**{**asdict(data), "id": cursor.lastrowid})

    def get(self, obj_id: int) -> UserObj | None:
        with sqlite3.connect(self.db_file) as connection:
            row = connection.execute(
                "select * from users where id = ?", [obj_id]
            ).fetchone()
            if row:
                user_id, name, age = row
                return User(id=user_id, name=name, age=age)

        return None
