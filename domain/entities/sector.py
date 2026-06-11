from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SectorDemand:
    name: str
    demand: int
    peoples: int
    raw: dict[str, object]