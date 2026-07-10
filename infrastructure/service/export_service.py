from __future__ import annotations

from pathlib import Path

import pandas as pd

class ExportService:
    """
    Serviço responsável pela exportação de DataFrames.

    Centraliza toda a lógica de escrita dos arquivos da pipeline.
    """

    @staticmethod
    async def export_parquet(
        df: pd.DataFrame,
        output_folder: Path,
        filename: str,
        compression: str = 'zstd',
    ) -> Path:
        """
        Exporta um DataFrame para Parquet.
        """

        output_folder.mkdir(parents=True, exist_ok=True)

        output_file = output_folder / f'{filename}.parquet'

        df.to_parquet(
            output_file,
            index=False,
            compression=compression
        )

        return output_file
    
    @staticmethod
    async def export_csv(
        df: pd.DataFrame,
        output_folder: Path,
        filename: str,
        sep: str = ";",
        encoding: str = 'utf-8-sig',
    ) -> Path:
        """
        Exporta um DataFrame para CSV.
        """

        output_folder.mkdir(parents=True, exist_ok=True)

        output_file = output_folder / f'{filename}.csv'

        df.to_csv(
            output_file,
            index=False,
            sep=sep,
            encoding=encoding,
        )

        return output_file
    
    @staticmethod
    async def export_excel(
        df: pd.DataFrame,
        output_folder: Path,
        filename: str,
    ) -> Path:
        """
        Exporta um DataFrame para Excel.
        """

        output_folder.mkdir(parents=True, exist_ok=True)

        output_file = output_folder / f'{filename}.xlsx'

        df.to_excel(
            output_file,
            index=False,
        )

        return output_file