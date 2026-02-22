import uuid

from pydantic import Field
from sqlalchemy import Boolean, Integer, String, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.core.response.base_schema import CustomModel
from app.database.postgresql.base import PostgresBase

# ==============================
# Pydantic Base Model
# ==============================


class UsersBaseModel(CustomModel):
    id: int | None = Field(default=None)
    username: str | None = Field(default=None)
    email: str | None = Field(default=None)
    role: str | None = Field(default=None)
    hashed_password: str | None = Field(default=None)
    is_active: bool = True


# ==============================
# PostgreSQL User Model
# ==============================


class TblUser(PostgresBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ----------------------------------
    # CREATE
    # ----------------------------------
    @classmethod
    async def create(cls, db: AsyncSession, user: UsersBaseModel):
        new_user = cls(**user.model_dump(exclude_unset=True))
        db.add(new_user)
        return new_user

    # ----------------------------------
    # GET BY ID
    # ----------------------------------
    @classmethod
    async def get_by_id(cls, db: AsyncSession, user_id: int):
        result = await db.execute(select(cls).where(cls.id == user_id))
        return result.scalar_one_or_none()

    # ----------------------------------
    # GET BY USERNAME
    # ----------------------------------
    @classmethod
    async def get_by_username(cls, db: AsyncSession, username: str):
        result = await db.execute(select(cls).where(cls.username == username))
        return result.scalar_one_or_none()

    # ----------------------------------
    # UPDATE
    # ----------------------------------
    @classmethod
    async def update(cls, db: AsyncSession, user: UsersBaseModel):
        if not user.id:
            return None
        existing_user = await cls.get_by_id(db, user.id)
        if not existing_user:
            return None

        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(existing_user, key, value)

        await db.flush()
        return existing_user
