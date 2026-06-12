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

router = APIRouter(tags=['auth'])
templates = Jinja2Templates(directory=str(get_settings().templates.frontend_dir))

@router.get("/cadastro", response_class=HTMLResponse)
async def signup_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="register.html", context={})

@router.post("/cadastro")
async def signup(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
) -> RedirectResponse:
    try:
        dto = RegisterUserDTO(full_name=full_name.strip(), email=email.strip().lower(), password=password)
        await use_case.execute(dto)
        return RedirectResponse("/login", status_code=303)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail="Dados de cadastro inválido") from exc
    except Exception as exc:
        raise HTMLResponse(status_code=400, detail=str(exc)) from exc
    
@router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case),
) -> RedirectResponse:
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
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(key=get_settings().security.access_token_cookie)
    return response