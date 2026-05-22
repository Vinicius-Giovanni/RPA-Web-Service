from fastapi import APIRouter, Request, Depends, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.auth import get_current_user
from core.forms import as_form
from core.database import supabase, SUPABASE_URL, SUPABASE_KEY

router = APIRouter()
templates = Jinja2Templates(directory='frontend/templates')

# Rota index
@router.get('/', response_class=HTMLResponse)
async def index(request: Request, current_user: dict = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={}
    )

# Rota Dashboard
@router.get('/dashboard', response_class=HTMLResponse)
async def read_users(request: Request):
    response = supabase.table('user_table').select("full_name").execute()
    users = response.data
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request,
         "users": users}
    )
