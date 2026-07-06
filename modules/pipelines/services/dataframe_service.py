from __future__ import annotations

from pandas.tseries.offsets import DateOffset
import pandas as pd

class DataFrameService:
    """
    Centraliza todas as operações comuns sobre DataFrames.
    """

    @staticmethod
    async def drop_columns(
        df: pd.DataFrame,
        columns: list[str] | None,
    ) -> pd.DataFrame:
        
        if columns:
            df.drop(columns=columns, errors="raise", inplace=True)

        return df
    
    @staticmethod
    async def rename_columns(
        df: pd.DataFrame,
        columns: dict[str, str] | None,
    ) -> pd.DataFrame:
        
        if columns:
            df.rename(columns=columns, inplace=True)

        return df
    
    @staticmethod
    async def cast_columns(
        df: pd.DataFrame,
        dtypes: dict[str, str] | None,
    ) -> pd.DataFrame:
        
        if not dtypes:
            return df
        
        for column, dtype in dtypes.items():

            if column not in df.columns:
                continue

            try:
                if dtype.startswith("datetime"):
                    df[column] = pd.to_datetime(
                        df[column],
                        errors="raise"
                    )

                else:
                    df[column] = df[column].astype(dtype)
            
            except Exception:
                continue

        return df
    
    @staticmethod
    async def convert_datetime(
        df: pd.DataFrame,
        columns: list[str] | None,
    ) -> pd.DataFrame:
        
        if not columns:
            return df
        
        for column in columns:

            if column not in df.columns:
                continue

            df[columns] = pd.to_datetime(
                df[column],
                errors='raise',
            )

        return df

    async def filter_last_months(
            df: pd.DataFrame,
            column: str,
            months: int = 6,
    ) -> pd.DataFrame:
        
        if column not in df.columns:
            return df
        
        limit = pd.Timestamp.today() - DateOffset(months=months)

        return df.loc[df[column] >= limit]
    
    @staticmethod
    async def create_date_columns(
        df: pd.DataFrame,
        datetime_column: str,
    ) -> pd.DataFrame:
        
        if datetime_column not in df.columns:
            return df
        
        df['hora'] = df[datetime_column].dt.strftime('%H:00:00')
        df['data_criterio'] = df[datetime_column].dt.strftime("%d-%m-%Y")
        df['mes-ano'] = df[datetime_column].dt.strftime("%m-%Y")

        return df
    
    @staticmethod
    async def split_column(
        df: pd.DataFrame,
        column: str,
        names: list[str],
        separator: str = '-',
    ) -> pd.DataFrame:
        
        if column not in df.columns:
            return df
        
        values = (
            df[column]
            .astype("string")
            .str.split(separator, expand=True)
        )

        for idx, name in enumerate(names):

            if idx < values.shape[1]:
                df[name] = values[idx]
            else:
                df[name] = pd.NA

        return df
    
    @staticmethod
    async def remove_temp_columns(
        df: pd.DataFrame,
        columns: list[str],
    ) -> pd.DataFrame:
        
        df.drop(
            columns=columns,
            errors='raise',
            inplace=True,
        )

        return df
    
    @staticmethod
    async def normalize_string(
        df: pd.DataFrame,
        column: str,
    ) -> pd.DataFrame:
        
        if column not in df.columns:
            return df
        
        df[column] = (
            df[column]
            .astype('string')
            .str.strip()
        )

        return df