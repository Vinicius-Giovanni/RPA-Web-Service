from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.logging.config import get_logger
from core.logging.context import get_correlation_id

"""
Tratamento global de exceções de aplicação.

Este módulo centraliza a definição e o registro dos handlers
globais de erro utilizados pela API.

Responsabilidades:

- Definir exceções de domínio da aplicação.
- Padronizar respostas de erro.
- Registrar eventos de falha nos logs.
- Propagar Correlation IDs para rastreabilidade.
- Evitar vaxamentos de detalhes internos para clientes externos.

Todas exceções não tratadas são capturadas por um handler
genérico que retorna uma resposta padronizada ao consumidor.
"""

logger = get_logger(__name__)

class ApplicationError(Exception):
    """
    Exceção base da aplicação.

    Deve ser utilizada como classe raiz para erros conhecidos
    do domínio ou da camada de aplicação.

    Attributes:
        status_code:
            Código HTTP retornado ao cliente.
        
        message:
            Mensagem descritiva do erro.
    """
    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class ConfigurationError(ApplicationError):
    """
    Exceção utilizada para falhas de configuração

    Deve ser lançada quando recursos obrigatórios da aplicação
    não estiverem corretamente configurados, como variáveis
    de ambiente ou integrações externas.

    Returns:
        HTTP 500 Internal Server Error.
    """
    status_code = 500

async def application_error_handler(request: Request, exc: ApplicationError) -> JSONResponse:
    """
    Processa exceções conhecidas da aplicação.

    O erro é registrado em log como warning e uma resposta
    padronizada é retornada ao cliente contendo o Correlation ID
    para facilitar rastreamento e suporte.

    Args:
        request:
            Requisição que originou a exceção.

        exc:
            Exceção da aplicação capturada.

    Returns:
        JSONResponse:
            Resposta contendo detalhes do erro e identificador
            de correlação.
    """
    logger.warning("application_error", extra={"path": request.url.path, "error": exc.message})
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "correlation_id": get_correlation_id()},
    )

async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Processa exceções não tratadas.

    Este handler atua como mecanismo de protelão global,
    impedindo q detahles internos da aplicação sejam
    expostos ao cliente.

    O erro completo é registrado nos logs para posterior investigação.

    Args:
        request:
            Requisição que originou a falha.

        exc:
            Exceção capturada.

    Returns:
        JSONResponse:
            Resposta genérica de erro interno.
    """
    logger.exception("unhandled_error", extra={"path": request.url.path})
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno inesperado.", "correlation_id": get_correlation_id()},
    )

def register_exception_handlers(app: FastAPI) -> None:
    """
    Registra os handler globais de exceção da aplicação.

    Os handlers sao executadas automaticamente pelo FastAPI
    sempre que uma exceção correspondente for lançada durante
    o processamento de uma requisição.

    Handlers registrados:

    - ApplicationError
    - Exception

    Args:
        app:
            Instância da aplicação FastAPI.
    """
    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)