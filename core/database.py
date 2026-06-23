from __future__ import annotations

from core.config.settings import get_settings
from infrastructure.database.supabase_client import get_supabase_client

"""
Centraliza o acesso à configuração e ao cliente do Supabase.

Este módulo expõe:
- Configurações relacionadas ao Supabase.
- Uma instância de cliente com inicialização de banco de dados.

A utilização de um proxy lazy evita a crição imediata do
cliente durante a importação dos módulos, reduzind acoplamento
e possíveis problemas de inicialização da aplicação.
"""

settings = get_settings()
SUPABASE_URL = settings.supabase.url
SUPABASE_KEY = settings.supabase.anon_key
SUPABASE_JWT = settings.supabase.jwt_secret
SUPABASE_JWKS_URL = settings.supabase.jwks_url

class _LazySupabaseClient:
    def __getattr__(self, name: str):
        return getattr(get_supabase_client(), name)

supabase = _LazySupabaseClient()