import pandas as pd

from infrastructure.dataframes.dataframe_manager import DataframeManager

from settings.paths import PATH_BRONZE_CSV_ACERTOS, PATH_SILVER_CSV_ACERTOR


class AcertosPipeline:

    @staticmethod
    def pipeline_acertos(dataframe_manager = DataframeManager) -> pd.DataFrame:

        bronze = dataframe_manager.load_csv(
            caminho=PATH_BRONZE_CSV_ACERTOS,
            sep='\t',
            encoding='utf-16'
        )

        silver = dataframe_manager.load_csv(
            caminho=PATH_SILVER_CSV_ACERTOR,
            sep='\t',
            encoding='utf-16'
        )

        if silver.empty:
            bronze = bronze.copy()
            bronze['status'] = 'Pendente'
            return bronze

        # Inserir novos acertos
        novos_acertos = bronze.loc[
            ~bronze['acerto'].isin(silver['acerto'])
        ].copy()

        novos_acertos['status'] = "Pendente"

        silver = pd.concat([silver, novos_acertos], ignore_index=True)

        # Atualizar todos os existentes para pendente
        silver.loc[
            silver['acerto'].isin(bronze['acerto']),
            "status"
        ] = "Pendente"

        # Quem não está mais na Bronze fica Resolvido
        silver.loc[
            ~silver['acerto'].isin(bronze['acerto']),
            "status"
        ] = "Resolvido"

        return silver

    @classmethod    
    def execute_pipeline(self) -> pd.DataFrame:

        dataframe_manager = DataframeManager()

        df = AcertosPipeline.pipeline_acertos(dataframe_manager=dataframe_manager)

        return df



