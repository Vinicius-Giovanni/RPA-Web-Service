from __future__ import annotations

from typing import Protocol

from domain.entities.user import AuthenticatedUser

"""
Contratos de acesso aos dados de usuários.

Este módulo define a interfaces utilizadas pelo domínio e pela camada de aplicação para operações relacionadas a usuários e
autenticação.

As implementações concretas deste contrato pertencem à camada
de infraestrutura, permitindo que as regras de negócio permaneçam
desacopladas de tecnologias específicas de persistência e
autenticação.
"""

class UserRepository(Protocol):
    """
    Contrato de acesso às informações e operações de usuários.

    Esta interface define as funcionalidades necessárias para:

    - Cadastro de usuários;
    - Autenticação;
    - Consulta de perfis;
    - Gerenciamento de informações básicas do usuário.

    Implementações possíveis:
    - Supabase
    - PostgreSQL
    - API Externa
    - Repositórios em memória para testes

    O domínio depende apenas deste contrato, nunca de
    implementações concretas.
    """
    async def create_user_profile(self, user_id: str, full_name: str) -> None:
        """
        Cria o perfil do usuário após o cadastro.

        Args:
            user_id:
                Identificador único do usuário.

            full_name:
                Nome completo do usuário
        """

    async def get_full_name(self, user_id: str) -> str:
        """
        Obtém o nome completo de um usuário.

        Args:
            user_id:
                Identificador único do usuário.

            Returns:
                str:
                    Nome completo do usuário.
        """

    async def sign_up(self, full_name: str, email: str, password: str) -> str:
        """
        Realiza o cadastro de um novo usuário.

        Args:
            full_name:
                Nome completo do usuário.
            
                email:
                    E-mail utilizado para autenticação.

                password:
                    Senha do usuário.

        Returns:
            str:
                Identificador único do usuário criado.
        """

    async def sign_in(self, email:str, password: str) -> tuple[AuthenticatedUser, str]:
        """
        Autentica um usuário.

        Args:
            email:
                E-mail do usuário.
            
            password:
                Senha do usuário.

        Returns:
            tuple[AuthenticatedUser, str]:
                Tupla contendo:

                - Entidade do usuário autenticado.
                - Token de acesso JWT.
        """