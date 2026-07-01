from pathlib import Path
from datetime import datetime
import aiofiles
import json
from uuid import uuid4

from settings.paths import LOG_DIR

class ExecutionLogger:
    LOG_DIRECTORIES = {
        "execution": "executions",
        "error": "errors",
        "audit": "audit",
    }

    def __init__(
            self,
            automation_name: str,
            execution_id: str,
            log_type: str = 'execution',
    ):
        
        self.automation_name = automation_name
        self.execution_id = execution_id
        self.log_type = self._normalize_log_type(log_type)

       
    @staticmethod
    def _normalize_log_type(log_type: str) -> str:
        return log_type.strip().lower().replace(" ", "_")

    def _file_for(self, log_type: str) -> Path:
        normalized_log_type = self._normalize_log_type(log_type)
        directory_name = self.LOG_DIRECTORIES.get(normalized_log_type, "executions")
        log_path = LOG_DIR / directory_name / self.automation_name
        log_path.mkdir(parents=True, exist_ok=True)
        return log_path / f"{normalized_log_type}.jsonl"

    async def write(
            self,
            level: str,
            message: str,
            log_type: str | None = None,
    ):
        normalized_log_type = self._normalize_log_type(log_type or self.log_type)
        file_path = self._file_for(normalized_log_type)

        payload = {
           "timestamp": datetime.now().isoformat(),
            "level": level,
            "type": normalized_log_type,
            "execution_id": self.execution_id,
            "automation_name": self.automation_name,
            "message": message,
        }

        async with aiofiles.open(
            file_path,
            "a",
            encoding="utf-8"
            ) as f:
            
            await f.write(
                json.dumps(payload, ensure_ascii=False) + "\n"
            )
    
    async def info(self, message: str):
        await self.write(
            "INFO",
            message,
            log_type='execution',
        )
    
    async def warning(self, message: str):
        await self.write(
            "WARNING",
            message,
            log_type='error',
        )

    async def error(self, message: str):
        await self.write(
            "ERROR",
            message,
            log_type='error'
        )

    async def audit(self, message: str):
        await self.write(
            "AUDIT",
            message,
            log_type='audit',
        )
    
    async def sucess(self, message: str):
        await self.write(
            "SUCCESS",
            message,
            log_type='execution',
        )


execution_id = str(uuid4())

logger = ExecutionLogger(
    automation_name="log",
    execution_id=execution_id
)
