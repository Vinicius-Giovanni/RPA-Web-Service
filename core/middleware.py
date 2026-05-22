from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from time import monotonic
from collections import defaultdict, deque
from typing import Dict, Deque

class AdvancedMiddleware(BaseHTTPMiddleware):
    """
    Middleware de observabilidade + rate limit básico por IP.

    Lógica:
    - Rotas públicas comuns: até 120 req/min por IP
    - Rotas sensíveis de autenticação/cadastro: até 10 req/min por IP
    - Ignora assets estáticos e favicon
    """

    DEFAULT_LIMIT_PER_MIN = 120
    AUTH_LIMIT_PER_MIN = 10

    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_records: Dict[str, Deque[float]] = defaultdict(deque)

    async def log_message(self, message: str):
        print(message)

    def _is_ignored_path(self, path: str) -> bool:
        return path.startswith("/static") or path == '/favicon.ico'
    
    def _is_auth_path(self, path: str) -> bool:
        return path in {'/cadastro', '/login'}

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if self._is_ignored_path(path):
            return await call_next(request)
        
        client_ip = request.client.host if request.client else 'unknown'
        limit_per_min = self.AUTH_LIMIT_PER_MIN if self._is_auth_path(path) else self.DEFAULT_LIMIT_PER_MIN

        now = monotonic()
        window_start = now - 30
        key = f'{client_ip}:{"auth" if self._is_auth_path(path) else "default"}'
        request_times = self.rate_limit_records[key]

        while request_times and request_times[0] < window_start:
            request_times.popleft()

        if len(request_times) >= limit_per_min:
            return Response(content='Rate limit exceeded', status_code=429)
        
        request_times.append(now)
        await self.log_message(f'Request to {path}')

        start_time = monotonic()
        response = await call_next(request)

        process_time = monotonic() - start_time

        response.headers['X-Process-Time'] = str(process_time)
        await self.log_message(f'Response for {path} took {process_time} seconds')
        return response
