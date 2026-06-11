from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.logging.config import get_logger
from core.logging.context import get_correlation_id

logger = get_logger(__name__)

class ApplicationError(Exception):
    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class ConfigurationError(ApplicationError):
    status_code = 500

async def apllication_error_handler(request: Request, exc: ApplicationError) -> JSONResponse:
    logger.warning("application_error", extra={"path": request.url.path, "error": exc.message})
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "correlation_id": get_correlation_id()},
    )

async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled_error", extra={"path": request.url.path})
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno inesperado.", "correlation_id": get_correlation_id()},
    )

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationError, apllication_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)