"""
Responsável por validar explicitamente se a sessão A do PCOMM está aberta,
conectada e pronta para receber comandos (tela estabilizada, sem 'X System',
sem inibição de entrada)

Utiliza o Operator Information Area (OIA) exposto pelo PcommClient
"""

import time

from core.logging.log import ExecutionLogger
from uuid import uuid4

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="pcomm_session_validator",
        execution_id=execution_id
)

from infrastructure.pcomm.client import PcommClient
from settings.pcomm_settings import pcomm_settings

class SessionValidator:
    """
    Valida o estado da sessão 3270 utilizando o OIA (Operator Information Areaa)

    O OIA do PCOMM (autECLOIA) expõe constantes que indicam o estado atual
    da sessão, como:
        - XStatus: indica se há mensagem de espera/erro na tela (X System, X Clock etc...)
        - InputInhibited: Indica se a entrada de dados está bloqueada.
    """

    # Constantes do enum ECLOIAXStatus (definidas pela API COM do PCOMM)
    OIA_XTATUS_NOTINHIBITED = 0

    def __init__(self, client: PcommClient):
        self._client = client

    # validação de sessão aberta
    async def is_session_open(self) -> bool:
        """
        Verifica rapidamente se a sessão está conectada (sem esperar estabilização)
        """
        return self._client.is_connected
    
    async def ensure_session_open(self) -> None:
        """
        Garante que a sessão está conectada. Caso não esteja, tenta conectar.
        Levanta PcommConnectionError se a conexão falhar.
        """

        if not self._client.is_connected:
            await logger.warning('Sessão não conectada. Tentando conectar....')
            self._client.connect()

        if not self._client.is_connected:
            await logger.error('Não foi possível abrir a sessão do PCOMM configurada.')

    async def await_until_ready(self) -> None:
        """
        Aguarda até que a sessão esteja pronta para interação, verificando
        o OIA em intervalos definidos por pcomm_settings.timeouts.

        Levanta SessionNotReadyError se o timeout for atingido
        """

        self.ensure_session_open()

        timeout = pcomm_settings.timeouts.screen_ready_timeout
        interval = pcomm_settings.timeouts.polling_interval
        max_retries = pcomm_settings.timeouts.max_retries

        elapsed = 0.0
        attempts = 0

        while elapsed < timeout and attempts < max_retries:
            if self._is_ready():
                logger.info('Sessão pronta após %.2fs (%d tentativas).')
                return
            
            time.sleep(interval)
            elapsed +=interval
            attempts +=1

        raise await logger(f'Sessão "{pcomm_settings.session.session_id}" não ficou pronta após {timeout}s ({attempts} tentativas)')
    

    async def _is_ready(self) -> bool:
        """
        Checa o estado atual do OIA.
        Considera a sessão pronta quando não há inibição de entrada
        e não há indicador de espera do sistema (X Clock / X System)
        """
        try:
            oia = self._client.oia

            input_inhibited = oia.InputInhibited
            x_status = oia.XStatus

            is_not_inhibited = input_inhibited == self.OIA_XTATUS_NOTINHIBITED
            is_no_wait_indicator = x_status == self.OIA_XTATUS_NOTINHIBITED

            return is_not_inhibited and is_no_wait_indicator
        except Exception:
            logger.warning('Erro ao consultar OIA - sessão pode ter caído ou não está respondendo')
            return False
        
    # Validação explicita de sessão "A"
    async def validate_session_a(self) -> bool:
        """
        Validação explícita e nomeada, conforme requisito de negócio:
        confirma que a sessão configurada (por padrão 'A') está aberta e pronta

        Retorna True/False ao invés de lançar exceção, para uso em checagens
        rápidas (ex: health-check antes de iniciar um lote de processamento)
        """
        try:
            self.wait_until_ready()
            return True
        except Exception as e:
            logger.error(f"Falha na validação da sessão: %s", e)
            return False