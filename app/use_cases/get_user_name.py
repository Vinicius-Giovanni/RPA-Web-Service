from __future__ import annotations

from domain.repositories.user_repository import UserRepository

class GetUserNameUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user_id: str) -> str:
        return await self.user_repository.get_full_name(user_id)
        