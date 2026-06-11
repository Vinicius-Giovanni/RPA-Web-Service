from __future__ import annotations

from asyncio import to_thread

from domain.entities.sector import SectorDemand
from infrastructure.database.supabase_client import get_supabase_client


class SupabaseSectorRepository:
    async def list_demands(self) -> list [SectorDemand]:
        def _select() -> list[SectorDemand]:
            response = get_supabase_client().table("sectors").select("*").execute()
            sectors: list[SectorDemand] = []
            for item in response.data or []:
                sectors.append(
                    SectorDemand(
                        name=str(item.get("name") or item.get("sector") or ""),
                        demand=int(item.get("demand") or 0),
                        peoples=int(item.get("peoples") or 0),
                        raw=dict(item),
                    )
                )
            
            return sectors
        
        return await to_thread(_select)