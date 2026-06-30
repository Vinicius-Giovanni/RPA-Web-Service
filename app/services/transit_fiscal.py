import pandas as pd
from datetime import datetime

from infrastructure.files.file_manager import FileManager
from infrastructure.files.txt_manager import TxtManager
from infrastructure.dataframes.dataframe_manager import DataframeManager
from domain.services.historic_trans_fiscal import HistoricTransitFiscal
from utils.log import ExecutionLogger
from uuid import uuid4

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="transit_fiscal",
        execution_id=execution_id
)


class TransitFiscal:

    def __init__(
            self,
            origem_txt,
            destino_txt,
            destino_csv,
            historico_csv
    ):
        self.origem_txt = origem_txt
        self.destino_txt = destino_txt
        self.destino_csv = destino_csv
        self.historico_csv = historico_csv

        self.file_manager = FileManager()
        self.processor = TxtManager()
        self.repository = DataframeManager()


    async def execute(self):

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
            await self.repository.load_csv(self.historico_csv)
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
            HistoricTransitFiscal.calcular_atrasos(df_historic)
        )

        await self.repository.save_csv(
            self.historico_csv,
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
