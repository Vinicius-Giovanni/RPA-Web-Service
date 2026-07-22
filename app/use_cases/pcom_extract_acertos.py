from __future__ import annotations

from dotenv import load_dotenv
import os
import pandas as pd
from tqdm import tqdm

from settings.paths import ENV_PATH, PATH_BRONZE_CSV_ACERTOS
from settings.pcomm_settings import CHECKPOINT

from pipe.pcomm.pipeline_acertos import AcertosPipeline

load_dotenv(dotenv_path=ENV_PATH)

from infrastructure.pcomm.client import PcommClient
from infrastructure.dataframes.dataframe_manager import DataframeManager
from models.schemas.acertos_model import ExecutePcommExtractAcertosModel

class ExecutePcommExtractAcertos:

    def reset_pcom(self) -> None:

        with PcommClient() as pcom:

            pcom.send_key('[pf9]')
            pcom.wait_ready()
            pcom.send_key('[pf3]')


    def routine_S7DA(self, dataframe_manager = DataframeManager()) -> pd.DataFrame:

        self.reset_pcom()

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

        return df

    def routine_S6CA(self, df: pd.DataFrame ,dataframe_manager = DataframeManager()) -> pd.DataFrame:

        self.reset_pcom()

        df_consulta = (
            df[
                [
                    'nota_fiscal',
                    'mes_emissao',
                    'ano_emissao',
                    'filial'
                ]
            ]
            .drop_duplicates(
                subset=['nota_fiscal']
            )
            .reset_index(drop=True)
        )

        print(df.head())

        with PcommClient() as pcom:

            pcom.send_key('[enter]')

            pcom.wait_ready()

            pcom.send_text('3')
            pcom.send_key('[enter]')

            pcom.wait_ready()

            pcom.send_key('S6CA')
            pcom.send_key('[enter]')

            pcom.wait_ready()

            pcom.send_text('211200d1')

            pcom.send_text('1', 5, 5)
            pcom.send_key('[enter]')

            pcom.wait_ready()

            pcom.send_text(text=os.getenv('PCOMM_EMP'), row=3, column=51)
            pcom.send_text(text=os.getenv('PCOMM_USER'), row=3,column=54)
            pcom.send_text(text=os.getenv('PCOMM_PASSWORD'), row=3,column=70)
            pcom.send_text('2', 8, 25)
            pcom.send_text('1', 21, 2)
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
                df.itertuples(),
                total=len(df_consulta),
                desc='Consultando NFS S6CA',
                unit='nota_fiscal'
            ):
                
                nf = row.nota_fiscal
                filial = row.filial
                mes = row.mes_emissao
                ano = row.ano_emissao

                # Envia os dados para o pcom

                pcom.send_text(text='21', row=3, column=25)
                pcom.send_text(text=filial, row=3, column=33)
                pcom.send_text(text=nf,row=3,column=43)
                pcom.send_text(text=mes,row=3,column=64)
                pcom.send_text(text=ano,row=3,column=67)
                pcom.send_key('[enter]')

                # extrair dados da dela
                # ex:
                # situacao = pcom.wait_text(row=7,column=8,length=14)

                # salvar no df
                #df_consulta.at[row.Index, 'nome_coluna'] = situacao.strip()

                # Checkpoint
                try:
                    if(row.Index + 1) % CHECKPOINT == 0:
                        dataframe_manager.save_csv(
                            caminho=...,
                            df=df_consulta,
                            sep=';'
                        )

                    print(f'Checkpoint salvo: {row.Index + 1} NFs processadas.')

                except Exception as e:
                    print(f'Erro ao salvar checkpoint: {e}')

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
                
            return df


    def activate_pipeline_bronze(self):

        dataframe_manager = DataframeManager()

        df = self.routine_S7DA(dataframe_manager=dataframe_manager)

        df = AcertosPipeline.column_descricao(df=df)

        df = self.routine_S6CA(df=df, dataframe_manager=dataframe_manager)

        dataframe_manager.save_csv(
            caminho=PATH_BRONZE_CSV_ACERTOS,
            df=df,
            encoding='utf-16',
            sep='\t'
        )

    def execute(self):

        self.activate_pipeline_bronze()










