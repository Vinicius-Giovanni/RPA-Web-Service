from __future__ import annotations

import pandas as pd

class ConversionService:
    """
    Serviço responsável por conversões de tipos de dados.
    """

    @staticmethod
    async def to_numeric(
        df: pd.DataFrame,
        column: str,
        decimal: str = ',',
        errors: str = 'coerce',
    ) -> pd.DataFrame:
        
        if column not in df.columns:
            return df
        
        series = df[column]

        if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):
            series = (
                series.astype('string')
                .str.replace(decimal, '.', regex=False)
                .str.strip()
            )

        df[column] = pd.to_numeric(
            series,
            errors=errors,
        )

        return df
    
    @staticmethod
    async def to_integer(
        df: pd.DataFrame,
        column: str,
    ) -> pd.DataFrame:
        
        if column not in df.columns:
            return df
        
        df[column] = (
            pd.to_numeric(df[column], errors='coerce')
            .astype('Int64')
        )

        return df
    
    @staticmethod
    async def to_float(
        df: pd.DataFrame,
        column: str,
    ) -> pd.DataFrame:
        
        if column not in df.columns:
            return df
        
        df[column] = (
            pd.to_numeric(df[column], errors='coerce')
            .astype('Float64')
        )

        return df