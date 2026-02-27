from collections.abc import Generator
from contextlib import contextmanager
from urllib.parse import quote_plus

from fastapi import status
from pymysql import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
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

try:
    _engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        future=True,
        pool_recycle=3600,
    )
    _session_local = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
except Exception as _exc:
    # Defer the import to avoid circular imports at module level
    from app.core.error.error_types import ErrorType
    from app.core.error.message_codes import MessageCode
    from app.core.middleware.exception_middleware import AppException

    logger.critical(
        "MySQL engine creation failed — check MYSQL_HOST / MYSQL_DB / credentials. "
        "Error: %s",
        _exc,
    )
    raise AppException(
        ErrorType.SYS_500_INTERNAL_ERROR,
        MessageCode.INTERNAL_ERROR,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"MySQL connection error: {_exc}",
    ) from _exc


def get_mysql_db() -> Generator[Session, None, None]:
    """
    Get the MySQL database session.

    Yields
    ------
        db: The active SQLAlchemy Session.

    Raises
    ------
        AppException: Wraps any PyMySQL / SQLAlchemy operational error into a
            structured 500 response so callers always receive a clean JSON body.
    """
    from app.core.error.error_types import ErrorType
    from app.core.error.message_codes import MessageCode
    from app.core.middleware.exception_middleware import AppException

    db = _session_local()
    try:
        yield db
    except (OperationalError, SQLAlchemyOperationalError) as exc:
        logger.exception("MySQL OperationalError: %s", exc)
        raise AppException(
            ErrorType.SYS_500_INTERNAL_ERROR,
            MessageCode.INTERNAL_ERROR,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"MySQL error: {exc}",
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected MySQL session error: %s", exc)
        raise
    finally:
        db.close()


@contextmanager
def get_ctx_mysql_db() -> Generator[Session, None, None]:
    """Get the MySQL database session within a context manager."""
    from app.core.error.error_types import ErrorType
    from app.core.error.message_codes import MessageCode
    from app.core.middleware.exception_middleware import AppException

    db = _session_local()
    try:
        yield db
    except (OperationalError, SQLAlchemyOperationalError) as exc:
        logger.exception("MySQL OperationalError (ctx): %s", exc)
        raise AppException(
            ErrorType.SYS_500_INTERNAL_ERROR,
            MessageCode.INTERNAL_ERROR,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"MySQL error: {exc}",
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected MySQL session error (ctx): %s", exc)
        raise
    finally:
        db.close()
