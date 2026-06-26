from __future__ import annotations
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / ".env"
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
LOG_EXECUTIONS = LOG_DIR / 'executions'

# Dados -- ALterar depois
PATH_ILPNS = DATA_DIR / "ILPNs.xlsx"
PATH_PIX = DATA_DIR / "PIX.xlsx"
PATH_COLABORADORES = DATA_DIR / "colaboradores.xlsx"
PATH_ILPNS_PENDENTES = DATA_DIR / "ILPNs_pendentes.xlsx"
PATH_PRONTO_ENVIO = DATA_DIR / "ILPNs_pendentes_pronta_entrega.xlsx"
PATH_HISTORICO_PBI = DATA_DIR / "historico_pbi.xlsx"
PATH_LOG_EXECUCAO = LOG_EXECUTIONS / "controle_estoque.jsonl"

def ensure_output_dirs() -> None:
    for path in (DATA_DIR, LOG_DIR, LOG_EXECUTIONS):
        path.mkdir(parents=True, exist_ok=True)

ensure_output_dirs()