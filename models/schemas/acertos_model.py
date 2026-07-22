import pandas as pd

from settings.pipelines_config import ExecutePcommExtractAcertosModel_COLUMNS_TYPES, ExecutePcommExtractAcertosModel_REQUIRED_COLUMNS

class ExecutePcommExtractAcertosModel:

    _REQUIRED_COLUMNS = ExecutePcommExtractAcertosModel_REQUIRED_COLUMNS
    _COLUMNS_TYPES = ExecutePcommExtractAcertosModel_COLUMNS_TYPES

    @classmethod
    def _create_empty_schema(cls) -> pd.DataFrame:
        """
        Cria um DataFrame vazio contendo todas as colunas esperadas
        e seus respectivos tipos.
        """
        df = pd.DataFrame(columns=cls._REQUIRED_COLUMNS)
        return df.astype(cls._COLUMNS_TYPES)

    @classmethod
    def validate_schema(cls, df: pd.DataFrame) -> pd.DataFrame:

        # Primeira execução (df vazio e sem colunas)
        if df.empty and len(df.columns) == 0:
            return cls._create_empty_schema()

        # Remove colunas completamente vazia
        df = df.dropna(axis=1, how='all')

        # Remove espaços do nome das colunas
        df.columns = df.columns.str.strip()

        missing = set(cls._REQUIRED_COLUMNS) - set(df.columns)

        if missing:
            raise ValueError(
                f'Colunas obrigatórias ausentes: {sorted(missing)}'
            )
        
        # Mantém somente as colunas esperadas
        df = df[cls._REQUIRED_COLUMNS]

        # Garante os tipos
        df = df.astype(cls._COLUMNS_TYPES)

        return df