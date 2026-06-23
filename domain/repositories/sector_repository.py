from __future__ import annotations

from typing import Protocol

from domain.entities.sector import SectorDemand

"""
Contratos de acesso aos dados de setores.

Este módulo define as interfaces utilizadas pela camada de
domínio para obtenção de informações relacionadas às demandas
dos setores.

As implementações concretas deste contrato pertencem à camada
de infraestrutura, permitindo que o domínio permaneça
desacoplado de tecnologias específicas de persistência.
"""

class SectorRepository(Protocol):
    """
    Contrato para acesso às informações de demanda dos setores.

    Esta interface define as operações necessárias para obtenção
    dos dados utilizados pelos casos de uso e servições de domínio.

    Implementações possíveis:
    - Supabase
    - PostgreSQL
    - API Externa
    - Arquivos CSV
    - Dados Mockados para testes

    O domínio depende apenas deste contrato, e não de implementações concretas.
    """
    async def list_demands(self) -> list[SectorDemand]: ...
    """
    Obtém a lista de demandas dos setores.

    Returns:
        list[SectorDemand]:
            Coleção contento as demandas de todos os setores
            disponíveis na fonte de dados.
    """