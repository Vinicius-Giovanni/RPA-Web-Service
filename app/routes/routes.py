from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auth.auth_middleware import get_current_user
from app.services.user_service import name_user_auth
from app.services.sector_service import demand_sector

router = APIRouter()
templates = Jinja2Templates(directory='frontend/templates')

# Rota index
@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    """
    Renderiza a página de index

    Args:
        request (Request): requisição HTTP.
    Returns:
        HTMLReponse: página index.html renderizada.
    """
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={
        }
    )

# Rota Dashboard
@router.get('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request,
                    current_user: dict = Depends(get_current_user)):
    """
    Renderiza a página de dashboard
    """
    return templates.TemplateResponse(
        name="dashboard.html",
        request=request,
        context={
            'user_email': current_user['email']
            }
    )

# Rota landpange
@router.get('/landpage', response_class=HTMLResponse)
async def landpage(request: Request, 
                   current_user: dict = Depends(get_current_user),
                   user_name: str = Depends(name_user_auth)):
    
    sectors, t_dem, t_peo = await demand_sector()

    return templates.TemplateResponse(
        name="landpage.html",
        request=request,
        context={
            'user_email': current_user['email'],
            'user_name': user_name,
            'sectors': sectors,
            't_dem': t_dem,
            't_peo': t_peo
        }
    )

# Rota abastecimento
@router.get('/abastecimento', response_class=HTMLResponse)
async def landpage(request: Request, 
                   current_user: dict = Depends(get_current_user),
                   user_name: str = Depends(name_user_auth)):
    
    sectors = await demand_sector()

    return templates.TemplateResponse(
        name="setor_abastecimento.html",
        request=request,
        context={
            'user_email': current_user['email'],
            'user_name': user_name,
            'sectors': sectors,
        }
    )

@router.get('/online', response_class=HTMLResponse)
async def landpage(request: Request, 
                   current_user: dict = Depends(get_current_user),
                   user_name: str = Depends(name_user_auth)):
    
    sectors = await demand_sector()

    return templates.TemplateResponse(
        name="setor_online.html",
        request=request,
        context={
            'user_email': current_user['email'],
            'user_name': user_name,
            'sectors': sectors,
        }
    )

@router.get('/pesados', response_class=HTMLResponse)
async def landpage(request: Request, 
                   current_user: dict = Depends(get_current_user),
                   user_name: str = Depends(name_user_auth)):
    
    sectors = await demand_sector()

    return templates.TemplateResponse(
        name="setor_pesados.html",
        request=request,
        context={
            'user_email': current_user['email'],
            'user_name': user_name,
            'sectors': sectors,
        }
    )

@router.get('/par', response_class=HTMLResponse)
async def landpage(request: Request, 
                   current_user: dict = Depends(get_current_user),
                   user_name: str = Depends(name_user_auth)):
    
    sectors = await demand_sector()

    return templates.TemplateResponse(
        name="setor_par.html",
        request=request,
        context={
            'user_email': current_user['email'],
            'user_name': user_name,
            'sectors': sectors,
        }
    )

@router.get('/1200-outbound', response_class=HTMLResponse)
async def landpage(request: Request, 
                   current_user: dict = Depends(get_current_user),
                   user_name: str = Depends(name_user_auth)):
    
    sectors = await demand_sector()

    return templates.TemplateResponse(
        name="1200_outbound.html",
        request=request,
        context={
            'user_email': current_user['email'],
            'user_name': user_name,
            'sectors': sectors,
        }
    )

@router.get('/1200-inbound', response_class=HTMLResponse)
async def landpage(request: Request, 
                   current_user: dict = Depends(get_current_user),
                   user_name: str = Depends(name_user_auth)):
    
    sectors = await demand_sector()

    return templates.TemplateResponse(
        name="1200_inbound.html",
        request=request,
        context={
            'user_email': current_user['email'],
            'user_name': user_name,
            'sectors': sectors,
        }
    )

@router.get('/recebimento', response_class=HTMLResponse)
async def landpage(request: Request, 
                   current_user: dict = Depends(get_current_user),
                   user_name: str = Depends(name_user_auth)):
    
    sectors = await demand_sector()

    return templates.TemplateResponse(
        name="setor_recebimento.html",
        request=request,
        context={
            'user_email': current_user['email'],
            'user_name': user_name,
            'sectors': sectors,
        }
    )

@router.get('/retorno', response_class=HTMLResponse)
async def landpage(request: Request, 
                   current_user: dict = Depends(get_current_user),
                   user_name: str = Depends(name_user_auth)):
    
    sectors = await demand_sector()

    return templates.TemplateResponse(
        name="setor_retorno.html",
        request=request,
        context={
            'user_email': current_user['email'],
            'user_name': user_name,
            'sectors': sectors,
        }
    )

@router.get('/rpa', response_class=HTMLResponse)
async def landpage(request: Request, 
                   current_user: dict = Depends(get_current_user),
                   user_name: str = Depends(name_user_auth)):

    return templates.TemplateResponse(
        name="rpa.html",
        request=request,
        context={
            'user_email': current_user['email'],
            'user_name': user_name,
        }
    )