from __future__ import annotations

from fastapi import Depends

from api.dependencies.repositories import get_sector_repository, get_user_repository
from app.use_cases.authenticate_user import AuthenticatedUserCase
from app.use_cases.get_sector_metrics import GetSectorMetricsUseCase
from app.use_cases.get_user_name import GetUserNameUseCase
from app.use_cases.register_user import RegisterUserUseCase
from domain.repositories.sector_repository import SectorRepository
from domain.repositories.user_repository import UserRepository
from domain.services.sector_metrics import SectorMetricsService

def get_register_user_use_case(repository: UserRepository = Depends(get_user_repository)) -> RegisterUserUseCase:
    return RegisterUserUseCase(repository)

def get_authenticate_user_use_case(repository: UserRepository = Depends(get_user_repository)) -> AuthenticatedUserCase:
    return AuthenticatedUserCase(repository)

def get_user_name_use_case(repository: UserRepository = Depends(get_user_repository)) -> GetUserNameUseCase:
    return GetSectorMetricsUseCase(repository)

def get_sector_metrics_use_case(repository: SectorRepository = Depends(get_sector_repository),) -> GetSectorMetricsUseCase:
    return GetSectorMetricsUseCase(repository, SectorMetricsService())
