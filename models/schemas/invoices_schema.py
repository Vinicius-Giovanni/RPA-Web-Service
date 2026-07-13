from datetime import datetime
import pandas as pd

class InvoiceModel:
    REQUIRED_COLUMNS = [
        'Data Saída',
        'NF'
    ]

    @classmethod
    def validate_schema(cls, df: pd.DataFrame) -> bool:

        missing_columns = set(cls.REQUIRED_COLUMNS) - set(df.columns)

        if missing_columns:
            raise ValueError(
                f'Colunas obrigatórias ausentes: {missing_columns}'
            )
        
        return True
    
    @classmethod
    def transform(cls, df: pd.DataFrame) -> pd.DataFrame:

        cls.validate_schema(df)

        # Data Saída
        df['Data Saída'] = pd.to_datetime(
            df['Data Saída'],
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'
        )

        # Criar formato esperado pelo PCOM: MM AAAA
        df['mes_ano'] = (
            df['Data Saída']
            .dt.strftime('%m %Y')
        )

        # Separar NF
        df[['filial', 'nota fiscal']] = (
            df['NF']
            .str.extract(
                r"(\d+)\s*-\s*(\d+)"
            )
        )

        # Converter filial
        df['filial'] = (
            df['filial']
            .astype(int)
        )

        return df

