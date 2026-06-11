from __future__ import annotations

from contextvars import ContextVar
from uuid import uuid4

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")
execution_id_var: ContextVar[str] = ContextVar("execution_id", default="")

def get_correlation_id() -> str:
    value = correlation_id_var.get()

    if value:
        return value
    value = str(uuid4())
    correlation_id_var.set(value)
    return value

def set_correlation_id(value: str | None=None) -> str:
    value = value or str(uuid4())
    correlation_id_var.set(value)
    return value

def get_execution_id() -> str:
    value = execution_id_var.get()
    if value:
        return value
    value = str(uuid4())
    execution_id_var.set(value)
    return value

def set_execution_id(value: str | None=None) -> str:
    value = value or str(uuid4())
    execution_id_var.set(value)
    return value
