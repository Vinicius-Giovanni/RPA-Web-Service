
from core.database import supabase
from fastapi import Depends

from app.auth.auth_middleware import get_current_user

# Extração de nome do usuário logado

async def name_user_auth(current_user: dict = Depends(get_current_user)):
    user_data = supabase.table('user_table').select('full_name').eq('id', current_user['sub']).single().execute()

    full_name = user_data.data['full_name']

    return full_name