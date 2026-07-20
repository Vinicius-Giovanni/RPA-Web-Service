from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
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
    def status_pcom(cls, df: pd.DataFrame) -> None:

        df['status_pcom'] = np.where(
            df['situacao_2'].str.contains('Confirma', na=False),
            "Resolvido",
            'Pendente'
        )

    @classmethod
    def transform(cls, df: pd.DataFrame) -> pd.DataFrame:

        cls.validate_schema(df)

        # Data Saída
        df['Data Saída'] = pd.to_datetime(
            df['Data Saída'],
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'
        )

        # Remove dadas NaN
        df = df.dropna(
            subset=['Data Saída']
        )

        # Criar formato esperado pelo PCOM: MM AAAA
        df['mes_ano'] = (
            df['Data Saída']
            .dt.strftime('%m%Y')
        )

        # Separar NF
        df[['filial', 'nota_fiscal']] = (
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

        df = df.reset_index(drop=True)

        return df
    
    @staticmethod
    def update_history(
        bronze_df: pd.DataFrame,
        gold_path: str | Path,
        nf_column: str = 'nota_fiscal',
        status_column: str = 'status_pcom'
    ) -> pd.DataFrame:
        """
        Atualiza o histórico de Notas Fiscais.

        Regras:
        1. Se não existir histórico, cria um novo.
        2. Apenas NFs novas são adicionadas.
        3. Apenas o status é atualizado.
        4. Uma NF Resolvida nunca volta para Pendente
        5. O hitórico é salvo em formato Parquet.
        """

        gold_path = Path(gold_path)
        gold_path.mkdir(parents=True, exist_ok=True)

        history_path = gold_path/ 'history.parquet'

        # Cria um df auxiliar contendo apenas NF + Status

        bronze_status = (
            bronze_df[[nf_column, status_column]]
            .drop_duplicates(subset=[nf_column])
            .copy()
        )

        print(bronze_df.columns)

        # Primeira execução
        if not history_path.exists():

            gold_path.parent.mkdir(parents=True, exist_ok=True)

            bronze_df.to_parquet(
                history_path,
                index=False
            )

            return bronze_df
        
        # Leitura de parquet gerado

        history_df = pd.read_parquet(history_path)

        # att de nfs resolvidas

        nfs_resolvidas = bronze_status.loc[
            bronze_status[status_column] == 'Resolvido',
            nf_column
        ]

        mask = (
            history_df[nf_column].isin(nfs_resolvidas)
            &
            (history_df[status_column] == 'Pendente')
        )

        history_df.loc[
            mask,
            status_column
        ] = 'Resolvido'

        # Descobre quais NFs ainda não existem na camada gold

        new_nfs = bronze_df.loc[
            ~bronze_df[nf_column].isin(
                history_df[nf_column]
            )
        ]

        # Add new NFs

        if not new_nfs.empty:

            history_df = pd.concat(
                [history_df, new_nfs],
                ignore_index=True
            )
        
        history_df.to_parquet(
            history_path,
            index=False
        )

        return history_df


