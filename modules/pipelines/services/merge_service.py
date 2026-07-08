from __future__ import annotations

import pandas as pd

class MergeService:
    """
    Serviço responsável por operações de junção entre DataFrames
    """

    @staticmethod
    async def left(
        left: pd.DataFrame,
        right: pd.DataFrame,
        on: str | list[str],
        suffixes: tuple[str, str] = ("", "_right"),
    ) -> pd.DataFrame:

        return left.merge(
            right,
            how='left',
            on=on,
            suffixes=suffixes,
            copy=False,
        )
    
    @staticmethod
    async def inner(
        left: pd.DataFrame,
        right: pd.DataFrame,
        on: str | list[str],
        suffixes: tuple[str, str] = ("", "_right"),
    ) -> pd.DataFrame:
        
        return left.merge(
            right,
            how='inner',
            on=on,
            suffixes=suffixes,
            copy=False,
        )
    
    @staticmethod
    async def right(
        left: pd.DataFrame,
        right: pd.DataFrame,
        on: str | list[str],
        suffixes: tuple[str, str] = ("", "_right"),
    ) -> pd.DataFrame:
        
        return left.merge(
            right,
            how='right',
            on=on,
            suffixes=suffixes,
            copy=False,
        )

    @staticmethod
    async def outer(
        left: pd.DataFrame,
        right: pd.DataFrame,
        on: str | list[str],
        suffixes: tuple[str, str] = ("", "_right"),
    ) -> pd.DataFrame:
        
        return left.merge(
            right,
            how='outer',
            on=on,
            suffixes=suffixes,
            copy=False,
        )
    
    @staticmethod
    async def deduplicate(
        df: pd.DataFrame,
        subset: str | list[str],
        keep: str = "first",
    ) -> pd.DataFrame:
        
        return df.drop_duplicates(
            subset=subset,
            keep=keep,
            ignore_index=True,
        )