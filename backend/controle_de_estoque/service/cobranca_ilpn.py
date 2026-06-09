import time

import pandas as pd

from config.paths import PATH_PRONTO_ENVIO
from repositories.excel_repository import DataFrameRepository
from email_ilpn import EmailService
from teams_service import TeamsService
from utils.dataframe_utils import clear_null

from utils.log import ExecutionLogger
from uuid import uuid4

"""
Serviço responsável pela execução das cobranças automáticas de ILPNs
pendentes.

Fluxo de execução:

1. Carrega ILPNs aptas para cobrança.
2. Agrupa registros por usuário e destinatários.
3. Identifica o maior nível de atraso.
4. Monta o conteúdo das notificações.
5. Envia mensagem para Teams.
6. Envia e-mail para os responsáveis.
7. Registra eventos de auditoria.

Integrações:
- ExcelRepository
- EmailService
- TeamsService
- ExecutionLogger
"""

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="3.11 - Status Wave + oLPN",
        execution_id=execution_id
)

class CobrancaService:
    """
    Serviço responsável pelo processamento e envio das cobranças.

    A classe centraliza todas as regras de negócio relacionadas
    ao acionamento de usuários, gestores e coordenadores para
    tratamento de ILPNs pendentes.

    Responsabilidades
    -----------------
    - Agrupar pendências.
    - Determinar severidade do atraso.
    - Gerar mensagens para Teams.
    - Gerar notificações por e-mail.
    - Registrar logs operacionais.
    """
    def __init__(
            self,
            repository: DataFrameRepository | None = None,
            email_service: EmailService | None = None,
            teams_service: TeamsService | None = None,
    ):
        self.repository = repository or DataFrameRepository()
        self.email_service = email_service or EmailService()
        self.teams_service = teams_service or TeamsService()

    @staticmethod
    async def obter_pior_atraso(df_grupo: pd.DataFrame) -> str:
        """
        Determina a faixa de atraso mais crítica
        presente no grupo analisado.

        Ordem de prioridade:

        1. Atrasado + de 10 dias
        2. Atrasado de 6 a 10 dias
        3. Atrasado de 2 a 5 dias
        4. Atraso Recente

        Parameters
        ----------
        df_grupo : pd.DataFrame
            Grupo de ILPNs do mesmo usuário.

        Returns
        -------
        str
            Faixa de atraso mais severa.
        """
        atrasos = df_grupo["Tempo de atraso"].unique()
        if "Atrasado + de 10 dias" in atrasos:
            return "Atrasado + de 10 dias"
        
        if "Atrasado de 6 a 10 dias" in atrasos:
            return "Atrasado de 6 a 10 dias"
        
        if "Atrasado de 2 a 5 dias" in atrasos:
            return "Atrasado de 2 a 5 dias"
        return "Atraso Recente"
    
    async def send_cobranca(self) -> None:
        """
        Executa o fluxo completo de cobrança.

        Processo:
        --------
        1. Carrega a base consolidada de ILPNs.
        2. Agrupa os registros por usuário.
        3. Calcula o pior atraso do grupo.
        4. Envia mensagem ao Teams.
        5. Envia e-mail aos responsáveis.
        6. Registra eventos de auditoria.

        Returns
        -------
        None
        """
        import asyncio
        logger.info("Iniciando a leitura das ILPNs atrasadas")

        df = await self.repository.read_csv(PATH_PRONTO_ENVIO)
        
        if df.empty:
            logger.warning("Nenhum registro de ILPN atrasada encontrada")
            return
        
        grupos = df.groupby(["Usuário", "Destinatários"])
        logger.info(f"Escrevendo {len(grupos)} blocos de mensagens via teams")

        try:
            for (usuario_origem, destinatarios), df_grupo in grupos:
                nome_coordenador = nome_gestor = nome_setor = "Não Localizado"

                try:
                    pior_atraso = await self.obter_pior_atraso(df_grupo)
                    fluxo = str(df_grupo["Fluxo aplicado"].iloc[0])
                    nome_coordenador = str(df_grupo["COORDENADOR"].iloc[0])
                    nome_gestor = str(df_grupo['GESTOR'].iloc[0])
                    nome_setor = str(df_grupo['SETOR_RH'].iloc[0])

                    await texto_ilpns_teams = self._montar_detalhes_teams(df_grupo, nome_coordenador, nome_gestor)
                    await self.teams_service.enviar_card_separado(nome_coordenador, nome_gestor, nome_setor, texto_ilpns_teams)
                    await asyncio.sleep(2)

                    enviado = self.email_service.send_email(
                        usuario_origem, destinatarios, df_grupo, pior_atraso, nome_setor, fluxo
                    )

                    if enviado:
                        logger.info(f"Email reportando ILPN atrasada enviada para: {nome_gestor} responsável pelo setor {nome_setor}")
                except Exception as e:
                    logger.error(f"Erro ao enviar email reportando ILPN atrasada para o gestor {nome_gestor} responsável pelo setor {nome_setor}\nDetalhe:\n{e}\nIndo para próxima execução")
                    continue

            logger.sucess('Os e-mails e mensagens via teams foram enviados')
        except Exception as e:
            logger.error(f"Não foi possível enviar os e-mails e mensagens via teams\nDetalhe:\n{e}")

    async def _montar_detalhes_teams(df_grupo: pd.DataFrame, nome_coordenador: str, nome_gestor: str) -> str:
        texto = ""
        
        for v, row in df_grupo.iterrows():
            texto += f"🔹 **DATA:** {row['Data ilpn´s']}\n\n"
            texto += f"🔹 **USUÁRIO:** {row['Usuário']}\n\n"
            texto += f"🔹 **ILPN:** {row['LPN']} | ⏳ **ATRASO:** {row['Tempo de atraso']}\n\n"
            texto += f"🔹 **REF 1:** {clear_null(row.get('Referencia 1'))}\n\n"
            texto += f"🔹 **REF 2:** {clear_null(row.get('Referencia 2'))}\n\n"
            texto += "------------------------------------------------\n\n"
        return texto + f"📌 **@{nome_coordenador}** (Coord.)\n\n📌 **@{nome_gestor}** (Gest.)\n\n"
    

    async def service_send_cobranca() -> None:
        CobrancaService().send_cobranca