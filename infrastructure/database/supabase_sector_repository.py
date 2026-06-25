from __future__ import annotations

from asyncio import to_thread

from domain.entities.sector import SectorDemand
from infrastructure.database.supabase_client import get_supabase_client

"""
Implementação do repositório de setores utilizando o Supabase.

Este módulo contém a implementação responsável por consultar
os dados persistidos na tabela de setores e convertê-los para
entidades do domínio da aplicação.

A comunicação com o banco de dados é realizada por meio do
cliente Supabase, enquanto a transformação dos dados é
responsabilidade deste repositório.
"""
class SupabaseSectorRepository:
    """
    Repositório responsável pelo acesso aos dados de demanda
    dos setores no Supabase.

    Esta implementação encapsula as operações de leitura da
    tabela de setores e realiza o mapeamento dos registros
    retornados para entidades de domínio.
    """
    async def list_demands(self) -> list [SectorDemand]:
        """
        Obtém a lista de demandas dos setores armazenadas
        no banco de dados.

        Os registros recuperados da tabela ``sectors`` são
        convertidos em instância da entidade
        ``SectorDemand``.

        A operação de acesso ao banco é executada em uma
        thread separada para evitar o bloqueio do loop de
        eentos da aplicação assíncrona.

        Returns:
            list[SectorDemand]:
                Lista contendo as demandas de cada setor
                recuperados do banco de dados.
        """
        def _select() -> list[SectorDemand]:
            """
            Executa a consulta à tabela de setores e realiza
            o mapeamento dos registros para entidades de domínio.

            Returns:
                list[SectorDemand]:
                    Lista de entidades representando as demandas dos setores.
            """
            response = get_supabase_client().table("sectors").select("*").execute()
            sectors: list[SectorDemand] = []
            for item in response.data or []:
                sectors.append(
                    SectorDemand(
                        name=str(item.get("name") or item.get("sector") or ""),
                        demand=int(item.get("demand") or 0),
                        peoples=int(item.get("peoples") or 0),
                        raw=dict(item),
                    )
                )
            
            return sectors
        
        return await to_thread(_select)