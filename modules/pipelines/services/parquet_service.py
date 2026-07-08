from __future__ import annotations

from pathlib import Path
import pandas as pd

class ParquetService:
    """
    Serwviço responsável pelas operações com arquivos Parquet.
    """

    @staticmethod
    async def read(
        folder: Path,
        columns: list[str] | None = None,
    ) -> pd.DataFrame:
        
        files = sorted(folder.rglob('*.parquet'))

        if not files:
            return pd.DataFrame()
        
        dfs = []

        for file in files:
            try:
                dfs.append(
                    pd.read_parquet(
                        file,
                        columns=columns
                    )
                )
            except Exception:
                continue
        
        if not dfs:
            return pd.DataFrame()
        
        return pd.concat(
            dfs,
            ignore_index=True,
        )
    
    @staticmethod
    async def write(
        df: pd.DataFrame,
        output_file: Path,
        compression: str = 'zstd',
    ) -> None:
        
        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_parquet(
            output_file,
            index=False,
            compression=compression,
        )
    
    @staticmethod
    async def exists(folder: Path) -> bool:
        return any(folder.rglob('*.parquet'))
    
    @staticmethod
    async def list_files(folder: Path) -> list[Path]:
        return sorted(folder.rglob('*.parquet'))
    
    @staticmethod
    async def count_rows(folder: Path) -> int:

        total = 0

        for file in folder.rglob('*.parquet'):
            total += len(pd.read_parquet(file, columns=[]))

        return total