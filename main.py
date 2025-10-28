from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware  # ← correct import
from typing import Optional

from models import User, Role
from schemas import (
    RegisterIn, RegisterOut,
    LoginIn, TokenOut,
    MeOut, VerifyOut,
)
from repositories import UserRepository
from services import AuthService, UserService

# --- wiring ---
user_repo = UserRepository()
auth = AuthService(user_repo=user_repo, jwt_secret="CHANGE_ME_SUPER_SECRET")
users = UserService(user_repo=user_repo, auth=auth)

# seed HOST (super-admin who doesn't need to register)
host = User.new(
    email="host@highestmath.example",
    username="Host",
    password_hash=auth.hash_password("host-does-not-login"),
    role=Role.HOST,
)
host.is_verified = True
user_repo.add(host)


app = FastAPI(title="Highest Math Moodle API", version="0.1")
app.add_middleware(
    CORSMiddleware,                      # ← not CORSMMiddleware
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def bearer_token(authorization: Optional[str] = Header(default=None)) -> Optional[str]:
    if not authorization:
        return None
    if not authorization.lower().startswith("bearer "):
        return None
    return authorization.split(" ", 1)[1]

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/auth/register", response_model=RegisterOut)
def register(payload: RegisterIn):
    try:
        users.register(payload.email, payload.username, payload.password)
        return {"message": "verification passed successfully"}
    except ValueError as e:
        key = str(e)
        if key == "email_exists":
            raise HTTPException(status_code=400, detail="this email already exists")
        if key == "username_exists":
            raise HTTPException(status_code=400, detail="this username already exists")
        raise

@app.post("/auth/login", response_model=TokenOut)
def login(payload: LoginIn):
    u = users.login(payload.login, payload.password)
    if not u:
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = auth.create_token(u, remember=payload.remember)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/auth/me", response_model=MeOut)
def me(token: Optional[str] = Depends(bearer_token)):
    if not token:
        raise HTTPException(status_code=401, detail="missing token")
    try:
        data = auth.parse_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")
    sub = data.get("sub")
    u = user_repo._by_id.get(sub)
    if not u:
        raise HTTPException(status_code=401, detail="user not found")
    return MeOut(id=u.id, email=u.email, username=u.username, role=u.role, is_verified=u.is_verified)

@app.post("/auth/verify", response_model=VerifyOut)
def verify():
    return {"message": "verification passed successfully"}
