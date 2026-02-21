"""Async PostgreSQL helper using SQLAlchemy AsyncEngine."""
from __future__ import annotations

import asyncio
from typing import AsyncGenerator, List

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import inspect

from app.config import settings as CONFIG_SETTINGS
from app.database.postgresql.base import PostgresBase



_engine: AsyncEngine | None = None
_session_maker: async_sessionmaker[AsyncSession] | None = None


def get_database_url() -> str:
    user = CONFIG_SETTINGS.POSTGRES_USER
    password = CONFIG_SETTINGS.POSTGRES_PASSWORD
    host = CONFIG_SETTINGS.POSTGRES_HOST or "localhost"
    port = CONFIG_SETTINGS.POSTGRES_PORT or 5432
    db = CONFIG_SETTINGS.POSTGRES_DB or "postgres"

    connection=f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
    print("connection configured successfully : ", connection)
    return connection


def init_engine(echo: bool = False) -> AsyncEngine:
    global _engine, _session_maker

    if _engine is None:
        _engine = create_async_engine(
            get_database_url(),
            echo=echo,
            pool_pre_ping=True,
        )
        _session_maker = async_sessionmaker(
            _engine, expire_on_commit=False
        )

    return _engine


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    if _session_maker is None:
        init_engine()
    return _session_maker  # type: ignore[return-value]


async def get_postgres_db() -> AsyncGenerator[AsyncSession, None]:
    session_maker = get_session_maker()
    async with session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

def get_engine() -> AsyncEngine:
    if _engine is None:
        return init_engine()
    return _engine

# =====================================================
# CREATE TABLES
# =====================================================

async def create_tables() -> None:
    engine = get_engine()

    async with engine.begin() as conn:
        await conn.run_sync(PostgresBase.metadata.create_all)
