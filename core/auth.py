from fastapi import Request, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from .database import SUPABASE_JWT

async def auth_middleware(request:Request, call_next):
    """
    Se existir cookie 'access_token', injeta Authorizarion no scope ASGI.
    Isso permite reuso do dependency HTTPBearer sem mutar objetos internos privados.
    """
    token = request.cookies.get('access_token')
    has_auth_header = 'authorization' in request.headers

    if token and token.startswith('Bearer ') and not has_auth_header:
        scope_headers = list(request.scope.get('headers', []))
        scope_headers.append((b'authorization', token.encode()))
        request.scope['headers'] = scope_headers

    response = await call_next(request)
    return response

def get_current_user(request: Request):

    token = request.cookies.get('access_token')

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Cookies not authenticated'
        )

    try:

        payload = jwt.decode(
            token,
            SUPABASE_JWT,
            algorithms=['HS256'],
            options={'verify_aud': False}
        )

        user_id = payload.get('sub')

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid auth creds'
            )
        
        return payload
    
    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token has expired'
        )

    except jwt.PyJWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )