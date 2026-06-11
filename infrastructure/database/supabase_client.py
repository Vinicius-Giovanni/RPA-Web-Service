from __future__ import annotations

from functools import lru_cache

from supabase import Client, create_client

from core.config.settings import get_settings
from core.exceptions.handlers import ConfigurationError

@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    settings = get_settings().supabase
    if not settings.is_configured:
        raise ConfigurationError("Supabase não configurado. Defina os parâmetros necessários (API_URL e API_KEY_ANON_PUBLIC) no ambiente")
    return create_client(settings.url, settings.anon_key)