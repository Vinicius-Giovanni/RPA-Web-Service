from __future__ import annotations

from dataclasses import dataclass

"""
Entidades relacionadas ao domínio de setores.

Este módulo define as estruturas que representam as informações
de demanda operacional dos setores da empresa.

As entidades de domínio possuem o objetivo de encapsular dados
de negócio e servir como contrato entre as camadas da aplicação,
independentemente da tecnologia de persistência utilizada.
"""

@dataclass(frozen=True, slots=True)
class SectorDemand:
    """
    Representa a demanda operacional de um setor.

    Cada instância contém as informaçções necessárias para
    cálculo de indicadores, dashboards e métricas de operação.

    A entidade é imutável (fronze=True), garantindo que os
    dados de negócio não sejam alterados acidentalmente após
    sua crição.

    Attributes:
        name:
            Nome do setor.
        
        demand:
            Quantidade de demanda pendente ou em processamento
            no setor.
        
            peoples:
                Quantidade de pessoas alocadas no setor.
            
            raw:
                Dados originais recebidos da fonte de dados,
                preservados para auditoria, depuração ou futuras
                necessidades de processamento.
    """
    name: str
    demand: int
    peoples: int
    raw: dict[str, object]