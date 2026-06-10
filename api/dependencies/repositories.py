from __future__ import annotations

from domain.repositories.sector_repository import SectorRepository
from domain.repositories.user_repository import UserRepository
from infrastructure.database.supabase_sector_repository import SupabaseSectorRepository
from infrastructure.database.supabase_user_repository import SupabaseUserRepository

def get_user_repository() -> UserRepository:
    return SupabaseUserRepository()

def get_sector_repository() -> SectorRepository:
    return SupabaseSectorRepository