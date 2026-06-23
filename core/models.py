from pydantic import BaseModel, Field, field_validator
from .forms import as_form

"""
Modelos utilizados para validação de formulários HTTP.

Este módulo define schemas Pydantic utilizados pela camada
de apresentação para validação dos dados recebidos através
de formulários HTML.

Os modelos são decorados com ``@as_form`` para permitir
injeção direta de dados enviados via ``multipart/form-data``
ou ``application/x-www-form-urlencoded`` nos endpoints
do FastAPI.
"""
@as_form
class RegisterUser(BaseModel):
    """
    Representa os dados enviados pelo formulário de cadastro.

    Este modelo é responsável pela validação inicial das
    informações fornecidas pelo usuário antes que os dados
    sejam convertidos em DTOs ou encaminhados para a cadama
    de aplicação.

    Attribute:
        full_name:
            Nome completo do usuário.

            Restrições:
                - Obrigatório.
                - Mínimo de 3 caracteres.
                - Máximo de 50 caracteres.
            
            email:
                Endereço de e-mail informado pelo usuário.

                Restrições:
                - Obrigatório.
                - Mínimo de 3 caracteres.
                - Máximo de 50 caracteres.
                - Deve possuir formato de e-mail válido.
    """
    full_name: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=3, max_length=50)


    @field_validator('email')
    def validate_email(cls, v):
        """
        Valida o formato do endereço de e-mail.

        Args:

        """
        if not ['@'] in v:
            raise ValueError('Invalid email address')
        
        return v