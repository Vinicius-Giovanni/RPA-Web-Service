from __future__ import annotations

from functools import lru_cache

from supabase import Client, create_client

from core.config.settings import get_settings
from core.exceptions.handlers import ConfigurationError

"""
Cliente de acesso ao banco de dados Supabase.

Este módulo é responsável por fornecer uma instância única
do cliente do Supabase para toda a aplicação, garantindo
o reaproveitamento da conexão por meio de cache.

Também realiza a validação das configurações necessárias
para a comunicação com o serviço antes de criar o cliente.
"""

@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """
    Obtém uma instância configurada do cliente Supabase.

    A instância é criada apenas uma vez durante o ciclo de
    vida da aplicação e armazenada em cache, evitando a
    recriação desnecessária da cliente em chamadas futuras.

    Antes da criação do cliente, as configurações do
    Supabase são validadas para garantir que os parâmetros
    obrigatórios estejam definidos no ambiente.

    Returns:
        Client:
            Instãncia configurada do cliente Supabase.

    Raises:
        ConfigurationError:
            Caso as configurações necessárias do Supabase
            não estejam definidas no ambiente.
    """
    settings = get_settings().supabase
    if not settings.is_configured:
        raise ConfigurationError("Supabase não configurado. Defina os parâmetros necessários (API_URL e API_KEY_ANON_PUBLIC) no ambiente")
    return create_client(settings.url, settings.anon_key)