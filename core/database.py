from __future__ import annotations

from core.config.settings import get_settings
from infraestructure.database.supabase_client import get_supabase_client

settings = get_settings()
SUPABASE_URL = settings.supabase.url
SUPABASE_KEY = settings.supabase.anon_key
SUPABASE_JWT = settings.supabase.jwt_secret
SUPABASE_JWKS_URL = settings.supabase.jwks_url

class _LazySupabaseClient:
    def __getattr__(self, name: str):
        return getattr(get_supabase_client(), name)

supabase = _LazySupabaseClient()