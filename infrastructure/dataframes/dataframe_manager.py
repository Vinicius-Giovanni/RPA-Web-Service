import pandas as pd
from pathlib import Path
from core.logging.log import ExecutionLogger
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
        
        if isinstance(caminho, str):
            path = Path(caminho)
        else:
            path = caminho

        if not path.exists():
            await logger.warning(f"O caminho fornecido para ler o dataframe não existe: {path}")
            return pd.DataFrame()  # Retorna um DataFrame vazio se o caminho não existir
        
        if path.stat().st_size == 0:
            await logger.warning(f'O arquivo CSV está vazio: {path}')
            return pd.DataFrame()  # Retorna um DataFrame vazio se o arquivo estiver vazio

        return pd.read_csv(
            path,
            sep=sep,
            encoding=encoding,
            dtype=str
        )
    
    def save_csv(self,
                       caminho: str | Path,
                       df: pd.DataFrame, 
                       encoding: str = "utf-8",
                       sep = ";") -> None:
        
        if isinstance(caminho, str):
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
        except Exception as e:
            print(f'Erro ao ler o CSV: {e}')


    def load_parquet(self, caminho: str | Path) -> pd.DataFrame:
        
        if isinstance(caminho, str):
            path = Path(caminho)
        else:
            path = caminho

        if not path.exists():
            return pd.DataFrame()  # Retorna um DataFrame vazio se o caminho não existir
        
        if path.stat().st_size == 0:
            return pd.DataFrame()  # Retorna um DataFrame vazio se o arquivo estiver vazio
        
        return pd.read_parquet(path).astype('string')
    
    async def save_parquet(self, caminho: str | Path, df: pd.DataFrame) -> None:
        if isinstance(caminho, str):
            path = Path(caminho)
        else:
            path = caminho

        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            df.to_parquet(
                path,
                index=False,
                engine='pyarrow',
                compression='zstd'
            )
            await logger.info(f'Arquivo Parquet criado com sucesso no caminho: {path}')
        except Exception as e:
            await logger.error(f'Erro ao tentar gerar arquivo Parquet no caminho: {path}\n erro: {e}')
            raise

    def load_txt(
            self,
            caminho: str | Path,
            sep: str = ';',
            encoding: str = 'utf-8',
            columns: list[str] | None = None
    ) -> pd.DataFrame:
        
        if isinstance(caminho, str):
            path = Path(caminho)
        else:
            path = caminho

        if not path.exists():
            return pd.DataFrame()
        
        arquivos_txt = []

        # Caso seja um arquivo único
        if path.is_file():

            if path.suffix.lower() != ".txt":
                return pd.DataFrame()
            
            arquivos_txt.append(path)
        
        # Caso seja uma pasta
        elif path.is_dir():

            arquivos_txt = list(path.glob("*.txt"))

            if not arquivos_txt:
                return pd.DataFrame()
            
        dataframes = []

        try:
            for arquivo in arquivos_txt:

                if arquivo.stat().st_size == 0:
                    continue
                
                df = pd.read_csv(
                    arquivo,
                    sep=sep,
                    encoding=encoding,
                    dtype=str,
                    usecols=columns
                )

                dataframes.append(df)

            if not dataframes:
                return pd.DataFrame()
            
            return pd.concat(
                dataframes,
                ignore_index=True
            )
        
        except Exception as e:
            raise