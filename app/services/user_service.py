from __future__ import annotations

from fastapi import Depends
from api.dependencies.auth import get_current_user
from api.dependencies.use_cases import get_user_name_use_case
from app.use_cases.get_user_name import GetUserNameUseCase

"""
Serviços auxiliares relacionados ao usuário autenticado.

Este módulo centraliza operações de obtenção de informações
do usuário autal e partir dos dados presentes no token JWT
e dos casos de uso da aplicação.
"""

async def name_user_auth(
        current_user: dict[str, object] = Depends(get_current_user),
        use_case: GetUserNameUseCase = Depends(get_user_name_use_case)
 ) -> str:
    """
    Recupera o nome do usuário autenticado.

    A função utiliza os dados presentes no payload do JWT para
    identificar o usuário atual e consulta a camada de aplicação
    para obtenção do nome cadastrado.

    Esta dependência pode ser reutilizada por múltiplos endpoints
    que necessitem exibir informações do usuário autenticado.

    Args:
        current_user:
                Payload JWT validado contendo os dados do usuário.
        
                use_case:
                        Caso de uso responsável pela recuperação do nome
                        do usuário.

    Returns:
        str:
                Nome do usuário autenticado.
    """
    return await use_case.execute(str(current_user.get("sub", "")))