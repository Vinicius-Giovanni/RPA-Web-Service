from fastapi import APIRouter, Request, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from core.forms import as_form
from core.database import supabase, SUPABASE_URL, SUPABASE_KEY
from core.models import RegisterUser

# STATIC
#routes.mount('/static', StaticFiles(directory='frontend/static'), name='static')

router = APIRouter()
templates = Jinja2Templates(directory='frontend/templates')

# Rota index
@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={}
    )

# Rota Login x Cadastro
@router.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='login.html',
        context={}
    )

@router.get('/cadastro', response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='register.html',
        context={}
    )

@router.post('/cadastro')
async def register_user(
    request: Request,
    users: RegisterUser = Depends(RegisterUser.as_form)
):
    supabase.table('user_table').insert({
        'full_name': users.full_name,
        'email': users.email,
    }).execute()

    return RedirectResponse(url='/login', status_code=303)

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
