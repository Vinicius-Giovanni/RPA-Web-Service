from __future__ import annotations

from datetime import datetime

import pandas as pd

class DatetimeService:
    """
    Serviço responsável pelas tranformações relacionadas a datas e horas.
    """

    @staticmethod
    async def to_datetime(
        df: pd.DataFrame,
        columns: list[str],
        dayfirst: bool = True,
    ) -> pd.DataFrame:
        
        for column in columns:

            if columns not in df.columns:
                continue

            df[column] = pd.to_datetime(
                df[column],
                errors='coerce',
                dayfirst=dayfirst,
            )

        return df
    
    @staticmethod
    async def filter_last_months(
        df: pd.DataFrame,
        column: str,
        months: int = 6,
    ) -> pd.DataFrame:
        
        if column not in df.columns:
            return df
        
        limit = pd.Timestamp.now() - pd.DateOffset(months=months)

        return df.loc[df[column] >= limit]
    
    @staticmethod
    async def add_date_columns(
        df: pd.DataFrame,
        datetime_column: str,
    ) -> pd.DataFrame:
        
        if datetime_column not in df.columns:
            return df
        
        dt = df[datetime_column]

        df['data_criterio'] = dt.dt.date
        df['hora'] = dt.dt.strftime('%H:00:00')
        df['mes'] = dt.dt.month
        df['ano'] = dt.dt.year
        df['mes_ano'] = dt.dt.strftime("%m/%Y")

        return df
    
    @staticmethod
    async def add_execution_date(
        df: pd.DataFrame,
        column: str = 'data_execucao',
    ) -> pd.DataFrame:
        
        df[column] = datetime.now()

        return df
    
    @staticmethod
    async def remove_invalid_dates(
        df: pd.DataFrame,
        column: str,
    ) -> pd.DataFrame:
        
        if column not in df.columns:
            return df
        
        return df[df[column].notna()]
    
    @staticmethod
    async def sort_by_datetime(
        df: pd.DataFrame,
        column: str,
        ascending: bool = True,
    ) -> pd.DataFrame:
        
        if column not in df.columns:
            return df
        
        return df.sort_values(
            by=column,
            ascending=ascending,
            ignore_index=True,
        )