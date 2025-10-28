from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from passlib.hash import argon2          # ✅ use argon2
from models import User
from repositories import UserRepository

JWT_ALG = "HS256"


class AuthService:
    def __init__(self, user_repo: UserRepository, jwt_secret: str) -> None:
        self.user_repo = user_repo
        self.jwt_secret = jwt_secret

    # ✅ argon2, not bcrypt
    def hash_password(self, raw: str) -> str:
        return argon2.hash(raw)

    def verify_password(self, raw: str, hashed: str) -> bool:
        return argon2.verify(raw, hashed)

    def create_token(self, user: User, remember: bool = False) -> str:
        exp_days = 30 if remember else 1
        now = datetime.now(tz=timezone.utc)
        payload = {
            "sub": user.id,
            "role": user.role,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(days=exp_days)).timestamp()),
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=JWT_ALG)

    def parse_token(self, token: str) -> dict:
        return jwt.decode(token, self.jwt_secret, algorithms=[JWT_ALG])


class UserService:
    def __init__(self, user_repo: UserRepository, auth: AuthService) -> None:
        self.user_repo = user_repo
        self.auth = auth

    def register(self, email: str, username: str, password: str) -> User:
        user = User.new(
            email=email,
            username=username,
            password_hash=self.auth.hash_password(password),
        )
        self.user_repo.add(user)
        return user

    def login(self, login: str, password: str) -> Optional[User]:
        u = self.user_repo.get_by_login(login)
        if not u:
            return None
        if not self.auth.verify_password(password, u.password_hash):
            return None
        return u

