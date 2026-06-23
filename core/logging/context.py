from __future__ import annotations

from contextvars import ContextVar
from uuid import uuid4

"""
Gerenciamento de contexto de execução da aplicação.

Este módulo centraliza os identificadores utilizados para
rastreamento e observabilidade do sistema.

Os identificadores são armazenados utilizando ContextVar,
garantindo isolamento entre requisições concorrentes em
ambientes assíncronos.

Identificadores disponíveis:

- Correlation ID:
    Identifica uma requisição de ponta a ponta.

- Execution ID:
    Identifica uma execução específica dentro do sistema.

Esses valores são automaticamente incorporados aos logs
estruturados da aplicação.
"""

# Identificador utilizado para correlacionar eventos
# pertencentes à mesma requisição.
correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")

# Identificador utilizado para rastrear uma execução
# específica dentro do sistema.
execution_id_var: ContextVar[str] = ContextVar("execution_id", default="")

def get_correlation_id() -> str:
    """
    Retorna o Correlation ID atual.

    Caso nenhum identificador esteja definido no contexto
    atual, um novo UUID é gerado automaticamente.

    Returns:
        str:
            Correlation ID associado À execução atual.
    """
    value = correlation_id_var.get()

    if value:
        return value
    value = str(uuid4())
    correlation_id_var.set(value)
    return value

def set_correlation_id(value: str | None=None) -> str:
    """
    Define o CorrelationID do contexto atual.

    Caso nenhum valor seja fornecido, um novo UUID é gerado.

    Args:
        value:
            Identificador a ser utilizado.

    Returns:
        str:
            Correlation ID armazenado no contexto.
    """
    value = value or str(uuid4())
    correlation_id_var.set(value)
    return value

def get_execution_id() -> str:
    """
    Retorna o Execution ID atual.

    Caso não exista um identificador definido pra o contexto,
    um novo UUID é criado automaticamente.

    Returns:
        str:
            Execution ID associado à execução atual.
    """
    value = execution_id_var.get()
    if value:
        return value
    value = str(uuid4())
    execution_id_var.set(value)
    return value

def set_execution_id(value: str | None=None) -> str:
    """
    Define o execution id do contexto atual.

    Caso nenhum valor seja informado, um novo UUID será gerado.

    Args:
        value:
            Identificador da execução.

    Returns:
        str:
            Execution ID armazenado no contexto.
    """
    value = value or str(uuid4())
    execution_id_var.set(value)
    return value
