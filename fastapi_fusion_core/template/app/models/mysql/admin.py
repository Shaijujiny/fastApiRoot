from pydantic import Field
from sqlalchemy import Boolean, Integer, String, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.core.response.base_schema import CustomModel
from app.database.mysql.base import MysqlBase

# ==============================
# Pydantic Base Model
# ==============================


class AdminBaseModel(CustomModel):
    id: int | None = Field(default=None)
    username: str | None = Field(default=None)
    role: str | None = Field(default=None)
    email: str | None = Field(default=None)
    hashed_password: str | None = Field(default=None)
    is_active: bool = True


# ==============================
# MySQL Admin Model
# ==============================


class TblAdmin(MysqlBase):
    __tablename__ = "admins"

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
    async def create(cls, db: Session, user: AdminBaseModel):
        new_user = cls(**user.model_dump(exclude_unset=True))
        db.add(new_user)
        db.flush()
        return new_user

    # ----------------------------------
    # GET BY ID
    # ----------------------------------
    @classmethod
    async def get_by_id(cls, db: Session, user_id: int):
        result = db.execute(select(cls).where(cls.id == user_id))
        return result.scalar_one_or_none()

    # ----------------------------------
    # GET BY USERNAME
    # ----------------------------------
    @classmethod
    async def get_by_username(cls, db: Session, username: str):
        result = db.execute(select(cls).where(cls.username == username))
        return result.scalar_one_or_none()

    # ----------------------------------
    # UPDATE
    # ----------------------------------
    @classmethod
    async def update(cls, db: Session, user: AdminBaseModel):
        if not user.id:
            return None
        existing_user = await cls.get_by_id(db, user.id)
        if not existing_user:
            return None

        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(existing_user, key, value)

        db.flush()
        return existing_user
