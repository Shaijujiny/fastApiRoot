from sqlalchemy.ext.asyncio import AsyncSession
from app.database.postgresql.session import AsyncPostgresSession


async def get_postgres_db() -> AsyncSession:
    async with AsyncPostgresSession() as session:
        try:
            yield session
        finally:
            await session.close()