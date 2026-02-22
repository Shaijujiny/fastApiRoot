from sqlalchemy.orm import Session

from app.database.mysql.session import get_mysql_db


def get_my_db() -> Session:
    """Dependency for getting a MySQL database session."""
    for session in get_mysql_db():
        yield session
