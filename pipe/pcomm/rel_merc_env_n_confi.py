from __future__ import annotations

from models.schemas.invoices_model import RelMercEnvNConfModel
from infrastructure.dataframes.dataframe_manager import DataframeManager
from settings.paths import PATH_ORIGIN, PATH_BRONZE_CSV, PATH_GOLD_PARQUET

print(PATH_ORIGIN.exists())

dataframe_manager = DataframeManager()

df_txt = dataframe_manager.load_txt(
    caminho=PATH_ORIGIN,
    encoding='utf-8'
)

df_csv = dataframe_manager.load_csv(
    caminho=PATH_BRONZE_CSV
)

if not df_csv.empty:
    df_csv = RelMercEnvNConfModel.validate_schema(df_csv)

df_txt = RelMercEnvNConfModel.transform(df_txt)
df_txt = RelMercEnvNConfModel.validate_schema(df_txt)
df = RelMercEnvNConfModel.update_status(
        df_origem=df_txt,
        df_historico=df_csv
    )
df = RelMercEnvNConfModel.enrich(df)

dataframe_manager.save_csv(
    caminho=PATH_BRONZE_CSV,
    df=df
)

dataframe_manager.save_parquet(
    caminho=PATH_GOLD_PARQUET,
    df=df
)

print(df.info())