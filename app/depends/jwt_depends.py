import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import Depends,status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.config import settings
from app.core.error.error_types import ErrorType
from app.core.error.message_codes import MessageCode
from app.core.middleware.exception_middleware import AppException
from app.database.postgresql.session import get_postgres_db
from app.database.mysql.session import get_mysql_db
from app.models.postgresql.users import TblUser
from app.models.mysql.admin import TblAdmin


security = HTTPBearer()


# ============================================================
# JWT SERVICE
# ============================================================

class JWTService:

    def __init__(self):

        self.redis = Redis(
            host=settings.REDIS_DB_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASS,
            decode_responses=True,
        )

        self.private_key = settings.APP_JWT_PRIVATE_KEY.replace("\\n", "\n")
        self.public_key = settings.APP_JWT_PUBLIC_KEY.replace("\\n", "\n")

        self.issuer = settings.PROJECT_NAME
        self.audience = "api"

        self.access_exp = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_exp = settings.REFRESH_TOKEN_EXPIRE_MINUTES


    # ================= INTERNAL =================

    def _now(self):
        return datetime.now(timezone.utc)

    def _generate_payload(
        self,
        user_id: int,
        role: str,
        expire_minutes: int,
        token_type: str,
    ) -> dict[str, Any]:

        jti = uuid.uuid4().hex
        expire = self._now() + timedelta(minutes=expire_minutes)

        return {
            "sub": str(user_id),  # Always string
            "role": role,
            "type": token_type,
            "iss": self.issuer,
            "aud": self.audience,
            "iat": int(self._now().timestamp()),
            "exp": int(expire.timestamp()),
            "jti": jti,
        }


    # ================= CREATE ACCESS =================

    async def create_access_token(self, user_id: int, role: str) -> str:

        payload = self._generate_payload(
            user_id=user_id,
            role=role,
            expire_minutes=self.access_exp,
            token_type="access",
        )

        token = jwt.encode(payload, self.private_key, algorithm="RS256")

        await self.redis.setex(
            f"access:{payload['jti']}",
            self.access_exp * 60,
            payload["sub"],
        )

        return token


    # ================= CREATE REFRESH =================

    async def create_refresh_token(self, user_id: int, role: str) -> str:

        payload = self._generate_payload(
            user_id=user_id,
            role=role,
            expire_minutes=self.refresh_exp,
            token_type="refresh",
        )

        token = jwt.encode(payload, self.private_key, algorithm="RS256")

        await self.redis.setex(
            f"refresh:{payload['jti']}",
            self.refresh_exp * 60,
            payload["sub"],
        )

        return token


    # ================= VERIFY =================

    async def verify_token(self, token: str, expected_type: str):

        try:
            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=["RS256"],
                issuer=self.issuer,
                audience=self.audience,
            )

        except jwt.ExpiredSignatureError:
            raise AppException(
                ErrorType.AUTH_401_TOKEN_EXPIRED,
                MessageCode.TOKEN_EXPIRED,status.HTTP_401_UNAUTHORIZED
            )

        except jwt.InvalidTokenError:
            raise AppException(
                ErrorType.AUTH_401_INVALID_TOKEN,
                MessageCode.INVALID_CREDENTIALS,status.HTTP_401_UNAUTHORIZED
            )

        # Check token type
        if payload.get("type") != expected_type:
            raise AppException(
                ErrorType.AUTH_401_INVALID_TOKEN,
                MessageCode.INVALID_CREDENTIALS,status.HTTP_401_UNAUTHORIZED
            )

        # Check Redis session
        redis_key = f"{expected_type}:{payload['jti']}"
        stored = await self.redis.get(redis_key)

        if not stored:
            raise AppException(
                ErrorType.AUTH_401_SESSION_INVALID,
                MessageCode.UNAUTHORIZED_ACCESS,status.HTTP_401_UNAUTHORIZED
            )

        return payload


    # ================= LOGOUT =================

    async def revoke_user(self, user_id: int):

        keys = await self.redis.keys("*")

        for key in keys:
            value = await self.redis.get(key)
            if value == str(user_id):
                await self.redis.delete(key)


jwt_service = JWTService()


# ============================================================
# USER DEPENDENCY (PostgreSQL)
# ============================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_postgres_db),
):

    token = credentials.credentials

    payload = await jwt_service.verify_token(token, "access")

    user_id = int(payload["sub"])
    user = await TblUser.get_by_id(db, user_id)

    if not user:
        raise AppException(
            ErrorType.RES_404_USER_NOT_FOUND,
            MessageCode.UNAUTHORIZED_ACCESS,status.HTTP_401_UNAUTHORIZED
        )

    return user


# ============================================================
# ADMIN DEPENDENCY (MySQL)
# ============================================================

async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_mysql_db),
):

    token = credentials.credentials

    payload = await jwt_service.verify_token(token, "access")

    admin_id = int(payload["sub"])
    admin = await TblAdmin.get_by_id(db, admin_id)

    if not admin:
        raise AppException(
            ErrorType.RES_404_USER_NOT_FOUND,
            MessageCode.UNAUTHORIZED_ACCESS,status.HTTP_401_UNAUTHORIZED
        )

    return admin