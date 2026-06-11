from __future__ import annotations

from typing import Protocol

from domain.entities.user import AuthenticatedUser

class UserRepository(Protocol):
    async def create_user_profile(self, user_id: str, full_name: str) -> None: ...

    async def get_full_name(self, user_id: str) -> str: ...

    async def sign_up(self, full_name: str, email: str, password: str) -> str: ...

    async def sign_in(self, email:str, password: str) -> tuple[AuthenticatedUser, str]: ...