from dataclasses import dataclass
from enum import Enum
import uuid

class Role(str, Enum):
    HOST = "HOST"
    ADMIN = "ADMIN"
    INSTRUCTOR = "INSTRUCTOR"
    STUDENT = "STUDENT"
    BANNED = "BANNED"

@dataclass
class User:
    id: str
    email: str
    username: str
    password_hash: str
    role: Role = Role.STUDENT
    is_verified: bool = False

    @staticmethod
    def new(email: str, username: str, password_hash: str, role: Role = Role.STUDENT) -> "User":
        return User(
            id=str(uuid.uuid4()),
            email=email,
            username=username,
            password_hash=password_hash,
            role=role,
        )

