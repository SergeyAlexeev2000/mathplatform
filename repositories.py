from typing import Optional, Dict
from models import User


class UserRepository:
    def __init__(self) -> None:
        # simple in-memory store
        self._by_id: Dict[str, User] = {}
        self._by_email: Dict[str, User] = {}
        self._by_username: Dict[str, User] = {}

    # internal save
    def _save(self, user: User) -> None:
        self._by_id[user.id] = user
        self._by_email[user.email.lower()] = user
        self._by_username[user.username.lower()] = user

    # public API
    def add(self, user: User) -> None:
        if self.get_by_email(user.email) is not None:
            raise ValueError("email_exists")
        if self.get_by_username(user.username) is not None:
            raise ValueError("username_exists")
        self._save(user)

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._by_id.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return self._by_email.get(email.lower())

    def get_by_username(self, username: str) -> Optional[User]:
        return self._by_username.get(username.lower())

    # optional helper used during seeding
    def seed_host(self, user: User) -> None:
        self._save(user)
