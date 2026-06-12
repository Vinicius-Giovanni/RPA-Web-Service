from __future__ import annotations

from domain.repositories.sector_repository import SectorRepository
from domain.services.sector_metrics import SectorMetrics, SectorMetricsService

class GetSectorMetricsUseCase:
    def __init__(self, sector_repository: SectorRepository, metrics_service: SectorMetricsService):
        self.sector_repository = sector_repository
        self.metrics_service = metrics_service

    async def execute(self) -> SectorMetrics:
        sectors = await self.sector_repository.list_demands()
        return self.metrics_service.calculate(sectors)
        