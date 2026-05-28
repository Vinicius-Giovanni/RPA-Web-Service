
from core.database import supabase
from fastapi import Depends

# extração de quantidade de demanda dos setores
async def demand_sector() -> dict:

    demands = supabase.table('sectors').select("*").execute()

    return demands.data