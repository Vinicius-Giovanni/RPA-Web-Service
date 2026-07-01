from __future__ import annotations

from domain.repositories.sector_repository import SectorRepository
from domain.repositories.user_repository import UserRepository
from infrastructure.database.supabase_sector_repository import SupabaseSectorRepository
from infrastructure.database.supabase_user_repository import SupabaseUserRepository

def get_user_repository() -> UserRepository:
    """
    Fornece uma instância concreta do repositório de usuários.

    Esta dependência realiza a associação entre a interface
    UserRepository, definida na camada de domínio, e sua implementação
    baseada em Supabase.

    A utilização dessa abstração permite que a aplicação permaneça
    desacoplada da tecnologia de persistência utilizada, facilitando
    testes, manutenção e futuras substituições de infraestrutura.

    Returns:
        UserRepository:
            Implementação concreta do repositório de usuário.
    """
    return SupabaseUserRepository()

def get_sector_repository() -> SectorRepository:
    """
    Fornece uma instância concreta do repositório de setores.

    Esta dependência conecta a interface SectorRepository à sua
    implementação baseada em Supabase, garantindo que os casos
    de uso dependam apenas de contratos definidos na camada
    de domínio.

    Returns:
        SectorRepository:
            Implementação concreta do repositório de setores.
    """
    return SupabaseSectorRepository()