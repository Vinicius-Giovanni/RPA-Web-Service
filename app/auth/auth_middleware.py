from fastapi import Request, HTTPException, status
import jwt
from jwt import PyJWKClient

from core.database import SUPABASE_URL,SUPABASE_JWKS_URL

jwks_client = PyJWKClient(SUPABASE_URL+SUPABASE_JWKS_URL)

def get_current_user(request: Request):

    token = request.cookies.get('access_token')

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:

        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256"],
            options={"verify_aud": False}  # Desabilita a verificação de audiência
        )

        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")