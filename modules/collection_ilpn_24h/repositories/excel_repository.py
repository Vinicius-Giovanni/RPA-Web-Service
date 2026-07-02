from pathlib import Path

import pandas as pd

from modules.collection_ilpn_24h.service.dataframe_utils import read_csv


class DataFrameRepository:
    """
    Repositório responsável pelas operações de leitura e escrita de arquivos tabulares.

    Esta camada abstrai o acesso físico aos arquivos utilizados pela automação, permitindo que os servições consumam dados sem conhecer detalhes de armazenamento.

    Responsabilidade
    - Leitura de arquivos CSV
    - Leitura de arquivos Excel
    - Escrita de arquivos Excel
    - Padronização do acesso aos dados.
    """
    async def read_csv(self, caminho: str | Path) -> pd.DataFrame:
        return read_csv(str(caminho))
    
    async def read_excel(self, caminho: str | Path) -> pd.DataFrame:
        return pd.read_excel(caminho)
    
    async def save_excel(self, dataframe: pd.DataFrame, caminho: str | Path) -> None:
        dataframe.to_excel(caminho, index=False)

    