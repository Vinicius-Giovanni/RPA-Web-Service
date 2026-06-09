from pathlib import Path
from datetime import datetime
import aiofiles
import json
from uuid import uuid4

from settings.paths import LOG_EXECUTIONS

class ExecutionLogger:

    def __init__(
            self,
            automation_name:str,
            execution_id:str
    ):
        
        self.automation_name = automation_name
        self.execution_id = execution_id

        self.log_path = LOG_EXECUTIONS / automation_name

        self.log_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.file = (
            self.log_path / f"{execution_id}.jsonl"
        )
    
    async def write(
            self,
            level:str,
            message:str
    ):
        
        payload = {
            "timestamp":
                datetime.utcnow().isoformat(),

            "level":
                level,

            "message":
                message
        }

        async with aiofiles.open(
            self.file,
            "a",
            encoding="utf-8"
        ) as f:
            
            await f.write(
                json.dumps(payload) + "\n"
            )
    
    async def info(self, message:str):
        await self.write(
            "INFO",
            message
        )
    
    async def warning(self, message:str):
        await self.write(
            "WARNING",
            message
        )

    async def error(self, message:str):
        await self.write(
            "ERROR",
            message
        )
    
    async def sucess(self, message:str):
        await self.write(
            "SUCCESS",
            message
        )


execution_id = str(uuid4())

logger = ExecutionLogger(
    automation_name="log",
    execution_id=execution_id
)
