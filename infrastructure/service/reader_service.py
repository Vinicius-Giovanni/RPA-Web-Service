from __future__ import annotations

from pathlib import Path
from typing import Any
import duckdb
import pandas as pd
from uuid import uuid4

from core.logging.log import ExecutionLogger

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="reader_service",
        execution_id=execution_id
)


class ReaderService:
    """
    Responsável por leitura e escrita de arquivos

    toda interação com CSV, Parquet e Duckdb deve passar por esta classe.
    """

    def __init__(self, pipeline_config: dict, chunksize: int = 100_000):
        self.pipeline_config = pipeline_config
        self.chunksize = chunksize

    # PUBLIC

    async def read_csv(self, path: Path, pipeline_key: str) -> pd.DataFrame:

        cfg = self._get_pipeline_config(pipeline_key)

        encoding = cfg.get('encoding', 'utf-16')
        separator = cfg.get('sep', ';')

        files = self._get_csv_files(path)

        if not files:
            await logger.warning(f"Nenhum CSV encontrado no caminho fornecido: {path}")
            return pd.DataFrame()
        
        try:
            return self._read_csv_duckdb(
                files=files,
                separator=separator,
                encoding=encoding,
            )
        except Exception as e:
            await logger.warning(f'Duckdb falhou ao ler CSV. Fallback para Pandas. Motivo: {e}')

            return self._read_csv_pandas(
                files=files,
                separator=separator,
                encoding=encoding,
            )
        
    async def read_parquet(
            self,
            folder: Path,
            columns: list[str] | None = None,
    ) -> pd.DataFrame:
        
        files = sorted(folder.rglob('*.parquet'))

        if not files:
            await logger.info(f'Nenhum arquivo parquet mapeado')
            return pd.DataFrame()
        
        sql_files = self._sql_path_list(files)

        with duckdb.connect(':memory:') as conn:

            if columns:
                cols = ",".join(columns)
            else:
                cols = "*"

            return conn.execute(
                f"""
                SELECT {cols}
                FROM parquet_scan(
                    {sql_files},
                    union_by_name = true
                    )
                """
            ).df()
    
    async def export_parquet(
            self,
            dataframe: pd.DataFrame,
            output_file: Path,
    ) -> None:
        
        output_file.parent.mkdir(parents=True, exist_ok=True)

        dataframe = self._normalize_object_columns(dataframe)

        dataframe.to_parquet(
            output_file,
            index=False,
            compression='zstd',
        )
    
    # PRIVATE

    async def _read_csv_duckdb(
            self,
            files: list[Path],
            separator: str,
            encoding: str,
    ) -> pd.DataFrame:
        
        sql_files = self._sql_path_list(files)

        with duckdb.connect(':memory:') as conn:

            df = conn.execute(
                f"""
                SELECT *

                FROM read_csv_auto(
                    {sql_files},
                    delim='{separator}',
                    header=True,
                    sample_size=20000,
                    ignore_error=False,
                    ali_varchar=True,
                    union_by_name=True,
                    encoding='{self._duckdb_encoding(encoding)}'
                    )
                """
            ).df()
        
        return self.normalize_columns(df)
    
    async def _read_csv_pandas(
            self,
            files: list[Path],
            separator: str,
            encoding: str,
    ) -> pd.DataFrame:
        
        chunks = []

        for file in files:

            for chunk in pd.read_csv(
                file,
                sep=separator,
                encoding=encoding,
                chunksize=self.chunksize,
                low_memory=False,
            ):
                chunks.append(chunk)
            
        if not chunks:
            await logger.warning('Chunk vazia')
            return pd.DataFrame()
        
        return self.normalize_columns(
            pd.concat(chunks, ignore_index=True)
        )
    
    @staticmethod
    async def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:

        if df.empty:
            await logger.warning('Dataframe vazio')
            return df
        
        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r"\s+", "_", regex=True)
        )

        return df
    
    @staticmethod
    async def ensure_columns(
        df: pd.DataFrame,
        columns: list[str],
        default: Any = pd.NA,
    ) -> pd.DataFrame:
        
        for col in columns:

            if col not in df.columns:
                df[col] = default
        
        return df
    
    @staticmethod
    async def _normalize_object_columns(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        
        object_columns = df.select_dtypes(include=['object']).columns

        for col in object_columns:

            non_null = df[col].dropna()

            if non_null.empty:
                continue

            if len({type(x) for x in non_null}) > 1:
                df[col] = df[col].astype('string')
        
        return df
    
    async def _get_pipeline_config(self, key: str) -> dict:

        cfg = self.pipeline_config.get(key)

        if cfg is None:
            await logger.warning(f"Pipeline '{key}' não encontrado")
            raise ValueError(f"Pipeline '{key}' não encontrado")
        
        return cfg
    
    @staticmethod
    async def _get_csv_files(path: Path) -> list[Path]:

        if path.is_file():
            return [path]
        
        return sorted(path.glob("*.csv"))
    
    @staticmethod
    async def _duckdb_encoding(encoding: str) -> str:

        mapping = {
            "utf-8": "UTF-8",
            'utf-16': 'UTF-16',
            'latin-1': 'LATIN-1',
        }

        return mapping.get(
            encoding.lower(),
            encoding.upper(),
        )
    
    @staticmethod
    async def _sql_path_list(files: list[Path]) -> str:

        return(
            "["
            + ", ".join(
                f"'{str(file).replace('\'', '\'\'')}'"
                for file in files
            )
            + "]"
        )