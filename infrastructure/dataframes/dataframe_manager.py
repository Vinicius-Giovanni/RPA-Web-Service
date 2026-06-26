import pandas as pd
from pathlib import Path
from utils.log import ExecutionLogger
from uuid import uuid4

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="dataframe_manager",
        execution_id=execution_id
)

class DataframeManager:

    async def load_csv(self, caminho: str | Path, sep: str, enconding: str) -> pd.DataFrame:

        if not Path(caminho).exists():
            await logger.warning(f"O caminho fornecido para ler o dataframe não existe: {caminho}")

        return pd.read_csv(
            caminho,
            sep=sep,
            encoding=enconding,
            dtype=str
        )
    
    async def save_csv(self,
                       caminho: str | Path,
                       df: pd.DataFrame, 
                       encoding: str = "utf-8",
                       sep = ";") -> None:
        try:
            df.to_csv(
                caminho,
                index=False,
                sep=sep,
                encoding=encoding
            )
            await logger.info(f"Arquivo CSV criado com sucesso no caminho: {caminho}")
        except Exception as e:
            await logger.error(f"Erro ao tentar gerar arquivo CSV no caminho: {caminho}\n erro: {e}")

