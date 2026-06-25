from __future__ import annotations

from asyncio import to_thread

from domain.entities.user import AuthenticatedUser
from infrastructure.database.supabase_client import get_supabase_client

"""
Implementação do repositório de usuários utilizando o Supabase.

Este módulo contém as operações de persistência e autenticação
de usuários por meio dos serviços disponibilizados pelo Supabase.

As responsabilidades deste repositório incluem:

- Criação do perfil de usuários na base de dados;
- Consulta de informações do usuário;
- Cadastro de novas contas;
- Autenticação de usuários existentes.

As operações síncronas do cliente Supabase são executadas em
threads separadas para evitar o bloqueio do loop de eventos
da aplicação assíncrona.
"""
class SupabaseUserRepository:
    """
    Repositório responsável pelas operações de persistência e
    autenticação de usuários.

    Esta implementação encapsula o acesso às tabelas e aos
    serviços de autenticação do Supabase, convertendo os
    resultados para entidades pertencentes ao domínio da
    aplicação.
    """
    async def create_user_profile(self, user_id: str, full_name: str) -> None:
        """
        Cria o perfil de um usuário na tabela de usuários.

        Args:
            user_id:
                Identificador único do usuário.
            full_name:
                Nome completo do usuário.
        """
        def _insert() -> None:
            get_supabase_client().table("user_table").insert({"id": user_id, "full_name": full_name}).execute()

        await to_thread(_insert)

    async def get_full_name(self, user_id: str) -> str:
        """
        Obtém o nome completo de um usuário.

        Args:
            user_id:
                Identificador único do usuário.

            Returns:
                str:
                    Nome completo do usuário. Caso o registro
                    não seja encontrado, retorna uma string vazia.
        """
        def _select() -> None:
            response = get_supabase_client().table("user_table").select("full_name").eq("id", user_id).single().execute()
            data = response.data or {}
            return str(data.get("full_name", ""))
        
        return await to_thread(_select)
    
    async def sign_up(self, full_name: str, email: str, password: str) -> str:
        """
        Realiza o cadastro de um novo usuário.

        Além de criar a conta de autenticação, o nome completo
        é armazenado nos metadados do usuário.

        Args:
            full_name:
                Nome completo do usuário.

            email:
                Endereço de e-mail utilizado no cadastro.

            password:
                Senha da conta.
        
        Returns:
            str:
                Identificador único do usuário criado.
        
        Raises:
            ValueError:
                Caso o processo de cadastro falhe.
        """
        def _sign_up() -> str:
            response = get_supabase_client().auth.sign_up(
                {"email": email, "password": password, "options": {"data": {"full_name": full_name}}}
            )
            if response.user is None:
                raise ValueError("Signup failed")
            return str(response.user.id)
        
        return await to_thread(_sign_up)
    
    async def sign_in(self, email: str, password: str) -> tuple[AuthenticatedUser, str]:
        """
        Autentica um usuário utilizando e-mail e senha.

        Args:
            email:
                Endereço de e-mail do usuário.

            password:
                Senha da conta.

            Returns:
                tuple[AuthenticatedUser, str]:
                    Tupla contendo a entidade do usuário autenticado
                    e o token de acesso da sessão.

            Raises:
                ValueError:
                    Caso as credenciais sejam inválidas ou o processo
                    de autenticação falhe.
        """
        def _sign_in() -> tuple[AuthenticatedUser, str]:
            response = get_supabase_client().auth.sign_in_with_password({"email": email, "password": password})
            if response.user is None or response.session is None:
                raise ValueError("Login failed")
            user = AuthenticatedUser(id=str(response.user.id), email=email)
            return user, str(response.session.access_token)
        
        return await to_thread(_sign_in)