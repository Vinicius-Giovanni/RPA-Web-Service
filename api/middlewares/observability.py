from __future__ import annotations

from collections import defaultdict, deque
from time import monotonic
from typing import Deque

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from core.logging.config import get_logger
from core.logging.context import set_correlation_id, set_execution_id

logger = get_logger(__name__)

class ObservabilityMiddleware(BaseHTTPMiddleware):
    default_limit_per_window = 120
    auth_limit_per_window = 10
    window_seconds = 30

    def __init__(self, app): # type: ignore[no-untyped-def]
        super().__init__(app)
        self.rate_limit_records: dict[str, Deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path
        if self._is_ignored_path(path):
            return await call_next(request)
        
        correlation_id = set_correlation_id(request.headers.get("X-Correlation-ID"))
        execution_id = set_execution_id(request.headers.get("X-Execution-ID"))

        limited_response = self._rate_limit(request)
        if limited_response is not None:
            return limited_response
        
        start_time = monotonic()

        logger.info("request_started",
                    extra={"path": path, "method": request.method})
        
        response = await call_next(request)
        process_time = monotonic() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers['X-Execution-ID'] = execution_id

        logger.info(
            "request_finished",
            extra={"path": path, "method": request.method, "status_code": response.status_code, "process_time": process_time},
        )

        return response
    
    def _rate_limit(self, request: Request) -> Response | None:
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"
        is_auth = self._is_auth_path(path)
        limit = self.auth_limit_per_window if is_auth else self.default_limit_per_window
        key = f"{client_ip}:{'auth' if is_auth else 'default'}"
        now = monotonic()
        request_times = self.rate_limit_records[key]
        while request_times and request_times[0] < now - self.window_seconds:
            request_times.popleft()
        
        if len(request_times) >= limit:
            
            logger.warning(
                "rate_limit_exceeded",
                extra={"path": path, "client_ip": client_ip}
            )

            return Response(content="Rate limit exceeded", status_code=429)
        request_times.append(now)
        return None
    
    @staticmethod
    def _is_ignored_path(path: str) -> bool:
        return path.startswith("/static") or path =="/favicon.ico"
    
    @staticmethod
    def _is_auth_path(path: str) -> bool:
        return path in {"/castro", "/login"}