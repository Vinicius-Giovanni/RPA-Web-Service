from __future__ import annotations

from typing import Type

from modules.pipelines.base.base_pipeline import BasePipeline

class PipelineFactory:
    """
    Responsável por registrar e instanciar pipelines.
    """

    _pipelines: dict[str, Type[BasePipeline]] = {}

    @classmethod
    async def register(
        cls,
        pipeline_key: str,
        pipeline_class: Type[BasePipeline],
    ) -> None:
        
        cls._pipelines[pipeline_key] = pipeline_class

    @classmethod
    async def create(
        cls,
        pipeline_key: str,
        **kwargs,
    ) -> BasePipeline:
        
        try:
            pipeline = cls._pipelines[pipeline_key]
        except KeyError:
            raise ValueError(
                f"Pipeline '{pipeline_key}' não registrada."
            )

        return pipeline(**kwargs)
    
    @classmethod
    async def registered_pipelines(cls) -> list[str]:
        return sorted(cls._pipelines.keys())
    
    @classmethod
    async def exists(cls, pipeline_key: str) -> bool:
        return pipeline_key in cls._pipelines