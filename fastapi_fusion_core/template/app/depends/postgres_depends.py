from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgresql.session import get_postgres_db


async def get_pg_db() -> AsyncSession:
    """Dependency for getting a PostgreSQL async database session."""
    async for session in get_postgres_db():
        yield session
