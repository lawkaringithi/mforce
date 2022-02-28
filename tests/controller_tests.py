import os
from unittest import TestCase

from common import User
from controllers import CSVController, SQLiteController, UserObj


class TestCsvController(TestCase):
    def setUp(self) -> None:
        self.csv_controller = CSVController()

    def tearDown(self) -> None:
        # delete csv data file
        try:
            os.remove(self.csv_controller.csv_file_name)
        except FileNotFoundError:
            pass

    def test_user_creation(self) -> None:
        new_user: User = User(name=f"John Doe", age=94)
        self.csv_controller.create(new_user)
        fetched_user: UserObj | None = self.csv_controller.get(1)

        assert fetched_user is not None
        assert fetched_user.id == 1
        assert fetched_user.name == new_user.name
        assert fetched_user.age == new_user.age


class TestSQLiteController(TestCase):
    def setUp(self) -> None:
        self.sqlite_controller = SQLiteController()

    def tearDown(self) -> None:
        # delete sqlite database file
        try:
            os.remove(self.sqlite_controller.db_file)
        except FileNotFoundError:
            pass

    def test_user_creation(self) -> None:
        new_user: User = User(name=f"Jane Doe", age=75)
        self.sqlite_controller.create(new_user)
        fetched_user: UserObj | None = self.sqlite_controller.get(1)

        assert fetched_user is not None
        assert fetched_user.id == 1
        assert fetched_user.name == new_user.name
        assert fetched_user.age == new_user.age
