from __future__ import annotations

import logging
from logging.config import dictConfig
from pathlib import Path

from pythonjsonlogger import jsonlogger

from core.config.settings import LoggingSettings, get_settings
from core.logging.context import get_correlation_id, get_execution_id

"""
Configuração central do sistema de logging.

Este módulo é responsável por:

- Configurar o logging estruturado em formato JSON.
- Adicionar informações de rastreabilidade as logs.
- Criar diretórios necesários para armazenamento.
- Configurar handlers para diferentes categorias de logs.
- Disponibilizar loggers padronizados para a aplicação.

Os registros produzidos incluem automaticamente:

- Correlation ID
- Execution ID
- Nome do logger
- Nivel do log

A configuração é aplicada durante a inicialização da aplicação
e permanece ativa durante todo o ciclo de vida do processo.
"""

class CorrelationJsonFormatter(jsonlogger.jsonFormatter):
    """
    Formatter responsável por enriquecer logs estruturados.

    Estende o formatter JSON padrão adicionando informações
    de rastreabilidade e contexto da execução.

    Campos adicionados automaticamente:

    - correlation_id
    - execution_id
    - logger
    - level

    Esses atributos permitem correlacionar eventos
    pertencentes à mesma requisição ou execução.
    """
    def add_fields(self, log_record, record, message_dict): # type: ignore[no-untyped-def]
        """
        Adiciona campos extras ao registro de log.

        O método é executado para cada evento registrado,
        enriquecendo o payload JSON com informações de
        rastreamento e contexto.

        Args:
            log_record:
                Dicionário que será serializado para JSON.

            record:
                Objeto LogRecord produzido pelo módulo logging.
            
            message_dict:
                Campos adicionais enviados através do parâmetro
                ``extra`` durante a chamada do logger.
        """
        super().add_fields(log_record, record, message_dict)
        log_record.setdefault('correlation_id', get_correlation_id())
        log_record.setdefault('execution_id', get_execution_id())
        log_record.setdefault('logger', record.name)
        log_record.setdefault('level', record.levelname)

def _ensure_dirs(settings: LoggingSettings) -> None:
    """
    Garante a existência dos diretórios de logging.

    Caso os diretórios configurados não existam,
    eles são criados automaticamente durante a
    inicialização da aplicação.

    Diretórios criados:

    - logs gerais
    - logs de execução
    - logs de erro
    - logs de auditoria

    Args:
        settings:
            Configurações do sistema de logging.
    """
    for directory in (settings.log_dir, settings.execution_dir, settings.error_dir, settings.audit_dir):
        Path(directory).mkdir(parents=True, exist_ok=True)

def configure_logging() -> None:
    """
    Configura o sistema global de logging da aplicação.

    A configuração inclui:

    - Formatter JSON estruturado.
    - Handler para console.
    - Handler para logs de execução.
    - Handler para logs de erro.
    - Handler para logs de auditoria.
    - Rotação automática de arquivos.
    - Inclusão automática de metadados de rastreamento.

    Arquivos gerados:

    - application.jsonl
    - errors.jsonl
    - audit.jsonl

    O método deve ser executado apenas uma vez durante a inicialização da aplicação.
    """
    settings = get_settings().logging
    _ensure_dirs(settings)
    formatter_path = "core.logging.config.CorrelationJsonFormatter"
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatter": {
                "json": {
                    "()": formatter_path,
                    "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s %(correlation_id)s %(execution_id)s"
                }
            },
            "handlers": {
                "console": {"class": "logging.StreamHandler", "formatter": "json"},
                "execution_file": {
                    "class": "concurrent_log_handler.ConcurrentRotatingFileHandler",
                    "filename": str(settings.execution_dir / "application.jsonl"),
                    "maxBytes": settings.max_bytes,
                    "backupCount": settings.backup_count,
                    "formatter": "json",
                    "encoding": "utf-8",
                },
                "error_file": {
                    "class": "concurrent_log_handler.ConcurrentRotatingFileHandler",
                    "filename": str(settings.error_dir / "errors.jsonl"),
                    "maxBytes": settings.max_bytes,
                    "formatter": "json",
                    "encoding": "utf-8",
                    "level": "ERROR",
                },
                "audit_file": {
                    "class": "concurrent_log_handler.ConcurrentRotatingFileHandler",
                    "filename": str(settings.audit_dir / "audit.jsonl"),
                    "maxBytes": settings.max_bytes,
                    "backupCount": settings.backup_count,
                    "formatter": "json",
                    "encoding": "utf-8",
                },
            },
        "loggers" : {
            "audit": {"handlers": ["audit_file", "console"], "level": settings.level, "propagate": False},
        },
        "root": {"handlers": ["console", "execution_file", "error_file"], "level": settings.level},
        }
    )

def get_logger(name:str) -> logging.Logger:
    """
    Retorna um logger configurado da aplicação.

    O logger retornado utiliza toda a configuração
    definida em ``configure_logging``.

    Args:
        name:
            Nome do logger.

    Returns:
        logging.Logger:
            Instância configurada do logger.
    """
    return logging.getLogger(name)

def get_audit_logger() -> logging.Logger:
    """
    Retorno o logger de auditoria.

    Este logger deve ser utilizado para eventos
    relacionados à rastreabilidade de ações do sistema,
    incluindo operações críticas e atividades dos usuários.

    Returns:
        logging.Logger:
            Logger configurado para auditoria.
    """
    return logging.getLogger("audit")