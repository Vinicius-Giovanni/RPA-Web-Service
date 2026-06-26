import pandas as pd
from datetime import datetime
from utils.log import ExecutionLogger
from uuid import uuid4

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="3.11 - Status Wave + oLPN",
        execution_id=execution_id
)

class HistoricTransitFiscal:

    @staticmethod
    async def create_key(df_for_transit_fiscal):

        df_for_transit_fiscal["CHAVE_UNICA"] =(
            df_for_transit_fiscal["FILIAL_EMI"].fillna("").str.strip()
            + "_"
            + df_for_transit_fiscal["NOTA"].fillna("").str.strip()
            + "_"
            + df_for_transit_fiscal["SERIE"].fillna("").str.strip()
        )

        return df_for_transit_fiscal
    
    @staticmethod
    async def update(
        df_today: pd.DataFrame,
        df_historic: pd.DataFrame,
        date_execution: str
    ):
        
        qtd_new = 0
        qtd_resolved = 0

        if df_historic.empty:

            df_historic = df_today.copy()

            df_historic["Status"] = "Pendente"
            df_historic['Data Entrada'] = date_execution
            df_historic['Data Resolução'] = ""

            return (
                df_historic,
                len(df_historic),
                0
            )
        
        keys_today = set(
            df_today['CHAVE_UNICA']
        )

        keys_historic = set(
            df_historic["CHAVE_UNICA"]
        )

        resolved = (
            (df_historic['Status'] == 'Pendente')
            &
            (
                ~df_historic['CHAVE_UNICA'].isin(keys_today)
            )
        )

        qtd_resolved = resolved.sum()

        df_historic.loc[
            resolved,
            'Status'
        ] = 'Resolvido'

        df_historic.loc[
            resolved,
            'Data Resolução'
        ] = date_execution

        df_new = df_today[
            ~df_today["CHAVE_UNICA"].isin(keys_historic)
        ].copy()

        qtd_new = len(df_today)

        if not df_new.empty:

            df_new['Status'] = 'Pendente'
            df_new['Data Entrada'] = date_execution
            df_new['Data Resolução'] = ""

            df_historic = pd.concat(
                [df_historic, df_new],
                ignore_index=True
            )

        return (
            df_historic,
            qtd_new,
            qtd_resolved
        )
    
    @staticmethod
    def calcular_atrasos(
        df: pd.DataFrame
    ):
        
        today = pd.Timestamp.today()

        df['DT_EMI_DT'] = pd.to_datetime(
            df['DT_EMI'],
            errors='coerce'
        )

        pending = (
            df['status'] == 'Pendente'
        )

        resolved = (
            df['status'] == 'Resolvido'
        )

        df.loc[
            pending,
            'Dias em Atraso'
        ] = (
            today
            - df.loc[
                pending,
                "DT_EMI_DT"
            ]
        ).dt.days

        date_resolved = pd.to_datetime(
            df['Data Resolução'],
            format="%d/%m/%Y",
            errors='coerce'
        )

        df.loc[
            resolved,
            "Dias em Atraso"
        ] = (
            date_resolved
            - df['DT_EMI_DT']
        ).dt.days

        df.drop(
            columns=['DT_EMI_DT'],
            inplce=True
        )

        return df
