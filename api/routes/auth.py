from __future__ import annotations

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from api.dependencies.use_cases import get_authenticate_user_use_case, get_register_user_use_case
from app.dto.auth import LoginDTO, RegisterUserDTO
from app.use_cases.authenticate_user import AuthenticateUserUseCase
from app.use_cases.register_user import RegisterUserUseCase
from core.config.settings import get_settings

"""
Endpoints responsáveis pelo fluxo de autenticação da aplicação.

Este módulo concentra as operações relacionadas ao clico de vida
de autenticação dos usuários.

- Exibição da tela de cadastro.
- Registro de novos usuários.
- Autenticação via credenciais.
- Encerramento da sessão (logout).

Os endpoints utilizam casos de uso da camada de aplicação
para garantir separação entre regra de negócio e camada HTTP. 
"""

router = APIRouter(tags=['auth'])
templates = Jinja2Templates(directory=str(get_settings().templates.frontend_dir))

@router.get("/cadastro", response_class=HTMLResponse)
async def signup_page(request: Request) -> HTMLResponse:
    """
    Exibe a página de cadastro do usuários.

    Este endpoint renderiza o formulário utilizado para criação
    de novas contas na plataforma.

    Args:
        request:
            Requisição HTTP atual.

    Returns:
        HTMLResponse
            Página de cadastro renderizada.
    """
    return templates.TemplateResponse(request=request, name="register.html", context={})

@router.post("/cadastro")
async def signup(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
) -> RedirectResponse:
    """
    Realiza o cadastro de um novo usuário.

    Os dados enviados pelo formulário são convertidos para um DTO
    e encaminhados ao caso de uso responsável pelo registro.

    Em caso de sucesso, o usuário é redirecionado para a tela
    de login.

    Args:
        full_name:
            Nome completo informado pelo usuário.

        email:
            Endereço de e-mail.
        
        password:
            Senha escolhida pelo usuário.
        
        use_case:
            Caso de uso responsável pelo registro.
    
    Returs:
        RedirectResponse:
            Redirecionamento para a página de login.
    
    Raises:
        HTTPException:
            Caso os dados fornecidos sejam inválidos.
    """
    try:
        dto = RegisterUserDTO(full_name=full_name.strip(), email=email.strip().lower(), password=password)
        await use_case.execute(dto)
        return RedirectResponse("/login", status_code=303)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail="Dados de cadastro inválido") from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    
@router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case),
) -> RedirectResponse:
    """
    Autentica um usuário na aplicação.

    Após a validação das credenciais, um token JWT é gerado
    e armazenado em cookie HTTP Only para autenticação
    das próximas requisições.

    Args:
        email:
            E-mail do usuário.

        password:
            Senha informada.
        
            use_case:
                Caso de uso responsável pela autenticação.

    Returns:
        RedirectResponse:
            Redirecionamento para a página inicial autenticada.

    Raises:
        HTTPException:
            Caso as credenciais sejam inválidas ou o processo
            de autenticação falhe.
    """
    try:
        dto = LoginDTO(email=email.strip().lower(), password=password)
        access_token = await use_case.execute(dto)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail="Email inválido") from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    
    settings = get_settings()
    response = RedirectResponse('/landpage', status_code=303)
    response.set_cookie(
        key=settings.security.access_token_cookie,
        value=access_token,
        httponly=True,
        secure=settings.security.secure_cookies,
        samesite=settings.security.same_site,
        path="/",
    )

    return response

@router.get("/logout")
async def logout() -> RedirectResponse:
    """
    Encerra a sessão do usuário autenticado.

    Remove o cookie de autenticação armazeanado no navegador
    e redirecionoa o usuário para a página inicial pública.

    Returns:
        RedirectResponse:
            Redirecionamento para a página inicial.
    """
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(key=get_settings().security.access_token_cookie)
    return response