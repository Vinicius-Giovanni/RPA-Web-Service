from __future__ import annotations
import asyncio
import pandas as pd
from uuid import uuid4

from modules.controle_de_estoque.repositories.excel_repository import DataFrameRepository
from modules.controle_de_estoque.service.email_ilpn import EmailService
from modules.controle_de_estoque.service.teams_service import TeamsService
from settings.paths import PATH_PRONTO_ENVIO
from utils.dataframe_utils import limpar_nan
from utils.log import ExecutionLogger


execution_id = str(uuid4())
logger = ExecutionLogger(automation_name="3.11 - Status Wave + oLPN", execution_id=execution_id)

class CobrancaService:
    def __init__(self, repository: DataFrameRepository | None=None, email_service: EmailService | None=None, teams_service: TeamsService | None=None) -> None:
        self.repository = repository or DataFrameRepository()
        self.email_service = email_service or EmailService()
        self.teams_service = teams_service or TeamsService()
    
    @staticmethod
    def obter_pior_atraso(df_grupo: pd.DataFrame) -> str:
        atrasos = set(df_grupo["Tempo de atraso"].astype(str).unique())
        prioridades = (
            "Atrasado + de 10 dias",
            "Atrasado de 6 a 10 dias",
            "Atrasado de 2 a 5 dias",
        )

        return next((atraso for atraso in prioridades if atraso in atrasos), "Atraso Recente")
    
    async def send_cobranca(self) -> None:
        await logger.info("Iniciando a leitura das ILPNs atrasadas")
        df = await self.repository.read_excel(PATH_PRONTO_ENVIO)

        if df.empty:
            await logger.warning("Nenhum registro de ILPN atrasada encontrada")
            return
    
        grupos = df.groupby(["Usuário", "Destinatários"])
        await logger.info(f"Escrevendo {len(grupos)} blocos de mensagens via Teams")

        for (usuario_origem, destinatarios), df_grupo in grupos:
            nome_coordenador = nome_gestor = nome_setor = "Não Localizado"

            try:
                pior_atraso = self.obter_pior_atraso(df_grupo)
                fluxo = str(df_grupo["Fluxo aplicado"].iloc[0])
                nome_coordenador = str(df_grupo["COORDENADOR"].iloc[0])
                nome_gestor = str(df_grupo["GESTO"].iloc[0])
                nome_setor str(df_grupo["SETOR_RH"].iloc[0])
                texto_ilpns_teams = self._montar_detalhes_teams(df_grupo, nome_coordenador, nome_gestor)

                self.teams_service.enviar_card_separado(nome_coordenador, nome_gestor, nome_setor, texto_ilpns_teams)
                await asyncio.sleep(2)

                enviado = self.email_service.enviar_email(
                    str(usuario_origem), str(destinatarios), df_grupo, pior_atraso, nome_setor, fluxo
                )

                if enviado:
                    await logger.info(f"Email reportando ILPN atrasada enviado para {nome_gestor}, responsável pelo setor {nome_setor}")

            except Exception as e:
                await logger.error(
                    f"Erro ao enviar cobrança para {nome_gestor}/{nome_setor}. Detalhe: {e}. Indo para próxima execução"
                )
        await logger.sucess("Os e-mails e mensagens via teams foram enviados")

    @staticmethod
    def _montar_detalhes_teams(df_grupo: pd.DataFrame, nome_coordenador: str, nome_gestor: str) -> str:
        linhas: list[str] = []
        for _, row in df_grupo.iterrows():
            linhas.extend(
                [
                    f"🔹 **DATA:** {row['Data ilpn´s']}\n",
                    f"🔹 **USUÁRIO:** {row['Usuário']}\n",
                    f"🔹 **ILPN:** {row['LPN']} | ⏳ **ATRASO:** {row['Tempo de atraso']}\n",
                    f"🔹 **REF 1:** {limpar_nan(row.get('Referencia 1'))}\n",
                    f"🔹 **REF 2:** {limpar_nan(row.get('Referencia 2'))}\n",
                    "------------------------------------------------\n", 
                ]
            )
        
        linhas.append(f"📌 **@{nome_coordenador}** (Coord.)\n📌 **@{nome_gestor}** (Gest.)\n")
        return "\n".join(linhas)
    
    async def service_send_cobranca() -> None:
        await CobrancaService().send_cobranca()