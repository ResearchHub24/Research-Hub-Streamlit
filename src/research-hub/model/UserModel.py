import time
from dataclasses import dataclass
from enum import Enum


class UserType(Enum):
    STUDENTS = "STUDENTS"
    PROFESSORS = "PROFESSORS"


@dataclass
class UserModel:
    uid: str
    email: str
    password: str
    name: str
    photoUrl: str = None
    userType: str = UserType.STUDENTS.name
    created: float = time.time()
    links: str = ""
    verified: bool = False
