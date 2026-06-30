import shutil
from pathlib import Path
from core.logging.log import ExecutionLogger
from uuid import uuid4

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="file_manager",
        execution_id=execution_id
)


class FileManager:
    
    @staticmethod
    async def _exists(caminho: str | Path) -> bool:
        if caminho is str:
            path = Path(caminho)
        else:
            path = caminho
        
        if path.exists():
            await logger.info(f"Caminho validado: {path}")
            return True
        
        await logger.error( f'Caminho não encontrado: {path}')
        raise FileNotFoundError(f'Caminho não encontrado: {path}')
    
    @staticmethod
    async def _copy(origem: str | Path, destino: str | Path):
        origem_path = Path(origem)
        destino_path = Path(destino)
        destino_path.parent.mkdir(parents=True,exist_ok=True)

        await FileManager._exists(origem_path)
        shutil.copy2(origem_path, destino_path)
        await logger.info(f'Arquivo copiado do origem: {origem_path} e colado para o destino: {destino_path}')

    @staticmethod
    async def _create_folder(caminho: str | Path):
        path = Path(caminho)
        path.mkdir(parents=True, exist_ok=True)
        await logger.info(f"Pasta criada no caminho: {path}")

