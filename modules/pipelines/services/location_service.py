import numpy as np
import pandas as pd

class LocationService:
    """
    Responsável pelas transformações relacionadas à localização de picking.
    """

    PAR_STREETS = {'CP1', 'CS1', 'P02', 'RO1', 'R02'}

    @classmethod
    async def split_location(
        cls,
        df: pd.DataFrame,
        source_column: str = 'local_de_picking',
    ) -> pd.DataFrame:
        
        if source_column not in df.columns:
            return df
        
        split = (
            df[source_column]
            .astype('string')
            .str.split('-', expand=True)
        )

        df['rua'] = split[0] if split.shape[1] > 0 else pd.NA
        df['endereco'] = split[1] if split.shape[1] > 1 else pd.NA
        df['nivel'] = split[2] if split.shape[1] > 2 else pd.NA

        df['rua'] = df['rua'].fillna('').str.strip()
        df['endereco'] = df['endereco'].fillna('').str.strip()
        df['nivel'] = df['nivel'].fillna('').str.strip()

        return df
    
    @classmethod
    async def classify_location(cls, df: pd.DataFrame) -> pd.DataFrame:

        required = {'rua', 'endereco'}

        if not required.issubset(df.columns):
            return df
        
        df['localizacao'] = np.where(
            (
                df['rua'].isin(cls.PAR_STREETS)
            ) | (
                df['endereco'].eq('PAR')
            ),
            "P.A.R",
            "Salao",
        )

        return df