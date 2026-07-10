import pandas as pd
from datetime import datetime

from infrastructure.files.file_manager import FileManager
from infrastructure.files.txt_manager import TxtManager
from infrastructure.dataframes.dataframe_manager import DataframeManager
from infrastructure.service.invoice_historic_invoce_fiscal import HistoricTransitFiscal
from core.logging.log import ExecutionLogger
from uuid import uuid4

"""
Fluxo de processamento doe dados de trânsito fiscal.

Este módulo contém a implementação responsável por orquestrar
todo o processo de atualização e acompanhamento dos dados de trânsito fiscal.

O fluxo executado consiste em:

- Validar a existência do arquivo de origem (TXT);
- Copiar o arquivo de origem para o destino (TXT);
- Converter o arquivo TXT para CSV;
- Carregar os dados do dia atualizados;
- Atualiza o histórico com  novos registros e resoluções;
- Recalcular os indicadores de atraso;
- Persistir o histórico atualizado;
- Retornar um resumo de execução.

A lógica de negócio relacionada à atualização dos dados é
delegada aos serviços de caso de uso(use cases), enquanto este módulo atua
como coordenador do processo.
"""

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="transit_fiscal",
        execution_id=execution_id
)


class TransitFiscal:
    """
    Orquestra o processo de atualização e acompanhamento dos dados de trânsito fiscal.

    Esta classe coordena todas as etapas necessárias para a 
    atualizaçã dos dados, utilizando componenetes da camada
    de infraestrutura e serviços pertencentes ao domínio da
    aplicação.
    """

    def __init__(
            self,
            origem_txt,
            destino_txt,
            destino_csv,
            historico_parquet
    ) -> None:
        """
        Inicializa o fluxo de processamento.

        Args:
            origem_txt (str): Caminho do arquivo de origem (TXT).
            destino_txt (str): Caminho do arquivo de destino (TXT).
            destino_csv (str): Caminho do arquivo de destino (CSV).
            historico_parquet (str): Caminho do arquivo de histórico (Parquet).
        """
        self.origem_txt = origem_txt
        self.destino_txt = destino_txt
        self.destino_csv = destino_csv
        self.historico_parquet = historico_parquet

        self.file_manager = FileManager()
        self.processor = TxtManager()
        self.repository = DataframeManager()


    async def execute(self):
        """
        Executa o fluxo completo de atualização dos dados de trânsito fiscal.

        O processamento realiza as seguintes etapas:

        1. Valida a existência do arquivo de origem (TXT);
        2. Copia o arquivo de origem para o destino (TXT);
        3. Converte o arquivo TXT para CSV;
        4. Carrega os dados do dia atualizados;
        5. Atualiza o histórico com novos registros e resoluções;
        6. Recalcula os indicadores de atraso;
        7. Persiste o histórico atualizado;
        8. Retorna um resumo de execução contendo a quantidade de novos registros.

        Returns:
            dict[str, int]:
                Dicionário contendo um resumo da execução,
                incluindo a quantidade de registros novos,
                resolvidos, pendentes e o total de registros
                presentes no histórico.
        """

        await self.file_manager._exists(self.origem_txt)

        await self.file_manager._copy(
            self.origem_txt,
            self.destino_txt
        )

        await self.processor.process(
            self.destino_txt,
            self.destino_csv
        )

        df_today = pd.read_csv(
            self.destino_csv,
            sep=";",
            dtype=str
        )

        df_today = (
            HistoricTransitFiscal.create_key(df_today)
        )

        df_historic = (
            await self.repository.load_parquet(self.historico_parquet)
        )

        if not df_historic.empty:
            df_historic = (
                HistoricTransitFiscal.create_key(df_historic)
            )

        (
            df_historic,
            qtd_new,
            qt_resolved
        ) = (
            HistoricTransitFiscal.update(
                df_today=df_today,
                df_historic=df_historic,
                date_execution=datetime.now().strftime("%d/%m/%Y")
            )
        )

        df_historic = (
            HistoricTransitFiscal.calculate_delay_days(df_historic)
        )

        await self.repository.save_parquet(
            self.historico_parquet,
            df_historic
        )

        return {
            "novos": int(qtd_new),
            "resolvidos": int(qt_resolved),
            "pendentes": int((
                df_historic['Status'] == "Pendente"
            ).sum()),
            "total": int(len(df_historic))
        }
