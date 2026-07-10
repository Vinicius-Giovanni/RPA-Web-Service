import pandas as pd
from datetime import datetime
from core.logging.log import ExecutionLogger
from uuid import uuid4

"""
Serviços de domínio para manutenção do histórico de trânsito fiscal.

Este módulo contém as regras de negócio responsável pela
consolidação do historico de pendências de trânsito fiscal.

As funcionalidades implementadas incluem:

- Geração de chave única de identificação dos registros;
- Atualização do histórico com novos e resolvidos;
- Cálculo dos dias de atraso das pendências.

Todas as regras presentes neste módulo são independentes de
mecanismos de persistência, interface gráfica ou frameworks,
pertecendo exclusivamente ao domínio da aplicação.
"""

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="historic_trans_fiscal",
        execution_id=execution_id
)

class HistoricTransitFiscal:
    """
    Serviço de domínio responsável pelo processamento do
    histórico de trânsito fiscal.

    Esta classe encapsula regras de negócio utilizadas
    para consolidar o histórico de pendências, identificar
    novos registros, marcar registros resolvidos e calcular
    os indicadores de atraso.
    """

    @staticmethod
    def create_key(df_for_transit_fiscal):
        """
        Cria a chave única de identificação dos registros.

        A chave é formada pela concatenação dos campos de
        filial emissora, número da nota e série da nota,
        permitindo identificar unicamente cada documento
        fiscal.

        Args:
            df_for_transit_fiscal:
                DataFrame contendo os registros de trânsito
                fiscal.

        Returns:
            pd.DataFrame:
                DataFrame com a coluna ``CHAVE_UNICA``
                adicionada.
        """

        df_for_transit_fiscal["CHAVE_UNICA"] =(
            df_for_transit_fiscal["FILIAL_EMI"].fillna("").str.strip()
            + "_"
            + df_for_transit_fiscal["NOTA"].fillna("").str.strip()
            + "_"
            + df_for_transit_fiscal["SERIE"].fillna("").str.strip()
        )

        return df_for_transit_fiscal
    
    @staticmethod
    def update(
        df_today: pd.DataFrame,
        df_historic: pd.DataFrame,
        date_execution: str
    ):
        """
        Atualiza o histórico de trânsito fiscal.

        O processamento realiza as seguintes operações:

        - Identifica novos registros;
        - Identifica pendências resolvidas;
        - Atualiza os status do histórico;
        - Insere novos registros no histório.

        Args:
            df_today:
                DataFrame contendo os registros da execução
                atual.
            
                df_historic:
                    Histórico consolidado das execuções
                    anteriores.

                date_execution:
                    Data de execução utilizada para registrar a
                    entrada e resolução das pendências.

        Returns:
            tuple[pd.DaFrame, int, int]:
                Tupla contendo:

                - O histórico atualizado;
                - A quantidade de novos registros;
                - A quantidade de registros resolvidos.
        """
        
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

        qtd_resolved = int(resolved.sum())

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

        qtd_new = len(df_new)

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
    def calculate_delay_days(
        df: pd.DataFrame
    ):
        """
        Calcula os dias de atraso de cada registro

        Para registros pendentes, o atraso é calculado entre
        a data de emissão e a data atual.

        Para registros resolvidos, o atraso corresponde ao
        período entre a data de emissão e a data de
        resolução.

        Args:
            df:
                Histórico consolidado contendo os registros
                de trânsito fiscal.

        Returns:
            pd.DataFrame:
                DataFrame atualizado com a coluna
                ``Dias em Atraso`` recalculada.

        """
        
        today = pd.Timestamp.today()

        df['DT_EMI_DT'] = pd.to_datetime(
            df['DT_EMI'],
            errors='coerce'
        )

        df['Dias em Atraso'] = pd.to_numeric(
            df.get('Dias em Atraso'),
            errors='coerce'
        )

        pending = (
            df['Status'] == 'Pendente'
        )

        resolved = (
            df['Status'] == 'Resolvido'
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
            date_resolved.loc[resolved]
            - df.loc[resolved, 'DT_EMI_DT']
        ).dt.days

        df.drop(
            columns=['DT_EMI_DT'],
            inplace=True
        )

        return df
