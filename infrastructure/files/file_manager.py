import shutil
from pathlib import Path
from utils.log import ExecutionLogger
from uuid import uuid4

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="file_manager",
        execution_id=execution_id
)


class FileManager:
    
    @staticmethod
    async def _exists(caminho: str) -> bool:
        if Path(caminho).exists():
            logger.info(f"Caminho validado: {caminho}")
        else:
            logger.info(f"Caminho nãõ foi encontrado: {caminho}")

    
    @staticmethod
    async def _copy(origem: str, destino: str):
        if shutil.copy2(origem, destino):
            logger.info(f"Arquivo copiado da origem: {origem} e colado para o destino: {destino}")
        else:
            logger.info(f"Arquivo não encontrado na origem: {origem}")

    @staticmethod
    async def _create_folder(caminho: str):
        if Path(caminho).mkdir(parents=True, exist_ok=True):
            logger.info(f"Pasta criada no caminho: {caminho}")
        else:
            logger.info(f"Pasta não foi criada no caminho: {caminho}")
