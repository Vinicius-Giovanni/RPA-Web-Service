import pandas as pd

from settings.pipelines_config import COLUMNS_TYPES, REQUIRED_COLUMNS

class RelMercEnvNConfModel:

    _REQUIRED_COLUMNS = REQUIRED_COLUMNS
    _COLUMNS_TYPES = COLUMNS_TYPES

    @classmethod
    def validate_schema(cls, df: pd.DataFrame) -> pd.DataFrame:
    
        # Remove colunas completamente vazia
        df = df.dropna(axis=1, how='all')

        # Remove espaços do nome das colunas
        df.columns = df.columns.str.strip()

        missing = set(cls._REQUIRED_COLUMNS) - set(df.columns)

        if missing:
            raise ValueError(
                f'Colunas obrigatórias ausentes: {sorted(missing)}'
            )
        
        # Mantém somente as colunas esperadas
        df = df[cls._REQUIRED_COLUMNS]

        # Garante os tipos
        df = df.astype(cls._COLUMNS_TYPES)

        return df
    
    @classmethod
    def update_status(
        cls,
        df_origem: pd.DataFrame,
        df_historico: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Atualiza o histórico.

        Regras:
        - Se a NOTA existir na origem -> STATUS_CONTROLE = Pendente
        - Se a NOTA existir apenas no histórico -> STATUS_CONTROLE = Resolvido
        - Se a NOTA for nota -> adiciona todas as linhas dessa nota ao histórico
            com STATUS_CONTROLE = Pendente
        """

        df_origem = df_origem.copy()
        df_historico = df_historico.copy()

        if "STATUS_CONTROLE" not in df_historico.columns:
            df_historico['STATUS_CONTROLE'] = pd.NA

        notas_origem = set(df_origem['NOTA'])
        notas_historico = set(df_historico['NOTA'])

        # Atualiza o histórico
        df_historico['STATUS_CONTROLE'] = df_historico['NOTA'].map(
            lambda nota: "Pendente" if nota in notas_origem else "Resolvido"
        )

        # Apenas notas que nunca existiram no histórico
        notas_novas = notas_origem - notas_historico

        novas_linhas = df_origem[
            df_origem['NOTA'].isin(notas_novas)
        ].copy()

        novas_linhas['STATUS_CONTROLE'] = "Pendente"

        return pd.concat(
            [df_historico, novas_linhas],
            ignore_index=True
        )

    