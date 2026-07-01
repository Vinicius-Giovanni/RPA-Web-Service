from __future__ import annotations

from fastapi import Depends

from api.dependencies.repositories import get_sector_repository, get_user_repository
from app.use_cases.authenticate_user import AuthenticateUserUseCase
from app.use_cases.get_sector_metrics import GetSectorMetricsUseCase
from app.use_cases.get_user_name import GetUserNameUseCase
from app.use_cases.register_user import RegisterUserUseCase
from domain.repositories.sector_repository import SectorRepository
from domain.repositories.user_repository import UserRepository
from domain.services.sector_metrics import SectorMetricsService

def get_register_user_use_case(repository: UserRepository = Depends(get_user_repository)) -> RegisterUserUseCase:
    """
    Cria e fornece o caso de uso responsável pelo cadastro de usuários.

    A dependência injeta automaticamente a implementação do
    repositório de usuários necessária para execução da regra de negócio.

    Args:
        repository:
            Repositório responsável pela persistência de usuários.

    Returns:
        RegisterUserUseCase:
            Caso de uso configurado para registro de usuários.
    """
    return RegisterUserUseCase(repository)

def get_authenticate_user_use_case(repository: UserRepository = Depends(get_user_repository)) -> AuthenticateUserUseCase:
    """
    Cria e fornece o caso de uso responsável pela autenticação
    de usuários.

    O caso de uso utiliza o repositório de usuários para validar
    credenciais e recuperar informações necessárias para o processo
    de autenticação.

    Args:
        repository:
            Repositório responsável pelo acesso aos dados de usuários.

    Returns:
        AuthenticateUserUseCase:
            Caso de uso configurado para autenticação.
    """
    return AuthenticateUserUseCase(repository)

def get_user_name_use_case(repository: UserRepository = Depends(get_user_repository)) -> GetUserNameUseCase:
    """
    Cria e fornece o caso de uso responsável pela recuperação
    das informações do usuário autenticado.

    A dependência injeta o repositório necessário para consulta
    dos dados persistidos.

    Args:
        repository:
            Repositório responsável pelo acesso aos daods de usuários.
    """
    return GetUserNameUseCase(repository)

def get_sector_metrics_use_case(repository: SectorRepository = Depends(get_sector_repository),) -> GetSectorMetricsUseCase:
    """
    Cria e fornece o caso de uso responsável pelo cálculo
    e consolidação de métricas dos setores.

    Além do repositório de dados, este caso de uso recebe uma
    instância do serviço de domínio responsável pelas regras
    de cálculo das métricas.

    Args:
        repository:
            Repositório responsável pelo acesso aos dados dos setores.
    
    Returns:
        GetSectorMetricsUseCase:
            Caso de uso configurado para geração de métricas.
    """
    return GetSectorMetricsUseCase(repository, SectorMetricsService())
