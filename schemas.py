from pydantic import BaseModel, EmailStr, Field

class RegisterIn(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=40)
    password: str = Field(min_length=6, max_length=128)

class RegisterOut(BaseModel):
    message: str

class LoginIn(BaseModel):
    login: str         # email or username
    password: str
    remember: bool = False

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MeOut(BaseModel):
    id: str
    email: EmailStr
    username: str
    role: str
    is_verified: bool

class VerifyOut(BaseModel):
    message: str
