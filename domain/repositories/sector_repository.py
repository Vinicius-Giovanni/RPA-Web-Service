from __future__ import annotations

from typing import Protocol

from domain.entities.sector import SectorDemand

class SectorRepository(Protocol):
    async def list_demands(self) -> list[SectorDemand]: ...