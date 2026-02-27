from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError

from app.config import settings
from app.core.error.error_types import ErrorType
from app.core.error.message_codes import MessageCode
from app.core.response.response_builder import ResponseBuilder


class AppException(HTTPException):
    def __init__(
        self,
        error_type: ErrorType,
        message_code: MessageCode,
        status_code: int,
        detail: str | None = None,
    ):
        self.error_type = error_type
        self.message_code = message_code
        self.status_code = status_code
        self.detail = detail
        # Use provided detail if available, otherwise fallback to message_code
        super().__init__(status_code=status_code, detail=detail or message_code)


async def global_exception_handler(request: Request, exc: Exception):
    """Handles all uncaught exceptions."""
    exc_type = type(exc).__name__

    # ── SQLAlchemy / PyMySQL database connection errors ──────────────────────
    # Covers: unknown database, wrong credentials, host unreachable, etc.
    if isinstance(exc, SQLAlchemyOperationalError):
        # Extract the root cause message cleanly
        root_cause = exc.orig.args[1] if exc.orig and exc.orig.args else str(exc)
        return ResponseBuilder.build(
            ErrorType.SYS_500_INTERNAL_ERROR,
            MessageCode.INTERNAL_ERROR,
            lang="en",
            data={"detail": f"Database connection error: {root_cause}"},
        )

    # ── asyncpg / PostgreSQL catalog errors ──────────────────────────────────
    if "asyncpg" in str(type(exc)) or exc_type == "InvalidCatalogNameError":
        return ResponseBuilder.build(
            ErrorType.SYS_500_INTERNAL_ERROR,
            MessageCode.INTERNAL_ERROR,
            lang="en",
            data={"detail": f"Database error: {exc}"},
        )

    # ── Development: expose full exception detail ────────────────────────────
    if settings.ENVIRONMENT == "development":
        return ResponseBuilder.build(
            ErrorType.SYS_500_INTERNAL_ERROR,
            MessageCode.INTERNAL_ERROR,
            lang="en",
            data={
                "exception_type": exc_type,
                "detail": str(exc),
            },
        )

    # ── Production: return generic error ────────────────────────────────────
    return ResponseBuilder.build(
        ErrorType.SYS_500_INTERNAL_ERROR,
        MessageCode.INTERNAL_ERROR,
        lang="en",
    )


async def app_exception_handler(request: Request, exc: AppException):
    """Handles custom AppException."""
    lang = request.headers.get("Accept-Language", "en")

    data = None
    if exc.detail and exc.detail != exc.message_code:
        data = {"detail": exc.detail}

    return ResponseBuilder.build(
        error_type=exc.error_type,
        message_code=exc.message_code,
        lang=lang,
        data=data,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles Pydantic validation errors."""
    lang = request.headers.get("Accept-Language", "en")

    return ResponseBuilder.build(
        error_type=ErrorType.VAL_400_VALIDATION_ERROR,
        message_code=MessageCode.VALIDATION_ERROR,
        lang=lang,
        data=exc.errors(),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handles standard FastAPI HTTPExceptions."""
    lang = request.headers.get("Accept-Language", "en")

    # Map status code to our error type if possible
    status_map = {
        400: (ErrorType.VAL_400_INVALID_INPUT, MessageCode.INVALID_INPUT),
        401: (ErrorType.AUTH_401_UNAUTHORIZED, MessageCode.UNAUTHORIZED_ACCESS),
        403: (ErrorType.AUTH_403_ACCESS_DENIED, MessageCode.ACCESS_DENIED),
        404: (ErrorType.RES_404_NOT_FOUND, MessageCode.RESOURCE_NOT_FOUND),
        409: (ErrorType.CON_409_CONFLICT_ERROR, MessageCode.CONFLICT_ERROR),
    }

    error_type, message_code = status_map.get(
        exc.status_code, (ErrorType.SYS_500_INTERNAL_ERROR, MessageCode.INTERNAL_ERROR)
    )

    return ResponseBuilder.build(
        error_type=error_type,
        message_code=message_code,
        lang=lang,
        data={"detail": exc.detail},
    )
