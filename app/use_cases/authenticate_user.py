from __future__ import annotations

from app.dto.auth import LoginDTO
from domain.repositories.user_repository import UserRepository

"""
Caso de uso responsável pela autenticação de usuarios.

Este módulo implementa o fluxo de login da aplicação,
delegando ao repositório a validação das credenciais
e a obtenção do token de acesso.

A camada de apresentação deve interagir com este caso
de uso em vez de acessar diretamente a infraestrutura
de autenticação.
"""

class AuthenticateUserUseCase:
    """
    Executa o processo de autenticação de usuários.

    Este caso de uso recebe credenciais informadas
    pelo usuário, normaliza os dados necessários e
    delega ao repositório a validação do login.

    Em caso de sucesso, retorna o token de acesso
    gerado pelo provedor de autenticação.

    Attributes:
        user_repository:
            Repositório responsável pelas operações
            de autenticação e acesso aos usuários.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, dto: LoginDTO) -> str:
        """
        Realiza a autenticação de um usuário.

        O e-mail é normalizado antes da autenticação para
        garantir consistência durante a busca das credenciais.

        Fluxo:
        
        1. Recebe os dados de login.
        2. Normaliza o e-mail.
        3. Solicita autenticação ao repositório.
        4. Obtém o token de acesso.
        5. Retorna o token gerado.

        Args:
            dto:
                Dados de autenticação fornecidos pelo usuário.
        Returns:
            str:
                Token JWT de acesso gerado após autenticação
                bem-sucedida.
        Raises:
            Exception:
                Qualquer exceção propagada pelo repositório
                durante o processo de autenticação.
        """
        _, access_token = await self.user_repository.sign_in(str(dto.email).strip().lower(), dto.password)
        return access_token