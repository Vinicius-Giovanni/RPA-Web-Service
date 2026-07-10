from __future__ import annotations

import pandas as pd

class DurationService:
    """
    Responsável pelos cálculos de duração da pipeline
    """

    @staticmethod
    async def calculation_duration(
        df: pd.DataFrame,
        start_column: str,
        end_column: str,
        output_column: str,
        absolute: bool = True,
    ) -> pd.DataFrame:
        
        if start_column not in df.columns or end_column not in df.columns:
            return df
        
        duration = (
            df[end_column] - df[start_column]
        ).df.total_seconds()

        if absolute:
             duration = duration.abs()

        df[output_column] = duration.astype('Int64')

        return df
    
    @staticmethod
    async def calculate_group_duration(
        df: pd.DataFrame,
        group_columns: list[str],
        datetime_column: str,
        output_column: str,
    ) -> pd.DataFrame:
        
        required = set(group_columns + [datetime_column])

        if not required.issubset(df.columns):
            return df
        
        duration = (
            df.groupby(group_columns)[datetime_column]
            .agg(['min', 'max'])
            .reset_index()
        )

        duration[output_column] = (
            duration['max'] - duration['min']
        ).dt.total_seconds()

        df = df.merge(
            duration[group_columns + [output_column]],
            on=group_columns,
            how='left',
        )

        df[output_column] = (
            df[output_column]
            .clip(lower=60)
            .astype("Int64")
        )

        return df