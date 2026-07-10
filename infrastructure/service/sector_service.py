from __future__ import annotations

from api.dependencies.repositories import get_sector_repository
from app.use_cases.get_sector_metrics import GetSectorMetricsUseCase
from domain.services.sector_metrics import SectorMetricsService

"""
Serviços auxiliares relacionados aos indicadores dos setores.

Este módule encapsula chamadas aos casos de uso responsáveis
pela obtenção e consolidação das métricas operacionais dos setores.

Seu objetivo é simplificar o acesso às informações agregadas
quando utilizadas por templates, componentes ou outras camadas
da aplicação.
"""

async def demand_sector() -> tuple[list[dict[str, object]], int, int]:
    """
    Recupera as métricas consolidadas dos setores.

    Internamente, a função instancia o caso de uso responsável
    pela geração das métricas e retorna apenas os dados
    necessários para consumo pela camada de apresentação.

    Dados retornados:

    - Lista de setores com seus indicadores.
    - Total consolidado de demanda.
    - Total consolidado das pessoas.

    Returns:
        tuple[list[dict[str, object]], int, int]:
            tlupa contendo:

            - Lista de métricas dos setores.
            - Total de demanda.
            - Total de pessoas.

    """
    use_case = GetSectorMetricsUseCase(get_sector_repository(), SectorMetricsService())
    metrics = await use_case.execute()
    return metrics.sectors, metrics.total_demand, metrics.total_people