from __future__ import annotations

from collections import defaultdict, deque
from time import monotonic
from uuid import uuid4
from typing import Deque

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from core.logging.log import ExecutionLogger

from core.logging.context import set_correlation_id, set_execution_id

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="observability_middleware",
        execution_id=execution_id
)


"""
Middleware responsável pela camada transversal de observabilidade.

Este componente centraliza:

- Logging estruturado.
- Correlation ID.
- Execution ID.
- Métricas de latência.
- Rate limitindg.

Seu objetivo é fornecer rastreabilidade completa das requisições
e proteção básica contra abuso da API.
"""
class ObservabilityMiddleware(BaseHTTPMiddleware):
    """
    Middleware responsável por observabilidade e proteção básica da API.

    Funcionalidades implementadas:

    - Geração e propagação de Correlation ID.
    - Geração e propagação de Execution ID.
    - Registro estruturado de logs de entrada e saída.
    - Medição do tempo de processamento das requisições.
    - Controle de taxas (Rate Limiting) por IP.
    - Inclusão de metadados de rastreamento nos headers da resposta.

    O middleware é executado para todas as requisições HTTP,
    exceto para caminhos explicitamente ignorados.

    Rate limits configurados:

    -   Rotas padrão:
        120 requisições por janela.

    -   Rotas de autenticação:
        10 requisições por janela.
    
    A janela de controle é definida por ``window_seconds``.

    Attributes:
        default_limit_per_window:
            Limite padrão de requisições por janela.
        
        auth_limit_per_window:
            Limite específico para endoints de autenticação.

        window_seconds:
            Duração da janela de rate limiting em segundos.
        
            rate_limit_records:
                Estrutura utilizada para armazenar os timestamps das
                requisições realizadas por cada cliente.
    """
    default_limit_per_window = 120
    auth_limit_per_window = 10
    window_seconds = 30

    def __init__(self, app): # type: ignore[no-untyped-def]
        """
        Inicializa o middleware.

        Cria a estrutura em memória utilizada para controle
        das requisições por cliente.

        Args:
            app:
                Aplicação ASGI que será imterceptada pelo middleware.
        """
        super().__init__(app)
        self.rate_limit_records: dict[str, Deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Processa todas as requisições HTTP recebidas pela aplicação.

        Fluxo de execução:

        1. Ignora caminhos configurados.
        2. Define Correlation ID e Execution ID.
        3. Executa validação de rate limit.
        4. Registra início da requisição
        5. Processa a requisição.
        6. Calcula tempo de execução.
        7. Adiciona headers de observabilidade.
        8. Registra finalização da requisição

        Args:
            request:
                Requisição HTTP recebida.

            call_next:
                Próximo middleware ou endpoint da cadeia de execução.

        Returns:
            Response:
                Resposta HTTP produzida pela aplicação.
        """
        path = request.url.path
        if self._is_ignored_path(path):
            return await call_next(request)
        
        correlation_id = set_correlation_id(request.headers.get("X-Correlation-ID"))
        execution_id = set_execution_id(request.headers.get("X-Execution-ID"))

        limited_response = self._rate_limit(request)
        if limited_response is not None:
            return limited_response
        
        start_time = monotonic()

        await logger.info("Processando requisição HTTP")
        
        response = await call_next(request)
        process_time = monotonic() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers['X-Execution-ID'] = execution_id

        logger.info("Requisição HTTP finalizada")

        return response
    
    def _rate_limit(self, request: Request) -> Response | None:
        """
        Aplica controle de taxa baseado em IP.

        O algoritmo utiliza uma janela deslizante (Sliding Window),
        armazenando os timestamps das requisições realizadas por cada
        cliente durante o período configurado.

        Caso o limite seja excedido, uma resposta HTTP 429 é retornada.

        Args:
            request:
                Requisição HTTP atual.
        
        Returns:
            Response | None:
                Retorna uma resposta HTTP 429 caso o limite seja
                excedido. Caso contrário, retorna None.
        """

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
            
            logger.warning("Rate limit excedido")

            return Response(content="Rate limit exceeded", status_code=429)
        request_times.append(now)
        return None
    
    @staticmethod
    def _is_ignored_path(path: str) -> bool:
        """
        Verifica se o caminho deve ser ignorado pelo middleware.

        Caminhos ignorados não recebem controle de observabilidade
        nem validação de rate limiting.

        Args:
            path:
                Caminho da requisição.

        Returns:
            bool:
                True caso o caminho deve ser ignorado.
        """
        return path.startswith("/static") or path =="/favicon.ico"
    
    @staticmethod
    def _is_auth_path(path: str) -> bool:
        """
        Verifica se o endpoint pertence ao fluxo de autenticação.

        Endpoints de autenticação possuem um limite de requisições 
        mais restritivo para reduzir tentativas de abuso e ataques
        de força bruta.

        Args:
            path:
                Caminho da requisição.

        Returns:
            bool:
                True caso seja uma rota de autenticação.
        """
        return path in {"/castro", "/login"}