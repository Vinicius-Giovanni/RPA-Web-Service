from __future__ import annotations
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

ENV_PATH = Path(".env")
load_dotenv(dotenv_path=ENV_PATH)

# Variáveis protegidas
ID_EMPLOYEE = os.getenv('ID_EMPLOYEE')

# All configs =========================================================
BASE_DIR = Path(f'C:/Users/{ID_EMPLOYEE}/Desktop/project/RPA-Web-Service')
DATA_DIR = Path(f'C:/Users/{ID_EMPLOYEE}/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse')
LOG_DIR = BASE_DIR / "logs"
LOG_EXECUTIONS = LOG_DIR / 'executions'

TODAY = datetime.now()



# # Dados -- ALterar depois
# PATH_ILPNS = DATA_DIR / "ILPNs.xlsx"
# PATH_PIX = DATA_DIR / "PIX.xlsx"
# PATH_COLABORADORES = DATA_DIR / "colaboradores.xlsx"
# PATH_ILPNS_PENDENTES = DATA_DIR / "ILPNs_pendentes.xlsx"
# PATH_PRONTO_ENVIO = DATA_DIR / "ILPNs_pendentes_pronta_entrega.xlsx"
# PATH_HISTORICO_PBI = DATA_DIR / "historico_pbi.xlsx"
# PATH_LOG_EXECUCAO = LOG_EXECUTIONS / "controle_estoque.jsonl"

# Transito Fiscal ============================================================
PENDING_FISCAL_ORIGEM_TXT = Path(f'//nascds.viavarejo.com.br/cd1200/share2/ger_oper1200/Controles_Logisticos/Controle_NF_transito/REL_MERC_N_RECEBIDA_{TODAY.strftime("%Y%m%d")}txt')
PENDING_FISCAL_DESTINO_TXT = Path(f'C:/Users/{ID_EMPLOYEE}/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/REL_MERC_N_RECEBIDA/DIR_TXT/REL_MERC_N_RECEBIDA_{TODAY.strftime("%Y%m%d")}txt')
PENDING_FISCAL_DESTINO_CSV = Path(f'C:/Users/{ID_EMPLOYEE}/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/REL_MERC_N_RECEBIDA/DIR_CSV/REL_MERC_N_RECEBIDA_{TODAY.strftime("%Y%m%d")}.csv')
PENDING_FISCAL_HISTORICO_PARQUET = Path(f'C:/Users/{ID_EMPLOYEE}/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Gold (Business Layer)/REL_MERC_N_RECEBIDA/BASE_INDICADORES_MERC_N_RECEBIDA.parquet')

# Geração de Base de Dados para Transito Fiscal
EXTRACT_INVOICES_TXT_PATH = Path(r'\\nascds.viavarejo.com.br\cd1200\share2\ger_oper1200\Controles_Logisticos\Controle_Transito_fiscal')