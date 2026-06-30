from __future__ import annotations
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r'C:/Users/2960006959/Desktop/project/RPA-Web-Service')
ENV_PATH = BASE_DIR / ".env"
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
LOG_EXECUTIONS = LOG_DIR / 'executions'

TODAY = datetime.now()

# Dados -- ALterar depois
PATH_ILPNS = DATA_DIR / "ILPNs.xlsx"
PATH_PIX = DATA_DIR / "PIX.xlsx"
PATH_COLABORADORES = DATA_DIR / "colaboradores.xlsx"
PATH_ILPNS_PENDENTES = DATA_DIR / "ILPNs_pendentes.xlsx"
PATH_PRONTO_ENVIO = DATA_DIR / "ILPNs_pendentes_pronta_entrega.xlsx"
PATH_HISTORICO_PBI = DATA_DIR / "historico_pbi.xlsx"
PATH_LOG_EXECUCAO = LOG_EXECUTIONS / "controle_estoque.jsonl"

# Transito Fiscal ==============================
PENDING_FISCAL_ORIGEM_TXT = Path(f'//nascds.viavarejo.com.br/cd1200/share2/ger_oper1200/Controles_Logisticos/Controle_NF_transito/REL_MERC_N_RECEBIDA_{TODAY.strftime("%Y%m%d")}txt')
PENDING_FISCAL_DESTINO_TXT = Path(f'C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES/REL_MERC_N_RECEBIDA/REL_MERC_N_RECEBIDA_{TODAY.strftime("%Y%m%d")}txt')
PENDING_FISCAL_DESTINO_CSV = Path(f'C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES/REL_MERC_N_RECEBIDA/REL_MERC_N_RECEBIDA_{TODAY.strftime("%Y%m%d")}.csv')
PENDING_FISCAL_HISTORICO_CSV = Path(f'C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES/REL_MERC_N_RECEBIDA/BASE_INDICADORES_MERC_N_RECEBIDA.csv')

def ensure_output_dirs() -> None:
    for path in (DATA_DIR, LOG_DIR, LOG_EXECUTIONS):
        path.mkdir(parents=True, exist_ok=True)

ensure_output_dirs()