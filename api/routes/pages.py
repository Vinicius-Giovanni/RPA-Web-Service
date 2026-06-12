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

router = APIRouter(tags=['pages'])
templates = Jinja2Templates(directory=str(get_settings()templates.frontend_dir))

@dataclass(frozen=True, slots=True)
class SectorPage:
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
    return templates.TemplateResponse(request=request, name="index.html", context={})

@router.get('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request, current_user: dict[str, object] = Depends(get_current_user)) -> HTMLResponse:
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
    metrics = await sector_metrics_use_case.execute()
    user_name = await user_name_use_case.execute(str(current_user.get("sub", "")))
    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context=_base_context(current_user, user_name, metrics),
    )

def _base_context(current_user: dict[str, object], user_name: str, metrics: SectorMetrics) -> dict[str, object]:
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
