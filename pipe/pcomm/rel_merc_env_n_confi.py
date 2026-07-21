from __future__ import annotations

from models.schemas.invoices_model import RelMercEnvNConfModel
from infrastructure.dataframes.dataframe_manager import DataframeManager
from settings.paths import PATH_ORIGIN, PATH_BRONZE_CSV, PATH_GOLD_PARQUET

print(PATH_ORIGIN.exists())

dataframe_manager = DataframeManager()

df = dataframe_manager.load_txt(
    caminho=PATH_ORIGIN,
    encoding='utf-8'
)

_df = dataframe_manager.load_csv(
    caminho=PATH_BRONZE_CSV
)

RelMercEnvNConfModel.transform(df)
RelMercEnvNConfModel.validate_schema(df)
_df_ = RelMercEnvNConfModel.update_status(
        df_origem=df,
        df_historico=_df
    )

dataframe_manager.save_csv(
    caminho=PATH_BRONZE_CSV,
    df=_df_
)

dataframe_manager.save_parquet(
    caminho=PATH_GOLD_PARQUET,
    df=_df_
)

print(_df_.info())