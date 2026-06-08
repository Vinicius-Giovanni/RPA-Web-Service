from pathlib import Path
from datetime import datetime
import aiofiles
import json

class ExecutionLogger:

    def __init__(
            self,
            automation_name:str,
            execution_id:str
    ):
        
        self.automation_name = automation_name
        self.execution_id = execution_id

        self.log_path = 