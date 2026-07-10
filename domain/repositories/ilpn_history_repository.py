from pathlib import Path

import pandas as pd

from models.ilpn.model_cobranca_ilpn import  COLUNAS_HISTORICO

class HistoricoRepository:
    """
    Repositório responsável pela persistência do histórico de ILPNs

    O histórico é utilizado par comparação entre execuções, identificação de novas pendências, resoluções e alterações
    de status ao longo do tempo.

    Responsabilidades
    - Carregar snapshots históricos
    - Criar estrutura inicial quando inexistente
    - Persistir novas versões do histórico
    - Garantir padronização das colunas utilizadas no processo
    """
    def __init__(self, caminho_historico: str | Path):
        self.caminho_historico = Path(caminho_historico)

    def carregar(self) -> pd.DataFrame:
        if not self.caminho_historico.exists():
            return pd.DataFrame(columns=COLUNAS_HISTORICO)
        return pd.read_excel(self.caminho_historico).astype(object)
    
    def salvar(self, dataframe: pd.DataFrame) -> None:
        dataframe.to_excel(self.caminho_historico, index=False)