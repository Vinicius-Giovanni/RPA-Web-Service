from pathlib import Path

import pandas as pd

from modules.collection_ilpn_24h.service.dataframe_utils import normalizar_email

class ColaboradorRepository:
    """
    Responsável pelo carregamento e indexação dos dados de colaboradores.

    Este repositório fornece estruturas otimizadas para consultas rápidas de informações cadastrais através de e-mail, matrícula ou nome.

    - Carregar a base de colaboradores
    - Normalizar chaves de pesquisa
    - Construir índices de busca em memória
    - Disponibilizar acesso rápido aos dados do RH
    """

    def __init__(self, caminho_colaboradores: str | Path):
        """
        Inicializa o repositório
        
        caminho_colaboradores: str | Path
            Caminho do arquivo Excel contendo os dados do RH
        """
        self.caminho_colaboradores = caminho_colaboradores

    async def load_dataframe(self) -> pd.DataFrame:
        """
        Carrega a planilha de colaboradores

        pd.DataFrame
            DataFrame contendo os registros do RH
        """
        return pd.read_excel(self.caminho_colaboradores)
    
    async def carregar_indices_rh(self) -> tuple[dict[str, dict], dict[str, dict]]:
        """
        Constrói índices de consulta para os colaboradores.

        Dois índices são gerados:
        1. índice  e-mail/matrícula
        2. índice por nome

        Os índices são utilizados durante o processo de enriquecimento
        das ILPNs para localizar gestor, coordenador e setor responsável

        Returns
        tuple[dict[str, dict], dict[str, dict]]

            dict_email:
                Estrutura indexada por e-mail ou matrícula

            dict_nome:
                Estrutura indexada por nome normalizada
        """
        dict_email: dict[str, dict] = {}
        dict_nome: dict[str, dict] = {}
        df_colab = self.load_dataframe()

        if "EMAIL | MATRICULA" in df_colab.columns:
            df_colab['CHAVE_BUSCA'] = df_colab["EMAIL | MATRICULA"].apply(normalizar_email)
            df_email = df_colab[df_colab['CHAVE_BUSCA'] != ""].drop_duplicates(subset=["CHAVE_BUSCA"], keep="first")
            dict_email = df_email.set_index("CHAVE_BUSCA").to_dict("index")
        
        col_nome = next((col for col in df_colab.columns if "NOME" in str(col).upper()), None)

        if col_nome:
            df_colab['NOME_BUSCA'] = df_colab[col_nome].astype(str).str.strip().str.upper()
            df_nome = df_colab[
                (df_colab['NOME_BUSCA'] != "") & (df_colab['NOME_BUSCA'] != "NAN")
            ].drop_duplicates(subset=['NOME_BUSCA'], keep="first")
            dict_nome = df_nome.set_index('NOME_BUSCA').to_dict("index")

        return dict_email, dict_nome
