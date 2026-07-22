from __future__ import annotations

from dotenv import load_dotenv
import os
import pandas as pd

from settings.paths import ENV_PATH, PATH_BRONZE_CSV_ACERTOS, PATH_SILVER_CSV_ACERTOR

load_dotenv(dotenv_path=ENV_PATH)

from infrastructure.pcomm.client import PcommClient
from infrastructure.dataframes.dataframe_manager import DataframeManager
from models.schemas.acertos_model import ExecutePcommExtractAcertosModel

class ExecutePcommExtractAcertos:


    def execute_pcom(self):
        dataframe_manager = DataframeManager()


        with PcommClient() as pcom:

            pcom.send_key('[enter]')

            pcom.wait_ready()

            pcom.send_text('3')
            pcom.send_key('[enter]')

            pcom.wait_ready()

            pcom.send_key('S7DA')
            pcom.send_key('[enter]')

            pcom.wait_ready()

            pcom.send_text('211200d1')
            pcom.send_text('2', 10, 20)
            pcom.send_key('[enter]')
            
            pcom.wait_ready()

            pcom.send_text(text=os.getenv('PCOMM_EMP'), row=3, column=49)
            pcom.send_text(text=os.getenv('PCOMM_USER_ACERTO'), row=3,column=52)
            pcom.send_text(text=os.getenv('PCOMM_PASSWORD_ACERTO'), row=3,column=68)
            pcom.send_text('1', 6, 14)
            pcom.send_text('1', 22, 2)
            pcom.send_key('[enter]')

            reg = []

            while True:

                for row in range(6, 23): # linhas 6 até 22

                    codigo = pcom.wait_text(row, 6, 7).strip()
                    filial = pcom.wait_text(row, 14, 7).strip()
                    descricao = pcom.wait_text(row, 22, 26).strip()
                    tipo = pcom.wait_text(row, 52, 26).strip()

                    if codigo in ("", "VAZIO"):
                        continue

                    empresa, filial = filial.split()

                    reg.append({
                        "codigo": codigo,
                        "filial": filial,
                        "empresa": empresa,
                        "descricao": descricao,
                        "tipo_de_acerto": tipo
                    })

                    print(f'codigo: {codigo}, filial: {filial}, descricao: {descricao}, tipo_de_acerto: {tipo}')

                fim_da_relacao = pcom.wait_text(24, 2, 3)

                if fim_da_relacao == "FIM":
                    break
                
                    
                pcom.send_key('[pf8]')
                pcom.wait_ready()

        df = dataframe_manager.load_dataframe(reg)

        df = ExecutePcommExtractAcertosModel.validate_schema(df)

        dataframe_manager.save_csv(
            caminho=PATH_BRONZE_CSV_ACERTOS,
            df=df,
            encoding='utf-16'
        )








