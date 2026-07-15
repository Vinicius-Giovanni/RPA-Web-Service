from __future__ import annotations
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os
import datetime

ENV_PATH = Path(".env")
load_dotenv(dotenv_path=ENV_PATH)

# Variáveis protegidas
ID_EMPLOYEE = os.getenv('ID_EMPLOYEE')

# Principal configs ======================================================================================================
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

# Geração de Base de Dados para Transito Fiscal ======================================================================================================
EXTRACT_INVOICES_TXT_PATH = Path(r'\\nascds.viavarejo.com.br\cd1200\share2\ger_oper1200\Controles_Logisticos\Controle_Transito_fiscal')

SAVE_CSV_INVOICES = Path(fr'{DATA_DIR}/Gold (Business Layer)/pcom_validade_invoices/extract_invoice_{datetime.now():%Y-%m-%d_%H%M}.csv')

# Extração de relatórios do IBM Cognos

COOKIES_FILE = Path(r'cookies.json')

FILES_DIRS = {
    ''
}