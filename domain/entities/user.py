from __future__ import annotations

from dataclasses import dataclass

"""
Entidades relacionadas ao domínio de usuários.

Este módulo define a estruturas utilizadas para representar
um usuário autenticado na aplicação.

As entidades de domínio são independentes de frameworks,
banco de dados ou mecanismos de autenticação, servindo como
contratos de negócio entre as camadas do sistema.
"""

@dataclass(frozen=True, slots=True)
class AuthenticatedUser:
    """
    Representa um usuário autenticado na aplicação.

    Esta entidade contém as informações básicas de indentidade
    do usuário após a validação do processo de autenticação.

    A entidade é imutável (frozen=True), garantindo que os
    dados do usuário não sejam alterados acidentalmente durante
    o processamento de uma requisição.

    Attributes:
        id:
            Identificador únido do usuário.
        email:
            Endereço de e-mail do usuário.
        full_name:
            Nome completo do usuário.

            Este campo é opctional e pode não estar disponível
            em alguns fluxos de autenticação.
    """
    id: str
    email: str
    full_name: str = ""