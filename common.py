from dataclasses import dataclass
from typing import NamedTuple


@dataclass(frozen=True)
class User:
    """
    User class based on dictionary
    """

    name: str
    age: int
    id: int = 0


class UserT(NamedTuple):
    """
    User class based on tuple
    Preferred way of writing UserT = namedtuple("UserT", "id, name, age")
    """

    name: str
    age: int
    id: int = 0
