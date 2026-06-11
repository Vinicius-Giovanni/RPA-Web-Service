from __future__ import annotations

from api.dependencies.repositories import get_sector_repository
from application.use_cases.get_sector_metrics import GetSectorMetricsUseCase
from domain.services.sector_metrics import SectorMetricsService

async def demand_sector() -> tuple[list[dict[str, object]], int, int]:
    use_case = GetSectorMetricsUseCase(get_sector_repository(), SectorMetricsService())
    metrics = await use_case.execute()
    return metrics.sector, metrics.total_demand, metrics.total_people