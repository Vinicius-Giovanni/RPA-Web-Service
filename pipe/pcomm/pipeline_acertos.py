import pandas as pd

class AcertosPipeline:

    @staticmethod
    def column_descricao(df: pd.DataFrame) -> pd.DataFrame:
        """
        Extrai a Nota Fiscal e a Data de Emissão da coluna 'descricao'.

        Exemplo:
            NF:360052 DT EMI.: 7  2026

        Resultado:
            nota_fiscal -> 360052
            mes_emissao -> 7
            ano_emissao -> 2026
        """

        extraido = df['descricao'].str.extract(
            r"NF:(?P<nota_fiscal>\d+)\s+DT EMI\.:\s*(?P<mes_emissao>\d{1,2})\s+(?P<ano_emissao>\d{4})"
        )

        df['nota_fiscal'] = pd.to_numeric(
            extraido['nota_fiscal'],
            errors="coerce"
        ).astype('Int64')

        df['mes_emissao'] = pd.to_numeric(
            extraido['mes_emissao'],
            errors="coerce"
        ).astype("Int64")

        df['ano_emissao'] = pd.to_numeric(
            extraido['ano_emissao'],
            errors='coerce'
        ).astype('Int64')

        return df