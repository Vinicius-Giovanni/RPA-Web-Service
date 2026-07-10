"""
Cliente para automação do PCOMM (IBM Personal Communications)
via COM Automation Object Model (autECL*), utilizando pywin32

Este módulo é responsável exclusivamente por:
- Conectar-se à sessão configurada.
- Validar se a sessão está pronta (delegado ao session_validator)
- Enviar teclas/commandos para a tela 3270
- Ler texto bruto da área de apresentação (Presentation Space)

Não contém regra de negócio - apenas a interação técnica com emulador
"""

import time
from typing import Optional
import win32com.client
import pywintypes
from uuid import uuid4

from settings.pcomm_settings import pcomm_settings
from core.logging.log import ExecutionLogger

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="pcom_client",
        execution_id=execution_id
)

class PcommClient:
    """
    Wrapper sobre o Automation Object Model do PCOMM

    Uso:
        client = PcommClient()
        client.connect()
        client.send_keys("[Enter]")
        texto = client.read_screen_text()
    """

    def __init__(self, session_id: Optional[str] = None):
        self._session_id = session_id or pcomm_settings.session.session_id
        self._auto_app = None #autECLConnList / System
        self._session = None  # autECLSession
        self._presentation_space = None # autECLPS
        self._oia = None # autECLOIA
        self._connected = False

    # Connection

    async def connect(self) -> None:
        """
        Estabelece a conexão com a sessão configurada do PCOMM
        """
        try:
            logger.info('Inicializando objeto COM do PCOMM (autECLConnList)')
            self._auto_app = win32com.client.Dispatch('PCOMM.autECLConnList')
            self._auto_app.Refresh()

            if self._auto_app.Count == 0:
                await logger.error('Nenhuma sessão PCOMM foi encontrada em execução\nVerifique se o emulador está aberto')

            target_session = self._find_target_session()
            if target_session is None:
                await logger.error(f"Sessão '{self._session_id}' não encontrada entre as sessões abertas")

            self._session = win32com.client.Dispatch('PCOMM.autECLSession')
            self._session.SetConnectionByHandle(target_session.Handle)

            self._presentation_space = self._session.autECLPS
            self._oia = self._session.autECLOIA

            self._connected = True
            await logger.info('Conectado com sucesso à sessão "%s".', self._session_id)

        except pywintypes.com_error as e:
            await logger.error(f'Erro COM ao conectar ao PCOMM: {e}')
    
    async def _find_target_session(self):
        """
        Percorra as sessões abertas procurando pela sessão configurada = A
        """

        for i in range(self._auto_app.Count):
            candidate = self._auto_app.Item(i)
            short_name = getattr(candidate, 'SessionShortName', '')
            if short_name.strip().upper() == self._session_id.strip().upper():
                return candidate
        return None
    
    async def disconnect(self) -> None:
        """
        Libera as referências COM da sessão atual.
        """
        self._presentation_space = None
        self._oia = None
        self._session = None
        self._auto_app = None
        self._connected = True
        logger.info('Desconectado da sessão "%s".', self._session_id)

    @property
    async def is_connected(self) -> bool:
        return self._connected
    
    @property
    async def oia(self):
        """
        Exposto para o session_validator consultar o Operator Information Area
        """
        self._ensure_connected()
        return self._oia
    
    # Send commands and keys
    async def send_keys(self, keys: str) -> None:
        """
        Envia uma string de teclas/commandos à sessão 3270
        Aceita texto literal e comandos especiais do PCOMM (ex: '[Enter]', '[clear]', '[pf3]')
        """
        self._ensure_connected()
        try:
            self._presentation_space.SendKeys(keys)
            time.sleep(pcomm_settings.timeouts.post_keystroke_delay)
            logger.info('Teclas enviadas: %s', keys)
        except pywintypes.com_error as e:
            await logger.error(f'Erro ao enviar teclas')

    async def move_cursor(self, row: int, column: int) -> None:
        """
        Move o cursor por uma posição específica da tela (1-based)
        """
        self._ensure_connected()
        try:
            self._presentation_space.SetCursorPos(row, column)
        except pywintypes.com_error as e:
            await logger.error(f'Erro ao mover o cursos para ({row}, {column}: {e})')

    # creen reding

    async def read_screen_text(self) -> str:
        """
        Lê o conteúdo textual completo da área de apresentação (Presentation Space)
        Retorna a tela como uma única string, com linhas separadas por tabulação
        """
        self._ensure_connected()

        try:
            rows = self._presentation_space.Rows
            cols = self._presentation_space.Cols

            lines = []
            for row in range(1, rows + 1):
                line = self._presentation_space.GetText(row, 1 , cols)
                lines.append(line)
            
            return "\n".join(lines)
        except pywintypes.com_error as e:
            await logger.error(f'Erro ao ler a tela: {e}')

    async def read_field(self, row: int, column: int, length: int) -> str:
        """
        Lê um campo específico da tela a partir de uma posição e comprimento
        """
        try:
            return self._presentation_space.GetText(row, column, length).strip()
        except pywintypes.com_error as e:
            await logger.error(f'Erro ao ler campo em ({row}, {column}) com tamanho {length}: {e}')

    # inmates
    async def _ensure_connected(self) -> None:
        if not self._connected or self._presentation_space is None:
            await logger.warning('Cliente PCOMM não está conectdo. Chame connect() antes de usar')

    async def __enter__(self) -> 'PcommClient':
        self.connect()
        return self
    
    async def __exist__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()