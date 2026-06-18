from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field

"""
Data Transfer Objects (DTOs) relacionados ao fluxo de autenticação.

Os DTOs são responsáveis por transportar dados entre a camada
de apresentação (rotas HTTP) e a camada de aplicação (casos de uso),
garantindo validação e tipagem consistentes antes da execução
das regras de negócio.
"""

class RegisterUserDTO(BaseModel):
    """
    Objeto de transferência de dados utilizados no cadastro do usuários.

    Este DTO representa os dados necessários para criação de uma nova conta na plataforma e aplica validação de entrada antes da execução das regras de negócio.
    """
    full_name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class LoginDTO(BaseModel):
    """
    Objeto de transferência de dados utilizado no processo de autenticação.

    Este DTO encapsula as credenciais fornecidas pelo usuário
    durante o login e garante que os dados recebidos atendam
    aos requisitos minimos de validação.
    """
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
