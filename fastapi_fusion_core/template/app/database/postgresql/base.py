from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData


# PostgreSQL Naming Convention
POSTGRES_NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_label)s",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class PostgresBase(DeclarativeBase):
    """
    Base class for all PostgreSQL models.
    """

    metadata = MetaData(naming_convention=POSTGRES_NAMING_CONVENTION)

    def __repr__(self) -> str:
        pk = getattr(self, "id", None)
        return f"<{self.__class__.__name__} id={pk!r}>"