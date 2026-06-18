from __future__ import annotations

from domain.repositories.sector_repository import SectorRepository
from domain.services.sector_metrics import SectorMetrics, SectorMetricsService

"""
Caso de uso responsávei pela obtenção das métricas dos setores.

Este módulo coordena a recuperação dos dados operacionais e
a aplicação das regras de negócio necessárias para geração
dos indicadores consolidados da operação.

A responsabilidade do cálculo permanece na camada de domínio,
através do serviço SectorMetricsService


"""
class GetSectorMetricsUseCase:
    """
    Recupera e consolida métricas dos setores operacionais.

    Este caso de uso atua como orquestrador entre a camada
    de persistência e a camada de domínio.

    Fluxo executado:
    1. Recupera os dados dos setores através do repositório.
    2. Encaminha os dados para o serviço de domínio.
    3. Obtém as métricas calculadas.
    4. Retorna os indicadores consolidados.

    Attributes:
        sector_repository:
            Repositório responsável pela consulta dos dados
            dos setores.

        metrics_service:
            Serviço de domínio responsável pelo cálculo
            das métricas operacionais.
    """
    def __init__(self, sector_repository: SectorRepository, metrics_service: SectorMetricsService):
        self.sector_repository = sector_repository
        self.metrics_service = metrics_service

    async def execute(self) -> SectorMetrics:
        """
        Recupera e calcula as métricas dos setores.

        Os dados operacionais são obtidos através do repositório
        e processados pelo serviço de domínio responsável pelos
        cálculos e consolidações.

        Returns:
            SectorMetrics:
                Objeto contendo as métricas consolidadas da
                operação, incluindo indicadores por setor e
                totais agregados.
        """
        sectors = await self.sector_repository.list_demands()
        return self.metrics_service.calculate(sectors)
        