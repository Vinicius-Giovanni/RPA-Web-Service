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
    """
    Execute o processa de cadastro de usuários.

    Este caso de uso coordena as operações necessárias para
    criação de uma nova conta na plataform.

    Fluxo executado:

    1. Recebe os dados do usuário.
    2. Normaliza nome e e-mail.
    3. Cria a conta de autenticação.
    4. Cria o perfil do usuário.
    5. Retorna o identificador gerado.

    Attributes:
        user_repository:
            Repositório responsável pelas operações de
            autenticação e persistência dos usuários.
    """
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, dto:RegisterUserDTO) -> str:
        """
        Realiza o cadastro de um novo usuário.

        Os dados recebidos são normalizados antes de persistência
        para garantir consistência no armazenamento.

        Operações executadas:

        - Remoção de espaços extras do nome.
        - Normalização do e-mail para letras minúsculas.
        - Criação da conta de autenticação.
        - Criação do perfil do usuário.

        Args:
            dto:
                Dados necessários para registro do usuário.

        Returns:
            str:
                Identificador único do usuário criado.

        Raises:
            Exception:
                Qualquer exceção propagada pelo repositório durante
                o processo de cadastro.
        """
        full_name = dto.full_name.strip()
        email = str(dto.email).strip().lower()
        user_id = await self.user_repository.sign_up(full_name, email, dto.password)
        await self.user_repository.create_user_profile(user_id, full_name)
        return user_id