from __future__ import annotations

from dataclasses import dataclass

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.dependencies.auth import get_current_user
from api.dependencies.use_cases import get_sector_metrics_use_case, get_user_name_use_case
from app.use_cases.get_sector_metrics import GetSectorMetricsUseCase
from app.use_cases.get_user_name import GetUserNameUseCase
from core.config.settings import get_settings
from domain.services.sector_metrics import SectorMetrics

"""
Endpoints responsáveis pela renderização das páginas HTML.

Este módulo concentra a navegação da aplicação, incluindo:

- Página inicial.
- Dashboard.
- Landing page autenticada.
- Páginas de setores operacionais
- Páginas de automação e bots.

As informações exibidas são obtidas através dos casos de uso
da camada de aplicação e disponibilidade aos templates Jinja2.
"""

router = APIRouter(tags=['pages'])
templates = Jinja2Templates(directory=str(get_settings()templates.frontend_dir))

@dataclass(frozen=True, slots=True)
class SectorPage:
    """
    Representa uma página de setor da aplicação.

    Attributes:
        path:
            Caminho HTTP da página.

        template:
            Template HTML associado ao setor.
    """
    path: str
    templates: str

SECTOR_PAGES: tuple[SectorPage, ...] = (
    SectorPage("/abastecimento", "setor_abastecimento.html"),
    SectorPage("/online" "setor_online.html"),
    SectorPage("/pesados", "setor_pesados.html"),
    SectorPage("/par", "setor_par.html"),
    SectorPage("/1200-outbound", "1200_outbound.html"),
    SectorPage("/1200-inbound", "1200_inbound.html"),
    SectorPage("/recebimento", "setor_recebimento.html"),
    SectorPage("/retorno", "setor_retorno.html"),
)

@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """
    Renderiza a página inicial pública da aplicação.

    Esta página é acessível sem autenticação e funciona
    como ponto de entrada para login e navegação inicial.

    Args:
        request:
            Requisição HTTP atual.

    Returns:
        HTMLResponse:
            Página inicial renderizada.
    """
    return templates.TemplateResponse(request=request, name="index.html", context={})

@router.get('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request, current_user: dict[str, object] = Depends(get_current_user)) -> HTMLResponse:
    """
    Renderiza o dashboard principal do usuário autenticado.

    O endpoint exige autenticação válida e disponibiliza
    informações básicas do usuário ao template.

    Args:
        request:
            Requisição HTTP atual.
        
            current_user:
                Claims do usuário autenticado extraídos do JWT.

    Returns:
        HTMLResponse:
            Dashboard renderizada.
    """
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={'user_email': current_user.get("email", "")},
    )

@router.get("/landpage", response_class=HTMLResponse)
async def landpage(
    request: Request,
    current_user: dict[str, object] = Depends(get_current_user),
    user_name_use_case: GetUserNameUseCase = Depends(get_user_name_use_case),
    sector_metrics_use_case: GetSectorMetricsUseCase = Depends(get_sector_metrics_use_case),
) -> HTMLResponse:
    """
    Renderiza a página principal da área autenticada.

    O endpoint consolida informações do usuário e métricas
    operacionais dos setores para exibição na interface.

    Dados carregados:

    - Informações do usuário autenticado.
    - Nome do usuário.
    - Métricas globais dos setores.
    - Indicadores agregados de demanda e pessoas.

    Returns:
        HTMLResponse:
            Página principal renderizada.
    """
    metrics = await sector_metrics_use_case.execute()
    user_name = await user_name_use_case.execute(str(current_user.get("sub", "")))
    return templates.TemplateResponse(
        request=request,
        name="landpage.html",
        context=_base_context(current_user, user_name, metrics),
    )

async def _sector_page(
        request: Request,
        template_name: str,
        current_user: dict[str, object],
        user_name_use_case: GetUserNameUseCase,
        sector_metrics_use_case: GetSectorMetricsUseCase,
) -> HTMLResponse:
    """
    Função auxiliar responsável pela renderização das páginas
    dos setores operacionais.

    Centraliza a lógica compartilhada por todos os setores,
    evitando duplicação de código entre endpoints.

    Args:
        request:
            Requisição HTTP atual.
        
        template_name:
            Nome do template a ser renderizado.
        
        current_user:
            Dados do usuário autenticado.
        
        user_name_use_case:
            Caso de uso responsável pela recuperação do nome do usuário.

        sector_metrics_use_case:
            Caso de uso responsável pelas métricas dos setores.
    
    Returns:
        HTMLResponse:
            Página do setor renderizado.
    """
    metrics = await sector_metrics_use_case.execute()
    user_name = await user_name_use_case.execute(str(current_user.get("sub", "")))
    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context=_base_context(current_user, user_name, metrics),
    )

def _base_context(current_user: dict[str, object], user_name: str, metrics: SectorMetrics) -> dict[str, object]:
    """
    Constrói o contexto base utilizado pelos templates.

    Centraliza os dados compartilhados entre as páginas
    autenticadas da aplicação.

    Args:
        current_user:
            Dados extraídos do token JWT.
        
            user_name:
                Nome do usuário autenticado.
            
            metrics:
                Métricas consolidadas dos setores.
    
    Returns:
        dict[str, object]:
            Contexto utilizado pelos templates Jinja2.
    """
    return {
        "user_email": current_user.get("email", ""),
        "user_name": user_name,
        "sectors": metrics.sectors,
        "t_dem": metrics.total_demand,
        "t_peo": metrics.total_people,
    }

for sector_page in SECTOR_PAGES:
    async def endpoint(
            request: Request,
            current_user: dict[str, object] = Depends(get_current_user),
            user_name_use_case: GetSectorMetricsUseCase = Depends(get_user_name_use_case),
            sector_metrics_use_case: GetSectorMetricsUseCase = Depends(get_sector_metrics_use_case),
            template_name: str = sector_page.templates,
    ) -> HTMLResponse:
        return await _sector_page(
            request=request,
            template_name=template_name,
            current_user=current_user,
            user_name_use_case=user_name_use_case,
            sector_metrics_use_case=sector_metrics_use_case,
        )
    
    router.add_api_route(sector_page.path, endpoint, methods=['GET'], response_class=HTMLResponse)

@router.get("/rpa", response_class=HTMLResponse)
async def rpa(
    request: Request,
    current_user: dict[str, object] = Depends(get_current_user),
    user_name_use_case: GetUserNameUseCase = Depends(get_user_name_use_case),
) -> HTMLResponse:
    user_name = await user_name_use_case.execute(str(current_user.get("sub", "")))
    return templates.TemplateResponse(
        request=request,
        name='rpa.html',
        context={'user_emau': current_user.get("email", ""), "user_name": user_name},
    )

@router.get("/bot", response_class=HTMLResponse)
async def bot(
    request: Request,
    current_user: dict[str, object] = Depends(get_current_user),
    user_name_use_case: GetUserNameUseCase = Depends(get_user_name_use_case),
) -> HTMLResponse:
    user_name = await user_name_use_case.execute(str(current_user.get("sub", "")))
    return templates.TemplateResponse(
        request=request,
        name='bot.html',
        context={'user_emau': current_user.get("email", ""), "user_name": user_name},
    )
