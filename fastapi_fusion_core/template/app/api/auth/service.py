from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.auth.schema import (
    AdminRegisterRequest,
    ProfileResponse,
    TokenData,
    UserRegisterRequest,
)
from app.core.error.error_types import ErrorType
from app.core.error.message_codes import MessageCode
from app.core.response.response_builder import ResponseBuilder
from app.depends.jwt_depends import jwt_service
from app.models.mysql.admin import AdminBaseModel as MyUserBase
from app.models.mysql.admin import TblAdmin
from app.models.postgresql.users import TblUser
from app.models.postgresql.users import UsersBaseModel as PgUserBase
from app.utils.crypto_utils import hash_password, verify_password


class AuthService:
    # ======================================
    # USER REGISTER → PostgreSQL
    # ======================================
    @staticmethod
    async def register_user(data: UserRegisterRequest, db: AsyncSession, lang: str):

        existing = await TblUser.get_by_username(db, data.username)
        if existing:
            return ResponseBuilder.build(
                ErrorType.VAL_400_VALIDATION_ERROR,
                MessageCode.USERNAME_EXISTS,
                lang,
            )

        user_data = PgUserBase(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            role="1",
        )

        await TblUser.create(db, user_data)
        await db.commit()
        return ResponseBuilder.build(
            ErrorType.SUC_201_RESOURCE_CREATED,
            MessageCode.RESOURCE_CREATED,
            lang,
        )

    # ======================================
    # ADMIN REGISTER → MySQL
    # ======================================
    @staticmethod
    async def register_admin(data: AdminRegisterRequest, db: Session, lang: str):

        existing = await TblAdmin.get_by_username(db, data.username)
        if existing:
            return ResponseBuilder.build(
                ErrorType.CON_409_CONFLICT_ERROR,
                MessageCode.USERNAME_EXISTS,
                lang,
            )

        admin_data = MyUserBase(
            username=data.username,
            email=data.email,
            role="admin",
            hashed_password=hash_password(data.password),
        )

        await TblAdmin.create(db, admin_data)
        db.commit()

        return ResponseBuilder.build(
            ErrorType.SUC_201_RESOURCE_CREATED,
            MessageCode.RESOURCE_CREATED,
            lang,
        )

    # ======================================
    # USER LOGIN (Postgres)
    # ======================================
    @staticmethod
    async def user_login(data, db: AsyncSession, lang: str):

        user = await TblUser.get_by_username(db, data.username)

        if not user or not verify_password(data.password, user.hashed_password):
            return ResponseBuilder.build(
                ErrorType.AUTH_401_INVALID_CREDENTIALS,
                MessageCode.INVALID_CREDENTIALS,
                lang,
            )

        access_token = await jwt_service.create_access_token(
            user_id=user.id, role=user.role
        )
        refresh_token = await jwt_service.create_refresh_token(
            user_id=user.id, role=user.role
        )

        return ResponseBuilder.build(
            ErrorType.SUC_200_SUCCESS,
            MessageCode.LOGIN_SUCCESS,
            lang,
            data=TokenData(
                access_token=str(access_token), refresh_token=str(refresh_token)
            ),
        )

    # ======================================
    # ADMIN LOGIN (MySQL)
    # ======================================
    @staticmethod
    async def admin_login(data, db: Session, lang: str):

        admin = await TblAdmin.get_by_username(db, data.username)

        if not admin or not verify_password(data.password, admin.hashed_password):
            return ResponseBuilder.build(
                ErrorType.AUTH_401_INVALID_CREDENTIALS,
                MessageCode.INVALID_CREDENTIALS,
                lang,
            )

        access_token = await jwt_service.create_access_token(
            user_id=admin.id, role=admin.role
        )
        refresh_token = await jwt_service.create_refresh_token(
            user_id=admin.id, role=admin.role
        )

        return ResponseBuilder.build(
            ErrorType.SUC_200_SUCCESS,
            MessageCode.LOGIN_SUCCESS,
            lang,
            data=TokenData(
                access_token=str(access_token), refresh_token=str(refresh_token)
            ),
        )

    # ===============================
    # USER PROFILE
    # ===============================
    @staticmethod
    async def user_profile(user, lang: str):

        return ResponseBuilder.build(
            ErrorType.SUC_200_SUCCESS,
            MessageCode.DATA_FETCHED,
            lang,
            data=ProfileResponse.model_validate(user),
        )

    # ===============================
    # ADMIN PROFILE
    # ===============================
    @staticmethod
    async def admin_profile(admin, lang: str):

        return ResponseBuilder.build(
            ErrorType.SUC_200_SUCCESS,
            MessageCode.DATA_FETCHED,
            lang,
            data=ProfileResponse.model_validate(admin),
        )
