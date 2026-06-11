from __future__ import annotations

from dataclasses import dataclass

from domain.entities.sector import SectorDemand

@dataclass(frozen=True, slots=True)
class SectorMetrics:
    sectors: list[dict[str, object]]
    total_demand: int
    total_people: int

class SectorMetricsService:
    def calculate(self, sectors: list[SectorDemand]) -> SectorMetrics:
        return SectorMetrics(
            sectors=[sector.raw for sector in sectors],
            total_demand=sum(sector.demand for sector in sectors),
            total_people=sum(sectors.peoples for sector in sectors),
        )