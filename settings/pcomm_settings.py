"""
Configurações centrais para a automação do PCOMM (IBM 3270 - Personal Communications)
Define parâmetros de sessão, timeouts e constantes utilizadas pela camada de infraestrutura.
"""

from dataclasses import dataclass

from pathlib import Path

@dataclass(frozen=True)
class PcommSessionSettings:
    """
    Configurações da sessão do PCOMM a ser automatizada
    """

    session_id: str = 'A'

    window_title_pattern: str = 'Session A - [24 x 80]'

    # Caminho do executável do PCOMM, caso seja necessário abrir automaticamente
    pcomm_executable_path: Path = Path(r"")

    # Caminho do arquivo de workspace/sessão (.ws) do PCOMM
    workspace_file_path: Path = Path(r'')

@dataclass(frozen=True)
class PcommTimeoutSettings:
    """
    Timeout utilizados nas interações com o emulador
    """

    # Tempo max de espera para sessão abrir/conectar
    connect_timeout: float = 15.0

    # Tempo max de espera pela estabilização da tela (OIA 'pronto')
    screen_ready_timeout: float = 10.0

    # intervalo entre tentativa de polling de tela
    polling_interval: float = 0.3

    # Tempo de espera padrão após envio de uma tecla/commando
    post_keystroke_delay: float = 0.5

    # Nº max de tentativasao validar se a sessão está pronta
    max_retries: int = 5

@dataclass(frozen=True)
class PcommAutomationSettings:
    """
    Agrupador geral de configurações usadas pelo client PCOMM.
    """

    session: PcommSessionSettings = PcommSessionSettings()
    timeouts: PcommTimeoutSettings = PcommTimeoutSettings()

    # Nome da classe da janela do PCOMM (usada em buscas via win32gui.FindWindow)
    window_class_name: str = 'PS_Session'

    # Habilita logs detalhados de automação (útil para debug de macros/HLLAPI)
    debug_mode: bool = False


# instância única (singleon simples) para uso direto nos demais módulos
pcomm_settings = PcommAutomationSettings()

CHECKPOINT = 1000 # A cada 1000nfs consultadas, ele faz um save para não perdermos o progresso
