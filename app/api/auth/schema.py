from pydantic import  EmailStr, Field

from app.core.response.base_schema import CustomModel


# =============================
# REGISTER
# =============================

class UserRegisterRequest(CustomModel):
    username: str
    email: EmailStr
    password: str


class AdminRegisterRequest(CustomModel):
    username: str
    email: EmailStr
    password: str


# =============================
# LOGIN
# =============================

class LoginRequest(CustomModel):
    username: str
    password: str


# =============================
# TOKEN RESPONSE
# =============================

class TokenData(CustomModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# =============================
# PROFILE
# =============================

class ProfileResponse(CustomModel):

    id: int | None =Field(default=None)
    username: str | None =Field(default=None)
    email: str | None =Field(default=None)
    role: str | None =Field(default=None)