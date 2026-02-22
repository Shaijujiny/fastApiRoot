
from collections.abc import Generator
from contextlib import contextmanager
from urllib.parse import quote_plus

from pymysql import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


from app.config import settings as CONFIG_SETTINGS
from app.core.logging.logger import get_logger

logger = get_logger(__name__)


def build_sqlalchemy_database_url_from_settings():
    """
    Build a SQLAlchemy URL based on the provided settings.

    Parameters
    ----------
        CONFIG_SETTINGS (Settings): An instance of the Settings class
        containing the PostgreSQL connection details.

    Returns
    -------
        str: The generated SQLAlchemy URL.
    """
    db_host = CONFIG_SETTINGS.MYSQL_HOST
    db_port = CONFIG_SETTINGS.MYSQL_PORT
    db_name = CONFIG_SETTINGS.MYSQL_DB
    db_user = CONFIG_SETTINGS.MYSQL_USER
    db_pass = CONFIG_SETTINGS.MYSQL_PASSWORD

    encoded_password = quote_plus(db_pass.encode()) if db_pass else None
    if not db_pass:
        database_url = f"mysql+pymysql://{db_user}@{db_host}:{db_port}/{db_name}"
    else:
        database_url = f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"


    return database_url



SQLALCHEMY_DATABASE_URL = build_sqlalchemy_database_url_from_settings()
_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True,
    pool_recycle=3600,
)

_session_local = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def get_mysql_db() -> Generator[Session, None, None]:
    """
    Get the database session.

    Returns
    -------
        db: The database session.

    Raises
    ------
        OperationalError: If an error occurs while accessing the database.
    """
    db = _session_local()
    try:
        yield db
    except OperationalError as e:
        error_message = f"An error occurred while getting the database session. Error: {e!s}"
        logger.exception(error_message)
        raise  # Re-raise the exception for proper error handling outside the context manager
    finally:
        db.close()


@contextmanager
def get_ctx_mysql_db() -> Generator[Session, None, None]:
    """Get the database session within a context manager."""
    db = _session_local()  # Assuming _session_local() creates a new session
    try:
        yield db
    except Exception as e:
        error_message = f"An error occurred while getting the database session. Error: {e!s}"
        logger.exception(error_message)
        raise  # Re-raise the exception for proper error handling outside the context manager
    finally:
        db.close()  # Close the database session
