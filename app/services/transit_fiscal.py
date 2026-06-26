import pandas as pd
from datetime import datetime

from infrastructure.files.file_manager import FileManager
from infrastructure.files.txt_manager import TxtManager
from infrastructure.dataframes.dataframe_manager import DataframeManager
from domain.services.historic_trans_fiscal import HistoricTransitFiscal

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