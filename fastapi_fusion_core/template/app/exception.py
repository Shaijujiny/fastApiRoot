from fastapi import Request
from app.config import settings
from app.core.error.message_codes import MessageCode
from app.core.response.response_builder import ResponseBuilder
from app.core.error.error_types import ErrorType



async def custom_exception_handler(request: Request, exc: Exception):

    # Development mode → show real error
    if settings.ENVIRONMENT == "development":
        return ResponseBuilder.build(
            ErrorType.SYS_500_INTERNAL_ERROR,
            MessageCode.INTERNAL_ERROR,
            lang="en",
            data={
                "exception_type": type(exc).__name__,
                "detail": str(exc),
            },
        )

    # Production mode → hide internal details
    return ResponseBuilder.build(
        ErrorType.SYS_500_INTERNAL_ERROR,
        MessageCode.INTERNAL_ERROR,
        lang="en",
    )