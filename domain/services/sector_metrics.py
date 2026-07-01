from __future__ import annotations

from dataclasses import dataclass

from domain.entities.sector import SectorDemand

"""
Serviços de domínio relacionados às métricas dos setores.

Este módulo contém os componentes responsáveis por calcular
indicadores consolidados a partir das demandas dos setores.

As regras implementadas aqui pertencem ao domínio da aplicação
e são independentes de frameworks, banco de dados ou mecanismos
de apresentação.
"""

@dataclass(frozen=True, slots=True)
class SectorMetrics:
    """
    Representa o resultado consolidado das métricas dos setores

    Esta entidade é utilizada para transportar informações
    agregadas calculadas pelo serviço de domínio.

    Attributes:
        sectors:
            Lista contendo os dados brutos de cada setor.
        
        total_demand:
            Soma total das demandas de todos os setores.

        total_people:
            Soma total de pessoas alocadas em todos os setores.
            
    """
    sectors: list[dict[str, object]]
    total_demand: int
    total_people: int

class SectorMetricsService:
    """
    Serviço do domínio responsável pelo cálculo das métricas
    operacionais dos setores.

    Este serviço encapsula regras de agregação e consolidação
    dos dados provenienentes das entidades de domínio.
    """
    def calculate(self, sectors: list[SectorDemand]) -> SectorMetrics:
        """
        Calcula métricas consolidadas dos setores.

        As métricas calculadas incluenm:

        - Lista de dados brutos dos setores;
        - Total de demandas;
        - Total de pessoas.

        Args:
            sectors:
                Lista de entidades contendo as informações de cada
                setor.
        
        Returns:
            SectorMetrics:
                Objeto contendo os indicadores consolidados.
        """
        return SectorMetrics(
            sectors=[sector.raw for sector in sectors],
            total_demand=sum(sector.demand for sector in sectors),
            total_people=sum(sectors.peoples for sectors in sectors),
        )