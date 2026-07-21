from __future__ import annotations

from infrastructure.dataframes.dataframe_manager import DataframeManager
from settings.paths import PATH_ORIGIN

print(PATH_ORIGIN.exists())

dataframe_manager = DataframeManager()

df = dataframe_manager.load_txt(
    caminho=PATH_ORIGIN,
    encoding='utf-8'
)

print(df.info())