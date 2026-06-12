from __future__ import annotations

from app.dto.auth import LoginDTO
from domain.repositories.user_repository import UserRepository

class AuthenticatedUserUseCase:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, dto: LoginDTO) -> str:
        _, access_token = await self.user_repository.sign_in(str(dto.email).strip().lower(), dto.password)
        return access_token