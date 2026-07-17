from __future__ import annotations

import os
from dotenv import load_dotenv
from tqdm import tqdm

from settings.paths import ENV_PATH, EXTRACT_INVOICES_TXT_PATH, SAVE_CSV_INVOICES
import numpy as np  

load_dotenv(dotenv_path=ENV_PATH)

from infrastructure.dataframes.dataframe_manager import DataframeManager
from models.schemas.invoices_schema import InvoiceModel
from infrastructure.pcomm.client import PcommClient

class ExecutePcommExtractInvoices:

    def execute_pcom(self):

        dataframe_manager = DataframeManager()
        df = dataframe_manager.load_txt(
            caminho=EXTRACT_INVOICES_TXT_PATH,
            encoding='latin1'
        )

        df = InvoiceModel.transform(df)

        df_consulta = (
            df[
                [
                    'filial',
                    'nota_fiscal',
                    'mes_ano'
                ]
            ]
            .drop_duplicates(
                subset=['nota_fiscal']
            )
            .reset_index(drop=True)
        )

        df_consulta['situacao'] = None
        df_consulta['situacao_2'] = None
        df_consulta['sefaz'] = None

        print(df.head())

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

            pcom.send_text(text=os.getenv('PCOMM_EMP'), row=3, column=51)
            pcom.send_text(text=os.getenv('PCOMM_USER'), row=3,column=54)
            pcom.send_key('[tab]')
            pcom.send_text(text=os.getenv('PCOMM_PASSWORD'), row=3, column=70)
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

            for row in tqdm(
                df_consulta.itertuples(),
                total=len(df_consulta),
                desc='Consultando NFs',
                unit='NF'):

                data_saida = row.mes_ano
                filial = row.filial
                nf = row.nota_fiscal

                # Envia os dados para o pcom

                pcom.wait_ready()

                pcom.send_text(text='21', row=3, column=25)
                pcom.send_text(text=filial, row=3, column=33)
                pcom.send_text(text=nf,row=3,column=43)
                pcom.send_text(text=data_saida,row=3,column=64)
                pcom.send_key('[enter]')

                situacao = pcom.wait_text(row=7,column=8,length=14)
                sefaz = pcom.wait_text(row=7,column=61,length=10)
                situacao_2 = pcom.wait_text(row=7,column=22,length=26)

                df_consulta.at[row.Index, "situacao"] = situacao.strip()
                df_consulta.at[row.Index, "situacao_2"] = situacao_2.strip()
                df_consulta.at[row.Index, "sefaz"] = sefaz.strip()

                pcom.send_key('[enter]')

            df = df.merge(
                df_consulta[
                    [
                        'filial',
                        'nota_fiscal',
                        'situacao',
                        'situacao_2',
                        'sefaz'
                    ]
                ],
                on=[
                    'filial',
                    'nota_fiscal'
                ],
                how='left'
            )

            InvoiceModel.status_pcom(df=df)

            dataframe_manager.save_csv(
                caminho=SAVE_CSV_INVOICES,
                df=df,
                sep='\t'
            )

            # Criando histórico

            InvoiceModel.update_history(
                bronze_df=df,
                gold_path=...,
                nf_column='nota_fiscal',
                status_column='status_pcom'
            )