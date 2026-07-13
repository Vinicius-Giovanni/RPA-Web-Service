from __future__ import annotations

import os
from dotenv import load_dotenv

from settings.paths import ENV_PATH, EXTRACT_INVOICES_TXT_PATH
from pathlib import Path

load_dotenv(dotenv_path=ENV_PATH)

from infrastructure.dataframes.dataframe_manager import DataframeManager
from models.schemas.invoices_schema import InvoiceModel
from infrastructure.pcomm.client import PcommClient

class ExecutePcommExtractInvoices:

    def execute_pcom(self):

        dataframe_manager = DataframeManager()

        with PcommClient() as pcom:

            pcom.send_key('[enter]')

            pcom.wait_ready()

            pcom.send_text('3')
            pcom.send_key('[enter]')

            pcom.send_text('S6CA')
            pcom.send_key('[enter]')

            pcom.wait_ready()

            pcom.send_text('211200d1')
            pcom.send_key('[enter]')

            pcom.wait_ready()

            pcom.send_text(os.getenv('PCOMM_EMP'))
            pcom.send_text(os.getenv('PCOMM_USER'))
            pcom.send_key('[tab]')
            pcom.send_text(os.getenv('PCOMM_PASSWORD'))
            pcom.send_key('[tab]')

            pcom.send_text('2')
            pcom.send_key('[tab]')
            pcom.send_text('1')
            pcom.send_key('[enter]')

            pcom.wait_ready()

            pendencias = pcom.read(16, 33, 12)

            if "S=Sim/N=Nao:" in pendencias:
                pcom.send_text(text='N', row=16, column=46)
                pcom.send_key('[enter]')

            pcom.wait_ready()

            pcom.send_text('1')
            pcom.send_key('[enter]')
            pcom.wait_ready()

            df = dataframe_manager.load_txt(
                caminho=EXTRACT_INVOICES_TXT_PATH,
                encoding='latin1',
                columns=['Data Saída', 'NF']
            )

            print(df.head())

            df = InvoiceModel.transform(df)

            print(df.head())

            for _, row in df.iterrows():

                data_saida







        







