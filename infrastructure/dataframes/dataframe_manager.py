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

    async def load_csv(
            self,
            caminho: str | Path,
            sep: str = ';',
            encoding: str = 'utf-8'
            ) -> pd.DataFrame:
        
        if caminho is str:
            path = Path(caminho)
        else:
            path = caminho

        if not Path(caminho).exists():
            await logger.warning(f"O caminho fornecido para ler o dataframe não existe: {path}")
        
        if path.stat().st_size == 0:
            await logger.warning(f'O arquivo CSV está vazio: {path}')

        return pd.read_csv(
            path,
            sep=sep,
            encoding=encoding,
            dtype=str
        )
    
    async def save_csv(self,
                       caminho: str | Path,
                       df: pd.DataFrame, 
                       encoding: str = "utf-8",
                       sep = ";") -> None:
        
        if caminho is str:
            path = Path(caminho)
        else:
            path = caminho
        
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            df.to_csv(
                path,
                index=False,
                sep=sep,
                encoding=encoding
            )
            await logger.info(f"Arquivo CSV criado com sucesso no caminho: {path}")
        except Exception as e:
            await logger.error(f"Erro ao tentar gerar arquivo CSV no caminho: {path}\n erro: {e}")
            raise

