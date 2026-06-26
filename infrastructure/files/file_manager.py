import shutil
from pathlib import Path

class FileManager:
    
    @staticmethod
    async def exists(caminho: str) -> bool:
        return Path(caminho).exists()
    
    @staticmethod
    async def copy(origem: str, destino: str):
        shutil.copy2(origem, destino)

    @staticmethod
    async def create_folder(caminho: str):
        Path(caminho).mkdir(parents=True, exist_ok=True)