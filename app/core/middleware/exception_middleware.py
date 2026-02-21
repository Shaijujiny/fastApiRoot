# app/core/exception_handlers.py

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.config import settings
from app.core.error.error_types import ErrorType
from app.core.error.message_codes import MessageCode
from app.core.response.response_builder import ResponseBuilder
from app.core.response.status_mapper import get_http_status


class AppException(HTTPException):
    def __init__(self, error_type, message_code, status_code):
        self.error_type = error_type
        self.message_code = message_code
        self.status_code = status_code


async def global_exception_handler(request: Request, exc: Exception):

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

    return ResponseBuilder.build(
        ErrorType.SYS_500_INTERNAL_ERROR,
        MessageCode.INTERNAL_ERROR,
        lang="en",
    )


async def app_exception_handler(request, exc: AppException):

    lang = request.headers.get("Accept-Language", "en")


    response = ResponseBuilder.build(
        error_type=exc.error_type,
        message_code=exc.message_code,
        lang=lang,
    )

    return response