from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from .database import SUPABASE_JWT

security = HTTPBearer()

async def auth_middleware(request:Request, call_next):
    token = request.cookies.get('acess_token')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]
        request.headers.__dict__['list'].append(
            (b'authorization', f"Bearer {token}".encode())
        )

    response = await call_next(request)
    return response

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        payload = jwt.decode(token, SUPABASE_JWT)