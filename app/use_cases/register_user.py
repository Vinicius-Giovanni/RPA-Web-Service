from __future__ import annotations

from app.dto.auth import RegisterUserDTO
from domain.repositories.user_repository import UserRepository

"""
Caso de uso responsável pelo registro de novos usuários.

Este módulo implenta o fluxo de criação de contas da aplicação,
coordenando as operações necessárias para cadastro de credenciais
e criação do perfil do usuário.

O processo garante que os dados sejam normalizados antes da
persistência e centraliza a lógica de registro na camada
de aplicação
"""

class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, dto:RegisterUserDTO) -> str:
        full_name = dto.full_name.strip()
        email = str(dto.email).strip().lower()
        user_id = await self.user_repository.sign_up(full_name, email, dto.password)
        await self.user_repository.create_user_profile(user_id, full_name)
        return user_id