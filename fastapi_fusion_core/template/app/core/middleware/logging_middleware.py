import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging.logger import get_logger


logger = get_logger("app.middleware")


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        try:
            response = await call_next(request)
            status_code = response.status_code

        except Exception as exc:
            logger.exception(
                f"Exception occurred | {method} {path} | IP: {client_ip}"
            )
            raise exc

        process_time = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"{method} {path} | "
            f"Status: {status_code} | "
            f"Time: {process_time}ms | "
            f"IP: {client_ip}"
        )

        return response