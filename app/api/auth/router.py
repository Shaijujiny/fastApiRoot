from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.database.mysql.session import get_mysql_db

from app.database.postgresql.session import get_postgres_db
from app.depends.jwt_depends import get_current_admin, get_current_user
from app.depends.language_depends import get_language

from .service import AuthService
from .schema import (
    UserRegisterRequest,
    AdminRegisterRequest,
    LoginRequest,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ======================================
# USER REGISTER → PostgreSQL
# ======================================
@router.post("/user/register")
async def register_user(
    data: UserRegisterRequest,
    db: AsyncSession = Depends(get_postgres_db),
    lang: str = Depends(get_language),
):
    return await AuthService.register_user(data, db, lang)


# ======================================
# ADMIN REGISTER → MySQL
# ======================================
@router.post("/admin/register")
async def register_admin(
    data: AdminRegisterRequest,
    db: Session = Depends(get_mysql_db),
    lang: str = Depends(get_language),
):
    return await AuthService.register_admin(data, db, lang)


# ======================================
# USER LOGIN
# ======================================
@router.post("/user/login")
async def user_login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_postgres_db),
    lang: str = Depends(get_language),
):
    return await AuthService.user_login(data, db, lang)


# ======================================
# ADMIN LOGIN
# ======================================
@router.post("/admin/login")
async def admin_login(
    data: LoginRequest,
    db: Session = Depends(get_mysql_db),
    lang: str = Depends(get_language),
):
    return await AuthService.admin_login(data, db, lang)


# ======================================
# USER PROFILE
# ======================================
@router.get("/user/profile")
async def user_profile(
    current_user = Depends(get_current_user),
    lang: str = Depends(get_language),
):
    return await AuthService.user_profile(current_user, lang)


# ======================================
# ADMIN PROFILE
# ======================================
@router.get("/admin/profile")
async def admin_profile(
    current_admin = Depends(get_current_admin),
    lang: str = Depends(get_language),
):
    return await AuthService.admin_profile(current_admin, lang)