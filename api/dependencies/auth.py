from __future__ import annotations

from functools import lru_cache

import jwt
from fastapi import Depends, HTTPException, Request, status
from jwt import PyJWKClient

from core.config.settings import get_settings
from domain.entities.user import AuthenticatedUser

@lru_cache(maxsize=1)
def get_jwks_client() -> PyJWKClient:
    """
    Retorna uma instância cacheada do cliente JWKS

    O cliente é utilizado para recuperar automaticamente as chaves
    públicas disponibilizadas pelo provedor de autenticação,
    permitindo a validação da assinatura dos tokens JWT recebidos.

    O cache evita múltiplas inicializações do cliente durante o ciclo
    de vida da aplicação.

    Returns:
        PyJWKClient: Cliente configurado para consulta das chaves JWKS.

    Raises:
        HTTPException:
            - 503 Service Unavailable caso o Supabase não esteja configurado.
    """

    settings = get_settings().supabase
    if not settings.url:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Banco de dados não configurado")
    return PyJWKClient(f'{settings.url}{settings.jwks_url}')

async def get_current_user(request: Request) -> dict[str, object]:
    """
    Obtém e valida o token JWT presente nos cookies da requisição.

    O fluxo executa as seguintes etapas:

    1. Recupera o token de acesso armazenado em cookie.
    2. Obtém a chave pública correspondente através do endpoint JWKS.
    3. Valida a assinatura e integridade do token.
    4. Decodifica o payload JWT.
    5. Retorna os claims do usuário autenticado.

    Esta dependência é utilizada como base para autenticação das rotas
    protegidas da aplicação.

    Args:
        request: Objeto da requisição HTTP atual.

    Returns:
        dict[str, object]:
            Payload decodificado do JWT contendo os claims do usuário.
            
    """
    settings = get_settings()
    token = request.cookies.get(settings.security.access_token_cookie)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        signing_key = get_jwks_client().get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=list(settings.security.jwt_algorithms),
            options={"verify_aud": False},
        )
        return dict(payload)
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired') from exc
    except jwt.InvalidAlgorithmError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    
async def get_authenticated_user(payload: dict[str, object] = Depends(get_current_user)) -> AuthenticatedUser:
    return AuthenticatedUser(id=str(payload.get('sub', "")), email=str(payload.get('email', "")))