from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

class DuckDBService:
    """
    Serviço responsável por toda interação com DuckDB
    """

    def __init__(self, database: str = ':memory'):
        self.database = database

    async def execute(self, sql: str) -> pd.DataFrame:
        with duckdb.connect(self.database) as conn:
            return conn.execute(sql).df()
        
    async def execute_file(self, sql_file: Path, **params) -> pd.DataFrame:
        query = sql_file.read_text(encoding='utf-8')

        for key, value in params.items():
            query = query.replace(f"{{{{{key}}}}}", str(value))

        return self.execute(query)
    
    async def register(self, name: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        with duckdb.connect(self.database) as conn:
            conn.register(name, dataframe)
            return conn.execute(f"SELECT * FROM {name}").df()
        
    async def query(
            self,
            dataframe: pd.DataFrame,
            sql: str,
            table_name: str = 'df',
    ) -> pd.DataFrame:
        with duckdb.connect(self.database) as conn:
            conn.register(table_name, dataframe)
            return conn.execute(sql).df()
        
    @staticmethod
    async def parquet_scan(files: list[Path]) -> str:
        escaped = [
            str(file).replace("'", "''")
            for file in files
        ]

        return "[" + ",".join(f"'{f}'" for f in escaped) + "]"