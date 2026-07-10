from __future__ import annotations

import pandas as pd

class SectorService:
    """
    Responsável pela classificação de setores.

    Todas as regras de negócio relacionadas ao setor devem ficar
    centralizaas nesta classe.
    """

    def __init__(self, sector_rules: dict[str, str]):
        self.__sector_rules = sector_rules

    async def classify(
            self,
            df: pd.DataFrame,
            source_colummn: str,
            target_column: str = 'setor',
            default: str = 'OUTROS',
    ) -> pd.DataFrame:
        
        if source_colummn not in df.columns:
            return df
        
        values = (
            df[source_colummn]
            .fillna('')
            .astype(str)
            .str.upper()
            .str.strip()
        )

        df[target_column] = values.map(self.__sector_rules).fillna(default)

        return df
    
    async def classify_by_prefix(
            self,
            df: pd.DataFrame,
            source_column: str,
            prefix_rules: dict[str, str],
            target_culumn: str = 'setor',
            default: str = 'OUTROS',
    ) -> pd.DataFrame:
        
        if source_column not in df.columns:
            return df
        
        values = (
            df[source_column]
            .fillna('')
            .astype(str)
            .str.upper()
            .str.strip()
        )

        df[target_culumn] = default

        for prefix, sector in prefix_rules.items():
            mask = values.str.startswith(prefix)
            df.loc[mask, target_culumn] = sector

        return df