from __future__ import annotations

from abc import ABC, abstractclassmethod
from pathlib import Path
import pandas as pd
from uuid import uuid4

from core.logging.log import ExecutionLogger

from modules.pipelines.services.reader_service import ReaderService

execution_id = str(uuid4())

logger = ExecutionLogger(
        automation_name="base_pipeline",
        execution_id=execution_id
)


class BasePipeline(ABC):
    """
    Classe base para todos os pipelines.

    Responsável por controlar o fluxo de execução comum:
        - leitura
        - pré-processamento
        - transformação
        - exportação
    """

    def __init__(
            self,
            *,
            pipeline_key: str,
            pipeline_name: str,
            output_filename: str,
            pipeline_config: dict,
            reader_service: ReaderService,
    ) -> None:
        
        self.key = pipeline_key
        self.name = pipeline_name
        self.output_filename = output_filename
        self.reader = reader_service

        self.cfg = pipeline_config

        if self.cfg is None:
            raise ValueError(f"Pipeline '{self.key}' não encontrado.")
        
        self.df = pd.DataFrame()
    
    #PUBLIC

    async def run(
            self,
            input_path: Path,
            output_path: Path,
    ) -> pd.DataFrame:
        
        await logger.info(f"Iniciando pipeline '{self.key}'")

        output_path.mkdir(parents=True, exist_ok=True)
        input_path.mkdir(parents=True, exist_ok=True)

        self.df = self.reader_csv(
            path=input_path,
            pipeline_key = self.key,
        )

        if self.df.empty:
            await logger.warning("Nenhum dado encontrado no dataframe fornecido.")
            return self.df
        
        self.preprocess()

        self.transform()

        self.postprocess()

        self.reader.export_parquet(
            dataframe=self.df,
            output_file=output_path / f'{self.output_filename}.parquet',
        )

        await logger.info(f"Pipeline '{self.key}' finalizada.")

        return self.df
    
    # COMMON STEPS

    async def preprocess(self) -> None:
        """
        Pré-processamento comum.

        As transformações compartilhadas serão adicionadas
        conforme criarmos os Services.
        """
        pass

    async def postprocess(self) -> None:
        """
        Pós-processamento comum.
        """
        pass

    # ABSTRACT

    @abstractclassmethod
    async def transform(self) -> None:
        """
        Implementação específica da pipelines.
        """

        raise NotImplementedError