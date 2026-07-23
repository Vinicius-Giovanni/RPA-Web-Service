from __future__ import annotations

from dotenv import load_dotenv
import os
import pandas as pd

from settings.paths import ENV_PATH, PATH_BRONZE_CSV_ACERTOS, PATH_SILVER_CSV_ACERTOR
from settings.pcomm_settings import CHECKPOINT

load_dotenv(dotenv_path=ENV_PATH)

from infrastructure.pcomm.client import PcommClient
from infrastructure.dataframes.dataframe_manager import DataframeManager
from pipe.pcomm.pipeline_acertos import AcertosPipeline
from infrastructure.pcomm.S7DA import RoutineS7DA
from infrastructure.pcomm.S6CA import RoutineS6CA
from infrastructure.pcomm.S7EA import RoutineS7EA

class ExecutePcommExtractAcertos:

    def routine_S7DA_extract_acertos(self, dataframe_manager = DataframeManager()) -> pd.DataFrame:
        # Extrai acertos

        with PcommClient() as pcom:

            RoutineS7DA.gotoroutine(pcom)

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

                    acerto = pcom.wait_text(row, 6, 7).strip()

                    if acerto in ("", "VAZIO"):
                        continue


                    reg.append({
                        "acerto": acerto,
                    })

                    print(f'acert: {acerto}')

                fim_da_relacao = pcom.wait_text(24, 2, 3)

                if fim_da_relacao == "FIM":
                    break
                
                    
                pcom.send_key('[pf8]')
                pcom.wait_ready()

        df = dataframe_manager.load_dataframe(reg)

        return df

    def routine_S7DA_extract_detail_acertos(self, df: pd.DataFrame ,dataframe_manager = DataframeManager()) -> pd.DataFrame:
        # Consulta Acerto

        df_consulta = (
            df[
                [
                    'acerto',
                ]
            ]
            .drop_duplicates(
                subset=['acerto']
            )
            .reset_index(drop=True)
        )

        print(df.head())

        with PcommClient() as pcom:

            RoutineS7DA.gotoroutine(pcom)

            pcom.send_text('2')
            pcom.send_key('[enter]')
            pcom.wait_ready()

            verif_S7UU = pcom.wait_text(1, 2, 4)

            if verif_S7UU != "S7UU":
                raise RuntimeError(
                    f'Verificação de verif_S7UU: {verif_S7UU} não retornou a tela esperada, encerrando tentativa.'
                )

            pcom.send_text(text=os.getenv('PCOMM_EMP'), row=3, column=49)
            pcom.send_text(text=os.getenv('PCOMM_USER_ACERTO'), row=3,column=52)
            pcom.send_text(text=os.getenv('PCOMM_PASSWORD_ACERTO'), row=3,column=68)

            pcom.send_text('12', 6, 14)
            pcom.send_text('1', 22, 2)
            pcom.send_key('[enter]')
            pcom.wait_ready()

            verif_S7UB = pcom.wait_text(1, 1, 5)

            if verif_S7UB != "S7UB":
                raise RuntimeError(
                    f'Verificação de verif_S7UB: {verif_S7UB} não retornou a tela esperada, encerrando tentativa.'
                )

            reg = []

            # Extração de dados
            for idx, row in enumerate(df_consulta.itertuples()):
                acerto = row.acerto

                pcom.send_text(acerto, 4, 18)
                pcom.send_key('[enter]')

                motivo = pcom.wait_text(5, 9, 68).strip()
                sku = pcom.wait_text(7, 18, 7).strip()
                desc_sku = pcom.wait_text(7, 26, 39).strip()
                qte = pcom.wait_text(7, 72, 6).strip()
                dt_inclusao = pcom.wait_text(8, 18, 10).strip()
                empresa = pcom.wait_text(11, 17, 2).strip()
                filial = pcom.wait_text(11, 20, 4).strip()
                nf = pcom.wait_text(11, 37, 8).strip()
                ano_emissao = pcom.wait_text(11, 74, 4)
                mes_emissao = pcom.wait_text(11, 71, 2)
                carga = pcom.wait_text(4, 60, 7)

                reg.append({
                    "acerto": acerto,
                    "motivo": motivo,
                    "sku": sku,
                    "desc_sku": desc_sku,
                    "qte": qte,
                    "dt_inclusao": dt_inclusao,
                    "empresa": empresa,
                    "filial": filial,
                    "nf": nf,
                    "ano_emissao": ano_emissao,
                    "mes_emissao": mes_emissao,
                    "carga": carga,
                })

                pcom.send_key('[enter]')
                pcom.wait_ready()

            df_acerto = dataframe_manager.load_dataframe(reg)

            df = df.merge(
                df_acerto,
                on='acerto',
                how='left'
            )
            return df

    def routine_S7EA_extract_detail_carga(self, df: pd.DataFrame, dataframe_manager = DataframeManager()) -> pd.DataFrame:
        # Consulta de carga

        df_consulta = (
            df[
                [
                    'carga',
                ]
            ]
            .drop_duplicates(
                subset=['carga']
            )
            .reset_index(drop=True)
        )

        print(df.head())

        with PcommClient() as pcom:

            RoutineS7EA.gotoroutine(pcom)

            pcom.send_text(text=os.getenv('PCOMM_EMP'), row=3, column=51)
            pcom.send_text(text=os.getenv('PCOMM_USER'), row=3,column=54)
            pcom.send_text(text=os.getenv('PCOMM_PASSWORD'), row=3,column=70)

            pcom.send_text('4', 8, 5)
            pcom.send_text('1', 20, 4)
            pcom.send_key('[enter]')

            pcom.wait_ready()

            verif_S7ED = pcom.wait_text(1, 2, 4)

            if verif_S7ED != "S7ED":
                raise RuntimeError(
                    f'Verificação de verif_S7ED: {verif_S7ED} não retornou a tela esperada, encerrando tentativa.'
                )

            pcom.send_text('1', 7, 27)
            pcom.send_key('[enter]')
            pcom.wait_ready()

            reg = []

            # Extração de dados
            for idx, row in enumerate(df_consulta.itertuples()):
                carga = row.carga

                pcom.send_text(carga, 3, 16)
                pcom.send_key('[enter]')
                pcom.wait_ready()

                print("Verificando carga:",carga)

                carga_nao_encontrada = pcom.wait_text(24, 7, 5)
                if carga_nao_encontrada == 'CARGA':
                    pcom.send_key('[pf3]')
                    pcom.wait_ready()
                    verif_S7ED = pcom.wait_text(1, 2, 4)

                    if verif_S7ED != "S7ED":
                        raise RuntimeError(
                            f'Verificação de verif_S7ED: {verif_S7ED} não retornou a tela esperada, encerrando tentativa.'
                        )
                    pcom.send_text('1', 7 , 27)
                    pcom.send_key('[enter]')
                    pcom.wait_ready()
                    continue

                transp = pcom.wait_text(8, 5, 40).strip()
                box = pcom.wait_text(3, 55, 4)

                reg.append({
                    "carga": carga,
                    "transp": transp,
                    "box": box
                })

                pcom.send_key('[enter]')
                pcom.wait_ready()


            df_carga = dataframe_manager.load_dataframe(reg)

            df = df.merge(
                df_carga,
                on='carga',
                how='left'
            )

            return df

    def routine_S6CA_validate_invoice(self, df: pd.DataFrame, dataframe_manager = DataframeManager):
        # Validação de NF

        df_consulta = (
            df[
                [
                    'nf',
                    'mes_emissao',
                    'ano_emissao',
                    'empresa',
                    'filial'
                ]
            ]
            .drop_duplicates(
                subset=['nf']
            )
            .reset_index(drop=True)
        )

        print(df.head())

        with PcommClient() as pcom:

            RoutineS6CA.gotoroutine(pcom)

            pcom.send_text('1', 5, 5)
            pcom.send_key('[enter]')
            pcom.wait_ready()


            verif_S6CF = pcom.wait_text(1, 2, 4)

            if verif_S6CF != "S6CF":
                raise RuntimeError(
                    f'Verificação de verif_S7ED: {verif_S6CF} não retornou a tela esperada, encerrando tentativa.'
                )

            pcom.send_text(text=os.getenv('PCOMM_EMP'), row=3, column=51)
            pcom.send_text(text=os.getenv('PCOMM_USER'), row=3,column=54)
            pcom.send_text(text=os.getenv('PCOMM_PASSWORD'), row=3,column=70)

            pcom.send_text('2', 8, 25)
            pcom.send_text('1', 21, 2)
            pcom.send_key('[enter]')
            pcom.wait_ready()

            verif_S6CFM02 = pcom.wait_text(1, 2, 7)

            if verif_S6CFM02 != "S6CFM02":
                raise RuntimeError(
                    f'Verificação de verif_S6CFM02: {verif_S6CFM02} não retornou a tela esperada, encerrando tentativa.'
                )

            notas_pendentes = pcom.wait_text(1, 41, 9)

            if notas_pendentes == 'PENDENTES':
                pcom.send_text('n', 16, 46)
                pcom.send_key('[enter]')
                pcom.wait_ready()

            verif_S6K1 = pcom.wait_text(1, 2, 7)

            if verif_S6K1 != "S6K1":
                raise RuntimeError(
                    f'Verificação de verif_S6K1: {verif_S6K1} não retornou a tela esperada, encerrando tentativa.'
                )

            pcom.send_text('1', 8, 17)
            pcom.send_key('[enter]')
            pcom.wait_ready()

            verif_S6AWM01 = pcom.wait_text(1, 2, 7)

            if verif_S6AWM01 != "S6AWM01":
                raise RuntimeError(
                    f'Verificação de verif_S6AWM01: {verif_S6AWM01} não retornou a tela esperada, encerrando tentativa.'
                )

            reg = []

            # Extração de dados
            for idx, row in enumerate(df_consulta.itertuples()):
                nf = row.nf
                mes_emissao = row.mes_emissao
                ano_emissao = row.ano_emissao
                empresa = row.empresa
                filial = row.filial

                pcom.send_text(empresa, 3, 25)
                pcom.send_text(filial, 3, 33)
                pcom.send_text(nf, 3, 43)
                pcom.send_text(mes_emissao, 3, 64)
                pcom.send_text(ano_emissao, 3, 67)

                pcom.send_key('[enter]')

                empresa_dst = pcom.wait_text(8, 21, 2)
                filial_dst = pcom.wait_text(8, 24, 4)

                reg.append({
                    "nf": nf,
                    "empresa_dst": empresa_dst,
                    'filial_dst': filial_dst

                })

                pcom.send_key('[enter]')
                pcom.wait_ready()


            df_nf = dataframe_manager.load_dataframe(reg)

            df = df.merge(
                df_nf,
                on='nf',
                how='left'
            )

            return df

    def activate_pipeline_bronze(self):

        dataframe_manager = DataframeManager()

        df_acerto = self.routine_S7DA_extract_acertos(dataframe_manager=dataframe_manager)

        df_detail_acerto = self.routine_S7DA_extract_detail_acertos(df=df_acerto, dataframe_manager=dataframe_manager)

        df_detail_carga = self.routine_S7EA_extract_detail_carga(df=df_detail_acerto, dataframe_manager=dataframe_manager)

        df_detail_nf = self.routine_S6CA_validate_invoice(df=df_detail_carga, dataframe_manager=dataframe_manager)

        dataframe_manager.save_csv(
            caminho=PATH_BRONZE_CSV_ACERTOS,
            df=df_detail_nf,
            encoding='utf-16',
            sep='\t'
        )

        df = AcertosPipeline.execute_pipeline()

        dataframe_manager.save_csv(
            caminho=PATH_SILVER_CSV_ACERTOR,
            df=df,
            encoding='utf-16',
            sep='\t'
        )

    def execute(self):

        self.activate_pipeline_bronze()










