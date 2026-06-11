from __future__ import annotations

import logging
from logging.config import dictConfig
from pathlib import Path

from pythonjsonlogger import jsonlogger

from core.config.settings import LoggingSettings, get_settings
from core.logging.context import get_correlation_id, get_execution_id

class CorrelationJsonFormatter(jsonlogger.jsonFormatter):
    def add_fields(self, log_record, record, message_dict): # type: ignore[no-untyped-def]
        super().add_fields(log_record, record, message_dict)
        log_record.setdefault('correlation_id', get_correlation_id())
        log_record.setdefault('execution_id', get_execution_id())
        log_record.setdefault('logger', record.name)
        log_record.setdefault('level', record.levelname)

def _ensure_dirs(settings: LoggingSettings) -> None:
    for directory in (settings.log_dir, settings.execution_dir, settings.error_dir, settings.audit_dir):
        Path(directory).mkdir(parents=True, exist_ok=True)

def configure_logging() -> None:
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
                    "maxBytes": settings.backup_count,
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
    return logging.getLogger(name)

def get_audit_logger() -> logging.Logger:
    return logging.getLogger("audit")