from __future__ import annotations

from domain.repositories.user_repository import UserRepository

"""
Caso de uso responsável pela recuperação do nome do usuário.

Este módulo encapsula a consulta das informações de identificação
do usuário, abstraindo a camada de persistência da camada de apresentação.

Seu objetivo é fornecer um ponto único de acesso para obtenção
do nome completo de usuários cadastrados.
"""

class GetUserNameUseCase:
    """
    Recupera o nome completo de um usuário.

    Este caso de uso atua como intermediário entre a camada
    de apresentação e o repositório de usuários, garantindo
    que o acesso às informações seja realizado através da
    camada de aplicação.

    Attributes:
        user_repository:
            Repositório responsável pela consulta dos dados
            dos usuários.
    """
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user_id: str) -> str:
        """
        Recupera o nome compleeto de um usuário.

        A consulta é realizada através do indentificador único
        do usuário fornecido.

        Args:
            user_id:
                identificador único do usuário.

        Returns:
            str:
                Nome completo do usuário.

        Raises:
            Exception:
                Qualquer exceção propagada pelo repositório durante
                o processo de consulta.
        """
        return await self.user_repository.get_full_name(user_id)
        